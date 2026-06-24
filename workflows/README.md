# workflows/ — environment & process automation

Reusable automation for the dev environment and development process.
This is **Dimension 3**.

```
loom/          the workflow substrate — gate/ (state machine + pre-commit enforcement)
warp/          parallel-execution assets — slice manifest + worktree/slice scripts
raid/          autonomous-coordinator assets — cycle log, briefs, quota, active-task
contracts/     contract-first interfaces (opt-in) — openapi-spectral + gRPC/async/graphql stubs
ci-cd/         github-actions/, gitlab-ci/, ... pipeline presets
devcontainers/ .devcontainer presets for reproducible environments
git/           branching models (trunk-based, gitflow), hooks, commit conventions
testing/       tdd, bdd setups and runners
release/       semver, changelog generation, conventional commits
```

## The workflow toolkit

`loom/`, `warp/`, `raid/` are the process-automation half of the agent workflow toolkit;
their command harnesses live in [`ai/agents/claude-code/commands/`](../ai/) and the shared
model is the SSOT in [`ai/rules/task-workflow.md`](../ai/rules/task-workflow.md). The 2×2:
loom (serial, human-gated) · warp (parallel, human-gated) · raid (autonomous) · amaw (overlay).

## Notes

- Entries are **drop-in fragments** a recipe copies into a target project.
- Keep CI presets parameterized by the placeholder convention where they
  reference project names or package paths.
- One CI preset should run this collection's own **template-verification job**:
  instantiate each template/recipe and build + test it on a schedule, so
  scaffolds don't silently rot.
