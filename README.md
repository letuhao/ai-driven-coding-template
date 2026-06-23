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

## Picking pieces

See [`docs/choosing.md`](docs/choosing.md) for the decision matrix
(which architecture / process fits your case) and [`docs/decisions.md`](docs/decisions.md)
for the design rationale behind this collection.
