# Architecture

## Scope

This repository is limited to Turkish IBAN normalization, validation,
formatting, masking, provider-code extraction and lookup, plus the reference
data required for those operations. Address, postal code, tax office, plate,
telephone and other unrelated Türkiye datasets belong in separate projects.

## Canonical Data

`data/source/institutions.json` is the only hand-edited institution dataset. It
contains the reviewed snapshot version, Turkish IBAN structure, a source
catalog, and sorted institution records. Records reference the source catalog
through `sourceIds`; source URLs and metadata are not copied into every source
record.

The canonical file is validated by
`data/schema/institutions-source.schema.json`. Its model contains no JavaScript
functions, module paths, runtime values, or language-specific date objects.
Codes and dates are strings with documented formats so separate JavaScript,
Python, PHP, Go, Rust and .NET clients can consume the same contract.

## Generation Pipeline

`python scripts/generate-data.py` is offline and deterministic. It reads the
canonical source and writes, in code order:

- `data/tr-banks.json`
- `data/tr-banks.csv`
- `data/tr-banks.sql`
- `data/tr-banks.sqlite`
- `data/source-manifest.json`
- `packages/typescript/data/tr-banks.json`
- `packages/typescript/src/generated/banks.ts`
- synthetic valid, invalid and lookup fixtures

Generated files are never edited by hand. `python scripts/generate-data.py
--check` builds all outputs in a temporary directory and compares their bytes
with the committed artifacts. A difference fails CI.

Text outputs always use LF line endings. SQLite's informational producer-library
version header is normalized after creation so Windows and Linux produce the
same release bytes and SHA-256 checksum from identical canonical data.

## Remote Source Review

Normal builds never use the network. `scripts/check-sources.py` downloads the
configured official sources only during an explicit maintenance check. It
compares source hashes, parses the primary participant publication, and reports
added, removed and changed institution records. A changed page, parse error or
record diff requires human review and cannot update canonical or release data.

The scheduled workflow opens or updates a GitHub issue containing the report.
The HTML/PDF extraction is deliberately treated as a change detector, not a
trusted automatic publisher.

## Runtime Library

`packages/typescript/src/index.ts` provides the existing `tr-iban` public API.
It imports generated TypeScript data, performs no runtime network requests and
has no runtime dependencies. ESM, CommonJS and declaration builds are produced
from the same source. Existing exports and compatibility aliases remain in
place until a documented major release.

## Test Layers

- TypeScript unit tests cover parsing, validation, formatting, masking and lookup.
- Fixture contract tests exercise every known code plus unknown and invalid cases.
- Data validation checks JSON Schema and complete JSON/CSV/SQL/SQLite equality.
- Generated drift checks prove outputs match the canonical source.
- Privacy scanning permits only explicitly marked synthetic fixtures.
- Packed-consumer tests install the real NPM tarball in clean ESM and CommonJS projects.
- Executable examples verify JavaScript and direct data-file use.
- Release tests stage every asset and its SHA-256 checksum.

## Release Pipeline

CI must pass before a release tag is created. The release workflow verifies the
tag/package version, runs the complete offline suite, stages the data formats,
schemas, fixtures, NPM tarball and SBOM, verifies checksums, then creates an
immutable GitHub Release. NPM publishing separately requires that matching tag
and GitHub Release.
