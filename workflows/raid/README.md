# workflows/raid — autonomous coordinator assets

Supporting assets for the [`/raid`](../../ai/agents/claude-code/commands/raid.md) autonomous
Coordinator mode. The command is the harness; these are the durable, per-branch state it
drives. SSOT for phases: [`ai/rules/task-workflow.md`](../../ai/rules/task-workflow.md).

## What belongs here (and where it lives in a project)

| Asset | Location in a project | Purpose |
|---|---|---|
| `active-task.yaml` | `.raid/active-task.yaml` | per-branch task identity — which task is active on this branch |
| Cycle log | `docs/raid/CYCLE_LOG.md` | one row per cycle: status, deps, commit sha, completed_at |
| Cycle briefs | `docs/raid/cycle_briefs/<NN>-<slug>.md` | the hermetic brief a cold-start cycle runner reads |
| Escalations | `docs/raid/ESCALATIONS.md` | where a halted cycle records cycle/type/reason/action |
| Quota / budget log | `docs/raid/QUOTA_LOG.jsonl` | per-cycle burn, drives the proceed/warn/pause check |
| In-progress state | `docs/raid/IN_PROGRESS/cycle-<N>-state.md` | per-cycle crash-recovery state |

Durable state in the cycle log + audit log + in-progress files is what makes a run
**resumable** — re-invoking `/raid` picks up the next ready cycle. This mirrors the
[paperwork standard](../../documents/standards/paperwork-standard.md) Log→State + crash-recovery model.

## active-task.yaml (shape)

```yaml
task: <task-slug>
branch: <branch this task runs on>
workflow_doc: docs/raid/<task>/RAID_WORKFLOW.md   # the task's mega-plan
cycle_log:   docs/raid/CYCLE_LOG.md
quota_log:   docs/raid/QUOTA_LOG.jsonl
bounds:                                            # paths a cycle may NOT touch
  - <charter / SSOT>
  - <prod env>
```

## Porting note

Generalize the cycle-helper + quota-check scripts (prefer one runtime). Keep the
**Coordinator overhead budget** (small per-cycle token cost) and the **cold-start cycle
runner** (reads only its brief + listed files), so long runs don't accumulate context.
