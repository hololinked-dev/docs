from hololinked.client import ObjectProxy

spectrometer_proxy = ObjectProxy(instance_name='spectrometer') 
spectrometer_proxy.serial_num = 5 # raises AttributeError
# when server does not have property serial_num

spectrometer_proxy = ObjectProxy(instance_name='spectrometer') 
spectrometer_proxy.serial_num = 5 # OK!!

spectrometer_proxy = ObjectProxy(instance_name='spectrometer', 
                                protocol='IPC', handshake_timeout=10) 
spectrometer_proxy = ObjectProxy(instance_name='spectrometer', 
                                protocol='IPC', load_thing=False)
spectrometer_proxy.serial_number = 'USB2+H15897' # raises AttributeError
spectrometer_proxy.zmq_client.handshake()
spectrometer_proxy.load_thing() 
spectrometer_proxy.serial_number = 'USB2+H15897' # now OK!!

# wait only for 10 seconds for server to respond per call
spectrometer_proxy = ObjectProxy(instance_name='spectrometer', 
                                protocol='IPC', invokation_timeout=10) 

