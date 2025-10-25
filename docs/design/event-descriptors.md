# Event Descriptors

The main purpose of event descriptors is to return a pub-sub object that can be used to publish events. This ensures event delivery that is controlled by the server side. The event payload is defined by a schema,
which can be either a JSON schema or a Pydantic model.

```python linenums="1"
class Energy(BaseModel):
    """A history of energy data points along with the timsestamp of measurement"""
    timestamp: float
    energy: float

class Statistics(BaseModel):
    """Statistics of the energy data points"""
    min: float
    max: float
    avg: float
    pulse_count: Annotated[int, Field(ge=0, description="Number of pulses detected")]

class GentecMaestroEnergyMeter(Maestro):
    """
    Simple example to implement acquisition loops and events
    to push the captured data. Customize it for your application or
    implement your own.
    """

    data_point_event = Event(data_schema=Energy.model_json_schema(),
                            doc='Event raised when a new data point is available',
                            label='Data Point Event')

    statistics_event = Event(data_schema=Statistics.model_json_schema(),
                            doc='Event raised when a new statistics is available',
                            label='Statistics Event')

    def loop(self):
        self._run = True
        while self._run:
            if self.new_value_ready: # property that checks if a new value is available
                self._last_measurement = self.current_value # property that returns the current value
                timestamp = datetime.datetime.now()
                timestamp = timestamp.strftime("%H:%M:%S") + '.{:03d}'.format(int(timestamp.microsecond /1000))
                self.data_point_event.push(EnergyDataPoint(timestamp=timestamp, energy=self._last_measurement))
                if self._statistics_enabled:
                    self.statistics_event.push(self.statistics)
                self.logger.debug(f"New data point : {self._last_measurement} J")
            else:
                self.logger.debug("No new data point available")
            # auto serialization of the event data happens when a json() method is implemented,
            # which has been done in the dataclass
            time.sleep(self.measurement_gap)
```
