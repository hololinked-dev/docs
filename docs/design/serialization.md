# Serialization

Serialization customization is available on a per-interaction-affordance basis. The purpose is to offer an easy to use API:

- without having to write serialization handlers in protocol request handler logic
- to stick to JSON serialization by default
- to allow non-JSON serialization when needed
- register and use arbitrary serialization protocols

Every serializer must define a 

- `dumps`
- `loads`
- `content_type` property







