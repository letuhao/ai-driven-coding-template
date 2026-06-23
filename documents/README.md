# documents/ — paperwork standards

Templates for the project artifacts humans and AI agents read and write.
This is **Dimension 5**.

In AI-driven development the paperwork is the **interface** between human intent
and agent execution: a good spec lets an agent implement in one pass, an ADR
stops it re-litigating settled decisions, and consistent doc shapes make agent
output predictable and reviewable.

```
spec/         feature spec / PRD — the agent's primary input for building work
adr/          architecture decision record — why a decision was made
github/       issue + PR templates, CODEOWNERS
```

Future additions when a project actually needs them: `rfc/`, `design-doc/`,
`runbook/`, `postmortem/`. Keep this catalog **thin and opinionated** — ship the
artifacts that earn their keep, not every document type that exists.

## How it composes

- A [recipe](../recipes/) lists which document standards to drop into a new project.
- Pair with [`../ai/rules/`](../ai/): a rule can instruct the agent to read/write
  the spec in `documents/spec/` before implementing.
- Use the project-wide placeholder convention (see
  [`../docs/decisions.md`](../docs/decisions.md)) for names and dates.
