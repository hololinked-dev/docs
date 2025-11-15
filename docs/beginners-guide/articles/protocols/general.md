# General

There are multiple ways to start serving your `Thing`:

- One needs to run one `Thing` in multiple protocols
- One needs to run multiple `Thing`s in one protocol
- One needs to run multiple `Thing`s in multiple protocols

## Run Single Thing in Multiple Protocols

There are two possible syntax options:

```python linenums="1"
from hololinked.server import HTTPServer, MQTTServer

http_server = HTTPServer(port=9000)
mqtt_server = MQTTServer(host='mqtt.example.com', port=1883)
zmq_server = ZMQServer(access_points=['IPC', 'tcp://*:9001'])

Oscilloscope(id='oscilloscope').run(servers=[http_server, mqtt_server, zmq_server])
```

OR

```python linenums="1"
from hololinked.server import HTTPServer, MQTTServer

Oscilloscope(id='oscilloscope').run(
    access_points=(
        ('HTTP', 9000),
        ('MQTT', 'mqtt.example.com'),
        ('ZMQ', ['IPC', 'tcp://*:9001']),
    )
)
```

The first option is obviously preferred.

## Run Multiple Things in One Protocol

```python linenums="1"
from hololinked.server import HTTPServer

server = HTTPServer(port=9000)
server.add_thing(Oscilloscope(id='oscilloscope'))
server.add_thing(DCPowerSupply(id='dc-power-supply'))

server.run()
```

## Run Multiple Things in Multiple Protocols

```python linenums="1"
from hololinked.server import HTTPServer, MQTTServer, run

http_server = HTTPServer(port=9000)
mqtt_server = MQTTServer(host='mqtt.example.com', port=1883)

http_server.add_thing(Oscilloscope(id='oscilloscope'))
mqtt_server.add_thing(DCPowerSupply(id='dc-power-supply'))

run(servers=[http_server, mqtt_server])
```
