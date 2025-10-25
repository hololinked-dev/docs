# Configuing Thing Class

### Logger

A default logger with IO stream handler is configured for each `Thing` instance. One can override the logger by passing a custom logger instance to the `Thing` constructor:

```py title="Custom Logger" linenums="1" hl_lines="12"
class WarningsToFileHandler(logging.FileHandler):
    """Custom handler that writes only WARNING+ logs to a separate file."""
    def emit(self, record):
        if record.levelno >= logging.WARNING:
            super().emit(record)

logger = logging.getLogger("custom_logger")
logger.setLevel(logging.DEBUG)
warn_file = WarningsToFileHandler("warnings.log")
warn_file.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

thing = Thing(id="test-thing", logger=logger)
thing.run_with_http_server(port=9000)
```

#### Remote Access to Logger

To be updated after integration with opentelemetry & EFK stack. See [issues](https://github.com/hololinked-dev/hololinked/issues?q=is%3Aissue%20state%3Aopen%20milestone%3A%22logging%2C%20metrics%20and%20traces%22).

<!--

To stream the logs remotely, specify `remote_access_handler=True` while instantiating the `Thing`.

```py title="Remote Logger" linenums="1"
thing = Thing(id="test-thing", remote_accessible_logger=True)
thing.run_with_http_server(port=9000)
```

or while defining the `Thing` class:

```py title="Remote Logger" linenums="1"
class MyThing(Thing):
    """Example Thing with remote accessible logger."""
    remote_accessible_logger = True
```

The logger will be accessible under:

Endpoint | Description
--- | ---
`http(s)://<host>:<port>/<thing_id>/logger/logs` | all logs
`http(s)://<host>:<port>/<thing_id>/logger/logs/debug` | debug logs and above -->

### Meta

To be updated with use cases of modifying Thing metaclass, in the meanwhile there is decent documentation in
the developer notes: [Thing MetaClass](../../../design/metaclasses.md#metaclasses).

### Post Init

To be updated, please refer to the developer notes in the meantime: [Thing Post Init](../../../design/metaclasses.md#__post_init__-method).

<!-- `Thing` classes define a `__post_init__` method which is invoked after loading properties from a database.
All initialization logic which depend on database loaded properties can placed in this method:

```py title="Post Init" linenums="1"

class MyThing(Thing):

    def __post_init__(self):
        super().__post_init__() # dont forget to call parent
        self.logger.info("Thing initialized with properties from DB")
```
-->

### Composition

To be updated.
