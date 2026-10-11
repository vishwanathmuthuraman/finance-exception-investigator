import copy
import json
import shutil
from pathlib import Path

import pytest

from finance_exception_investigator.common import ContractError
from finance_exception_investigator.core import import_csv, reconcile, validate_bundle

ROOT = Path(__file__).resolve().parents[1]
BUNDLES = sorted((ROOT / "fixtures/development").glob("*.bundle.json"))


@pytest.fixture
def bundle():
    return json.loads((ROOT / "fixtures/development/clean-settled.bundle.json").read_text())


@pytest.mark.parametrize("path", BUNDLES, ids=lambda path: path.stem)
def test_original_development_bundles(path):
    bundle = json.loads(path.read_text())
    expected = json.loads(
        (ROOT / f"fixtures/expected/{bundle['bundle_id']}.expected.json").read_text()
    )
    result = reconcile(bundle)
    assert result["outcome"] == expected["expected_outcome"]
    assert result["outstanding_minor"] == expected["expected_outstanding_minor"]
    assert {row["type"] for row in result["findings"]} == {
        row["type"] for row in expected["expected_findings"]
    }

    def key(row):
        return row["from_record_id"], row["to_record_id"], row["relationship"]

    assert {key(row) for row in result["links"]} == {key(row) for row in expected["expected_links"]}
    records = {
        row["record_id"]: row
        for kind in ("orders", "invoices", "payments", "ledger_entries")
        for row in bundle[kind]
    }
    for finding in result["findings"]:
        for citation in finding["citations"]:
            assert citation["pointer"].removeprefix("/") in records[citation["record_id"]]


def test_json_csv_business_equivalence_and_real_row_provenance(bundle):
    csv_bundle = import_csv(ROOT / "fixtures/csv/clean-settled")
    assert reconcile(csv_bundle)["outcome"] == reconcile(bundle)["outcome"] == "clear"
    for kind in ("orders", "invoices", "payments", "ledger_entries"):
        for csv_row, json_row in zip(csv_bundle[kind], bundle[kind], strict=True):
            assert {k: v for k, v in csv_row.items() if k != "source"} == {
                k: v for k, v in json_row.items() if k != "source"
            }
            assert csv_row["source"]["file"] == kind + ".csv"
            assert csv_row["source"]["row"] >= 2


@pytest.mark.parametrize(
    "mutation", ["float", "bool", "negative", "duplicate_id", "future", "currency", "early_due"]
)
def test_invalid_bundle_rejected(bundle, mutation):
    if mutation in {"float", "bool", "negative"}:
        bundle["orders"][0]["amount_minor"] = {"float": 10000.0, "bool": True, "negative": -1}[
            mutation
        ]
    elif mutation == "duplicate_id":
        bundle["orders"].append(copy.deepcopy(bundle["orders"][0]))
    elif mutation == "future":
        bundle["payments"][0]["paid_on"] = "2026-02-01"
    elif mutation == "currency":
        bundle["currency"] = "INR"
    else:
        bundle["invoices"][0]["due_on"] = "2026-01-01"
    with pytest.raises(ContractError):
        validate_bundle(bundle)


def test_same_reference_different_supplier_never_matches(bundle):
    bundle["payments"][0]["supplier_id"] = "OTHER"
    result = reconcile(bundle)
    assert result["outcome"] == "insufficient_evidence"
    assert not any(row["relationship"] == "payment_invoice" for row in result["links"])


def test_due_date_is_inclusive_and_next_day_is_overdue(bundle):
    bundle["as_of"] = "2026-01-20"
    bundle["payments"][0]["amount_minor"] = bundle["ledger_entries"][1]["amount_minor"] = 4000
    assert reconcile(bundle)["outcome"] == "clear"
    bundle["as_of"] = "2026-01-21"
    assert reconcile(bundle)["outcome"] == "review_required"


def test_ambiguous_order_reference_cannot_clear(bundle):
    another = dict(bundle["orders"][0], record_id="O2")
    bundle["orders"].append(another)
    assert reconcile(bundle)["outcome"] == "insufficient_evidence"


def test_csv_decimal_rejected_without_inventing_cents(tmp_path):
    target = tmp_path / "csv"
    shutil.copytree(ROOT / "fixtures/csv/clean-settled", target)
    path = target / "orders.csv"
    path.write_text(path.read_text().replace(",10000", ",100.00"))
    with pytest.raises(ContractError, match="integer"):
        import_csv(target)


def test_input_immutable_and_output_repeatable(bundle):
    original = copy.deepcopy(bundle)
    assert reconcile(bundle) == reconcile(bundle)
    assert bundle == original


def test_ambiguous_ledger_payment_reference_cannot_clear(bundle):
    payment = bundle["payments"][0]
    payment["amount_minor"] //= 2
    bundle["payments"].append(dict(payment, record_id="P2"))
    result = reconcile(bundle)
    assert result["outcome"] == "insufficient_evidence"
    assert any(row["type"] == "ambiguous_link" for row in result["findings"])
    assert not any(row["relationship"] == "ledger_payment" for row in result["links"])


def test_empty_bundle_cannot_claim_clear(bundle):
    for kind in ("orders", "invoices", "payments", "ledger_entries"):
        bundle[kind] = []
    with pytest.raises(ContractError, match="empty"):
        reconcile(bundle)
