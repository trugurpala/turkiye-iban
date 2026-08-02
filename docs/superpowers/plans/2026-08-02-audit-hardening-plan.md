# Audit Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Resolve the audit's proven development, privacy, SQL import, and large-input risks without changing the public API or canonical provider data.

**Architecture:** Preserve `data/source/institutions.json` as the only editable data source. Make generator output repeatable, keep runtime behavior stable for normal inputs, and express every hardening decision as a regression test plus public documentation.

**Tech Stack:** Node.js 22+, TypeScript, Python 3.12+, SQLite, npm workspaces, node:test, unittest.

## Global Constraints

- Do not alter canonical institution records, their schema, or public TypeScript exports.
- Use synthetic fixtures only; never add a real IBAN or account data.
- Keep the change patch-compatible and deterministic.
- Update README, CHANGELOG, API/security/release documentation only where the public contract changes.

---

### Task 1: Developer-tooling safety

**Files:** `.gitignore`, `scripts/check-format.py`, `tools/test_quality_scripts.py`.

- [ ] Add regressions proving ignored virtual environments are excluded from formatting and a pre-existing `release-artifacts` directory survives the release-artifact quality test.
- [ ] Run the targeted quality tests and confirm they fail against the unmodified implementation.
- [ ] Ignore `.venv/` and `venv/`; replace repository-level cleanup with a test-owned `TemporaryDirectory` output path.
- [ ] Run the targeted quality tests again and confirm they pass.

### Task 2: Repeatable data import and privacy detection

**Files:** `scripts/generate-data.py`, `scripts/check-privacy.py`, `tools/test_quality_scripts.py`, generated SQL output.

- [ ] Add tests that execute generated SQL twice in one SQLite database and detect hyphenated/line-wrapped unapproved IBAN-like content.
- [ ] Run those tests and confirm the old implementation fails.
- [ ] Generate transactional replace SQL with explicit columns and normalize privacy separators before fixture comparison.
- [ ] Regenerate artifacts; rerun focused tests and data validation.

### Task 3: Bounded runtime input

**Files:** `packages/typescript/src/index.ts`, `packages/typescript/test/index.test.ts`, `docs/API.md`.

- [ ] Add a failing TypeScript test for a 1,025-character input.
- [ ] Introduce a non-exported length guard used by parse, formatting, masking, and provider-code extraction, preserving existing return types and errors.
- [ ] Confirm normal fixture behavior remains unchanged and the new test passes.

### Task 4: Public contract and release readiness

**Files:** `README.md`, `CHANGELOG.md`, `docs/SECURITY.md`, `docs/RELEASE.md`, `docs/RISK_REGISTER.md`.

- [ ] Document request-size responsibility, privacy-scanner limits, repeatable SQL import semantics, and virtual-environment-safe test use.
- [ ] Mark the patch as unreleased and state that no provider data or public API changed.
- [ ] Run `npm test`, `npm pack --dry-run`, `npm audit`, `pip-audit`, source check, and final generated drift check.
- [ ] Review the full diff, list reviewed public surfaces, and prepare a focused PR without publishing a release.
