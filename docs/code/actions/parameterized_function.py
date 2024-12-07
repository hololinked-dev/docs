import multiprocessing
from hololinked.server import Thing, action
from hololinked.param import ParameterizedFunction
from hololinked.server.properties import ClassSelector
from hololinked.client import ObjectProxy
import numpy



class OceanOpticsSpectrometer(Thing):
    """
    Test object for testing the server
    """

    def __init__(self, instance_name, **kwargs):
        super().__init__(instance_name=instance_name, **kwargs)
        self.last_intensity = numpy.array([0 for i in range(1024)])

    last_intensity = ClassSelector(default=None, allow_None=True, class_=numpy.ndarray, 
                	doc="last measurement intensity (in arbitrary units)")

    @action() # non-JSON arguments are not supported with HTTP
    class subtract_custom_background(ParameterizedFunction):
        """Test function with return value"""

        custom_background = ClassSelector(default=None, allow_None=True, 
                                class_=numpy.ndarray, 
                                doc="background intensity to subtract (in arbitrary units)") 
        
        def __call__(self, 
                instance : "OceanOpticsSpectrometer", 
                custom_background : numpy.ndarray) -> numpy.ndarray:
            return instance.last_intensity - custom_background

    @action()
    def subtract_custom_background(self, custom_background):
        if not isinstance(custom_background, numpy.ndarray):
            raise TypeError("custom_background must be a numpy array")
        return self.last_intensity - custom_background
    

   
def client():
    client = ObjectProxy(instance_name='spectrometer', protocol='IPC', 
                        serializer='pickle')
    ret = client.subtract_custom_background(
        custom_background=numpy.array([1 for i in range(len(client.last_intensity))]))
    print("reply", type(ret) , ret)
    # prints - reply <class 'numpy.ndarray'> [-1 -1 -1 ... -1 -1 -1]

def server():
    O = OceanOpticsSpectrometer(
        instance_name='spectrometer',
        serial_number='S14155',
        zmq_serializer='pickle'	
    )
    O.run(zmq_protocols='IPC')

if __name__ == "__main__":
    multiprocessing.Process(target=server).start()
    client()