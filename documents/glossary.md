# Glossary — neutralized terms

The paperwork/governance standard in this collection is harvested from the Dead Light
Framework (DLF), whose source uses themed vocabulary. Per [ADR (naming)](../docs/optimization-plan.md)
the template ships **only the neutral canonical terms below**. This table is the
authoritative mapping; contributions must use the canonical column.

| Canonical term (use this) | Meaning | DLF source term |
|---|---|---|
| **Sealed Charter** | Immutable project purpose, laws, principles — frozen authority no participant rewrites at will | Astronomican |
| **Founding Council** | The one-time group that seals the Charter before kickoff | Ascension Council |
| **Steward** | Human with interpretation authority over the Charter | High Lord |
| **Workstream Lead** | Human leading an individual module of work | Planetary Governor |
| **Agent Role** | A category of AI agent | Chapter |
| **Agent Operating Bounds** | A role's permissions, hard stops, autonomy thresholds, output contract | Codex |
| **Failure Modes** | The drift the standard defends against: context rot, architect rot, authority drift, scope chaos | The Chaos |
| **Escalation Trigger** | The closed set of conditions that force an agent to stop and escalate | Notify Trigger / CCIR |
| **Hard Stop / Owner Sign-off Gate** | A point an agent may not pass without human sign-off | Hard Stop / HS-2 |
| **Session Re-priming** | How a fresh session reloads full state from local copies | Re-priming protocol |
| **Handoff Record / After-Action Record** | Durable record of session state / what happened after the fact | Departure / Reckoning record |
| **Partitioning** | Splitting work by administrative unit (Tier 2) | Sectoring |
| **Maturity Tier** | Project size/scale band that gates which standards apply (Tier 0/1/2) | M-tier (M0/M1/M2) |
| **Decision Record** | A recorded decision; the adversarial variant is a *decision-debate* | Debate |
| **State document** | The current-snapshot doc, derived from the Log (`HANDOFF.md`) | (same) |
| **Log document** | The append-only history doc; source of truth (`LOG.md`) | (same) |

See [[paperwork-standard]] for how these compose. A `[[name]]` link points at a file in
this catalog by its slug.
