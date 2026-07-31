# Contributing

`turkiye-iban` accepts small, sourced and tested improvements within Turkish
IBAN validation, provider lookup and reference data. Unrelated Türkiye datasets
and additional language packages belong in separate repositories.

## Privacy Rule

Never use a real IBAN, account holder or customer name, telephone number,
payroll record, statement, screenshot, support transcript or production
financial data in issues, pull requests, commits, fixtures or examples. Use only
the explicitly synthetic values described in `TEST_DATA.md`. Report security or
privacy incidents privately through `SECURITY.md`.

## Setup

```bash
python -m pip install -r tools/requirements.txt
npm ci
npm test
```

Normal generation, tests and builds are offline.

Create a focused branch, keep commits limited to one concern, and open a pull
request against `main`. Explain the behavior or data impact, list at least five
reviewed public surfaces, and include the commands you actually ran.

## Data Changes

Start with a remote review:

```bash
npm run data:check-remote
```

This command never changes release data. Review its source hashes and
added/removed/changed institution report against the official document. Apply
an accepted change only to `data/source/institutions.json`, then run:

```bash
npm run generate:data
npm test
```

Do not edit JSON, CSV, SQL, SQLite, TypeScript generated data or fixtures by
hand. A data PR must include the official source URL, access date, evidence
scope, change reason, review report and resulting generated diff. An active
license registry entry is not automatically provider-code evidence.

## Code Changes

- Preserve the current public API, package exports and compatibility aliases.
- Add a failing test before changing behavior.
- Keep runtime code deterministic, dependency-free and network-free.
- Check both ESM and CommonJS packed consumers.
- Never log a raw IBAN; use `maskIban` in diagnostics.
- Breaking changes require a major release and migration guide.

## Documentation and Public Surfaces

Every task follows `AGENTS.md`. Review at least five public surfaces and record
each as `updated` or `no change required` in the pull request. README,
CHANGELOG, relevant technical documentation, tests, generated data, schemas,
security and release impact must never be silently skipped.

## Pull Request Verification

```bash
npm test
npm pack --workspace packages/typescript --dry-run
```

Complete the pull request checklist. Maintainers may reject changes whose
evidence, privacy treatment, compatibility or release impact is unclear.
