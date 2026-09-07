

::: hololinked.core.eventloop.eventloop.EventLoop
    options:
        members:
            - __init__
            - things
            - per_job_scheduler_types
            - per_thing_schedulers
            - pending_operations
            - add_thing
            - add_things
            - is_running
            - submit
            - execute
            - execute_operation
            - run
            - run_things
            - run_thing_instance
            - tunnel_message_to_things
            - run_coro_threadsafe
            - add_stop_hook
            - stop

## Attributes

### `logger`
`structlog.stdlib.BoundLogger` <br />
`instance-attribute`, `read-only` <br />
logger instance, bound with `component="eventloop"` and the implementing class name.

### `event_bus`
`EventBus` <br />
`instance-attribute`, `read-only` <br />
publishes events of every served `Thing` to the subscribed protocol servers.
Replaces the ZMQ `EventPublisher` that the RPC server used to own.
