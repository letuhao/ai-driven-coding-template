# GraphQL SDL — the GraphQL contract preset (stub)

> **Stub.** Sibling of the REST preset for **GraphQL** APIs. Add the real ruleset when a project
> needs it.

For GraphQL, the **SDL schema** (`schema.graphql`) is the contract. Lint + guard with a schema
linter (e.g. `graphql-schema-linter`) and a **breaking-change check** against the published
schema (the immutability guard). Layout: `contracts/graphql/<service>/schema.graphql`. Same
[convention](../README.md): the schema is the source of truth, checked in CI, frozen by `/warp`,
and lives at the nearest common ancestor of its consumers.

Note: GraphQL evolves a single schema additively rather than via `v<N>` dirs — deprecate fields
with `@deprecated` instead of forking a version, and rely on the breaking-change check.
