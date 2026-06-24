# workflows/warp — parallel-execution assets

Supporting assets for the [`/warp`](../../ai/agents/claude-code/commands/warp.md)
parallel-execution mode. The command is the harness; these are the durable scaffolding it
drives. SSOT for phases: [`ai/rules/task-workflow.md`](../../ai/rules/task-workflow.md).

## What belongs here

| Asset | Purpose | Contract |
|---|---|---|
| `EXAMPLE-manifest.yaml` | the slice manifest shape | disjoint write-sets + a frozen interface pinned by git blob sha |
| `slice-manifest-validate` (script) | the independence gate | proves write-sets are path-prefix-disjoint + frozen files unchanged vs pinned sha; exit non-zero = BLOCK |
| `worktrees` (script) | slice worktree lifecycle | `check` / `list` / `cleanup` / **`pin-base`** (force a slice branch onto BASE_SHA — the self-heal) |
| `slice-runner-prompt.md` | the slice sub-agent template | reads ONLY the frozen interface + its own write-set; returns a small structured result |

A run records its manifest + slice briefs under `docs/warp/<task-slug>/` (durable record).

## Porting note

Generalize from the source repo: replace `services/<name>/` write-set prefixes with the
project's module-boundary globs; prefer one runtime (e.g. `python`) for the scripts to avoid
shell-shim issues on Windows; keep the **BASE_SHA pin + post-fan-out descent check** — worktree
isolation does not reliably base a slice on HEAD.
