# Extending

Properties can also be extended to define custom types, validation and coercion based on specific requirements. As a contrived example, one may define a JPEG image attribute which may accept a numpy array as input, have a compression level setting, transpose and flip the image if necessary.

To create the property, inherit from the `Property` object and define the `__init__`:

```py title='Subclassing Property' linenums="1"
--8<-- "docs/beginners-guide/code/properties/extending.py:2:2"
--8<-- "docs/beginners-guide/code/properties/extending.py:4:20"
```

It is possible to use the `__set__()` to carry out type validation & coercion:

```py title='Validation with __set__()' linenums="1"
--8<-- "docs/beginners-guide/code/properties/extending.py:1:7"
--8<-- "docs/beginners-guide/code/properties/extending.py:39:58"
```

Basically, check the types, manipulate your data if necessary and pass it to the parent. It is necessary to use the `instance_descriptor` decorator as shown above to allow `class_member` option to function correctly. If the `Property` will not be a `class_member`, this decorator can be skipped.

Further, the parent class [`Property` takes care](https://github.com/VigneshVSV/hololinked/blob/main/hololinked/server/property.py) of allocating an instance variable, checking `constant`, `readonly`, pushing change events, writing the value to the database etc. To avoid double checking of certain options like `readonly` and `constant`, its better to carry out the validation and coercion within the method `validate_and_adapt()` instead of `__set__`:

```py title='Validation and Adaption' linenums="1"
--8<-- "docs/beginners-guide/code/properties/extending.py:4:6"
--8<-- "docs/beginners-guide/code/properties/extending.py:20:37"
```

The `__set__()` method automatically invokes `validate_and_adapt()`, therefore the new value or validated value can be returned from this method.

To use the `JPEG` property in a `Thing` class, follow the normal procedure of property instantiation:

```py title="Instantiating Custom Property" linenums="1"
--8<-- "docs/beginners-guide/code/properties/extending.py:62:76"
```

In this particular example, since we dont want the `JPEG` to be set externally by a client, we create a local `Property` which carries out the image manipulation and an externally visible `readonly` Property that can fetch the processed image.

The difference between using a custom setter/`fset` method and overloading the `Property` is that, one can accept certain options specific to the `Property` in the `__init__` of the
`Property`:

```py title="Reusing Custom Property" linenums="1"
--8<-- "docs/beginners-guide/code/properties/extending.py:64:65"
--8<-- "docs/beginners-guide/code/properties/extending.py:78:86"
```

!!! Note

    This is a contrived example and may not lead to optimized Property APIs for the client. Please adapt them suitably or rethink their implementation.

One may also use slots to store the attributes of the `Property`. Most properties predefined in this package use slots:

```py title="Using slots" linenums="1"
--8<-- "docs/beginners-guide/code/properties/extending.py:90:"
```
