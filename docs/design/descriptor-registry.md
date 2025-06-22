# Descriptor Registries for Interaction Affordances

Descriptor Registries keep track of the available interaction affordances for a given class or instance, allowing for dynamic introspection with the `Thing`'s capabilities. 
The purpose can be summarized as:

- add and remove affordances in runtime
- find by name or check their existence
- iterate and introspect affordances
- implement group operations on affordances (`readMultipleProperties`, `writeMultipleProperties`, `readAllProperties`, `writeAllProperties`)

[Current Implementations](../UML/PDF/DescriptorRegistry.pdf) are:

- `PropertyRegistry` for managing property descriptors
- `ActionRegistry` for managing action descriptors
- `EventRegistry` for managing event descriptors

### Find by Name/Check Existence

Lets say a serial device supports an optional list of supported commands. The presence or absence of this property could indicate whether such a list is available or not.

```python
class SerialUtility(Thing):

    @action()
    def execute(self, command: str, expected_return_data_size: int = 0) -> Any:
        """Execute a command on the serial device."""
        if (
            'instructions' in self.properties and \
            command not in self.properties["instructions"]
        ):
            raise RuntimeError(f"command {command} not a valid command.")
        # Implementation of command execution
        return result

    @action()
    def add_command(self, command: str) -> None:
        """Add a command to the list of supported commands."""
        if 'instructions' not in self.properties:
            self.properties.add(
                'instructions',
                List(default=None, item_type=str, doc="List of supported commands")
            )
        self.properties['instructions'].append(command)
        # or self.instructions.append(command)
```

Of course, one could use an empty list instead of having a dynamic property. 
This is a contrived example, but the affordance registry can be used to check for the existence of a property or action.

### Iterate and Introspect Affordances

Lets say you have overloaded a getter of a composite property that returns a group of properties' values:

```python
class Spectrometer(Thing):

    settings = Property(
        default=None,
        readonly=True,
        model=..., # please use a decent JSON schema or pydantic model here
        doc="Settings of the spectrometer, including integration time, trigger mode etc."
    )
    
    @settings.getter
    def read_settings(self, **kwargs) -> None:
        setting_props = dict()
        for name in [
            "integration_time", "trigger_mode", "pixel_count", 
            "nonlinearity_correction", "background_subtraction"
        ]:
            if name in self.properties:
                setting_props[name] = dict(
                    current_value=self.properties[name].__get__(),
                    default=self.properties[name].default,
                    nullable=self.properties[name].allow_None,
                )
        return setting_props
```

One could also alter the metadata of interaction affordances as an administrative task. For example, one could make an action inaccessible or make a property read-only 
even if the setter is defined. 

```python
class Spectrometer(Thing):

    @action()
    def freeze_important_settings(self) -> None:
        """Calibrate the spectrometer at a specific wavelength."""
        self.properties['background_correction'].readonly = True
        self.properties['nonlinearity_correction'].readonly = True
        self.properties['trigger_mode'].readonly = True
        self._inaccessible_actions["send_raw_command"] = self.actions.pop("send_raw_command")
        # remove from descriptor registry to make actions inaccessible

    integration_time = Number(default=1000, bounds=(0.001, None), crop_to_bounds=True,
                        doc="integration time of measurement in milliseconds") # type: float
    # can be set to readonly even if not originally defined as such

    trigger_mode = Selector(objects=[0, 1, 2, 3, 4], default=0, observable=True,
                        doc="""0 = normal/free running, 1 = Software trigger, 
                        2 = Ext. Trigger Level, 3 = Ext. Trigger Synchro/ Shutter mode, 
                        4 = Ext. Trigger Edge""") # type: int
    
    @trigger_mode.setter 
    def apply_trigger_mode(self, value : int):
        self.device.trigger_mode(value)
        
    @trigger_mode.getter 
    def get_trigger_mode(self):
        return self.device.trigger_mode()
        # can be set to readonly even if the setter is defined

    @action()
    def unfreeze_important_settings(self) -> None:
        """Unfreeze the important settings."""
        ...
```

