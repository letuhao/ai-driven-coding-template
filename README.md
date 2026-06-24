# ai-driven-coding-template

A collection that helps you stand up a new, AI-ready repository fast.

It is organized around **five independent dimensions** you mix and match, plus a **recipe**
layer + an **assembler** that compose them into a working project.

| Dimension | Folder | Varies by |
|---|---|---|
| Source scaffolds | [`templates/`](templates/) | tech choice |
| Architecture patterns | [`architectures/`](architectures/) | design choice |
| Environment & process automation | [`workflows/`](workflows/) | team choice |
| AI agent assets | [`ai/`](ai/) | tooling choice |
| Paperwork standards | [`documents/`](documents/) | artifact choice |

The catalogs stay **flat and orthogonal** so each grows independently. Instead of
pre-building every cross-product, a [recipe](recipes/) lists the catalog **pieces** a project
needs, and the [assembler](scripts/new-project.py) copies them and fills `{{ }}` placeholders.

## Create a project

```bash
python scripts/new-project.py --list
python scripts/new-project.py --recipe go-minimal --name myapp \
  --var go_module=example.com/myapp --out ../myapp
```

The generated project builds and tests out of the box (verified in CI). Recipes available:
`go-minimal`, `ts-minimal`, `python-microservice-tdd`.

## Layout

```
templates/      source scaffolds — languages/{go,typescript,python} (no architecture opinion)
architectures/  structural patterns — doc-first (when to use, skeleton, tradeoffs)
workflows/      loom (workflow gate) · warp · raid · contracts/ · ci-cd/ · git/ · testing/
ai/             agents/<tool>/commands · rules/ (task-workflow SSOT) · prompts/roles
documents/      paperwork standard (Log→State) · taxonomy · charter/handoff/log · glossary
recipes/        composers — recipe.json|yaml: pieces[{src,dest}] + variables
scripts/        new-project.py — assembles a project from a recipe
docs/           adoption/ · choosing.md · decisions.md (ADRs) · optimization-plan.md
.github/        template-verify CI — assembles + builds every template (ADR-002)
```

## The workflow toolkit (the AI-driven core)

A 2×2 of modes sharing one [SSOT](ai/rules/task-workflow.md) + a generic
[`workflow-gate`](workflows/loom/gate/README.md): **loom** (serial, human-gated — the default),
**warp** (parallel, disjoint-slice fan-out), **raid** (autonomous long runs), **amaw** (opt-in
review overlay). State survives sessions via the append-only Log → derived Handoff model in the
[paperwork standard](documents/standards/paperwork-standard.md). Everything is a **generic
engine + per-project config** so it runs on any project.

## Picking pieces

- [`docs/adoption/`](docs/adoption/) — how to adopt this collection, by role (owner / developer / AI agent).
- [`docs/choosing.md`](docs/choosing.md) — decision matrix: architecture, process, contracts, Maturity Tier.
- [`docs/decisions.md`](docs/decisions.md) — the design rationale (ADR-001..010).
- [`docs/optimization-plan.md`](docs/optimization-plan.md) — how the collection was harvested from three source repos.

## License

MIT — see [LICENSE](LICENSE). Code you generate from these templates is yours, unencumbered.
