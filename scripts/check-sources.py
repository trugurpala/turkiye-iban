from __future__ import annotations

import argparse
import json
from pathlib import Path

from source_review import build_remote_review, render_markdown_report


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare live official sources with reviewed canonical data.")
    parser.add_argument("--report", default="source-change-report.md")
    parser.add_argument("--json-report", default="source-change-report.json")
    args = parser.parse_args()

    canonical = json.loads((ROOT / "data/source/institutions.json").read_text(encoding="utf-8"))
    report = build_remote_review(canonical)
    Path(args.report).write_text(render_markdown_report(report), encoding="utf-8")
    Path(args.json_report).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Source review complete: {len(report['institutionChanges']['added'])} added, "
        f"{len(report['institutionChanges']['removed'])} removed, "
        f"{len(report['institutionChanges']['changed'])} changed"
    )
    if report["requiresHumanReview"]:
        print(f"Human review required. See {args.report}")
        return 1
    print("Official source content and normalized participant records are unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
