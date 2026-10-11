# 07 — Delivery, product decisions and risks

Status: planned work. Task estimates are planning assumptions, not logged effort.

## Milestones and ownership

One builder can implement the core, but accounting conventions and explanation audits need an independent reviewer. Reviewer availability is a dependency, not an assumed resource. Assign named owners privately before work begins; public roles suffice in this blueprint.

| Milestone | Tasks | Exit evidence | Suggested window |
|---|---|---|---|
| Contracts and ingestion | T01–T08 | Validated importer, repeat-safe store, exact arithmetic | Week 1–2 |
| Deterministic investigator | T09–T17 | All seeded categories, citations and case reports | Week 2–3 |
| Optional explanations and review | T18–T26 | AI fallback, reviewer workflow and local UI | Week 3–5 |
| Evaluation preparation | T27–T32 | Split corpus, scorer, freeze and spend pilot | Week 5–6 |
| Evaluation and release | T33–T38 | Results, audit, reproduction and release review | Week 7–10 |

Follow tracker dependencies; build the CLI first. Estimates exclude external waiting.

## Decisions and change control

Proposed choices: USD; integer cents; zero tolerance; exact and rule comparators; three AI trials; human review; local SQLite; no financial posting. Revisit only with a written reason, affected FRs, estimate and benchmark impact.

Every scope change records decision, alternatives, owner, date and consequence in a future docs/decision-log.md. Adding OCR, multicurrency or live connectors is a separate release. Changes to schemas, tolerance, prompts or corpus after freeze require a new version and an explicit evaluation-status decision.

Demonstrate each milestone; record completed tasks, blockers and changed assumptions weekly.

## Risk register

| Risk | Trigger | Response / owner |
|---|---|---|
| Incorrect financial convention | Reviewer disputes payable or payment treatment | Resolve with finance reviewer before corpus freeze; document simplification. |
| False clearance | Seeded exception returned clear | Block product acceptance, diagnose and report; an honest experimental release remains possible. Replace confirmatory tests after held-out tuning. |
| Benchmark leakage | Source label, ancestry or oracle enters any evaluated input | Quarantine run, fix split/path controls and replace affected evaluation. |
| AI produces plausible unsupported cause | Fact lacks supporting evidence | Reject fact, retain deterministic output, require explicit hypothesis wording. |
| Duplicate overcounting | Duplicate invoices inflate liability | Hold case for review; never pick a duplicate arbitrarily. |
| Reviewer unavailable | No independent oracle/explanation audit | Record unmet gate; publish only preliminary results. |
| Scope expands | Requests for live ERP, OCR or currency conversion | Defer; keep the one-currency contract stable. |
| Sensitive data or secrets | Real export/key enters working folder | Keep private/raw paths ignored; inspect publication file list and history. |
| Unbounded cost | Retry loop or unexpectedly long prompt | Per-run cap, one retry, cumulative budget stop and pilot first. |
| Weak commercial differentiation | Existing finance stack already solves the problem | Document discovery outcome; retain educational/research value without inventing a market. |

## Cost assumptions

Local compute, storage and browser UI are assumed available; no hosting expense is required for the proposed demo. Dependencies and any external services must be reviewed before use.

For 480 AI held-out runs, an illustrative 3,000 input and 800 output tokens per run yields 1.44 million input and 0.384 million output tokens before retries. Cost = 1.44 × provider input price per million + 0.384 × provider output price per million. These are workload assumptions, not quotes or measured consumption. Add development/pilot usage, audit effort and up to one retry. Record actual token usage and price date.

Choose a cumulative spend limit after the 10-bundle development pilot; the supplied default model budget is zero so the eventual adapter requires an explicit local configuration change. A dollar budget alone is insufficient if provider usage is delayed: also enforce token and request limits.

Commercial discovery is separate from build acceptance. Ask practitioners about a recent mismatch, its existing workflow, consequence, evidence access and budget owner. Interviews do not become customer validation by count alone; record concrete incidents and competing solutions.
