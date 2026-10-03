# FastJSONSchemaValidator

Unlike [`JSONSchemaValidator`](json-schema.md) and [`PydanticSchemaValidator`](pydantic.md), this one
is **not** registered under a name in
[`SchemaValidators`](../injection/schema-validators.md), as a default JSON schema validator is available. To use `FastJSONSchemaValidator`:

```python
from hololinked import SchemaValidators
from hololinked.schema_validators import FastJSONSchemaValidator

SchemaValidators.register(FastJSONSchemaValidator, "json_schema", predicate=lambda schema: isinstance(schema, dict))
```

It needs the `validators` extra dependencies (`pip install hololinked[validators]`).

::: hololinked.schema_validators.fast_json_schema.FastJSONSchemaValidator
    options:
        show_root_heading: true
        heading_level: 2
        inherited_members: true
        members:
            - __init__
            - schema
            - json
            - validator
            - validate
            - validate_method_call
            - check_schema
