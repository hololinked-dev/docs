# Actions

[API Reference](../../api-reference/action/index.md)

Only methods decorated with `action()` are exposed to clients.

```py title="Actions" linenums="1"
--8<-- "docs/howto/code/thing_example_2.py:168:172"
--8<-- "docs/howto/code/thing_example_2.py:365:374"
--8<-- "docs/howto/code/thing_example_2.py:510:513"
--8<-- "docs/howto/code/thing_example_2.py:446:451"
--8<-- "docs/howto/code/thing_example_2.py:455:456"
--8<-- "docs/howto/code/thing_example_2.py:375:380"
```

Arguments are loosely typed and may need to be constrained with a schema based
on the robustness the developer is expecting in their application:

<a id="actions-argument-schema"></a>
=== "JSON Schema"

    === "Single Argument"

        ```py title="Input Schema" linenums="1"
        --8<-- "docs/howto/code/thing_example_2.py:168:172"
        --8<-- "docs/howto/code/thing_example_2.py:189:205"
        ```

    === "Multiple Arguments"

        ```py title="Input Schema with Multiple Arguments" linenums="1"
        --8<-- "docs/howto/code/thing_example_3.py:47:75"
        --8<-- "docs/howto/code/thing_example_3.py:78:80"
        --8<-- "docs/howto/code/thing_example_3.py:83:83"
        --8<-- "docs/howto/code/thing_example_3.py:188:195"
        --8<-- "docs/howto/code/thing_example_3.py:219:219"
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
--8<-- "docs/howto/code/thing_example_2.py:168:172"
--8<-- "docs/howto/code/thing_example_2.py:558:559"
```

The return value must be validated by the clients themselves. While a schema for the return value can be supplied, there is no separate validation performed on the server:

=== "JSON Schema"

    ```py title="Output Schema" linenums="1"
    --8<-- "docs/howto/code/thing_example_3.py:22:36"
    --8<-- "docs/howto/code/thing_example_3.py:38:45"
    --8<-- "docs/howto/code/thing_example_3.py:78:80"
    --8<-- "docs/howto/code/thing_example_3.py:83:83"
    --8<-- "docs/howto/code/thing_example_3.py:307:323"
    ```

=== "pydantic"

    ```py title="" linenums="1"
    ```

It is always possible to custom validate the arguments after invoking the action:

```py title="Custom Validation" linenums="1"
--8<-- "docs/howto/code/actions/parameterized_function.py:3:3"
--8<-- "docs/howto/code/actions/parameterized_function.py:9:27"
```

The last and least preferred possibility is to use `ParameterizedFunction`:

```py title="Parameterized Function" linenums="1"
--8<-- "docs/howto/code/actions/parameterized_function.py:52:"
```

`ParameterizedFunction`(s) are classes that implement the `__call__` method and whose arguments are type defined using the same objects as properties. However, this type definition using `Property` object do not make these properties of the `Thing`. The implementation follows convention used by `param` where the
properties are termed as "parameters" (also hence the word "ParameterizedFunction").

The `__call__` method signature accepts its own self as the first argument,
followed by the `Thing` instance as the second argument and then the arguments supplied by the client. On the
client side, there is no difference between invoking a normal action and an action implemented as
`ParameterizedFunction`:

=== "server"

    ```py title="Custom Validation" linenums="1"
    --8<-- "docs/howto/code/actions/parameterized_function.py:38:44"
    ```

=== "client"

    ```py title="Custom Validation" linenums="1"
    --8<-- "docs/howto/code/actions/parameterized_function.py:30:36"
    ```
