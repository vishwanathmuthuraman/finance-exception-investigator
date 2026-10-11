# 04 — Evaluation protocol

Status: preregistration draft. No measured result exists.

## Research question and hypotheses

Does rules-plus-AI investigation improve evidence-backed diagnosis over deterministic reconciliation without increasing incorrect clearances?

H1: AI hypotheses increase correct supported diagnoses among exception bundles. H2: this can occur without increasing false clearance or unsupported factual claims. These hypotheses may fail. Because the proposed AI cannot override deterministic clearance, equal clearance outcomes between rules and rules-plus-AI are expected by construction; that equality is not evidence that free-form agents are safe.

The benchmark measures seeded synthetic problems under declared conventions. It cannot establish accounting assurance, real-world loss prevention, compliance or human time saved.

## Corpus and split

Create 200 original bundles: 40 development and 160 held out. The 40 development bundles include the eight supplied seeds; do not count the CSV rendering of the clean seed twice. The remaining 32 and all 160 held-out bundles are future work.

Development target: 20 exception and 20 clean bundles. Held-out target: 80 exception and 80 clean. Allocate held-out exceptions as 20 duplicate invoices, 20 amount discrepancies, 20 overdue partial/unpaid balances and 20 missing-record cases. Include clean partial payments among the 80 clean. Each exception bundle has one primary category; record additional effects separately to avoid double-counting.

Nominal generation targets are 20 development and 80 held-out template families, usually two bundles per family. These are planning targets, not independent-sample counts or guaranteed power. The eight supplied seeds share one lineage. Identify highest shared ancestry before splitting: variants, templates and descendants stay together regardless of family names. Review independence, report actual lineage counts, and adjust template construction within the fixed 40/160 totals. Random row splitting is prohibited. Vary dates, amounts, reference noise and record ordering without encoding outcomes in metadata.

An evaluator maintains expected links, exception category, correct outcome, diagnosis concepts and required evidence. Every strategy receives only the strict sanitized projection: opaque bundle/record/source IDs, no readable filenames, family/lineage/split/category labels or truth. Evaluator-only reverse mappings resolve citations after scoring. Keep archives, mappings and truth outside strategy/model access. Have a second reviewer validate the held-out oracle before freezing; log ambiguous cases and resolve them without looking at model outputs.

Seal evaluator-only manifests containing IDs, ancestry, projection version and source/projected hashes. Record generation seed, schema version and protocol revision. A held-out set is evaluated once after tuning. After results inform changes, call it a validation set and create a new test set for a new confirmatory claim.

## Three comparators and execution count

| Strategy | Behavior |
|---|---|
| exact | Literal same-supplier reference matching and exact checks; abstains on missing/ambiguous links. |
| rules | Normalization, duplicate detection, deterministic invariants, partial balances and documented unique fallback matching. |
| rules_ai | Identical rules output plus model hypotheses and evidence requests. No hidden extra records or ground-truth access. |

Give all strategies identical input bundles and calculation definitions. Freeze rules, tolerance, prompt, allowed model and cost ceiling on development data. Report different actual work and costs; never imply equal cost because inputs match.

Run exact once and rules once across 160 held-out bundles: 320 runs. Run rules_ai three independent trial IDs per bundle: 480 runs. Total: 800, excluding development, spend pilots and optional sensitivity checks. Record failed/time-out runs in the denominator. Seeds, temperature and model settings are logged where supported; model nondeterminism may remain.

## Metrics with explicit denominators

| Metric | Definition |
|---|---|
| Link precision / recall | Correct accepted record-pair links divided by all accepted links / all oracle links; also report ambiguous abstentions. |
| Exception recall | Exception bundles explicitly flagged with the correct primary category divided by 80. Missing-evidence flags count only for matching oracle cases. |
| Missed-exception rate | Exception bundles without the correct exception flag divided by 80; includes failed runs and unclassified abstentions. |
| False-clearance rate | Exception bundles returned clear divided by 80. Report three AI trial rates separately plus the proportion with any false clearance. |
| Clean-case false alarm | Clean bundles flagged review_required or insufficient_evidence divided by 80. Report failed runs separately. |
| Clearance coverage | All bundles returned clear divided by 160; also clean clearances divided by 80. Low false clearance by abstaining on everything is not success. |
| Diagnosis correctness | Exception bundles with the required causal diagnosis supported by observed records divided by 80; audit rubric permits multiple valid phrasings. |
| Citation correctness | Audited citations that resolve to the claimed record/field and support the associated factual statement divided by all audited citations. Report resolution and semantic support separately. |
| Unsupported-claim rate | Unsupported factual claims divided by all audited factual claims; separately count uncited facts. Hypotheses remain audited for misleading certainty. |
| Cost / performance | Actual tokens, priced API cost, retries, wall-clock duration and failure count per strategy; disclose price date/model. |

Use paired bundle comparisons. Cluster uncertainty by highest shared lineage, nesting families, bundles and AI trials within it; descendants are not independent. Report actual independent-cluster counts and interval limitations. Publish per-category results and every false clearance. For zero observed errors, state the numerator and denominator; never claim zero real-world risk.

## Human audit and reporting

Prespecify 40 held-out bundles, ten per exception category, selected by a recorded seed before execution. Audit all three AI trials for those bundles; a second reviewer independently audits the same claims. Additionally inspect all false clearances and any clean-case unsupported factual claims flagged by automated checks. Report disagreements and adjudications; if no independent reviewer is available, state that the external-audit gate is unmet.

Reject unexpected projection fields. Test renamed sources, shuffled opaque IDs and injected label canaries; business outcomes must be invariant after ID remapping. Inspect serialized strategy/model requests for leaks. The scorer validates pointers, IDs and arithmetic; semantic support needs judgment. Never use the evaluated model as the sole judge of its own explanations. Grader fixes require a documented reason and rescoring all affected strategies.

The report must include setup, provenance, baselines, frozen configuration, corpus distribution, failures, paired effects, uncertainty, cost, limitations and a conclusion even if AI provides no improvement.
