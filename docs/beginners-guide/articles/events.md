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

    In the asynchronous mode, the `subscribe_event` method creates an event listening task in the running async loop:

    ```py title="Subscription" linenums="1" hl_lines="9"
    from hololinked.client import ClientFactory

    energy_meter = ClientFactory.http(url="http://localhost:8000/energy-meter")
    # energy_meter = ClientFactory.zmq(id="energy_meter", access_point="IPC")

    def event_cb(event_data):
        print(event_data)

    energy_meter.subscribe_event(
        name="data_point_event",
        callbacks=event_cb,
        asynch=True
    )
    ```

---

One can also supply multiple callbacks which may called in series, threaded or async:

=== "sequential"

    The background thread that listens to the event executes the callbacks in series in its own thread:

    ```py title="Sequential Callbacks" linenums="1" hl_lines="9"
    def event_cb1(event_data):
        print("First Callback", event_data)

    def event_cb2(event_data):
        print("Second callback", event_data)

    energy_meter.subscribe_event(
        name="statistics_event",
        callbacks=[event_cb1, event_cb2]
    )
    ```

    So please be careful while using GUI frameworks like PyQt where you can paint the GUI only from the main thread.
    You would need to use signals and slots or other mechanisms.

=== "threaded"

    The background thread that listens to the event executes the callbacks by spawning new threads:

    ```py title="Thread Callbacks" linenums="1" hl_lines="9-10"
    def event_cb1(event_data):
        print("First Callback", event_data)

    def event_cb2(event_data):
        print("Second callback", event_data)

    energy_meter.subscribe_event(
        name="statistics_event",
        callbacks=[event_cb1, event_cb2],
        thread_callbacks=True
    )
    ```
    Again, please be careful while using GUI frameworks like PyQt where you can paint the GUI only from the main thread.

=== "async"

    Applies only when listening to event with `async=True`, the `async` method creates new tasks in the current loop:

    ```py title="Thread Callbacks" linenums="1"
    async def event_cb1(event_data):
        print("First Callback", event_data)
        await some_async_function1(event_data)

    async def event_cb2(event_data):
        print("Second callback", event_data)
        await some_async_function2(event_data)

    energy_meter.subscribe_event(
        name="statistics_event",
        callbacks=[event_cb1, event_cb2],
        asynch=True,
        create_task_for_cbs=True
    )
    ```

---

To unsubscribe:

```py title="Unsubscription" linenums="1"
energy_meter.unsubscribe_event(name="data_point_event")
```

## Payload Schema

Schema may be supplied for the validation of the event data on the client:

```py title="" linenums="1" hl_lines="13"
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

| Key          | Supported | Comment                                                                            |
| ------------ | --------- | ---------------------------------------------------------------------------------- |
| subscription | ✖         |                                                                                    |
| data         | ✔         | payload schema for the event                                                       |
| dataResponse | ✖         | schema for response message after arrival of an event, will be supported in future |
| cancellation | -         | Server sent events can be cancelled by the client directly                         |
