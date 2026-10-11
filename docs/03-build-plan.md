# 03 — Build plan

Every task below is **not started**. Draft specifications, schemas and seed data already exist; implementation, tests and evaluation do not. Paths in the tasks are proposed outputs unless present in this documentation package.

Work from this standalone repository. No sibling project, shared package, employer system or private service is required. Use [the CSV tracker](task-tracker.csv) as the editable task record; its IDs match this plan and its command_group column maps each task to the command contracts below.

## Prerequisites and command conventions

A working uv installation is a prerequisite. Follow the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/) for the local operating system, then verify uv --version. This blueprint does not install tools. Python 3.12 must be available; uv can manage its installation according to the [official Python guide](https://docs.astral.sh/uv/guides/install-python/).

All commands below are **future commands**, not commands run while preparing this blueprint. Execute them from repository root after their producing task exists. Preserve existing documents.

    uv init --package --python 3.12 --name finance-exception-investigator
    uv add pydantic fastapi "uvicorn[standard]" jinja2
    uv add --dev pytest ruff jsonschema httpx
    uv sync
    uv run python --version

T03 must wire a fei console entry point to finance_exception_investigator.cli:main. Implement CLI parsing with the standard library or explicitly add a selected library. FastAPI and UI dependencies can be deferred until T23. No provider SDK is selected; add one only after T18 research.

For task command groups beginning test_, use the named test from [traceability](05-definition-of-done.md) or that task's planned output:

    uv run pytest tests/unit/test_calculations.py -q
    uv run pytest tests/integration/test_ingest.py -q
    uv run ruff check .
    uv run pytest -q

Only meaningful implemented tests provide verification.

## Dependency-ordered task instructions

### 1. T01 — Review scope and conventions

Deps: none. Effort: 2 h. Inputs: docs/01-product-requirements.md;fixtures/README.md.

Record USD convention, exclusions, user workflow and reviewer role. Files: docs/decision-log.md.

Verify: Every accounting assumption has an explicit decision and unresolved questions are logged.

### 2. T02 — Approve data contracts

Deps: T01. Effort: 3 h. Inputs: schemas/;fixtures/.

Review required fields and cross-record checks; add planned schema tests. Files: schemas/;tests/unit/test_contracts.py.

Verify: Each input/truth validates; altered currency, decimals and malformed dates fail.

### 3. T03 — Create Python package

Deps: T01. Effort: 2 h. Inputs: docs/02-architecture.md.

Install prerequisites, initialize package and declare only needed dependencies. Files: pyproject.toml;uv.lock;src/finance_exception_investigator/.

Verify: Python 3.12 environment resolves; imports work; docs preserved.

### 4. T04 — Create test and quality harness

Deps: T02;T03. Effort: 2 h. Inputs: approved contracts.

Set unit/integration/evaluation directories and lint configuration. Files: tests/;pyproject.toml.

Verify: One meaningful contract check runs and malformed input test fails as expected.

### 5. T05 — Implement CSV and JSON reader

Deps: T04. Effort: 5 h. Inputs: fixtures/csv/clean-settled/;fixtures/development/.

Parse strict columns, integers and dates; produce row-specific errors. Files: src/finance_exception_investigator/ingest.py;tests/integration/test_ingest.py.

Verify: CSV and JSON normalize to equivalent business records; invalid import is atomic.

### 6. T06 — Implement normalization and provenance

Deps: T05. Effort: 4 h. Inputs: source locator contract.

Preserve originals; build evaluator-only opaque-ID projection and reverse map; normalize keys. Files: src/finance_exception_investigator/normalization.py;evaluation/project.py;tests/unit/test_normalization.py.

Verify: Leading zeros survive; all strategies receive only allowlisted business fields and opaque IDs.

### 7. T07 — Implement transactional store

Deps: T06. Effort: 5 h. Inputs: bundle/version design.

Create tables, foreign keys, canonical digests and conflict behavior. Files: src/finance_exception_investigator/store.py;tests/integration/test_idempotency.py.

Verify: Same import is a no-op; changed content under same ID conflicts; rollback leaves no partial bundle.

### 8. T08 — Implement deterministic arithmetic

Deps: T04. Effort: 4 h. Inputs: integer amount contract.

Add bounded sums, differences and outstanding balances with input citations. Files: src/finance_exception_investigator/calculations.py;tests/unit/test_calculations.py.

Verify: Exact cents and overflow tests pass; no float arithmetic.

### 9. T09 — Implement exact baseline

Deps: T07;T08. Effort: 4 h. Inputs: raw references and supplier keys.

Match literal references; expose unlinked and ambiguous records. Files: src/finance_exception_investigator/matching.py;tests/unit/test_matching.py.

Verify: No cross-supplier link; missing reference does not cause invented match.

### 10. T10 — Implement rules matching

Deps: T09. Effort: 6 h. Inputs: normalization and candidate rules.

Add normalized references and bounded unique-candidate fallback. Files: src/finance_exception_investigator/matching.py;tests/unit/test_matching.py.

Verify: Multiple equal candidates abstain; partial payments link by reference.

### 11. T11 — Implement duplicate detection

Deps: T10. Effort: 4 h. Inputs: duplicate-invoice fixture.

Detect same-supplier invoice-number duplicates and block liability aggregation. Files: src/finance_exception_investigator/rules.py;tests/unit/test_duplicates.py.

Verify: Duplicate case flags both records; same number at different supplier is not conflated.

### 12. T12 — Implement amount discrepancy checks

Deps: T10;T08. Effort: 4 h. Inputs: amount-mismatch fixture.

Compare order/invoice and invoice/payment ledger amounts with versioned tolerance. Files: src/finance_exception_investigator/rules.py;tests/unit/test_amounts.py.

Verify: Every difference has correct sign/value and input citations; boundary tests pass.

### 13. T13 — Implement partial payment semantics

Deps: T10;T08. Effort: 4 h. Inputs: clean-partial;overdue-partial;clean-two-payments.

Aggregate unique payments and evaluate due date, outstanding and overpayment. Files: src/finance_exception_investigator/rules.py;tests/unit/test_partial_payments.py.

Verify: Clean and overdue variants differ correctly; exact due date is not overdue.

### 14. T14 — Implement missing-evidence checks

Deps: T10. Effort: 4 h. Inputs: missing-ledger;missing-invoice.

Check required order/invoice/ledger support; distinguish unpaid from absent invoice. Files: src/finance_exception_investigator/rules.py;tests/unit/test_missing_records.py.

Verify: Specific evidence request points to an observed reference; no synthetic missing source.

### 15. T15 — Assemble deterministic cases

Deps: T11;T12;T13;T14. Effort: 4 h. Inputs: rule findings and calculations.

Apply outcome precedence and retain all findings in stable order. Files: src/finance_exception_investigator/cases.py;tests/unit/test_cases.py.

Verify: Any unresolved missing source blocks clearance; clean open remains clear.

### 16. T16 — Implement citation resolver

Deps: T15. Effort: 4 h. Inputs: record pointers and calculation inputs.

Resolve evidence against immutable source version and validate calculation links. Files: src/finance_exception_investigator/citations.py;tests/unit/test_citations.py.

Verify: Broken, wrong-bundle or nonexistent field references are rejected.

### 17. T17 — Serialize versioned reports

Deps: T16. Effort: 3 h. Inputs: schemas/investigation-report.schema.json.

Create stable report identity and schema-valid deterministic serialization. Files: src/finance_exception_investigator/contracts.py;tests/unit/test_reports.py.

Verify: Repeated deterministic run produces same report content and identity.

### 18. T18 — Implement optional model adapter

Deps: T17. Effort: 6 h. Inputs: provider official docs;dummy config.

Select provider; record version, timeout and usage; implement disabled/mock/live modes. Files: src/finance_exception_investigator/ai.py;tests/integration/test_ai_boundary.py.

Verify: Disabled mode makes no request; mock timeout preserves rules report.

### 19. T19 — Write bounded investigation prompt

Deps: T18. Effort: 4 h. Inputs: permitted records and calculation schema.

Build model context only from sanitized inputs and computed findings; require grounded hypotheses. Files: prompts/investigation-v1.txt;tests/integration/test_prompt_boundary.py.

Verify: No readable source names, ancestry, splits, labels, truth or secrets enter serialized model requests.

### 20. T20 — Validate AI claims and fallback

Deps: T19;T16. Effort: 5 h. Inputs: claim schema;adversarial mock outputs.

Reject malformed or ungrounded facts; retain deterministic outcome and reason. Files: src/finance_exception_investigator/ai.py;tests/integration/test_ai_boundary.py.

Verify: AI cannot clear a flagged case or replace any authoritative amount.

### 21. T21 — Implement human review events

Deps: T17. Effort: 4 h. Inputs: schemas/review-event.schema.json.

Append version-bound decisions with reason and idempotency key. Files: src/finance_exception_investigator/review.py;tests/integration/test_reviews.py.

Verify: Repeated request is safe; dismissal without evidence and stale versions fail.

### 22. T22 — Implement command-line workflow

Deps: T17;T20;T21. Effort: 4 h. Inputs: proposed commands below.

Expose validate, ingest, investigate and review subcommands; wire export in T26. Files: src/finance_exception_investigator/cli.py;tests/integration/test_cli.py.

Verify: Example import and rules investigation execute from repository root.

### 23. T23 — Implement local HTTP adapter

Deps: T22. Effort: 4 h. Inputs: proposed route contract.

Add local queue/case/import/review/export routes and input limits. Files: src/finance_exception_investigator/api.py;tests/integration/test_api.py.

Verify: Loopback app returns expected responses; invalid cases return useful errors.

### 24. T24 — Build case queue

Deps: T23. Effort: 5 h. Inputs: FR-12 screen specification.

Implement counts, filters, search and empty/loading/error states. Files: src/finance_exception_investigator/templates/queue.html;static/app.css.

Verify: Keyboard navigation works and filter counts agree with stored cases.

### 25. T25 — Build case/evidence view

Deps: T24;T21. Effort: 6 h. Inputs: FR-09;FR-11;FR-12.

Show calculations, timeline, evidence drawer, hypotheses and review controls. Files: src/finance_exception_investigator/templates/case.html.

Verify: Every visible claim opens evidence; narrow screen remains usable.

### 26. T26 — Implement portable exports

Deps: T25. Effort: 4 h. Inputs: case report and review events.

Export versioned JSON and printable escaped HTML snapshots. Files: src/finance_exception_investigator/export.py;tests/integration/test_exports.py.

Verify: Exports reproduce reviewed facts and do not execute source text as HTML.

### 27. T27 — Complete development corpus

Deps: T15. Effort: 6 h. Inputs: 8 starter bundles;corpus protocol.

Create 32 bundles to reach 20 clean and 20 exception; record highest shared ancestry. Files: evaluation/generate.py;evaluation/manifests/development.json.

Verify: 40 unique bundles; CSV is not extra; eight seeds count as one independent lineage; oracle reviewed.

### 28. T28 — Create and seal held-out corpus

Deps: T27. Effort: 8 h. Inputs: independent templates and oracle review.

Create 160 bundles: 80 clean and 20 exceptions per category; review ancestry independence. Files: evaluation/manifests/heldout.json;private/heldout/.

Verify: No shared lineage crosses splits; evaluator-only mappings/truth and projected hashes sealed.

### 29. T29 — Implement evaluator and scorer

Deps: T22;T27. Effort: 8 h. Inputs: metric definitions and oracle contracts.

Run strategies, score counts/citations and retain all failed runs. Files: evaluation/run.py;evaluation/score.py;tests/evaluation/test_protocol.py.

Verify: Hand-scored miniature cases agree with computed denominators and scores.

### 30. T30 — Test failures and data boundaries

Deps: T20;T23;T26. Effort: 6 h. Inputs: fault/adversarial inputs.

Test input faults, prompt injection, budget, renamed sources, opaque-ID permutations and label canaries. Files: tests/integration/test_failures.py.

Verify: Source/label changes cannot alter remapped business outcomes; payload inspection proves no metadata leakage.

### 31. T31 — Freeze protocol and versions

Deps: T28;T29;T30. Effort: 3 h. Inputs: development results and complete configuration.

Freeze schemas, projection, ancestry, rules, prompt, model, tolerance, seeds and audit sample. Files: evaluation/manifests/freeze.json;docs/decision-log.md.

Verify: Freeze precedes evaluation; independent lineage count reviewed; no unresolved semantic ambiguity.

### 32. T32 — Run development spend pilot

Deps: T31. Effort: 3 h. Inputs: 10 development bundles;provider pricing.

Measure real token/cost use and set bounded run budget; do not inspect held-out. Files: reports/pilot.md.

Verify: Budget includes retries and cumulative cap; disabled mode remains default.

### 33. T33 — Execute frozen comparison

Deps: T32. Effort: 6 h. Inputs: frozen manifest and held-out inputs.

Run 320 deterministic and 480 AI trials with complete status records. Files: outputs/evaluation/;reports/run-accounting.json.

Verify: 800 run slots accounted for; missing/failed runs are not silently omitted.

### 34. T34 — Audit explanations independently

Deps: T33. Effort: 6 h. Inputs: prespecified 40-bundle sample and flagged failures.

Two reviewers score support and adjudicate disagreements using the frozen rubric. Files: evaluation/audit.py;reports/audit.csv.

Verify: Audit coverage, agreement, disputes and unresolved limits are documented.

### 35. T35 — Analyze and report results

Deps: T34. Effort: 5 h. Inputs: all run records and audit labels.

Report paired effects, highest-lineage clustered uncertainty, category results, cost and failures. Files: reports/benchmark.md;reports/metrics.json.

Verify: All metrics have denominators; actual independent clusters reported; negative findings retained.

### 36. T36 — Verify fresh install and demo

Deps: T26;T35. Effort: 4 h. Inputs: lockfile and six-minute script.

Use a clean environment to reproduce setup, fixtures, local UI and exports. Files: reports/reproduction.md;README.md.

Verify: Setup and demo evidence recorded with actual environment and revision.

### 37. T37 — Collect workflow feedback

Deps: T36. Effort: 4 h. Inputs: demo and review rubric.

Invite authorized practitioner review; distinguish simulation from observed use. Files: reports/workflow-feedback.md.

Verify: Specific usability findings and revisions recorded; absent feedback disclosed.

### 38. T38 — Review release and license

Deps: T35;T36;T37. Effort: 4 h. Inputs: publication and done checklists.

Choose license, inspect content, reconcile claims and record remaining acceptance gaps. Files: reports/release-checklist.md;LICENSE if selected.

Verify: Artifact status and performance status are separate; no remote created without authorization.

## Future workflow commands and expected outputs

These names and flags are implementation contracts to create in T22/T29, not existing interfaces.

    uv run fei validate --input fixtures/development
    uv run fei ingest --input fixtures/csv/clean-settled --database outputs/demo.sqlite
    uv run fei investigate --bundle clean-settled --strategy rules --database outputs/demo.sqlite
    uv run fei investigate --bundle clean-settled --strategy rules_ai --trial-id demo-1 --database outputs/demo.sqlite
    uv run fei export --bundle clean-settled --format html --database outputs/demo.sqlite --output outputs/clean-settled.html

Expected: eight schema-valid development inputs; one stored clean-settled bundle; repeat import unchanged; a clear deterministic outcome; optional AI status disabled unless locally enabled; an export reproducing the report. CLI exits: 0 successful processing, 2 invalid input, 3 processing failure. A detected exception is a successful processing result, not a crash.

    uv run uvicorn finance_exception_investigator.api:app --host 127.0.0.1 --port 8000

Expected after T23–T25: local queue and evidence pages. The implementation should document the selected database configuration; the API must use the same report contract as CLI.

    uv run python -m evaluation.generate --partition development --count 40
    uv run python -m evaluation.split --validate --manifest evaluation/manifests/freeze.json
    uv run python -m evaluation.run --manifest evaluation/manifests/development.json --pilot-count 10
    uv run python -m evaluation.run --manifest evaluation/manifests/freeze.json --strategies exact rules rules_ai --ai-trials 3
    uv run python -m evaluation.score --runs outputs/evaluation --output reports/metrics.json
    uv run python -m evaluation.audit --prepare --runs outputs/evaluation

The generator must preserve the eight seed cases and reach 40 total rather than adding 40. Held-out construction is a separate reviewer-controlled operation; do not expose truth through application arguments. Expected freeze validation: 40/160 split, held-out 80/80 balance, four exception categories of 20, no shared-ancestry overlap. Expected run accounting: 800 slots; status and actual cost for each. The audit command prepares evidence for human review; it cannot manufacture independent judgments.

Manual command groups: manual = record a decision/review; manual_ui = execute the screen and keyboard checklist; freeze = hash/version review; pilot/benchmark = matching evaluation commands; audit = independent rubric work; analysis = scorer plus written interpretation; reproduce = clean setup and demo; release = publication checklist. Store evidence paths in the tracker when tasks change status.
