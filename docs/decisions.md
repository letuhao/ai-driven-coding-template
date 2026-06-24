# Design decisions

Lightweight ADRs capturing *why* the collection is shaped this way, so the
rationale isn't lost. Each is a decision we can revisit, not dogma.

---

## ADR-001 — Four orthogonal catalogs + a recipe composer

**Decision.** Model the collection as four independent, flat catalogs
(`templates`, `architectures`, `workflows`, `ai`) plus a `recipes` layer that
references one piece from each.

**Why.** Nesting the dimensions (`python/microservices/tdd/...`) explodes
combinatorially and makes every catalog touch the others. Flat catalogs grow
independently; recipes provide combination without pre-building the cross-product.

---

## ADR-002 — Templates are verified by CI, not trusted

**Decision.** A scheduled CI job instantiates every template/recipe and runs
build + tests. Each entry records a "last verified" date.

**Why.** Template rot (stale deps, dead CI syntax, deprecated APIs) is the #1
long-term failure mode. A template that doesn't build is worse than none.

---

## ADR-003 — Two placeholder conventions, split by actor (RESOLVED)

**Decision.** Two conventions, distinguished by *who fills them and when*:

- **`{{ variable }}`** (Jinja/Mustache — the industry de facto for scaffolding) —
  filled by the **assembler at scaffold time** from `recipe.yaml::variables`
  (e.g. `{{project_name}}`, `{{date}}`). This is the only thing the assembler expands.
- **`<descriptive blank>`** (angle-bracket — the convention **DLF already uses** in its
  living doc templates) — left for a **human or agent to fill when authoring a document
  instance** later (e.g. `<root cause>`, `<one-line decision>`).

**Why two, not one.** They are not redundant: they are filled by *different actors at
different times* (machine at init vs. author later). Forcing one syntax breaks one of
the two — and `<...>` specifically is unsafe for machine substitution because angle
brackets collide with real content (generics `Vec<T>`, HTML, comparison operators), so
it must stay a human-fill marker only. `{{ }}` is the chosen de facto for machine fill.

**Consequence.** The doc templates I scaffolded earlier (`documents/spec/TEMPLATE.md`,
`documents/adr/TEMPLATE.md`) currently use `{{ }}` for author-time blanks like
`{{title}}`/`{{owner}}` — those must be re-aligned to `<title>`/`<owner>` during
extraction, reserving `{{ }}` for fields the assembler actually fills (e.g. project name).

---

## ADR-004 — Scope: one-shot scaffolder, not a live updater

**Decision.** The collection scaffolds at project `init` and then steps out of
the way. It does **not** (yet) support pulling later updates into existing projects.

**Why.** "Day 2" update-merge is an order of magnitude more complex. Stating the
scope prevents accidental drift toward it. Revisit only with explicit demand.

---

## ADR-005 — Tool-agnostic AI substance

**Decision.** AI substance (`ai/rules`, `ai/prompts`) is tool-agnostic; only
`ai/agents/<tool>` may assume a specific AI tool. Prefer generating per-tool
files from shared fragments.

**Why.** Avoids coupling the whole collection to one vendor, and keeps rule
snippets small for the per-turn AI context budget.

---

## ADR-006 — Safe-by-default and clear licensing

**Decision.** Every template ships secrets-aware `.gitignore`, `.env.example`
(never `.env`), pinned deps, no hardcoded creds. Document that **generated code
belongs to the user, unencumbered**, separate from the collection's own LICENSE.

**Why.** Copied templates become everyone's baseline — a bad default propagates.
Ambiguous licensing kills adoption of a scaffolder.

---

## ADR-007 — Maturity-Tier gate: hybrid (trigger for 0→1, scale for 1→2)

**Decision.** Three neutral tiers (M0/M1/M2 kept as DLF aliases). The gate is **hybrid**:
the lower boundary is trigger-based; the upper boundary is scale-based.

- **Tier 0 — Prototype** *(M0)*: `README.md` suffices; no Log/State. The default until a
  Tier-1 trigger fires.
- **Tier 0 → Tier 1 — by trigger.** Enter **Tier 1 — Continuity** if **any**:
  1. work spans **>1 session** and earlier decisions must survive (the *why* is not
     recoverable from code/git alone);
  2. **≥2 actors** (human or agent) touch it over time;
  3. source **+ its rationale no longer fit comfortably in one agent context** for a
     fresh re-read each session.
  *(Soft proxy when the above are ambiguous: ~10 KLOC, language-adjusted.)*
  Tier 1 machinery: sealed Charter + State/Log split (one `HANDOFF` + one `LOG`),
  self-sufficient log events, causal cursor, crash recovery. **Single unit.**
