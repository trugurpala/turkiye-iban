# Release Process

## Preflight

```bash
python -m pip install -r tools/requirements.txt
npm ci
npm test
npm run prepare:release
npm -w packages/typescript pack --dry-run
```

## Versioning

Use semantic versioning.

- Patch: documentation, source refresh with no API changes, fixture additions.
- Minor: new package API, new generated artifact shape that remains backward
  compatible.
- Major: breaking API, data model, SQL schema, or fixture contract change.

## GitHub Release

Attach the files generated under `release-artifacts/vX.Y.Z`:

- `tr-banks.json`
- `tr-banks.csv`
- `tr-banks.sql`
- `tr-banks.schema.json`
- `valid.synthetic.json`
- `invalid.synthetic.json`
- `SHA256SUMS.txt`

Release notes must include the source retrieval date and a summary of provider
additions, removals, renames, or status changes.

## NPM

Publish from `packages/typescript` after `npm pack --dry-run` shows the expected
files.

```bash
npm -w packages/typescript publish --access public
```

Recheck the package name before the first public publish.

## Composer

Composer publication is phase two. It must consume the same root data files and
fixtures rather than maintaining a separate source of truth.
