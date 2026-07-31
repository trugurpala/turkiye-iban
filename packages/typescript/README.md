# tr-iban

![tr-iban: Türkiye IBAN doğrulama ve kuruluş kodu verisi](https://raw.githubusercontent.com/trugurpala/turkiye-iban/main/docs/assets/github/hero.png)

[![Divan ile üretildi](https://img.shields.io/badge/Divan%20ile-%C3%BCretildi-087F8C)](https://github.com/trugurpala/divan)

`tr-iban`, Türkiye'de kullanılan bir Uluslararası Banka Hesap Numarasının (IBAN) yazım kurallarına uygun olup olmadığını kontrol eder ve IBAN içindeki beş haneli kuruluş kodunu doğrulanmış Türkiye Cumhuriyet Merkez Bankası (TCMB) verileriyle eşleştirir.

> [!IMPORTANT]
> Paket hesabın varlığını, hesap sahibini veya para transferi yapılabilirliğini doğrulamaz. Yalnızca IBAN yazımını ve kuruluş kodu eşleşmesini kontrol eder.

[Kurulum](#kurulum) · [İlk kullanım](#ilk-kullanım) · [Sonuçları yorumlama](#sonuçları-yorumlama) · [Verinin kaynağı](#verinin-kaynağı) · [API](#kullanabileceğiniz-fonksiyonlar)

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

## Kontrol rakamları neyi doğrular?

IBAN içindeki iki kontrol rakamı, diğer harf ve rakamların matematiksel olarak birbiriyle uyumlu olup olmadığını gösterir. Bu hesabın teknik adı MOD 97-10'dur; formülü bilmeniz gerekmez, paket kontrolü otomatik yapar.

Başarılı sonuç, IBAN'ın matematiksel olarak tutarlı yazıldığını gösterir. Hesabın bankada gerçekten bulunduğunu veya kime ait olduğunu göstermez.

## Sonuçları yorumlama

| Sonuç | Anlamı | Önerilen davranış |
| --- | --- | --- |
| `isValid: false` | Ülke, uzunluk, karakter, rezerv alanı veya kontrol rakamları hatalıdır | IBAN'ı kabul etmeyin |
| `isValid: true`, `providerStatus: "known"` | Yazım geçerlidir ve kuruluş kodu veri kümesinde bulunur | Kuruluş alanını otomatik doldurabilirsiniz |
| `isValid: true`, `providerStatus: "unknown"` | Yazım geçerlidir ancak kod bu veri sürümünde yoktur | Kuruluşu otomatik seçmeyin; veri sürümünü ve iş kuralınızı kontrol edin |

## Bilinmeyen kuruluş kodu

`providerStatus: "unknown"` sonucu, IBAN'ın otomatik olarak hatalı olduğu anlamına gelmez. IBAN yazım ve kontrol rakamı kurallarından geçebilir, ancak beş haneli kod bu paket sürümündeki doğrulanmış veri kümesinde bulunmayabilir.

Bu durumda kuruluşu otomatik seçmeyin. Veri sürümünü veya uygulamanızın kabul politikasını kontrol edin.

## Verinin kaynağı

Kuruluş eşleştirmesine yalnız TCMB Ödeme Sistemleri Katılımcıları listesinde koduyla yayımlanan kayıtlar girer. Aktif ödeme ve elektronik para kuruluşu sayfaları mevcut kayıtların tür ve statüsünü zenginleştirir; tek başına yeni bir IBAN kuruluş kodu üretmez.

Paket sürümlenmiş veriyle çalışır ve runtime sırasında ağ isteği yapmaz. Kaynak adresleri, erişim tarihleri ve SHA-256 dijital parmak izleri [ana projede](https://github.com/trugurpala/turkiye-iban#verinin-kaynağı) yayımlanır.

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

## Topluluğa katılın

Veri kaynakları, dil bağımsız JSON/CSV/SQL dosyaları ve katkı kuralları için [turkiye-iban GitHub deposuna](https://github.com/trugurpala/turkiye-iban) bakın. Sorular ve fikirler için [Discussions](https://github.com/trugurpala/turkiye-iban/discussions), hatalar ve resmî veri değişiklikleri için [issue formları](https://github.com/trugurpala/turkiye-iban/issues/new/choose) kullanılabilir.

Gerçek IBAN, müşteri adı, hesap sahibi veya başka kişisel finansal veri paylaşmayın. Proje yalnız sentetik test örneklerini kabul eder.

## Divan ile üretildi

Bu proje [Divan](https://github.com/trugurpala/divan) ile tasarlandı ve üretildi. Divan araştırma, teknik şartname, planlama, uygulama, doğrulama ve yayın sürecinde kullanıldı; `tr-iban` paketinin runtime bağımlılığı değildir.
