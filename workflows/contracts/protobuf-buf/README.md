# Protobuf + buf — the gRPC contract preset (stub)

> **Stub.** Sibling of the REST preset for **gRPC / Protobuf** interfaces. Add the real ruleset
> when a project needs it. The [contract-first convention](../README.md) is identical; only the
> wire format and linter differ.

For gRPC, the `.proto` files are the contract. Use:

- **`buf lint`** — style + correctness rules (replaces Spectral).
- **`buf breaking`** — detects breaking changes against a baseline (the immutability guard the
  REST preset gets from versioned `v<N>` dirs).
- Layout: `contracts/proto/<service>/v1/*.proto` + a `buf.yaml` ruleset + `buf.gen.yaml` for codegen.

Frozen by `/warp` the same way (pin the `.proto` blob sha). Lives at the nearest common ancestor
of its consumers.
