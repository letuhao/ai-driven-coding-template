# recipes/ — the composer

A recipe binds catalog pieces into a project. This is what makes "set up a new repo fast"
actually happen — it avoids pre-building every cross-product of the catalogs. The
[assembler](../scripts/new-project.py) reads a recipe, copies its pieces, substitutes
`{{ variable }}` placeholders, and emits a working project.

```
<recipe-name>/
  recipe.json   (or recipe.yaml — needs PyYAML)
```

## Schema

```json
{
  "name": "go-minimal",
  "description": "...",
  "maturity": "experimental",          // experimental | stable
  "tags": ["go", "minimal"],
  "variables": {
    "project_name": { "required": true },
    "go_module":    { "required": true },   // or { "default": "..." }
  },
  "pieces": [
    { "src": "templates/languages/go", "dest": "." },          // base template at root
    { "src": "ai/agents/claude-code/commands", "dest": ".claude/commands" }
  ]
}
```

Each **piece** copies a collection path (file or dir) to `<out>/<dest>`. The base template
usually has `dest: "."`. Use as many pieces as the project needs — one from `templates/`, plus
any `ai/`, `workflows/`, `documents/`, `contracts/` pieces. Gate inclusion of optional dimensions
(contracts, paperwork) by **Maturity Tier** ([choosing.md](../docs/choosing.md)).

## Examples (both assemble + verify)

- [`go-minimal`](go-minimal/recipe.json) — the 80% start: just the Go template.
- [`python-microservice-tdd`](python-microservice-tdd/recipe.yaml) — multi-piece: Python
  template + the loom workflow gate + the paperwork standard.

## Use

```bash
python scripts/new-project.py --list
python scripts/new-project.py --recipe go-minimal --name myapp --var go_module=example.com/myapp --out ../myapp
```
