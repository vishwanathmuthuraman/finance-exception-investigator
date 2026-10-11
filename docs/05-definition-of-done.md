# 05 — Definition of done

**All targets below are proposed and unachieved.** Specification validation is different from application or benchmark validation.

## Requirement-to-test traceability

Tests named here are planned files; M IDs refer to the [public milestones](03-build-plan.md).

| Requirements | Planned verification | Milestone |
|---|---|---|
| FR-01 | tests/integration/test_ingest.py: JSON/CSV equivalence, atomic invalid import | M1 |
| FR-02 | tests/unit/test_calculations.py: cents, totals, overflow | M2 |
| FR-03 | tests/integration/test_idempotency.py: repeat/conflict/retry | M1, M3 |
| FR-04 | tests/unit/test_matching.py: references, unique fallback, ambiguity | M2 |
| FR-05 | tests/unit/test_duplicates.py: same/different suppliers, conflicting duplicates | M2 |
| FR-06 | tests/unit/test_amounts.py: every comparison and tolerance boundary | M2 |
| FR-07 | tests/unit/test_partial_payments.py: due-date boundary, overpayment | M2 |
| FR-08 | tests/unit/test_missing_records.py: invoice/order/ledger, legitimate unpaid | M2 |
| FR-09 | tests/unit/test_citations.py: broken pointer, wrong source, arithmetic | M3, M4 |
| FR-10 | tests/integration/test_ai_boundary.py: malformed output, unsupported fact, fallback | M4 |
| FR-11 | tests/integration/test_reviews.py: transitions, stale versions, reason required | M3 |
| FR-12 | Recorded keyboard and narrow-screen UI walkthrough; API contract tests | M3 |
| FR-13 | tests/integration/test_exports.py: snapshot fidelity and safe escaping | M3 |
| FR-14 | tests/integration/test_failures.py: prompt injection, oversized file, timeout, budget | M4, M5 |
| FR-15 | tests/evaluation/test_protocol.py: projection canaries, opaque IDs, ancestry split/clusters and denominators | M5 |
| FR-16 | Recorded clean-environment setup and complete demo | M6 |

## Artifact completion and product acceptance

Artifact completion requires items 1, 2, 6, 7 and 8 below. Items 3–5 are separate product-performance targets. A reproducible research artifact may be complete even when a performance target or AI hypothesis fails; its status and conclusions must say so explicitly.

1. Every implementation FR has verification evidence; all eight starter fixtures match their oracle semantics. FR-15 requires faithful measurement, not a favorable experimental result.
2. Full corpus exists: 40 development and 160 held-out, with 80 clean/80 exception held-out and no shared ancestry across partitions. All 800 runs are accounted for. Projection/label-invariance tests pass, request payloads exclude labels, and actual independent-lineage counts are reported.
3. Rules and rules_ai each have **0/80 false clearances** per held-out trial. Exception recall is at least **95% (76/80)**; clean-case false alarms at most **10% (8/80)**. These are project acceptance targets, not industry standards.
4. Accepted-link precision is at least **98%**, recall at least **95%**. Publish actual denominators; do not suppress difficult bundles.
5. Citation resolution is **100%**; audited factual support at least **98%**. Uncited factual claims are **0**. Invalid model output must cause fallback, not silently enter the evidence packet.
6. Independent audit is complete and disagreements documented. The analysis does not require AI to beat rules: a negative result is acceptable when reported honestly.
7. Fresh installation succeeds with a lockfile; the CLI, queue, evidence view, review and exports work locally. No live financial action is possible.
8. Public-release review, license selection and dependency notices are complete.

If performance targets fail but artifact gates pass, a research v1 release may be complete with those failures prominently reported. It has not met the product-performance acceptance targets and must not be described as validated for operational use. Incomplete reproduction, missing audit or unaccounted runs mean artifact completion remains unmet. Do not retune on held-out cases and reuse the same set as independent proof.

## Six-minute demonstration

- 0:00–0:45: explain synthetic scope and import clean-settled CSV; repeat import and show no duplicates.
- 0:45–1:30: show settled evidence and exact calculations; open clean-partial to show the legitimate outstanding balance.
- 1:30–2:30: open duplicate-invoice and amount-mismatch; inspect both record fields and differences.
- 2:30–3:30: open overdue-partial and missing-ledger; identify the specific missing evidence or due-date fact.
- 3:30–4:30: compare deterministic findings with optional AI hypotheses; show a rejected/failed AI response retaining the rules report.
- 4:30–5:15: append a reasoned human review event and export the reviewed snapshot.
- 5:15–6:00: show the benchmark table, denominators and one failure/limitation.

Completion evidence belongs in a future reports/release-checklist.md with artifact links, software revision, configuration, date and reviewer. Leave unchecked items visible.
