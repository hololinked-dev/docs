# General

There are multiple ways to start serving one's `Thing` instance based on the application requirements:

- One needs to run one `Thing` instance in one or multiple protocols
- One needs to run multiple `Thing` instances in one protocol
- One needs to run multiple `Thing`s instances in multiple protocols

## Run Single Thing in Multiple Protocols

To configure a protocol server in a detailed fashion, instantiate them explicitly. 
To start serving, one can pass them as an argument to the `run()` method of the `Thing`:

```python linenums="1" title="Multiple Protocol Servers"
from hololinked.server import HTTPServer, MQTTPublisher, ZMQServer

http_server = HTTPServer(port=9000)
mqtt_server = MQTTPublisher(host='mqtt.example.com')
zmq_server = ZMQServer(id='oscilloscope-server', access_points=['IPC', 'tcp://*:9001'])

Oscilloscope(id='oscilloscope').run(servers=[http_server, mqtt_server, zmq_server])
```

Based on the protocol, the servers may support overriding the exposed configuration, for example, changing the HTTP URL path, or overriding an MQTT publishing worker.

> The number of such features supported is generally a work in progress. Please consider reading the codebase if you wish to implement a highly specific feature, and also consider contributing your feature to the repository - [How to Contribute](https://docs.hololinked.dev/introduction/contributing/).

Alternatively, to quickly expose the `Thing` instance, supply the protocol name and the access point (port or address) as a tuple to the `run()` method.

```python linenums="1" title="Quick Start"
Oscilloscope(id='oscilloscope').run(
    access_points=(
        ('HTTP', 9000),
        ('MQTT', 'mqtt.example.com'),
        ('ZMQ', ['IPC', 'tcp://*:9001']),
    )
)
```

HTTP and ZMQ support a `run_with_<protocol>` method:

```python linenums="1" title="Quick Start Option 2"
Oscilloscope(id='oscilloscope').run_with_http_server(port=9000, ssl_context=ssl_context)
```

## Run Multiple Things in One Protocol

All protocols support an `add_thing()` method that accepts a `Thing` instance
and a `run()` and `stop()` method that control their boot up & shutdown: 

```python linenums="1" title="add Things to protocol server"
from hololinked.server import HTTPServer

server = HTTPServer(port=9000)
server.add_thing(Oscilloscope(id='oscilloscope'))
server.add_thing(DCPowerSupply(id='dc-power-supply'))

server.run()
```

## Run Multiple Things in Multiple Protocols

Use the global `run()` method along with `server.add_thing()` to start any number of `Thing` instances in any number of protocols:

```python linenums="1" title="Run Multiple Things in Multiple Protocols"
from hololinked.server import HTTPServer, MQTTPublisher, run

http_server = HTTPServer(port=9000)
mqtt_server = MQTTPublisher(host='mqtt.example.com')

http_server.add_thing(Oscilloscope(id='oscilloscope'))
mqtt_server.add_thing(DCPowerSupply(id='dc-power-supply'))

run(servers=[http_server, mqtt_server])
# HTTP server serves Oscilloscope and MQTTPublisher publishes events from DCPowerSupply
```
