# 02 — Proposed architecture

Status: design only. Named modules, database tables, commands and routes below do not exist yet.

## Components and flow

    CSV/JSON -> validation -> immutable bundle store -> deterministic links/calculations
                                                      -> findings -> case report
                                                                  -> optional AI hypotheses
    case report -> human review -> JSON/HTML export
    evaluator-only truth -> scorer (never into the application or model)

Use Python 3.12 and uv for dependency management; SQLite for local persistence; FastAPI for the optional local HTTP adapter and planned browser interface. The CLI is the first usable interface. Bind HTTP to loopback. Remote multi-user deployment requires a later authentication and authorization design.

## Planned file layout

    pyproject.toml, uv.lock
    src/finance_exception_investigator/
      cli.py, config.py, api.py
      contracts.py, ingest.py, normalization.py, store.py
      matching.py, calculations.py, rules.py, cases.py, citations.py
      ai.py, review.py, export.py
      templates/queue.html, case.html
      static/app.css
    tests/unit/, tests/integration/, tests/evaluation/
    evaluation/generate.py, split.py, run.py, score.py, audit.py
    evaluation/manifests/, reports/
    outputs/                 # generated, ignored

Contracts are in [schemas](../schemas/README.md); review them before implementation.

## Data contracts and ingestion

Each input has schema version, bundle ID, template family, lineage group, as-of date, USD currency and four arrays. Every record has a stable ID, supplier ID and source locator. Orders contain order number, date and total; invoices contain invoice number, order reference, issue/due dates and total; payments contain payment reference, optional invoice reference, date and total; ledger entries identify invoice/payment kind, relevant reference, date and total.

CSV files are orders.csv, invoices.csv, payments.csv and ledger_entries.csv. Their headers match the supplied [CSV example](../fixtures/csv/clean-settled/orders.csv), with bundle ID, template family, lineage group, as-of and currency repeated. The importer creates source locators from actual filenames and physical row numbers, including the header as row 1. It must not trust a caller-provided CSV provenance field. Empty files still require headers. Reject mismatched bundle metadata.

Store source bytes with a digest and normalized records with stable IDs. Normalize text using Unicode NFC, surrounding-whitespace removal and case folding for matching; preserve original text, punctuation and leading zeros. Reject duplicate record IDs. Unique record IDs do not imply unique invoices.

Dates are ISO calendar dates. All event dates must be on or before as-of; a due date may be later but must not precede issue date. All monetary fields are integers between 1 and 1,000,000,000,000 cents. Derived totals must remain within signed 64-bit storage bounds; reject overflow before persistence.

## Evaluated input boundary

An evaluator-owned allowlist converts archives to [strategy-input.schema.json](../schemas/strategy-input.schema.json) before **every** strategy, including exact and rules. Replace bundle IDs, record IDs and source locators with opaque random tokens independent of outcomes. Preserve mapping consistency and business references. Exclude descriptive filenames, paths, template_family, lineage_group, partition/split, category labels, oracle fields and comments. Retain necessary business facts.

All strategies receive identical projected bytes. Model context may add only calculations/findings derived from those bytes; derived finding types are not oracle labels. Strategies/models cannot read reverse maps, archives or truth. Citations use opaque IDs and field pointers. After scoring, the evaluator joins its reverse map to render readable source citations. Never feed enriched UI/export output back into evaluation.

## Matching and calculations

Exact baseline: raw same-supplier references only; exact amount checks; no inferred link when a reference is absent. Rules baseline: normalized references, duplicate checks, partial-payment aggregation and defined fallback candidates. Both use the same authoritative arithmetic.

Accept an invoice-to-order link only when its order reference identifies one order for the supplier. Link payment-to-invoice by unique reference; multiple payments may link to one invoice. For a missing payment invoice reference, a rules candidate must share supplier, exactly match the invoice amount, and fall within 14 days after issue and before as-of. Accept only a unique candidate. No fuzzy name-only match and no arbitrary tie-breaking. Candidate ambiguity requires review.

Link invoice ledger entries by supplier and invoice reference, and payment ledger entries by supplier and payment reference. Require exactly one corresponding ledger entry per unique invoice and per payment in v1; multiple ledger entries remain an ambiguity because split journal entries are outside scope.

Calculate outstanding = invoice total minus sum of uniquely linked payments. A negative result is an overpayment discrepancy. Zero is settled. Positive with as-of after due date is an overdue partial/unpaid exception; otherwise it is a clean open balance if other checks pass. Do not aggregate duplicate invoice faces into liability. Conflicting duplicates prevent clearance.

Check invoice against order total, invoice ledger against invoice total and payment ledger against payment total. Default tolerance is zero; any configured nonzero tolerance is visible and versioned. Clean partial payments do not need each payment to equal the invoice total.

## Persistence and idempotency

Proposed tables: bundles, records, runs, links, calculations, findings, claims, review_events and exports. Foreign keys connect every child to its parent. Use parameterized SQL, explicit transactions and connection-level foreign-key enforcement.

Bundle identity is bundle ID plus a canonical-content digest. Identical re-import is a no-op; changed content under an existing ID is a conflict, requiring a new bundle version. A deterministic run key hashes bundle digest, strategy, configuration and rules version. For AI, also include provider/model snapshot, prompt version and trial ID; repeated trial IDs reuse the result. Different trial IDs intentionally rerun.

A review action has a client idempotency key unique within report/actor. Repeat returns the existing event. Events append; concurrent stale report updates return conflict. No destructive edit of the underlying evidence is part of review.

## AI boundary, evidence and failures

The model receives only sanitized records and their deterministic links, calculations and findings. It cannot access expected-outcome files, filesystem tools or posting functions. Treat every source string as untrusted data. Supply a fixed output contract and reject unknown fields.

Claims have kind fact, hypothesis or missing_evidence. Facts cite existing record fields or calculation IDs; citations must resolve and calculations must agree. Hypotheses say what could explain a finding and what would discriminate it; a citation alone does not establish that interpretation is true. Missing-evidence claims name a needed source and cite the observed reference creating that need.

The deterministic outcome is clear, review_required or insufficient_evidence. A processing failure produces failed. AI may add hypotheses and evidence requests; it cannot change an outcome to clear, remove findings, or authorize a posting. The result records unavailable/failed AI status distinctly from completed AI output.

## Proposed local HTTP contract

GET /cases lists paginated metadata; GET /cases/{id} retrieves a report; GET /cases/{id}/records/{record_id} resolves evidence; POST /imports validates local uploads; POST /cases/{id}/reviews appends a review; GET /cases/{id}/export returns a snapshot. Reject oversized input, unsafe filenames and unknown records. No endpoint mutates a bank, ERP or ledger.

Use timeouts, at most one retry for transient provider errors, and a per-run token/cost ceiling. On failure keep the deterministic report and record the reason. Do not save secrets or raw provider request bodies in public logs.
