# turkiye-iban-php Tasarımı

Bu belge, ayrı `turkiye-iban-php` deposu ve Composer paketi için karar kaydıdır.
PHP istemcisi bu repository içine eklenmeyecek; bu projenin sürümlenmiş release
assetlerini, JSON Schema sözleşmesini ve sentetik fixture'larını tüketecektir.

## Repository ve Paket

| Alan | Karar |
| --- | --- |
| GitHub repository | `trugurpala/turkiye-iban-php` |
| Composer paket adı | `trugurpala/turkiye-iban` |
| PHP namespace | `TurkiyeIban` |
| Minimum PHP sürümü | `8.2` |
| Lisans | `MIT` |
| Runtime ağ isteği | Yok |
| Veri kaynağı | Sabitlenmiş `turkiye-iban` GitHub Release assetleri |

## Public API Eşitliği

PHP istemcisi TypeScript paketindeki yedi temel davranışı korur. Fonksiyonlar
snake_case ile yayınlanır; sınıf temelli servis yalnız bu fonksiyonları çağıran
ince bir uyumluluk katmanı olabilir.

| PHP fonksiyonu | TypeScript karşılığı | Dönüş |
| --- | --- | --- |
| `parse_iban(string $iban): ParsedTurkishIban` | `parseIban` | Ayrışmış sonuç ve hata listesi |
| `validate_turkish_iban(string $iban): bool` | `validateTurkishIban` | Biçim ve MOD 97-10 sonucu |
| `get_bank_code_from_iban(string $iban): ?string` | `getBankCodeFromIban` | Beş haneli kod veya `null` |
| `find_bank_by_code(string $code): ?TurkishIbanProvider` | `findBankByCode` | Kuruluş kaydı veya `null` |
| `identify_bank_from_iban(string $iban): IdentifiedTurkishIban` | `identifyBankFromIban` | IBAN ve kuruluş sonucu |
| `format_iban(string $iban): string` | `formatIban` | Dörtlü gruplu gösterim |
| `mask_iban(string $iban): string` | `maskIban` | Güvenli gösterim |

`providerStatus` sonucu yalnız `"known"` veya `"unknown"` olabilir. `"known"` kod
eşleşmesidir; hesap varlığı, hesap sahibi, lisans statüsü veya transfer
yapılabilirliği kanıtı değildir.

## Veri Tüketimi

İlk sürüm, `turkiye-iban` release `v0.2.1` assetlerini sabitler:

- `tr-banks.json`
- `tr-banks.schema.json`
- `valid.synthetic.json`
- `invalid.synthetic.json`
- `lookup.synthetic.json`
- `SHA256SUMS`

Paket release hazırlığında assetleri indirir, `SHA256SUMS` ile doğrular ve
paketin içine `resources/` altında gömülü olarak ekler. Runtime sırasında ağ
isteği yapmaz. Yeni veri sürümü için PR, önce sabitlenen release tag'ini ve
checksum kayıtlarını değiştirir; PHPUnit fixture kontratı geçmeden publish
yapılmaz.

## Test ve Kalite Kapıları

- PHPUnit ortak sentetik fixture'ları çalıştırır.
- `valid.synthetic.json` içindeki tüm kayıtlar valid olmalıdır.
- `invalid.synthetic.json` içindeki tüm kayıtlar invalid olmalıdır.
- `lookup.synthetic.json` içindeki known ve unknown sonuçları TypeScript
  semantiğiyle aynı olmalıdır.
- Gerçek IBAN veya kişisel finansal veri fixture, README, issue veya testte
  kullanılmaz.
- Composer package audit, static analysis ve clean install smoke testi CI'da
  çalışır.

## Yayın

Uygulama repository'si [trugurpala/turkiye-iban-php](https://github.com/trugurpala/turkiye-iban-php)
adresindedir. GitHub release `v0.1.5` yayınlanmıştır; Packagist index kaydı bu
tarih itibarıyla doğrulanmamıştır. Ayrıntılı adımlar [package index yayın
durumu](../PACKAGE_INDEX_PUBLICATION.md) belgesindedir.
Tek tek public API testleri [PHP Test Report](https://github.com/trugurpala/turkiye-iban-php/blob/main/TEST_REPORT.md)
belgesinde, paralel Python istemcisi ise [turkiye-iban-python](https://github.com/trugurpala/turkiye-iban-python)
adresinde bulunur.

Packagist yayını GitHub Actions üzerinden yapılır. Yayından önce:

1. Release asset checksum doğrulaması geçer.
2. PHPUnit ve static analysis geçer.
3. Clean Composer project içinde `composer require trugurpala/turkiye-iban`
   smoke testi planlanır.
4. Release notları, tüketilen `turkiye-iban` release tag'ini ve checksum
   kaynağını belirtir.

Packagist provenance veya trusted publishing desteği kullanılamayan noktalarda
sınır açıkça README ve release notlarında belirtilir; destek varmış gibi
sunulmaz.

## Kapsam Dışı

- Bu repository içine PHP kodu eklemek
- Runtime ağ isteğiyle canlı TCMB kaynağı okumak
- Hesap varlığını veya hesap sahibini doğrulamak
- TCMB onaylı paket olduğunu ima etmek
