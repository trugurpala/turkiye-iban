from __future__ import annotations

import shutil
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
