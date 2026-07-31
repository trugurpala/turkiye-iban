from __future__ import annotations

import json
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class QualityScriptsTest(unittest.TestCase):
    def run_python(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_validate_data_script_passes_for_generated_files(self) -> None:
        result = self.run_python("scripts/validate-data.py")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Data validation passed", result.stdout)

    def test_data_contract_uses_source_evidence_without_iban_eligibility_claims(self) -> None:
        payload = json.loads((ROOT / "data" / "tr-banks.json").read_text(encoding="utf-8"))

        self.assertRegex(payload["dataVersion"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertGreater(len(payload["providers"]), 100)
        for provider in payload["providers"]:
            self.assertNotIn("ibanEligible", provider)
            self.assertTrue(provider["codeEvidence"])
            self.assertTrue(
                set(provider["codeEvidence"])
                <= {
                    "payment_system_participant",
                    "licensed_payment_institution",
                    "licensed_electronic_money_institution",
                }
            )

    def test_source_manifest_records_retrieval_hashes(self) -> None:
        manifest = json.loads((ROOT / "data" / "source-manifest.json").read_text(encoding="utf-8"))

        self.assertRegex(manifest["generatedAt"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(len(manifest["sources"]), 3)
        for source in manifest["sources"]:
            self.assertTrue(source["url"].startswith("https://"))
            self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")

    def test_sql_artifact_applies_cleanly(self) -> None:
        sql_text = (ROOT / "data" / "tr-banks.sql").read_text(encoding="utf-8")
        connection = sqlite3.connect(":memory:")
        try:
            connection.executescript(sql_text)
            row_count = connection.execute("SELECT COUNT(*) FROM tr_iban_providers").fetchone()[0]
        finally:
            connection.close()

        payload = json.loads((ROOT / "data" / "tr-banks.json").read_text(encoding="utf-8"))
        self.assertEqual(row_count, len(payload["providers"]))

    def test_normal_test_script_is_offline(self) -> None:
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))

        self.assertNotIn("generate:data", package["scripts"]["test"])
        self.assertIn("data:update", package["scripts"])

    def test_typescript_package_declares_dual_module_exports(self) -> None:
        package = json.loads(
            (ROOT / "packages" / "typescript" / "package.json").read_text(encoding="utf-8")
        )
        root_export = package["exports"]["."]

        self.assertEqual(package["engines"]["node"], ">=22")
        self.assertEqual(root_export["import"], "./dist/esm/index.js")
        self.assertEqual(root_export["require"], "./dist/cjs/index.js")
        self.assertEqual(root_export["types"], "./dist/types/index.d.ts")
        self.assertEqual(package["repository"]["url"], "git+https://github.com/trugurpala/turkiye-iban.git")

    def test_privacy_guard_accepts_only_known_synthetic_ibans(self) -> None:
        result = self.run_python("scripts/check-privacy.py")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Privacy scan passed", result.stdout)

    def test_prepare_release_writes_artifacts_and_checksums(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.run_python(
                "scripts/prepare-release.py",
                "--version",
                "0.1.0-test",
                "--output-dir",
                temp_dir,
            )
            release_dir = Path(temp_dir) / "v0.1.0-test"

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((release_dir / "tr-banks.json").is_file())
            self.assertTrue((release_dir / "tr-banks.csv").is_file())
            self.assertTrue((release_dir / "tr-banks.sql").is_file())
            self.assertTrue((release_dir / "SHA256SUMS.txt").is_file())

            checksums = (release_dir / "SHA256SUMS.txt").read_text(encoding="utf-8")
            self.assertIn("tr-banks.json", checksums)
            self.assertIn("tr-banks.csv", checksums)
            self.assertIn("tr-banks.sql", checksums)

        shutil.rmtree(ROOT / "release-artifacts", ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
