from hololinked.client import ObjectProxy

# events works also through inter-process communication, apart from TCP
energy_meter_proxy = ObjectProxy(instance_name='gentec-maestro', protocol='IPC') 

def event_cb(event_data):
    print(event_data)

energy_meter_proxy.subscribe_event(name='data_point_event', 
                                callbacks=event_cb)


def event_cb1(event_data):
    print(event_data)

def event_cb2(event_data):
    print("Second callback", event_data)

energy_meter_proxy.subscribe_event(
                                name='statistics_event', 
                                callbacks=[event_cb1, event_cb2]         
                            )

energy_meter_proxy.subscribe_event(
                                name='statistics_event', 
                                callbacks=[event_cb1, event_cb2], 
                                thread_callbacks=True
                            )