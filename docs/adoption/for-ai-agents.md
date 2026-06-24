# For AI agents — re-priming primer

You start from zero each session. This front-loads what you need to converge fast in a repo
built from this collection. Terminology: [documents/glossary.md](../../documents/glossary.md).

## Re-prime (in order)

1. **This primer** (you are here).
2. The **Sealed Charter** (`docs/.../charter` or the project's charter) — purpose, immutable
   laws, principles, boundaries. It is frozen authority; do not propose rewriting it.
3. The **workflow SSOT**: [ai/rules/task-workflow.md](../../ai/rules/task-workflow.md) — the
   12-phase model, size table, anti-skip rules.
4. **Current state**: read `HANDOFF.md` first, then the `LOG.md` lines committed **after** the
   handoff's `cursor:`. Now you are current. (Tier 2: also read the ancestor chain — see the
   [paperwork standard](../../documents/standards/paperwork-standard.md) §R12.)
5. **Spot inconsistencies** between the charter, the handoff, and the code before you act.

## Operate within bounds

- **Never** self-authorize a phase skip — STOP, announce, ask the human. Phases skip only per
  the size table.
- **Human checkpoints are hard:** STOP and WAIT at end of CLARIFY and at POST-REVIEW.
- **Never** modify a `[sealed]` decision or the Charter; if a sealed directive is wrong given
  new local facts, **suspend-and-refer-back** (don't override, don't silently obey).
- **VERIFY is evidence-gated:** run the command, read the full output, then claim. No "should work".
- Don't push without explicit approval. Stage only changed files.

## Output discipline

- **Log every state change** as a self-sufficient line: `<date> · <agent-id> · <kind> · <one
  sentence> [ (reason: …) ] [tags]`. Append-only; a correction is a new `dispute` line.
- On finishing, update `HANDOFF.md` (rewrite freely; reset `cursor:`), commit atomically, and
  record non-obvious lessons.
- Don't persist state in your context — persist it in the artifacts, so the next cold session
  recovers it.

## `/amaw` is human-initiated

Never propose, announce, or enable `/amaw` yourself — not even for load-bearing work. If the
human wants cold-start reviews, they turn it on.
