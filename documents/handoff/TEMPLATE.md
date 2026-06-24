---
title: HANDOFF — {{project_name}}
status: working          # draft | working | sealed
doc_kind: state
cursor: '<SHA of the last LOG.md commit folded into this snapshot>'
# ancestor_cursors:      # Tier 2 only — one cursor per ancestor unit this one reads
#   platform: '<SHA>'
#   parent-service: '<SHA>'
---

<!--
  HANDOFF.md — the CURRENT-STATE snapshot (the "State document" in the Paperwork Standard).
  A fresh session reads THIS first, then the LOG.md lines committed AFTER `cursor:`,
  and is immediately current.

  Rules:
    - Place at the unit root as HANDOFF.md. REWRITE freely — it always describes "now".
      History does NOT live here; it lives in the append-only LOG.md ([[log-template]]).
    - cursor: set to `git log -1 --format=%H -- LOG.md` whenever you rewrite this file.
    - ancestor_cursors: Tier 2 only — one entry per ancestor unit this one reads.
    - Full rules: ../standards/paperwork-standard.md  ·  terms: ../glossary.md
    - Placeholders: {{project_name}} is filled by the scaffolder; <...> are yours to fill.
-->

# HANDOFF — {{project_name}}

<!-- STARTER LAYOUT (flat) — good until HANDOFF passes ~100 lines, then split into
     a derived "Mechanical" section + an authored "Narrative" section. -->

## Now
<!-- what is true today, in a few lines -->
- <...>

## In flight
<!-- work mid-task + which session/agent owns it, so another session can resume -->
- <...>

## Decided
<!-- settled decisions — do NOT re-litigate. One line of WHY each, so they stick. -->
- <decision> — <one-line why>

## Start here next
<!-- the single next concrete action a session should take -->
- <...>
