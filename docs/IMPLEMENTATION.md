# Initial implementation — 0.1.0

This is the first implemented offline slice. “Complete” below means the bounded component passed the recorded checks; it does not mean the proposed product or evaluation is complete.

## Completed component tasks

| Task | Work | Status | Delivered behavior |
|---|---|---|---|
| C01 | Import JSON and the four CSV tables | Complete for this slice | Strict metadata, headers and exact integer amounts; preserve physical CSV start-row provenance and normalized record pointers. |
| C02 | Reconcile explicit references conservatively | Complete for this slice | Supplier-scoped normalized references, exact balances, overdue dates, duplicate invoices, missing/ambiguous links and field-cited findings. |
| C03 | Package, test and document the slice | Complete for this slice | Independent Python package, packaged existing schema resources, locked dependencies, CLI error behavior, behavioral tests, CI and captured demo evidence. |
| M1 / FR-03 (store slice) | Immutable source hashes and bundle identity | Complete for this slice | Local SQLite store: SHA-256 of exact delivered bytes (CSV: ordered per-file hashes), canonical content digest that excludes physical provenance, identical redelivery is a no-op, reformatted deliveries are recorded under the same identity, and changed content under an existing bundle ID is rejected without storing it. |

Source: [core](../src/finance_exception_investigator/core.py), [contracts/utilities](../src/finance_exception_investigator/common.py), [CLI](../src/finance_exception_investigator/cli.py), [behavioral tests](../tests/test_core.py), [CLI tests](../tests/test_cli.py), [store](../src/finance_exception_investigator/store.py), [store tests](../tests/test_store.py). Runtime selection is recorded in [ADR 0001](decisions/0001-offline-core.md).

## What actually ran

Verified on Python **3.12.13**, Darwin: **27 tests passed, zero failed**, Ruff lint/format checks passed. A wheel was built, installed with locked dependency hashes into a fresh environment and exercised from outside the checkout; its schema files loaded from the installed package. The CLI input/output hashes and implementation-file hashes are in the [verification record](../reports/initial-implementation/verification.json). That file identifies exact tested inputs; expected specifications were not copied into an execution report.

```sh
uv sync --locked
uv run --locked fei reconcile fixtures/development/overdue-partial.bundle.json
uv run --locked ruff check src tests
uv run --locked ruff format --check src tests
uv run --locked pytest
```

Observed demo: The overdue partial-payment case retains its exact outstanding balance and produces a supported overdue finding. Missing or ambiguous records cannot return clear. Duplicate invoices stay in review without choosing one as payment truth.

[Captured output](../reports/initial-implementation/demo-1.json). Test use of authored expected files is restricted to development assertions; application code does not open them. These are component regressions, not independent held-out evaluation or performance measurements.

## Store slice evidence (FR-03)

Commands actually run in this revision: `uv run --locked ruff format src tests`, `uv run --locked ruff check src tests`, `uv run --locked pytest -q`, `python scripts/check_public_docs.py`. Observed: Ruff passed; **36 tests passed** (27 earlier plus 9 in `tests/test_store.py`); the documentation check completed. Python/OS of this run were not separately recorded here, and the wheel/installed-package check is left to the post steps. The earlier verification record above was not regenerated.

Limits: the store is not wired into the CLI; no run, link or finding persistence; no concurrency or crash-recovery testing; bundle versioning is only the rejection of conflicts; CSV delivery bytes are stored in a canonical JSON wrapper rather than the original files; unit tests are not performance or production evidence.

## Relationship to the full plan

M1 and M2 have initial importer/reconciler evidence; M3 has field citations only. Storage idempotency, review workflow and the comparative study remain pending.

The [build plan](03-build-plan.md), [requirements](01-product-requirements.md), [evaluation](04-evaluation.md) and [definition of done](05-definition-of-done.md) remain the release criteria. Planned acceptance registers describe the wider system; partial progress does not replace their full conditions. Documentation checks validate authored artifacts separately from application CI.

## Explicit limits

Only the supplied USD contract and normalized explicit references are supported. Missing-reference fallback matching, durable source snapshots/idempotent imports, human dispositions, exports, UI, optional AI and the held-out comparison are unimplemented. The eight starter bundles are development fixtures.

All example records and observations are synthetic. No network integration or external business action exists in this slice. Financial and property results support human review. No customer impact, trained-model quality, production readiness or independent endorsement is established.

## Next implementation steps

1. Expose the store through the CLI, persist runs/findings, and add physical multiline CSV provenance tests (source hashes and repeat/conflict handling exist; see above).
2. Implement the specified conservative fallback matcher with ambiguity tests, then append reviewer decisions without changing source findings.
3. Add a faithful escaped export and complete the independent evaluation projection before expanding the corpus.

For each step, add meaningful failure-case tests, capture actual output, preserve evidence/time/money boundaries, and update this record with the revision and unresolved limitations. Do not mark the full release complete from component test counts.
