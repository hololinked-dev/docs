

::: hololinked.core.zmq.rpc_server.RPCServer
    options:
        members:
            - __init__
            - run
            - stop
            - exit
            - get_thing_description
            - run_zmq_request_listener
            - recv_requests_and_dispatch_jobs
            - tunnel_message_to_things
            - run_things
            - run_thing_instance
            - execute_operation
         

## Attributes

### `id`
`str` <br/> 
`instance-attribute`, `writable` <br />
ID of the RPC server, used to direct requests from client. Must be unique. 
For IPC & INPROC sockets, ID is used to create the socket as well. For TCP, it is used for 
message routing. 

### `things` 
`List[Thing]` <br />
`instance-attribute`, `read-only` <br />
`Thing` objects that will be served by this RPC server.

### `logger` 
`logging.Logger` <br />
logger instance

### `req_rep_server`
`AsyncZMQServer` <br />
`instance-attribute`, `read-only` <br />
ZMQ server that handler request-reply pattern. Used for properties & actions. 

### `event_publisher`
`EventPublisher` <br /> 
`instance-attribute`, `read-only` <br />
ZMQ servers that publishes events to clients in publish-subscribe pattern. 

### `schedulers`
`tying.Dict[str, Scheduler]` <br />
`instance-attribute` <br />
A map of thing ID to a `Scheduler` object. For actions requiring special scheduling,
additional schdulers with ID "(thing ID).(action name).(opertaion)" is created. 

