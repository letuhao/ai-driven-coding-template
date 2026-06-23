# Standards optimization plan

How we turn three mature repos into generalized, drop-in template standards.
**This is a plan, not the extraction** — nothing under the catalogs changes until
this is reviewed. Decisions here feed back into [`decisions.md`](decisions.md).

## Sources

DLF is **WIP and not yet adopted** into the other two repos — they are **not**
case studies of it. They are mature working repos with an *earlier, ad-hoc*
paperwork approach; DLF's Paperwork Standard is the **successor design** that
supersedes that approach.

| Repo | Role | What it contributes |
|---|---|---|
| `dead-light-framework` (DLF) | the **methodology** — WIP, designed but not yet adopted | the chosen Paperwork Standard, governance model, role guides, decision-debate process, templates |
| `lore-weave` | mature working repo — polyglot product | the **workflow toolkit** (`/loom` primary, `/raid` long-run, `/amaw` rare), RAID cycles, contract-first OpenAPI, per-service layout; *earlier* ad-hoc docs taxonomy |
| `free-context-hub` | mature working repo — TS context-hub/KG service | workflow substrate (`workflow-gate`, `review-impl`), QC harness; *earlier* ad-hoc docs taxonomy + handoff/log |

Guiding rules:
- For **tooling/workflow**, harvest the **tiered toolkit** with `/loom` as the
  default daily driver; `/raid` (long runs) and `/amaw` (rare, load-bearing) escalate
  from it. Generalize the shared substrate (CLAUDE.md Task-Workflow SSOT + workflow-gate)
  before the individual commands.
- For the **paperwork spine**, DLF **supersedes** the ad-hoc taxonomies *by design*,
  even though it is not yet battle-tested — see below for why.

## Why the DLF Paperwork Standard is the spine

It is the only one of the three designed for the hard case: **many agents working
across many services/modules at the same time — one branch or many — conflict-free.**
The mechanism:

- **Append-only Logs** — agents *append*, never edit shared state, so concurrent
  writers don't collide.
- **State derived as a CRDT fold** over the logs — divergent regenerations are
  guaranteed to converge; two agents folding the same logs cannot disagree.
- **Partition by administrative unit** + a federation model — each service/module
  owns its own log stream; cross-repo work composes without a central lock.
- **Self-sufficient log bundles + re-priming from local copies** — a fresh agent
  session rebuilds full context with no coordination.

The ad-hoc taxonomies in lore-weave / free-context-hub carry session state well for a
*single* stream of work but were not designed for conflict-free concurrency. The
template adopts DLF's model as the standard and treats those taxonomies as input on
*document categories*, not on the concurrency model.

## Decision 1 — naming: NEUTRALIZE FULLY

DLF's Warhammer-40K vocabulary maps to plain, canonical terms. The template ships
only the neutral names; no theme overlay.

| DLF term | Neutral canonical term |
|---|---|
| Astronomican | **Sealed Charter** — immutable project purpose, laws, principles |
| Ascension Council | **Founding Council** — the one-time charter-sealing group |
| High Lords | **Stewards** — humans with interpretation authority over the charter |
| Planetary Governors | **Workstream Leads** — humans leading individual modules |
| Chapter | **Agent Role** — a category of AI agent |
| Codex (per chapter) | **Agent Operating Bounds** — a role's permissions, hard stops, autonomy thresholds, output contract |
| The Chaos | **Failure Modes** — context rot, architect rot, authority drift, scope chaos |
| Notify Triggers (N-1..N-5) / CCIR | **Escalation Triggers** — the closed set that forces escalation |
| Hard Stop / HS-2 owner sign-off | **Hard Stop / Owner Sign-off Gate** |
| Re-priming protocol | **Session Re-priming** — how a fresh session reloads state |
| Departure / Reckoning records (D-N, AAR) | **Handoff Record / After-Action Record** |
| Sectoring | **Partitioning** — splitting work by administrative unit |
| Tier-decision-card | **Tier Selection Guide** |
| M-tier (M0, M1, …) | **Maturity Tier** — project size/scale band that gates which standards apply |
| Debate | **Decision Record** (adversarial variant of an ADR) |

A `documents/glossary.md` will carry this table so the mapping is discoverable and
contributions stay consistent.

## Decision 2 — deliverable: this plan first

Resolved. Extraction proceeds only after review.

## Asset → template-entry mapping

### Dimension 5 — `documents/` (the spine)

| Source asset | Generalized entry | Generalize / strip |
|---|---|---|
| DLF Paperwork Standard v1.2 | `documents/standards/paperwork-standard.md` | Strip 40K terms; keep Log→State, self-sufficient log bundles, re-priming, Maturity-Tier sizing, CAP-AP framing. Trim provenance to a short note. |
| lore-weave `docs/00_index…05_qa` | `documents/taxonomy/` (README + numbered skeleton) | Document the **numbering rule** to stop drift (see drift notes). |
| DLF `handoff-template` / `log-template` | `documents/handoff/TEMPLATE.md`, `documents/log/TEMPLATE.md` | Neutralize; keep append-only + derived-state shape. |
| DLF `astronomican-template` | `documents/charter/TEMPLATE.md` | Rename to Sealed Charter. |
| lore-weave dated `specs/` + `plans/` | extend existing `documents/spec/` with the `YYYY-MM-DD-topic.md` + paired-plan convention | — |
| DLF `debates/` | `documents/adr/` gains a **decision-debate** variant | Keep adversarial structure; drop chapter lore. |

