import datetime, threading
from hololinked.server import Thing, Event, Property
import json


class GentecMaestroEnergyMeter(Thing):
    """
    Simple example to implement acquisition loops and events
    to push the captured data. Customize it for your application or 
    implement your own.
    """

    data_point_event = Event(friendly_name='data-point-event', 
                            doc='Event raised when a new data point is available',
                            label='Data Point Event')
    
    statistics_event = Event(friendly_name='statistics-event',
                            doc='Event raised when a new statistics is available',
                            label='Statistics Event')

    def loop(self):
        self._run = True
        while self._run:
            self._last_measurement = self.current_value
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.data_point_event.push(dict(
                    timestamp=timestamp, 
                    energy=self._last_measurement
                ))
            if self._statistics_enabled:
                self.statistics_event.push(self.statistics)

    statistics = Property(doc="Get latest computed statistics", 
                        readonly=True)

    @statistics.getter
    def get_statistics(self):
        """get latest computed statistics"""
        raw_data = self.serial_comm_handle.execute_instruction("*VSU\r\n", 1000)
        if raw_data is not None:
            data = raw_data.split('\t')
            ret = {}
            for qty in data:
                name, value = qty.split(':')
                ret[name] = float(value)
            return ret
        raise RuntimeError("Could not get statistics")
    
   
    data_point_event_schema = {
        "type": "object",
        "properties": {
            "timestamp": {"type": "string"},
            "energy": {"type": "number"}
        },
        "required": ["timestamp", "energy"]
    }

    # Convert the schema to JSON
    data_point_event = Event(friendly_name='data-point-event', 
                            doc='Event raised when a new data point is available',
                            label='Data Point Event', schema=data_point_event_schema)
  
    
if __name__ == "__main__":
    threading.Thread(target=start_https_server).start()
    # add your HTTP server starter code in the above method
    GentecMaestroEnergyMeter(
        instance_name='gentec-maestro'
    ).run(zmq_protocols='IPC')