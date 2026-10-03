# ZMQ runtime configuration

::: hololinked.server.zmq.config.RuntimeConfig
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - thing_description_service

Pass as a plain dictionary to the `config` argument of [`ZMQServer`](index.md):

```python
ZMQServer(config=dict(thing_description_service=MyService))
```