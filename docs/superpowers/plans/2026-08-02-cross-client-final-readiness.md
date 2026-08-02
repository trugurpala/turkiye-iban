# Cross-Client Final Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `core-pack:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a truthful, cross-platform, community-friendly final maintenance pass across the TypeScript, Python, and PHP Turkish IBAN repositories.

**Architecture:** The main repository remains the data and public-discussion authority. Client repositories make their own tests and READMEs correct while consuming the unchanged v0.2.1 conformance data. GitHub branch protection supplies the shared merge quality gate.

**Tech Stack:** GitHub Actions, GitHub branch protection, Python 3.10+, PHP 8.2+, Composer, pytest, PHPUnit, PHPStan.

## Global Constraints

- Do not change canonical institution data or fixture semantics.
- Do not use real IBANs or personal data.
- Do not state that Packagist works unless a public registry lookup and clean Composer installation prove it.
- Do not create a package release without an intentional version bump and its separate release verification.
- Keep one central Discussions space at `trugurpala/turkiye-iban`.

---

### Task 1: Record the cross-client decision

**Files:**
- Create: `docs/superpowers/specs/2026-08-02-cross-client-final-readiness-design.md`
- Create: `docs/superpowers/plans/2026-08-02-cross-client-final-readiness.md`

- [ ] Record published package evidence, Packagist 404 evidence, Windows
  fixture-hash cause, scope boundaries, and verification requirements.
- [ ] Commit the documentation-only coordination record to the main repository.

### Task 2: Correct the Python user journey and fixture portability

**Repository:** `trugurpala/turkiye-iban-python`

**Files:**
- Modify: `README.md`
- Modify: `tests/test_fixtures.py`
- Modify: `tests/test_iban.py`
- Modify: `CHANGELOG.md`

- [ ] Add a helper that hashes canonical LF fixture content so Windows CRLF
  checkout conversion cannot falsely fail the unchanged conformance contract.
- [ ] Add a focused regression assertion using CRLF fixture bytes.
- [ ] Lead README installation with `python -m pip install turkiye-iban==0.1.5`;
  preserve the GitHub wheel as a pinned fallback and label both accurately.
- [ ] Add the central Discussions link to the README.
- [ ] Run pytest, coverage, mypy, build, Twine check, and a clean PyPI smoke
  test with an allowed synthetic IBAN.

### Task 3: Correct PHP fixture portability and community entry point

**Repository:** `trugurpala/turkiye-iban-php`

**Files:**
- Modify: `README.md`
- Modify: `tests/ConformanceTest.php`
- Modify: `CHANGELOG.md`

- [ ] Add a canonical LF fixture-hash helper and a CRLF regression check.
- [ ] Add the central Discussions link to the README.
- [ ] Preserve the Packagist 404 warning and GitHub Release installation path.
- [ ] Run Composer tests, PHPStan, and asset preparation when supported locally;
  otherwise retain the exact environmental blocker and verify GitHub CI.

### Task 4: Align protected-branch discussion quality

**Repositories:** `trugurpala/turkiye-iban-python`, `trugurpala/turkiye-iban-php`

- [ ] Update each existing branch-protection configuration to require resolved
  review conversations while retaining its current required status checks,
  linear history, admin enforcement, and blocked force-push/deletion settings.
- [ ] Re-read the GitHub protection endpoint after the change.

### Task 5: Merge and verify publicly

- [ ] Open focused PRs for the main coordination record, Python patch, and PHP
  patch; include public surface review and actual commands.
- [ ] Wait for each required GitHub CI matrix and merge only when it succeeds.
- [ ] Re-read merged README text, package-index state, CI evidence, and branch
  protections; report NPM, PyPI, GitHub Release, and Packagist independently.
