# Import Namespaces

These are the important namespaces in the repository.

| Namespace                | Description                                                                                                                                                                                                                                                                |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `hololinked.core`        | Definition of [`Thing`](thing/index.md) class, [`Property`](property/index.md), [`Action`](action/index.md) and [`Event`](events/index.md) classes, [`StateMachine`](state-machine/state-machine.md), [`Logger`](thing/logger.md) & the [`EventLoop`](eventloop/eventloop.md) that executes operations. |
| `hololinked.serializers` | Serializers for different data formats (JSON, MessagePack, etc.)                                                                                                                                                                                                           |
| `hololinked.server`      | Protocol specific server implementations                                                                                                                                                                                                                                   |
| `hololinked.client`      | [`ObjectProxy`](clients/object-proxy.md), protocol specific client implementations, client abstractions and [`ClientFactory`](clients/base.md).                                                                                                                            |
| `hololinked.param`       | Copy of [`holoviz param`](https://param.holoviz.org/en/docs/latest/index.html) library with implementation specific modifications.                                                                                                                                         |
| `hololinked.storage`     | Database clients for data persistence.                                                                                                                                                                                                                                     |
| `hololinked.metadata`    | Device description languages a `Thing` can be described in. `hololinked.metadata.td` holds the W3C Web of Things Thing Description/[ThingModel](td/tm.md) parsing and generation. |
| `hololinked.injection`   | Dependency injection layer, holds the lazy adapter registries like `Serializers`, `SchemaValidators`, `StorageBackends` and `MetadataFormats` that resolve an implementation by name on first use. |
| `hololinked.schema_validators` | Validators that check property, action and event payloads against a schema (JSON Schema, fastjsonschema, pydantic). |

A [hexagonal architecture](../design/hexagonal-architecture.md) is followed with `hololinked.core` being the important part of the repository.

<img src="../../assets/hexagonal-architecture.drawio.svg" alt="Hexagonal architecture diagram" style="width: 100%; height: auto;" />