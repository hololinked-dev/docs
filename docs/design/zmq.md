# ZMQ RPC layer

The main purpose of the RPC layer is for adding scheduling control for the interaction affordances. Three types of scheduling are supported:

- synchronous - the default, blocking until the interaction affordance is completed
- async - non-blocking and can be scheduled on the current async loop  
- threaded - non-blocking and can be scheduled on a separate thread

All protocols retrieve information from the request which can be used to create a scheduling message. The message is then sent to the ZMQ server, which will handle the scheduling and execution of the interaction affordance. The ZMQ server will then send the response back to protocol handler which returns the response the client.

In a certain way, this is a protocol-to-protocol transfer of request and response, with a minor difference that ZMQ handles this over its `INPROC` transport over threads, which is more efficient than TCP-to-TCP communication. Essentially, it behaves like a queue when the request is sent, scheduled and the response is received.