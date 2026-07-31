# Permanent Task Standard

This repository has one responsibility: Turkish IBAN validation, provider-code
lookup, and the language-neutral reference data that supports those operations.
Do not add unrelated Turkish address, tax, telephone, plate, postal-code, or
geographic datasets.

## Every Task

A task is not complete when only code or canonical data changed. Review every
public surface affected by the change, including examples, schemas, generated
artifacts, security guidance, package metadata, and the release process.
Before completion, check README, CHANGELOG, the relevant technical document,
tests, and release notes. Do not edit an unaffected document merely to create
churn; report that it was reviewed and required no change.

Evaluate at least five of these public surfaces on every task:

- README
- CHANGELOG
- usage examples
- API documentation
- data schema and DATA_SCHEMA.md
- DATA_SOURCES.md
- SECURITY.md
- CONTRIBUTING.md
- release notes and RELEASE.md
- GitHub issue and pull request templates
- generated JSON, CSV, SQL, and SQLite files
- package metadata
- migration or backward compatibility notes

The final task report must list each reviewed surface as `updated` or `no change
required`.

## Required Checklist

- [ ] Code or data change completed
- [ ] Tests updated
- [ ] README reviewed
- [ ] CHANGELOG updated
- [ ] Relevant public documentation reviewed
- [ ] Generated data files rebuilt
- [ ] Schema validation passed
- [ ] Security impact reviewed
- [ ] Backward compatibility reviewed
- [ ] Release impact determined
- [ ] Release note or draft updated
- [ ] No real personal data was used

Run `npm test` before completion. Data changes also require a reviewed remote
source report and `npm run generate:data`; ordinary builds and tests remain
offline and deterministic.
