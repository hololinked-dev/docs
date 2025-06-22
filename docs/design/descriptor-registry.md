# Descriptor Registries for Interaction Affordances

Descriptor registries keep track of the available interaction affordances for a given class or instance, allowing for dynamic introspection with the `Thing` class's capabilities. 

API possibilities include:

- add and remove affordances in runtime
- find by name or check their existence
- iterate and introspect affordances
- implement group operations on affordances (`readMultipleProperties`, `writeMultipleProperties`, `readAllProperties`, `writeAllProperties`)

Current implementations are:

- `PropertyRegistry` for managing property descriptors
- `ActionRegistry` for managing action descriptors
- `EventRegistry` for managing event descriptors
