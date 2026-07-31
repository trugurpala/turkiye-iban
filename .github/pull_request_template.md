## Summary

Describe the change.

## Type

- [ ] Code
- [ ] Data
- [ ] Documentation
- [ ] Governance or policy

## Data Source

If this changes provider data, include the official source URL and date checked.

## Privacy

- [ ] This pull request contains no real IBANs, customer names, account owner data, phone numbers, payroll data, screenshots, or private financial data.
- [ ] Fixtures and examples are synthetic.

## Verification

- [ ] `npm run data:update` (only when official data changed)
- [ ] `npm test`
- [ ] `npm pack --workspace packages/typescript --dry-run` (when package contents changed)
