from hololinked.client import ObjectProxy

spectrometer_proxy = ObjectProxy(instance_name='spectrometer', 
                                protocol='IPC', async_mixin=True)
# synchronous call is always available, not optional
spectrometer_proxy.serial_number = 'USB2+H15897'
spectrometer_proxy.invoke_action('connect', trigger_mode=2, integration_time=1000)
spectrometer_proxy.set_properties(
    integration_time=100, 
    nonlinearity_correction=False
)
spectrometer_proxy.disconnect()


#----------------------------
# async calls example
import asyncio
# invoke action
asyncio.run(spectrometer_proxy.async_invoke_action('connect', 
                                trigger_mode=2, integration_time=1000))
# get multiple properties
asyncio.run(spectrometer_proxy.async_write_multiple_properties(
    integration_time=100, 
    nonlinearity_correction=False
))
# set multiple properties
asyncio.run(spectrometer_proxy.async_read_multiple_properties(
    names=["integration_time", "trigger_mode"]))
# get single property
asyncio.run(spectrometer_proxy.async_read_property('serial_number'))
# set single property
asyncio.run(spectrometer_proxy.async_write_property('serial_number', 
                                                'USB2+H15897'))

#----------------------------
# running multiple clients
async def async_example(spectrometer : ObjectProxy):
    await spectrometer.async_invoke_action("start_acquisition")
    for i in range(1000):
        await spectrometer.async_read_property("last_intensity")
        await asyncio.sleep(0.025)
    await spectrometer.async_invoke_action("stop_acquisition")

spectrometer1_proxy = ObjectProxy(instance_name='spectrometer1', 
                                protocol='IPC', async_mixin=True)
spectrometer2_proxy = ObjectProxy(instance_name='spectrometer2', 
                                protocol='IPC', async_mixin=True)
spectrometer3_proxy = ObjectProxy(instance_name='spectrometer3', 
                                protocol='IPC', async_mixin=True)

asyncio.get_event_loop().run_until_complete(asyncio.gather(
    *[async_example(spectrometer) for spectrometer in [
        spectrometer1_proxy, spectrometer2_proxy, spectrometer3_proxy]]
))