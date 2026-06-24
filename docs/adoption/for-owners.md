# For project owners

You set the frozen authority and the gates. Three jobs:

## 1. Pick the Maturity Tier

Decide what the project needs ([choosing.md](../choosing.md), [ADR-007](../decisions.md)):
Tier 0 (prototype, README only) · Tier 1 (continuity: charter + handoff + log) · Tier 2
(federation: multiple units, partitioning). Adopt higher later; never lower.

## 2. Seal the Charter (Tier 1+)

The **Sealed Charter** ([documents/charter/TEMPLATE.md](../../documents/charter/TEMPLATE.md)) is
the frozen source of authority — purpose, immutable laws, guiding principles, boundaries. Fill
it with a small founding group, then **seal** it (pin at a commit). After sealing, no
participant — human or agent — rewrites it at will; changing it means re-convening the group.

- Keep laws/principles small (~7 each) so they fit working memory.
- State at least 3 explicit **out-of-scope** items — this is what stops agents over-building.

## 3. Set the gates

- The workflow's human checkpoints are **end of CLARIFY** and **POST-REVIEW** — you approve
  scope and you approve before commit. Everything between runs without you.
- Decide what is a **Hard Stop / owner sign-off** (migrations, security-critical paths,
  destructive ops) so agents escalate instead of proceeding.
- A settled decision is recorded once (a Decision Record / `[sealed]` log entry) and not
  re-litigated; that is the whole point of the paperwork standard.

You don't run the toolkit day-to-day — you own the charter, the tier, and the gates. The rest
is [for-developers.md](for-developers.md) and [for-ai-agents.md](for-ai-agents.md).
