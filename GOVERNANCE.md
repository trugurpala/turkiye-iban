# Governance

`turkiye-iban` is maintained as an official-source-first open source project.

## Maintainer Responsibilities

- Keep data-source policy clear and enforceable.
- Review data changes against official or institutional sources.
- Reject real IBANs and personal financial data in public contributions.
- Keep runtime packages small, deterministic, and dependency-light.
- Publish releases with generated data artifacts and checksums.

## Decision Making

Routine fixes can be merged by one maintainer after tests pass. Data-source
policy changes, package API changes, new runtime dependencies, and governance
changes require maintainer consensus.

## Release Authority

Only maintainers listed in `MAINTAINERS.md` can publish GitHub Releases, NPM
packages, or future Composer packages.
