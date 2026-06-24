---
description: On-demand adversarial implementation review. Invoke when POST-REVIEW needs a deeper look, or after COMMIT when something feels off.
---

# /review-impl — adversarial implementation review

A deep adversarial review of the most recent implementation — the **separate mental mode**
that POST-REVIEW deliberately does not do. SSOT: [`ai/rules/task-workflow.md`](../../../rules/task-workflow.md).

## Scope

Whatever the user is focused on. If `$ARGUMENTS` names a task/ticket, scope to its files.
Otherwise scope to the latest commit (`git show --stat HEAD`).

## How it differs from REVIEW (code), phase 7

| Phase 7 REVIEW-CODE | `/review-impl` |
|---|---|
| "Does the code implement the design? Are patterns clean?" | "What does test coverage **miss**? What could break that nothing guards?" |
| The code as written | The *surface area the code leaves exposed* |
| 2-stage: spec compliance + quality | 1-stage: coverage gaps + drift risk + adjacent correctness |

## Mental mode (before reading any file)

List, in your head: every field on every input model (persisted, transformed, or silently
dropped?); every upstream normalization (does it make a downstream defense moot?); every
invariant the code claims (idempotence, ordering, dedup keys — could a future change break it
with no test catching it?); every boundary with callers/callees (what contract is assumed, what
if it drifts?).

## Process

1. Read the task's plan/ticket to recover acceptance criteria in original form.
2. Re-read all changed files **from disk** (`git show HEAD` or files matching the task).
3. Read callers and callees **one hop out** — boundary partners hide bugs.
4. For each input field: persisted, transformed, or dropped? Intentional?
5. For each defensive op (sanitize/validate/dedup): does an upstream step make it moot? Is
   there a test that would catch if it did?
6. For each test added: does it prove the invariant, or just exercise the happy path?

## Output

Numbered findings, **ordered by severity**: HIGH (production bug), MED (real risk, not
exploitable today), LOW (coverage/drift/docs), COSMETIC (test-quality smell). Per finding: a
one-line title + severity, a `file:line`, what's wrong (1–3 sentences), and a suggested fix or
"accept and document".

**If you find nothing, say why convincingly** — list the specific coverage checks you made and
what you verified. Do NOT output "0 issues found" without that evidence; that's the rubber-stamp
this command exists to avoid.

- HIGH → fix now, loop back to VERIFY.
- MED → human decides: fix now or deferred.
- LOW + COSMETIC → default to deferred unless batching with HIGH/MED. Never silently accept a HIGH.
