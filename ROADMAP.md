# Roadmap

Current status: the stable foundation described below is complete as of
`v0.2.1`. The remaining sections contain optional, evidence-dependent ideas;
they are not unfinished release requirements or delivery commitments.

## Completed Foundation (`v0.2.1`)

- [x] Preserve Turkish IBAN parsing, validation, formatting, masking and lookup APIs.
- [x] Establish one canonical, schema-validated institution source.
- [x] Generate deterministic JSON, CSV, SQL, SQLite and TypeScript artifacts.
- [x] Validate complete cross-format equality and generated-file drift.
- [x] Detect official source changes and require human review.
- [x] Publish synthetic fixtures, checksums, SBOM and community policies.
- [x] Publish GitHub build provenance attestations for release assets.

## Optional Future Repository Work

- Add historical institution validity periods only when official evidence supports them.
- Add a small static data browser only if it consumes released artifacts without becoming a second data source.
- Improve source parsers when official publication formats change, with fixture-based parser tests.

## Possible Separate Language Clients

Future Python, PHP, Go, Rust and .NET clients must be separate repositories that
consume versioned schemas, fixtures and release assets from this project. They
must not be added as packages in this repository. Suggested names are:

- `turkiye-iban-python` ([design](docs/clients/PYTHON_CLIENT.md))
- `turkiye-iban-php` ([design](docs/clients/PHP_CLIENT.md))
- `turkiye-iban-go`
- `turkiye-iban-rust`
- `turkiye-iban-dotnet`

Each client should preserve the core validation semantics and run the shared
synthetic fixture contract, while maintaining its own ecosystem release cycle.
PHP and Python client implementations now exist in separate repositories and
have GitHub releases (`turkiye-iban-php` v0.1.4 and `turkiye-iban-python` v0.1.1).
Packagist and PyPI indexing remain separate publication steps and are not
claimed here until their public index entries are verified.

Unrelated Türkiye data such as addresses, postal codes, tax offices, plate
codes and telephone codes are outside this roadmap and would require separate
projects.