Of course, such administrative tasks needs to be wrapped in a security definition to prevent unauthorized execution.

### Implement Group Operations

One could iterate through all the available interactions to perform group operations. WoT operations on multiple properties are implemented as follows:

=== "`readMultipleProperties`/`readAllProperties`"

    ```python
    class PropertyRegistry(DescriptorRegistry):
        
        def get(self, **kwargs: typing.Dict[str, typing.Any]) -> typing.Dict[str, typing.Any]:
            """
            read properties from the object, implements WoT operations `readAllProperties` and `readMultipleProperties`
            
            Parameters
            ----------
            **kwargs: typing.Dict[str, typing.Any]
                - names: `List[str]`
                    list of property names to be fetched
                - name: `str`
                    name of the property to be fetched, along with a 'rename' for the property in the response.
                    For example { 'foo_prop' : 'fooProp' } will return the property 'foo_prop' as 'fooProp' in the response.
            """
            data = {}
            if len(kwargs) == 0:
                # read all properties
                for name, prop in self.remote_objects.items():
                    if self.owner_inst is None and not prop.class_member:
                        continue
                    data[name] = prop.__get__(self.owner_inst, self.owner_cls)
                return data
            elif 'names' in kwargs:
                # read multiple properties whose names are specified
                names = kwargs.get('names')
                if not isinstance(names, (list, tuple, str)):
                    raise TypeError("Specify properties to be fetched as a list, tuple or comma separated names. " + 
                                    f"Given type {type(names)}")
                if isinstance(names, str):
                    names = names.split(',')
                kwargs = {name: name for name in names}
            for requested_prop, rename in kwargs.items():
                if not isinstance(requested_prop, str):
                    raise TypeError(f"property name must be a string. Given type {type(requested_prop)}")
                if not isinstance(rename, str):
                    raise TypeError(f"requested new name must be a string. Given type {type(rename)}")
                if requested_prop not in self.descriptors:
                    raise AttributeError(f"property {requested_prop} does not exist")
                if requested_prop not in self.remote_objects:
                    raise AttributeError(f"property {requested_prop} is not remote accessible")
                prop = self.descriptors[requested_prop]
                if self.owner_inst is None and not prop.class_member:
                    continue
                data[rename] = prop.__get__(self.owner_inst, self.owner_cls)                   
            return data 
    ```

=== "`writeMultipleProperties`/`writeAllProperties`"

    ```python
    class PropertyRegistry(DescriptorRegistry):
        
        def set(self, **values : typing.Dict[str, typing.Any]) -> None:
            """ 
            set properties whose name is specified by keys of a dictionary; implements WoT operations `writeMultipleProperties`
            or `writeAllProperties`. 
            
            Parameters
            ----------
            values: typing.Dict[str, typing.Any]
                dictionary of property names and its new values
            
            Raises
            ------
            AttributeError
                if property does not exist or is not remote accessible
            RuntimeError
                if some properties could not be set due to errors, 
                check exception notes or server logs for more information
            """
            errors = ''
            for name, value in values.items():
                try:
                    if name not in self.descriptors:
                        raise AttributeError(f"property {name} does not exist")
                    if name not in self.remote_objects:
                        raise AttributeError(f"property {name} is not remote accessible")
                    prop = self.descriptors[name]
                    if self.owner_inst is None and not prop.class_member:
                        raise AttributeError(f"property {name} is not a class member and cannot be set at class level")
                    setattr(self.owner, name, value)
                except Exception as ex:
                    errors += f'{name}: {str(ex)}\n'
            if errors:
                ex = RuntimeError("Some properties could not be set due to errors. " + 
                                "Check exception notes or server logs for more information.")
                ex.__notes__ = errors
                raise ex from None
    ```




