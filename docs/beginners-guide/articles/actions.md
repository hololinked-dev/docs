# Actions

[API Reference](../../api-reference/action/index.md)

Only methods decorated with `action()` are exposed to clients.

```py title="Actions" linenums="1" hl_lines="5 10 15 16 21 25"
--8<-- "docs/beginners-guide/code/thing_example_2.py:189:192"
--8<-- "docs/beginners-guide/code/thing_example_2.py:431:445"
--8<-- "docs/beginners-guide/code/thing_example_2.py:643:646"
--8<-- "docs/beginners-guide/code/thing_example_2.py:542:546"
```

## Payload Validation

If arguments are loosely typed, the action will be invoked with given payload without any validation. One may validate them manually inside the method. However, one can also specify the expected argument schema using either `JSON Schema` or `pydantic` models:

<a id="actions-argument-schema"></a>
=== "JSON Schema"

    === "Single Argument"

        Specify the expected type of the argument (with or without name)

        ```py title="Input Schema" linenums="1" hl_lines="8"
        --8<-- "docs/beginners-guide/code/thing_example_2.py:189:192"
        --8<-- "docs/beginners-guide/code/thing_example_2.py:210:222"
        ```

        ???+ note "JSON schema seen in Thing Description"

            ```py
            GentecOpticalEnergyMeter.set_sensor_model.to_affordance().json()
            ```

            ```json
            {
                "description": "Set the attached sensor to the meter under control. Sensor should be defined as a class and added to the AllowedSensors dict.",
                "input": {
                    "type": "string",
                    "enum": ["QE25LP-S-MB", "QE12LP-S-MB-QED-D0"]
                },
                "synchronous": True
            }
            ```

    === "Multiple Arguments"

        Specify the argument names under the `properties` field with `type` as `object`.
        Names not found in the `properties` field can be subsumed under python spread operator `**kwargs` if necessary (dont set `additionalProperties` to `False` in that case).

        ```py title="Input Schema with Multiple Arguments" linenums="1" hl_lines="32"
        --8<-- "docs/beginners-guide/code/thing_example_3.py:57:85"
        --8<-- "docs/beginners-guide/code/thing_example_3.py:87:87"
        --8<-- "docs/beginners-guide/code/thing_example_3.py:213:226"
        --8<-- "docs/beginners-guide/code/thing_example_3.py:247:247"
        ```

        ???+ note "JSON schema seen in Thing Description"

            ```py
            Picoscope6000.set_channel.to_affordance().json()
            ```

            ```json
            {
                "description": "Set the parameter for a channel. https://www.picotech.com/download/manuals/picoscope-6000-series-a-api-programmers-guide.pdf",
                "input": {
                    "type": "object",
                    "properties": {
                        "channel": {"type": "string", "enum": ["A", "B", "C", "D"]},
                        "enabled": {"type": "boolean"},
                        "voltage_range": {
                            "type": "string",
                            "enum": [
                                "10mV",
                                "20mV",
                                "50mV",
                                "100mV",
                                "200mV",
                                "500mV",
                                "1V",
                                "2V",
                                "5V",
                                "10V",
                                "20V",
                                "50V",
                                "MAX_RANGES"
                            ]},
                        "offset": {"type": "number"},
                        "coupling": {"type": "string", "enum": ["AC", "DC"]},
                        "bw_limiter": {"type": "string", "enum": ["full", "20MHz"]}
                    }
                },
                "synchronous": True
            }
            ```

    === "Return Type"

        Specify return type under `output_schema` field:

        ```py title="With Return Type" linenums="1" hl_lines="38 39"
        --8<-- "docs/beginners-guide/code/thing_example_3.py:22:55"
        --8<-- "docs/beginners-guide/code/thing_example_3.py:87:87"
        --8<-- "docs/beginners-guide/code/thing_example_3.py:349:356"
        ```

        ???+ note "JSON schema seen in Thing Description"

            ```py
            Picoscope6000.get_analogue_offset.to_affordance().json()
            ```

            ```json
            {
                "description": "analogue offset for a voltage range and coupling",
                "synchronous": True,
                "input": {
                    "type": "object",
                    "properties": {
                        "voltage_range": {
                            "type": "string",
                            "enum": ["10mV",
                                "20mV",
                                "50mV",
                                "100mV",
                                "200mV",
                                "500mV",
                                "1V",
                                "2V",
                                "5V",
                                "10V",
                                "20V",
                                "50V",
                                "MAX_RANGES"
                            ]
                        },
                        "coupling": {"type": "string", "enum": ["AC", "DC"]}
                    }
                },
                "output": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {"type": "number"}
                },
            }
            ```

