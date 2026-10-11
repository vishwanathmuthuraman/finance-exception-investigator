"""Synthetic bundle ingestion and conservative exact-reference reconciliation."""

import csv
import re
import unicodedata
from datetime import date
from pathlib import Path

from .common import ContractError, digest, exact_integer, unique, validate_shape

KINDS = ("orders", "invoices", "payments", "ledger_entries")
META = ("bundle_id", "template_family", "lineage_group", "as_of", "currency")
FIELDS = {
    "orders": ("record_id", "supplier_id", "order_number", "ordered_on", "amount_minor"),
    "invoices": (
        "record_id",
        "supplier_id",
        "invoice_number",
        "order_ref",
        "issued_on",
        "due_on",
        "amount_minor",
    ),
    "payments": (
        "record_id",
        "supplier_id",
        "payment_reference",
        "invoice_ref",
        "paid_on",
        "amount_minor",
    ),
    "ledger_entries": (
        "record_id",
        "supplier_id",
        "entry_type",
        "invoice_ref",
        "payment_ref",
        "posted_on",
        "amount_minor",
    ),
}


def normalize(text):
    return unicodedata.normalize("NFC", text).strip().casefold()


def validate_bundle(bundle):
    validate_shape(bundle, "bundle")
    all_records = [row for kind in KINDS for row in bundle[kind]]
    unique(all_records, lambda row: row["record_id"])
    cutoff = date.fromisoformat(bundle["as_of"])
    for record in all_records:
        exact_integer(record["amount_minor"], 1, 1_000_000_000_000)
        for key in ("ordered_on", "issued_on", "paid_on", "posted_on"):
            if key in record and date.fromisoformat(record[key]) > cutoff:
                raise ContractError("record is later than bundle as-of date")
        if "due_on" in record and date.fromisoformat(record["due_on"]) < date.fromisoformat(
            record["issued_on"]
        ):
            raise ContractError("due date precedes invoice")
    exact_integer(sum(row["amount_minor"] for row in all_records))
    return bundle


def import_csv(directory):
    bundle = {"schema_version": "1.0", **{kind: [] for kind in KINDS}}
    metadata = None
    for kind in KINDS:
        path = Path(directory) / (kind + ".csv")
        if path.stat().st_size > 5_000_000:
            raise ContractError("CSV exceeds 5 MB limit")
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.reader(handle)
            columns = next(reader, [])
            if columns != list(META + FIELDS[kind]):
                raise ContractError("missing, duplicated or unexpected CSV headers")
            previous_line = reader.line_num
            for values in reader:
                source_row = previous_line + 1
                previous_line = reader.line_num
                if len(values) != len(columns):
                    raise ContractError("invalid CSV column count")
                row = dict(zip(columns, values, strict=True))
                current = {key: row[key] for key in META}
                if metadata is not None and current != metadata:
                    raise ContractError("inconsistent CSV bundle metadata")
                metadata = current
                record = {key: row[key] for key in FIELDS[kind]}
                if not re.fullmatch(r"[0-9]+", record["amount_minor"]):
                    raise ContractError("CSV amount must be integer minor units")
                record["amount_minor"] = int(record["amount_minor"])
                for reference in ("invoice_ref", "payment_ref"):
                    if reference in record and record[reference] == "":
                        record[reference] = None
                record["source"] = {
                    "file": path.name,
                    "row": source_row,
                    "pointer": "/" + kind + "/" + str(len(bundle[kind])),
                }
                bundle[kind].append(record)
    if metadata is None:
        raise ContractError("empty bundle has no declared metadata")
    bundle.update(metadata)
    return validate_bundle(bundle)


