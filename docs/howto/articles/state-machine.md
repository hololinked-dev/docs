Using Finite State Machine
--------------------------

:doc:`API Reference <../../autodoc/server/thing/state_machine>`

Often, certain operations are not allowed during certain conditions, for example, 
one can turn ON a switch twice in a row, or one does not wish to change the 
exposure of a camera during video capture (say).

To implement these contraints, a state machine may be used to prevent property writes or 
action executions in certain states (events are not supported). A ``StateMachine`` is a class-level 
attribute which accepts a finite list of states and the allowed properties and actions 
in these states.  

definition:

.. literalinclude:: code/fsm/def.py
    :language: python
    :linenos:
    :lines: 1, 12-15, 34-36, 40-41


Specify the machine conditions as keyword arguments to the ``state_machine`` with properties and actions 
in a list:

.. literalinclude:: code/fsm/def.py
    :language: python
    :linenos:
    :lines: 1-2, 12-41

As expected, one needs to set the ``StateMachine`` state to indicate state changes:

.. literalinclude:: code/fsm/def.py 
    :language: python 
    :linenos: 
    :lines: 

One can also sepcify the allowed state of a property or action directly
on the corresponding objects:

.. literalinclude:: code/fsm/def.py 
    :language: python 
    :linenos:
    :lines: 

State machines also push state change event when the state changes:

.. literalinclude:: code/fsm/client.py 
    :language: python 
    :linenos:
    :lines: 

One can suppress state change events by setting ``push_state_change_event=False``.

Lastly, one can also supply callbacks which are executed when entering and exiting certain states, 
irrespective of where or when the state change occured:

.. literalinclude:: code/fsm/client.py 
    :language: python 
    :linenos:
    :lines: 