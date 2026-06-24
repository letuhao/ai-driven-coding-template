# scripts/ — assembly tooling

[`new-project.py`](new-project.py) reads a [recipe](../recipes/) and emits a new project:
copy the referenced catalog pieces, substitute `{{ variable }}` placeholders in file
contents and names (scaffolder-fill, [ADR-003](../docs/decisions.md)), and write it out.
**Zero-dependency** Python (stdlib; PyYAML only for `.yaml` recipes). One-shot
([ADR-004](../docs/decisions.md)) — it does not track or update the project afterwards.

```bash
new-project --list
new-project --recipe <name> --name <project> --out <dir> [--var key=value ...]
```

`new-project` (POSIX sh) and `new-project.ps1` (Windows) are thin wrappers over
`new-project.py`. The assembler is **language-agnostic** — it only copies files and
substitutes the placeholder convention; the recipe decides what goes where.

## Verified end-to-end

- `go-minimal` → the **generated project builds + tests pass** (`go build`/`go test`).
- `python-microservice-tdd` → the **generated project's test passes** and the bundled
  `workflow-gate.py` runs inside it; `{{python_package}}` dir is renamed, no `{{ }}` remain.
