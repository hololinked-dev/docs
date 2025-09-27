# Common arguments to all properties

[API Reference](../../../api-reference/property/index.md)

### `allow_None`, `constant` & `readonly`

- if `allow_None` is `True`, property supports `None` apart from its own type
- `readonly` (being `True`) makes the property read-only or execute only the getter method
- `constant` (being `True`), again makes the property read-only but can be set once if `allow_None` is `True`.
  This is useful to set the property once at `__init__()` but remain constant after that.

```py title="allow None, constant and readonly" linenums="1" hl_lines="11 19 27 28 36"
--8<-- "docs/beginners-guide/code/properties/common_args_1.py:1:39"
```

=== "`allow_None=True`"

    ```py title="allow None, constant and readonly" linenums="1"
    --8<-- "docs/beginners-guide/code/properties/common_args_1.py:44:47"
    ```

=== "`allow_None=False`"

    ```py title="allow None, constant and readonly" linenums="1"
    --8<-- "docs/beginners-guide/code/properties/common_args_1.py:49:51"
    ```

=== "`readonly=True`"

    ```py title="allow None, constant and readonly" linenums="1"
    --8<-- "docs/beginners-guide/code/properties/common_args_1.py:53:54"
    ```

=== "`constant=True`"

    ```py title="allow None, constant and readonly" linenums="1"
    --8<-- "docs/beginners-guide/code/properties/common_args_1.py:56:59"
    ```

### `doc` and `label`

`doc` allows clients to fetch a docstring for the property. `label` can be used to show the property
in a GUI with a readable name (for example).

```py title="allow None, constant and readonly" linenums="1" hl_lines="8-9"
--8<-- "docs/beginners-guide/code/properties/common_args_1.py:5:14"
```

### `default`, `fget`, `fset` & `fdel`

To provide a getter-setter (& deleter) method is optional.

If none given, when the property is set/written, the value is stored inside the instance's `__dict__` under the name `<given property name>_param_value`
(for example, `serial_number_param_value` for `serial_number`). In layman's terms, `__dict__` is the internal map where the attributes of the object are stored by python.

When a value assignment was never called on the property, `default` is returned when reading the value. If a setter/deleter is given, getter is mandatory. In this case, `default` is also ignored & the getter is always executed.

=== "with decorator"

    ```py linenums="1" hl_lines="24 31"
    --8<-- "docs/beginners-guide/code/properties/common_args_2.py:24:50"
    --8<-- "docs/beginners-guide/code/properties/common_args_2.py:53:60"
    --8<-- "docs/beginners-guide/code/properties/common_args_2.py:135:140"
    ```

=== "with fget-fset-fdel arguments"

    ```py linenums="1" hl_lines="26-27"
    --8<-- "docs/beginners-guide/code/properties/common_args_2.py:24:30"
    --8<-- "docs/beginners-guide/code/properties/common_args_2.py:32:37"
    --8<-- "docs/beginners-guide/code/properties/common_args_2.py:39:53"
    ```

If default is desirable, one has to return it manually in the getter method by accessing the property [descriptor object directly](../#__codelineno-2-15).

### `class_member`

If `class_member` is True, the value is set in the class' `__dict__` (i.e. becomes a class attribute)
instead of instance's `__dict__` (instance's attribute).
Custom getter-setter-deleter are not compatible with this option currently. `class_member` takes precedence over fget-fset-fdel,
which in turn has precedence over `default`.

```py title="class member" linenums="1" hl_lines="26"
--8<-- "docs/beginners-guide/code/properties/common_args_2.py:7:22"
--8<-- "docs/beginners-guide/code/properties/common_args_2.py:24:26"
--8<-- "docs/beginners-guide/code/properties/common_args_2.py:64:73"
--8<-- "docs/beginners-guide/code/properties/common_args_2.py:135:136"
--8<-- "docs/beginners-guide/code/properties/common_args_2.py:141:143"
```

`class_member` can still be used with a default value if there is no custom fget-fset-fdel.

### `remote`

setting `remote` to False makes the inaccessible to a client but accessible to the object locally. This is still useful to type-restrict python attributes to provide an interface to other developers using your class, for example, when someone else inherits your `Thing`. For example, the `Thing`'s `logger` is implemented in this fashion:

```py title="local properties" linenums="1" hl_lines="11"
import logging
from hololinked.core.properties import ClassSelector

class Thing(metaclass=ThingMeta):
    """Subclass from here to expose hardware or python objects on the network"""

    logger = ClassSelector(
        class_=logging.Logger,
        default=None,
        allow_None=True,
        remote=False,  # does not make sense to expose the logger object, its not serializable
        doc="""logging.Logger instance to print log messages.
            Default logger with a IO-stream handler and network
            accessible handler is created if none supplied."""
    )  # type: logging.Logger
```

### `state`

When `state` is specifed, the property is writeable only when the `Thing`'s `StateMachine` is in that specified state (or
in the list of allowed states):

```py title="state machine state" linenums="1" hl_lines="22"
--8<-- "docs/beginners-guide/code/properties/common_args_2.py:24:26"
--8<-- "docs/beginners-guide/code/properties/common_args_2.py:77:100"
```

This is also currently applicable only when set operations are called by clients. Local set operations are always executed irrespective of the state machine state. A get operation is always executed even from the clients irrespective of the state.

## `observable`

Observable properties push change events when the property is set or read. This is useful when one wants to monitor the
property for changes without polling from the client. The payload of the change event is the new value of the property.

```py title="observable" linenums="1" hl_lines="29"
--8<-- "docs/beginners-guide/code/properties/common_args_2.py:24:26"
--8<-- "docs/beginners-guide/code/properties/common_args_2.py:104:133"
```

## `metadata`

`metadata` is a free-flow dictionary that allows storing arbitrary metadata about the property. For example, one can store units of the physical
quantity.

## `db_init`, `db_commit` & `db_persist`

Properties can be stored in a file or a database and loaded from them when the `Thing` is stopped and restarted. This is useful especially to preserve the settings of the hardware when the server undergoes a restart, either through system restart, server crash or any other reason.

- `db_init` only loads a property from database. When the property value is changed, its not written back to the database.
  For this option, the value has to be pre-created in the database in some other fashion.

- `db_commit` only writes the value into the database when an assignment/write operation is called.

- `db_persist` stores and loads the property from the database. property value is assigned after `__init__()` method, therefore its recommended to ensure that the device connection is established at `__init__()` itself. Other, errors should be expected.

Supported databases are MySQL, Postgres & SQLite currently. Look at database how-to for supply database configuration.
