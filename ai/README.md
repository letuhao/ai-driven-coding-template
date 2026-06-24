# ai/ — AI agent assets

Everything that makes a repo "AI-ready." This is **Dimension 4**.

```
agents/      per-tool configs — the ONLY place that may assume a specific tool
  claude-code/
    commands/  loom · warp · raid · amaw · review-impl (the workflow toolkit)
  cursor/
  copilot/
  windsurf/
rules/       reusable, tool-agnostic rule snippets (style, security, testing)
  task-workflow.md   the workflow SSOT (12 phases, size table, anti-skip) — keep loaded
prompts/     reusable, tool-agnostic prompt/instruction fragments
  roles/     adversary · scope-guard · healer (cold-start review roles, used by /amaw)
subagents/   specialized agent definitions
mcp/         MCP server configs
```

## Workflow toolkit

The `commands/` are thin harnesses; the **substance is tool-agnostic** in `rules/task-workflow.md`
(the SSOT) and `prompts/roles/`. The enforcement substrate (gate + state machine) lives under
[`workflows/loom/gate/`](../workflows/). See [`rules/task-workflow.md`](rules/task-workflow.md)
for the 2×2 model (loom / warp / raid + amaw overlay).

## Design rules

- **Tool-agnostic substance lives in `rules/` and `prompts/`.** Only `agents/<tool>/`
  may assume a specific AI tool. This keeps the collection from being coupled to
  any one vendor.
- **Write once, generate per-tool.** Prefer composing tool files
  (`CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`) from shared
  `rules/` + `prompts/` fragments via an adapter, rather than maintaining each by hand.
- **Mind the context budget.** Rules load into every agent turn — keep each
  snippet small, single-purpose, and composable. Avoid monolithic walls.