=== "pydantic"

    === "Single Argument"

        Type annotate the argument, either plainly or with `Annotated`. A pydantic model will be composed with the argument name as the field name and the type annotation as the field type:

        ```py title="Input Schema with Single Argument" linenums="1" hl_lines="7"
        from typing import Annotated

        class GentecOpticalEnergyMeter(Thing):

            @action()
            def start_acquisition(self,
                max_count: Annotated[int, Field(gt=0)]
            ) -> None:
                """
                Start acquisition of energy measurements.

                Parameters
                ----------
                max_count: int
                    maximum number of measurements to acquire before stopping automatically.
                """
        ```

        ???+ note "JSON schema seen in Thing Description"

            ```py
            GentecOpticalEnergyMeter.start_acquisition.to_affordance().json()
            ```

            ```json
            {
                "description": "Start acquisition of energy measurements. max_count: maximum number of measurements to acquire before stopping automatically.",
                "input": {
                    "properties": {
                        "max_count": {
                            "exclusiveMinimum": 0,
                            "type": "integer"
                        }
                    },
                    "required": ["max_count"],
                    "title": "start_acquisition_input",
                    "type": "object"
                },
                "synchronous": True
            }
            ```

    === "Multiple Arguments"

        Again, type annotate the arguments, either plainly or with `Annotated`:

        ```py title="Input Schema with Multiple Arguments"
        from typing import Literal

        class Picoscope6000(Thing):

            @action()
            def set_channel(
                self,
                channel: Literal["A", "B", "C", "D"],
                enabled: bool = True,
                v_range: Literal[
                    "10mV",
                    "20mV",
                    "50mV",
                    "100mV",
                    "200mV",
                    "500mV",
                    "1V",
                    "2V",
                    "5V",
                    "10V",
                    "20V",
                    "50V",
                    "MAX_RANGES",
                ] = "2V",
                offset: float = 0,
                coupling: Literal["AC", "DC"] = "DC_1M",
                bw_limiter: Literal["full", "20MHz"] = "full",
            ) -> None:
        ```

        ???+ note "JSON schema seen in Thing Description"

            ```py
            Picoscope6000.set_channel.to_affordance().json()
            ```

            ```json
            {
                "description": "Set the parameter for a channel. https://www.picotech.com/download/manuals/picoscope-6000-series-a-api-programmers-guide.pdf",
                "input": {
                    "properties": {
                        "channel": {
                            "enum": ["A", "B", "C", "D"],
                            "type": "string"
                        },
                        "enabled": {"default": True, "type": "boolean"},
                        "v_range": {
                            "default": "2V",
                            "enum": [
                                "10mV",
                                "20mV",
                                "50mV",
                                "100mV",
                                "200mV",
                                "500mV",
                                "1V",
                                "2V",
                                "5V",
                                "10V",
                                "20V",
                                "50V",
                                "MAX_RANGES"
                            ],

                            "type": "string"
                        },
                        "offset": {"default": 0, "type": "number"},
                        "coupling": {
                            "default": "DC_1M",
                            "enum": ["AC", "DC"],
                            "type": "string"
                        },
                        "bw_limiter": {
                            "default": "full",
                            "enum": ["full", "20MHz"],
                            "type": "string"
                        }
                    },
                    "required": ["channel"],
                    "type": "object"
                },
                "synchronous": True
            }
            ```

    === "Return Type"

        type annotate the return type:

        ```py
        from typing import Annotated
        from pydantic import Field

        class SerialUtility(Thing):

            @action()
            def execute_instruction(
                self, command: str, return_data_size: Annotated[int, Field(ge=0)] = 0
            ) -> str:
                """
                executes instruction given by the ASCII string parameter 'command'. If return data size is greater than 0, it reads the response and returns the response. Return Data Size - in bytes - 1 ASCII character = 1 Byte.
                """
        ```

        ???+ note "JSON schema seen in Thing Description"

            ```py
            SerialUtility.execute_instruction.to_affordance().json()
            ```

            ```json
            {
                "description": "executes instruction given by the ASCII string parameter 'command'. If return data size is greater than 0, it reads the response and returns the response. Return Data Size - in bytes - 1 ASCII character = 1 Byte.",
                "input": {
                    "properties": {
                        "command": {"type": "string"},
                        "return_data_size": {"default": 0, "minimum": 0, "type": "integer"}
                    },
                    "required": ["command"],
                    "type": "object"
                },
                "output": {"type": "string"},
                "synchronous": True
            }
            ```

    === "Supply Models Directly"

        If the composed models from the type annotations are not sufficient or contain errors, one may directly supply the models:

        ```py title="With Direct Models" linenums="1" hl_lines="3 7 22"
        from pydantic import BaseModel, field_validator

        class CommandModel(BaseModel):
            command: str
            return_data_size: int = Field(0, ge=0)

            @field_validator("command")
            def validate_command(cls, v):
                if not isinstance(v, str) or not v:
                    raise ValueError("Command must be a non-empty string")
                if command not in SerialUtility.supported_commands:
                    raise ValueError(f"Command {command} is not supported")
                return v

        class ResponseModel(BaseModel):
            response: str = Field(..., description="Response from the device")

        class SerialUtility(Thing):

            supported_commands = ["*IDN?", "MEAS:VOLT?", "MEAS:CURR?"]

            @action(input_schema=CommandModel, output_schema=ResponseModel)
            def execute_instruction(self, command: str, return_data_size: int = 0) -> str:
                """
                executes instruction given by the ASCII string parameter 'command'
                """
        ```

