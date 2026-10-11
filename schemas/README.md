# JSON contracts

Draft 2020-12 contracts, proposed v1. [Input bundle](bundle.schema.json), [expected outcome](expected-outcome.schema.json), [investigation report](investigation-report.schema.json), [review event](review-event.schema.json), and [sanitized strategy input](strategy-input.schema.json).

Input and expected-outcome examples are provided in [fixtures](../fixtures/README.md). The report/review contracts intentionally have no fabricated application output examples.

Use explicit date/date-time format validation. JSON Schema validates structure; planned application checks must additionally enforce unique IDs, source pointer resolution, date ordering, references, integer aggregate bounds, accounting relationships and review state transitions. A valid schema instance alone is not a financially correct result.

Expected outcomes belong to the evaluator. Do not include them in prompts, retrieval indexes or import paths. Schema and fixture validation during blueprint preparation does not constitute product testing.

Archival bundles are not evaluated inputs. Project them into the strict strategy-input contract: opaque bundle/record/source IDs and business fields only. Reverse mappings remain evaluator-only until scoring. Seed files are not sanitized projections.
