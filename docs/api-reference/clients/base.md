


::: hololinked.client.abstractions.ConsumedThingAction
    options:
        members:
        - __init__
        - __call__
        - async_call
        - oneway
        - noblock
        - last_return_value
        - get_last_return_value

::: hololinked.client.abstractions.ConsumedThingProperty
    options:
        members:
        - __init__
        - set
        - get
        - async_get
        - async_set
        - noblock_set
        - noblock_get
        - oneway_set
  
::: hololinked.client.abstractions.ConsumedThingEvent
    options:
        members:
        - __init__
        - subscribe
        - unsubscribe
        - listen
        - add_callbacks