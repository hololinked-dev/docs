# Serialization

Serialization customization is available on a per-interaction-affordance basis. The purpose is to offer an easy to use API:

- without having to write serialization handlers in protocol request handler logic
- to stick to JSON serialization by default
- to allow non-JSON serialization only for the specific interaction affordances that require it
- register and use arbitrary serialization protocols

Every serializer must define a

- `dumps`
- `loads`
- `content_type` property

The `content_type` is set as the `contentType` field in the Thing Description.
