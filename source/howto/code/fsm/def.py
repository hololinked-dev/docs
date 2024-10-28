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
    def connect(self):
        ...

    @action()
    def disconnect(self):
        ...

    @action()
    def start_acquisition(self):
        ... 

    @action()
    def stop_acquisition(self):
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
        ON=[start_acquisition, disconnect],
        MEASURING=[stop_acquisition]
    )
    # v2

    def connect(self):
        # add connect logic here
        self.state_machine.set_state('ON')

    def disconnect(self):
        # add disconnect logic here
        self.state_machine.current_state = 'DISCONNECTED'
        # same as self.state_machine.set_state('DISCONNECTED', push_event=True, skip_callbacks=False)

    @action(state=[states.ON])
    def start_acquisition(self):
        # add start measurement logic
        self.state_machine.set_state(states.MEASURING)

    @action(state=[states.MEASURING, states.FAULT, states.ALARM])
    def stop_acquisition(self):
        # add stop measurement logic
        if self.state_machine.state == states.MEASURING:
            self.state_machine.set_state(states.ON)
        # else allow FAULT or ALARM state to persist 