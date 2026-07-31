from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "source-manifest.json"


def fetch_sha256(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "turkiye-iban-source-check/0.1"},
    )
    digest = hashlib.sha256()
    with urllib.request.urlopen(request, timeout=30) as response:
        for chunk in iter(lambda: response.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    changed: list[str] = []

    for source in manifest["sources"]:
        actual = fetch_sha256(source["url"])
        if actual != source["sha256"]:
            changed.append(source["id"])
            print(f"CHANGED {source['id']}: expected {source['sha256']}, received {actual}")
        else:
            print(f"UNCHANGED {source['id']}: {actual}")

    if changed:
        print("Official sources changed; run `npm run data:update` and review the diff.")
        return 1

    print(f"Source check passed: {len(manifest['sources'])} official sources unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
