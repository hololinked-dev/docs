from hololinked.server import Thing
from hololinked.server.properties import String, Number, TypedList

class OceanOpticsSpectrometer(Thing):
    """Spectrometer example object """

    serial_number = String(default="USB2+H15897", allow_None=False, readonly=True, 
                        doc="serial number of the spectrometer (string)",
                        label="serial number") # type: str

    integration_time = Number(default=1000, bounds=(0.001, None), allow_None=False,
                            crop_to_bounds=True, label="Integration Time (ms)",
                            doc="integration time of measurement in milliseconds")
    
    model = String(default=None, allow_None=True, constant=True, 
                label="device model", doc="model of the connected spectrometer")
    
    custom_background_intensity = TypedList(item_type=(float, int), default=None, 
                    allow_None=True, label="Custom Background Intensity",
                    doc="user provided background substraction intensity")
    
       
spectrometer = OceanOpticsSpectrometer(id='spectrometer1', serial_number='S14155')
    
# allow_None
spectrometer.custom_background_intensity = None # OK 
spectrometer.custom_background_intensity = [] # OK
spectrometer.custom_background_intensity = None # OK

# allow_None = False
spectrometer.integration_time = None # NOT OK, raises TypeError
spectrometer.integration_time = 2000 # OK

# readonly = True
spectrometer.serial_number = "USB2+H15897" # NOT OK - raises ValueError

# constant = True, mandatorily needs allow_None = True
spectrometer.model = None # OK - constant accepts None when initially None
spectrometer.model = 'USB2000+' # OK - can be set once 
spectrometer.model = None # NOT OK - raises ValueError