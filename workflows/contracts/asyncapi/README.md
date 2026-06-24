# AsyncAPI — the event/async contract preset (stub)

> **Stub.** Sibling of the REST preset for **event-driven / message-queue / streaming**
> interfaces (Kafka, NATS, AMQP, webhooks). Add the real ruleset when a project needs it.

For async APIs, an **AsyncAPI** document is the contract (the event-world analogue of OpenAPI):
it describes channels, messages, and payload schemas. Lint with the **AsyncAPI CLI** or the
`spectral-asyncapi` ruleset. Layout: `contracts/events/<domain>/v1/asyncapi.yaml`. Same
[convention](../README.md): versioned, immutable once published, lives at the nearest common
ancestor of producers + consumers, frozen by `/warp`.
