# Synthetic Test Data

This repository contains no real customer, account-holder or production IBAN
data. Every IBAN-shaped test value is generated for this project and marked
with `"synthetic": true`.

## Fixture Sets

- `fixtures/valid.synthetic.json` contains one checksum-valid synthetic IBAN
  per reviewed institution code.
- `fixtures/invalid.synthetic.json` covers checksum, country, length,
  character and reserve-field failures.
- `fixtures/lookup.synthetic.json` separates checksum validity from known and
  unknown provider-code lookup.

The generator uses reserved-looking account fields beginning with `9999` and
computes MOD 97-10 check digits locally. The fixtures demonstrate parser
behavior only; they do not prove that an account exists or can receive money.

## Contribution Rule

Do not replace a fixture with a bank statement, payroll record, customer
support example, screenshot, log line or an IBAN copied from a real system. A
new test case must be generated synthetically and carry the explicit marker.

`scripts/check-privacy.py` scans tracked text, normalizes compact or spaced
Turkish IBAN candidates, and permits only values present in marked fixture
files. Unknown candidates fail CI; diagnostic output reports only the file path
and character offset, never any part of the candidate value.
