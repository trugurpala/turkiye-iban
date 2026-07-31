# tr-iban

Türkiye IBAN biçimi/checksum doğrulaması ve TCMB kaynaklı sağlayıcı kodu eşlemesi
için sıfır runtime bağımlılıklı ESM/CommonJS paketi.

```bash
npm install tr-iban
```

```ts
import { identifyBankFromIban } from "tr-iban";

// Sentetik test fixture'ı; gerçek hesap değildir.
const result = identifyBankFromIban("TR510004609999000000000011");

result.parsed.isValid; // true
result.providerCode; // "00046"
result.providerStatus; // "known"
result.provider?.nameOfficial; // "AKBANK T.A.Ş."
```

API: `parseIban`, `validateTurkishIban`, `getBankCodeFromIban`,
`findBankByCode`, `identifyBankFromIban`, `formatIban`, `maskIban`.

`providerStatus: "unknown"` yalnız kodun paket veri sürümünde bulunmadığını
belirtir; hesap varlığını veya sahibini hiçbir sonuç doğrulamaz. Gerçek IBAN'ları
loglamayın; gösterim ve hata mesajlarında `maskIban` kullanın.

Ana proje, veri kaynakları ve katkı politikası:
https://github.com/trugurpala/turkiye-iban
