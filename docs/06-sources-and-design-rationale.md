# 06 — Sources and design rationale

Sources checked 11 October 2026. These publications motivate discovery; they do not endorse this project or establish product-market fit.

| Source finding | Method and limits | Project inference |
|---|---|---|
| [BCG, How to get ROI from AI in the finance function](https://www.bcg.com/publications/2025/how-finance-leaders-can-get-roi-from-ai), 4 June 2025: 45% of surveyed finance leaders could quantify AI ROI; the article discusses data, implementation and auditability difficulties. | Surveyed more than 280 executives experienced with AI/GenAI in finance at large companies globally in March 2025. Self-reported, not a controlled intervention. | Test whether a narrow evidence workflow improves diagnosis, and expose investigation cost. The study does not measure demand for this specific tool or prove savings. |
| [McKinsey, Redefining procurement performance in the era of agentic AI](https://www.mckinsey.com/capabilities/operations/our-insights/redefining-procurement-performance-in-the-era-of-agentic-ai), 5 February 2026: describes procurement agents using supplier information and assessing cost, service and risk tradeoffs. | Industry analysis, not independent evaluation of this investigator. | Purchase-to-payment records provide a plausible bounded workflow. The chosen reconciliation rules, corpus and UI are original project design decisions, not findings from the report. |

Existing finance products already reconcile records. Establish a concrete workflow gap before claiming commercial differentiation.

## Technical references

- [uv project guide](https://docs.astral.sh/uv/guides/projects/): proposed environment and package workflow. Pin actual dependency versions in the future lockfile.
- [Python 3.12 sqlite3 documentation](https://docs.python.org/3.12/library/sqlite3.html): local storage and explicit transaction behavior. Parameterize SQL.
- [FastAPI first steps](https://fastapi.tiangolo.com/tutorial/first-steps/): optional local HTTP adapter. Proposed project routes are our design, not a third-party API.
- [JSON Schema draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core): contracts. The schema format alone does not enforce cross-record accounting relationships.
- [jsonschema validation documentation](https://python-jsonschema.readthedocs.io/en/stable/validate/): use Draft202012Validator with explicit format checking.

Provider selection is deferred. Before implementing a provider adapter, consult its current official documentation for structured responses, timeouts, model identifiers and pricing. No provider API or current price is assumed here.

All supplied fixture records are newly constructed fictional data. No report PDF, customer dataset or private work artifact is included.
