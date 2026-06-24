---
title: Paperwork Standard — full reference (edge cases)
status: experimental
maturity: experimental
audience: both
read_when: on-demand — you hit a rare case the operational core does not cover
derived_from: Dead Light Framework Paperwork Standard (WIP)
---

# Paperwork Standard — full reference

> **Cold path — read on demand, not every session.** The [operational core](paperwork-standard.md)
> covers the 95% case and is what you load at each re-prime. Open *this* file only when you
> hit a rare situation: federation, lifecycle transitions, disputes, dormant decisions,
> concurrent-fold tie-breaks, long-partition catch-up. Keeping it out of the hot path is
> what keeps re-priming cheap on long autonomous runs. Terms: [[glossary]].

## R1. State vs Event (recap)

Two `doc_kind`s. **State doc** = what is true *now*, regenerated only, never hand-edited.
**Log doc** = events over *time*, append-only, a past entry is never edited. The Log is the
source of truth; the State is a deterministic CRDT-style fold of it (R6). A snapshot
disagreeing with the Log at an equal cursor is a **protocol violation**, not normal drift.

## R2. Partition model & tier hierarchy *(Tier 2)*

```
Root tier (shared)  — read by every unit: sealed Charter + shared operating bounds
                      + a root LOG of seal/amendment events. Bounded.
Unit                — one governance partition: its own HANDOFF.md + LOG.md + artifacts.
                      A unit MAY nest child units; it is then their parent tier.
```

The hierarchy can be deeper than two levels (`Root → parent unit → child unit → …`). A unit
reads its **full ancestor chain top-down to itself** (R12); it does **not** read a *sibling*
unit's Log. The **nearest common ancestor** of two peers is **their parent unit** (the Root
tier only when no closer parent exists). Shared artifacts live in that nearest common
ancestor (R9), recorded in *its* Log — placement classifies ownership, no guessing.

**Single-repo layout:** the repo root hosts the Root tier and the unit folders; there is no
separate "root coordinating unit". **Operating-bounds overrides** live *inside* a unit
(`.operating-bounds-overrides/`) and **extend, never relax** the shared bounds.

**Module granularity is a tag, not a folder:** below a unit, each Log entry carries a
`unit:` field naming the module; a module graduates to its own folder only on crossing the
partition trigger (R11).

## R3. Log entry — the self-sufficient durable bundle

| Field | Meaning |
|---|---|
| `ts` | ISO-8601 — human readability only; **not** the ordering key |
| `instance` | provenance of the acting session/agent |
| `event` | event type (R4) |
| `subject` | artifact / decision / item affected |
| `unit` | module tag (R2) |
| `post_state` | the subject's **full metadata after the change** |
| `content_ref` | path + version + **git blob SHA** of the payload (no inline content) |
| `causal_parent` | git SHA of the prior event in this unit's Log (R5) |
| `note` | one human-readable line |

`post_state` + `content_ref` let a later instance rebuild *state* and locate *content* with
no runtime context. **Self-sufficiency is mandatory** — it is what makes async work.

**Commit cadence:** an artifact change + its Log entry are committed in **one git commit**,
**per state change as it goes — not batched at session end**. A pre-commit crash then loses
only the single in-flight change; an uncommitted working-tree change is an **orphan** (R7).

## R4. Full event catalog

`unit.chartered` · `unit.sectored` · `session.started` · `session.ended` ·
`artifact.created` · `artifact.state_changed` · `artifact.superseded` ·
`decision.recorded` · `decision.sealed` · `decision.overrode_frozen_intent` (R8) ·
`decision.referred_back` (R8) · `dispute.resolved` · `escalation.raised` ·
`escalation.federation_stale` · `departure.recorded` · `log.entry_disputed`.

Two cross-cutting fields: `kind: request | board` (`request` blocks until an Authority-tier
response; `board` is non-blocking/claimable) and `priority: bulk | normal | expedited`
(a sync-ordering hint; `expedited` jumps the queue but never beats the propagation floor).

## R5. Causal ordering

