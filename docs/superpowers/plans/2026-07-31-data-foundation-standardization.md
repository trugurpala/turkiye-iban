# Türkiye IBAN Data Foundation Standardization Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `core-pack:executing-plans` to implement this plan task-by-task.

**Goal:** Preserve the current `tr-iban` API while turning the repository into a deterministic, language-neutral Turkish IBAN data foundation with reproducible release assets.

**Architecture:** `data/source/institutions.json` becomes the only hand-edited institution source. Offline generators derive the existing JSON/CSV/SQL paths, a SQLite database, TypeScript data, source manifest, and synthetic fixtures. Remote TCMB checks produce candidate snapshots and human-reviewable diffs but never publish automatically.

**Tech Stack:** Python 3.12 standard library, JSON Schema 2020-12, TypeScript 5.9, Node.js 22/24, GitHub Actions.

## Global Constraints

- Keep the repository limited to Turkish IBAN validation, formatting, masking, provider-code lookup, and reference data.
- Preserve all current public API functions, package exports, and `data/tr-banks.*` compatibility paths.
- Never add real IBANs, customer data, account-holder data, or production financial records.
- Generated outputs are deterministic and must fail CI when they drift from the canonical source.
- Remote source changes require human review before data or release publication.

### Task 1: Contract tests

- [ ] Add failing tests for the canonical source, deterministic generation, SQLite parity, release assets, workflow names, and permanent documentation checklist.
- [ ] Run focused tests and confirm they fail for the missing foundation.

### Task 2: Canonical data and offline generation

- [ ] Create `data/source/institutions.json` and its JSON Schema.
- [ ] Refactor generation to read only the canonical source during normal builds.
- [ ] Generate JSON, CSV, SQL, SQLite, TypeScript data, manifest, and synthetic fixtures in stable order.
- [ ] Add a `--check` drift mode that never edits files.

### Task 3: Source review workflow

- [ ] Separate remote fetching/parsing from offline generation.
- [ ] Produce added, removed, and changed institution reports against the canonical source.
- [ ] Make scheduled checks create or update a human-review issue without changing release data.

### Task 4: CI and release gates

- [ ] Add format, lint, typecheck, unit, integration, schema, drift, privacy, build, example, and release-asset commands.
- [ ] Add dedicated data validation and scheduled source workflows.
- [ ] Include SQLite and schema assets with SHA-256 checksums in releases.

### Task 5: Public documentation and governance

- [ ] Add `ARCHITECTURE.md`, `DATA_SCHEMA.md`, `RELEASE.md`, `ROADMAP.md`, `TEST_DATA.md`, and `AGENTS.md`.
- [ ] Update README, CHANGELOG, contribution, support, source, security, release, package, issue, and PR surfaces.
- [ ] Record the required public-surface review checklist for every future task.

### Task 6: Verification

- [ ] Run generation drift checks, full tests, package build, packed-consumer tests, release preparation, checksum verification, and privacy scan.
- [ ] Inspect the final diff for scope, compatibility, generated artifacts, and undocumented changes.
