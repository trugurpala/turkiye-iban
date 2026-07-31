from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from datetime import date
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
GENERATED_DATE = date.today().isoformat()

SOURCES = {
    "tcmb-payment-systems-participants-2026": {
        "url": "https://www.tcmb.gov.tr/wps/wcm/connect/9fa62a85-5b6d-46c5-9b01-eb461d43723d/TCMB%2B%C3%96deme%2BSistemleri%2BKat%C4%B1l%C4%B1mc%C4%B1lar%C4%B1%2B%282025%29.pdf?MOD=AJPERES",
        "system": "TCMB_PAYMENT_SYSTEMS",
        "evidence": "payment_system_participant",
    },
    "tcmb-active-payment-institutions": {
        "url": "https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb%2Btr/main%2Bmenu/temel%2Bfaaliyetler/odeme%2Bhizmetleri/odeme%2Bkuruluslari",
        "system": "TCMB_PAYMENT_SERVICES_REGISTRY",
    },
    "tcmb-active-electronic-money-institutions": {
        "url": "https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb%2Btr/main%2Bmenu/temel%2Bfaaliyetler/odeme%2Bhizmetleri/elektronik%2Bpara%2Bkuruluslari",
        "system": "TCMB_PAYMENT_SERVICES_REGISTRY",
    },
}


@dataclass
class Provider:
    code: str
    rawCode: str
    nameOfficial: str
    nameShort: str
    type: str
    status: str = "active"
    systems: set[str] = field(default_factory=set)
    codeEvidence: set[str] = field(default_factory=set)
    aliases: set[str] = field(default_factory=set)
    sources: list[dict[str, str]] = field(default_factory=list)
    lastVerifiedAt: str = GENERATED_DATE

    def to_json(self) -> dict[str, object]:
        return {
            "code": self.code,
            "rawCode": self.rawCode,
            "nameOfficial": self.nameOfficial,
            "nameShort": self.nameShort,
            "type": self.type,
            "status": self.status,
            "systems": sorted(self.systems),
            "codeEvidence": sorted(self.codeEvidence),
            "aliases": sorted(self.aliases),
            "sources": self.sources,
            "lastVerifiedAt": self.lastVerifiedAt,
        }


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.tables: list[list[list[str]]] = []
        self.current_table: list[list[str]] = []
        self.current_row: list[str] = []
        self.current_cell: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table":
            self.in_table = True
            self.current_table = []
        elif self.in_table and tag == "tr":
            self.in_row = True
            self.current_row = []
        elif self.in_row and tag in {"td", "th"}:
            self.in_cell = True
            self.current_cell = []
        elif self.in_cell and tag in {"br", "p"}:
            self.current_cell.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self.in_cell:
            text = " ".join("".join(self.current_cell).split())
            self.current_row.append(unescape(text))
            self.in_cell = False
        elif tag == "tr" and self.in_row:
            if self.current_row:
                self.current_table.append(self.current_row)
            self.in_row = False
        elif tag == "table" and self.in_table:
            self.tables.append(self.current_table)
            self.current_table = []
            self.in_table = False

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.current_cell.append(data)


def fetch_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "turkiye-iban-data-generator/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def short_name(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name).strip()
    replacements = [
        r"\s+T\.A\.O\.$",
        r"\s+T\.A\.Ş\.$",
        r"\s+A\.Ş\.$",
        r"\s+A\.S\.$",
        r"\s+N\.A\.$",
    ]
    for pattern in replacements:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def source_ref(source_id: str) -> dict[str, str]:
    return {
        "id": source_id,
        "url": SOURCES[source_id]["url"],
        "retrievedAt": GENERATED_DATE,
    }


def provider_type_from_payment_systems(raw_code: str, name: str) -> str:
    if raw_code == "0001":
        return "central_bank"
    if raw_code == "0807":
        return "postal_operator"
    if raw_code in {"0806", "0132"}:
        return "financial_market_infrastructure"
    return "bank"


