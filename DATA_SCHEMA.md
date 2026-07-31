# Data Schema

The machine-readable contracts are
`data/schema/institutions-source.schema.json`,
`data/schema/tr-banks.schema.json`, and
`data/schema/source-manifest.schema.json`. This document explains their stable
human-facing meaning.

## Canonical Document

| Field | Type | Required | Example | Rule |
| --- | --- | --- | --- | --- |
| `$schema` | string | no | `../schema/institutions-source.schema.json` | Relative schema reference |
| `schemaVersion` | string | yes | `1.0.0` | Semantic version of the canonical model |
| `country` | string | yes | `TR` | Always `TR` |
| `ibanFormat` | object | yes | `{ "length": 26, ... }` | Fixed Turkish IBAN field lengths |
| `dataVersion` | date string | yes | `2026-07-31` | Reviewed snapshot date, `YYYY-MM-DD` |
| `sourcePolicy` | string | yes | `Official-source-first...` | Short evidence policy summary |
| `sources` | array | yes | source objects | Source IDs must be unique and sorted |
| `institutions` | array | yes | institution objects | Codes must be unique and sorted |

## Institution Record

| Field | Type | Required | Example | Uniqueness and normalization |
| --- | --- | --- | --- | --- |
| `code` | string | yes | `00046` | Unique; exactly five decimal digits |
| `rawCode` | string | yes | `0046` | Published code; left-padding with `0` must equal `code` |
| `nameOfficial` | string | yes | `AKBANK T.A.Ş.` | Whitespace normalized; source spelling retained |
| `nameShort` | string | yes | `AKBANK` | Non-empty display name; not a legal identity claim |
| `type` | enum string | yes | `bank` | One documented institution category |
| `status` | enum string | yes | `active` | `active`, `inactive`, or `unknown` |
| `systems` | string array | yes | `TCMB_PAYMENT_SYSTEMS` | Unique values, sorted by generator |
| `codeEvidence` | string array | yes | `payment_system_participant` | Must contain reviewed code evidence |
| `aliases` | string array | yes | `[]` | Unique alternate names, sorted |
| `sourceIds` | string array | yes | `tcmb-payment-systems-participants-2025` | Every ID must exist in `sources` |
| `lastVerifiedAt` | date string | yes | `2026-07-31` | `YYYY-MM-DD`; maintainer-reviewed date |

## Source Record

| Field | Type | Required | Example | Rule |
| --- | --- | --- | --- | --- |
| `id` | string | yes | `tcmb-payment-systems-participants-2025` | Unique stable identifier |
| `publisher` | string | yes | `Türkiye Cumhuriyet Merkez Bankası` | Publishing institution |
| `title` | string | yes | `TCMB Ödeme Sistemleri Katılımcıları (2025)` | Publication title |
| `url` | HTTPS string | yes | `https://www.tcmb.gov.tr/...` | Direct official location where possible |
| `classification` | enum string | yes | `official` | `official`, `secondary`, or `manually_verified` |
| `usage` | enum string | yes | `primary_code_evidence` | Also `enrichment` or `monitor_only` |
| `evidenceScope` | string array | yes | `provider_code` | Facts the source is allowed to support |
| `retrievedAt` | date string | yes | `2026-07-31` | Last reviewed retrieval date |
| `sha256` | string | yes | 64 lowercase hex characters | Hash of retrieved source content |
| `extractionMethod` | string | yes | `PDF text table extraction...` | Honest extraction description |
| `redistributionStatus` | string | yes | `Extracted factual fields...` | Known redistribution treatment |

## Distribution Compatibility

`data/tr-banks.json` keeps the existing top-level `providers` array and expands
each `sourceIds` reference into a source object. CSV flattens arrays with `|`.
SQL and SQLite use snake_case database columns. These are format mappings of the
same records, not independent datasets.

The legacy names `tr-banks.*`, `providers`, `rawCode`, and public NPM data path
remain for v0.x compatibility. A breaking rename requires a major release and a
migration guide.
