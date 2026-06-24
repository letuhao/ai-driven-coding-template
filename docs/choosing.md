# Choosing the right pieces

A collection's real value is helping you **decide**. This is the decision matrix.
(Can be generated from recipe/template metadata once tags are in place.)

## Architecture

| If your situation is... | Consider |
|---|---|
| Small app, prototype, solo / fast iteration | `monolith` |
| Growing app, want boundaries without ops overhead | `modular-monolith` |
| Logic must outlive its delivery; swappable infra; testability | `hexagonal` |
| Independent scaling/deploy, multiple teams, accept ops cost | `microservices` |
| Complex domain, ubiquitous language matters | `ddd` (often + hexagonal) |

## Development process

| If your team... | Consider |
|---|---|
| Ships continuously, small batches, strong CI | `git/trunk-based` |
| Needs release branches / scheduled releases | `git/gitflow` |
| Wants automated changelogs & versioning | `release/conventional-commits` |
| Wants tests-first discipline | `testing/tdd` |

## Maturity Tier — do you even need the paperwork standard?

Gate the paperwork/governance standard by tier (see
[`decisions.md` ADR-007](decisions.md)). Hybrid gate: trigger for 0→1, scale for 1→2.

| Tier | Enter when | You get |
|---|---|---|
| **0 — Prototype** | single session, single actor, throwaway; rationale recoverable from code/git | `README.md` only — no Log/State |
| **1 — Continuity** | **any:** work spans >1 session & decisions must survive · ≥2 actors over time · source+rationale no longer fit one fresh context *(soft proxy ~10 KLOC)* | sealed Charter + one `HANDOFF` + one `LOG`, self-sufficient events, crash recovery — single unit |
| **2 — Federation** | **any:** >50 KLOC · ≥2 governance units (independent deploy / separate on-call / negotiated contracts) · concurrent overlapping sessions or branches | Tier 1 + partitioning, cross-unit decisions, federation, full lifecycle |

Adopt higher, never lower. In a multi-unit (Tier 2) repo, a small unit still keeps a
minimal `HANDOFF`+`LOG` stub.

## Start simple

If unsure, take the **minimal path**: a single-language `monolith` recipe with
trunk-based git and one AI agent config. You can refactor toward more structure
later — over-architecting day one is the more common mistake.
