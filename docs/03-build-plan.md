# 03 — Public milestones

The repository currently contains a specification, contracts and eight synthetic development bundles. Application implementation and benchmark execution are pending.

| Milestone | Intended result | Evidence required |
|---|---|---|
| M1 — Validated ingestion | Import the documented JSON/CSV records with strict types, provenance and idempotent storage. | Equivalent-input, invalid-import and repeat/conflict tests. |
| M2 — Deterministic reconciliation | Calculate exact balances and identify supported mismatches without guessing missing evidence. | Arithmetic, matching, duplicate, due-date and missing-record tests. |
| M3 — Reviewable evidence | Present record-linked findings, append human decisions and export faithful snapshots. | Citation, review-state, interface and escaped-export tests. |
| M4 — Optional AI explanations | Accept only bounded, validated proposals and preserve the deterministic report on failure. | Unsupported-claim, injection, timeout and budget-boundary tests. |
| M5 — Frozen comparative study | Compare exact, rules and rules-plus-AI strategies using the published protocol. | Ancestry audit, full run inventory, measured outcomes and independent review record. |
| M6 — Reproducible release | Reproduce the local workflow and publish conclusions consistent with its evidence. | Clean-install/demo record, versioned report and release review. |

Read the [requirements](01-product-requirements.md), [architecture](02-architecture.md), [evaluation protocol](04-evaluation.md) and [definition of done](05-definition-of-done.md). The eight starter bundles illustrate semantics; they are not the planned held-out corpus or proof of detection quality.

The intended application uses a local command-line interface with a review queue and evidence view. There is no application quick start today. Commands may become public usage instructions after they have been implemented and verified.

Milestones require evidence linked to a specific software revision. Keep deterministic findings distinct from model hypotheses, and distinguish a reproducible research artifact from a product that meets its proposed performance targets. No milestone authorizes financial posting or real payment activity.
