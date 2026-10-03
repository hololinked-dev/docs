# Storage models

The SQLAlchemy table definitions used by [`SQLAlchemyDB`](sqlalchemy.md).

::: hololinked.storage.models.SerializedProperty
    options:
        show_root_heading: true
        heading_level: 2

::: hololinked.storage.models.ThingInformation
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - id
            - thing_id
            - thing_class
            - script
            - init_kwargs
            - server_id
            - json

::: hololinked.storage.models.DeserializedProperty
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - thing_id
            - name
            - value
            - created_at
            - updated_at


::: hololinked.storage.models.ThingTableBase
    options:
        show_root_heading: true
        heading_level: 2