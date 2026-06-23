# architectures/ — structural patterns

Architecture is a **decision** more than code, so entries here are **doc-first**.
This is **Dimension 2**.

```
monolith/
modular-monolith/
hexagonal/
microservices/
ddd/
```

Each entry contains a `README.md` with:

1. **What it is** — one-paragraph description.
2. **When to use it / when not to** — the honest tradeoffs.
3. **Folder skeleton** — the directory layout it implies, language-agnostic.
4. **Composition notes** — how it overlays onto a `templates/languages/*` start.

A recipe references an architecture to lay its skeleton over a chosen language
template. Keep these decoupled from any specific language or AI tool.
