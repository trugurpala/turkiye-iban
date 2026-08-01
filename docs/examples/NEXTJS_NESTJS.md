# Next.js ve NestJS Sentetik Kullanim Ornekleri

Bu sayfadaki IBAN degerleri yalniz test icin uretilmis sentetik fixture'lardir.
Gercek IBAN, musteri adi, hesap sahibi veya finansal veri kullanmayin.

## Next.js Personel Formu

Client veya server action tarafinda girisi once bicimlendirin, sonra
`identifyBankFromIban` sonucunu kullanin. `providerStatus: "known"` ise kurulus
alani otomatik doldurulabilir.

```ts
import { formatIban, identifyBankFromIban, maskIban } from "tr-iban";

type BankSelection =
  | { state: "selected"; code: string; name: string; formattedIban: string }
  | { state: "blocked"; reason: string; maskedIban: string };

export function resolveBankSelection(inputValue: string): BankSelection {
  const formattedIban = formatIban(inputValue);
  const identified = identifyBankFromIban(formattedIban);

  if (!identified.parsed.isValid) {
    return {
      state: "blocked",
      reason: "IBAN bicimi veya kontrol basamaklari gecersiz.",
      maskedIban: maskIban(inputValue),
    };
  }

  if (identified.providerStatus !== "known" || identified.provider === null) {
    return {
      state: "blocked",
      reason: "Kurulus kodu bu veri surumunde taninmiyor.",
      maskedIban: maskIban(inputValue),
    };
  }

  return {
    state: "selected",
    code: identified.provider.code,
    name: identified.provider.nameOfficial,
    formattedIban,
  };
}

const known = resolveBankSelection("TR56000460ABC123DEF456GHIJ");

if (known.state === "selected") {
  known.code; // "00046"
  known.name; // "AKBANK T.A.S."
}
```

## Unknown Kurulus Kodu

`providerStatus: "unknown"` otomatik banka secimi yaptirmamalidir. Genel paket bu
sonucu IBAN checksum gecerliliginden ayri raporlar; personel veya odeme ekrani
gibi yerlerde kaydi kabul edip etmeme karari uygulamanin is kuralidir.

Yonetim-Paneli icin tercih edilen davranis daha siki tutulur: unknown sonucunda
banka temizlenir, manuel secim acilmaz, kayit engellenir ve veri surumu
incelenir.

```ts
const unknown = identifyBankFromIban("TR16999990ABC123DEF456GHIJ");

unknown.parsed.isValid; // true
unknown.providerCode; // "99999"
unknown.providerStatus; // "unknown"
unknown.provider; // null
```

## NestJS Backend Kontrolu

Frontend sonucu guvenlik siniri degildir. Backend ayni kontrolu tekrar etmeli ve
loglarda ham IBAN yerine `maskIban` kullanmalidir.

```ts
import {
  identifyBankFromIban,
  maskIban,
  type IdentifiedTurkishIban,
} from "tr-iban";

interface VerifiedIbanProvider {
  iban: string;
  providerCode: string;
  providerName: string;
  dataVersion: string;
}

export function verifyPayrollIban(iban: string): VerifiedIbanProvider {
  const identified: IdentifiedTurkishIban = identifyBankFromIban(iban);

  if (!identified.parsed.isValid) {
    throw new Error("IBAN bicimi veya kontrol basamaklari gecersiz.");
  }

  if (identified.providerStatus !== "known" || identified.provider === null) {
    throw new Error("IBAN kurulus kodu taninmiyor.");
  }

  return {
    iban: identified.parsed.normalized,
    providerCode: identified.provider.code,
    providerName: identified.provider.nameOfficial,
    dataVersion: identified.dataVersion,
  };
}

export function logRejectedIban(iban: string): Record<string, string> {
  return {
    iban: maskIban(iban),
    event: "iban_rejected",
  };
}
```

## Sinirlar

- Paket hesap varligini, hesap sahibini veya transfer yapilabilirligini
  dogrulamaz.
- `providerStatus: "known"` yalniz bes haneli kodun veri kumesinde eslestigini
  gosterir.
- Kurulus nesnesindeki `status` farkli bir alandir; acik faaliyet statusu kaniti
  yoksa `unknown` kalir.
- Public issue, PR, log ve orneklerde gercek IBAN kullanmayin.
