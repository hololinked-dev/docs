from hololinked.client import ObjectProxy

spectrometer = ObjectProxy(
    server_id="spectrometer", thing_id="spectrometer", access_point="IPC"
)
# synchronous call is always available, not optional
spectrometer.serial_number = "USB2+H15897"
spectrometer.invoke_action("connect", trigger_mode=2, integration_time=1000)
spectrometer.set_properties(integration_time=100, nonlinearity_correction=False)
spectrometer.disconnect()


# ----------------------------
# async calls example
import asyncio

spectrometer = ObjectProxy(
    server_id="spectrometer", thing_id="spectrometer", access_point="IPC"
)


async def setup_spectrometer():
    # write a property
    await spectrometer.async_write_property("serial_number", "USB2+H15897")
    # invoke action
    await spectrometer.async_invoke_action(
        "connect", trigger_mode=2, integration_time=1000
    )
    # write multiple properties
    await spectrometer.async_write_multiple_properties(
        background_correction="AUTO", nonlinearity_correction=False
    )
    await spectrometer.async_invoke_action("start_acquisition")


asyncio.run(setup_spectrometer())


# ----------------------------
# running multiple clients
async def async_example(spectrometer: ObjectProxy):
    await spectrometer.async_invoke_action("start_acquisition")
    for i in range(1000):
        await spectrometer.async_read_property("last_intensity")
        await asyncio.sleep(0.025)
    await spectrometer.async_invoke_action("stop_acquisition")


spectrometer1_proxy = ClientFactory.zmq(
    instance_name="spectrometer1", protocol="IPC", async_mixin=True
)
spectrometer2_proxy = ClientFactory.zmq(
    instance_name="spectrometer2", protocol="IPC", async_mixin=True
)
spectrometer3_proxy = ClientFactory.zmq(
    instance_name="spectrometer3", protocol="IPC", async_mixin=True
)

asyncio.get_event_loop().run_until_complete(
    asyncio.gather(
        *[
            async_example(spectrometer)
            for spectrometer in [
                spectrometer1_proxy,
                spectrometer2_proxy,
                spectrometer3_proxy,
            ]
        ]
    )
)
