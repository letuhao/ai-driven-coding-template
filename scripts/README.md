# scripts/ — assembly tooling

Reads a [recipe](../recipes/) and emits a new project: copy the referenced
catalog pieces, overlay the architecture skeleton, apply placeholder
substitution, then run any post-init hooks.

```
new-project --list
new-project --recipe <name> --name <project> --out <dir> [--var key=value ...]
```

Provide both `new-project.ps1` (Windows) and `new-project.sh` (POSIX) as thin
wrappers over the same logic. Keep the assembler language-agnostic — it should
not know anything about Python/Node/etc., only about copying files and
substituting the placeholder convention (see [`../docs/decisions.md`](../docs/decisions.md)).
