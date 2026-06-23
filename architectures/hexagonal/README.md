# Hexagonal (Ports & Adapters)

> Example doc-first architecture entry. Use this as the template for new ones.

## What it is

Business logic (the "domain") sits in the center and knows nothing about the
outside world. It exposes **ports** (interfaces); **adapters** implement those
ports for specific technologies (HTTP, DB, queues). Dependencies point inward.

## When to use it

- Logic outlives its delivery mechanism (multiple UIs, swappable DB/providers).
- You want fast unit tests against the domain without spinning up infrastructure.

## When not to

- Small CRUD apps or short-lived prototypes — the indirection is overhead.
- A team unfamiliar with the pattern under deadline pressure.

## Folder skeleton (language-agnostic)

```
src/
  domain/          entities, value objects, domain services — zero I/O imports
  application/     use cases; depends only on ports
  ports/           interfaces the application needs (driven + driving)
  adapters/
    inbound/       http, cli, events -> call application
    outbound/      db, http-clients, queues -> implement ports
  config/          composition root: wire adapters to ports
tests/
  domain/          pure, fast
  integration/     adapters against real/contained infra
```

## Composition notes

Overlays onto any `templates/languages/*` start. The composition root in
`config/` is the only place allowed to import concrete adapters.

<!-- last verified: TODO -->
