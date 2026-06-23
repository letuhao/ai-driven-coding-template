# Design decisions

Lightweight ADRs capturing *why* the collection is shaped this way, so the
rationale isn't lost. Each is a decision we can revisit, not dogma.

---

## ADR-001 — Four orthogonal catalogs + a recipe composer

**Decision.** Model the collection as four independent, flat catalogs
(`templates`, `architectures`, `workflows`, `ai`) plus a `recipes` layer that
references one piece from each.

**Why.** Nesting the dimensions (`python/microservices/tdd/...`) explodes
combinatorially and makes every catalog touch the others. Flat catalogs grow
independently; recipes provide combination without pre-building the cross-product.

---

## ADR-002 — Templates are verified by CI, not trusted

**Decision.** A scheduled CI job instantiates every template/recipe and runs
build + tests. Each entry records a "last verified" date.

**Why.** Template rot (stale deps, dead CI syntax, deprecated APIs) is the #1
long-term failure mode. A template that doesn't build is worse than none.

---

## ADR-003 — One placeholder convention, collection-wide

**Decision.** Pick a single substitution convention (e.g. `{{project_name}}`)
used by every catalog entry; the assembler is the only thing that expands it.

**Why.** Without a shared convention every recipe reinvents substitution. This is
painful to retrofit, so it is fixed up front. *(Concrete syntax: TODO — confirm.)*

---

## ADR-004 — Scope: one-shot scaffolder, not a live updater

**Decision.** The collection scaffolds at project `init` and then steps out of
the way. It does **not** (yet) support pulling later updates into existing projects.

**Why.** "Day 2" update-merge is an order of magnitude more complex. Stating the
scope prevents accidental drift toward it. Revisit only with explicit demand.

---

## ADR-005 — Tool-agnostic AI substance

**Decision.** AI substance (`ai/rules`, `ai/prompts`) is tool-agnostic; only
`ai/agents/<tool>` may assume a specific AI tool. Prefer generating per-tool
files from shared fragments.

**Why.** Avoids coupling the whole collection to one vendor, and keeps rule
snippets small for the per-turn AI context budget.

---

## ADR-006 — Safe-by-default and clear licensing

**Decision.** Every template ships secrets-aware `.gitignore`, `.env.example`
(never `.env`), pinned deps, no hardcoded creds. Document that **generated code
belongs to the user, unencumbered**, separate from the collection's own LICENSE.

**Why.** Copied templates become everyone's baseline — a bad default propagates.
Ambiguous licensing kills adoption of a scaffolder.
