from hololinked.client import ClientFactory

energy_meter = ClientFactory.http(url="http://localhost:8000/energy-meter")
# energy_meter = ClientFactory.zmq(id="energy_meter", access_point="IPC")


def event_cb(event_data):
    print(event_data)


energy_meter.subscribe_event(name="data_point_event", callbacks=event_cb)


def event_cb1(event_data):
    print(event_data)


def event_cb2(event_data):
    print("Second callback", event_data)


energy_meter.subscribe_event(
    name="statistics_event", callbacks=[event_cb1, event_cb2]
)

energy_meter.subscribe_event(
    name="statistics_event",
    callbacks=[event_cb1, event_cb2],
    thread_callbacks=True,
)
