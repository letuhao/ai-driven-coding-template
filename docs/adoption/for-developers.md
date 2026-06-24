# For developers

Your day-to-day is the **workflow toolkit**. The model is the SSOT in
[ai/rules/task-workflow.md](../../ai/rules/task-workflow.md); keep it loaded.

## Pick the mode (the 2×2)

| | Serial | Parallel |
|---|---|---|
| **Human-gated** | `/loom` — default, almost always | `/warp` — decomposable M/L/XL across independent boundaries |
| **Autonomous** | (rare) | `/raid` — long multi-cycle runs |

`/amaw` is an opt-in deepening overlay (cold-start review roles) for L+ load-bearing work —
**you** turn it on; agents never self-propose it.

## The loop

1. **Classify size** from the repo root: `workflow-gate.py size <XS|S|M|L|XL> <files> <logic> <side_effects>`.
   Size by complexity + risk, not file count; side effects set a hard floor.
2. Drive **CLARIFY → … → RETRO** with the gate. STOP for the human at CLARIFY end + POST-REVIEW.
3. **VERIFY is an evidence gate** — run it, read the full output, *then* claim. ≥2 deployed
   modules ⇒ include a live cross-module smoke token.
4. **SESSION:** update the handoff's "Start here next"; land it in the same commit. **COMMIT:**
   stage changed files only; push only with approval. **RETRO:** record non-obvious lessons.

## State that survives sessions

- **`LOG.md`** is append-only history (never edit a past line); **`HANDOFF.md`** is the derived
  snapshot you rewrite freely. A fresh session reads HANDOFF, then LOG after its `cursor:`. See
  [paperwork standard](../../documents/standards/paperwork-standard.md).
- Specs/plans are dated `YYYY-MM-DD-<topic>.md` ([taxonomy](../../documents/taxonomy/README.md)).

## Contracts (if you expose an API)

If others consume your interface, freeze it first: an OpenAPI/Protobuf/AsyncAPI/GraphQL contract,
linted in CI ([workflows/contracts](../../workflows/contracts/README.md)). `/warp` pins it by git
blob sha during parallel work.