def add_provider(providers: dict[str, Provider], raw_code: str, name: str, kind: str, source_id: str) -> None:
    raw = raw_code.strip()
    code = raw.zfill(5)
    official_name = " ".join(name.strip().split())
    provider = providers.get(code)
    if provider is None:
        provider = Provider(
            code=code,
            rawCode=raw,
            nameOfficial=official_name,
            nameShort=short_name(official_name),
            type=kind,
        )
        providers[code] = provider
    else:
        provider.aliases.add(official_name)
    provider.systems.add(SOURCES[source_id]["system"])
    provider.codeEvidence.add(SOURCES[source_id]["evidence"])
    provider.sources.append(source_ref(source_id))


def enrich_provider_from_registry(
    providers: dict[str, Provider], raw_code: str, name: str, kind: str, source_id: str
) -> None:
    """Enrich an already verified participant without promoting registry-only codes."""
    provider = providers.get(raw_code.strip().zfill(5))
    if provider is None:
        return

    official_name = " ".join(name.strip().split())
    if official_name != provider.nameOfficial:
        provider.aliases.add(official_name)
    provider.type = kind
    provider.systems.add(SOURCES[source_id]["system"])
    provider.sources.append(source_ref(source_id))


def parse_payment_systems_pdf(pdf_bytes: bytes) -> list[tuple[str, str]]:
    pdf_path = ROOT / "work" / "tcmb-payment-systems-participants.pdf"
    pdf_path.parent.mkdir(exist_ok=True)
    pdf_path.write_bytes(pdf_bytes)
    reader = PdfReader(str(pdf_path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    rows: list[tuple[str, str]] = []
    for line in text.splitlines():
        match = re.match(r"^\s*\d+\s+(\d{4})\s+(.+?)(?:\s+\(\*\))?\s*$", line)
        if match:
            rows.append((match.group(1), match.group(2).strip()))
    if len(rows) < 50:
        raise RuntimeError(f"Expected at least 50 payment-system rows, found {len(rows)}")
    return rows


def parse_first_html_table(html_bytes: bytes) -> list[list[str]]:
    parser = TableParser()
    parser.feed(html_bytes.decode("utf-8", errors="ignore"))
    if not parser.tables:
        raise RuntimeError("No HTML table found")
    return parser.tables[0]


def parse_institution_rows(html_bytes: bytes) -> list[tuple[str, str]]:
    rows = []
    for row in parse_first_html_table(html_bytes):
        if len(row) >= 3 and row[0].isdigit() and row[1].isdigit():
            rows.append((row[1], row[2]))
    if not rows:
        raise RuntimeError("No institution rows found")
    return rows


def sql_string(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def write_json_csv_sql(providers: list[dict[str, object]]) -> None:
    data_dir = ROOT / "data"
    package_data_dir = ROOT / "packages" / "typescript" / "data"
    data_dir.mkdir(exist_ok=True)
    package_data_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "$schema": "./schema/tr-banks.schema.json",
        "country": "TR",
        "ibanFormat": {
            "length": 26,
            "providerCodeLength": 5,
            "reserveLength": 1,
            "accountLength": 16,
        },
        "generatedAt": GENERATED_DATE,
        "dataVersion": GENERATED_DATE,
        "sourcePolicy": "Official-source-first. See DATA_SOURCES.md and DATA_UPDATE_POLICY.md.",
        "providers": providers,
    }

    json_text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    (data_dir / "tr-banks.json").write_text(json_text, encoding="utf-8")
    (package_data_dir / "tr-banks.json").write_text(json_text, encoding="utf-8")

    csv_path = data_dir / "tr-banks.csv"
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
        )
        writer.writeheader()
        for provider in providers:
            writer.writerow(
                {
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
            )

    sql_lines = [
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
    for provider in providers:
        values = [
            sql_string(str(provider["code"])),
            sql_string(str(provider["rawCode"])),
            sql_string(str(provider["nameOfficial"])),
            sql_string(str(provider["nameShort"])),
            sql_string(str(provider["type"])),
            sql_string(str(provider["status"])),
            sql_string("|".join(provider["systems"])),
            sql_string("|".join(provider["codeEvidence"])),
            sql_string("|".join(provider["aliases"])),
            sql_string(json.dumps(provider["sources"], ensure_ascii=False, separators=(",", ":"))),
            sql_string(str(provider["lastVerifiedAt"])),
        ]
        sql_lines.append(f"INSERT INTO tr_iban_providers VALUES ({', '.join(values)});")
    (data_dir / "tr-banks.sql").write_text("\n".join(sql_lines) + "\n", encoding="utf-8")


def compute_check_digits(provider_code: str, account_number: str, reserve_digit: str = "0") -> str:
    bban = provider_code + reserve_digit + account_number
    rearranged = bban + "TR00"
    numeric = "".join(str(ord(ch) - 55) if ch.isalpha() else ch for ch in rearranged)
    remainder = 0
    for char in numeric:
        remainder = (remainder * 10 + int(char)) % 97
    return str(98 - remainder).zfill(2)


def build_iban(provider_code: str, account_number: str) -> str:
    return "TR" + compute_check_digits(provider_code, account_number) + provider_code + "0" + account_number


def write_fixtures(providers: list[dict[str, object]]) -> None:
    fixture_dir = ROOT / "fixtures"
    fixture_dir.mkdir(exist_ok=True)
    valid = []
    for index, provider in enumerate(providers, start=1):
        account_number = ("9999" + str(index).zfill(12))[-16:]
        iban = build_iban(str(provider["code"]), account_number)
        valid.append(
            {
                "iban": iban,
                "providerCode": provider["code"],
                "rawCode": provider["rawCode"],
                "providerName": provider["nameOfficial"],
                "synthetic": True,
            }
        )
    invalid = [
        {"iban": "TR000004600000000000000026", "reason": "invalid_check_digits"},
        {"iban": "DE330004600000000000000026", "reason": "invalid_country"},
        {"iban": "TR33000460000000000000002", "reason": "invalid_length"},
        {"iban": "TR51000460999900000000001!", "reason": "invalid_character"},
        {"iban": "TR510004619999000000000011", "reason": "invalid_reserve_digit"},
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
    (fixture_dir / "valid.synthetic.json").write_text(
        json.dumps(valid, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (fixture_dir / "invalid.synthetic.json").write_text(
        json.dumps(invalid, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (fixture_dir / "lookup.synthetic.json").write_text(
        json.dumps(lookup, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_typescript_data(providers: list[dict[str, object]]) -> None:
    generated_dir = ROOT / "packages" / "typescript" / "src" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)
    body = json.dumps(providers, ensure_ascii=False, indent=2)
    text = (
        "/* This file is generated by scripts/generate-data.py. Do not edit by hand. */\n"
        f"export const dataVersion = {json.dumps(GENERATED_DATE)} as const;\n"
        f"export const providers = {body} as const;\n"
        "export type GeneratedProvider = (typeof providers)[number];\n"
    )
    (generated_dir / "banks.ts").write_text(text, encoding="utf-8")


def write_source_manifest(source_payloads: dict[str, bytes]) -> None:
    manifest = {
        "$schema": "./schema/source-manifest.schema.json",
        "generatedAt": GENERATED_DATE,
        "sources": [
            {
                "id": source_id,
                "url": SOURCES[source_id]["url"],
                "retrievedAt": GENERATED_DATE,
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
            for source_id, payload in source_payloads.items()
        ],
    }
    (ROOT / "data" / "source-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    providers_by_code: dict[str, Provider] = {}
    source_payloads = {
        source_id: fetch_bytes(source["url"])
        for source_id, source in SOURCES.items()
    }

    payment_pdf_id = "tcmb-payment-systems-participants-2026"
    for raw_code, name in parse_payment_systems_pdf(source_payloads[payment_pdf_id]):
        add_provider(
            providers_by_code,
            raw_code,
            name,
            provider_type_from_payment_systems(raw_code, name),
            payment_pdf_id,
        )

    payment_id = "tcmb-active-payment-institutions"
    for raw_code, name in parse_institution_rows(source_payloads[payment_id]):
        enrich_provider_from_registry(
            providers_by_code, raw_code, name, "payment_institution", payment_id
        )

    emoney_id = "tcmb-active-electronic-money-institutions"
    for raw_code, name in parse_institution_rows(source_payloads[emoney_id]):
        enrich_provider_from_registry(
            providers_by_code, raw_code, name, "electronic_money_institution", emoney_id
        )

    providers = [item.to_json() for item in sorted(providers_by_code.values(), key=lambda item: item.code)]
    write_json_csv_sql(providers)
    write_fixtures(providers)
    write_typescript_data(providers)
    write_source_manifest(source_payloads)
    print(f"Generated {len(providers)} providers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
