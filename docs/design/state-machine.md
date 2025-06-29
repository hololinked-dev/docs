# State Machine

A finite state machine is a simplistic and intuitive constraint on the execution of properties and actions. Usage of a state machine must be optional
depending on the complexity of the use case as it can lead to unintended side effects or dead locks if the device enters a wrong state. 

API possibilities include:

- specify the list of allowed states, initial state and the writable properties and invokable actions for each state
- read state as a property and push state change events
- introspection of actions or properties executable in a given state
- specify transition callbacks when the state changes

An example could be as follows:

```python
class Spectrometer(Thing):

    class States(StrEnum):
        DISCONNECTED = "DISCONNECTED"
        ON = "ON"
        FAULT = "FAULT"
        MEASURING = "MEASURING"
        ALARM = "ALARM"
        SIMULATION = "SIMULATION"

    state_machine = StateMachine(
        states=states,
        initial_state=states.DISCONNECTED,
        push_state_change_event=True,
        DISCONNECTED=[connect, serial_number, simulate],
        ON=[
            # actions
            start_acquisition, start_acquisition_single, disconnect, simulate,
            # properties (writeProperty)
            integration_time, trigger_mode, background_correction, nonlinearity_correction
        ],
        MEASURING=[stop_acquisition],
        FAULT=[stop_acquisition, reset_fault],
        SIMULATION=[stop_simulation]
    )

    def start_acquisition(self, max_count = None):
        # write acquisition start logic here
        self.state_machine.current_state = self.states.MEASURING

    def stop_acquisition(self):
        # write acquisition stop logic here
        self.state_machine.current_state = self.states.ON
```