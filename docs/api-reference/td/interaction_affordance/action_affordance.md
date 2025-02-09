

::: hololinked.td.interaction_affordance.ActionAffordance

| field        | supported | meaning                       | default usage                  |
|--------------|-----------|-------------------------------|--------------------------------|
| input | ✔️ | schema of the input required to invoke action | `input_schema` value of `action` decorator |
| output | ✔️ | schema of the output returned by the action | `output_schema` value of `action` decorator |
| safe | ✔️ | `true` if the action is safe | `safe` value of `action` decorator |
| idempotent | ✔️ | `true` if the action is idempotent | `idempotent` value of `action` decorator |
| synchronous | ✔️ | `true` if the action is synchronous | `synchronous` value of `action` decorator, (`false` for `async` or threaded functions) |