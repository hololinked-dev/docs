from hololinked.client import ObjectProxy

# events works also through inter-process communication, apart from TCP
energy_meter_proxy = ObjectProxy(instance_name='gentec-maestro', protocol='IPC') 

def event_cb(event_data):
    print(event_data)

energy_meter_proxy.subscribe_event(name='statistic-event', 
                                callbacks=event_cb)
# You can use either the friendly name or the attribute name of the event
energy_meter_proxy.subscribe_event(name='statistic_event', 
                                callbacks=event_cb)

def event_cb1(event_data):
    print(event_data)

def event_cb2(event_data):
    print("Second callback", event_data)

energy_meter_proxy.subscribe_event(name='statistic-event', 
                                callbacks=[event_cb1, event_cb2], 
                                # thread_callbacks=True
                            )
# thread callbacks by setting thread_callbacks=True in the subscribe_event method