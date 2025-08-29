import numpy
from hololinked.core import Thing, Property


class TestObject(Thing):
    """test object demonstrating properties"""

    my_untyped_serializable_attribute = Property(
        default=frozenset([2, 3, 4]),
        allow_None=True,
        doc="this property can hold any python value",
    )

    my_custom_typed_serializable_attribute = Property(
        default=[2, "foo"],
        allow_None=False,
        doc="""this property can hold some 
            values based on get-set overload""",
    )

    @my_custom_typed_serializable_attribute.getter
    def get_prop(self):
        try:
            return self._foo
        except AttributeError:
            return self.properties.descriptors[
                "my_custom_typed_serializable_attribute"
            ].default

    @my_custom_typed_serializable_attribute.setter
    def set_prop(self, value):
        if isinstance(value, (list, tuple)) and len(value) < 100:
            for index, val in enumerate(value):
                if not isinstance(val, (str, int, type(None))):
                    raise ValueError(
                        f"Value at position {index} not "
                        + "acceptable member type of "
                        + "my_custom_typed_serializable_attribute "
                        + f"but type {type(val)}"
                    )
            self._foo = value
        elif isinstance(value, numpy.ndarray):
            self._foo = value
        else:
            raise TypeError(
                "Given type is not list or tuple for "
                + f"my_custom_typed_serializable_attribute but type {type(value)}"
            )

    def __init__(self, *, id: str, **kwargs) -> None:
        super().__init__(id=id, **kwargs)
        self.my_untyped_serializable_attribute = kwargs.get("some_prop", None)
        self.my_custom_typed_serializable_attribute = [1, 2, 3, ""]

    """
    
    def __init__(
        self, *, id: str, my_untyped_serializable_attribute: Any, **kwargs
    ) -> None:
        super().__init__(
            id=id,
            my_untyped_serializable_attribute=my_untyped_serializable_attribute,
            **kwargs,
        )
    """

    my_property = Property(
        default=[2, "foo"],
        allow_None=False,
        doc="this property can hold some values based on get-set overload",
    )

    @my_property.getter
    def my_property(self):
        # wrong - please dont use the property's name for the getter method
        return self._foo