- **Tier 1 → Tier 2 — by scale.** Enter **Tier 2 — Federation** if **any**:
  1. **>50 KLOC** (`cloc`/`scc`, language-adjusted, soft/owner-calibratable);
  2. **≥2 governance units** (independently deployed services / separate team or on-call /
     cross-unit API-or-schema contracts that must be negotiated) — size-independent;
  3. **concurrent overlapping sessions or branches** on one unit.
  Tier 2 machinery: Tier 1 + partitioning, cross-unit decisions, federation, full lifecycle.

**Carried from DLF.** Adopt a higher tier, never lower. **Mixed-tier units:** each unit
gates on its own signals; a Tier-0 unit inside a Tier-2 repo keeps a minimal
`HANDOFF`+`LOG` stub so it joins the ancestor chain.

**Why hybrid.** The standard exists to solve **session-continuity** and **concurrency**,
not raw size — so the 0→1 boundary (does this project even need durable state?) is
anchored on those observable triggers, not on a KLOC line DLF itself calls "soft" and
"not a citable cutoff." Scale (LOC + unit count) only governs the 1→2 split, where it is
the genuinely relevant signal (when does one unit become a federation?).

---

## ADR-010 — Contracts: opt-in, multi-preset, "contract-first" is the principle

**Decision.** Model `workflows/contracts/` as an **opt-in, multi-preset** dimension. The
generalizable thing is the **principle**, not the tool: a versioned interface schema +
a linter + a home, as the single source of truth between producer and consumer, frozen
before code. OpenAPI + Spectral is the **REST preset** (shipped, runnable); Protobuf+buf
(gRPC), AsyncAPI (events), and GraphQL SDL are **sibling presets** (stubbed, added on demand).

A recipe includes a contracts preset **only when the project exposes a cross-boundary API**,
and it is most warranted at **Tier 2** (≥2 governance units with negotiated contracts —
ADR-007). CLI/library/frontend-only/single-unit recipes omit it.

**Why.** OpenAPI+Spectral is **not universal** — it is REST-specific; gRPC/events/GraphQL/CLI
need other (or no) contracts. Forcing it on every project would be wrong. But the *contract-first*
principle generalizes, and it is the same idea as `/warp`'s frozen interface and the paperwork
standard's shared-artifact-in-nearest-common-ancestor — the cross-boundary agreement surface
that makes concurrent multi-module work safe. So: ship the common preset, name the principle,
gate inclusion on actual need.

---

## ADR-009 — Workflow gate is a generic engine + per-project config

**Decision.** Ship one **project-agnostic** `workflow-gate` engine plus a single
per-project `workflow.config.json` (or `.yaml` when PyYAML is present). The engine code is
byte-identical across projects; everything project-specific lives in config:

- `module_globs` — which path prefixes count as independently-deployed modules (replaces the
  source's hardcoded `services/<name>/` cross-service detection);
- `paths.audit` — where the audit log lives;
- `verify.smoke_tokens` / `verify.cross_module_smoke` — the live-smoke soft-gate policy;
- `integrations.lessons_store_cmd` / `guardrails_cmd` — **optional, pluggable** commands
  (replace the source's hardcoded ContextHub/mcp-query bridge); `null` ⇒ no-op.

The engine is a **single zero-dependency Python script** (no assumption about the project's
own language), config is **JSON-canonical** (stdlib, runs anywhere; YAML accepted if PyYAML
is installed), and it works **zero-config** with sensible defaults.

**Why.** "Any project can use it" requires that adopting the toolkit means *writing a config
file, not editing engine code*. Externalizing module boundaries + integrations behind a
config is what makes the same gate run on a Go monorepo, a TS app, or a Python service
unchanged. JSON + stdlib keeps the zero-dependency, runs-anywhere guarantee.

---

## ADR-008 — DLF Paperwork Standard ships as `experimental`

**Decision.** The harvested DLF Paperwork Standard ships with maturity
**`experimental`**, not `stable`. Adoption guides must say so plainly and frame it as
opt-in. It graduates to `stable` only after real adoption evidence (e.g. it is in use in
lore-weave / free-context-hub, or another project, through at least one full lifecycle).

**Why.** DLF is **WIP and not yet adopted anywhere** (see the optimization plan). It is
the chosen spine for its *design* (conflict-free concurrent multi-agent/multi-module work),
not a track record. Shipping it `stable` would overstate its maturity and mislead adopters;
`experimental` is the honest tag and matches the safe-default ethos of ADR-006. The
maturity vocabulary (`experimental` | `stable`) is the same one used for recipes
(see `recipes/README.md`), so the signal is consistent across the collection.
