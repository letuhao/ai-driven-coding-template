# workflow-gate — the enforcement substrate

A small state machine that enforces the [Task Workflow](../../../ai/rules/task-workflow.md):
it classifies task size, tracks the current phase, records completion evidence, and (via a
pre-commit hook) blocks commits that skip VERIFY / POST-REVIEW / SESSION. `/loom`, `/warp`,
and `/raid` all drive the same gate.

A runnable, **project-agnostic** reference engine ships here: [`workflow-gate.py`](workflow-gate.py)
— one zero-dependency Python script (stdlib only; no assumption about the project's own
language). It works **zero-config**, or reads an optional per-project
[`workflow.config.json`](workflow.config.example.json) (YAML accepted if PyYAML is installed).
The engine is **identical across projects**; only the config differs ([ADR-009](../../../docs/decisions.md)).

```bash
python workflow-gate.py size M 3 4 0 85     # classify (logic=4, side_effects=0, context=85%)
python workflow-gate.py phase build         # enter a phase (refuses illegal jumps)
python workflow-gate.py complete verify "ran suite, 42 pass"
python workflow-gate.py status
```

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

## Per-project config (the only thing that changes per project)

```json
{
  "module_globs": ["services/*", "packages/*", "apps/*"],
  "paths": { "audit": "docs/audit/AUDIT_LOG.jsonl" },
  "verify": { "cross_module_smoke": true, "smoke_tokens": ["live smoke", "live infra unavailable"] },
  "integrations": { "lessons_store_cmd": null, "guardrails_cmd": null }
}
```

- `module_globs` — which path prefixes count as independently-deployed modules (generalizes
  the source's hardcoded `services/<name>/` cross-module smoke detection).
- `integrations.lessons_store_cmd` / `guardrails_cmd` — **optional, pluggable** shell commands;
  `null` ⇒ no-op (the engine never depends on them). A configured lessons command is invoked at
  RETRO as `<cmd> --title … --content … --tags …`.
- The scaffolder fills this file per project (placeholders where useful); the engine code is
  never edited.

## Still to port (separate scripts)

The `slices` subcommand delegates to `workflows/warp/slice-manifest-validate.py`, and the raid
cycle-helper/quota scripts are specified as contracts in their READMEs — not yet implemented.
