

::: hololinked.server.Thing
    options:
        members:
            - __init__
            - run_with_http_server
            - run_with_zmq_server
            - exit
            - get_thing_description
            - get_thing_model
            - properties


## Attributes

### `id: str`
`instance-attribute`, `writable` <br />
Unique string identifier of the instance. This value is used for many operations,
for example - creating zmq socket address, tables in databases, and to identify the instance 
in the HTTP Server - (http(s)://{domain and sub domain}/{instance name}). 
If creating a big system, instance names are recommended to be unique.


{{ my_macro() }}