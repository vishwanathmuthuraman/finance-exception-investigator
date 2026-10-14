import hashlib
import json
import shutil
from pathlib import Path

import pytest

from finance_exception_investigator.common import ContractError
from finance_exception_investigator.store import BundleStore, ConflictError, content_digest

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "fixtures/development/clean-settled.bundle.json"
CSV_DIR = ROOT / "fixtures/csv/clean-settled"


@pytest.fixture
def store():
    with_store = BundleStore()
    yield with_store
    with_store.close()


def test_first_import_records_source_hash_and_bytes(store):
    result = store.import_path(JSON_PATH)
    assert result["bundle_created"] and result["delivery_recorded"]
    assert result["source_sha256"] == hashlib.sha256(JSON_PATH.read_bytes()).hexdigest()
    assert store.source_bytes(result["source_sha256"]) == JSON_PATH.read_bytes()


def test_repeated_identical_delivery_is_noop(store):
    first = store.import_path(JSON_PATH)
    second = store.import_path(JSON_PATH)
    assert second["content_digest"] == first["content_digest"]
    assert not second["bundle_created"] and not second["delivery_recorded"]
    assert store.delivery_count(first["bundle_id"]) == 1


def test_same_content_reformatted_is_new_delivery_same_identity(store, tmp_path):
    first = store.import_path(JSON_PATH)
    copy = tmp_path / "reformatted.json"
    copy.write_text(json.dumps(json.loads(JSON_PATH.read_text()), indent=7))
    second = store.import_path(copy)
    assert second["content_digest"] == first["content_digest"]
    assert second["source_sha256"] != first["source_sha256"]
    assert not second["bundle_created"] and second["delivery_recorded"]
    assert store.delivery_count(first["bundle_id"]) == 2


def test_conflicting_content_under_same_bundle_id_is_rejected_and_not_stored(store, tmp_path):
    first = store.import_path(JSON_PATH)
    changed = json.loads(JSON_PATH.read_text())
    changed["orders"][0]["amount_minor"] += 1
    path = tmp_path / "changed.json"
    path.write_text(json.dumps(changed))
    with pytest.raises(ConflictError):
        store.import_path(path)
    assert store.delivery_count(first["bundle_id"]) == 1
    assert store.import_path(JSON_PATH)["content_digest"] == first["content_digest"]


def test_invalid_bundle_is_never_committed(store, tmp_path):
    bad = json.loads(JSON_PATH.read_text())
    bad["orders"][0]["amount_minor"] = 1.5
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(bad))
    with pytest.raises(ContractError):
        store.import_path(path)
    assert store.db.execute("SELECT COUNT(*) FROM bundles").fetchone()[0] == 0


def test_csv_and_json_share_identity_with_distinct_source_hashes(store):
    from_json = store.import_path(JSON_PATH)
    from_csv = store.import_path(CSV_DIR)
    assert from_csv["content_digest"] == from_json["content_digest"]
    assert from_csv["source_sha256"] != from_json["source_sha256"]
    assert not from_csv["bundle_created"] and from_csv["delivery_recorded"]


def test_csv_source_hash_covers_physical_bytes_and_ignores_provenance(store, tmp_path):
    first = store.import_path(CSV_DIR)
    copy = tmp_path / "csv"
    shutil.copytree(CSV_DIR, copy)
    # LF line endings keep every business value but change the delivered bytes.
    target = copy / "orders.csv"
    target.write_bytes(target.read_bytes().replace(b"\r\n", b"\n"))
    second = store.import_path(copy)
    assert second["content_digest"] == first["content_digest"]
    assert second["source_sha256"] != first["source_sha256"]
    assert second["delivery_recorded"]


def test_content_digest_excludes_source_provenance():
    from finance_exception_investigator.core import import_csv

    bundle = import_csv(CSV_DIR)
    assert "source" in bundle["orders"][0]
    assert content_digest(bundle) == content_digest(json.loads(JSON_PATH.read_text()))


def test_file_backed_store_persists_across_connections(tmp_path):
    database = tmp_path / "store.db"
    one = BundleStore(database)
    first = one.import_path(JSON_PATH)
    one.close()
    two = BundleStore(database)
    again = two.import_path(JSON_PATH)
    two.close()
    assert not again["bundle_created"] and not again["delivery_recorded"]
    assert again["content_digest"] == first["content_digest"]
