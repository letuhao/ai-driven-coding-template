# Contributing

## Adding a catalog entry

- **template** → `templates/languages/<lang>` or `templates/stacks/<combo>`;
  must build + pass tests in CI; include a "last verified" date.
- **architecture** → `architectures/<name>/README.md`; doc-first (what / when /
  skeleton / composition notes). Mirror `architectures/hexagonal/`.
- **workflow** → `workflows/<area>/<name>`; a drop-in fragment, parameterized by
  the placeholder convention.
- **ai asset** → keep substance in `ai/rules` & `ai/prompts` (tool-agnostic);
  only `ai/agents/<tool>` may assume a tool.

## Adding a recipe

Create `recipes/<name>/recipe.yaml` referencing existing catalog pieces only.
Set `maturity` and `tags`. The assembler validates that every referenced path
exists.

## Invariants (CI-enforced where possible)

1. Every template/recipe instantiates and builds.
2. No catalog except `ai/agents/` assumes a specific AI tool.
3. Placeholder convention used consistently.
4. Safe-by-default: secrets-aware `.gitignore`, `.env.example`, pinned deps.
