# tr-iban

TypeScript package for Turkish IBAN validation and provider-code lookup.

```ts
import { identifyBankFromIban } from "tr-iban";

const result = identifyBankFromIban("TR510004609999000000000011");
console.log(result.bank?.nameOfficial);
```

The package validates format and provider code only. It does not validate account
existence, account ownership, or transfer availability.
