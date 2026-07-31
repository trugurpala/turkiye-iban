from __future__ import annotations

import csv
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
DATABASE_COLUMNS = (
    "code",
    "raw_code",
    "name_official",
    "name_short",
    "type",
    "status",
    "systems",
    "code_evidence",
    "aliases",
    "sources_json",
    "last_verified_at",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_schema(value: Any, schema: dict[str, Any], label: str) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(value), key=lambda error: list(error.absolute_path))
    require(
        not errors,
        "\n".join(f"{label} {list(error.absolute_path)}: {error.message}" for error in errors),
    )


def validate_mod97(iban: str) -> bool:
    rearranged = iban[4:] + iban[:4]
    numeric = "".join(str(ord(character) - 55) if character.isalpha() else character for character in rearranged)
    remainder = 0
    for character in numeric:
        if not character.isdigit():
            return False
        remainder = (remainder * 10 + int(character)) % 97
    return remainder == 1


def expected_providers(canonical: dict[str, Any]) -> list[dict[str, Any]]:
    source_map = {source["id"]: source for source in canonical["sources"]}
    providers = []
    for institution in canonical["institutions"]:
        providers.append(
            {
                "code": institution["code"],
                "rawCode": institution["rawCode"],
                "nameOfficial": institution["nameOfficial"],
                "nameShort": institution["nameShort"],
                "type": institution["type"],
                "status": institution["status"],
                "systems": sorted(institution["systems"]),
                "codeEvidence": sorted(institution["codeEvidence"]),
                "aliases": sorted(institution["aliases"]),
                "sources": [
                    {
                        "id": source_id,
                        "url": source_map[source_id]["url"],
                        "retrievedAt": source_map[source_id]["retrievedAt"],
                        "classification": source_map[source_id]["classification"],
                        "usage": source_map[source_id]["usage"],
                        "evidenceScope": sorted(source_map[source_id]["evidenceScope"]),
                    }
                    for source_id in sorted(institution["sourceIds"])
                ],
                "lastVerifiedAt": institution["lastVerifiedAt"],
            }
        )
    return providers


def expected_manifest(canonical: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "./schema/source-manifest.schema.json",
        "generatedAt": canonical["dataVersion"],
        "sources": [
            {
                "id": source["id"],
                "url": source["url"],
                "retrievedAt": source["retrievedAt"],
                "sha256": source["sha256"],
                "publisher": source["publisher"],
                "title": source["title"],
                "classification": source["classification"],
                "usage": source["usage"],
                "evidenceScope": sorted(source["evidenceScope"]),
                "extractionMethod": source["extractionMethod"],
                "redistributionStatus": source["redistributionStatus"],
            }
            for source in sorted(canonical["sources"], key=lambda item: item["id"])
        ],
    }


def database_values(provider: dict[str, Any]) -> tuple[str, ...]:
    return (
        provider["code"],
        provider["rawCode"],
        provider["nameOfficial"],
        provider["nameShort"],
        provider["type"],
        provider["status"],
        "|".join(provider["systems"]),
        "|".join(provider["codeEvidence"]),
        "|".join(provider["aliases"]),
        json.dumps(provider["sources"], ensure_ascii=False, separators=(",", ":")),
        provider["lastVerifiedAt"],
    )


def read_database_rows(connection: sqlite3.Connection) -> list[tuple[str, ...]]:
    columns = ", ".join(DATABASE_COLUMNS)
    return connection.execute(
        f"SELECT {columns} FROM tr_iban_providers ORDER BY code"
    ).fetchall()


