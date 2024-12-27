Properties In-Depth
===================

Properties expose python attributes to clients & support custom get-set(-delete) functions. 
``hololinked`` uses ``param`` under the hood to implement properties, which in turn uses the
descriptor protocol. 

!!! note

    Python's own `property` is not supported for remote access due to limitations in using foreign attributes 
    within the `property` object. Said limitation causes redundancy with implementation of 
    `hololinked.server.Property`, nevertheless, the term `Property`
    (with capital 'P') is used to comply with the terminology of Web of Things. 

Untyped/Custom Typed Property 
-----------------------------

[API Reference](../../api-reference/property)

To make a property take any python value, use the base class `Property`:

```py title="Untyped Property" linenums="1"
--8<-- "docs/howto/code/properties/untyped.py:1:10 
--8<-- "docs/howto/code/properties/untyped.py:39:41"
```

The object (descriptor instance of ``Property``) that performs the get-set operations or auto-allocation 
of an internal instance variable for the property can be accessed by the instance under 
``self.properties.descriptors["<property name>"]``:

```
--8<-- "docs/howto/code/properties/untyped.py:1:7
--8<-- 11-
```
    :language: python
    :linenos:
    :lines: 

Expectedly, the value of the property must be serializable to be read by the clients. Read the serializer 
section for further details & customization. 

To make a property only locally accessible, set ``remote=False``, i.e. such a property will not accessible 
on the network. 

Built-in Typed Properties
-------------------------

:doc:`API Reference <../../autodoc/server/properties/types/index>`

Certain typed properties are already available in ``hololinked.server.properties``, 
defined by ``param``:

.. list-table::

    *   - type 
        - Property class  
        - options 
    *   - str
        - ``String``
        - comply to regex
    *   - float, integer 
        - ``Number`` 
        - min & max bounds, inclusive bounds, crop to bounds, multiples 
    *   - integer 
        - ``Integer`` 
        - same as ``Number``
    *   - bool 
        - ``Boolean``
        - tristate if ``allow_None=True``
    *   - iterables 
        - ``Iterable``
        - length/bounds, item_type, dtype (allowed type of the iterable itself like list or tuple or deque etc.)
    *   - tuple 
        - ``Tuple`` 
        - same as iterable 
    *   - list 
        - ``List`` 
        - same as iterable  
    *   - one of many objects 
        - ``Selector``
        - allowed list of objects 
    *   - one or more of many objects 
        - ``TupleSelector``
        - allowed list of objects 
    *   - class, subclass or instance of an object 
        - ``ClassSelector``
        - comply to instance only or class/subclass only 
    *   - path, filename & folder names 
        - ``Path``, ``Filename``, ``Foldername``
        - 
    *   - datetime 
        - ``Date``
        - format
    *   - typed list 
        - ``TypedList``
        - typed appends, extends 
    *   - typed dictionary
        - ``TypedDict``, ``TypedKeyMappingsDict``
        - typed updates, assignments    

An example:

.. literalinclude:: ../code/properties/typed.py 
    :language: python
    :linenos:
    :lines: 2-5, 37-60

For typed properties, before the setter is invoked, the value is internally validated. 
The return value of getter method is never validated and is left to the developer's or the client object's caution. 

Schema Constrained Property 
---------------------------

For complicated data structures, one can use ``pydantic`` or JSON schema based type definition and validation. 
``pydantic`` supports all python types whereas JSON schema allows only JSON compatible types. Set the model argument 
to define the type:
