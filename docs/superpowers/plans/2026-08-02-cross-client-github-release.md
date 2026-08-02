# Cross-Client GitHub Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to carry out this release task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish reproducible, CI-verified GitHub patch releases for the TypeScript/NPM foundation and its Python and PHP clients.

**Architecture:** The three repositories remain independently versioned. Each tag points to the current protected `main` commit; its existing release workflow rebuilds and uploads the repository's native assets. Registry publication is a separate, post-release action and is never claimed until the relevant registry confirms it.

**Tech Stack:** Git, GitHub Actions, Node.js 24, Python 3.12, PHP 8.2, npm, PyPI Trusted Publishing, Composer.

## Global Constraints

- Main repository release: `v0.2.3`; Python and PHP client releases: `v0.1.6`.
- These are PATCH releases: no public API, canonical data, schema, fixture meaning, or compatibility contract changes.
- Release tags must reference the exact current `origin/main` commit after the release-preparation PR merges.
- GitHub Release assets and checksums must be produced by the existing workflows; do not upload locally assembled substitutes.
- NPM, PyPI, and Packagist claims must remain evidence-based. Packagist is out of scope until its index returns a package record.

---

### Task 1: Prepare release metadata

**Files:**
- Modify: `package.json`, `package-lock.json`, `packages/typescript/package.json`, `CHANGELOG.md`, `README.md`
- Create: `docs/superpowers/plans/2026-08-02-cross-client-github-release.md`
- Modify in Python client: `pyproject.toml`, `CHANGELOG.md`, `README.md`
- Modify in PHP client: `CHANGELOG.md`, `README.md`

- [x] Set repository and package versions to their tag-equivalent patch versions.
- [x] Move already merged, user-visible fixes from `Unreleased` to dated release sections.
- [x] Keep registry installation wording truthful until each registry confirms publication.
- [x] Preserve the existing public API, canonical dataset, generated data and synthetic fixtures.

### Task 2: Verify release candidates

**Files:** no source changes.

- [x] Run the complete main-repository quality suite: `npm test`.
- [x] Run Python tests, strict type checking, build and package metadata validation.
- [x] Run PHP syntax and canonical fixture verification locally; require the hosted PHP 8.2-8.4 Composer CI matrix before tagging.
- [x] Inspect each diff for release-only scope and confirm no real IBAN or personal data was added.

### Task 3: Merge and tag protected main branches

**Files:** GitHub pull requests and tags.

- [ ] Open focused release-preparation PRs and merge only after required checks pass.
- [ ] Confirm each merged `main` head equals the intended tag target.
- [ ] Create annotated `v0.2.3` and `v0.1.6` tags and push them.
- [ ] Wait for GitHub Release workflows; verify their native release assets and generated notes.

### Task 4: Validate publication surfaces

**Files:** GitHub Releases and package registries.

- [ ] Verify each release exists, is non-draft, and contains its workflow-generated assets.
- [ ] Dispatch trusted NPM/PyPI publishing only after the matching GitHub Release is visible; verify registry responses before updating public claims.
- [ ] Do not state that PHP is installable from Packagist unless `repo.packagist.org` returns the package.
- [ ] Report CI evidence, registry evidence, release URLs, and any remaining external limitation.

## Public Surface Review

- [ ] `README.md`: direct download and status wording reviewed.
- [ ] `CHANGELOG.md`: dated release section and comparison links reviewed.
- [ ] `RELEASE.md` / client publishing documentation: workflow and registry separation reviewed.
- [ ] Package metadata: versions match tags.
- [ ] Workflows: release artifacts remain workflow-produced and checks remain required.
- [ ] Privacy boundary: no real IBAN or personal data introduced.
