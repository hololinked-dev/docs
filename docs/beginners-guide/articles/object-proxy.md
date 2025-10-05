# Object Proxy

[API Reference](../../api-reference/clients/object-proxy.md)

`Thing` objects can be consumed using an `ObjectProxy` instance per protocol, where the interactions with 
a property, action or event are abstracted as operations like:

- Read/Write/Observe Property
- Invoke Action
- Subscribe/Unsubscribe Event

To instantiate an `ObjectProxy`, use the `ClientFactory`:

=== "HTTP"

    ```py title="HTTP Client" linenums="1" hl_lines="7-10"
    from hololinked.client import ClientFactory

    thing = ClientFactory.http(url="http://localhost:8000/my-thing/resources/wot-td")
    ```

    One needs to append `/resources/wot-td` to the URL to load a [Thing Description](https://www.w3.org/TR/wot-thing-description11/#introduction-td) 
    of the `Thing`. The `Thing Description` contains the metadata of the `Thing` like available properties, actions and events,
    their data types, forms (protocols and endpoints) etc. which can be used to create the `ObjectProxy`.

=== "ZMQ"

    ```py title="ZMQ Client" linenums="1" hl_lines="7-10"
    from hololinked.client import ClientFactory

    thing = ClientFactory.zmq(server_id="test-server", thing_id="my-thing", access_point="tcp://localhost:5555")
    ```

    For `IPC`:

    ```py title="ZMQ Client IPC" linenums="1" hl_lines="7-10"
    thing = ClientFactory.zmq(server_id="test-server", thing_id="my-thing", access_point="IPC")
    ```

    When using TCP, on the server side one may choose the address as `access_point="tcp://*:5555"`. 
    On the client side, however, one must use the explicit address, like `access_point="tcp://my-pc:5555"` or
    `access_point="tcp://localhost:5555"`.

    The `Thing Description` is fetched automatically from the server.


!!! Note

    Only one protocol is allowed per client. 

### read and write properties

To read and write properties by name, one can use `read_property` and `write_property`, or the dot operator:

```py title="read and write property" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/sync.py:8:17"
```

To read and write multiple properties:

```py title="read and write multiple properties" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/sync.py:48:55"
```

### invoke actions

One can also access actions with dot operator and supply positional and keyword arguments:

```py title="invoke actions with dot operator" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/sync.py:21:30"
```

One can also use `invoke_action` to invoke an action by name

```py title="invoke_action()" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/sync.py:34:45"
```

### oneway scheduling

`oneway` scheduling do not fetch return value and exceptions that might occur while executing a property or an action.
The server schedules the operation and returns an empty response to the client, allowing it to process further logic.
It is possible to set a property, set multiple or all properties or invoke an action in 
oneway. Other operations are not supported.

```py title="oneway=True" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/sync.py:58:73"
```

Simply provide the keyword argument `oneway=True` to the operation method.

Importantly, one cannot have an action argument or a property on the server named `oneway` as it is a
reserved keyword argument to such methods on the client. At least they become inaccessible on the `ObjectProxy`.

### no-block scheduling

`noblock` allows scheduling a property or action but collecting the reply later:

```py title="noblock=True" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/sync.py:77:101"
```

When using `read_reply()`, `noblock` calls raise exception on the client if the server raised its own exception or fetch the return value . 

<!-- We supported this before, but not now, TODO renable -->
<!-- Timeout exceptions are raised when there is no reply within timeout specified. 

.. literalinclude:: code/object_proxy/sync.py
    :language: python
    :linenos:
    :lines: 95-98 -->

!!! Note

    One cannot combine `oneway` and `noblock` - `oneway` takes precedence over `noblock`.
    
### async client-side scheduling

All operations on the `ObjectProxy` can also be invoked in an asynchronous manner within an `async` function. 
Simply prefix `async_` to the method name, like `async_read_property`, `async_write_property`, `async_invoke_action` etc.:

```py title="asyncio" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/async.py:12:28"
```

There is no support for dot operator based access. One may also note that `async` operations  
do not change the nature of the execution on the server side. 
`asyncio` on `ObjectProxy` is purely a client-side non-blocking network call, so that one can 
simultaneously perform other (async) operations while the client is waiting for the network operation to complete. 

!!! Note

    `oneway` and `noblock` are not supported for async calls due to the asynchronous nature of the 
    operation themselves. 

### subscribe and unsubscribe events

To subscribe to an event, use `subscribe_event` method and pass a callback function that accepts a single argument, the event data: 

```py title="subscribe_event()" linenums="1"
from hololinked.client.abstractions import SSE

def update_plot(event: SSE):
    plt.clf()  # Clear the current figure
    plt.plot(x_axis, event.data["spectrum"], color='red', linewidth=2)
    plt.title(f'Live Spectrum - {event.data["timestamp"]} UTC')
    # assuming event data is a dictionary with keys spectrum and timestamp

spectrometer.subscribe_event("intensity_measurement_event", callbacks=update_plot)
```

To unsubscribe from an event, use `unsubscribe_event` method:

```py title="unsubscribe_event()" linenums="1"
spectrometer.unsubscribe_event("intensity_measurement_event")
```

One can also supply multiple callbacks to be executed in series or concurrently, schedule an async callback etc., see [events section](./events.md#subscription) for further details. 

### customizations

##### foreign attributes on client

Normally, there cannot be user defined attributes on the `ObjectProxy` as the attributes on the client
must mimic the available properties, actions and events on the server. An accidental setting of an unknown
property must raise an `AttributeError` when not found on the server, instead of silently going through and setting 
said property on the client object itself:

```py title="foreign attributes raise AttributeError" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/customizations.py:3:5"
```

One can overcome this by setting `allow_foreign_attributes` to `True`:

```py title="foreign attributes allowed" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/customizations.py:7:12"
```

##### controlling timeouts for non-responsive server

For invoking any operation (say property read/write & action call), two types of timeouts can be configured:

- `invokation_timeout` - the amount of time the server has to wait for an operation to be scheduled
- `execution_timeout` - the amount of time the server has to complete the operation once scheduled

When the `invokation_timeout` expires, the operation is guaranteed to be never scheduled. When the `execution_timeout` expires, the operation is scheduled but returns without the expected response. In both cases, a `TimeoutError` is raised on the client side specifying the timeout type. If an operation is scheduled but not completed within the `execution_timeout`, the server may still complete the operation and there can be unknown side effects or client does not know about it.

```py title="timeout specification" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/customizations.py:20:27"
```

!!! Note

    Currently only a global specification is supported. In future, one may be able to specify timeouts per operation.


<!-- #### change handshake timeout

Before sending the first message to the server, a handshake is always done explicitly to not loose messages on the socket. 
This is an artificat of ZMQ (which also does its own handshake). `handshake_timeout` controls how long to look for the server,
in case the server takes a while to boot. 

```py title="timeout" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/customizations.py:10:11"
```

Default value is 1 minute. A `ConnectionError` is raised if the server cannot be contacted. 

One can also delay contacting the server by setting `load_thing` to False. But one has to manually performing the `handshake` later 
before loading the server resources:

```py title="timeout" linenums="1"
--8<-- "docs/beginners-guide/code/object_proxy/customizations.py:12:17"
```

If one is completely sure that server is online, one may drop the manual handshake.  -->