### Dimension 4 + 3 — `ai/` and `workflows/` (the workflow toolkit)

The workflow layer is a **tiered toolkit**, not a single workflow. `/loom` is the
default; the others escalate from it. All share one substrate: a **CLAUDE.md "Task
Workflow" SSOT** + **`workflow-gate`** enforcement + the `review-impl` review step.
Generalize the *substrate first*, then each tier as a command on top of it.

| Tier | Source asset | Usage | Generalized entry | Generalize / strip |
|---|---|---|---|---|
| **substrate** | CLAUDE.md "Task Workflow" + `scripts/workflow-gate.{sh,py}` + `.workflow-state.json` | always | `workflows/loom/gate/` + `ai/rules/task-workflow.md` (the SSOT) | The 12-phase model + size table + anti-skip gate are the core. Strip repo-specific service notes. |
| **`/loom`** (primary) | `.claude/commands/loom.md` | almost always | `ai/agents/claude-code/commands/loom.md` | 12-phase human-in-loop, size-classified, PO checkpoints. Strip monorepo/service specifics; parameterize handoff paths. |
| **`/raid`** (long runs) | `.claude/commands/raid.md` + `.raid/active-task.yaml` + `scripts/raid/*` + `docs/raid/*` | long runs | `workflows/raid/` (autonomous coordinator) | Generalize cycle log, briefs, quota governance, per-branch `active-task.yaml`, escalations, resume semantics. |
| **`warp`** ("more control") | **not yet created in any repo** (user confirmed uncommitted/absent) | frequent-ish | TBD — capture once defined | Pending: user to describe what "more control" means vs loom/raid before it can be generalized. |
| **`/amaw`** (rare deepening) | `.claude/commands/amaw.md` + `agentic-workflow/` | rarely, opt-in | `ai/agents/claude-code/commands/amaw.md` | Position as an L+ load-bearing escalation invoked *inside* loom — NOT the headline workflow. |
| shared | `.claude` / `.cursor` / `.kiro` coexistence; `review-impl` | — | `ai/agents/<tool>/`; `ai/rules/` + `ai/prompts/` as shared source | Extract common rules from the three CLAUDE.md files; flag CLAUDE.md size growth as drift (keep rules small/composable). |

### Dimension 3 — `workflows/` (contracts)

| Source asset | Generalized entry | Generalize / strip |
|---|---|---|
| lore-weave `contracts/api/*/v1/openapi.yaml` + `.spectral.yaml` | `workflows/contracts/openapi-spectral/` | Ship the Spectral ruleset + a versioned-OpenAPI layout convention + a sample contract. |

### Dimension 2 + 1 — `architectures/` and `templates/`

| Source asset | Generalized entry | Generalize / strip |
|---|---|---|
| lore-weave Go service layout (`cmd/ + internal/{api,config,…}`) | `architectures/` skeleton + `templates/languages/go` | Make the `internal/` layout concrete; keep `.env.example`, Dockerfile, migrate pattern. |
| free-context-hub TS service (`src/{api,services,core,db}`, migrations, docker-compose) | `templates/languages/typescript` + `templates/stacks/` | Strip product specifics; keep structure + tooling. |

### Adoption guides — `docs/`

| Source asset | Generalized entry |
|---|---|
| DLF `distribution/for-{pms,ics,ai-aides,adopters}.md` | `docs/adoption/` role guides, neutralized |
| DLF `tier-decision-card`, `deployment-matrix` | fold into `docs/choosing.md` (Maturity-Tier gating) |

## Drifts observed (the standards must prevent these)

- lore-weave: duplicate `docs/04_analysis` **and** `docs/04_integration` (numbering
  collision) → taxonomy entry must state a one-owner-per-number rule.
- lore-weave: malformed tracked path with embedded newline under `services/` → add a
  path-hygiene lint to the template-verification CI (ADR-002).
- CLAUDE.md grows 5k→22k→34k across the repos → `ai/rules/` must stay small and
  composable; flag oversized agent-context files in CI.
- `frontend/` vs `frontend-game/` ambiguity → naming convention should mark the
  canonical entry.

## Sequencing (after this plan is approved)

1. `documents/` spine — paperwork standard + taxonomy + glossary (neutralized).
2. Workflow toolkit into `ai/` + `workflows/`: substrate (gate + Task-Workflow SSOT)
   → `/loom` (primary) → `/raid` (long-run) → `/amaw` (rare). Slot `warp` in once defined.
3. Contract-first `workflows/contracts/`.
4. Language templates (Go, TS) + architecture skeletons.
5. Adoption guides + Maturity-Tier gating in `docs/choosing.md`.

## Still open

- **ADR-003 placeholder syntax** — must be locked before step 2 parameterizes the
  AMAW install. (unchanged)
- **Maturity-Tier thresholds** — DLF gates adoption at "M1 and above"; we need neutral,
  defined bands (what counts as M0 vs M1+) before the Tier Selection Guide is useful.
