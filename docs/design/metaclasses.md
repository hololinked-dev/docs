# Metaclasses

The `Metaclass` allow customization of `Thing` subclass creation. One possible application could include enforcing certain behaviors across multiple `Thing` classes for grouping class definition for same hardware types.

Default metaclass implements:

- creation of descriptor registries at class level (so that registries can also be used without instances)
- `__post_init__` method to allow for code that should run post initialization of the class

Subclassing metaclasses can implement:

- mandate existence of certain properties, actions, or events according to the hardware type; also constrain the type of the properties, payload schema of actions, or events
- default code to run when a `Thing` class is created


## Enforce Existence of Properties, Actions, and Events according to Hardware Type


For example, lets say you have 3 different cameras, all of which need to have an image property of a specific custom implemented `Image` type, 
an image capture event. In the metaclass, one can assert this:

```python
class CameraMeta(type):

    def __call__(mcls, *args, **kwargs):
        cls = super().__call__(*args, **kwargs)
        mcls.validate_interactions(cls)
        mcls.setup(cls)
        return cls

    def validate_interactions(mcls, cls):
        if 'image' not in cls.properties and not isinstance(cls.image, Image):
            raise TypeError("Camera must have an 'image' property of type 'Image'")
        if 'image_captured_event' not in cls.events and \
            not isinstance(cls.image_captured_event, Event):
            raise TypeError("Camera must have an 'image_captured_event' of type 'Event'")

    def setup(mcls, cls):
        """Add code that should run after a class is created"""
        ...

class Image(Property):

    def __init__(self, 
                compression_ratio: int = 1, 
                transpose: bool = False, 
                flip_horizontal: bool = False, 
                flip_vertical: bool = False,
                observable: bool = False,
            ) -> None:
        ...

class RPiCamera(Thing, metaclass=CameraMeta):
    # raises TypeError
    image = String(observable=True, doc="Captured image from the camera")
    
class BaslerCamera(Thing, metaclass=CameraMeta):
    # OK
    image = Image(observable=True, doc="Captured image from the camera")

class IDSCamera(Thing, metaclass=CameraMeta):
    # OK
    image = Image(observable=True, doc="Captured image from the camera")
```

## `__post_init__` Method

There is no specific need to explicitly call a `__post_init__` method. A possible application of `__post_init__` could be to run default code after connecting to the hardware:

```python

class Camera(Thing):

    def __init__(self, serial_number: str = None):
        super().__init__()
        self.connect()

    def __post_init__(self):
        """
        This method is called after properties are initialized 
        from a database or configuration file.
        """
        self.setup_image_processing()
```

This is especially useful when there is a configuration management system in place, where properties are stored and loaded from a file or a database, and then applied onto the connected device when the server or `Thing` reboots. This can persist the a device's settings that are modelled as properties.

```mermaid
flowchart TD
    A[Instance is created <br/> __init__() is called] --> B[Device is connected by the user]
    B --> C[Configuration properties are loaded from file or database]
    C --> D[Properties are applied onto the connected device]
    D --> E[__post_init__() is called to run additional setup code]
```

Of course, the `__post__init__` method can be used for any other purpose.