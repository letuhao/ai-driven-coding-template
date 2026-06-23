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

## Start simple

If unsure, take the **minimal path**: a single-language `monolith` recipe with
trunk-based git and one AI agent config. You can refactor toward more structure
later — over-architecting day one is the more common mistake.
