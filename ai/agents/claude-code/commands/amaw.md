---
description: Enable AMAW (deepening review roles) for the current task only. Spawns cold-start sub-agents at the REVIEW + POST-REVIEW phases instead of main-session self-review. HUMAN-INITIATED ONLY — never self-proposed.
---

# /amaw — deepening review roles for this task

By default a repo uses the `/loom` human-in-loop workflow. Invoke `/amaw` to enable the
deepening overlay for the **current task only**: cold-start sub-agent reviews replace
main-session self-review at the review phases. SSOT: [`ai/rules/task-workflow.md`](../../../rules/task-workflow.md).
Role prompts: [`ai/prompts/roles/`](../../../prompts/roles/).

> **HUMAN-INITIATED ONLY.** The agent never proposes, announces, or invokes `/amaw` on its
> own — not at CLARIFY, not before BUILD, not even for L+/load-bearing work. If the human
> wants the cold-start reviews they turn it on. (The token cost is the human's call.)

## When it pays off

| Use case | Why |
|---|---|
| Data migration (schema/dim change) | cache coherence, side effects easy to miss |
| New module boundary / multi-system contract | edge cases compound across components |
| Security-critical path (auth, tenant isolation, destructive ops) | author blindness is real |
| Bulk op affecting >1 module | cross-module side effects hard to enumerate |

Not for: single-file bugs, doc updates, small refactors.

## What changes when active

1. **REVIEW (design) + REVIEW (code):** spawn the **[Adversary](../../../prompts/roles/adversary.md)**
   cold-start sub-agent instead of self-review; re-spawn fresh per round until APPROVED.
2. **QC + POST-REVIEW:** spawn the **[Scope Guard](../../../prompts/roles/scope-guard.md)** for a
   conservative final gate.
3. **RECONCILE / regression chases** (when combined with `/warp` or `/raid`): the
   **[Healer](../../../prompts/roles/healer.md)** fixes root cause in product code, never weakens tests.
4. An append-only **audit log** is the source of truth for phase transitions + verdicts.

All other phases (CLARIFY, PLAN, BUILD, VERIFY, SESSION, COMMIT, RETRO) still run unchanged.

## Calibration (don't run at max intensity blindly)

| Size | Rounds |
|---|---|
| **S** | 1 Adversary code review only (skip design review). |
| **M** | 1 design + 1 code review + Scope Guard. Stop at first APPROVED_WITH_WARNINGS. |
| **L** | Up to 3 design + 2 code review rounds + Scope Guard. |
| **XL** | Full overlay + sub-agent dispatch for parallel sub-tasks. |

Run a static check (type-checker/linter) before each Adversary code-review round — it catches
typo-level blocks for free. **Stop condition:** APPROVED_WITH_WARNINGS after round 2 is
acceptable; document the pragmatic stop + residual risk. Don't chase APPROVED endlessly.

## What this command does NOT do

- Does NOT change the default workflow for future tasks (per-task only; re-invoke if needed).
- Does NOT modify the SSOT or charter.
- Does NOT skip any phases.
