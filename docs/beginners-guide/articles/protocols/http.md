# HTTP

[API Reference](../../../api-reference/protocols/http/index.md)

## SSL context

One can enable SSL for HTTP server by providing an SSL context while creating the server:

```python linenums="1" title="Use SSL"
import ssl, os

cert_file = f'assets{os.sep}security{os.sep}certificate.pem'
key_file = f'assets{os.sep}security{os.sep}key.pem'
ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(cert_file, keyfile=key_file)
ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3

http_server = HTTPServer(port=9000, ssl_context=ssl_context)

Oscilloscope(id='oscilloscope').run(servers=[http_server])
# OR
Oscilloscope(
    id='oscilloscope',
).run_with_http_server(
    port=9000,
    ssl_context=ssl_context,
)
```

## Routes & HTTP Methods

The default URL path or HTTP routes are created as follows:

| Resource          | Path                           | Description                  | HTTP Handler                   | Default Method                                                 |
| ----------------- | ------------------------------ | ---------------------------- | ------------------------- | -------------------------------------------------------------- |
| Property          | `/<thing-id>/<foo-bar>`        | for property `foo_bar`       | `PropertyHandler`         | `GET` for read <br/> `PUT` for write <br/> `DELETE` for delete |
| Action            | `/<thing-id>/<foo-bar>`        | for action `foo_bar`         | `ActionHandler`           | `POST`                                                         |
| Event             | `/<thing-id>/<foo-bar>`        | for event `foo_bar`          | `EventHandler`            | `GET`                                                          |
| Thing Model       | `/<thing-id>/resources/wot-tm` | to get the Thing Model       | - acts as property -      | `GET`                                                          |
| Thing Description | `/<thing-id>/resources/wot-td` | to get the Thing Description | `ThingDescriptionHandler` | `GET`                                                          |

All python names underscores are converted to hyphens in the URL paths for every resource (property, action or event), and the Thing ID is a global prefix.

One can register custom routes and HTTP methods as follows:

```python linenums="1" title="Custom Routes"
from hololinked.server import HTTPServer

server = HTTPServer(port=9000)

server.add_property('/channels/data/A', Oscilloscope.channel_A)
server.add_action(
    '/channels/data/A/with-offset', 
    Oscilloscope.get_channel_data_with_offset, 
    method='GET',
)
server.add_event('/channels/data/A/stream', Oscilloscope.channel_A_data_event)

Oscilloscope(id='oscilloscope').run(servers=[server])
```

## Path Parameters

There are predefined URL path parameters with specific connotation:

| Parameter | Format Example | Description |
|-----------|----------------|-------------|
| oneway invokation | `https://localhost:8080/<thing-id>/<action-name>?oneway=true` | invokes an action in a fire & forget fashion |
| noblock invokation | `https://localhost:8080/<thing-id>/<action-name>?noblock=true` | schedules an action and returns a message ID that can be used to retrieve the reply |
| fetch execution logs | `https://localhost:8080/<thing-id>/<action-name>?fetchExecutionLogs=true` | fetches the logs that were accumulated during the execution of an operation |
| invokation timeout | `https://localhost:8080/<thing-id>/<action-name>?invokationTimeout=7` | Creates a custom invokation timeout of a specific operation |
| execution timeout | `https://localhost:8080/<thing-id>/<action-name>?executionTimeout=7` | Creates a custom execution timeout of a specific operation |
| ignore errors for metadata generation |  `https://localhost:8080/<thing-id>/resources/wot-tm?ignore_errors=true` | ignore errors during Web of Things Thing Description or Thing Model generation to generate at least a partial working model | 

All path parameters can be combined. 

For `GET` requests, the payload needs to be specified as path parameters and the names should not overlap with the above specified fields.

## Recognised Headers

There are specific headers that are respected by the server:

| Headers | Format Example | Description |
|---------|----------------|-------------|
| X-Message-ID |  | Message ID to read reply for no block operation |
| X-API-Key, Authorization | | Used by security schemes |

## Allow CORS

On the web browser, one may want to access the HTTP server from a different domain name, especially during development with `localhost` or in private networks. In such cases, one needs to enable CORS headers:

```python linenums="1" title="Enable CORS" hl_lines="8"
http_server = HTTPServer(port=9000, config=dict(cors=True))
Oscilloscope(id='oscilloscope').run(servers=[http_server])
# OR
Oscilloscope(
    id='oscilloscope',
).run_with_http_server(
    port=9000,
    config=dict(cors=True),
)
```

CORS headers are set only for authenticated clients.

> Note that for localhost, each port is considered a different domain. A web application and a server running on different ports on same machine will not be recognised to be in the same domain.

!!! warning
    CORS does not prevent execution of an operation on the server. It only prevents web browsers from reading the response of an HTTP request and is not a security mechanism in itself that can protect a HTTP server. Use [security schemes](../../security) to protect your server instead.

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
