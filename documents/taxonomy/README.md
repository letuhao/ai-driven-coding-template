# Document taxonomy — numbered folders + the numbering rule

A proven layout for a project's `docs/` tree, harvested from a mature repo. It gives
humans and agents a **predictable reading order** instead of a flat dumping ground.

## Layout

```
docs/
  00_index/        entry point: a DOCUMENT_CATALOG.md (reading order + per-doc purpose)
  01_foundation/   project overview, organization, V1 boundaries, techstack/service matrix
  02_governance/   working model, decision rights (RACI), charter, policies, styleguides
  03_planning/     roadmap, dated specs/plans, module packs
  04_analysis/     market / external context, research
  05_qa/           acceptance, QC, audit findings
```

Each `NN_` prefix sorts the folders and fixes a reading order. `00_index/DOCUMENT_CATALOG.md`
is the single entry point that lists every doc, its purpose, and the recommended path.

## The numbering rule (anti-drift)

Observed drift in the source repo: two folders both took `04_` (`04_analysis` **and**
`04_integration`). To prevent that:

1. **One owner per number.** A given `NN_` prefix maps to exactly one folder, forever.
   Adding a category = taking the **next unused** number, never reusing or forking one.
2. **Numbers are append-only**, like the Log: renumbering existing folders breaks links
   and history. Deprecate a category in place; don't renumber around it.
3. The catalog in `00_index/` is the source of truth for which numbers exist. Adding a
   folder without registering it there is the drift; CI may lint for unregistered `NN_`
   folders.

## Metadata taxonomy (per document)

Use these values consistently in every document's front-matter:

- **Status:** `Draft` (in review) · `Active` (approved, in use) · `Approved` (baseline) ·
  `Superseded` (replaced).
- **Owner:** a canonical role name (e.g. `Product Owner`, `Architect`), or `Role A + Role B`.
- **Last Updated / Approved Date:** `YYYY-MM-DD` (or `N/A` when pending).
- **Change History:** one row appended per change.

## Dated artifacts — specs & plans

Within `03_planning/`, specs and plans are named **`YYYY-MM-DD-<topic>.md`** and come in
**pairs** (a spec and its plan share the date+topic). See [[spec]] for the spec template.

## Relationship to the Paperwork Standard

This taxonomy organizes *categories of documents*. It is **subordinate to** the
[[paperwork-standard]], which governs the *concurrency model* (Log→State, cursor,
re-priming). Use the taxonomy for structure; use the Paperwork Standard for how state
survives sessions and concurrent agents.
