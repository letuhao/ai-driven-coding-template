---
title: Paperwork Standard — document organization for stateful session continuity
status: experimental
maturity: experimental
audience: both
derived_from: Dead Light Framework Paperwork Standard (WIP, not yet adopted)
---

# Paperwork Standard

> **Maturity: `experimental`.** Harvested from the Dead Light Framework, which is
> work-in-progress and **not yet adopted** in a real project through a full lifecycle.
> It is the chosen spine for its *design* (conflict-free concurrent multi-agent work),
> not a track record. Adopt opt-in; it graduates to `stable` only after adoption
> evidence. See [ADR-008](../../docs/decisions.md). Neutralized terms: [[glossary]].

## Summary

An AI session starts from zero every time, and several agents may work many modules at
once. This standard makes documentation carry **session-to-session state** for readers
that start cold, and makes concurrent work **conflict-free by construction**:

- **State** documents are *derived* from append-only **Log** documents.
- Log entries are **self-sufficient durable bundles** — each readable in isolation.
- A **causal cursor** (a git commit SHA) makes "what's recent" unambiguous.
- The State is a **deterministic fold** of the Log — divergent regenerations converge
  (a CRDT), so two agents folding the same Log cannot disagree.
- Work is **partitioned by unit** with a federation model across repos.
- **Session re-priming** rebuilds full context from local copies — no coordination.

This is the **zero-infrastructure** tier, deliberately on the **eventually consistent**
side: a session never blocks on another, so under partition it converges later. That is
a declared property, not a defect — strong consistency under concurrent writers needs a
runtime tier outside this standard.

## 1. When it applies — Maturity Tier

The standard applies at **Tier 1 and above**; Tier 0 projects need only a `README.md`.
The tier gate (trigger-based 0→1, scale-based 1→2) is defined in
[ADR-007](../../docs/decisions.md) and tabulated in [choosing.md](../../docs/choosing.md).

- **Tier 0 — Prototype:** outside the standard. `README.md` suffices; no Log, no State.
- **Tier 1 — Continuity:** the core below — one State + one Log, single unit.
- **Tier 2 — Federation:** Tier 1 + partitioning + federation (§5–§6).

A unit adopts a higher tier, never lower. In a Tier-2 repo, even a small unit keeps a
minimal `HANDOFF`+`LOG` stub so it joins the ancestor chain.

## 2. State / Log split (the core)

Two documents per unit:

| Doc | Kind | Rule |
|---|---|---|
| `LOG.md` | **Log** — append-only history | **Append only. Never edit a past line** — a correction is a new line. This is the source of truth. |
| `HANDOFF.md` | **State** — current snapshot | **Rewrite freely.** It always describes "now". History does not live here. |

A fresh session reads `HANDOFF.md` first, then the `LOG.md` lines added in commits
**after** the State's `cursor:`, and is immediately current.

Templates: [[handoff-template]] (State), [[log-template]] (Log).

## 3. Log events — self-sufficient bundles

One line per event; each line readable without its neighbors:

```
<YYYY-MM-DD> · <session/agent-id> · <kind> · <one self-sufficient sentence> [ (reason: …) ] [<tags>]
```

**Six event kinds** (the practitioner subset):

| Kind | Meaning |
|---|---|
| `decision` | a choice was made — carries `(reason: …)`. The most important kind. |
| `created` | a new artifact / sub-area appeared. |
| `changed` | an existing artifact's state moved — same identity, new state. |
| `note` | FYI context — no choice, no state change. Use sparingly. |
| `superseded` | a different artifact replaces this one — identity changes. |
| `dispute` | an earlier entry was wrong when written (cite its SHA). |

**Four lifecycle tags** (describe state, ride alongside the kind):
`[candidate]` (agent-produced, unconfirmed) · `[sealed]` (settled — suspend-and-refer-back
before changing) · `[disputed]` (was wrong when written) · `[dormant]` (sealed but not yet
in effect; carries `activates_when: …`).

## 4. Causal cursor — the fold

The State's `cursor:` is the SHA of the last `LOG.md` commit folded into the snapshot.
Two sessions with the same cursor read the same Log delta — there is no drift on the word
"recent". Regenerating the State is a **deterministic fold** over Log lines: same Log →
same State, regardless of who folds or in what order (a CRDT). This is why concurrent
regenerations cannot disagree.

## 5. Crash recovery

Durable state lives entirely in `LOG.md` (+ the State snapshot + any in-progress markers).
An interrupted session is recovered by: read State → replay Log after `cursor:` → note the
abnormal end as a new Log line. No external coordination is required. (Single-session
Tier 1 treats multi-window lease machinery as a no-op.)

## 6. Partitioning & Federation *(Tier 2)*

When a repo holds **≥2 governance units**, each unit owns its own `HANDOFF`+`LOG`
(partitioning). A unit's State may carry **`ancestor_cursors:`** — one cursor per ancestor
tier it reads — so cross-unit and cross-repo work composes without a central lock. Each
unit re-primes from its **own local copies**; federation is read-only reference, never a
blocking dependency. This is the execution counterpart's twin: see `/warp` for the
conflict-free *execution* layer.

## 7. What this standard does NOT do

- Does **not** provide strong consistency under concurrent partitioned writers (that needs
  a runtime tier; its absence here is correct, not a gap).
- Does **not** replace your delivery process (Scrum/Kanban) — it is the state/authority
  layer above it.
- Does **not** require any infrastructure beyond git + markdown.

## Provenance

Neutralized and trimmed from the Dead Light Framework Paperwork Standard (a WIP
methodology). Themed vocabulary mapped via [[glossary]]. Shipped `experimental` per
[ADR-008](../../docs/decisions.md); graduates to `stable` after real adoption evidence.
