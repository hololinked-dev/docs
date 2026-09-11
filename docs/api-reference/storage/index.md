# Storage

::: hololinked.storage
    options:
        show_root_heading: false
        members: false

A storage backend implements the [`BaseConfigurationRepository`](../interfaces/configuration-repository.md).

| backend | registered name | `Thing` flag | extra | needs a server |
| --- | --- | --- | --- | --- |
| [`JSONFileStorage`](json-file.md) | `json_file` | `use_json_file` | — | no |
| [`SQLAlchemyDB`](sqlalchemy.md) | `sqlalchemy` | `use_default_db` | `sqlalchemy`, `postgresql` | SQLite no, others yes |
| [`MongoDB`](mongodb.md) | `mongo` | `use_mongo_db` | `mongo` | yes |
