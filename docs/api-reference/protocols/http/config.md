# HTTP runtime configuration

::: hololinked.server.http.config.RuntimeConfig
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - cors
            - allowed_clients
            - security_schemes
            - server_id
            - property_handler
            - action_handler
            - event_handler
            - RW_multiple_properties_handler
            - thing_description_handler
            - liveness_probe_handler
            - readiness_probe_handler
            - stop_handler
            - thing_description_service

Pass these as a plain dictionary to the `config` argument of
[`HTTPServer`](index.md), not as a `RuntimeConfig` instance:

```python
HTTPServer(config=dict(cors=True, property_handler=MyPropertyHandler))
```

::: hololinked.server.http.config.HandlerMetadata
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - http_methods
