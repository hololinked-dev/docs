from hololinked.server import Thing, StateMachine, action, Property
from hololinked.server.properties import String
from enum import StrEnum

class states(StrEnum):
    DISCONNECTED = "DISCONNECTED"
    ON = "ON"
    FAULT = "FAULT"
    MEASURING = "MEASURING"
    ALARM = "ALARM"


class Picoscope(Thing):
    """A PC Oscilloscope from Picotech"""

    @action()
    def start_acquisition(self):
        ... 

    @action()
    def stop_acquisition(self):
        ...
    
    @action()
    def connect(self):
        ...

    @action()
    def disconnect(self):
        ...

    serial_number = String()

    state_machine = StateMachine(
        states=['DISCONNECTED', 'ON', 'FAULT', 'ALARM', 'MEASURING'],
        initial_state='DISCONNECTED',
        DISCONNECTED=[connect, serial_number],
        ON=[start_acquisition, disconnect],
        MEASURING=[stop_acquisition],
    )
    # state_machine is a reserved class attribute
    # v1

    state_machine = StateMachine(
        states=states,
        initial_state=states.DISCONNECTED,
        push_state_change_event=True,
        DISCONNECTED=[connect, serial_number],
        ON=[start_acquisition, start_acquisition_single, disconnect,
            integration_time, trigger_mode, background_correction, nonlinearity_correction],
        MEASURING=[stop_acquisition],
        FAULT=[stop_acquisition, reset_fault]
    )
    # v2

  
