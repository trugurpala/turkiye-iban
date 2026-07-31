from __future__ import annotations

import argparse
import csv
import json
import os
import sqlite3
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = ROOT / "data" / "source" / "institutions.json"
GENERATED_PATHS = (
    Path("data/tr-banks.json"),
    Path("data/tr-banks.csv"),
    Path("data/tr-banks.sql"),
    Path("data/tr-banks.sqlite"),
    Path("data/source-manifest.json"),
    Path("fixtures/valid.synthetic.json"),
    Path("fixtures/invalid.synthetic.json"),
    Path("fixtures/lookup.synthetic.json"),
    Path("packages/typescript/data/tr-banks.json"),
    Path("packages/typescript/src/generated/banks.ts"),
)

SQL_COLUMNS = (
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


def load_canonical() -> dict[str, Any]:
    return json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))


def normalized_institutions(canonical: dict[str, Any]) -> list[dict[str, Any]]:
    sources = {source["id"]: source for source in canonical["sources"]}
    institutions: list[dict[str, Any]] = []
    for raw in sorted(canonical["institutions"], key=lambda item: item["code"]):
        institution = {
            "code": raw["code"],
            "rawCode": raw["rawCode"],
            "nameOfficial": raw["nameOfficial"],
            "nameShort": raw["nameShort"],
            "type": raw["type"],
            "status": raw["status"],
            "systems": sorted(raw["systems"]),
            "codeEvidence": sorted(raw["codeEvidence"]),
            "aliases": sorted(raw["aliases"]),
            "sources": [
                {
                    "id": source_id,
                    "url": sources[source_id]["url"],
                    "retrievedAt": sources[source_id]["retrievedAt"],
                    "classification": sources[source_id]["classification"],
                    "usage": sources[source_id]["usage"],
                    "evidenceScope": sorted(sources[source_id]["evidenceScope"]),
                }
                for source_id in sorted(raw["sourceIds"])
            ],
            "lastVerifiedAt": raw["lastVerifiedAt"],
        }
        institutions.append(institution)
    return institutions


def distribution_payload(canonical: dict[str, Any], institutions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "$schema": "./schema/tr-banks.schema.json",
        "country": canonical["country"],
        "ibanFormat": canonical["ibanFormat"],
        # Kept for v0.x compatibility. It is the reviewed snapshot date, not the build clock.
        "generatedAt": canonical["dataVersion"],
        "dataVersion": canonical["dataVersion"],
        "sourcePolicy": "Official-source-first. See DATA_SOURCES.md and DATA_UPDATE_POLICY.md.",
        "providers": institutions,
    }


def source_manifest(canonical: dict[str, Any]) -> dict[str, Any]:
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


def sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def record_values(institution: dict[str, Any]) -> tuple[str, ...]:
    return (
        str(institution["code"]),
        str(institution["rawCode"]),
        str(institution["nameOfficial"]),
        str(institution["nameShort"]),
        str(institution["type"]),
        str(institution["status"]),
        "|".join(institution["systems"]),
        "|".join(institution["codeEvidence"]),
        "|".join(institution["aliases"]),
        json.dumps(institution["sources"], ensure_ascii=False, separators=(",", ":")),
        str(institution["lastVerifiedAt"]),
    )


def render_sql(institutions: list[dict[str, Any]]) -> str:
    lines = [
        "CREATE TABLE IF NOT EXISTS tr_iban_providers (",
        "  code TEXT PRIMARY KEY,",
        "  raw_code TEXT NOT NULL,",
        "  name_official TEXT NOT NULL,",
        "  name_short TEXT NOT NULL,",
        "  type TEXT NOT NULL,",
        "  status TEXT NOT NULL,",
        "  systems TEXT NOT NULL,",
        "  code_evidence TEXT NOT NULL,",
        "  aliases TEXT NOT NULL,",
        "  sources_json TEXT NOT NULL,",
        "  last_verified_at TEXT NOT NULL",
        ");",
        "",
    ]
    for institution in institutions:
        values = ", ".join(sql_string(value) for value in record_values(institution))
        lines.append(f"INSERT INTO tr_iban_providers VALUES ({values});")
    return "\n".join(lines) + "\n"


