# Security Policy

## Supported Versions

Only the latest released minor version receives security updates.

## Reporting a Vulnerability

Do not open a public issue for security vulnerabilities or real financial data
exposure.

When this repository is published on GitHub, maintainers should enable GitHub
Private Vulnerability Reporting and use GitHub Security Advisories for reports.
Until then, this local starter repository cannot receive private external
security reports.

Reports should include:

- A concise description of the issue.
- The affected package version or commit.
- Reproduction steps that use synthetic data only.
- Any impact on IBAN validation, provider identification, or accidental data
  exposure.

## Privacy Incidents

If real IBANs, customer names, account owner data, phone numbers, payroll
records, screenshots, or other personal financial data appear in an issue, pull
request, commit, or fixture, maintainers should remove the content from public
view and rotate any affected release artifacts if needed.
