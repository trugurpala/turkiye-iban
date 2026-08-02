# turkiye-iban-python Tasarımı

Bu belge, ayrı `turkiye-iban-python` deposu ve PyPI paketi için karar kaydıdır.
Python istemcisi bu repository içine eklenmeyecek; bu projenin sürümlenmiş release
assetlerini, JSON Schema sözleşmesini ve sentetik fixture'larını tüketecektir.

## Repository ve Paket

| Alan | Karar |
| --- | --- |
| GitHub repository | `trugurpala/turkiye-iban-python` |
| PyPI paket adı | `turkiye-iban` |
| Python import adı | `turkiye_iban` |
| Minimum Python sürümü | `3.10` |
| Lisans | `MIT` |
| Runtime ağ isteği | Yok |
| Veri kaynağı | Sabitlenmiş `turkiye-iban` GitHub Release assetleri |

## Public API Eşitliği

Python istemcisi TypeScript paketindeki yedi temel davranışı korur. Fonksiyonlar
PEP 8 uyumlu snake_case ile yayınlanır. Dönüş nesneleri `dataclass(frozen=True)`
olarak tasarlanır; alan adları JSON veri modeliyle uyumlu tutulur.

| Python fonksiyonu | TypeScript karşılığı | Dönüş |
| --- | --- | --- |
| `parse_iban(iban: str) -> ParsedTurkishIban` | `parseIban` | Ayrışmış sonuç ve hata listesi |
| `validate_turkish_iban(iban: str) -> bool` | `validateTurkishIban` | Biçim ve MOD 97-10 sonucu |
| `get_bank_code_from_iban(iban: str) -> str | None` | `getBankCodeFromIban` | Beş haneli kod veya `None` |
| `find_bank_by_code(code: str) -> TurkishIbanProvider | None` | `findBankByCode` | Kuruluş kaydı veya `None` |
| `identify_bank_from_iban(iban: str) -> IdentifiedTurkishIban` | `identifyBankFromIban` | IBAN ve kuruluş sonucu |
| `format_iban(iban: str) -> str` | `formatIban` | Dörtlü gruplu gösterim |
| `mask_iban(iban: str) -> str` | `maskIban` | Güvenli gösterim |

`provider_status` sonucu yalnız `"known"` veya `"unknown"` olabilir. `"known"`
kod eşleşmesidir; hesap varlığı, hesap sahibi, lisans statüsü veya transfer
yapılabilirliği kanıtı değildir.
Bu alan TypeScript API'deki `providerStatus` sonucunun Python karşılığıdır.

## Veri Tüketimi

İlk sürüm, `turkiye-iban` release `v0.2.1` assetlerini sabitler:

- `tr-banks.json`
- `tr-banks.schema.json`
- `valid.synthetic.json`
- `invalid.synthetic.json`
- `lookup.synthetic.json`
- `SHA256SUMS`

Paket release hazırlığında assetleri indirir, `SHA256SUMS` ile doğrular ve wheel
içine `turkiye_iban/data/` altında gömülü olarak ekler. Runtime sırasında ağ
isteği yapmaz. Yeni veri sürümü için PR, önce sabitlenen release tag'ini ve
checksum kayıtlarını değiştirir; pytest fixture kontratı geçmeden publish
yapılmaz.

## Test ve Kalite Kapıları

- pytest ortak sentetik fixture'ları çalıştırır.
- `valid.synthetic.json` içindeki tüm kayıtlar valid olmalıdır.
- `invalid.synthetic.json` içindeki tüm kayıtlar invalid olmalıdır.
- `lookup.synthetic.json` içindeki known ve unknown sonuçları TypeScript
  semantiğiyle aynı olmalıdır.
- `python -m build`, `twine check`, `pip install` clean venv smoke testi ve type
  check CI'da çalışır.
- Gerçek IBAN veya kişisel finansal veri fixture, README, issue veya testte
  kullanılmaz.

## Yayın

Uygulama repository'si [trugurpala/turkiye-iban-python](https://github.com/trugurpala/turkiye-iban-python)
adresindedir. GitHub release `v0.1.5` ve wheel/sdist assetleri yayınlanmıştır;
[PyPI `turkiye-iban==0.1.5`](https://pypi.org/project/turkiye-iban/0.1.5/)
yayınlanmış ve temiz virtualenv kurulumu sentetik IBAN smoke testiyle
doğrulanmıştır. Ayrıntılı adımlar
[package index yayın durumu](../PACKAGE_INDEX_PUBLICATION.md) belgesindedir.
Tek tek public API testleri [Python Test Report](https://github.com/trugurpala/turkiye-iban-python/blob/main/TEST_REPORT.md)
belgesinde, paralel PHP istemcisi ise [turkiye-iban-php](https://github.com/trugurpala/turkiye-iban-php)
adresinde bulunur.

PyPI yayını GitHub Actions OIDC trusted publishing ile yapılır. Yayından önce:

1. Release asset checksum doğrulaması geçer.
2. pytest, type check ve build kontrolleri geçer.
3. Clean virtual environment içinde `pip install turkiye-iban` smoke testi
   planlanır.
4. Release notları, tüketilen `turkiye-iban` release tag'ini ve checksum
   kaynağını belirtir.

PyPI provenance bilgisi ve trusted publishing durumu README, release notları ve
workflow çıktısında görünür tutulur.

## Kapsam Dışı

- Bu repository içine Python runtime paketi eklemek
- Runtime ağ isteğiyle canlı TCMB kaynağı okumak
- Hesap varlığını veya hesap sahibini doğrulamak
- TCMB onaylı paket olduğunu ima etmek
