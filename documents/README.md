# documents/ — paperwork standards

Templates and standards for the project artifacts humans and AI agents read and write.
This is **Dimension 5**.

In AI-driven development the paperwork is the **interface** between human intent and agent
execution: a good spec lets an agent implement in one pass, a sealed Charter and decision
records stop it re-litigating settled choices, and a Log→State model lets a fresh session —
or several concurrent agents — stay current without conflict.

```
glossary.md            neutralized term map (authoritative — use these terms)
standards/
  paperwork-standard.md   the spine: Log→State, cursor, re-priming, tiers (experimental)
taxonomy/
  README.md            numbered docs/ layout + the anti-drift numbering rule
charter/TEMPLATE.md    Sealed Charter — frozen project authority (purpose/laws/principles)
handoff/TEMPLATE.md    State snapshot (HANDOFF.md) — derived, rewritten freely
log/TEMPLATE.md        append-only history (LOG.md) — source of truth
spec/TEMPLATE.md       feature spec / PRD — the agent's primary build input
adr/TEMPLATE.md        decision record (+ optional decision-debate variant)
github/                PR + issue templates
```

## How it fits together

- The **[[paperwork-standard]]** governs the concurrency/continuity model (Log→State,
  causal cursor, re-priming). It is the spine; everything else is subordinate to it.
- The **[[glossary]]** is authoritative for vocabulary — the standard is harvested from a
  themed framework and fully neutralized here.
- The **taxonomy** organizes document *categories*; the Paperwork Standard organizes *state*.
- A [recipe](../recipes/) lists which of these to drop into a new project, gated by
  **Maturity Tier** (see [choosing.md](../docs/choosing.md)): Tier 0 needs only a README;
  Tier 1+ adopts the Charter + Handoff + Log core.

## Placeholders

Per [ADR-003](../docs/decisions.md): `{{ project_name }}` is filled by the scaffolder at
init; `<descriptive blank>` is left for a human/agent to fill when authoring an instance.

## Maturity

The Paperwork Standard ships **`experimental`** ([ADR-008](../docs/decisions.md)) — the
source framework is WIP and not yet adopted through a full lifecycle. Adopt opt-in.
