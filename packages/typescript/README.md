# tr-iban

`tr-iban`, Türkiye'de kullanılan bir Uluslararası Banka Hesap Numarasının (IBAN) yazım kurallarına uygun olup olmadığını kontrol eder ve IBAN içindeki beş haneli kuruluş kodunu doğrulanmış Türkiye Cumhuriyet Merkez Bankası (TCMB) verileriyle eşleştirir.

> [!IMPORTANT]
> Paket hesabın varlığını, hesap sahibini veya para transferi yapılabilirliğini doğrulamaz. Yalnızca IBAN yazımını ve kuruluş kodu eşleşmesini kontrol eder.

## Kurulum

Node.js 22 veya üzeriyle paketi kurun:

```bash
npm install tr-iban
```

Paketin çalışırken yüklediği başka bir NPM bağımlılığı yoktur.

## İlk kullanım

Aşağıdaki IBAN yalnızca test amacıyla üretilmiştir:

```ts
import { identifyBankFromIban } from "tr-iban";

const result = identifyBankFromIban(
  "TR510004609999000000000011",
);

result.parsed.isValid; // true
result.providerCode; // "00046"
result.providerStatus; // "known"
result.provider?.nameOfficial; // "AKBANK T.A.Ş."
```

`isValid`, IBAN'ın ülke, uzunluk, karakter ve kontrol rakamı kurallarından geçip geçmediğini gösterir. `providerStatus: "known"` ise beş haneli kuruluş kodunun paket veri kümesinde bulunduğunu belirtir.

## Türkiye IBAN'ının bölümleri

Sentetik örnek `TR | 51 | 00046 | 0 | 9999000000000011` şeklinde ayrılır:

| Bölüm | Değer | Açıklama |
| --- | --- | --- |
| Ülke kodu | `TR` | IBAN'ın Türkiye'ye ait olduğunu gösterir |
| Kontrol rakamları | `51` | Yazım hatalarını matematiksel olarak kontrol eder |
| Kuruluş kodu | `00046` | Banka veya ödeme kuruluşunu tanımlar |
| Rezerv alanı | `0` | Türkiye IBAN standardında `0` olmalıdır |
| Hesap alanı | `9999000000000011` | 16 karakterdir ve harf içerebilir |

Paket hesap alanının bankada kayıtlı olup olmadığını kontrol etmez.

## MOD 97-10 nedir?

MOD 97-10, IBAN standardının yazım hatalarını yakalamak için kullandığı matematiksel kontrolün adıdır. Paket bu hesabı otomatik yapar.

Başarılı sonuç, IBAN'ın matematiksel olarak tutarlı yazıldığını gösterir. Hesabın bankada gerçekten bulunduğunu veya kime ait olduğunu göstermez.

## Bilinmeyen kuruluş kodu

`providerStatus: "unknown"` sonucu, IBAN'ın otomatik olarak hatalı olduğu anlamına gelmez. IBAN yazım ve kontrol rakamı kurallarından geçebilir, ancak beş haneli kod bu paket sürümündeki doğrulanmış veri kümesinde bulunmayabilir.

Bu durumda kuruluşu otomatik seçmeyin. Veri sürümünü veya uygulamanızın kabul politikasını kontrol edin.

## Biçimlendirme ve güvenli gösterim

Gerçek IBAN'ları loglara açık biçimde yazmayın. Gösterim ve hata mesajlarında `maskIban` kullanın:

```ts
import { formatIban, maskIban } from "tr-iban";

const iban = "TR510004609999000000000011";

formatIban(iban); // "TR51 0004 6099 9900 0000 0000 11"
maskIban(iban); // "TR51 **** **** **** **** **00 11"
```

## Kullanabileceğiniz fonksiyonlar

| Fonksiyon | Ne yapar? |
| --- | --- |
| `parseIban` | IBAN'ı bölümlerine ayırır ve hataları listeler |
| `validateTurkishIban` | Türkiye IBAN kurallarının geçerli olup olmadığını döndürür |
| `getBankCodeFromIban` | Beş haneli kuruluş kodunu çıkarır |
| `findBankByCode` | Kuruluş kodunu doğrulanmış veri kümesinde arar |
| `identifyBankFromIban` | IBAN kontrolünü ve kuruluş aramasını birleştirir |
| `formatIban` | IBAN'ı okunabilir gruplara ayırır |
| `maskIban` | IBAN'ın büyük bölümünü gizler |

Veri kaynakları, dil bağımsız JSON/CSV/SQL dosyaları ve katkı kuralları için [turkiye-iban GitHub deposuna](https://github.com/trugurpala/turkiye-iban) bakın.
