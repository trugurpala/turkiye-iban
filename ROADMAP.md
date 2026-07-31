# Roadmap

## Stable Foundation

- [x] Preserve Turkish IBAN parsing, validation, formatting, masking and lookup APIs.
- [x] Establish one canonical, schema-validated institution source.
- [x] Generate deterministic JSON, CSV, SQL, SQLite and TypeScript artifacts.
- [x] Validate complete cross-format equality and generated-file drift.
- [x] Detect official source changes and require human review.
- [x] Publish synthetic fixtures, checksums, SBOM and community policies.

## Next Repository Improvements

- Add signed release attestations when the hosting workflow supports them cleanly.
- Add historical institution validity periods only when official evidence supports them.
- Add a small static data browser only if it consumes released artifacts without becoming a second data source.
- Improve source parsers when official publication formats change, with fixture-based parser tests.

## Separate Language Clients

Future Python, PHP, Go, Rust and .NET clients must be separate repositories that
consume versioned schemas, fixtures and release assets from this project. They
must not be added as packages in this repository. Suggested names are:

- `turkiye-iban-python`
- `turkiye-iban-php`
- `turkiye-iban-go`
- `turkiye-iban-rust`
- `turkiye-iban-dotnet`

Each client should preserve the core validation semantics and run the shared
synthetic fixture contract, while maintaining its own ecosystem release cycle.

Unrelated Türkiye data such as addresses, postal codes, tax offices, plate
codes and telephone codes will be designed as separate projects.
