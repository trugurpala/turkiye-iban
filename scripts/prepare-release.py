from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def project_version() -> str:
    package_json = json.loads((ROOT / "packages" / "typescript" / "package.json").read_text(encoding="utf-8"))
    return str(package_json["version"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare GitHub Release data artifacts.")
    parser.add_argument("--version", default=project_version())
    parser.add_argument("--output-dir", default=str(ROOT / "release-artifacts"))
    args = parser.parse_args()

    version = args.version.removeprefix("v")
    release_dir = Path(args.output_dir).resolve() / f"v{version}"
    release_dir.mkdir(parents=True, exist_ok=True)

    artifact_paths = [
        ROOT / "data" / "tr-banks.json",
        ROOT / "data" / "tr-banks.csv",
        ROOT / "data" / "tr-banks.sql",
        ROOT / "data" / "schema" / "tr-banks.schema.json",
        ROOT / "fixtures" / "valid.synthetic.json",
        ROOT / "fixtures" / "invalid.synthetic.json",
    ]

    copied: list[Path] = []
    for source in artifact_paths:
        destination = release_dir / source.name
        shutil.copy2(source, destination)
        copied.append(destination)

    checksum_lines = [f"{sha256(path)}  {path.name}" for path in sorted(copied, key=lambda item: item.name)]
    (release_dir / "SHA256SUMS.txt").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    print(f"Prepared release artifacts in {release_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
