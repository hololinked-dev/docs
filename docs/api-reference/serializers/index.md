

::: hololinked.serializers.serializers.Serializers
    options:
        members:
            - for_object
            - register
            - register_content_type_for_object
            - register_content_type_for_object_by_name
            - register_for_object
  
## Attributes

### `json: JSONSerializer`
`class-attribute`, `writable` <br />
The default serializer for all properties, actions and events (`msgspec` based C++ implementation)

### `pickle: PickleSerializer`
`class-attribute`, `writable` <br />
pickle serializer, unsafe without encryption but useful for faster & flexible serialization of python specific types

### `msgpack: MsgPackSerializer`
`class-attribute`, `writable` <br />
MessagePack serializer, efficient binary format that is both fast & interoperable between languages but not human readable

### `default: BaseSerializer`
`JSONSerializer`, set it to use something else          