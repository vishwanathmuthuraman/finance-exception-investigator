"""Local SQLite store for immutable source deliveries and normalized bundle identity."""

import hashlib
import sqlite3
from pathlib import Path

from .common import ContractError, canonical, digest, read_json
from .core import KINDS, import_csv, validate_bundle


class ConflictError(ContractError):
    """The bundle ID already exists with different canonical content."""


SCHEMA = """
CREATE TABLE IF NOT EXISTS bundles (
    bundle_id TEXT PRIMARY KEY,
    content_digest TEXT NOT NULL,
    normalized_json TEXT NOT NULL
) STRICT;
CREATE TABLE IF NOT EXISTS deliveries (
    source_sha256 TEXT PRIMARY KEY,
    bundle_id TEXT NOT NULL REFERENCES bundles(bundle_id),
    source_kind TEXT NOT NULL CHECK (source_kind IN ('json', 'csv')),
    source_bytes BLOB NOT NULL
) STRICT;
"""


def content_digest(bundle):
    """Identity of business content; physical provenance (`source`) is excluded."""
    return digest(_strip_source(bundle))


def _csv_files(directory):
    return [Path(directory) / (kind + ".csv") for kind in KINDS]


def source_sha256(path):
    """SHA-256 of the exact delivered bytes (CSV: ordered per-file hashes and names)."""
    path = Path(path)
    if path.is_dir():
        parts = [[p.name, hashlib.sha256(p.read_bytes()).hexdigest()] for p in _csv_files(path)]
        return hashlib.sha256(canonical(parts).encode()).hexdigest()
    return hashlib.sha256(path.read_bytes()).hexdigest()


class BundleStore:
    def __init__(self, database=":memory:"):
        self.db = sqlite3.connect(database)
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript(SCHEMA)

    def close(self):
        self.db.close()

    def import_path(self, path):
        """Import a JSON file or CSV directory; return identity and whether anything was new."""
        path = Path(path)
        is_csv = path.is_dir()
        bundle = validate_bundle(import_csv(path) if is_csv else read_json(path))
        source_hash = source_sha256(path)
        if is_csv:
            raw = canonical([[p.name, p.read_bytes().hex()] for p in _csv_files(path)]).encode()
        else:
            raw = path.read_bytes()
        return self._commit(bundle, source_hash, "csv" if is_csv else "json", raw)

    def _commit(self, bundle, source_hash, kind, raw):
        identity = content_digest(bundle)
        with self.db:
            row = self.db.execute(
                "SELECT content_digest FROM bundles WHERE bundle_id = ?", (bundle["bundle_id"],)
            ).fetchone()
            if row is not None and row[0] != identity:
                raise ConflictError("bundle ID exists with different content; use a new version")
            created = row is None
            if created:
                self.db.execute(
                    "INSERT INTO bundles VALUES (?, ?, ?)",
                    (bundle["bundle_id"], identity, canonical(_strip_source(bundle))),
                )
            cursor = self.db.execute(
                "INSERT OR IGNORE INTO deliveries VALUES (?, ?, ?, ?)",
                (source_hash, bundle["bundle_id"], kind, raw),
            )
        return {
            "bundle_id": bundle["bundle_id"],
            "content_digest": identity,
            "source_sha256": source_hash,
            "bundle_created": created,
            "delivery_recorded": cursor.rowcount == 1,
        }

    def delivery_count(self, bundle_id):
        return self.db.execute(
            "SELECT COUNT(*) FROM deliveries WHERE bundle_id = ?", (bundle_id,)
        ).fetchone()[0]

    def source_bytes(self, source_hash):
        row = self.db.execute(
            "SELECT source_bytes FROM deliveries WHERE source_sha256 = ?", (source_hash,)
        ).fetchone()
        return None if row is None else row[0]


def _strip_source(bundle):
    return {
        key: ([{k: v for k, v in row.items() if k != "source"} for row in value])
        if key in KINDS
        else value
        for key, value in bundle.items()
    }
