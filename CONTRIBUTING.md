# Contributing

Thank you for helping improve `turkiye-iban`.

## Before You Start

- Do not submit real IBANs, account owner names, phone numbers, payroll data,
  screenshots, bank slips, or customer records.
- Use only synthetic examples in tests, fixtures, issues, and pull requests.
- Data changes must cite official or institutional sources.
- Schwifty can be used for comparison, but it is not an accepted primary data
  source for this repository.

## Development Setup

```bash
python -m pip install -r tools/requirements.txt
npm install
npm run generate:data
npm test
```

## Data Contributions

Data pull requests must include:

- The official source URL.
- The date you checked the source.
- A short explanation of the change.
- Regenerated `data/tr-banks.json`, `data/tr-banks.csv`, `data/tr-banks.sql`,
  and `packages/typescript/src/generated/banks.ts`.

Do not hand-edit generated data files unless the generator itself cannot express
the correction. If that happens, explain the reason in the pull request.

## Code Contributions

Keep the API small and deterministic. The package must not make network calls at
runtime, must not log IBANs, and must not introduce runtime dependencies without
a maintainer decision.

## Pull Request Checklist

- Tests pass with `npm test`.
- Generated data is up to date when data changed.
- No real IBANs or personal financial data are included.
- Documentation changed when behavior or policy changed.
