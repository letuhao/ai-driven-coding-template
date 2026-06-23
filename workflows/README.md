# workflows/ — environment & process automation

Reusable automation for the dev environment and development process.
This is **Dimension 3**.

```
ci-cd/         github-actions/, gitlab-ci/, ... pipeline presets
devcontainers/ .devcontainer presets for reproducible environments
git/           branching models (trunk-based, gitflow), hooks, commit conventions
testing/       tdd, bdd setups and runners
release/       semver, changelog generation, conventional commits
```

## Notes

- Entries are **drop-in fragments** a recipe copies into a target project.
- Keep CI presets parameterized by the placeholder convention where they
  reference project names or package paths.
- One CI preset should run this collection's own **template-verification job**:
  instantiate each template/recipe and build + test it on a schedule, so
  scaffolds don't silently rot.
