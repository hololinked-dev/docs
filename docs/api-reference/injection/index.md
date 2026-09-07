# Adapter Registries

::: hololinked.injection
    options:
        members: []
        show_root_heading: false

Each registry below resolves an implementation **by name, on first use**.

| Registry | Resolves | Adapters live in |
| --- | --- | --- |
| [`Serializers`](../serializers/index.md) | serializers | `hololinked.serializers` |
| [`SchemaValidators`](schema-validators.md) | schema validators | `hololinked.schema_validators` |
| [`StorageBackends`](storage-backends.md) | storage backends | `hololinked.storage` |
| [`MetadataFormats`](metadata-formats.md) | device description languages | `hololinked.metadata` |

The implementation is either already available in the package or can be supplied by the end user.
All four classes above are singletons, so anything set on them applies process-wide.

::: hololinked.injection.AdapterRegistry
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - adapter_kind
            - package
            - modules
            - tables
            - instantiate
            - install
            - forget_adapters

::: hololinked.injection.Registry
    options:
        show_root_heading: true
        heading_level: 2
