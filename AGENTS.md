# AGENTS.md

Guidance for an AI agent working in **this template-collection repo**. (For an agent working
in a project *generated* from it, see [`docs/adoption/for-ai-agents.md`](docs/adoption/for-ai-agents.md).)

## If the task is "create / scaffold a project" — DO NOT read the catalogs

Just run the assembler. It copies the right pieces and fills `{{ }}` placeholders for you:

```bash
python scripts/new-project.py --list
python scripts/new-project.py --recipe <name> --name <project> [--var key=value ...] --out <dir>
```

Recipes: `go-minimal`, `ts-minimal`, `python-microservice-tdd`. Required `--var`s are reported
if you omit them. You do **not** need to read `templates/`, `workflows/`, `documents/`, or the
ADRs to do this — that would waste context.

## If the task is "extend the collection" — read only what you touch

| You're adding… | Read only |
|---|---|
| a language template | [`templates/README.md`](templates/README.md) + an existing `templates/languages/*` |
| a recipe | [`recipes/README.md`](recipes/README.md) (the `pieces` schema) |
| a workflow command/script | [`ai/rules/task-workflow.md`](ai/rules/task-workflow.md) (the SSOT) + the relevant `workflows/*` |
| a contract preset | [`workflows/contracts/README.md`](workflows/contracts/README.md) |
| a paperwork doc | [`documents/README.md`](documents/README.md) + [`documents/glossary.md`](documents/glossary.md) |

The design rationale (why things are shaped this way) is in [`docs/decisions.md`](docs/decisions.md)
(ADR-001..010) — consult a specific ADR only when a decision is unclear; don't read all of it.

## Invariants to respect when extending

- **Placeholders:** `{{ var }}` = scaffolder-filled; `<blank>` = author-time human fill (ADR-003).
- **Templates carry no architecture opinion** and must build+test after rendering (ADR-002).
- **Generic engine + per-project config** everywhere — never hardcode project specifics into a
  script; put them in config (`workflow.config.json`, `.raid/active-task`, recipe `pieces`).
- **Safe defaults:** secrets-aware `.gitignore`, `.env.example`, pinned deps, no hardcoded creds.
- Only `ai/agents/<tool>/` may assume a specific AI tool; keep `ai/rules`+`ai/prompts` tool-agnostic.
