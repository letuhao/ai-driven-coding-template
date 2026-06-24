# {{project_name}}

A minimal, idiomatic Go start. **No architecture opinion** — add structure from
[`architectures/`](../../../architectures/) via a recipe.

## Layout

```
go.mod            module {{go_module}}
main.go           entrypoint
greeting.go       first behavior (replace it)
greeting_test.go  its test
.golangci.yml     linter config
Makefile          fmt · lint · test · build
```

## Use

```bash
make test     # go test ./... -race -cover
make lint     # golangci-lint run
make build
go run .
```

Ships safe defaults: secrets-aware `.gitignore`, `.env.example` (never commit `.env`).

<!-- Scaffolder fills {{project_name}} and {{go_module}}. last verified: TODO (pending template-verification CI, ADR-002). -->
