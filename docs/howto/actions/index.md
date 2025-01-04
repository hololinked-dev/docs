Actions
=======

[API Reference](../../api-reference/action/index.md)

Only methods decorated with ``action()`` are exposed to clients. 

```py title="Actions" linenums="1"
--8<-- "docs/howto/code/no_network_thing.py:40:43"
--8<-- "docs/howto/code/no_network_thing.py:230:237"
--8<-- "docs/howto/code/no_network_thing.py:303:307"
--8<-- "docs/howto/code/no_network_thing.py:312:312"
--8<-- "docs/howto/code/no_network_thing.py:370:373"
```

Arguments are loosely typed and may need to be constrained with a schema based 
on the robustness the developer is expecting in their application. However, a schema is optional and it only matters that 
the method signature is matching when requested from a client.
Since python is loosely typed, the server may need to verify the argument types
supplied by the client call. If the input data is JSON compliant (which is recommended),
one can supply an input schema to the action decorator:

```py title="Actions" linenums="1"
--8<-- "docs/howto/code/no_network_thing.py:40:40"
--8<-- "docs/howto/code/no_network_thing.py:56:68"
```

If an input schema is unspecified, the server will not validate the input data even if arguments are present. 
The return value must be validated by clients themselves and one may supply a schema for the return value; there is 
no separate validation on the server.

If one encounters an uncomfortable use case of validating non-JSON arguments, until support for type annotations based 
validations are added, one may perform one's own validation:

```py title="Actions" linenums="1"
--8<-- "docs/howto/code/actions/parameterized_function.py:9:20"
--8<-- "docs/howto/code/actions/parameterized_function.py:34:39"
```

The other builtin automatic validation possibility for non-JSON arguments is to use ``ParameterizedFunction``: 

```py title="Actions" linenums="1"
--8<-- "docs/howto/code/actions/parameterized_function.py:3:3"
--8<-- "docs/howto/code/actions/parameterized_function.py:9:33"
```

``ParameterizedFunction`` (s) are classes whose arguments are type defined using the same objects as properties 
and implement the ``__call__`` method. However, this type definition using property object do not make these 
arguments as properties of the ``Thing``. The implementation follows convention used by ``param`` where the 
properties are termed as "parameters" (also hence the word "ParameterizedFunction"). 

The ``__call__`` method signature accepts its own self as the first argument, 
followed by the ``Thing`` instance as the second argument and then the arguments supplied by the client. On the 
client side, there is no difference between invoking a normal action and an action implemented as 
``ParameterizedFunction``:

```py title="Actions" linenums="1"
--8<-- "docs/howto/code/actions/parameterized_function.py:43"
```