def reconcile(bundle):
    validate_bundle(bundle)
    links, findings, outstanding = [], [], {}
    if not any(bundle[kind] for kind in KINDS):
        raise ContractError("empty bundle cannot establish reconciliation")

    def find(kind, supplier, field, reference):
        if reference is None:
            return []
        return [
            row
            for row in bundle[kind]
            if row["supplier_id"] == supplier
            and row[field] is not None
            and normalize(row[field]) == normalize(reference)
        ]

    def link(left, right, relationship):
        links.append(
            {
                "from_record_id": left["record_id"],
                "to_record_id": right["record_id"],
                "relationship": relationship,
            }
        )

    def finding(kind, records, field, missing=None, difference=None):
        ids = sorted({row["record_id"] for row in records})
        findings.append(
            {
                "type": kind,
                "record_ids": ids,
                "missing_record_type": missing,
                "difference_minor": difference,
                "citations": [
                    {
                        "record_id": row["record_id"],
                        "pointer": "/" + (field if field in row else "amount_minor"),
                    }
                    for row in records
                ],
            }
        )

    duplicate_groups = {}
    for invoice in bundle["invoices"]:
        key = invoice["supplier_id"], normalize(invoice["invoice_number"])
        duplicate_groups.setdefault(key, []).append(invoice)
    for group in duplicate_groups.values():
        if len(group) > 1:
            finding("duplicate_invoice", group, "invoice_number")
    for invoice in bundle["invoices"]:
        orders = find("orders", invoice["supplier_id"], "order_number", invoice["order_ref"])
        if len(orders) == 1:
            link(invoice, orders[0], "invoice_order")
            difference = invoice["amount_minor"] - orders[0]["amount_minor"]
            if difference:
                finding(
                    "amount_discrepancy",
                    [invoice, orders[0]],
                    "amount_minor",
                    difference=difference,
                )
        else:
            finding(
                "missing_record" if not orders else "ambiguous_link",
                [invoice],
                "order_ref",
                "order" if not orders else None,
            )
    paid = {}
    missing_invoices = {}
    for payment in bundle["payments"]:
        candidates = find(
            "invoices", payment["supplier_id"], "invoice_number", payment["invoice_ref"]
        )
        if len(candidates) == 1:
            invoice = candidates[0]
            link(payment, invoice, "payment_invoice")
            if date.fromisoformat(payment["paid_on"]) < date.fromisoformat(invoice["issued_on"]):
                finding("unsupported_payment_timing", [payment, invoice], "paid_on")
            paid.setdefault(invoice["record_id"], []).append(payment)
        elif not candidates:
            missing_invoices.setdefault(
                (payment["supplier_id"], payment["invoice_ref"]), []
            ).append(payment)
    for ledger in bundle["ledger_entries"]:
        kind, field = (
            ("invoices", "invoice_ref")
            if ledger["entry_type"] == "invoice"
            else ("payments", "payment_ref")
        )
        reference_field = "invoice_number" if kind == "invoices" else "payment_reference"
        candidates = find(kind, ledger["supplier_id"], reference_field, ledger[field])
        if len(candidates) == 1:
            source = candidates[0]
            link(ledger, source, "ledger_invoice" if kind == "invoices" else "ledger_payment")
            difference = ledger["amount_minor"] - source["amount_minor"]
            if difference:
                finding(
                    "amount_discrepancy", [source, ledger], "amount_minor", difference=difference
                )
        elif not candidates:
            if kind == "invoices":
                missing_invoices.setdefault((ledger["supplier_id"], ledger[field]), []).append(
                    ledger
                )
            else:
                finding("missing_record", [ledger], field, "payment")
        elif kind == "payments":
            # Invoice ambiguity already has a duplicate_invoice review finding.
            finding("ambiguous_link", [ledger] + candidates, field)
    for records in missing_invoices.values():
        finding("missing_record", records, "invoice_ref", "invoice")
    for kind, field, entry_type in (
        ("invoices", "invoice_number", "invoice"),
        ("payments", "payment_reference", "payment"),
    ):
        for source in bundle[kind]:
            if (
                kind == "invoices"
                and len(
                    duplicate_groups[source["supplier_id"], normalize(source["invoice_number"])]
                )
                > 1
            ):
                continue
            ledgers = [
                row
                for row in bundle["ledger_entries"]
                if row["entry_type"] == entry_type
                and row["supplier_id"] == source["supplier_id"]
                and row[entry_type + "_ref"] is not None
                and normalize(row[entry_type + "_ref"]) == normalize(source[field])
            ]
            if len(ledgers) != 1:
                finding(
                    "missing_record" if not ledgers else "ambiguous_link",
                    [source] + ledgers,
                    field,
                    entry_type + "_ledger" if not ledgers else None,
                )
    for invoice in bundle["invoices"]:
        if len(duplicate_groups[invoice["supplier_id"], normalize(invoice["invoice_number"])]) > 1:
            continue
        payments = paid.get(invoice["record_id"], [])
        balance = invoice["amount_minor"] - exact_integer(
            sum(row["amount_minor"] for row in payments)
        )
        outstanding[invoice["record_id"]] = balance
        if balance < 0:
            finding("overpayment", [invoice] + payments, "amount_minor", difference=balance)
        elif balance > 0 and date.fromisoformat(bundle["as_of"]) > date.fromisoformat(
            invoice["due_on"]
        ):
            finding("overdue_balance", [invoice] + payments, "due_on", difference=balance)
    outcome = (
        "insufficient_evidence"
        if any(row["type"] in {"missing_record", "ambiguous_link"} for row in findings)
        else "review_required"
        if findings
        else "clear"
    )
    return {
        "schema_version": "0.1",
        "kind": "deterministic_reconciliation",
        "input_sha256": digest(bundle),
        "bundle_id": bundle["bundle_id"],
        "currency": bundle["currency"],
        "as_of": bundle["as_of"],
        "outcome": outcome,
        "links": links,
        "findings": findings,
        "outstanding_minor": outstanding,
        "ai_status": "not_implemented",
        "matching_scope": "normalized_explicit_references_only",
    }
