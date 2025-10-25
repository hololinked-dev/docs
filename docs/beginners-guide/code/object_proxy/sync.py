from hololinked.client import ClientFactory

spectrometer = ClientFactory.http(
    url="http://localhost:8000/my-thing/resources/wot-td"
)
spectrometer = ClientFactory.zmq(
    server_id="test-server",
    thing_id="my-thing",
    access_point="tcp://localhost:5555",
)
spectrometer = ClientFactory.zmq(
    server_id="test-server", thing_id="my-thing", access_point="IPC"
)

# ----------------------------
# create client
spectrometer = ClientFactory.http(
    url="http://localhost:8000/spectrometer/resources/wot-td"
)
# setting property by name
spectrometer.write_property("serial_number", "USB2+H15897")
# setting property with dot operator leads to the same effect
spectrometer.serial_number = "USB2+H15897"

# similar API for reading property
print(spectrometer.serial_number)  # prints 'USB2+H15897'
print(spectrometer.read_property("serial_number"))  # prints 'USB2+H15897'


# ----------------------------
# normal action call
# with keyword arguments
spectrometer.connect(trigger_mode=2, integration_time=1000)
spectrometer.disconnect()
# with positional arguments
spectrometer.connect(2, 1000)
spectrometer.disconnect()
# with both positional and keyword arguments
spectrometer.connect(2, integration_time=1000)
spectrometer.disconnect()


# ----------------------------
# using invoke_action
spectrometer.connect()
spectrometer.invoke_action("disconnect")
# keyword arguments
spectrometer.invoke_action("connect", trigger_mode=2, integration_time=1000)
spectrometer.invoke_action("disconnect")
# positional arguments
spectrometer.invoke_action("connect", 2, 1000)
spectrometer.invoke_action("disconnect")
# with both positional and keyword arguments
spectrometer.invoke_action("connect", 2, integration_time=1000)
spectrometer.invoke_action("disconnect")

# ----------------------------
# read and write multiple properties
print(
    spectrometer.read_multiple_properties(
        names=["integration_time", "trigger_mode"]
    )
)
spectrometer.write_multiple_properties(
    integration_time=100, nonlinearity_correction=False
)  # pass properties as keyword arguments
print(
    spectrometer.read_multiple_properties(
        names=[
            "state",
            "nonlinearity_correction",
            "integration_time",
            "trigger_mode",
        ]
    )
)

# ----------------------------
# oneway action call
spectrometer.invoke_action(
    "connect", trigger_mode=2, integration_time=1000, oneway=True
)
spectrometer.invoke_action("disconnect", oneway=True)
# oneway action with positional arguments
spectrometer.invoke_action("connect", 2, 1000, oneway=True)
# write multiple properties one way
spectrometer.write_multiple_properties(
    integration_time=100, nonlinearity_correction=False, oneway=True
)
# read multiple properties one way not supported
# as return value is mandatory
print(
    spectrometer.read_multiple_properties(
        names=[
            "state",
            "nonlinearity_correction",
            "integration_time",
            "trigger_mode",
        ]
    )
)
# write property one way
spectrometer.write_property("integration_time", 100, oneway=True)


# ----------------------------
# no block calls
spectrometer1_proxy = ClientFactory.zmq(
    server_id="server1",
    thing_id="spectrometer1",
    access_point="tcp://mypc1:8000",
)
spectrometer2_proxy = ClientFactory.http(
    url="http://mypc2:8000/spectrometer2/resources/wot-td"
)

reply_ids = []

for client in [spectrometer1_proxy, spectrometer2_proxy]:
    reply_id = client.write_property(
        "background_correction", "AUTO", noblock=True
    )
    reply_ids.append(reply_id)

# no return value expected, exceptions will be raised on read_reply and will not be None
assert all(client.read_reply(reply_id) is None for reply_id in reply_ids)
reply_ids = []

for client in [spectrometer1_proxy, spectrometer2_proxy]:
    reply_id = client.invoke_action(
        "start_acquisition",
        trigger_mode=2,
        integration_time=1000,
        noblock=True,
    )
    reply_ids.append(reply_id)

# no return value expected, exceptions will be raised on read_reply and will not be None
assert all(client.read_reply(reply_id) is None for reply_id in reply_ids)

reply_id3 = spectrometer1_proxy.invoke_action("disconnect")
reply_id4 = spectrometer2_proxy.invoke_action("disconnect")
# say disconnecting take 1 second per spectrometer
spectrometer1_proxy.read_reply(reply_id3, timeout=0.05)  # 50 milliseconds
# can raise TimeoutError
