[API Reference](../../api-reference/state-machine/state-machine.md)

The world of physical things is often constrained by certain physical conditions. One may need to constrain operations that are allowed when a `Thing` is said to be in a certain state. For example, a measurement device cannot modify a specific setting if a measurement is ongoing, as this could ruin the measurement. This could be considered as the device being in `MEASURING` state. Similarly, a device recovering from a fault condition (or `FAULT` state) requires a specific set of operations. To implement these contraints, a finite state machine may be used to prevent property writes or actions. Events are not supported. 

## Definition

A `StateMachine` is a class-level attribute which accepts a list of states and the allowed properties and actions in these states. One can custom define the set of state names:

```py title="Definition" linenums="1" 
--8<-- "docs/beginners-guide/code/fsm/def.py:1:1"
--8<-- "docs/beginners-guide/code/fsm/def.py:13:15"
--8<-- "docs/beginners-guide/code/fsm/def.py:30:33"
--8<-- "docs/beginners-guide/code/fsm/def.py:37:38"
```

Specify the machine conditions as keyword arguments to the `state_machine` with properties and actions in a list:

```py title="Specify Properties and Actions" linenums="1" hl_lines="23-27"
--8<-- "docs/beginners-guide/code/fsm/def.py:1:2"
--8<-- "docs/beginners-guide/code/fsm/def.py:12:38"
```

Set the `StateMachine` state in properties or actions to indicate state changes using the `set_state()` method or the assignment operator on `state_machine.current_state`. Actions or python methods are the most common place to set the state:

```py title="set_state()" linenums="1" hl_lines="6 12"
--8<-- "docs/beginners-guide/code/fsm/def.py:13:15"
--8<-- "docs/beginners-guide/code/fsm/def.py:54:63"
```

One can also specify the allowed state of a property or action directly on the corresponding objects:

```py title="Specify State Directly on Object" linenums="1" hl_lines="4 12"
--8<-- "docs/beginners-guide/code/fsm/def.py:13:15"
--8<-- "docs/beginners-guide/code/fsm/def.py:64:74"
```

## State Change Events

State machines also push state change event when the state changes. The `state` is also an observable property per definition in the base `Thing` class:

```py title="Definition" linenums="1" hl_lines="7"
--8<-- "docs/beginners-guide/code/fsm/def.py:13:16"
--8<-- "docs/beginners-guide/code/fsm/def.py:41:48"
```

One can suppress state change events by passing `push_event=False` when setting the state using the `set_state()` method:

```python title="suppress state change event"
self.state_machine.set_state('STATE', push_event=False)
```

Clients can subscribe to these state change events like any other observable property:

```python title="subscription" linenums="1"
def state_change_cb(event):
    print(f"State changed to {event.data}")

client.observe_property(name="state", callbacks=state_change_cb)
```

## State Change Callbacks

One can also supply callbacks which are executed when entering and exiting certain states, irrespective of where or 
when the state change occured. The state name and the list of callbacks are supplied as a dictionary to the `on_enter` 
and `on_exit` arguments. These callbacks are executed after the state change is effected, and are mostly useful when 
there are state changes at multiple places which need to trigger the same side-effects.

```py title="enter and exit callbacks" linenums="1" hl_lines="21"
--8<-- "docs/beginners-guide/code/fsm/def.py:13:15"
--8<-- "docs/beginners-guide/code/fsm/def.py:75:"
```

