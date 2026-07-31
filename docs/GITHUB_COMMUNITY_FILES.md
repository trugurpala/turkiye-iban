# GitHub Community Files

GitHub detects community health files from common repository locations such as
the repository root, `.github`, and `docs`. Issue templates are stricter: they
must live under `.github/ISSUE_TEMPLATE` and must have valid metadata.

This repository uses:

- Root files for `README.md`, `LICENSE`, `CODE_OF_CONDUCT.md`,
  `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `GOVERNANCE.md`,
  `MAINTAINERS.md`, and `CHANGELOG.md`.
- `.github/ISSUE_TEMPLATE/*.yml` for issue forms.
- `.github/pull_request_template.md` for pull request guidance.
- `.github/workflows/ci.yml` for basic validation.

Default organization-wide community health files can also be placed in a public
or internal `.github` repository, but this project keeps its policy files inside
the project repository so contributors see package-specific data and privacy
rules.

References checked on 2026-07-31:

- GitHub Docs: `https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file`
- GitHub Docs: `https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository`
- GitHub Docs: `https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository`
- GitHub Docs: `https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository`