Wall clocks aren't synchronized. **Ordering is by causal ancestry:** each entry's
`causal_parent` holds the git SHA of the prior committed event in this unit's Log,
inheriting git's tamper-evident hash chain. Genesis (`unit.chartered`) has
`causal_parent: null`; a graduated child unit also records `origin_anchor:` = the parent's
`unit.sectored` SHA, so the cross-repo link is explicit. A corrupt/missing parent is
detectable.

**Chunking:** when `LOG.md` would exceed the **500-line cap** it becomes a `log/` folder of
**monthly** files + a `log/INDEX.md` (chunk list in causal order; index exempt from the
cap). A chunk is archivable only once every downstream's sync cursor has passed it and no
live child unit's `origin_anchor` references it.

## R6. The snapshot — fold, cursor, eviction, staleness

**5-section handoff structure** (a receiving instance never searches for where info lives):
§1 Situation (established state) · §2 Mission (this unit's charter + inherited binding
context) · §3 Execution (open items — the computed Mechanical part) · §4 Sustainment
(ancestor refs + dependencies + federation pointers) · §5 Command & Signal (Narrative +
re-priming guidance + cursor).

- **Two parts:** *Mechanical* (open items, in-flight, cursor — a deterministic fold of the
  Log) and *Narrative* (what to start next, framing — authored synthesis).
- **Cursor** = the commit SHA of the last Log event the Mechanical part reflects;
  content-addressed, making drift detection O(1).
- **Eviction:** the Mechanical part lists only **open** items; a terminal event
  (sealed / superseded) drops its item at the next regeneration (it stays in the Log).
- **The fold is a CRDT-style per-subject last-writer-wins register keyed by causal order**;
  order-insensitive and idempotent, so two regenerations of the same committed Log are
  identical. **Two caveats:** (a) for **causally-concurrent** events the fold needs an
  explicit deterministic tie-break — **order by ascending git commit-SHA; lowest SHA loses**
  — and emits an `escalation.raised` so the loss is never silent; (b) LWW *discards* the
  losing concurrent write. In-unit this is avoided by **single-writer-per-artifact** (the
  lease, R7). Branch-merge concurrency is in scope (resolved by the fold); only *live
  overlapping* writers are the runtime tier's job.
- **Two regeneration paths:** (1) incremental (apply own committed deltas, advance cursor);
  (2) re-fold from cursor (walk Log cursor→head; for crash or detected drift). A non-author
  instance applies path 2 **verbatim** for the Mechanical part and may only annotate
  Narrative `[stale — review]`.
- **Periodic rebase:** an instance whose cursor lags the head by > a bound (default 500
  events) re-folds at re-prime, so an idle unit's gap never grows without limit.
- **Two-threshold staleness:** 90 days causal → item flagged `[stale-open]`; 180 days →
  an `escalation.raised` **forces triage** (re-activate / seal / supersede / explicitly
  defer). Open-item count is genuinely bounded, not merely asserted.

## R7. Crash recovery

1. Uncommitted work is only in the working tree; the last commit is a consistent
   `(artifacts + Log)` state.
2. If `cursor` lags the committed Log tail, re-fold from cursor (R6 path 2).
3. **Lease + attribution:** each in-progress artifact carries `session_id:` set at
   `session.started`. An open `session.started` with no `session.ended` is a lease; when
   the session is plainly gone, the lease is expired. Orphan files matching it are marked
   `[orphaned]` and surfaced — the new instance **resumes** if it can re-establish intent
   from the Log + artifact, else **discards** — and commits `session.ended` noting the
   abnormal end. (No-op for strict single-session Tier 1.)
4. **Content integrity:** verify each in-scope artifact's current blob SHA against the one
   its latest Log event recorded; a mismatch means post-commit corruption → `[corrupt]` +
   escalate. (A payload wrong *at commit time* needs a human/runtime oracle — R14.)

## R8. Lifecycle, override, refer-back, dormant decisions

- **Status machine.** Tier 2: `draft → working → baselined → for-review → sealed`
  (+ `superseded`, `read-only`). Tier 1: `draft → working → sealed` (+ `superseded`).
  Reaching `sealed`/`superseded` is terminal (triggers eviction).
