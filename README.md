# turkiye-iban

Official-source-first Turkish IBAN parsing, validation, and provider-code data.

`turkiye-iban` helps applications identify the bank, payment institution, or
electronic money institution encoded in a Turkish IBAN provider code. It ships
language-independent data files and a first-phase TypeScript package.

## What This Package Does

- Validates Turkish IBAN format and MOD 97-10 check digits.
- Extracts the five-digit Turkish payment service provider code from an IBAN.
- Looks up the provider code in the bundled Turkey provider dataset.
- Publishes the same core data as JSON, CSV, and SQL.
- Provides synthetic valid and invalid fixture sets for tests.

## What It Does Not Validate

This package does not verify that an account exists, that an account belongs to
a person or company, that a name matches the IBAN, or that a transfer can be
completed. Do not use it as a KYC, fraud, ownership, or payment-finality check.

## Install

```bash
npm install tr-iban
```

The package name is the planned first NPM name. Recheck registry ownership and
availability before first publication.

## Usage

```ts
import {
  formatIban,
  identifyBankFromIban,
  maskIban,
  validateTurkishIban,
} from "tr-iban";

const iban = "TR510004609999000000000011";

validateTurkishIban(iban); // true
formatIban(iban); // "TR51 0004 6099 9900 0000 0000 11"
maskIban(iban); // "TR51 **** **** **** **** **00 11"

const result = identifyBankFromIban(iban);
console.log(result.bank?.nameOfficial); // "AKBANK T.A.S."
```

## Data Files

- `data/tr-banks.json`
- `data/tr-banks.csv`
- `data/tr-banks.sql`
- `data/schema/tr-banks.schema.json`

Although the file name uses `banks` for package ergonomics, the dataset also
contains payment institutions and electronic money institutions where official
TCMB provider codes are available.

## Data Sources

The project prioritizes official and institutional sources:

- TCMB payment systems participants.
- TCMB active payment institutions.
- TCMB active electronic money institutions.
- TCMB IBAN regulation and public IBAN documentation.

See `DATA_SOURCES.md` and `DATA_UPDATE_POLICY.md` before changing data.

## Development

```bash
python -m pip install -r tools/requirements.txt
npm ci
npm test
```

Useful commands:

- `npm run generate:data`
- `npm run validate:data`
- `npm run check:privacy`
- `npm run prepare:release`
- `npm -w packages/typescript pack --dry-run`

## Documentation

- `docs/API.md`
- `docs/RELEASE_PROCESS.md`
- `docs/ROADMAP.md`
- `docs/YONETIM_PANELI_INTEGRATION.md`
- `docs/GITHUB_COMMUNITY_FILES.md`

## Synthetic Fixtures Only

Fixtures are generated synthetically from official provider codes and artificial
account areas. Real IBANs, customer names, phone numbers, account owners, payroll
records, or screenshots containing personal financial data are not accepted in
issues, pull requests, examples, fixtures, or tests.

## Project Goal

See `PROJECT_GOAL.md` for the Turkish project target statement.

## Built with Divan

Bu proje Divan ile tasarlandı ve üretildi. Divan, paketin runtime bağımlılığı
değildir; yalnızca tasarım, planlama ve geliştirme sürecinde yardımcı araç
olarak kullanılmıştır.

## License

MIT. See `LICENSE`.
