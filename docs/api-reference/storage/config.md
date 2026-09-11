# Storage configuration

::: hololinked.storage.config.SQLDBConfig
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - provider
            - host
            - port
            - database
            - user
            - password
            - dialect
            - uri
            - URL

::: hololinked.storage.config.SQLiteConfig
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - provider
            - dialect
            - file
            - in_memory
            - uri
            - URL

::: hololinked.storage.config.MongoDBConfig
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - provider
            - host
            - port
            - database
            - user
            - password
            - authSource
            - uri
            - URL
