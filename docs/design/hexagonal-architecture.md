# Hexagonal Architecture

At some point, it is intended to implement the hexagonal architecture (also known as ports and adapters architecture) 
to achieve better separation of concerns and allow the codebase to adapt to technological changes. 
The folder structure, base classes and consumption of interfaces is largely set up to reflect this architecture, 
although not in the import statements. A diagram illustrating this is shown below:

<img src="../../assets/hexagonal-architecture.drawio.svg" alt="Hexagonal architecture diagram" style="width: 100%; height: auto;" />

The namespaces may be explained as follows:

- The core namespace implements the domain logic, like the definition of `Thing` class, the RPC server, the 
operations possible on `Thing`s (like read property, invoke action, subscribe to events), 
and the event loop to execute these operations. Other items like descriptors, loggers and state machines are also defined. 
- Each of the driven dependencies (like serializers, thing description generator etc.), has their own namespace, 
and they are used by the core logic. 
- The driving dependencies currently constitute only the protocols.

The supported protocols themselves are only a thin layer which just extract the relevant information from the protocol 
and forward them to the core logic. This way, protocols can be added or removed without affecting the core domain logic, 
or the user could possibly choose which protocol runtimes need to be installed in their deployment.

The intention to implement this setup would be to:

- allow easier addition of new protocols, without needing to reimplement entire event loops for each protocol
to execute operations on `Thing`s 
- mix & match, protocols, content types and allow protocols to use as many content types as possible, and
allow `Thing`s to run on many protocols simultaneously without duplicating logic
- allow easier testing component-wise
- adapt to future changes in technology for any of the supported features
- add new features in their respective components without affecting other parts of the system

