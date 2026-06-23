# ai/ — AI agent assets

Everything that makes a repo "AI-ready." This is **Dimension 4**.

```
agents/      per-tool configs — the ONLY place that may assume a specific tool
  claude-code/
  cursor/
  copilot/
  windsurf/
rules/       reusable, tool-agnostic rule snippets (style, security, testing)
prompts/     reusable, tool-agnostic prompt/instruction fragments
subagents/   specialized agent definitions
mcp/         MCP server configs
```

## Design rules

- **Tool-agnostic substance lives in `rules/` and `prompts/`.** Only `agents/<tool>/`
  may assume a specific AI tool. This keeps the collection from being coupled to
  any one vendor.
- **Write once, generate per-tool.** Prefer composing tool files
  (`CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`) from shared
  `rules/` + `prompts/` fragments via an adapter, rather than maintaining each by hand.
- **Mind the context budget.** Rules load into every agent turn — keep each
  snippet small, single-purpose, and composable. Avoid monolithic walls.
