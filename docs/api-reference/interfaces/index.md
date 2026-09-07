# Interfaces

::: hololinked.core.interfaces
    options:
        members: []
        show_root_heading: false

These are contracts each replaceable dependency has to satisfy. Subclass from here to implement one's
own tech stack. If one needs a totally new feature, a base class needs to be defined in this namespace with business logic integrated into the repository, these need separate PRs and dont work out of the box.  

| Port | Registry | Adapters |
| --- | --- | --- |
| [`BaseSerializer`](serializer.md) | [`Serializers`](../serializers/index.md) | `hololinked.serializers` |
| [`BaseSchemaValidator`](schema-validator.md) | [`SchemaValidators`](../injection/schema-validators.md) | `hololinked.schema_validators` |
| [`BaseConfigurationRepository`](configuration-repository.md) | [`StorageBackends`](../injection/storage-backends.md) | `hololinked.storage` |
| [`MetadataFormat`](metadata.md) | [`MetadataFormats`](../injection/metadata-formats.md) | `hololinked.metadata` |

See [Hexagonal Architecture](../../design/hexagonal-architecture.md) for the reasoning behind the split.
