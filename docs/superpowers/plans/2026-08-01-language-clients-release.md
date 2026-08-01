# PHP and Python Client Packages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Publish separate, tested PHP/Composer and Python/PyPI clients that consume the `turkiye-iban` release data without changing the canonical data repository or its TypeScript API.

**Architecture:** Create two independent GitHub repositories: `trugurpala/turkiye-iban-php` and `trugurpala/turkiye-iban-python`. Each package embeds the pinned `turkiye-iban` v0.2.1 release assets after SHA-256 verification, implements the same seven public behaviors, runs shared synthetic fixtures, and performs no runtime network access. The main repository remains the language-independent source of truth and receives only links, release notes, and compatibility documentation after package releases.

**Tech Stack:** PHP 8.2+, Composer, PHPUnit, PHPStan; Python 3.10+, `pyproject.toml`, pytest, mypy, build, twine; GitHub Actions; GitHub Releases; Packagist/PyPI publishing where account configuration permits.

## Global Constraints

- Never include real IBANs, account holders, customer data, production logs, or personal financial data.
- Use only the existing synthetic fixtures from `turkiye-iban` v0.2.1.
- `providerStatus`/`provider_status` means dataset code match only; it does not prove account existence, ownership, license, activity, or transferability.
- No runtime network calls; network is allowed only during controlled package asset preparation.
- Keep the main repository single-purpose and preserve its public TypeScript API and generated data.
- Release only after clean-install, fixture parity, privacy, build, and package validation checks pass.

### Task 1: Freeze the source contract and package version

**Files:**
- Create: `docs/superpowers/plans/2026-08-01-language-clients-release.md`
- Read: `docs/clients/PHP_CLIENT.md`, `docs/clients/PYTHON_CLIENT.md`, `fixtures/*.synthetic.json`, `packages/typescript/src/index.ts`

- [ ] Confirm the pinned upstream tag, asset names, checksum URL, fixture shapes, and seven API behaviors.
- [ ] Record the package version as `0.1.0` for both clients because they are new packages.
- [ ] Do not change canonical data or TypeScript runtime code.

### Task 2: Create and scaffold the PHP repository

**Files:**
- Create repository: `trugurpala/turkiye-iban-php`
- Create: `composer.json`, `src/`, `tests/`, `resources/`, `scripts/`, `.github/workflows/ci.yml`, `.github/workflows/release.yml`
- Create: `README.md`, `CHANGELOG.md`, `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`

- [ ] Define Composer package `trugurpala/turkiye-iban`, namespace `TurkiyeIban`, PHP `^8.2`, PSR-4 autoloading, PHPUnit and PHPStan dev dependencies.
- [ ] Add deterministic asset preparation that downloads only pinned v0.2.1 release assets and verifies `SHA256SUMS` before writing `resources/`.
- [ ] Add a no-network runtime test and a clean install smoke test.

### Task 3: Implement PHP behavior with tests first

**Files:**
- Create: `src/Iban.php`, `src/ProviderRepository.php`, `src/Result/*.php`
- Create: `tests/Unit/IbanTest.php`, `tests/Unit/ProviderRepositoryTest.php`, `tests/Fixtures/*.json`

- [ ] Implement normalization, four-character formatting, masking, TR structure validation, MOD 97-10, provider-code extraction, lookup, and identification.
- [ ] Return immutable value objects or arrays with documented stable field names.
- [ ] Preserve unknown-provider semantics: structurally valid unknown code returns `providerStatus=unknown` and no provider; invalid structure remains invalid.
- [ ] Assert all valid, invalid, and lookup fixtures match TypeScript semantics.

### Task 4: Verify and release the PHP package

**Files:**
- Modify: PHP repository workflow and release metadata
- Modify main repo: `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `docs/clients/PHP_CLIENT.md`

- [ ] Run Composer install, PHPUnit, PHPStan, fixture parity, privacy scan, package archive, and clean-project smoke test.
- [ ] Create GitHub tag/release `v0.1.0` with source/checksum provenance.
- [ ] Publish to Packagist only if the Packagist account/webhook or token is configured and publication is verified.
- [ ] Update main repository links only with verified URLs and status.

### Task 5: Create and scaffold the Python repository

**Files:**
- Create repository: `trugurpala/turkiye-iban-python`
- Create: `pyproject.toml`, `src/turkiye_iban/`, `tests/`, `scripts/`, `.github/workflows/ci.yml`, `.github/workflows/release.yml`
- Create: `README.md`, `CHANGELOG.md`, `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`

- [ ] Define PyPI project `turkiye-iban`, import package `turkiye_iban`, Python `>=3.10`, typed public API, and package data inclusion.
- [ ] Add deterministic pinned asset preparation with SHA-256 verification and no runtime network code.
- [ ] Configure pytest, mypy, build, twine check, and clean virtual-environment smoke tests.

### Task 6: Implement Python behavior with tests first

**Files:**
- Create: `src/turkiye_iban/iban.py`, `src/turkiye_iban/providers.py`, `src/turkiye_iban/models.py`
- Create: `tests/test_iban.py`, `tests/test_providers.py`, `tests/fixtures/*.json`

- [ ] Implement the same seven behaviors with snake_case names and frozen dataclasses.
- [ ] Implement MOD 97-10 using incremental remainder arithmetic, including alphanumeric account fields.
- [ ] Match known/unknown provider and invalid-input semantics exactly.
- [ ] Assert all shared valid, invalid, and lookup fixtures produce the same results as TypeScript.

### Task 7: Verify and release the Python package

**Files:**
- Modify: Python repository workflow and release metadata
- Modify main repo: `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `docs/clients/PYTHON_CLIENT.md`

- [ ] Run pytest, mypy, build, twine check, privacy scan, and clean virtual-environment install smoke test.
- [ ] Create GitHub tag/release `v0.1.0` with upstream data version and checksums.
- [ ] Publish to PyPI through OIDC trusted publishing only if the PyPI project/trusted publisher is configured and publication is verified.
- [ ] Update main repository links only with verified URLs and status.

### Task 8: Cross-package integration and public documentation

**Files:**
- Modify main repo: `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `docs/clients/PHP_CLIENT.md`, `docs/clients/PYTHON_CLIENT.md`
- Create or modify: shared release compatibility notes and package examples

- [ ] Add Composer and pip installation examples only after the package indexes confirm availability.
- [ ] Document exact upstream data release consumed by each package.
- [ ] Add a compatibility matrix for TypeScript, PHP, and Python API names/results.
- [ ] Report public surface review and remaining publishing/account risks.

### Task 9: Final verification and delivery

- [ ] Run the main repository `npm.cmd test` after documentation changes.
- [ ] Run full clean-install tests in both package repositories.
- [ ] Confirm GitHub Actions, tags, release assets, package metadata, README links, and checksums.
- [ ] Confirm no real IBAN or personal data with repository-wide scans.
- [ ] Commit, push, open PRs where branch protection requires review, merge only after checks pass, and report actual release URLs.

