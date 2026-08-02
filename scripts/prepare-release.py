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
    parser.add_argument(
        "--extra",
        action="append",
        default=[],
        help="Additional artifact to copy into the release and checksum.",
    )
    args = parser.parse_args()

    version = args.version.removeprefix("v")
    release_dir = Path(args.output_dir).resolve() / f"v{version}"
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir(parents=True, exist_ok=True)

    artifact_paths = [
        ROOT / "data" / "tr-banks.json",
        ROOT / "data" / "tr-banks.csv",
        ROOT / "data" / "tr-banks.sql",
        ROOT / "data" / "tr-banks.sqlite",
        ROOT / "data" / "source-manifest.json",
        ROOT / "data" / "schema" / "institutions-source.schema.json",
        ROOT / "data" / "schema" / "tr-banks.schema.json",
        ROOT / "data" / "schema" / "source-manifest.schema.json",
        ROOT / "fixtures" / "valid.synthetic.json",
        ROOT / "fixtures" / "invalid.synthetic.json",
        ROOT / "fixtures" / "lookup.synthetic.json",
        ROOT / "conformance" / "manifest.json",
        ROOT / "conformance" / "schema.json",
    ]

    copied: list[Path] = []
    extra_paths = [Path(item).resolve() for item in args.extra]
    for source in [*artifact_paths, *extra_paths]:
        if not source.is_file():
            raise FileNotFoundError(f"Release artifact not found: {source}")
        destination = release_dir / source.name
        shutil.copy2(source, destination)
        copied.append(destination)

    checksum_lines = [f"{sha256(path)}  {path.name}" for path in sorted(copied, key=lambda item: item.name)]
    checksum_text = "\n".join(checksum_lines) + "\n"
    (release_dir / "SHA256SUMS").write_text(checksum_text, encoding="utf-8")
    # Keep the v0.x filename for consumers that already automate against it.
    (release_dir / "SHA256SUMS.txt").write_text(checksum_text, encoding="utf-8")

    print(f"Prepared release artifacts in {release_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