- **Departure / After-Action Record (D-N):** when planned process diverged from reality —
  5 sections: supposed-to-happen · actually-happened (evidence) · why (root cause) ·
  lessons · doctrine action. Emits `departure.recorded`.
- **Override (Authority tier only):** only the Authority tier may override a `sealed`
  constraint or the frozen Charter (Owner Sign-off Gate), recorded as
  `decision.overrode_frozen_intent` with a **mandatory rationale** referencing the
  overridden artifact by SHA. Execution tier can never emit this.
- **Refer-back (Execution tier's third path):** on receiving a binding `sealed` directive
  that — given **material local facts the Authority tier lacked** — would be harmful to
  execute as-is, Execution acknowledges authority, **suspends**, and **refers it back** via
  `decision.referred_back` (referencing the directive SHA, carrying the local facts). The
  item re-surfaces `[referred-back]` until re-decided. It is neither disobedience nor
  override. *Liveness:* a re-affirmation with no change **binds**; a second refer-back is
  allowed **only on new facts**; a dangling referral is caught by R6 forced triage.
  **Refer-back vs dispute:** dispute = entry was *wrong when written*; refer-back = entry
  was *right but local facts since changed*.
- **Conditional / dormant decisions:** a `decision.sealed` may carry `activates_when:`
  (a date, predicate, or named trigger). Immutable from sealing, but takes effect only when
  the condition holds. The fold treats it as committed-but-dormant; each re-priming instance
  evaluates dormant conditions in scope and commits the activation when one holds. A dormant
  decision is surfaced `[dormant]` and **not evicted**. A future-date trigger is dormant
  without triage churn until near its date; a predicate trigger is subject to causal-age
  triage so an orphaned condition surfaces.

## R9. Cross-unit decisions *(Tier 2)*

- **Placement classifies:** a shared artifact lives in the **nearest common ancestor tier**,
  not in one unit; a change to it is recorded in that tier's Log. **Recognition cue:** it
  carries `shared: true` + `consumers: [unit, …]`. A contract wrongly created inside one
  unit is a misplacement, fixed by `artifact.superseded` in the origin +
  `artifact.created` in the ancestor.
- **Sibling visibility (ancestor-tail pull):** re-priming reads each ancestor's Log tail
  since this unit's cursor for it — so a `decision.sealed` in an ancestor reaches every
  descendant's next re-prime even after eviction from the ancestor snapshot. Writes go *up*
  the chain; sibling Logs are never touched.
- **Impact notification:** an ancestor decision changing a shared artifact commits
  `escalation.raised` referencing each `consumers:` unit; each consumer's next re-prime
  flags its own artifacts possibly stale. **Retroactive conflict:** when a sync brings in an
  ancestor decision that changed an artifact a unit's own committed decision depended on, the
  unit flags its dependents `[stale]` — the standard detects; reconciliation is an
  owner/runtime act.

## R10. Unit lifecycle transitions *(Tier 2)*

- **Genesis:** create `<unit>/` with empty `LOG.md` + a 5-section `HANDOFF.md`; first event
  `unit.chartered` (`causal_parent: null`); cursor = its SHA.
- **Graduation (module → unit):** historical `unit:<module>` entries stay in the parent Log;
  a `unit.sectored` marker tells future parent re-folds to stop attributing them. Committed
  to **both** parent and new-unit genesis Logs. The new unit's Mechanical part is **seeded**
  from a fold of the parent Log filtered to `unit:<module>` at the marker SHA; its genesis
  records `origin_anchor:` = that SHA. Pre-graduation binding decisions fold into the new
  unit's §2 Mission; deeper history is **linked, not copied**. Graduation forces the parent
  project to Tier 2. **Cross-repo:** the new repo must register the parent as a federation
  ancestor and shadow it so `origin_anchor` resolves locally; state whether the parent
  remains an ongoing ancestor or is a one-time seed.
- **Maturity-Tier upgrade:** on upward crossing, commit `decision.recorded`; existing
  artifacts keep their status (new Tier-2 states are available, not retroactively mandatory);
  in-progress artifacts acquire lease frontmatter; the unit **stays one unit** (partitioning
  is independent, not auto-triggered).

## R11. Federation — multi-repository *(Tier 2)*

The ancestor chain is a **doctrinal relationship, not a filesystem path** — a unit may live
in a separate repo. Each unit-repo keeps durable **local shadows** of the ancestor tiers it
depends on; re-priming reads shadows — **local only, no network call**.

```yaml
federation:
  root:
    source: <git-remote-url>
    path: <path-in-source>
    shadow: .federation/root/
    cadence: weekly
    last_sync_cursor: <git-sha>
  ancestors:
    - { source: <url>, path: <p>, shadow: .federation/<name>/, cadence: weekly, last_sync_cursor: <sha> }
  downstreams:
    - { target: <git-remote-url> }
```

A sync (manual pull, scheduled CI, any carrier) copies new committed Log entries + snapshot
updates into `shadow/` and advances `last_sync_cursor`. If `now() − last_sync > cadence`,
the next re-prime commits `escalation.federation_stale`. A Log chunk is causally stable only
once **all** downstreams have passed it.

## R12. Re-priming protocol (full)

1. Read the **Root tier**: the sealed Charter (with operating-bounds overrides merged on
   top) + the root Log tail since this unit's cursor for it. Local (Tier 1) or
   `shadow/root/` (Tier 2 federated).
2. Read the **ancestor chain of State docs**, top-down, from local copies/shadows, down to
   this unit's own.
3. For each ancestor, read its **Log tail since this unit's recorded cursor for it** (the
   ancestor-tail pull). Single-repo: cursors live in `ancestor_cursors:` frontmatter; across
   repos: the `last_sync_cursor` values in `federation.yaml`.
