# Publish-Subscribe

::: hololinked.core.eventloop.pubsub.EventBus
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - __init__
            - register
            - unregister
            - subscribe
            - unsubscribe
            - publish
            - event_for
            - event_ids

::: hololinked.core.eventloop.pubsub.EventSubscription
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - __init__
            - event
            - bus
            - loop
            - queue
            - dropped
            - unique_identifier
            - receive
            - encode
            - event_callback_threadsafe
            - unsubscribe

::: hololinked.core.eventloop.pubsub.RegisteredEvent
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - descriptor
            - owner
            - unique_identifier
