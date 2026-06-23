# templates/ — classic source scaffolds

Minimal, idiomatic starting points for source code. This is **Dimension 1**.

```
languages/   minimal, idiomatic per-language starts (no architecture opinion)
  python/
  typescript/
  go/
  rust/
stacks/      opinionated full-stack combos
  nextjs-supabase/
  fastapi-postgres/
  react-spring-boot/
```

## Rules for entries

- **`languages/*` carry no architecture opinion** — just a clean, buildable start
  (formatter, linter, test runner, `.gitignore`, `.env.example`). Architecture
  comes from [`../architectures/`](../architectures/), composed by a recipe.
- **`stacks/*` are opinionated combos** that are tedious to wire up by hand.
- Use the project-wide **placeholder convention** (see
  [`../docs/decisions.md`](../docs/decisions.md)) for names — e.g. `{{project_name}}`.
- Each entry must **build and pass tests** in CI (see template-verification job).
  Record a **"last verified"** date in the entry's own README.
- Ship safe defaults: secrets-aware `.gitignore`, `.env.example` (never `.env`),
  pinned dependencies, no hardcoded credentials.
