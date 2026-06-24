# workflow-gate — the enforcement substrate

A small state machine that enforces the [Task Workflow](../../../ai/rules/task-workflow.md):
it classifies task size, tracks the current phase, records completion evidence, and (via a
pre-commit hook) blocks commits that skip VERIFY / POST-REVIEW / SESSION. `/loom`, `/warp`,
and `/raid` all drive the same gate.

This entry specifies the **contract**, so it can be implemented in any language. (Reference
implementation to be ported as a cross-platform script — prefer one runtime, e.g. `python`,
to sidestep shell-shim issues on Windows.)

## State file

One `.workflow-state.json` at the **repo root** (a subdir invocation would split it). Holds:
size classification, current phase, per-phase completion + evidence string, and an
`amaw_enabled` flag.

## CLI

```bash
gate size <XS|S|M|L|XL> <files> <logic> <side_effects> [context_pct]   # classify (mandatory first)
gate phase <name>                                                       # enter a phase
gate complete <name> "<evidence>"                                       # mark a phase done with evidence
gate status                                                             # show progress
gate amaw-enable [task-slug]                                            # flip the opt-in amaw flag
```

- `size` is mandatory before work; it sets allowed skips (size table) and the risk floor.
- `complete verify "<evidence>"` requires a real evidence string. When `git diff --name-only`
  shows **≥2 independently deployed modules**, the gate emits a **soft warning** unless the
  evidence carries a live-cross-module-smoke token (or an explicit deferral / infra-unavailable
  reason). Advisory, never blocking — the agent decides to smoke now or defer explicitly.

## Enforcement points

1. **Phase jumps** — `phase` refuses an out-of-order transition not permitted by the size
   table's allowed-skips.
2. **Pre-commit hook** — blocks a commit when VERIFY / POST-REVIEW / SESSION evidence is
   missing for the current effort.

## Generalize / strip (when porting from the source repo)

- Replace `services/<name>/` cross-service detection with a configurable
  **module-boundary glob** (which path prefixes count as independently deployed units).
- The optional **lessons store** bridge (RETRO `add_lesson`) is pluggable — default to
  appending a note in the handoff when no store is configured.
- Parameterize artifact paths (handoff, specs, plans, audit log) via the project's config,
  defaulting to the [document taxonomy](../../../documents/taxonomy/README.md).