<!-- To enable this, set global attribute`allow_relaxed_schema_actions=True`. This setting is used especially when a schema is useful for validation of arguments but not available - not for methods with no arguments.

```py title="Relaxed or Unavailable Schema for Actions" linenums="1"
--8<-- "docs/beginners-guide/code/thing_example_2.py:168:172"
--8<-- "docs/beginners-guide/code/thing_example_2.py:558:559"
``` -->

It is always possible to custom validate the arguments after invoking the action:

```py title="Custom Validation" linenums="1"
--8<-- "docs/beginners-guide/code/actions/parameterized_function.py:3:3"
--8<-- "docs/beginners-guide/code/actions/parameterized_function.py:9:27"
```

<!-- The last and least preferred possibility is to use `ParameterizedFunction`:

```py title="Parameterized Function" linenums="1"
--8<-- "docs/beginners-guide/code/actions/parameterized_function.py:52:"
```

`ParameterizedFunction`(s) are classes that implement the `__call__` method and whose arguments are type defined using the same objects as properties. However, this type definition using `Property` object do not make these properties of the `Thing`. The implementation follows convention used by `param` where the
properties are termed as "parameters" (also hence the word "ParameterizedFunction").

The `__call__` method signature accepts its own self as the first argument,
followed by the `Thing` instance as the second argument and then the arguments supplied by the client. On the
client side, there is no difference between invoking a normal action and an action implemented as
`ParameterizedFunction`:

=== "server"

    ```py title="Custom Validation" linenums="1"
    --8<-- "docs/beginners-guide/code/actions/parameterized_function.py:38:44"
    ```

=== "client"

    ```py title="Custom Validation" linenums="1"
    --8<-- "docs/beginners-guide/code/actions/parameterized_function.py:30:36"
    ``` -->

## Threaded & Async Actions

Actions can be made asynchronous or threaded by setting the `synchronous` flag to `False`. For methods that are **not** `async`:

```py title="Threaded Actions" linenums="3"
class ServoMotor(Thing):

    @action(synchronous=False)
    def poll_device_state(self) -> str:
        """check device state, especially when it got stuck up"""
        ...

    @action(threaded=True) # exactly the same effect for sync methods
    def poll_device_state(self) -> str:
        """check device state, especially when it got stuck up"""
        ...
```

The return value is fetched and returned to the client. One could also start long running actions without fetching a return value,
(although it would be better in many cases to manually thread out a long running action):

```py title="Threaded Actions" linenums="3"
class DCPowerSupply(Thing):
    """A DC Power Supply from 0-30V"""

    @action(threaded=True)
    def monitor_over_voltage(self, period: float = 5):
        """background voltage monitor loop"""
        while True:
            voltage = self.measure_voltage()
            if voltage > self.over_voltage_threshold:
                self.over_voltage_event(
                    dict(
                        timestamp=datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        voltage=voltage
                    )
                )
            time.sleep(period)
    # The suitability of this example in a realistic use case is untested
```

For `async` actions:

```py title="Async Actions" linenums="3"
class DCPowerSupply(Thing):

    @action(create_task=True)
    # @action(synchronous=False) # exactly the same effect for async methods
    async def monitor_over_voltage(self, period: float = 5):
        """background monitor loop"""
        while True:
            voltage = await asyncio.get_running_loop().run_in_executor(
                            None, self.measure_voltage
                    )
            if voltage > self.over_voltage_threshold:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.over_voltage_event(
                    dict(
                        timestamp=timestamp,
                        voltage=voltage
                    )
                )
            await asyncio.sleep(period)
    # The suitability of this example in a realistic use case is untested
```

For long running actions that do not return, call them with `oneway` flag on the client, otherwise expect a `TimeoutError`:

```py
client.invoke_action("monitor_over_voltage", period=10, oneway=True)
```

## Thing Description Metadata

| field       | supported | description                                                                                                                     |
| ----------- | --------- | ------------------------------------------------------------------------------------------------------------------------------- |
| input       | ✓         | schema of the input payload (validation carried out)                                                                            |
| output      | ✓         | schema of the output payload (validation not carried out)                                                                       |
| safe        | ✓         | whether the action is safe to execute, only treated as a metadata                                                               |
| idempotent  | ✓         | whether the action is idempotent, `True` when the action is executable in all states of a state machine, otherwise `False`      |
| synchronous | ✓         | whether the action is synchronous, `False` for threaded actions and async actions which are scheduled in the running event loop |
