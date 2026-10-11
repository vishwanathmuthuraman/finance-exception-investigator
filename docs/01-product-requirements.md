# 01 — Product requirements

Status: proposed v1 requirements; none is an achieved product capability.

## Problem, users and outcome

A controller sees records that disagree and must reconstruct what happened. The product should assemble the relevant records, calculate differences, identify missing evidence and prepare a reviewable case.

The primary user is a finance operations analyst investigating mismatches. The controller owns the review outcome. A finance systems engineer imports exports and diagnoses import problems. One local operator may perform these roles in the demonstration; this does not establish enterprise identity or segregation of duties.

The outcome is an evidence packet and recorded human decision. The initial product hypothesis is that contextual explanations can improve diagnosis beyond deterministic matching. Buyer demand and human time savings remain untested.

## Scope and accounting convention

One synthetic purchase-to-payment workflow, USD only, amounts in integer cents. A bundle contains related orders, invoices, payments and simplified ledger entries as of a fixed date. Invoice and payment ledger entries represent positive source amounts, not a complete double-entry general ledger. Taxes are included in document totals. One invoice references one order; one payment applies to one invoice; multiple payments may settle an invoice.

Cover duplicate invoice records, amount discrepancies, overdue partial payments and missing supporting records. A legitimate partial payment before the due date is a clean open balance, not automatically an exception. Invoice date, due date and as-of date govern this distinction.

Exclude exchange conversion, tax calculation, credit notes, refunds, netting, payment allocation across invoices, document OCR, real bank connections, ERP mutations and autonomous accounting decisions. Unsupported inputs fail validation or require review; silently approximating them is prohibited.

## Functional requirements and stories

| ID | User story and required behavior | Acceptance evidence to build |
|---|---|---|
| FR-01 | As an engineer, I import four CSV files or a bundle JSON and receive row-level validation errors before any invalid bundle is committed. | Valid JSON/CSV equivalent; missing headers, malformed dates, decimals and foreign currency rejected. |
| FR-02 | As an analyst, I trust balances because calculations use bounded integer minor units. | Exact totals, outstanding balance and difference values; no float conversion. |
| FR-03 | As an engineer, I can repeat an import or investigation without duplicate records or contradictory results. | Same content returns the same stored identity; conflicting content under the same bundle ID is rejected. |
| FR-04 | As an analyst, I see candidate and accepted links, the rule used and ambiguity. | Same-supplier reference matching, one-to-many partial payments and ambiguous candidates tested. |
| FR-05 | As an analyst, I see duplicate invoice evidence without counting it twice as a payable. | Same supplier plus normalized invoice number raises a duplicate finding; conflicting duplicates remain unresolved. |
| FR-06 | As an analyst, I see exact order/invoice, invoice/ledger and payment/ledger differences. | Nonzero differences beyond the configured tolerance have input-field citations and a calculation. |
| FR-07 | As an analyst, I distinguish clean open balances, fully settled invoices and overdue shortfalls. | Clean future-due partial payment and overdue variant produce different outcomes. |
| FR-08 | As an analyst, I see missing orders, invoices or required ledger records and a specific request for evidence. | No invented missing record or assumed zero; unpaid but not-due invoice does not require a payment record. |
| FR-09 | As a reviewer, I open the evidence supporting every substantive claim. | Record IDs and field pointers resolve; derived claims cite deterministic calculations; unsupported hypotheses are labeled. |
| FR-10 | As an analyst, I optionally obtain grounded hypotheses without letting AI override calculations or clear a case. | Invalid output, missing citations and timeout fall back to the deterministic report. |
| FR-11 | As a controller, I record acceptance, an evidence-backed dismissal or a request for evidence. | Immutable review event records actor, reason, evidence and report version; unresolved findings cannot disappear. |
| FR-12 | As a reviewer, I inspect a case queue and evidence timeline using keyboard navigation. | Queue filters, empty/error/loading states, ordered evidence and usable narrow-screen layout. |
| FR-13 | As a reviewer, I export the exact case I reviewed. | JSON plus printable HTML include versions, findings, evidence, human events and synthetic-data label. |
| FR-14 | As an operator, I receive explicit failure states and bounded optional model spend. | Invalid rows, interrupted work, malicious text, provider failure and budget exhaustion tested. |
| FR-15 | As an evaluator, I compare strategies using identical sanitized inputs without answer or source-name leakage. | Opaque projection, ancestry-separated splits, 800 runs and label-leakage tests; complete scoring. |
| FR-16 | As a new user, I reproduce the demonstration from documented setup. | Fresh local environment, locked dependencies, example commands and report artifacts verified. |

## Workflow and screen specification

1. **Import:** choose CSV directory or JSON; display bundle count, currency, as-of date and errors. Confirm the synthetic demonstration label.
2. **Queue:** columns: case ID, supplier, invoice references, deterministic outcome, open balance, exception types, review state. Filters: outcome, exception type and review state. Search by record/reference. Always show the total and filtered counts.
3. **Case:** header contains bundle/report versions and as-of date. Main column shows findings, exact calculations and ordered record events. Side panel shows AI hypotheses separately, evidence gaps and reviewer controls.
4. **Evidence drawer:** opens the source record, highlights a field and shows file/pointer or CSV row. Missing evidence displays the expected record type and reference, never a fabricated citation.
5. **Review/export:** reason and cited evidence required for dismissals; confirm the local review event; export a versioned snapshot.

Use text labels as well as color. Show amounts as USD with two decimal places while retaining cents in exports. Never label a reviewed case “paid” unless records substantiate payment. A human acknowledgment closes an investigation task, not a ledger balance.

## Interface decisions

Use a local server-rendered interface. AI defaults off. Avoid uncalibrated confidence percentages.
