---
title: LOG — {{project_name}}
status: working
doc_kind: log
---

<!--
  LOG.md — the APPEND-ONLY history (the "Log document" in the Paperwork Standard).
  Each line is one self-sufficient event. This is the source of truth; HANDOFF.md
  (the State snapshot) is DERIVED from it.

  Rules:
    - Place at the unit root as LOG.md. APPEND only. NEVER edit a past line —
      a correction is a NEW line (kind: dispute, citing the wrong line's SHA).
      That append-only discipline is what makes concurrent work conflict-free.
    - One line per event:
        <YYYY-MM-DD> · <session/agent-id> · <kind> · <one self-sufficient sentence>
                                                     [ (reason: ...) ]   [<tags>]
    - Six event kinds:
        decision   = a choice was made — with a (reason: ...). The most important kind.
        created    = a new artifact / sub-area appeared.
        changed    = an existing artifact's state moved — same identity, new state.
        note       = FYI context — no choice, no state change. Use sparingly.
        superseded = a different artifact replaces this one — identity changes.
        dispute    = an earlier entry was wrong when written (cite its SHA).
    - Four lifecycle tags (describe state):
        [candidate]  = agent-produced, not yet human-confirmed.
        [sealed]     = settled decision; suspend-and-refer-back before changing.
        [disputed]   = this entry was wrong when written (set by a later dispute).
        [dormant]    = sealed-but-not-yet-in-effect (has activates_when: ...).
    - Full rules: ../standards/paperwork-standard.md  ·  terms: ../glossary.md
-->

# LOG — {{project_name}}

- <YYYY-MM-DD> · session-1 · note · project bootstrapped; HANDOFF + LOG created
