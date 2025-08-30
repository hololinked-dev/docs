# Actions

[API Reference](../../api-reference/action/index.md)

Only methods decorated with `action()` are exposed to clients.

```py title="Actions" linenums="1"
--8<-- "docs/beginners-guide/code/thing_example_2.py:189:192"
--8<-- "docs/beginners-guide/code/thing_example_2.py:431:445"
--8<-- "docs/beginners-guide/code/thing_example_2.py:643:646"
--8<-- "docs/beginners-guide/code/thing_example_2.py:542:546"
```

Arguments are loosely typed and may need to be constrained with a schema based
on the robustness the developer is expecting in their application:

<a id="actions-argument-schema"></a>
=== "JSON Schema"

    === "Single Argument"

        Just specify the expected type of the argument (with or without name)

        ```py title="Input Schema" linenums="1"
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

        You need to specify the action argument names under the `properties` field with `type` as `object`.
        Names not found in the `properties` field can be subsumed under python spread operator `**kwargs` if necessary.

        ```py title="Input Schema with Multiple Arguments" linenums="1"
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

        ```py title="With Return Type"
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

    ```py title="Input Schema" linenums="1"
    ```

    === "Multiple Arguments"

    ```py title="Input Schema with Multiple Arguments" linenums="1"
    ```

However, a schema is optional and it only matters that
the method signature is matching when requested from a client. To enable this, set global attribute `allow_relaxed_schema_actions=True`. This setting is used especially when a schema is useful for validation of arguments but not available - not for methods with no arguments.

```py title="Relaxed or Unavailable Schema for Actions" linenums="1"
--8<-- "docs/beginners-guide/code/thing_example_2.py:168:172"
--8<-- "docs/beginners-guide/code/thing_example_2.py:558:559"
```

It is always possible to custom validate the arguments after invoking the action:

```py title="Custom Validation" linenums="1"
--8<-- "docs/beginners-guide/code/actions/parameterized_function.py:3:3"
--8<-- "docs/beginners-guide/code/actions/parameterized_function.py:9:27"
```

The last and least preferred possibility is to use `ParameterizedFunction`:

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
    ```