def validate_cross_format_outputs(providers: list[dict[str, Any]]) -> None:
    expected_rows = [database_values(provider) for provider in providers]

    with (ROOT / "data/tr-banks.csv").open(encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    require(len(csv_rows) == len(providers), "CSV row count differs from JSON provider count")
    for row, provider in zip(csv_rows, providers, strict=True):
        expected = {
            "code": provider["code"],
            "rawCode": provider["rawCode"],
            "nameOfficial": provider["nameOfficial"],
            "nameShort": provider["nameShort"],
            "type": provider["type"],
            "status": provider["status"],
            "systems": "|".join(provider["systems"]),
            "codeEvidence": "|".join(provider["codeEvidence"]),
            "aliases": "|".join(provider["aliases"]),
            "sourceIds": "|".join(source["id"] for source in provider["sources"]),
            "lastVerifiedAt": provider["lastVerifiedAt"],
        }
        require(row == expected, f"CSV record differs for {provider['code']}")

    sql_text = (ROOT / "data/tr-banks.sql").read_text(encoding="utf-8")
    connection = sqlite3.connect(":memory:")
    try:
        connection.executescript(sql_text)
        sql_rows = read_database_rows(connection)
    finally:
        connection.close()
    require(sql_rows == expected_rows, "SQL records differ from JSON records")

    connection = sqlite3.connect(ROOT / "data/tr-banks.sqlite")
    try:
        sqlite_rows = read_database_rows(connection)
    finally:
        connection.close()
    require(sqlite_rows == expected_rows, "SQLite records differ from JSON records")


def validate_fixtures(provider_codes: set[str], provider_count: int) -> None:
    valid_fixtures = load_json(ROOT / "fixtures/valid.synthetic.json")
    invalid_fixtures = load_json(ROOT / "fixtures/invalid.synthetic.json")
    lookup_fixtures = load_json(ROOT / "fixtures/lookup.synthetic.json")
    for label, fixtures in (
        ("valid", valid_fixtures),
        ("invalid", invalid_fixtures),
        ("lookup", lookup_fixtures),
    ):
        require(isinstance(fixtures, list) and fixtures, f"{label} fixtures must be a non-empty list")
        require(
            all(fixture.get("synthetic") is True for fixture in fixtures),
            f"Every {label} fixture must be explicitly synthetic",
        )

    require(len(valid_fixtures) == provider_count, "Valid fixture count must match provider count")
    seen_ibans: set[str] = set()
    for fixture in valid_fixtures:
        iban = fixture["iban"]
        require(iban not in seen_ibans, f"Duplicate fixture IBAN {iban}")
        seen_ibans.add(iban)
        require(re.fullmatch(r"TR[A-Z0-9]{24}", iban) is not None, f"Invalid fixture shape {iban}")
        require(validate_mod97(iban), f"Invalid fixture checksum {iban}")
        require(fixture["providerCode"] in provider_codes, f"Unknown fixture provider {iban}")

    invalid_reasons = {fixture["reason"] for fixture in invalid_fixtures}
    required_reasons = {
        "invalid_check_digits",
        "invalid_country",
        "invalid_length",
        "invalid_character",
        "invalid_reserve_digit",
    }
    require(required_reasons.issubset(invalid_reasons), "Invalid fixture set is missing required reasons")

    lookup_statuses = {fixture["providerStatus"] for fixture in lookup_fixtures}
    require(lookup_statuses == {"known", "unknown"}, "Lookup fixtures must cover known and unknown")
    for fixture in lookup_fixtures:
        iban = fixture["iban"]
        require(validate_mod97(iban), f"Invalid lookup fixture checksum {iban}")
        if fixture["providerStatus"] == "known":
            require(fixture["providerCode"] in provider_codes, f"Known lookup code missing for {iban}")
        else:
            require(fixture["providerCode"] not in provider_codes, f"Unknown lookup code exists for {iban}")


def main() -> int:
    canonical = load_json(ROOT / "data/source/institutions.json")
    canonical_schema = load_json(ROOT / "data/schema/institutions-source.schema.json")
    validate_schema(canonical, canonical_schema, "canonical source")

    source_ids = [source["id"] for source in canonical["sources"]]
    require(source_ids == sorted(source_ids), "Canonical sources must be sorted by id")
    require(len(source_ids) == len(set(source_ids)), "Canonical source ids must be unique")
    source_id_set = set(source_ids)

    institutions = canonical["institutions"]
    codes = [institution["code"] for institution in institutions]
    require(codes == sorted(codes), "Canonical institution codes must be sorted")
    require(len(codes) == len(set(codes)), "Canonical institution codes must be unique")
    require(len(codes) >= 50, "Expected at least 50 reviewed payment-system participants")
    used_source_ids: set[str] = set()
    for institution in institutions:
        require(institution["rawCode"].zfill(5) == institution["code"], f"rawCode/code mismatch for {institution['code']}")
        require(institution["sourceIds"], f"Institution {institution['code']} has no source")
        require(set(institution["sourceIds"]).issubset(source_id_set), f"Unknown source id for {institution['code']}")
        used_source_ids.update(institution["sourceIds"])
    for source in canonical["sources"]:
        if source["usage"] != "monitor_only":
            require(source["id"] in used_source_ids, f"Non-monitor source {source['id']} contributes no records")

    payload = load_json(ROOT / "data/tr-banks.json")
    distribution_schema = load_json(ROOT / "data/schema/tr-banks.schema.json")
    validate_schema(payload, distribution_schema, "distribution JSON")
    require(payload == load_json(ROOT / "packages/typescript/data/tr-banks.json"), "Package JSON data copy is out of sync")
    require(payload["dataVersion"] == canonical["dataVersion"], "Distribution dataVersion differs from canonical source")
    require(payload["generatedAt"] == canonical["dataVersion"], "generatedAt must be deterministic")

    providers = payload["providers"]
    require(providers == expected_providers(canonical), "Distribution JSON differs from canonical source")
    for provider in providers:
        require("ibanEligible" not in provider, f"Unsupported ibanEligible claim for {provider['code']}")
        require(provider["codeEvidence"] == ["payment_system_participant"], f"Invalid code evidence for {provider['code']}")

    manifest = load_json(ROOT / "data/source-manifest.json")
    manifest_schema = load_json(ROOT / "data/schema/source-manifest.schema.json")
    validate_schema(manifest, manifest_schema, "source manifest")
    require(manifest == expected_manifest(canonical), "Source manifest differs from canonical source catalog")

    validate_cross_format_outputs(providers)
    validate_fixtures(set(codes), len(codes))
    print(f"Data validation passed: {len(codes)} institutions, JSON/CSV/SQL/SQLite parity confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
