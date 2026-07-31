from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IBAN_PATTERN = re.compile(
    r"\bTR(?:[ \t]*[0-9]){8}(?:[ \t]*[A-Z0-9]){16}\b",
    re.IGNORECASE,
)
TEXT_SUFFIXES = {
    ".csv",
    ".json",
    ".md",
    ".py",
    ".sql",
    ".ts",
    ".tsx",
    ".txt",
    ".yml",
    ".yaml",
}
EXCLUDED_PARTS = {".git", "node_modules", "dist", "release-artifacts"}


def load_fixture_ibans() -> set[str]:
    allowed: set[str] = set()
    for relative_path in [
        "fixtures/valid.synthetic.json",
        "fixtures/invalid.synthetic.json",
        "fixtures/lookup.synthetic.json",
    ]:
        data = json.loads((ROOT / relative_path).read_text(encoding="utf-8"))
        for item in data:
            iban = item.get("iban")
            if isinstance(iban, str) and item.get("synthetic") is True:
                allowed.add(re.sub(r"\s+", "", iban).upper())
    return allowed


def iter_project_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return [ROOT / line for line in result.stdout.splitlines() if line]

    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return files


def main() -> int:
    allowed_ibans = load_fixture_ibans()
    violations: list[str] = []

    for path in iter_project_files():
        if not path.is_file():
            continue
        relative_path = path.relative_to(ROOT)
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in IBAN_PATTERN.finditer(text):
            iban = re.sub(r"\s+", "", match.group(0)).upper()
            if iban not in allowed_ibans:
                masked = iban[:4] + "*" * max(0, len(iban) - 8) + iban[-4:]
                violations.append(f"{relative_path}:{match.start()}: unknown IBAN-like value {masked}")

    if violations:
        print("Privacy scan failed. Unknown IBAN-like values found:")
        print("\n".join(violations))
        return 1

    print(f"Privacy scan passed: {len(allowed_ibans)} known synthetic IBAN values allowed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
