---
description: Run a task in /warp parallel mode — decompose into provably-disjoint slices, fan them out as worktree sub-agents, reconcile at a human junction. For decomposable M/L/XL tasks where wall-clock matters. Falls back to serial /loom when the work can't be sliced.
---

# /warp — parallel-execution mode

`/warp` runs a task as **parallel threads** on the loom: it decomposes the work into
**provably-disjoint slices**, fans them out as isolated worktree sub-agents running
concurrently, then **reconciles at a defined junction the human controls**. It is loom's
12-phase spine with 3 phases adjusted + 2 nodes inserted — **not** a new workflow and **not**
raid (no locked mega-plan, no quota; fully human-gated). SSOT: [`ai/rules/task-workflow.md`](../../../rules/task-workflow.md).

## When to use — and when NOT

**Use it** when the work is **additive across ≥2 independent boundaries** (separate
modules/services, or many independent mechanical sites) AND the inter-slice contract can be
**fully frozen up front**.

**Do NOT** (use `/loom`): XS/S tasks (orchestration overhead dwarfs the win); refactors of a
**shared type/API** (slices aren't independent); anything touching a **shared-write magnet**
that can't be confined to one slice (migration sequence numbers, DI/route registration, i18n
bundles, generated barrels/clients, an API index). **Bias to serial:** a missed
parallelization costs some wall-clock; a wrong one costs merge hell. When in doubt → `/loom`.

## Phase flow (the ‡/＋ steps differ from loom)

```
0.  TRIAGE-pre  ＋ Score the parallel-fit rubric. <enough independent signals, or interface
                   won't freeze → STOP, run /loom instead.
1.  CLARIFY        loom — scope + acceptance. Human checkpoint at end.
2.  DESIGN     ‡ BOUNDARY-FINDING: (a) the frozen interface (pin each shared file by git blob
                   sha); (b) a slice manifest (disjoint write-sets); (c) a merge plan
                   (integrate order + on_contract_violation: HALT_REDESIGN).
3.  REVIEW(des)‡ Two gates: validate disjoint write-sets + frozen files unchanged vs pinned sha
                   (BLOCK → fix or /loom); + an Adversary on the SLICING (hidden coupling? magnet?).
                   NO-GO → fall back to serial /loom BUILD in THIS session.
4.  PLAN       ‡ One hermetic slice brief per slice — references ONLY the frozen interface +
                   its own write-set. Zero cross-slice references.
5.  BUILD      ‡ FAN-OUT: N slice sub-agents, worktree-isolated, run in background.
5.5 RECONCILE  ＋ Merge slice branches in integrate order. By disjointness, expect ZERO
                   write-set conflicts. A real conflict ⇒ the manifest was wrong ⇒ HALT_REDESIGN.
6.  VERIFY        loom evidence gate — the cross-module live smoke IS the reconcile proof.
7.  REVIEW(code)  2-stage; may fan-out by dimension (security/perf/contract).
8.  QC            diff vs spec.
9.  POST-REVIEW   HUMAN STOP + WAIT — the junction you control. Suggest /review-impl if load-bearing.
10. SESSION       update the handoff's Start-here-next; same commit.
11. COMMIT        stage changed files only; message names slices + reconcile. Push on approval only.
12. RETRO         record lessons if notable.
```

## The disjointness dividend

Reconcile is near-trivial **by construction**: the gate already proved every slice's write-set
is path-prefix-disjoint, and slices may not write the frozen interface — so integrating N
branches touches N non-overlapping file sets and cannot conflict. If it *does*, that is proof
the manifest was wrong → **HALT_REDESIGN**, not a patch.

**Caveat:** disjoint write-sets guarantee no *file* collision, NOT semantic independence — a
slice that under-declares a `reads` dependency can compile-then-break at merge with zero file
conflict. Catching that is the phase-3 Adversary's job.

## Coordinator notes (BUILD + RECONCILE)

- **Commit the DESIGN artifacts first** (frozen interface + manifest + briefs), then capture a
  **BASE_SHA** and **pin every slice to it** — worktree isolation does not reliably base a
  slice on HEAD; pin it yourself, and each slice self-heals onto BASE_SHA in its first step.
- After each slice returns DONE, **verify its branch descends from BASE_SHA** before
  reconciling. A slice that didn't pin (or whose worktree wasn't created) is re-spawned or, if
  it persists, built serially in `/loom`.
- A slice that hits `needs_out_of_scope_write` / `frozen_interface_insufficient` is a DESIGN
  signal — STOP, return to DESIGN (re-slice / re-freeze). Do NOT patch around it.

## What /warp does NOT do

- Does NOT slice a task that can't be made independent — it **falls back to `/loom`** (same session).
- Does NOT skip phases or the human checkpoints; does NOT auto-gate POST-REVIEW (that's raid).
- Does NOT let a slice edit outside its write-set, the frozen interface, or a shared-write magnet.
- Does NOT push without explicit approval.