4. **Crash check:** if own cursor lags own Log tail, re-fold the gap.
5. **Drift check:** O(1) cursor==head; periodic deep check.

Total cost scales **O(chain depth)** — each tier is bounded (eviction + working-set bound);
depth is the multiplier. An ancestor tail is bounded by the gap since last sync (chunk-paged
via `log/INDEX.md`), not by cadence: after a long partition the catch-up is large but finite
and flagged. **All reads are local. No directory-tree scan.**

## R13. Documented residual risks (CAP-AP limits)

Not removable by paperwork — they need a runtime tier (R14) and are the accepted cost of the
eventually-consistent regime:

- **Bounded-staleness, not real-time, cross-unit visibility** — a consumer learns of an
  ancestor decision only at its next sync, within `cadence`, never instantly.
- **No prevention of a wrong-but-committed entry** — only detection + dispute; binding
  correction needs the owner.
- **No concurrent-write safety** — two overlapping live sessions on one artifact is
  undefined here by design.
- **No real-time enforcement of a frozen invariant** — between a dispute/escalation and the
  Authority seal, nothing *gates* a breaking commit; the standard detects + escalates, it
  cannot prevent.
- **No detection of semantically-wrong-but-committed content** — the blob-SHA check catches
  post-commit corruption, not a payload already wrong when committed.
- **Long-partition catch-up is gap-bounded, not cadence-bounded** — large but finite, and
  flagged.
- **Cross-branch live concurrency is the runtime tier's** — a lease can't be enforced across
  independent branches.
- **Authority-inaction on a referral** — paperwork surfaces it for triage but cannot force a
  decision.

## R14. Relationship to a runtime tier

This is the **zero-infrastructure tier** (git + markdown), targeting sequential-session work
at Tier 1+, eventually consistent by design. Strong consistency under concurrent actors —
durable event log + automatic projection + transactional claims + fencing tokens — is a
separate **runtime tier**, out of scope here. Its non-coverage is correct, not a defect.

## Provenance

Neutralized and trimmed from the Dead Light Framework Paperwork Standard (a WIP methodology);
themed vocabulary mapped via [[glossary]]. Ships `experimental` ([ADR-008](../../docs/decisions.md)).
