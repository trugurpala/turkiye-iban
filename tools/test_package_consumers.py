from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PackageConsumerTest(unittest.TestCase):
    def run_command(self, command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            command,
            cwd=cwd,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
            shell=False,
        )

    def test_packed_package_supports_esm_and_commonjs_consumers(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            pack = self.run_command(
                [
                    "npm.cmd",
                    "pack",
                    "--workspace",
                    "tr-iban",
                    "--pack-destination",
                    str(temp_path),
                    "--json",
                ],
                ROOT,
            )
            self.assertEqual(pack.returncode, 0, pack.stdout + pack.stderr)
            pack_result = json.loads(pack.stdout)
            tarball = temp_path / pack_result[0]["filename"]
            self.assertTrue(tarball.is_file())

            install = self.run_command(
                ["npm.cmd", "install", "--ignore-scripts", "--no-audit", "--no-fund", str(tarball)],
                temp_path,
            )
            self.assertEqual(install.returncode, 0, install.stdout + install.stderr)

            esm_script = temp_path / "consumer.mjs"
            esm_script.write_text(
                'import { identifyBankFromIban } from "tr-iban";\n'
                'const result = identifyBankFromIban("TR510004609999000000000011");\n'
                'console.log(result.providerStatus, result.provider?.nameOfficial);\n',
                encoding="utf-8",
            )
            cjs_script = temp_path / "consumer.cjs"
            cjs_script.write_text(
                'const { identifyBankFromIban } = require("tr-iban");\n'
                'const result = identifyBankFromIban("TR510004609999000000000011");\n'
                'console.log(result.providerStatus, result.provider?.nameOfficial);\n',
                encoding="utf-8",
            )

            for script in [esm_script, cjs_script]:
                result = self.run_command(["node", str(script)], temp_path)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("known AKBANK T.A.Ş.", result.stdout)

            package_files = {item["path"] for item in pack_result[0]["files"]}
            self.assertIn("dist/esm/index.js", package_files)
            self.assertIn("dist/cjs/index.js", package_files)
            self.assertIn("dist/types/index.d.ts", package_files)
            self.assertIn("data/tr-banks.json", package_files)
            self.assertFalse(any("test" in path.lower() for path in package_files))


if __name__ == "__main__":
    unittest.main()
