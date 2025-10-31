# HTTP

## SSL context

One can enable SSL for HTTP server by providing an SSL context while creating the server:

```python linenums="1" title="Use SSL"
import ssl, os

cert_file = f'assets{os.sep}security{os.sep}certificate.pem'
key_file = f'assets{os.sep}security{os.sep}key.pem'
ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(cert_file, keyfile=key_file)
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3

http_server = HTTPServer(port=8090, ssl_context=ssl_context)

Oscilloscope(id='oscilloscope').run(servers=[http_server])
# OR
Oscilloscope(
    id='oscilloscope',
).run_with_http_server(
    port=8090,
    ssl_context=ssl_context,
)
```

## Register Custom Routes & Methods

The default routes are created as follows:

| Resource          | Path                           | Description                  | Handler                   | Default Method                                                 |
| ----------------- | ------------------------------ | ---------------------------- | ------------------------- | -------------------------------------------------------------- |
| Property          | `/<thing-id>/<foo-bar>`        | for property `foo_bar`       | `PropertyHandler`         | `GET` for read <br/> `PUT` for write <br/> `DELETE` for delete |
| Action            | `/<thing-id>/<foo-bar>`        | for action `foo_bar`         | `ActionHandler`           | `POST`                                                         |
| Event             | `/<thing-id>/<foo-bar>`        | for event `foo_bar`          | `EventHandler`            | `GET`                                                          |
| Thing Model       | `/<thing-id>/resources/wot-tm` | to get the Thing Model       | - acts as property -      | `GET`                                                          |
| Thing Description | `/<thing-id>/resources/wot-td` | to get the Thing Description | `ThingDescriptionHandler` | `GET`                                                          |

All underscores are converted to hyphens in the URL paths for every resource, and the Thing ID is a global prefix.

One can register custom routes and methods as follows:

```python linenums="1" title="Custom Routes"
from hololinked.server import HTTPServer

server = HTTPServer(port=8090)

server.add_property('/channels/data/A', Oscilloscope.channel_A)
server.add_event('/channels/data/A/stream', Oscilloscope.channel_A_data_event)

Oscilloscope(id='oscilloscope').run(servers=[server])
```

## Allow CORS

On the web browser, one may want to access the HTTP server from a different domain name, especially during development or in private networks. In such cases, one needs to enable CORS headers:

```python linenums="1" title="Enable CORS"
http_server = HTTPServer(port=8090, config=dict(cors=True))
Oscilloscope(id='oscilloscope').run(servers=[http_server])
# OR
Oscilloscope(
    id='oscilloscope',
).run_with_http_server(
    port=8090,
    config=dict(cors=True),
)
```

CORS headers are set only for authenticated clients.

## Remotely Stop

If one wishes to remotely stop the HTTP server, one needs to exit both the served `Thing` instance as well as the server itself. This can be done as follows:

```python linenums="1" title="Remotely Stop HTTP Server"
import requests

response = requests.post('https://my-pc:9090/my-thing-id/exit')
assert response.status_code == 204
response = requests.post('https://my-pc:9090/stop')
assert response.status_code == 204
```

Make sure to use a [security scheme](../security.md) to prevent unauthorized access to the exit action.
