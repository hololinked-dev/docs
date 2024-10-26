Using Finite State Machine
--------------------------

:doc:`API Reference <../../autodoc/server/thing/state_machine>`

Often, certain activties are not allowed during certain conditions, for example,
one cannot turn ON a motor higher than 10 times per hour, or one cannot change 
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

