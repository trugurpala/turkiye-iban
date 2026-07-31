# API

The first package is `tr-iban` for TypeScript and JavaScript runtimes.

## Functions

### `parseIban(input)`

Normalizes a value, splits it into Turkish IBAN parts, validates format and
checksum, and returns structured errors.

### `validateTurkishIban(input)`

Returns `true` when the input is a valid Turkish IBAN shape with valid MOD 97-10
check digits. It does not require the provider code to be known in the bundled
dataset.

### `getBankCodeFromIban(input)`

Returns the five-digit provider code from the IBAN or `null` when the input is
not long enough to contain one.

### `findBankByCode(code)`

Looks up a provider by raw or normalized code. `46`, `0046`, and `00046` all
resolve to the same provider code.

### `identifyBankFromIban(input)`

Combines parsing and provider lookup. A result can be format-valid while
`isKnownProvider` is false.

### `formatIban(input)`

Formats a normalized IBAN in four-character groups.

### `maskIban(input)`

Keeps the first four and last four characters visible, masking the middle.

## Privacy

Do not log the raw input value in application code. Use `maskIban` for user
interface display, audit notes, and error messages.
