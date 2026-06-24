# workflows/raid — autonomous coordinator assets

Supporting assets for the [`/raid`](../../ai/agents/claude-code/commands/raid.md) autonomous
Coordinator mode. The command is the harness; these are the durable, per-branch state it
drives. SSOT for phases: [`ai/rules/task-workflow.md`](../../ai/rules/task-workflow.md).

## What ships here

| Asset | Status | Purpose |
|---|---|---|
| [`raid-coordinator.py`](raid-coordinator.py) | **shipped, runnable** | the loop core: `next-cycle` (next PENDING with deps DONE) + `done-cycle <N> <sha>`. Project-agnostic; paths from active-task or defaults. |
| [`active-task.example.yaml`](active-task.example.yaml) | shipped | per-branch task identity (`.raid/active-task.yaml`; `.json` works zero-dep) |
| [`CYCLE_LOG.template.md`](CYCLE_LOG.template.md) | shipped | the status-board table the coordinator parses |
| [`cycle-runner-prompt.md`](cycle-runner-prompt.md) | shipped | the cold-start sub-agent template (reads only its brief + listed files) |

```bash
python raid-coordinator.py next-cycle           # JSON {cycle,title,brief_path} or {idle:true}
python raid-coordinator.py done-cycle 7 <sha>    # mark cycle 7 DONE
```

Durable state in the cycle log + audit log is what makes a run **resumable** — re-invoking
`/raid` picks up the next ready cycle. This mirrors the
[paperwork standard](../../documents/standards/paperwork-standard.md) Log→State + crash-recovery model.

## Project-supplied (NOT generalizable)

These are bespoke per task and are **not** shipped — the project provides them:

- **Per-cycle verifiers** — each cycle's acceptance check is task-specific.
- **Cycle briefs** — `docs/raid/cycle_briefs/<NN>_<slug>.md`, authored per task (declare deps in
  a `## Dependencies` section).
- **Quota / escalation hooks** — optional. The coordinator runs without them; wire a budget
  check into the loop if your run needs one (mirrors the gate's pluggable-integration pattern).
- **The mega-plan** — `workflow_doc` in active-task, human-authored.
