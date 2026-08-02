# turkiye-iban-php Tasarimi

Bu belge, ayri `turkiye-iban-php` deposu ve Composer paketi icin karar kaydidir.
PHP istemcisi bu repository icine eklenmeyecek; bu projenin surumlenmis release
assetlerini, JSON Schema sozlesmesini ve sentetik fixture'larini tuketecektir.

## Repository ve Paket

| Alan | Karar |
| --- | --- |
| GitHub repository | `trugurpala/turkiye-iban-php` |
| Composer paket adi | `trugurpala/turkiye-iban` |
| PHP namespace | `TurkiyeIban` |
| Minimum PHP surumu | `8.2` |
| Lisans | `MIT` |
| Runtime ag istegi | Yok |
| Veri kaynagi | Sabitlenmis `turkiye-iban` GitHub Release assetleri |

## Public API Esitligi

PHP istemcisi TypeScript paketindeki yedi temel davranisi korur. Fonksiyonlar
snake_case ile yayinlanir; sinif temelli servis yalniz bu fonksiyonlari cagiran
ince bir uyumluluk katmani olabilir.

| PHP fonksiyonu | TypeScript karsiligi | Donus |
| --- | --- | --- |
| `parse_iban(string $iban): ParsedTurkishIban` | `parseIban` | Ayrismis sonuc ve hata listesi |
| `validate_turkish_iban(string $iban): bool` | `validateTurkishIban` | Bicim ve MOD 97-10 sonucu |
| `get_bank_code_from_iban(string $iban): ?string` | `getBankCodeFromIban` | Bes haneli kod veya `null` |
| `find_bank_by_code(string $code): ?TurkishIbanProvider` | `findBankByCode` | Kurulus kaydi veya `null` |
| `identify_bank_from_iban(string $iban): IdentifiedTurkishIban` | `identifyBankFromIban` | IBAN ve kurulus sonucu |
| `format_iban(string $iban): string` | `formatIban` | Dordlu gruplu gosterim |
| `mask_iban(string $iban): string` | `maskIban` | Guvenli gosterim |

`providerStatus` sonucu yalniz `"known"` veya `"unknown"` olabilir. `"known"` kod
eslesmesidir; hesap varligi, hesap sahibi, lisans statusu veya transfer
yapilabilirligi kaniti degildir.

## Veri Tuketimi

Ilk surum, `turkiye-iban` release `v0.2.1` assetlerini sabitler:

- `tr-banks.json`
- `tr-banks.schema.json`
- `valid.synthetic.json`
- `invalid.synthetic.json`
- `lookup.synthetic.json`
- `SHA256SUMS`

Paket release hazirliginda assetleri indirir, `SHA256SUMS` ile dogrular ve
paketin icine `resources/` altinda gomulu olarak ekler. Runtime sirasinda ag
istegi yapmaz. Yeni veri surumu icin PR, once sabitlenen release tag'ini ve
checksum kayitlarini degistirir; PHPUnit fixture kontrati gecmeden publish
yapilmaz.

## Test ve Kalite Kapilari

- PHPUnit ortak sentetik fixture'lari calistirir.
- `valid.synthetic.json` icindeki tum kayitlar valid olmalidir.
- `invalid.synthetic.json` icindeki tum kayitlar invalid olmalidir.
- `lookup.synthetic.json` icindeki known ve unknown sonuclari TypeScript
  semantigiyle ayni olmalidir.
- Gercek IBAN veya kisisel finansal veri fixture, README, issue veya testte
  kullanilmaz.
- Composer package audit, static analysis ve clean install smoke testi CI'da
  calisir.

## Yayin

Uygulama repository'si [trugurpala/turkiye-iban-php](https://github.com/trugurpala/turkiye-iban-php)
adresindedir. GitHub release `v0.1.5` yayinlanmistir; Packagist index kaydi bu
tarih itibariyla dogrulanmamistir. Ayrintili adimlar [package index yayin
durumu](../PACKAGE_INDEX_PUBLICATION.md) belgesindedir.
Tek tek public API testleri [PHP Test Report](https://github.com/trugurpala/turkiye-iban-php/blob/main/TEST_REPORT.md)
belgesinde, paralel Python istemcisi ise [turkiye-iban-python](https://github.com/trugurpala/turkiye-iban-python)
adresinde bulunur.

Packagist yayini GitHub Actions uzerinden yapilir. Yayindan once:

1. Release asset checksum dogrulamasi gecer.
2. PHPUnit ve static analysis gecer.
3. Clean Composer project icinde `composer require trugurpala/turkiye-iban`
   smoke testi planlanir.
4. Release notlari, tuketilen `turkiye-iban` release tag'ini ve checksum
   kaynagini belirtir.

Packagist provenance veya trusted publishing destegi kullanilamayan noktalarda
sinir acikca README ve release notlarinda belirtilir; destek varmis gibi
sunulmaz.

## Kapsam Disi

- Bu repository icine PHP kodu eklemek
- Runtime ag istegiyle canli TCMB kaynagi okumak
- Hesap varligini veya hesap sahibini dogrulamak
- TCMB onayli paket oldugunu ima etmek
