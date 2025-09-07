# Events

[API Reference](../../api-reference/events/index.md)

Events are pushed to the client through a publish-subscribe mechanism through all the protocols. Call `push()` method on the event to publish data to clients:

```py title="Definition" linenums="1" hl_lines="21-23"
--8<-- "docs/beginners-guide/code/events/definition.py:3:25"
```

## Subscription

One can subscribe to the event using the attribute name:

=== "threaded"

    In the default synchronous mode, the `subscribe_event` method spawns a thread that listens to the event in backgound:

    ```py title="Subscription" linenums="1" hl_lines="9"
    from hololinked.client import ClientFactory

    energy_meter = ClientFactory.http(url="http://localhost:8000/energy-meter")
    # energy_meter = ClientFactory.zmq(id="energy_meter", access_point="IPC")

    def event_cb(event_data):
        print(event_data)

    energy_meter.subscribe_event(name="data_point_event", callbacks=event_cb)
    ```

=== "async"

    In the asynchronous mode, the `subscribe_event` method creates an event listening task in the running async loop. This requires the client to be running in an async loop, otherwise no events will be received although the server will be publishing it:

    ```py title="Subscription" linenums="1" hl_lines="9"
    from hololinked.client import ClientFactory

    energy_meter = ClientFactory.http(url="http://localhost:8000/energy-meter")
    # energy_meter = ClientFactory.zmq(id="energy_meter", access_point="IPC")

    def event_cb(event):
        print(event)

    energy_meter.subscribe_event(
        name="data_point_event",
        callbacks=event_cb,
        asynch=True
    )
    ```

The callback function(s) must accept a single argument which is the event data payload, an instance of `SSE` object. The payload can be accessed as using the `data` attribute:

```py title="Event Data" linenums="1" hl_lines="9"
def event_cb(event):
    print(event.data)
```

> The `SSE` object also contains metadata like `id`, `event` name and `retry` interval, but these are currently not well supported. Improvements in the future are expected.

Each subscription creates a new event stream. One can also supply multiple callbacks which may called in series or concurrently:

=== "sequential"

    The background thread that listens to the event executes the callbacks in series in its own thread:

    ```py title="Sequential Callbacks" linenums="1" hl_lines="9"
    def event_cb1(event):
        print("First Callback", event.data)

    def event_cb2(event):
        print("Second callback", event.data)

    energy_meter.subscribe_event(
        name="statistics_event",
        callbacks=[event_cb1, event_cb2]
        # This also works for async where all callbacks are awaited in series
    )
    ```

=== "threaded"

    The background thread that listens to the event executes the callbacks by spawning new threads:

    ```py title="Thread Callbacks" linenums="1" hl_lines="9-10"
    def event_cb1(event):
        print("First Callback", event.data)

    def event_cb2(event):
        print("Second callback", event.data)

    energy_meter.subscribe_event(
        name="statistics_event",
        callbacks=[event_cb1, event_cb2],
        concurrent=True
    )
    ```

=== "async"

    The event listening task creates newer tasks in the running event loop:

    ```py title="Thread Callbacks" linenums="1" hl_lines="12-13"
    async def event_cb1(event):
        print("First Callback", event.data)
        await some_async_function1(event.data)

    async def event_cb2(event):
        print("Second callback", event.data)
        await some_async_function2(event.data)

    energy_meter.subscribe_event(
        name="statistics_event",
        callbacks=[event_cb1, event_cb2],
        asynch=True,
        concurrent=True
    )
    ```

> In GUI frameworks like PyQt, you cannot paint the GUI from the event thread. You would need to use signals and slots or other mechanisms to update the GUI to hand over the data.

---

To unsubscribe:

```py title="Unsubscription" linenums="1"
energy_meter.unsubscribe_event(name="data_point_event")
```

All subscriptions to the same event are removed.

## Payload Schema

Schema may be supplied for the validation of the event data on the client using pydantic or JSON schema:

```py title="Payload Schema" linenums="1" hl_lines="13"
class GentecMaestroEnergyMeter(Thing):

    data_point_event_schema = {
        "type": "object",
        "properties": {
            "timestamp": {"type": "string", "format": "date-time"},
            "energy": {"type": "number"}
        },
        "required": ["timestamp", "energy"],
    }

    data_point_event = Event(
        doc="Event raised when a new data point is available",
        label="Data Point Event",
        schema=data_point_event_schema,
    )
```

There is no separate validation on the server side.

> There is no validation on the client side currently implemented in `hololinked.client`. This will be added in future releases.

???+ "Schema as seen in Thing Description"

    ```py
    GentecMaestro.data_point_event.to_affordance().json()
    ```

    ```json
    {
        "description": "Event raised when a new data point is available",
        "data": {
            "type": "object",
            "properties": {
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "energy": {
                    "type": "number"
                }
            },
            "required": ["timestamp", "energy"]
        }
    }
    ```

## Thing Description Metadata

| Key          | Supported | Comment                                                    |
| ------------ | --------- | ---------------------------------------------------------- |
| subscription | ✖         |                                                            |
| data         | ✔         | payload schema for the event                               |
| dataResponse | ✖         | will be supported in a future release                      |
| cancellation | -         | Server sent events can be cancelled by the client directly |
