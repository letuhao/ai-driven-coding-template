# recipes/ — the composer

A recipe picks **one piece from each dimension** and binds them into a project.
This is what makes "set up a new repo fast" actually happen, and it avoids
pre-building every cross-product of the catalogs.

```
<recipe-name>/
  recipe.yaml    references templates + architecture + workflows + ai assets
```

See [`python-microservice-tdd/recipe.yaml`](python-microservice-tdd/recipe.yaml)
for the schema in practice. The [assembly script](../scripts/) reads a recipe,
copies the referenced pieces, applies placeholder substitution, and emits a project.

## Maturity

Tag each recipe `experimental` | `stable` so users know what to trust, and so
`docs/choosing.md` can be generated from recipe metadata.
