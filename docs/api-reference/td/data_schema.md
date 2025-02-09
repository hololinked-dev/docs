
::: hololinked.td.data_schema.DataSchema

## TD Supported Fields

| field        | supported | meaning                       | default usage                  |
|--------------|-----------|-------------------------------|--------------------------------|
| title        | ✔️ | Provides a human-readable title | label of `Property` or first line of docstring |
| titles       | ➖ | Provides multi-language human-readable titles | to be manually set |
| description  | ✔️ | Provides additional human-readable information | cleaned docstring of `Property` (`doc` value) |
| descriptions | ➖ | Provides multi-language human-readable descriptions | to be manually set |
| const        | ✔️ | `true` when value will remain constant | `Property.constant` value |
| default      | ✔️ | Provides a default value | `Property.default` value |
| format       | ➖ | format pattern such as "date-time", "email", "uri", etc. | to be manually set, will be supported in a future release |
| readOnly     | ✔️ | `true` when value is read-only | `Property.readonly` value |
| writeOnly    | ❌ | `true` when value is write-only | It is assumed that a property always has an associated value that can be read |
| unit         | ✔️ | Provides a human-readable unit | `Property.metadata["unit"]` value |
| type         | ✔️ | Provides a type for the property | typed inferred from specific subclass of `Property`, pydantic models are considered as an `object` currently even when having only one field or a root model (will be fixed in a future release |
| oneOf        | ✔️ | Provides a list of possible values | Usually for properties with `allow_None` apart from its own `type` |

See subclasses for more specific fields under same topic.