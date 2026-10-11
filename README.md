# Finance Exception Investigator

![Finance Exception Investigator — Follow the discrepancy. Preserve the evidence.](docs/assets/overview.svg)

[![Documentation integrity](https://github.com/vishwanathmuthuraman/finance-exception-investigator/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/vishwanathmuthuraman/finance-exception-investigator/actions/workflows/docs.yml)

**Can a reviewer trace a financial mismatch from its amount to the records that explain it?**

Use deterministic reconciliation to establish the exception, then attach record-linked explanations and a reviewable evidence trail.

**Stage: research specification.** This repository contains design work and synthetic examples. Application implementation and performance evaluation are pending; there is no working product or measured result yet.

[Explore the example](#a-concrete-example) · [Architecture](docs/02-architecture.md) · [Evaluation protocol](docs/04-evaluation.md) · [Engineering standards](ENGINEERING.md)

## A concrete example

An invoice, purchase order, payment and ledger entry disagree. A plausible explanation is insufficient: the reviewer needs the exact amounts, record relationships and unresolved gaps.

[Eight synthetic bundles and expected behavior](fixtures/README.md) · [Data contracts](schemas/README.md)

The expected outcomes describe the intended behavior. They are not output from an executed application.

## How the proposed system works

```mermaid
flowchart LR
    A[Orders and invoices] --> C[Deterministic checks]
    B[Payments and ledger] --> C
    C --> D[Exception and amount]
    D --> E[Record-linked explanation]
    E --> F[Human review queue]
```

Separate the correctness of arithmetic and matching from the usefulness of an optional generated explanation. An explanation must never silently invent a missing record.

## What you can inspect today

| Artifact | What it establishes |
|---|---|
| Requirements and architecture | The proposed problem, boundaries and consequential design decisions. |
| Original synthetic scenarios and schemas | Concrete inputs and explicit expected behavior. |
| Evaluation protocol and release criteria | How implementation and claims should be assessed. |
| Source rationale | Which public evidence motivated the design and which conclusions remain hypotheses. |
| Documentation checks | Whether the supplied JSON, relative links and original SVG assets are structurally valid. |

Eight original synthetic fixture bundles with separate expected outcomes, JSON schemas, requirements and a proposed comparison protocol.

## Technical choices

Python + SQL/SQLite for exact reconciliation and reproducibility. Monetary values use specified decimal/minor-unit rules. Optional AI output remains a labeled proposal.

Python, Go, Rust, SQL, TypeScript and Rails each have appropriate uses. This project follows [documented selection rules](ENGINEERING.md): add a runtime or framework only when requirements, profiling and maintainability justify it.

## What the evaluation must show

Compare three reconciliation strategies. Report detection quality, amount correctness, evidence support, unresolved cases and reviewer burden. The proposed development/held-out corpus is not yet implemented.

The [evaluation protocol](docs/04-evaluation.md) defines the comparison and limitations. No benchmark score, customer impact, novelty claim or independent endorsement is asserted.

## Read the design

| Start with | Then inspect |
|---|---|
| [Problem and requirements](docs/01-product-requirements.md) | [Architecture and boundaries](docs/02-architecture.md) |
| [Public implementation milestones](docs/03-build-plan.md) | [Evaluation protocol](docs/04-evaluation.md) |
| [Definition of done](docs/05-definition-of-done.md) | [Sources and design rationale](docs/06-sources-and-design-rationale.md) |
| [Technical limitations](docs/07-delivery-and-risk.md) | [Publication boundaries](docs/08-publication.md) |

## Check this documentation

From a clone of this repository with Python 3.12 or later:

```sh
python scripts/check_public_docs.py
```

This checks documentation only. Application installation and demo commands will be added when implemented and verified. The repository's **Documentation integrity** workflow runs the same check on pushes and pull requests.

## Research roadmap

- [x] Define the problem, contracts and illustrative synthetic scenarios.
- [x] Document evaluation methods and consequential failure cases.
- [ ] Implement and test a reproducible offline baseline.
- [ ] Complete held-out comparisons and publish actual results, including failures.
- [ ] Seek independent reproduction and review.

## Scope and contribution

See [contribution guidance](CONTRIBUTING.md) for useful review questions. Reports should include a minimal synthetic example and the relevant requirement or evaluation rule. Never submit customer records, credentials or private operational information.

This is a curated research repository. Internal delivery schedules and commercial planning are maintained separately. Public technical methods are deliberately inspectable; public availability does not imply production readiness.

Maintained by [Vishwanath Muthuraman](https://github.com/vishwanathmuthuraman). Source material is cited; citations do not imply endorsement. License selection is pending, and no code, documentation or data license grant is supplied.
