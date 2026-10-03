::: hololinked.server.zmq.ZMQServer
    options:
        inherited_members: true
        members:
            - __init__
            - from_params
            - id
            - config
            - context
            - logger
            - things
            - add_thing
            - add_things
            - add_property
            - add_action
            - add_event
            - inproc_server
            - ipc_server
            - tcp_server
            - transport_servers
            - inproc_event_publisher
            - ipc_event_publisher
            - tcp_event_publisher
            - event_publishers
            - setup
            - start
            - run
            - polling
            - recv_requests
            - process_request
            - stop_polling
            - get_thing_description
            - stop
            - exit
            - welcome_lines

Requires the `zmq` extra. Note the pin: `pyzmq<26.2`, which is what keeps IPC working on Windows.