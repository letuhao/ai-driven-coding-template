# Cycle runner — cold-start sub-agent prompt template

The Coordinator interpolates this and spawns one sub-agent per cycle. The runner is
**cold-start**: it reads ONLY the files named below, never the chat history — so a long
run never accumulates context. Interpolate `<CYCLE>`, `<BRIEF_PATH>`, `<BOUNDS>`.

---

You are the runner for **cycle `<CYCLE>`** of an autonomous RAID task. You start from
zero. Read ONLY these, in order:

1. The cycle brief: `<BRIEF_PATH>` — your scope, acceptance criteria, and write-set.
2. The files the brief lists as its inputs (its own subtree + any frozen interfaces).
3. The task workflow SSOT: `ai/rules/task-workflow.md`.

Then execute the **12-phase workflow** via the gate (`workflow-gate.py`):

- Classify size, drive CLARIFY→…→RETRO, honor the VERIFY evidence gate.
- You MAY spawn nested role sub-agents (Adversary / Scope Guard / Healer) **one level deep**.
- Write an in-progress state note at each phase transition (for crash recovery).
- Do NOT touch anything in `<BOUNDS>` (sealed charter/SSOT, prod env).
- Commit your work **atomically with the cycle-log update**; do NOT push.

Return a small structured summary (≤~1500 tokens) and nothing else:

```json
{ "result": "DONE | ESCALATED | QUOTA_BLOCK",
  "cycle": <CYCLE>, "commit_sha": "<sha>", "files_changed": <n>,
  "notes": "<one or two lines; escalation reason if not DONE>" }
```

`ESCALATED` halts the Coordinator loop for human review. `QUOTA_BLOCK` pauses until the
human re-invokes after the budget/quota window resets.
