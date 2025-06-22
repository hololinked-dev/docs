# Event Descriptors

The main purpose of event descriptors is to return a pub-sub object that can be used to publish events. 
The pub-sub object must publish (emit) the event to all subscribers at the moment the `publish` (or equivalent) method is called, 
ensuring event delivery that is controlled by the server side. The event payload is defined by a schema, 
which can be either a JSON schema or a Pydantic model.



