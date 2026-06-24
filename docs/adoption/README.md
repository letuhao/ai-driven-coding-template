# Adoption guides

How to adopt this collection, by role. Start here, then read the guide for your role.

## The contract

You **scaffold** a project from a recipe and then **own** the result. This is a one-shot
scaffolder ([ADR-004](../decisions.md)): the collection does not track, audit, or update your
project afterwards — standard fork-and-modify (like cookiecutter). Generated code is yours,
unencumbered ([ADR-006](../decisions.md)).

## Quickstart (clone → first project)

```bash
python scripts/new-project.py --list
python scripts/new-project.py --recipe go-minimal --name myapp \
  --var go_module=example.com/myapp --out ../myapp
```

Then, by **Maturity Tier** ([choosing.md](../choosing.md)):

- **Tier 0 (prototype):** you're done — a README suffices.
- **Tier 1+:** add the paperwork core (Sealed Charter + one HANDOFF + one LOG) and adopt the
  workflow toolkit (`/loom`). Use a multi-piece recipe (e.g. `python-microservice-tdd`) or add
  the pieces yourself.

## Role guides

- [for-owners.md](for-owners.md) — project owner / PM: seal the charter, pick the tier, set the gates.
- [for-developers.md](for-developers.md) — engineers: the day-to-day workflow toolkit.
- [for-ai-agents.md](for-ai-agents.md) — AI agents: how to re-prime and operate in a repo built this way.

Terminology is neutralized — see [documents/glossary.md](../../documents/glossary.md).
