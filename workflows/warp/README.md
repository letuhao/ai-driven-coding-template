# workflows/warp — parallel-execution assets

Supporting assets for the [`/warp`](../../ai/agents/claude-code/commands/warp.md)
parallel-execution mode. The command is the harness; these are the durable scaffolding it
drives. SSOT for phases: [`ai/rules/task-workflow.md`](../../ai/rules/task-workflow.md).

## What belongs here

| Asset | Status | Purpose / contract |
|---|---|---|
| [`EXAMPLE-manifest.yaml`](EXAMPLE-manifest.yaml) | shipped | the slice manifest shape — disjoint write-sets + a frozen interface pinned by git blob sha |
| [`slice-manifest-validate.py`](slice-manifest-validate.py) | **shipped, runnable** | the independence gate — pairwise path-prefix-disjoint write-sets, frozen-path immutability, reads-bounded; `--verify-frozen` checks HEAD blob shas. Exit 1 = BLOCK. Project-agnostic. |
| [`worktrees.py`](worktrees.py) | **shipped, runnable** | slice worktree lifecycle — `check` / `list` / `cleanup` / **`pin-base`** (force a slice branch onto BASE_SHA — the self-heal). Project-agnostic. |
| `slice-runner-prompt.md` | to port | the slice sub-agent template — reads ONLY the frozen interface + its own write-set; returns a small structured result |

The two scripts are **zero-dependency Python** (PyYAML only needed for `.yaml` manifests; `.json`
works stdlib-only). The [gate](../loom/gate/README.md) `slices` subcommand delegates to the
validator. A run records its manifest + slice briefs under `docs/warp/<task-slug>/`.

```bash
python slice-manifest-validate.py <manifest.json|.yaml> [--verify-frozen]
python worktrees.py check --task <slug>          # refuse a new fan-out if stale worktrees linger
python worktrees.py pin-base --branch warp/<slug>/slice-<id> --base <BASE_SHA>   # inside a slice
```

## Why these are already general

Both operate on **declared inputs** (the manifest's own write-sets; a git worktree namespace) —
no project-language or service-layout assumption. The only generalization applied was neutralizing
docstrings. Keep the **BASE_SHA pin + post-fan-out descent check**: worktree isolation does not
reliably base a slice on HEAD.
