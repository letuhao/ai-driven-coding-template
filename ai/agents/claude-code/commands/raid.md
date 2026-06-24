---
description: Enable RAID Coordinator mode — the main session dispatches each pending cycle as a cold-start sub-agent and runs the entire active task in one invocation until all cycles are DONE or an escalation halts. Task identity is read per-branch from .raid/active-task.yaml.
---

# /raid — autonomous Coordinator mode

By default a repo uses the `/loom` human-in-loop workflow. Invoke `/raid` to enter
**Coordinator mode** for whichever long-running task is declared in `.raid/active-task.yaml`:
the main session auto-dispatches each pending cycle as a cold-start sub-agent until all cycles
are DONE **or** an escalation halts the loop. SSOT for phases:
[`ai/rules/task-workflow.md`](../../../rules/task-workflow.md).

Per-branch portability: paths are not hardcoded — switch branch → a different
`.raid/active-task.yaml` → the Coordinator picks up the new task automatically.

## When to invoke

- A long, decomposed task with a cycle log of dependent cycles, on a RAID-eligible branch.
- After the bootstrap cycle is committed and any pre-flight checklist is signed off.
- When the cycle log has at least one PENDING cycle whose dependencies are all DONE.

## Coordinator loop

```
You (main session) are the RAID COORDINATOR.
LOOP until all cycles DONE or an escalation halts:
  1. Ask the cycle helper for the next ready cycle (deps satisfied) → {cycle, brief_path} or {idle}.
  2. idle → emit the final report → exit.
  3. Read the brief + the cycle-runner prompt template; interpolate {cycle, brief, locked decisions}.
  4. Check quota/budget for the cycle (PROCEED / warn-and-continue / pause-for-reset).
  5. Spawn a cold-start sub-agent (the cycle runner) with the interpolated prompt.
  6. Receive a small structured summary {result: DONE|ESCALATED|QUOTA_BLOCK, commit_sha, files, …}.
  7. Append an audit row + update the cycle-log row (status, sha, completed_at).
  8. ESCALATED → emit escalation summary; HALT; ask the human to investigate.
  9. QUOTA_BLOCK → pause; tell the human to re-invoke after the reset window; exit gracefully.
  10. else → continue the loop.
Keep Coordinator overhead lean (small per-cycle token budget); don't dump full sub-agent summaries.
```

## What the cycle runner (sub-agent) does

Cold-start: reads ONLY the files listed in its prompt (its cycle-log row, brief, relevant
locked decisions, parent plan). Executes the **12-phase workflow** per the SSOT via gate calls.
May spawn nested role sub-agents (Adversary / Scope Guard / Healer) one level deep. Writes an
in-progress state file at each phase transition. Commits atomically with the cycle-log update.
Returns a small (~≤1500-token) structured summary to the Coordinator.

## Resume semantics

All durable state lives in the cycle log + audit log + per-cycle in-progress state file.
Re-invoking `/raid` reads the cycle log and picks up the next PENDING cycle with satisfied
deps. A cycle interrupted mid-execution is resumed by its sub-agent (it validates the
in-progress state before continuing) per the [paperwork standard](../../../documents/standards/paperwork-standard.md)
crash-recovery model.

## What /raid does NOT do

- Does NOT execute the bootstrap cycle (that uses default `/loom`).
- Does NOT skip phases or bypass VERIFY gates (the sub-agent runs the gate).
- Does NOT push to origin during cycles (the human pushes between cycles if desired).
- Does NOT touch protected paths (charter/SSOT, prod env) — enforce via the cycle brief bounds.
