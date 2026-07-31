from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_mod97(iban: str) -> bool:
    rearranged = iban[4:] + iban[:4]
    numeric = "".join(str(ord(char) - 55) if char.isalpha() else char for char in rearranged)
    remainder = 0
    for char in numeric:
        if not char.isdigit():
            return False
        remainder = (remainder * 10 + int(char)) % 97
    return remainder == 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    data_path = ROOT / "data" / "tr-banks.json"
    package_data_path = ROOT / "packages" / "typescript" / "data" / "tr-banks.json"
    csv_path = ROOT / "data" / "tr-banks.csv"
    sql_path = ROOT / "data" / "tr-banks.sql"
    schema_path = ROOT / "data" / "schema" / "tr-banks.schema.json"
    valid_fixture_path = ROOT / "fixtures" / "valid.synthetic.json"
    invalid_fixture_path = ROOT / "fixtures" / "invalid.synthetic.json"

    payload = load_json(data_path)
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    require(not errors, "\n".join(error.message for error in errors))

    require(payload == load_json(package_data_path), "Package JSON data copy is out of sync")
    require(isinstance(payload, dict), "Data payload must be an object")
    providers = payload["providers"]
    require(isinstance(providers, list), "providers must be a list")
    require(len(providers) >= 100, "Expected at least 100 providers")

    codes = [provider["code"] for provider in providers]
    require(codes == sorted(codes), "Provider codes must be sorted")
    require(len(codes) == len(set(codes)), "Provider codes must be unique")

    provider_codes = set()
    for provider in providers:
        code = provider["code"]
        raw_code = provider["rawCode"]
        provider_codes.add(code)
        require(re.fullmatch(r"\d{5}", code) is not None, f"Invalid provider code {code}")
        require(raw_code.zfill(5) == code, f"rawCode/code mismatch for {code}")
        require(provider["sources"], f"Provider {code} has no source")
        for source in provider["sources"]:
            require(source["url"].startswith("https://"), f"Provider {code} has non-HTTPS source")

    with csv_path.open(encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    require(len(csv_rows) == len(providers), "CSV row count differs from JSON provider count")
    require([row["code"] for row in csv_rows] == codes, "CSV provider order differs from JSON")

    sql_text = sql_path.read_text(encoding="utf-8")
    insert_count = len(re.findall(r"^INSERT INTO tr_iban_providers VALUES", sql_text, flags=re.MULTILINE))
    require(insert_count == len(providers), "SQL insert count differs from JSON provider count")

    valid_fixtures = load_json(valid_fixture_path)
    invalid_fixtures = load_json(invalid_fixture_path)
    require(isinstance(valid_fixtures, list), "Valid fixtures must be a list")
    require(isinstance(invalid_fixtures, list), "Invalid fixtures must be a list")
    require(len(valid_fixtures) == len(providers), "Valid fixture count must match provider count")

    seen_ibans: set[str] = set()
    for fixture in valid_fixtures:
        iban = fixture["iban"]
        require(fixture.get("synthetic") is True, f"Fixture {iban} must be marked synthetic")
        require(iban not in seen_ibans, f"Duplicate fixture IBAN {iban}")
        seen_ibans.add(iban)
        require(re.fullmatch(r"TR\d{24}", iban) is not None, f"Invalid fixture shape {iban}")
        require(validate_mod97(iban), f"Invalid fixture checksum {iban}")
        require(fixture["providerCode"] in provider_codes, f"Unknown fixture provider {iban}")

    invalid_reasons = {fixture["reason"] for fixture in invalid_fixtures}
    require(
        {
            "invalid_check_digits",
            "invalid_country",
            "invalid_length",
            "invalid_character",
            "invalid_reserve_digit",
            "unknown_provider_code",
        }.issubset(invalid_reasons),
        "Invalid fixture set is missing required reasons",
    )

    print(f"Data validation passed: {len(providers)} providers, {len(valid_fixtures)} valid fixtures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
