# Cycle Log — {{project_name}}

The Coordinator's status board. One row per cycle. STATUS ∈ `PENDING` | `DONE` |
`BLOCKED`. The coordinator marks a row `DONE` (with the commit sha) when a cycle's
sub-agent returns; it picks the next `PENDING` row whose dependencies (declared in
the cycle brief's `## Dependencies` section) are all `DONE`.

| Cycle | Title | Status | Commit | Completed |
|---|---|---|---|---|
| 1 | <first cycle title> | PENDING | | |
| 2 | <second cycle title> | PENDING | | |
| 3 | <third cycle title> | PENDING | | |

<!-- Keep this an append-only-style board: update Status/Commit/Completed in place,
     but never delete a row. It is the durable, resumable state of the run. -->
