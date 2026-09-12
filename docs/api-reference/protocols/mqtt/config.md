# MQTT runtime configuration

::: hololinked.server.mqtt.config.RuntimeConfig
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - qos
            - topic_publisher
            - thing_description_publisher
            - thing_description_service

Pass these as a plain dictionary to the `config` argument of [`MQTTPublisher`](index.md), not as a
`RuntimeConfig` instance:

```python
MQTTPublisher(config=dict(qos=2, topic_publisher=MyTopicPublisher))
```
