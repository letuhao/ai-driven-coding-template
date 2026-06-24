---
description: Run a task through the 12-phase human-in-loop workflow — classify size, then drive CLARIFY→…→RETRO with human checkpoints and the workflow-gate. General-purpose, any module/track.
---

# /loom — run the human-in-loop 12-phase workflow

`/loom` weaves a task through the **12-phase workflow**. The phases, roles, size table, and
anti-skip rules are the SSOT in [`ai/rules/task-workflow.md`](../../../rules/task-workflow.md);
this command is just the invocation harness. `/loom` is **general-purpose** — not tied to any
one feature, module, or track.

**Argument** (optional): a free-text task, a ticket/milestone id, or `continue`.
- A task/id → scope the workflow to it.
- `continue` or empty → read the relevant **Start here next** block of the handoff and resume.

## Process

1. **Scope** the task (or the handoff's next block on `continue`). State task + goal in one line.
2. **Classify size** from the **repo root**: `gate size <XS|S|M|L|XL> <files> <logic> <side_effects> [context_pct]`.
3. **Enter CLARIFY** (`gate phase clarify`); recover acceptance criteria. **STOP at CLARIFY end**
   for the human checkpoint (skip the stop only when resuming a phase already past it).
4. Drive phases with the gate (`phase <name>` / `complete <name> "<evidence>"`). **VERIFY is an
   evidence gate** — run the command, read full output, *then* claim. ≥2 independently deployed
   modules ⇒ the VERIFY evidence needs a live cross-module smoke token (or explicit deferral).
5. **REVIEW (code)** is 2-stage (spec compliance + code quality). **At POST-REVIEW:** present a
   concise summary (files, decisions, verify evidence) and **STOP and WAIT**. Suggest
   `/review-impl` for load-bearing code (auth, tenant isolation, destructive ops, injection
   defenses, new module boundaries, concurrency, migrations).
6. **SESSION:** update the **Start here next** block of the handoff (date/HEAD, next items,
   deferred). Land it in the **same commit** as the code.
7. **COMMIT:** stage only changed files (no `git add -A`); message names phase/milestone + review
   fixes + test count. **Push only with explicit human approval.**
8. **RETRO:** record non-obvious decisions/workarounds (lessons store if configured, else a note
   in the handoff). Skip if nothing notable.

## Escalating from /loom

- Parallelizable M/L/XL across independent boundaries → consider **`/warp`**.
- Long autonomous multi-cycle run → **`/raid`**.
- L+ load-bearing and the human wants cold-start review depth → the human invokes **`/amaw`**
  (never self-propose it).

## What /loom does NOT do

- Does NOT skip phases or the human checkpoints.
- Does NOT self-authorize a size/skip change — if the task is bigger than classified, STOP,
  reclassify, announce.
- Is NOT tied to any single track/module/feature — scope comes from the argument or the handoff.
