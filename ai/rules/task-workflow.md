# Task Workflow (SSOT)

The single source of truth for the workflow toolkit. The `/loom`, `/warp`, `/raid`, and
`/amaw` commands are invocation harnesses around **this** model — keep this loaded; the
commands point back here. Generalized from a mature repo; strip nothing project-specific
into the commands that isn't here first.

## Modes (the 2×2 toolkit)

```
                 Serial             Parallel fan-out
Human-gated      loom (+amaw)       warp
Autonomous       (amaw-auto, rare)  raid
```

- **`/loom`** — default, human-in-loop, serial. Used almost always.
- **`/warp`** — parallel: provably-disjoint slices, worktree sub-agents, human junction.
- **`/raid`** — autonomous coordinator for long multi-cycle runs.
- **`/amaw`** — opt-in deepening overlay (cold-start review roles); **human-initiated only**,
  never self-proposed.

## The 12 phases

```
CLARIFY → DESIGN → REVIEW → PLAN → BUILD → VERIFY → REVIEW → QC → POST-REVIEW → SESSION → COMMIT → RETRO
```

**Human checkpoints (STOP and WAIT):** end of **CLARIFY**, and at **POST-REVIEW**.

| Phase | Role lens (default) |
|---|---|
| 1. CLARIFY | Architect + Owner — scope + acceptance criteria |
| 2. DESIGN | Lead |
| 3. REVIEW (design) | Lead self-review *(amaw: Adversary cold-start)* |
| 4. PLAN | Lead + Developer |
| 5. BUILD | Developer (TDD) |
| 6. VERIFY | Developer — **evidence gate** |
| 7. REVIEW (code) | Lead self-review, 2-stage *(amaw: Adversary cold-start)* |
| 8. QC | QA / Owner *(amaw: Scope Guard)* |
| 9. POST-REVIEW | **Human checkpoint — present + WAIT** *(amaw: Scope Guard)* |
| 10. SESSION | Developer — update the handoff |
| 11. COMMIT | Developer — stage changed files only |
| 12. RETRO | All — record non-obvious lessons |

## Task size classification (MANDATORY, before work)

**Size by complexity + risk, not file count.**
- **Logic** = distinct semantic changes (new behaviors, contracts, branches) — **primary**.
- **Side effects** = API/DB/config/migration/auth — **risk**; sets a hard **floor**.
- **Files** = breadth only. A mechanical sweep does **not** escalate; breadth bumps one tier
  only when the change is genuinely deep across it (`logic ≳ files`).

| Size | Logic | Risk floor | Allowed skips |
|------|-------|-----------|---------------|
| **XS** | 0–1 | no side effects | CLARIFY + PLAN |
| **S** | 2–3 | ≥1 side effect ⇒ min S | PLAN only |
| **M** | 4–6 | ≥2 side effects ⇒ min M | None |
| **L** | 7–12 | yes | None — write a plan |
| **XL** | 13+ | yes | None — write spec + plan; sub-agents recommended |

Classify the **whole effort**, not each sub-task. Undersizing on breadth is allowed (gate
warns, you proceed); undersizing below the **risk floor** is blocked.

**Budget-driven checkpoints (large-context models):** let context budget, not file count,
drive when to stop. Ample budget (<~70%) → run continuously, checkpoint at genuine risk
boundaries (a new contract, a migration, a cross-module seam, a shippable milestone).
Filling (>~80%) → checkpoint + compact at the next risk boundary.

## Phase 6 VERIFY — evidence gate

Run command → read complete output → confirm match → **then** claim. No "should work", no
trusting prior/cached runs. When a change touches **≥2 independently deployed
modules/services**, a unit suite is insufficient — the VERIFY evidence needs a
**live cross-module smoke** token (or an explicit deferral / "infra unavailable" reason).
Mock-only coverage repeatedly hides cross-module contract bugs.

## Anti-skip rules

- The agent **never** self-authorizes a skip — STOP, announce the attempt, ask the human.
- If during BUILD the task turns out larger than classified — STOP, reclassify, announce.
- Phases may be skipped **only** per the size-table "allowed skips" column.

## Enforcement

A state machine (`.workflow-state.json`) + a pre-commit hook block phase jumps and commits
without VERIFY + POST-REVIEW + SESSION evidence. The gate contract (CLI + state model) is in
[`workflows/loom/gate/`](../../workflows/loom/gate/README.md). Run the gate from the **repo
root** only — a subdir invocation splits the state file.
