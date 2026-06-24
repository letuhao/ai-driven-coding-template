# {{project_name}}

A minimal, idiomatic Python start (src layout). **No architecture opinion** — add structure
from [`architectures/`](../../../architectures/) via a recipe.

## Layout

```
pyproject.toml                  name {{project_name}}; ruff + pytest; pinned dev deps
src/{{python_package}}/         the importable package
  greeting.py                   first behavior (replace it)
tests/test_greeting.py          its test (pytest)
```

## Use

```bash
python -m venv .venv && . .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -e ".[dev]"
pytest          # tests
ruff check .    # lint
ruff format .   # format
```

Pinned dev deps + safe defaults: secrets-aware `.gitignore`, `.env.example` (never commit `.env`).

<!-- Scaffolder fills {{project_name}} and {{python_package}}. last verified: TODO (pending template-verification CI, ADR-002). -->
