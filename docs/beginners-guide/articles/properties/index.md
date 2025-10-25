# Properties In-Depth

Properties expose python attributes to clients & support custom get-set(-delete) operations. Further, change events can be subscribed/observed to be automatically informed of a change in the value of a property.
`hololinked` uses `param` under the hood to implement properties, which in turn uses the
descriptor protocol.

!!! Note

    Python's own `property` is not supported for remote access due to limitations in using foreign attributes
    within the `property` object. Said limitation causes redundancy with the existing implementation of
    `Property` class, nevertheless, the term `Property`
    (with capital 'P') is used to comply with the terminology of Web of Things.

### Untyped/Custom Typed Property

[API Reference](../../../api-reference/property/index.md)

To make a property take any python value, use the base class `Property`:

```py title="Untyped Property" linenums="1" hl_lines="4"
--8<-- "docs/beginners-guide/code/properties/untyped.py:5:12"
--8<-- "docs/beginners-guide/code/properties/untyped.py:49:53"
```

One can also pass the property value to the `Thing` parent's `__init__` to auto-set or auto-invoke the setter at `__init__`:

```py title="init" linenums="1" hl_lines="13-17"
--8<-- "docs/beginners-guide/code/properties/untyped.py:5:12"
--8<-- "docs/beginners-guide/code/properties/untyped.py:56:64"
```

As previously stated, by default, a data container is auto allocated at the instance level. One can supply a custom getter-setter if necessary,
especially when applying the property directly onto the hardware.
The descriptor object (instance of `Property`) that holds the property metadata and performs the get-set operations can be
accessed by the instance under `self.properties.descriptors["<property name>"]`:

```py title="Custom Typed Property" linenums="1" hl_lines="15 20-22 24"
--8<-- "docs/beginners-guide/code/properties/untyped.py:1:7"
--8<-- "docs/beginners-guide/code/properties/untyped.py:14:48"
```

The value of the property must be serializable to be read by the clients. Read the [serializer section](../serialization.md) for further details & customization. To make a property only locally accessible, set `remote=False`, i.e. such a property will not accessible on the network nevertheless the descriptor behaviour can still be leveraged.

### Predefined Typed Properties

[API Reference](../../../api-reference/property/typed/index.md)

Certain typed properties are already available in `hololinked.core.properties`,
defined by `param`:

| Property Class                      | Type                          | Options                                                               |
| ----------------------------------- | ----------------------------- | --------------------------------------------------------------------- |
| `String`                            | `str`                         | comply to regex                                                       |
| `Number`                            | `float`, `int`                | min & max bounds, inclusive bounds, crop to bounds, multiples         |
| `Integer`                           | `int`                         | same as `Number`                                                      |
| `Boolean`                           | `bool`                        | tristate if `allow_None=True`                                         |
| `Iterable`                          | general python iterables      | length/bounds, item_type, dtype (allowed type of the iterable itself) |
| `Tuple`                             | `tuple`                       | same as iterable                                                      |
| `List`                              | `list`                        | same as iterable                                                      |
| `Selector`                          | one of many objects           | allowed list of objects                                               |
| `TupleSelector`                     | one or more of many objects   | allowed list of objects                                               |
| `ClassSelector`                     | class, subclass or instance   | comply to instance only or class/subclass only                        |
| `Path`, `Filename`, `Foldername`    | path, filename & folder names |                                                                       |
| `Date`                              | `datetime`                    | format                                                                |
| `TypedList`                         | typed list                    | typed appends, extends                                                |
| `TypedDict`, `TypedKeyMappingsDict` | typed dictionary              | typed updates, assignments                                            |

An example:

```py title="Typed Properties" linenums="1"
--8<-- "docs/beginners-guide/code/properties/typed.py:2:5"
--8<-- "docs/beginners-guide/code/properties/typed.py:40:62"
```

For typed properties, before the setter is invoked, the value is internally validated.
The return value of getter method is never validated and is left to the developer's or the client's caution.

## Schema Constrained Property

For complicated data structures, one can use `pydantic` or JSON schema based type definition and validation. Set the `model` argument to define the type:

=== "pydantic"

    ```py title="Properties Using Schema - pydantic" linenums="1" hl_lines="7 62-63"
    --8<-- "docs/beginners-guide/code/properties/schema.py:1:64"
    ```

=== "JSON Schema"

    ```py title="Properties Using Schema - JSON schema" linenums="1" hl_lines="5 37"
    --8<-- "docs/beginners-guide/code/properties/schema.py:67"
    ```
