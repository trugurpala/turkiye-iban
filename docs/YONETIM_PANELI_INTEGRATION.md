# Yonetim-Paneli Integration

`turkiye-iban` should be consumed as an external dependency, not copied into the
Yonetim-Paneli repository.

## Frontend

Use `formatIban` while the user edits the IBAN field and `maskIban` anywhere the
IBAN is shown after entry. Do not show provider auto-detection as a guarantee
that the account exists.

```ts
import { formatIban, identifyBankFromIban } from "tr-iban";

const formatted = formatIban(inputValue);
const identified = identifyBankFromIban(formatted);

if (identified.parsed.isValid && identified.bank) {
  setSelectedBankCode(identified.bank.code);
}
```

## Backend

Repeat validation in NestJS before saving a personnel record. Never trust
frontend-only validation for payroll or personnel data.

```ts
import { identifyBankFromIban, maskIban } from "tr-iban";

const identified = identifyBankFromIban(dto.iban);

if (!identified.parsed.isValid) {
  throw new BadRequestException("IBAN formatı geçerli değil.");
}

logger.info({ iban: maskIban(dto.iban), providerCode: identified.bankCode }, "IBAN provider checked");
```

## Unknown Provider

If `identified.parsed.isValid` is true but `identified.isKnownProvider` is false,
keep manual bank/provider selection enabled. This means the IBAN format and
checksum are valid, but the bundled dataset does not know the provider code.

## Database Fallback

Applications that do not use NPM can import `data/tr-banks.sql` into their own
database and lookup by the five-digit `code` field.
