from __future__ import annotations

import hashlib
import io
import re
import urllib.request
from datetime import date
from typing import Any

from pypdf import PdfReader


USER_AGENT = "turkiye-iban-source-review/1.0"


def fetch_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def parse_payment_system_participants(pdf_bytes: bytes) -> list[dict[str, str]]:
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    institutions = []
    for line in text.splitlines():
        match = re.match(r"^\s*\d+\s+(\d{4})\s+(.+?)(?:\s+\(\*\))?\s*$", line)
        if not match:
            continue
        raw_code = match.group(1)
        institutions.append(
            {
                "code": raw_code.zfill(5),
                "rawCode": raw_code,
                "nameOfficial": " ".join(match.group(2).split()),
            }
        )
    institutions.sort(key=lambda item: item["code"])
    if len(institutions) < 50:
        raise ValueError(f"Expected at least 50 participant rows, found {len(institutions)}")
    if len({item["code"] for item in institutions}) != len(institutions):
        raise ValueError("Remote participant list contains duplicate codes")
    return institutions


def comparable_institution(item: dict[str, Any]) -> dict[str, str]:
    return {
        "code": str(item["code"]),
        "rawCode": str(item["rawCode"]),
        "nameOfficial": str(item["nameOfficial"]),
    }


def diff_institutions(
    current: list[dict[str, Any]], candidate: list[dict[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
    current_by_code = {item["code"]: comparable_institution(item) for item in current}
    candidate_by_code = {item["code"]: comparable_institution(item) for item in candidate}
    current_codes = set(current_by_code)
    candidate_codes = set(candidate_by_code)
    added = [candidate_by_code[code] for code in sorted(candidate_codes - current_codes)]
    removed = [current_by_code[code] for code in sorted(current_codes - candidate_codes)]
    changed = [
        {
            "code": code,
            "before": current_by_code[code],
            "after": candidate_by_code[code],
        }
        for code in sorted(current_codes & candidate_codes)
        if current_by_code[code] != candidate_by_code[code]
    ]
    return {"added": added, "removed": removed, "changed": changed}


def build_remote_review(canonical: dict[str, Any]) -> dict[str, Any]:
    source_changes = []
    errors = []
    candidate_institutions: list[dict[str, str]] | None = None
    for source in canonical["sources"]:
        try:
            content = fetch_bytes(source["url"])
            actual_hash = hashlib.sha256(content).hexdigest()
            status = "unchanged" if actual_hash == source["sha256"] else "changed"
            source_changes.append(
                {
                    "id": source["id"],
                    "usage": source["usage"],
                    "status": status,
                    "expectedSha256": source["sha256"],
                    "actualSha256": actual_hash,
                }
            )
            if source["usage"] == "primary_code_evidence":
                candidate_institutions = parse_payment_system_participants(content)
        except Exception as error:  # Network and upstream format failures must become review signals.
            errors.append({"id": source["id"], "message": str(error)})

    institution_changes = {"added": [], "removed": [], "changed": []}
    if candidate_institutions is not None:
        institution_changes = diff_institutions(canonical["institutions"], candidate_institutions)
    elif not errors:
        errors.append({"id": "primary-source", "message": "No primary participant candidate was produced"})

    has_source_change = any(item["status"] == "changed" for item in source_changes)
    has_institution_change = any(institution_changes[key] for key in institution_changes)
    return {
        "checkedAt": date.today().isoformat(),
        "requiresHumanReview": bool(errors or has_source_change or has_institution_change),
        "sourceChanges": source_changes,
        "institutionChanges": institution_changes,
        "errors": errors,
    }


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown_report(report: dict[str, Any]) -> str:
    status = "Human review required" if report["requiresHumanReview"] else "No reviewed data change detected"
    lines = [
        "# Turkish IBAN source review",
        "",
        f"- Checked at: `{report['checkedAt']}`",
        f"- Status: **{status}**",
        "- Safety: No data or release files were changed by this check.",
        "",
        "## Source content",
        "",
        "| Source | Usage | Status |",
        "| --- | --- | --- |",
    ]
    for source in report["sourceChanges"]:
        lines.append(
            f"| `{markdown_cell(source['id'])}` | `{markdown_cell(source.get('usage', 'unknown'))}` | "
            f"{markdown_cell(source['status'])} |"
        )

    changes = report["institutionChanges"]
    lines.extend(
        [
            "",
            "## Institution diff",
            "",
            f"- Added: {len(changes['added'])}",
            f"- Removed: {len(changes['removed'])}",
            f"- Changed: {len(changes['changed'])}",
        ]
    )
    for heading, key in (("Added", "added"), ("Removed", "removed")):
        if changes[key]:
            lines.extend(["", f"### {heading}", "", "| Code | Raw code | Official name |", "| --- | --- | --- |"])
            for item in changes[key]:
                lines.append(
                    f"| `{item['code']}` | `{item['rawCode']}` | {markdown_cell(item['nameOfficial'])} |"
                )
    if changes["changed"]:
        lines.extend(["", "### Changed", "", "| Code | Before | After |", "| --- | --- | --- |"])
        for item in changes["changed"]:
            lines.append(
                f"| `{item['code']}` | {markdown_cell(item['before']['nameOfficial'])} | "
                f"{markdown_cell(item['after']['nameOfficial'])} |"
            )
    if report["errors"]:
        lines.extend(["", "## Errors", ""])
        for error in report["errors"]:
            lines.append(f"- `{markdown_cell(error['id'])}`: {markdown_cell(error['message'])}")
    lines.extend(
        [
            "",
            "## Review action",
            "",
            "A maintainer must inspect the official sources and this diff before editing the canonical dataset or preparing a release.",
            "",
        ]
    )
    return "\n".join(lines)
