# workflows/ci-cd — pipeline presets

Drop-in CI pipeline fragments a recipe copies into a project (`.github/workflows/`,
`.gitlab-ci.yml`, …).

## This collection's own template-verification CI

The most important preset is the **template-verification job** (ADR-002): it assembles each
template via the real assembler and **builds + tests the generated project**, so scaffolds
don't silently rot. The collection runs it on itself — see
[`.github/workflows/template-verify.yml`](../../.github/workflows/template-verify.yml). It:

- assembles `go-minimal` / `python-microservice-tdd` / `ts-minimal` and builds+tests each;
- Spectral-lints the example OpenAPI contract;
- self-tests the workflow scripts (gate risk-floor block, warp validator BLOCK on overlap);
- runs on push, PR, and a weekly schedule (catches rot in pinned deps/toolchains).

Copy it as a starting point for a generated project's own CI, or as the model for a GitLab/other
runner. Keep CI presets parameterized by the `{{ }}` placeholder convention where they name the
project or package paths.
