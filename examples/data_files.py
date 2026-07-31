from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
payload = json.loads((ROOT / "data/tr-banks.json").read_text(encoding="utf-8"))

with (ROOT / "data/tr-banks.csv").open(encoding="utf-8", newline="") as handle:
    csv_rows = list(csv.DictReader(handle))

connection = sqlite3.connect(ROOT / "data/tr-banks.sqlite")
try:
    sqlite_count = connection.execute("SELECT COUNT(*) FROM tr_iban_providers").fetchone()[0]
    provider = connection.execute(
        "SELECT code, name_official FROM tr_iban_providers WHERE code = ?",
        ("00046",),
    ).fetchone()
finally:
    connection.close()

assert len(payload["providers"]) == len(csv_rows) == sqlite_count
assert provider == ("00046", "AKBANK T.A.Ş.")
print(f"Data example passed: {sqlite_count} institutions, provider {provider[0]}")