def write_sqlite(path: Path, institutions: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(".sqlite.tmp")
    temporary_path.unlink(missing_ok=True)
    connection = sqlite3.connect(temporary_path)
    try:
        connection.execute("PRAGMA page_size = 4096")
        connection.execute("PRAGMA journal_mode = OFF")
        connection.execute("PRAGMA synchronous = OFF")
        connection.execute(
            """
            CREATE TABLE tr_iban_providers (
              code TEXT PRIMARY KEY,
              raw_code TEXT NOT NULL,
              name_official TEXT NOT NULL,
              name_short TEXT NOT NULL,
              type TEXT NOT NULL,
              status TEXT NOT NULL,
              systems TEXT NOT NULL,
              code_evidence TEXT NOT NULL,
              aliases TEXT NOT NULL,
              sources_json TEXT NOT NULL,
              last_verified_at TEXT NOT NULL
            ) WITHOUT ROWID
            """
        )
        placeholders = ", ".join("?" for _ in SQL_COLUMNS)
        connection.executemany(
            f"INSERT INTO tr_iban_providers ({', '.join(SQL_COLUMNS)}) VALUES ({placeholders})",
            [record_values(institution) for institution in institutions],
        )
        connection.execute("PRAGMA user_version = 1")
        connection.commit()
        connection.execute("VACUUM")
    finally:
        connection.close()
    os.replace(temporary_path, path)


def compute_check_digits(provider_code: str, account_number: str, reserve_digit: str = "0") -> str:
    rearranged = provider_code + reserve_digit + account_number + "TR00"
    numeric = "".join(str(ord(character) - 55) if character.isalpha() else character for character in rearranged)
    remainder = 0
    for character in numeric:
        remainder = (remainder * 10 + int(character)) % 97
    return str(98 - remainder).zfill(2)


def build_iban(provider_code: str, account_number: str) -> str:
    return "TR" + compute_check_digits(provider_code, account_number) + provider_code + "0" + account_number


def fixture_payloads(institutions: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], ...]:
    valid = []
    for index, institution in enumerate(institutions, start=1):
        account_number = ("9999" + str(index).zfill(12))[-16:]
        valid.append(
            {
                "iban": build_iban(institution["code"], account_number),
                "providerCode": institution["code"],
                "rawCode": institution["rawCode"],
                "providerName": institution["nameOfficial"],
                "synthetic": True,
            }
        )
    invalid = [
        {"iban": "TR000004600000000000000026", "reason": "invalid_check_digits", "synthetic": True},
        {"iban": "DE330004600000000000000026", "reason": "invalid_country", "synthetic": True},
        {"iban": "TR33000460000000000000002", "reason": "invalid_length", "synthetic": True},
        {"iban": "TR51000460999900000000001!", "reason": "invalid_character", "synthetic": True},
        {"iban": "TR510004619999000000000011", "reason": "invalid_reserve_digit", "synthetic": True},
    ]
    lookup = [
        {
            "iban": valid[0]["iban"],
            "providerCode": valid[0]["providerCode"],
            "providerStatus": "known",
            "synthetic": True,
        },
        {
            "iban": build_iban("00046", "ABC123DEF456GHIJ"),
            "providerCode": "00046",
            "providerStatus": "known",
            "synthetic": True,
        },
        {
            "iban": build_iban("99999", "ABC123DEF456GHIJ"),
            "providerCode": "99999",
            "providerStatus": "unknown",
            "synthetic": True,
        },
    ]
    return valid, invalid, lookup


def write_text_lf(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def write_json(path: Path, value: Any) -> None:
    write_text_lf(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def write_outputs(output_root: Path) -> None:
    canonical = load_canonical()
    institutions = normalized_institutions(canonical)
    payload = distribution_payload(canonical, institutions)

    write_json(output_root / "data/tr-banks.json", payload)
    write_json(output_root / "packages/typescript/data/tr-banks.json", payload)
    write_json(output_root / "data/source-manifest.json", source_manifest(canonical))

    csv_path = output_root / "data/tr-banks.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "code",
                "rawCode",
                "nameOfficial",
                "nameShort",
                "type",
                "status",
                "systems",
                "codeEvidence",
                "aliases",
                "sourceIds",
                "lastVerifiedAt",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        for institution in institutions:
            writer.writerow(
                {
                    "code": institution["code"],
                    "rawCode": institution["rawCode"],
                    "nameOfficial": institution["nameOfficial"],
                    "nameShort": institution["nameShort"],
                    "type": institution["type"],
                    "status": institution["status"],
                    "systems": "|".join(institution["systems"]),
                    "codeEvidence": "|".join(institution["codeEvidence"]),
                    "aliases": "|".join(institution["aliases"]),
                    "sourceIds": "|".join(source["id"] for source in institution["sources"]),
                    "lastVerifiedAt": institution["lastVerifiedAt"],
                }
            )

    sql_path = output_root / "data/tr-banks.sql"
    write_text_lf(sql_path, render_sql(institutions))
    write_sqlite(output_root / "data/tr-banks.sqlite", institutions)

    valid, invalid, lookup = fixture_payloads(institutions)
    write_json(output_root / "fixtures/valid.synthetic.json", valid)
    write_json(output_root / "fixtures/invalid.synthetic.json", invalid)
    write_json(output_root / "fixtures/lookup.synthetic.json", lookup)

    generated_dir = output_root / "packages/typescript/src/generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    body = json.dumps(institutions, ensure_ascii=False, indent=2)
    write_text_lf(
        generated_dir / "banks.ts",
        "/* This file is generated by scripts/generate-data.py. Do not edit by hand. */\n"
        f"export const dataVersion = {json.dumps(canonical['dataVersion'])} as const;\n"
        f"export const providers = {body} as const;\n"
        "export type GeneratedProvider = (typeof providers)[number];\n",
    )


def check_generated_files() -> int:
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_root = Path(temporary_directory)
        write_outputs(temporary_root)
        drift = [
            str(relative_path)
            for relative_path in GENERATED_PATHS
            if not (ROOT / relative_path).is_file()
            or (ROOT / relative_path).read_bytes() != (temporary_root / relative_path).read_bytes()
        ]
    if drift:
        print("Generated file drift detected:")
        print("\n".join(f"- {path}" for path in drift))
        print("Run `npm run generate:data` and commit the generated outputs.")
        return 1
    print(f"Generated files are up to date: {len(GENERATED_PATHS)} artifacts")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Turkish IBAN artifacts from canonical data.")
    parser.add_argument("--check", action="store_true", help="Fail when generated files differ without writing them.")
    args = parser.parse_args()

    if args.check:
        return check_generated_files()
    write_outputs(ROOT)
    institution_count = len(load_canonical()["institutions"])
    print(f"Generated {institution_count} institutions from {CANONICAL_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
