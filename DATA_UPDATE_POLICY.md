# Data Update Policy

## Update Cadence

Check official sources before each release and at least once per month while the
project is active.

## Update Process

1. Fetch official TCMB sources.
2. Regenerate JSON, CSV, SQL, TypeScript generated data, and fixtures.
3. Run tests.
4. Review the diff for renamed, added, removed, or status-changed providers.
5. Cite the source and retrieval date in the release notes.

## Provider Code Normalization

TCMB source tables may show three- or four-digit institution codes. Turkish IBANs
encode the provider field as five digits, so the generated dataset stores:

- `rawCode`: the official code exactly as listed.
- `code`: the IBAN provider field, left-padded to five digits.

## Removal Policy

Do not silently delete providers. If an official source marks a provider as no
longer active, keep the record and update `status` when enough source evidence
exists. Removal from active source tables alone should be reviewed carefully.

## Privacy Policy

No real IBAN, account owner, customer, employee, payroll, phone, or transfer
data may be committed. All fixtures must be synthetic.
