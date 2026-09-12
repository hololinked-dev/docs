# Request handlers

Every HTTP route is served by a Tornado `RequestHandler` subclass. 

- [BaseHandler](base.md) — authentication and CORS are decided
- [RPCHandler](rpc.md) — `PropertyHandler` / `ActionHandler` / `RWMultiplePropertiesHandler`
- [EventHandler](event.md) — streams events
- [Probes and control](probes.md) — `ThingDescriptionHandler`, `LivenessProbeHandler`, `ReadinessProbeHandler`, `StopHandler`