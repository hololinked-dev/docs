# Scanning

## Bandit

You can always access the latest security scan results from the Bandit SAST tool in the CI pipeline job of the [main branch](https://github.com/hololinked-dev/hololinked/actions/workflows/ci-pipeline.yml?query=branch%3Amain).

The following are the currently reported issues and the justifications of ignoring them:

| Issue ID                                                                                                                                                                                                     | Severity | Title                  | Justification                                                                                                                                |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `hololinked.core.thing.Thing.run_with_http_server.address`                                                                                                                                                   | MEDIUM   | Bind to all interfaces | It is intended to bind to all interfaces                                                                                                     |
| <ul><li>`hololinked.core.zmq.rpc_server.RPCServer.get_thing_description.req_rep_socket_address`</li><li>`hololinked.core.zmq.rpc_server.RPCServer.pub_sub_socket_address`</li></ul>                          | MEDIUM   | Bind to all interfaces | Here only the address is swapped with the machine hostname, and not bound to all interfaces                                                  |
| <ul><li>`hololinked.serializers.serializers.pickle_import`</li><li>`hololinked.serializers.serializers.PickleSerializer.dumps`</li><li>`hololinked.serializers.serializers.PickleSerializer.loads`</li></ul> | MEDIUM   | Pickle usage           | pickle is disabled by default with `global_config.ALLOW_PICKLE` set to `False`. Set to it `True` at your own risk if you wish to use pickle. |
| <ul><li>`hololinked.server.http.HTTPServer.address`</li><li>`hololinked.server.http.HTTPServer.__init__.address`</li></ul>                                                                                   | MEDIUM   | Bind to all interfaces | It is intended to bind to all interfaces                                                                                                     |
| `hololinked.server.http.ApplicationRouter.get_basepath`                                                                                                                                                      | MEDIUM   | Bind to all interfaces | Here only the address is swapped with the machine hostname, and not bound to all interfaces                                                  |

## gitleaks

A gitleaks scan is also performed, found in the same CI pipeline job of the [main branch](https://github.com/hololinked-dev/hololinked/actions/workflows/ci-pipeline.yml?query=branch%3Amain).
This scan must pass before any code is merged into the main branch.
