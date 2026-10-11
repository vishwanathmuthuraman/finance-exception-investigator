# Finance Exception Investigator

**Status: specification and synthetic fixtures only. Application implementation has not started.** No application tests, benchmark runs, customer outcomes or savings are claimed. 

A planned local investigator of invoice, purchase-order, payment and ledger mismatches. Deterministic calculations establish amounts and exceptions; optional AI proposes explicitly labeled, record-linked explanations.

## Start here

1. Read [requirements](docs/01-product-requirements.md) and [architecture](docs/02-architecture.md).
2. Follow the numbered [build plan](docs/03-build-plan.md); update [the task tracker](docs/task-tracker.csv) as evidence is produced.
3. Study the original [fixture guide](fixtures/README.md) and [JSON contracts](schemas/README.md).
4. Freeze the [evaluation protocol](docs/04-evaluation.md) before opening the held-out set.
5. Use [definition of done](docs/05-definition-of-done.md) to decide whether the release is complete.

Also read [sources and rationale](docs/06-sources-and-design-rationale.md), [delivery and risks](docs/07-delivery-and-risk.md), and [publication checklist](docs/08-publication.md).

## Intended end state

A reproducible Python 3.12 application with local SQLite storage, three comparable reconciliation strategies, a review queue, an evidence timeline, exports, and a candid synthetic benchmark report. The planned local FastAPI interface has no external posting or payment endpoint.

Eight illustrative development bundles and their separate expected outcomes are supplied. The planned 40-development/160-held-out corpus has **not** been created. Future commands are specifications.

[Blueprint validation](docs/blueprint-validation.json) records documentation checks, not application results.

License selection is pending. No code, documentation or synthetic-data license grant is supplied. This repository is prepared for authorized public GitHub sharing as a specification and fixture blueprint; public availability is not an application release or deployment. Select and review license terms before an openly licensed reusable release.
