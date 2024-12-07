from collections import deque
from dataclasses import dataclass
import datetime
import sys 
import threading
import time 

from serial_utility import SerialCommunication
from hololinked.server import Thing, action, Event, Property
from hololinked.server.properties import Number, String, Integer, Boolean
from .sensors import allowed_sensors

POWER_WATT  = "POWER_WATT"
ENERGY = "ENERGY"
SINGLE_SHOT_ENERGY = "SSE"
FLUENCE = "FLUENCE"
IRRADIANCE = "IRRADIANCE"
ENERGY_DOSE = "ENEERGY DOSE"
POWER_DBM = "DBM"
NO_DETECTOR = "NO DETECTOR"
ERROR_MODE_NOT_READ = "ERROR, MODE NOT READ"

display_mode = {
    "0" : POWER_WATT,
    "1" : ENERGY, 
    "2" : SINGLE_SHOT_ENERGY,
    "3" : FLUENCE,
    "4" : IRRADIANCE,
    "5" : ENERGY_DOSE,
    "6" : POWER_DBM,
    "7" : NO_DETECTOR
}

OUT_OF_RANGE = "OUT OF RANGE"
SAVE_DETECTOR_SETTINGS_ACKNOWLEDGEMENT = "Your current configuration has been saved and will be used at startup."
LOAD_DETECTOR_SETTINGS_ACKNOWLEDGEMENT = "Done!"
ACKNOWLEDGED = "ACK"


