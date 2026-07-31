from __future__ import annotations

import json
import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".csv", ".cjs", ".json", ".md", ".mjs", ".py", ".sql", ".ts", ".txt", ".yml", ".yaml"}


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return [ROOT / line for line in result.stdout.splitlines() if line]


def main() -> int:
    errors = []
    checked = 0
    for path in tracked_files():
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        checked += 1
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        if text and not text.endswith("\n"):
            errors.append(f"{relative}: missing final newline")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.rstrip() != line:
                errors.append(f"{relative}:{line_number}: trailing whitespace")
        try:
            if path.suffix.lower() == ".json":
                json.loads(text)
            elif path.suffix.lower() in {".yml", ".yaml"}:
                yaml.compose(text)
        except Exception as error:
            errors.append(f"{relative}: parse error: {error}")

    if errors:
        print("Format check failed:")
        print("\n".join(errors))
        return 1
    print(f"Format check passed: {checked} tracked text files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
