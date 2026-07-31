# Release Policy

## Versioning

The JavaScript package and repository releases use Semantic Versioning.

- **PATCH:** documentation corrections, non-behavioral fixes, or institution
  metadata corrections that do not add records or change the public schema.
- **MINOR:** a new institution record, new generated format, new optional data
  field, or backward-compatible public API feature.
- **MAJOR:** a public API removal, import-path break, canonical/distribution
  schema break, incompatible data meaning, or removal of a documented alias.

Versions are selected by maintainers after reviewing the actual diff. Workflows
never choose or increment a version automatically.

Release tags must point to the current `origin/main` commit. The NPM trusted
publishing workflow accepts dispatches only from `main` and verifies that the
matching immutable GitHub Release and tag already exist at the same commit.

## Pre-release Gates

Run from a clean checkout:

```bash
python -m pip install -r tools/requirements.txt
npm ci
npm run data:check-remote
npm test
npm pack --workspace packages/typescript --dry-run
```

Remote source changes must be reviewed first. `npm test` is offline and covers
format, lint, typecheck, drift, schemas, privacy, unit, integration, examples
and release staging. The package version, `CHANGELOG.md`, data version and tag
must agree with the intended release.

## Release Assets

Every GitHub Release contains:

- `tr-banks.json`
- `tr-banks.csv`
- `tr-banks.sql`
- `tr-banks.sqlite`
- `tr-banks.schema.json`
- `institutions-source.schema.json`
- `source-manifest.json` and its schema
- valid, invalid and lookup synthetic fixture files
- `tr-iban-X.Y.Z.tgz`
- CycloneDX SBOM
- `SHA256SUMS` and the v0.x-compatible `SHA256SUMS.txt`

Verify downloaded assets on Linux or macOS with:

```bash
sha256sum --check SHA256SUMS
```

On PowerShell, compare `Get-FileHash -Algorithm SHA256 <file>` with the matching
line in `SHA256SUMS`.

## Retention and Rollback

Published assets are immutable. Old GitHub Releases, schemas and data snapshots
remain available. An incorrect NPM version is deprecated rather than silently
replaced, and a corrected version is released. A bad data release is superseded
by a new version whose CHANGELOG records the affected fields and evidence.

If a release exposes real personal data, follow `SECURITY.md`: remove public
access where possible, rotate or rebuild affected artifacts, investigate Git
history, and publish a transparent security correction without repeating the
data.