class GentecOpticalEnergyMeter(Thing):
    """
    Control Gentec EO optical energy meters through serial interface using this class. 
    """
    def __init__(self, instance_name, serial_url = "COM4", **kwargs):
        super().__init__(instance_name=instance_name, serial_url=serial_url, **kwargs)
        self.serial_comm_handle = SerialCommunication(
                                            instance_name='comm-handle', 
                                            serial_url=serial_url, 
                                            baud_rate=115200,
                                            read_timeout=0.1,
                                            write_timeout=0.1,
                                            **kwargs)
        self.serial_comm_handle.connect()
        self.set_sensor(kwargs.get('sensor', 'QE25LP-S-MB'))
        self._analog_output_enabled = False

    @action(URL_path='/set-sensor', input_schema={'type': 'string'})
    def set_sensor(self, value : str):
        """
        Set the attached sensor to the meter under control.
        Sensor should be defined as a class and added to the AllowedSensors dict. 
        """
        if value in list(allowed_sensors.keys()):
            sensor = allowed_sensors[value](instance_name='sensor')
            sensor.configure_meter(self)
            self._attached_sensor = sensor
        else:
            raise ValueError("Unknown sensor : {}".format(value))

   
    # This is how you define properties, they generally become instance attributes automatically.
    min_wavelength = Integer(default=200, bounds=(200,1000), metadata=dict(unit='nm'),
                            doc="""Software limit of the minimum allowed wavelength of the sensor, 
                            can be set as a different value from the sensor specification allowed limit. 
                            This value is useful for setting experimental measurement constraints. 
                            When setting the wavelength on the sensor, the given value is checked against 
                            this software limit.""") # type: int

    # claiming 'type: int' indicates the native type of the data so that code editors 
    # can provide better suggestions.
    
    max_wavelength = Integer(default=2100, bounds=(400,10000), metadata=dict(unit='nm'),
                            doc="""Software limit of the maximum allowed wavelength of the sensor, 
                            can be set as a different value from the sensor specification allowed limit. 
                            This value is useful for setting experimental measurement constraints. 
                            When setting the wavelength on the sensor, the given value is checked against 
                            this software limit.""") # type: int
                        
    min_offset = Number(default=sys.float_info.min, 
                        doc="""Software limit of the minimum allowed offset of the measurement value.
                        Useful for setting experimental measurement constraints. When setting the 
                        offset on the device, the given value is checked against this software limit. 
                        """) # type: float
    
    max_offset = Number(default=sys.float_info.max, 
                        doc="""Software limit of the maximum allowed offset of the measurement value. 
                        Useful for setting experimental measurement constraints. When setting the 
                        offset on the device, the given value is checked against this software limit. 
                        """) # type: float
    
    min_multiplier = Number(default=sys.float_info.min, 
                        doc="""Software limit of the minimum allowed multiplier of the measurement value. 
                        Useful for setting experimental measurement constraints. When setting the 
                        multiplier on the device, the given value is checked against this software limit 
                        """) # type: float
    
    max_multiplier = Number(default=sys.float_info.max,
                        doc="""Software limit of the maximum allowed multiplier of the measurement value.
                        Useful for setting experimental measurement constraints. When setting the 
                        multiplier on the device, the given value is checked against this software limit 
                        """) # type: float
   
    #---------------MEASUREMENT COMMANDS
    def read_current_value(self):
        """energy value of the latest measurement read"""
        value = self.serial_comm_handle.execute_instruction("*CVU", 100)[:-2]
        if value == 'New Data Not Available':
            return float("NaN")
        try:
            floatval = float(value)   
            if floatval >= 1e38: # if value == "3.40282e+038" or value == "3.402819e+38":
                return float("NaN")
            else:
                return floatval
        except Exception as ex:
            self.logger.error("error during measurement - " + str(ex))
            return float("NaN")

    # supply fget if you want to make a custom getter/value generator for the property
    current_value = Number(default=-1.0, fget=read_current_value, readonly=True,
                        doc="energy value of the latest measurement read", metadata=dict(unit='J'))
    # specify unit of property in a metadata dictionary with unit keyword. 

    def is_new_value_ready(self):
        """Did a measurement happen since the last read?"""
        value = self.serial_comm_handle.execute_instruction("*NVU", 100)
        if value[:-2] == "New Data Available":
            return True
        else: 
            return False
    
    new_value_ready = Boolean(default=False, fget=is_new_value_ready, readonly=True, 
                        doc="Did a measurement happen since the last read?")
      
    analog_output_enabled = Boolean(default=False, readonly=True, 
                fget=lambda self: self._analog_output_enabled
            )
    
    # some more actions
    @action()
    def enable_analog_output(self):
        self.serial_comm_handle.execute_instruction("*ANO1")
        self._analog_output_enabled = True
        # There are better ways to find if analog output is enabled than in this way,
        # but this is just an example.

    @action()
    def disable_analog_output(self):
        self.serial_comm_handle.execute_instruction("*ANO0")
        self._analog_output_enabled = False
   
    range = Integer(default=None, doc="current range of the measurement")
    # also you can use getter and setter decorator to specify get and set methods for a property
    @range.getter
    def get_range(self) -> int:
        """reads the current scale of measurement"""
        return int(self.serial_comm_handle.execute_instruction("*GCR", 100)[-4:-2]) 
    
    @range.setter
    def set_range(self, value) -> None:
        """sets current scale of measurement"""
        self.serial_comm_handle.execute_instruction("*SCS{}".format(str(value).zfill(2)))
    

    autorange = Boolean(default=None, doc="autoscale/autorange mode of the meter")

    @autorange.getter
    def get_autorange(self) -> bool:
        """checks if meter is in autoscale/autorange mode"""
        return bool(int(self.serial_comm_handle.execute_instruction("*GAS", 50)[-4:-2])) # Read last two characters

    @autorange.setter
    def set_autorange(self, value) -> None:
        """set or unset meter to autoscale/autorange"""
        self.serial_comm_handle.execute_instruction(f"*SAS{int(value)}")

    # for one-line getters, you can use lambda functions
    pulse_frequency = Number(readonly=True, default=None, allow_None=True, 
                    fget=lambda self: float(self.serial_comm_handle.execute_instruction("*GRR",100)[:-2]),
                    metadata=dict(unit='Hz'),
                    doc="the frequency of the pulses whose energy is being measured")
        

    #---------------MEASUREMENT SETUP COMMANDS
    def read_trigger_level(self) -> float:
        value = self.serial_comm_handle.execute_instruction("*GTL", 100)
        return float(value[15:-2]) 
        # 14 stands for the intial string "TRIGGER LEVEL:" in the reply and -2 stands for the \r\n ending

    def write_trigger_level(self, value : float) -> None:
        instruction = "*STL" + self.get_number_as_instruction(value)
        self.serial_comm_handle.execute_instruction(instruction)
    
    trigger_level = Number(default=None, allow_None=True,  bounds=(0.1, 99.9), step=0.01,
                        crop_to_bounds=True, fget=read_trigger_level, fset=write_trigger_level, 
                        doc="trigger level for measurement as a percentage of max value of current range",
                        metadata=dict(unit='%'))
    


    def read_wavelength(self):
        time.sleep(0.1)
        return int(self.serial_comm_handle.execute_instruction("*GWL", 100)[4:-2])
        # This instruction seems to have an issue. sometimes garbage data comes in before
        # although flush_input and flush_output are repeatedly called by the Serial Handler.
        # Issue is solved by adding a 100ms sleep. 

    def write_wavelength(self, value):
        if value >= self.min_wavelength and value <= self.max_wavelength: 
            value = str(value) # type: str
            value = ("0" * (5 - value.__len__())) + value 
            self.serial_comm_handle.execute_instruction("*PWC" + value)
        else:
            raise ValueError("wavelenght must be between {} and {} nm for writing to device.".format(
                            self.min_wavelength, self.max_wavelength))
    
    wavelength = Integer(fset=write_wavelength, fget=read_wavelength, # bounds are set by the sensor
                        doc="wavelength setting for energy calibration", metadata=dict(unit='nm'))
       
    @action()
    def set_current_value_as_zero_offset(self):
        self.serial_comm_handle.execute_instruction("*SOU")
    
    @action()
    def clear_zero_offset(self):
        self.serial_comm_handle.execute_instruction("*COU")

    @action()
    def clear_multiplier(self):
        self.multiplier = 1
             
    def read_multiplier(self):
        return float(self.serial_comm_handle.execute_instruction("*GUM", 100)[16:-2])

    def write_multiplier(self, value):   
        if value > self.min_multiplier and value < self.max_multiplier:
            self.serial_comm_handle.execute_instruction("*MUL"+self.get_number_as_instruction(value))
        else:
            raise ValueError("Multiplier out of range of software limit.")

    multiplier = Number(default=1.0, fget=read_multiplier, fset=write_multiplier,  
                    doc="multiplier for the measured value") 
  
    
    def read_offset(self) -> float:
        return float(self.serial_comm_handle.execute_instruction("*GUO", 100)[12:-2])
    
    def write_offset(self, value : float) -> None:
        if value > self.min_offset and value < self.max_offset:
            self.serial_comm_handle.execute_instruction("*OFF" + self.get_number_as_instruction(value))
        else:
            raise ValueError("Offset out of range of software limits")

    offset = Number(default=None, allow_None=True, fget=read_offset, fset=write_offset, 
                    doc="offset for the measurement" )

    zero_offset_active = Boolean(default=None, 
                            fget=lambda self : bool(int(self.serial_comm_handle.execute_instruction("*GZO", 100)[5:-2])),
                            doc="check if zero offset is currently active for measurements")

    #---------------INSTRUMENT AND DETECTOR INFORMATION COMMANDS

    @action()
    def ping_instrument(self):
        if self.serial_comm_handle.execute_instruction("*KPA", 100)[:-2] == ACKNOWLEDGED:
            return True 
        return False

    def read_version(self) -> str:
        return self.serial_comm_handle.execute_instruction("*VER",100)[:-2]

    version = String(fget=read_version, readonly=True, 
                    doc="Version string of the meter" ) 

    @action()
    def save_detector_settings(self):
        if self.serial_comm_handle.execute_instruction("*SDS", 200)[:-2] == SAVE_DETECTOR_SETTINGS_ACKNOWLEDGEMENT:
            return
        raise RuntimeError("Error saving detector settings")

    @action('/detector-settings/load')
    def load_detector_settings(self):
        if self.serial_comm_handle.execute_instruction("*LDS")[:-2] == LOAD_DETECTOR_SETTINGS_ACKNOWLEDGEMENT:
            return 
        raise RuntimeError("Error loading detector settings")
    
    #---------------UTILITY FUNCTIONS
    # a property that is only available locally and to the subclasses
    _data_string_maxlen = Integer(default=8, bounds=(0, None), allow_None=False, 
                                doc="maximum length of data string to be sent to the device", 
                                remote=False, class_member=True) # type: int
    
    # not an action, just a plain class method
    @classmethod 
    def get_number_as_instruction(cls, value):
        """
        convert a given float or int into a string of 8 characters. 
        useful for certain instructions, like setting offset, multiplier etc. Expection string is used for raising a type error when 
        the wrong type for the value is used. This is useful for throwing different types 
        of exception messages for the same TypeError when calling this function from different sections of the code. 
        This function is for internal use. 
        """
        value = str(value)
        if (value.__len__() > GentecOpticalEnergyMeter._data_string_maxlen):
            if value.find('.') > 8:
                raise ValueError(f"Given value greater than 8 characters - {value}")
            value = value[:8]
        if 'e' not in value:
            if "." in value:                    
                value = value + ( "0" * (GentecOpticalEnergyMeter._data_string_maxlen - value.__len__()))
            else:
                if '-' in value:
                    value = '-' + ( "0" * (GentecOpticalEnergyMeter._data_string_maxlen - value.__len__())) + value[1:]   
                else: 
                    value = ( "0" * (GentecOpticalEnergyMeter._data_string_maxlen - value.__len__())) + value        
        else: 
            e_index = value.find('e')
            len_after_e = value.__len__() - e_index 
            to_fill = GentecOpticalEnergyMeter._data_string_maxlen - len_after_e -e_index # e_index is also len_before_e
            if '-' in value[0:e_index]:
                if '.' in value[0:e_index]: 
                    value = value[0:e_index] + ( "0" * (to_fill)) + value[e_index:]  
                else: 
                    value = '-' + ( "0" * (to_fill)) + value[1:e_index] + value[e_index:]
            else:
                if '.' in value[0:e_index]:  
                    value = value[0:e_index] + ( "0" * (to_fill)) + value[e_index:]  
                else:    
                    value = ( "0" * (to_fill)) + value           
        return value
       
    #---------------DISPLAY COMMANDS
    def read_display_mode(self):
        return display_mode.get(self.serial_comm_handle.execute_instruction("*GMD", 100)[6], 
                                ERROR_MODE_NOT_READ)

    display_mode = String(default=ERROR_MODE_NOT_READ, readonly=True, fget=read_display_mode, 
                        doc="The measurement mode of the sensor. A mismoner, as it affects sensor measurement mode as well.")
    
    data_point_event = Event(name='data-point-event', 
                            doc='Event raised when a new data point is available',
                            label='Data Point Event')
    
    statistics_event = Event(name='statistics-event',
                            doc='Event raised when a new statistics is available',
                            label='Statistics Event')

    energy_history = Property(default=EnergyHistory(timestamp=deque(maxlen=300), energy=deque(maxlen=300)), 
                    readonly = True,
                    doc="Energy data as timestamps (datetime) in x-axis and energy value in y-axis (mJ)") # type: EnergyHistory

    measurement_gap = Number(default=0.1, bounds=(0, None), allow_None=True, 
                        doc="Time gap between two measurements, unit - seconds.")
    
    def __init__(self, instance_name, serial_url = "COM4", **kwargs):
        super().__init__(instance_name, serial_url, **kwargs)
        self._run = False
        self._measurement_worker = None
        self._last_measurement = None

    # not an action, just a plain method
    def loop(self):
        """runs the measurement/monitoring loop"""
        self._run = True
        while self._run:
            # Since the data point is a single float value and a timestamp which are very very small in size,
            # Its also sufficient if one implement's this loop purely at a client level. 
            # The server implementation is useful when the acquisition has to happen indenpendently of the
            # client.
            if self.new_value_ready:
                self._last_measurement = self.current_value
                timestamp = datetime.datetime.now()
                timestamp = timestamp.strftime("%H:%M:%S") + '.{:03d}'.format(int(timestamp.microsecond /1000))
                self.energy_history.timestamp.append(timestamp)
                self.energy_history.energy.append(self._last_measurement)
                self.data_point_event.push(EnergyDataPoint(timestamp=timestamp, energy=self._last_measurement))
                if self._statistics_enabled:
                    self.statistics_event.push(self.statistics)
                self.logger.debug(f"New data point : {self._last_measurement} J")
            else:
                self.logger.debug("No new data point available")
            # auto serialization of the event data happens when a json() method is implemented,
            # which has been done in the dataclass
            time.sleep(self.measurement_gap)


    @action()
    def start_acquisition(self):
        """Start the acquisition loop"""
        if not self._run: 
            self._measurement_worker = threading.Thread(target=self.loop)
            self._measurement_worker.start()
            self.logger.info("Acquisition loop started")
        else: 
            self.logger.info("Acquisition loop already running")

    @action()
    def stop_acquisition(self):
        """Stop the acquisition loop"""
        if self._run:
            self._run = False
            self._measurement_worker.join()
            self._measurement_worker = None
            self.logger.info("Acquisition loop stopped")
        else:
            self.logger.info("Acquisition loop already stopped")
      

@dataclass
class EnergyDataPoint:
    """A single data point of energy measurement along with the timestamp of measurement"""
    timestamp : str
    energy : float

    def json(self):
        return {
            'timestamp' : self.timestamp,
            'energy' : self.energy
        }
    

@dataclass 
class EnergyHistory:
    """A history of energy data points along with the timsestamp of measurement""" 
    timestamp : deque 
    energy : deque

    def json(self):
        return {
            'timestamp' : list(self.timestamp) if len(self) > 0 else None,
            'energy' : list(self.energy) if len(self) > 0 else None
        }
    
    def __len__(self):
        assert len(self.timestamp) == len(self.energy), "unequal length of timestamp and energy data detected"
        return len(self.timestamp)


