::: hololinked.server.zmq.brokers.BaseEventConsumer
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - __init__
            - subscribe
            - stop_polling
            - interrupt_message

::: hololinked.server.zmq.brokers.EventConsumer
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - receive
            - interrupt

::: hololinked.server.zmq.brokers.AsyncEventConsumer
    options:
        show_root_heading: true
        heading_level: 2
        members:
            - receive
            - interrupt