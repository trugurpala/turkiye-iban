# Roadmap

## Phase 1: TypeScript and Data

- Official-source-first data generator.
- JSON, CSV, SQL, schema, and synthetic fixtures.
- TypeScript/NPM package with deterministic runtime API.
- GitHub community, security, and governance files.
- Release artifact checksums.

## Phase 2: PHP and Composer

- Add `packages/php`.
- Reuse root fixtures in PHPUnit tests.
- Publish as `turkiye/iban` or the chosen Composer package name.
- Keep API names close to TypeScript where language conventions allow it.

## Phase 3: Python

- Add `packages/python`.
- Reuse root fixtures in pytest tests.
- Provide pure Python lookup and formatting helpers.

## Later

- GitHub Pages documentation site.
- Scheduled source refresh workflow.
- Maintainer dashboard for data diffs.
- Optional machine-readable source provenance report per release.
