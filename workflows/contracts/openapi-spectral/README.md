# OpenAPI + Spectral — the REST contract preset

Contract-first for HTTP/REST services: an OpenAPI document is the source of truth; Spectral
lints it in CI; it is versioned and immutable once published.

## Layout & versioning convention

```
contracts/
  .spectral.yaml                      # the ruleset (copy from this preset)
  api/
    <service>/
      v1/
        openapi.yaml                  # the contract for v1
        README.md                     # human notes: consumers, change log
      v2/                             # a BREAKING change = a NEW version dir
        openapi.yaml
```

- **`v<N>` is immutable once a consumer depends on it.** Additive (non-breaking) changes may
  bump a minor `info.version` inside the same `v<N>`; a breaking change is a new `v<N+1>` dir.
- One `openapi.yaml` per service version. The service implements it; consumers code against it.
- Put the contract at the **nearest common ancestor** of its consumers (paperwork standard §R9),
  and list them in the version README so a change knows who to notify.

## Lint

```bash
# Node tool; run via npx (no install) or add @stoplight/spectral-cli as a dev dep.
npx @stoplight/spectral-cli lint "contracts/api/**/openapi.yaml" -r contracts/.spectral.yaml
```

Wire this into CI (a [workflow](../../README.md) ci-cd preset) so a malformed or undocumented
contract fails the build. Treat `error`-level findings as blocking; `warn` as advisory.

## With /warp

During parallel work, `/warp` freezes the contract by pinning its **git blob sha** in the slice
manifest (`frozen_interface`). Slices read it but may not write it; changing the contract means
returning to DESIGN, not patching a slice. See [`workflows/warp/`](../../warp/README.md).

See [`EXAMPLE-openapi.yaml`](EXAMPLE-openapi.yaml) for a minimal contract that passes the ruleset.
