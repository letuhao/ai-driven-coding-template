# ai-driven-coding-template

A collection that helps you stand up a new, AI-ready repository fast.

It is organized around **four independent dimensions** you mix and match, plus a
**recipe** layer that composes them into a ready-to-use project.

| Dimension | Folder | Varies by |
|---|---|---|
| Source scaffolds | [`templates/`](templates/) | tech choice |
| Architecture patterns | [`architectures/`](architectures/) | design choice |
| Environment & process automation | [`workflows/`](workflows/) | team choice |
| AI agent assets | [`ai/`](ai/) | tooling choice |
| Paperwork standards | [`documents/`](documents/) | artifact choice |

The catalogs stay **flat and orthogonal** so each grows independently. Instead of
pre-building every cross-product, a [`recipe`](recipes/) is a thin manifest that
points at one piece from each catalog. The [assembly script](scripts/) reads a
recipe and emits a new project.

## Quick start

```bash
# list available recipes
scripts/new-project --list

# create a project from a recipe
scripts/new-project --recipe python-microservice-tdd --name my-service --out ../my-service
```

## Layout

```
templates/      classic source scaffolds (languages/, stacks/)
architectures/  structural patterns — doc-first (when to use, skeleton, tradeoffs)
workflows/      ci-cd/, devcontainers/, git/, testing/, release/
ai/             agents/<tool>/, rules/, prompts/, subagents/, mcp/
documents/      paperwork standards — spec/, adr/, github/
recipes/        composers: one pick from each dimension -> recipe.yaml
scripts/        assembles a new repo from a recipe
docs/           choosing.md (decision matrix), contributing.md, decisions.md
```

## Create a project

```bash
python scripts/new-project.py --list
python scripts/new-project.py --recipe go-minimal --name myapp \
  --var go_module=example.com/myapp --out ../myapp
```

## Picking pieces

- [`docs/adoption/`](docs/adoption/) — how to adopt this collection, by role (owner / developer / AI agent).
- [`docs/choosing.md`](docs/choosing.md) — decision matrix: architecture, process, contracts, Maturity Tier.
- [`docs/decisions.md`](docs/decisions.md) — the design rationale (ADRs).
- [`docs/optimization-plan.md`](docs/optimization-plan.md) — how the collection was harvested from three source repos.
