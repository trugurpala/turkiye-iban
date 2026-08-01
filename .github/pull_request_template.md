## Summary

Describe the Turkish IBAN code, data, documentation, or release change.

## Type

- [ ] Code
- [ ] Canonical data
- [ ] Generated artifact
- [ ] Documentation
- [ ] Governance or policy

## Data Source

For data changes, include the official source URL, access date, and the generated
added/removed/changed record report. A source change is never accepted or
published automatically.

## Required Checklist

- [ ] Code or data change completed
- [ ] Tests updated when needed, or confirmed unnecessary
- [ ] README reviewed
- [ ] CHANGELOG updated
- [ ] Relevant public documentation reviewed
- [ ] Generated JSON, CSV, SQL, SQLite, fixtures, and TypeScript data rebuilt when inputs changed, or confirmed unchanged
- [ ] Schema validation passed
- [ ] Security impact reviewed
- [ ] Risk register reviewed when public claims, source data, release, examples, or onboarding docs changed
- [ ] Backward compatibility reviewed
- [ ] Release impact determined
- [ ] Release note or draft updated
- [ ] No real IBAN or other personal data was used

## Public Surface Review

List at least five reviewed public surfaces and mark each `updated` or `no change
required`, for example:

- README.md:
- CHANGELOG.md:
- DATA_SCHEMA.md:
- RELEASE.md:
- examples/:

## Verification

- [ ] `npm run generate:data` when canonical data changed
- [ ] `npm test`
- [ ] `npm pack --workspace packages/typescript --dry-run` when package contents changed
