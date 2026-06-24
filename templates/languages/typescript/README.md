# {{project_name}}

A minimal, idiomatic TypeScript (ESM) start. **No architecture opinion** — add structure
from [`architectures/`](../../../architectures/) via a recipe.

## Layout

```
package.json          name {{project_name}}; pinned dev deps
tsconfig.json         strict, ES2022, ESM
src/index.ts          entrypoint
src/greeting.ts       first behavior (replace it)
src/greeting.test.ts  its test (vitest)
eslint.config.mjs     flat ESLint config
.prettierrc.json      formatter
```

## Use

```bash
npm install
npm test       # vitest run
npm run lint   # eslint .
npm run build  # tsc -> dist/
```

Pinned dev deps + safe defaults: secrets-aware `.gitignore`, `.env.example` (never commit `.env`).

<!-- Scaffolder fills {{project_name}}. last verified: TODO (pending template-verification CI, ADR-002). -->
