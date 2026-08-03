from __future__ import annotations

import importlib.util
import inspect
import json
import re
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def load_script_module(name: str):
    script_path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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

    def test_canonical_source_is_the_single_schema_validated_input(self) -> None:
        source_path = ROOT / "data" / "source" / "institutions.json"
        schema_path = ROOT / "data" / "schema" / "institutions-source.schema.json"

        self.assertTrue(source_path.is_file())
        self.assertTrue(schema_path.is_file())
        source = json.loads(source_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        errors = list(Draft202012Validator(schema).iter_errors(source))

        self.assertEqual(errors, [])
        self.assertEqual(source["institutions"], sorted(source["institutions"], key=lambda item: item["code"]))
        self.assertEqual(
            len(source["institutions"]),
            len({item["code"] for item in source["institutions"]}),
        )

    def test_generated_files_have_no_drift_from_canonical_source(self) -> None:
        result = self.run_python("scripts/generate-data.py", "--check")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Generated files are up to date", result.stdout)

    def test_sqlite_artifact_matches_json_records(self) -> None:
        database_path = ROOT / "data" / "tr-banks.sqlite"
        self.assertTrue(database_path.is_file())

        connection = sqlite3.connect(database_path)
        try:
            rows = connection.execute(
                "SELECT code, name_official FROM tr_iban_providers ORDER BY code"
            ).fetchall()
        finally:
            connection.close()

        payload = json.loads((ROOT / "data" / "tr-banks.json").read_text(encoding="utf-8"))
        expected = [(item["code"], item["nameOfficial"]) for item in payload["providers"]]
        self.assertEqual(rows, expected)

    def test_data_contract_uses_source_evidence_without_iban_eligibility_claims(self) -> None:
        payload = json.loads((ROOT / "data" / "tr-banks.json").read_text(encoding="utf-8"))

        self.assertRegex(payload["dataVersion"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertGreater(len(payload["providers"]), 50)
        for provider in payload["providers"]:
            self.assertNotIn("ibanEligible", provider)
            self.assertEqual(provider["codeEvidence"], ["payment_system_participant"])
            for source in provider["sources"]:
                self.assertEqual(source["classification"], "official")
                self.assertGreater(len(source["evidenceScope"]), 0)

    def test_institution_status_requires_explicit_source_evidence(self) -> None:
        canonical = json.loads(
            (ROOT / "data" / "source" / "institutions.json").read_text(encoding="utf-8")
        )
        sources = {source["id"]: source for source in canonical["sources"]}

        for institution in canonical["institutions"]:
            if institution["status"] == "unknown":
                continue

            status_is_evidenced = any(
                "institution_status" in sources[source_id]["evidenceScope"]
                for source_id in institution["sourceIds"]
            )
            self.assertTrue(
                status_is_evidenced,
                f"{institution['code']} publishes status={institution['status']} without status evidence",
            )

    def test_licence_registry_codes_are_not_promoted_to_iban_provider_codes(self) -> None:
        payload = json.loads((ROOT / "data" / "tr-banks.json").read_text(encoding="utf-8"))
        providers_by_code = {provider["code"]: provider for provider in payload["providers"]}

        # Code 825 is present in the active e-money registry but is not a row in
        # the TCMB payment-systems participant list used for IBAN lookup.
        self.assertNotIn("00825", providers_by_code)

    def test_source_manifest_records_retrieval_hashes(self) -> None:
        manifest = json.loads((ROOT / "data" / "source-manifest.json").read_text(encoding="utf-8"))

        self.assertRegex(manifest["generatedAt"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertEqual(len(manifest["sources"]), 3)
        for source in manifest["sources"]:
            self.assertTrue(source["url"].startswith("https://"))
            self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")

    def test_sql_artifact_can_be_applied_twice_without_duplicate_rows(self) -> None:
        sql_text = (ROOT / "data" / "tr-banks.sql").read_text(encoding="utf-8")
        connection = sqlite3.connect(":memory:")
        try:
            connection.executescript(sql_text)
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
        for script in [
            "format:check",
            "lint",
            "typecheck",
            "check:generated",
            "test:unit",
            "test:integration",
            "test:examples",
            "test:release",
        ]:
            self.assertIn(script, package["scripts"])

        self.assertTrue((ROOT / "examples/javascript.mjs").is_file())
        self.assertTrue((ROOT / "examples/data_files.py").is_file())

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
        for fixture_path in (ROOT / "fixtures").glob("*.synthetic.json"):
            fixtures = json.loads(fixture_path.read_text(encoding="utf-8"))
            self.assertTrue(fixtures)
            self.assertTrue(all(item.get("synthetic") is True for item in fixtures))

        result = self.run_python("scripts/check-privacy.py")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Privacy scan passed", result.stdout)

    def test_privacy_guard_detects_hyphenated_and_line_wrapped_iban_like_values(self) -> None:
        privacy = load_script_module("check-privacy")
        allowed = privacy.load_fixture_ibans()
        synthetic = next(iter(allowed))
        unknown = "TR" + ("0" * 24)
        line_wrapped_unknown = f"{unknown[:10]}" + chr(10) + unknown[10:]

        self.assertNotIn(unknown, allowed)
        self.assertEqual(privacy.find_unknown_ibans(f"{synthetic[:4]}-{synthetic[4:]}", allowed), [])
        self.assertEqual(
            len(privacy.find_unknown_ibans(line_wrapped_unknown, allowed)),
            1,
        )

    def test_prepare_release_writes_artifacts_and_checksums(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            extra_artifact = Path(temp_dir) / "tr-iban-0.1.0-test.tgz"
            extra_artifact.write_bytes(b"synthetic package artifact")
            stale_dir = Path(temp_dir) / "v0.1.0-test"
            stale_dir.mkdir()
            (stale_dir / "stale-artifact.txt").write_text("stale", encoding="utf-8")
            result = self.run_python(
                "scripts/prepare-release.py",
                "--version",
                "0.1.0-test",
                "--output-dir",
                temp_dir,
                "--extra",
                str(extra_artifact),
            )
            release_dir = Path(temp_dir) / "v0.1.0-test"

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((release_dir / "tr-banks.json").is_file())
            self.assertTrue((release_dir / "tr-banks.csv").is_file())
            self.assertTrue((release_dir / "tr-banks.sql").is_file())
            self.assertTrue((release_dir / "tr-banks.sqlite").is_file())
            self.assertTrue((release_dir / "tr-banks.schema.json").is_file())
            self.assertTrue((release_dir / "manifest.json").is_file())
            self.assertTrue((release_dir / "schema.json").is_file())
            self.assertTrue((release_dir / extra_artifact.name).is_file())
            self.assertTrue((release_dir / "SHA256SUMS.txt").is_file())
            self.assertTrue((release_dir / "SHA256SUMS").is_file())
            self.assertFalse((release_dir / "stale-artifact.txt").exists())

            checksums = (release_dir / "SHA256SUMS.txt").read_text(encoding="utf-8")
            self.assertIn("tr-banks.json", checksums)
            self.assertIn("tr-banks.csv", checksums)
            self.assertIn("tr-banks.sql", checksums)
            self.assertIn("tr-banks.sqlite", checksums)
            self.assertIn("manifest.json", checksums)
            self.assertIn("schema.json", checksums)
            self.assertIn(extra_artifact.name, checksums)

    def test_repository_has_permanent_task_and_public_surface_checklists(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        pull_request = (
            ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
        ).read_text(encoding="utf-8")

        agent_items = [
            "README",
            "CHANGELOG",
            "schema",
            "security",
            "backward compatibility",
            "release",
            "personal data",
        ]
        for item in agent_items:
            self.assertIn(item.lower(), agents.lower())

        pull_request_items = [
            "README",
            "CHANGELOG",
            "şema",
            "güvenlik",
            "geriye uyumluluk",
            "release",
            "kişisel veri",
        ]
        for item in pull_request_items:
            self.assertIn(item.lower(), pull_request.lower())

        self.assertIn("at least five", agents.lower())

    def test_residual_risk_register_is_linked_from_public_surfaces(self) -> None:
        risk_register = (ROOT / "docs" / "RISK_REGISTER.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        package_readme = (
            ROOT / "packages" / "typescript" / "README.md"
        ).read_text(encoding="utf-8")
        launch_guide = (ROOT / "docs" / "launch" / "LAUNCH_GUIDE.md").read_text(
            encoding="utf-8"
        )
        pull_request = (
            ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
        ).read_text(encoding="utf-8")

        for required in [
            "TCMB onaylı",
            "hesabı doğrular",
            "transfer garantisi verir",
            "her dilde paket hazır",
            "providerStatus",
            "Node `>=22`",
        ]:
            self.assertIn(required, risk_register)

        self.assertIn("docs/RISK_REGISTER.md", readme)
        self.assertIn("docs/examples/NEXTJS_NESTJS.md", readme)
        self.assertIn("docs/RISK_REGISTER.md", package_readme)
        self.assertIn("../RISK_REGISTER.md", launch_guide)
        self.assertIn(
            "Public iddia, kaynak verisi, release, örnek veya başlangıç belgesi değiştiyse risk kaydı gözden geçirildi",
            pull_request,
        )

    def test_nextjs_nestjs_example_documents_safe_synthetic_usage(self) -> None:
        framework_example = (
            ROOT / "docs" / "examples" / "NEXTJS_NESTJS.md"
        ).read_text(encoding="utf-8")

        for required in [
            "identifyBankFromIban",
            "providerStatus",
            "maskIban",
            "sentetik",
            "TR56000460ABC123DEF456GHIJ",
            "TR16999990ABC123DEF456GHIJ",
            "Yonetim-Paneli",
        ]:
            self.assertIn(required, framework_example)

        self.assertIn('providerStatus; // "unknown"', framework_example)
        self.assertIn("Gercek IBAN", framework_example)

    def test_framework_adapter_examples_are_scoped_and_safe(self) -> None:
        adapters = (ROOT / "docs" / "examples" / "FRAMEWORK_ADAPTERS.md").read_text(encoding="utf-8")
        for required in [
            "Laravel",
            "Symfony",
            "FastAPI",
            "Django",
            "identifyBankFromIban",
            "identify_bank_from_iban",
            "maskIban",
            "mask_iban",
            "sentetik",
            "providerStatus",
            "provider_status",
        ]:
            self.assertIn(required, adapters)

        self.assertIn("sentetik fixture", adapters)

    def test_conformance_manifest_is_publicly_linked_and_machine_readable(self) -> None:
        manifest = json.loads((ROOT / "conformance" / "manifest.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "conformance" / "schema.json").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertEqual(manifest["contractVersion"], "1.0.0")
        self.assertEqual({item["kind"] for item in manifest["files"]}, {"valid", "invalid", "lookup"})
        self.assertEqual(schema["title"], "T\u00fcrkiye IBAN cross-language conformance manifest")
        self.assertEqual(
            schema["$id"],
            "https://github.com/trugurpala/turkiye-iban/releases/latest/download/schema.json",
        )
        self.assertIn("conformance/README.md", readme)

    def test_separate_language_client_designs_are_decision_records(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        risk_register = (ROOT / "docs" / "RISK_REGISTER.md").read_text(encoding="utf-8")
        php_design = (ROOT / "docs" / "clients" / "PHP_CLIENT.md").read_text(
            encoding="utf-8"
        )
        python_design = (ROOT / "docs" / "clients" / "PYTHON_CLIENT.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("docs/clients/PHP_CLIENT.md", readme)
        self.assertIn("docs/clients/PYTHON_CLIENT.md", readme)
        self.assertIn("docs/clients/PHP_CLIENT.md", roadmap)
        self.assertIn("docs/clients/PYTHON_CLIENT.md", roadmap)
        self.assertIn("Packagist indeksinin henüz doğrulanmamış olması", risk_register)
        self.assertIn("PHP `v0.1.5`", risk_register)
        self.assertIn("Python `v0.1.5`", risk_register)

        expected_apis = [
            "parse_iban",
            "validate_turkish_iban",
            "get_bank_code_from_iban",
            "find_bank_by_code",
            "identify_bank_from_iban",
            "format_iban",
            "mask_iban",
        ]
        for design, repository, package_name in [
            (php_design, "trugurpala/turkiye-iban-php", "trugurpala/turkiye-iban"),
            (python_design, "trugurpala/turkiye-iban-python", "turkiye-iban"),
        ]:
            self.assertIn(repository, design)
            self.assertIn(package_name, design)
            self.assertIn("v0.2.1", design)
            self.assertIn("SHA256SUMS", design)
            self.assertIn("Runtime ağ isteği | Yok", design)
            self.assertIn("lookup.synthetic.json", design)
            self.assertIn("providerStatus", design)
            self.assertIn("Bu repository içine", design)
            for api in expected_apis:
                self.assertIn(api, design)

        self.assertIn("PHP sürümü | `8.2`", php_design)
        self.assertIn("Python sürümü | `3.10`", python_design)
        self.assertIn("PyPI yayını GitHub Actions OIDC trusted publishing", python_design)

    def test_issue_forms_collect_actionable_and_privacy_safe_reports(self) -> None:
        template_dir = ROOT / ".github" / "ISSUE_TEMPLATE"
        bug = yaml.safe_load((template_dir / "bug_report.yml").read_text(encoding="utf-8"))
        feature = yaml.safe_load((template_dir / "feature_request.yml").read_text(encoding="utf-8"))
        config = yaml.safe_load((template_dir / "config.yml").read_text(encoding="utf-8"))

        bug_ids = {item.get("id") for item in bug["body"]}
        feature_ids = {item.get("id") for item in feature["body"]}
        contact_urls = {item["url"] for item in config["contact_links"]}

        self.assertTrue({"actual", "expected", "environment", "privacy"}.issubset(bug_ids))
        self.assertIn("privacy", feature_ids)
        self.assertIn("https://github.com/trugurpala/turkiye-iban/discussions", contact_urls)

    def test_dependabot_does_not_silence_major_updates(self) -> None:
        dependabot = yaml.safe_load((ROOT / ".github" / "dependabot.yml").read_text(encoding="utf-8"))

        for update in dependabot["updates"]:
            for ignored in update.get("ignore", []):
                self.assertNotIn("version-update:semver-major", ignored.get("update-types", []))

    def test_required_quality_workflows_exist(self) -> None:
        workflow_dir = ROOT / ".github" / "workflows"
        for filename in [
            "ci.yml",
            "data-validation.yml",
            "release.yml",
            "scheduled-source-check.yml",
        ]:
            self.assertTrue((workflow_dir / filename).is_file(), filename)

    def test_workflows_pin_third_party_actions_to_full_commit_shas(self) -> None:
        workflow_dir = ROOT / ".github" / "workflows"
        uses_pattern = re.compile(r"^\s*-?\s*uses:\s+([^#\s]+)", re.MULTILINE)

        for workflow in workflow_dir.glob("*.yml"):
            text = workflow.read_text(encoding="utf-8")
            for action in uses_pattern.findall(text):
                reference = action.rsplit("@", 1)[-1]
                self.assertRegex(reference, r"^[0-9a-f]{40}$", f"Unpinned action in {workflow}")

    def test_publish_workflows_only_release_current_main(self) -> None:
        workflow_dir = ROOT / ".github" / "workflows"
        release = (workflow_dir / "release.yml").read_text(encoding="utf-8")
        publish_npm = (workflow_dir / "publish-npm.yml").read_text(encoding="utf-8")

        self.assertIn('git fetch --force origin main:refs/remotes/origin/main', release)
        self.assertIn('test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"', release)
        self.assertIn("github.ref == 'refs/heads/main'", publish_npm)

    def test_release_workflow_attests_published_assets(self) -> None:
        release = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")

        self.assertIn("attestations: write", release)
        self.assertIn("id-token: write", release)
        self.assertRegex(
            release,
            r"actions/attest-build-provenance@[0-9a-f]{40}",
        )
        self.assertIn("subject-path: release-artifacts/v*/*", release)

    def test_github_yaml_files_parse(self) -> None:
        for yaml_path in (ROOT / ".github").rglob("*.yml"):
            with self.subTest(path=yaml_path.relative_to(ROOT)):
                self.assertIsNotNone(yaml.compose(yaml_path.read_text(encoding="utf-8")))

    def test_github_yaml_parse_does_not_delete_existing_release_artifacts(self) -> None:
        test_source = inspect.getsource(self.test_github_yaml_files_parse)

        self.assertNotIn('shutil.rmtree(ROOT / "release-artifacts"', test_source)

    def test_virtual_environment_paths_are_ignored_by_format_check(self) -> None:
        result = subprocess.run(
            ["git", "check-ignore", ".venv/site-packages/example.py", "venv/site-packages/example.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_relative_markdown_links_resolve(self) -> None:
        link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

        for markdown_path in ROOT.rglob("*.md"):
            if any(part in {"node_modules", "dist", "dist-test", "work"} for part in markdown_path.parts):
                continue
            text = markdown_path.read_text(encoding="utf-8")
            for raw_target in link_pattern.findall(text):
                target = raw_target.strip().strip("<>").split("#", 1)[0]
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                resolved = (markdown_path.parent / unquote(target)).resolve()
                with self.subTest(path=markdown_path.relative_to(ROOT), target=target):
                    self.assertTrue(resolved.exists(), f"Broken relative link: {target}")


if __name__ == "__main__":
    unittest.main()
