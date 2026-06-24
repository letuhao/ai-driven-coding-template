# workflows/contracts — contract-first interfaces (opt-in, multi-preset)

A **contract** is a versioned interface schema that is the single source of truth between a
producer and its consumers, **frozen before code**. This dimension is **opt-in** ([ADR-010](../../docs/decisions.md)):
include a preset only when the project actually exposes a cross-boundary API, and it earns its
keep most at **Tier 2** (≥2 governance units with negotiated contracts — see
[choosing.md](../../docs/choosing.md)). A CLI, library, frontend-only, or single-unit project
omits it.

> The principle is the same surface as `/warp`'s **frozen interface** and the paperwork
> standard's **shared artifact in the nearest common ancestor** — the cross-boundary agreement
> that makes concurrent multi-module work safe. The tool just depends on the wire format.

## Pick the preset by interface type

| Interface | Preset | Status |
|---|---|---|
| **REST / HTTP** | [`openapi-spectral/`](openapi-spectral/) — OpenAPI + Spectral lint | **shipped, runnable** |
| **gRPC** | [`protobuf-buf/`](protobuf-buf/) — Protobuf + `buf lint`/`buf breaking` | stub |
| **Events / async / queues** | [`asyncapi/`](asyncapi/) — AsyncAPI + spectral-asyncapi | stub |
| **GraphQL** | [`graphql/`](graphql/) — SDL schema + a schema linter | stub |
| **Data (batch/pipeline)** | JSON Schema / Avro + a validator | not yet |
| CLI / library / frontend-only | — none (no network contract) | — |

## What every preset shares (the convention)

- **Versioned, immutable once published:** `…/<name>/v<N>/<schema>` — a breaking change is a new
  `v<N+1>`, never an edit to a shipped version.
- **Lint in CI:** the schema is checked on every change (the preset ships the ruleset).
- **Lives at the nearest common ancestor** of its consumers (paperwork standard §R9), with a
  `consumers:` note so a change knows who to notify.
- **Frozen before implementation:** producers and consumers agree the schema first; `/warp`
  pins it by git blob sha during parallel work.
