# Package Index Publication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Make the released PHP and Python clients ready for verified Packagist and PyPI publication without claiming an index release before it exists.

**Architecture:** Keep GitHub releases as the immutable package provenance layer. Use Packagist's repository import/webhook flow for Composer and a separate manually approved GitHub Actions workflow with PyPI OIDC Trusted Publishing for Python. Public documentation records the current verified state and the exact gate from GitHub release to package index.

**Tech Stack:** Composer metadata, Packagist, PyPI, GitHub Actions, OIDC, pytest, mypy, build, twine.

## Global Constraints

- Never publish or document a package index as available without a successful public index lookup and clean-install smoke test.
- No long-lived PyPI token is stored in GitHub.
- The clients consume the pinned `turkiye-iban` release data and do not make runtime network calls.
- No real IBAN or personal financial data is added.
- The main repository remains data-first and single-purpose.

### Task 1: Verify current release state

- [x] Confirm PHP GitHub release `v0.1.4` and Python GitHub release `v0.1.2` exist with expected assets.
- [ ] Confirm Packagist `trugurpala/turkiye-iban` and PyPI `turkiye-iban` public index queries before making any claim.

### Task 2: Prepare PyPI trusted publishing

**Files:**
- Create: `docs/PACKAGE_INDEX_PUBLICATION.md`
- Modify: `turkiye-iban-python/.github/workflows/publish-pypi.yml`
- Create: `turkiye-iban-python/PUBLISHING.md`

- [ ] Build and test before publish.
- [ ] Use a protected `testpypi` or `pypi` environment and `id-token: write` only in the publish job.
- [ ] Require a PyPI pending Trusted Publisher matching repository, workflow, project, and environment.
- [ ] Verify the public index and clean install after publishing.

### Task 3: Prepare Packagist

- [ ] Confirm `composer.json` package metadata and GitHub repository visibility.
- [ ] Submit the package to Packagist and enable the GitHub webhook.
- [ ] Verify the public package page and `composer require trugurpala/turkiye-iban` in a clean PHP 8.2 project.

### Task 4: Update public claims

- [ ] Link the package index status document from README and client designs.
- [ ] Keep “GitHub release ready” separate from “Packagist/PyPI published”.
- [ ] Update CHANGELOG only with verified status.

### Task 5: Final gates

- [ ] Run main `npm.cmd test`.
- [ ] Run Python package pytest, mypy, build, and twine checks.
- [ ] Verify PHP package CI on PHP 8.2, 8.3, and 8.4.
- [ ] Report any external account configuration blocker explicitly.
