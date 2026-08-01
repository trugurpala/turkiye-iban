# turkiye-iban-python Tasarimi

Bu belge, ayri `turkiye-iban-python` deposu ve PyPI paketi icin karar kaydidir.
Python istemcisi bu repository icine eklenmeyecek; bu projenin surumlenmis release
assetlerini, JSON Schema sozlesmesini ve sentetik fixture'larini tuketecektir.

## Repository ve Paket

| Alan | Karar |
| --- | --- |
| GitHub repository | `trugurpala/turkiye-iban-python` |
| PyPI paket adi | `turkiye-iban` |
| Python import adi | `turkiye_iban` |
| Minimum Python surumu | `3.10` |
| Lisans | `MIT` |
| Runtime ag istegi | Yok |
| Veri kaynagi | Sabitlenmis `turkiye-iban` GitHub Release assetleri |

## Public API Esitligi

Python istemcisi TypeScript paketindeki yedi temel davranisi korur. Fonksiyonlar
PEP 8 uyumlu snake_case ile yayinlanir. Donus nesneleri `dataclass(frozen=True)`
olarak tasarlanir; alan adlari JSON veri modeliyle uyumlu tutulur.

| Python fonksiyonu | TypeScript karsiligi | Donus |
| --- | --- | --- |
| `parse_iban(iban: str) -> ParsedTurkishIban` | `parseIban` | Ayrismis sonuc ve hata listesi |
| `validate_turkish_iban(iban: str) -> bool` | `validateTurkishIban` | Bicim ve MOD 97-10 sonucu |
| `get_bank_code_from_iban(iban: str) -> str | None` | `getBankCodeFromIban` | Bes haneli kod veya `None` |
| `find_bank_by_code(code: str) -> TurkishIbanProvider | None` | `findBankByCode` | Kurulus kaydi veya `None` |
| `identify_bank_from_iban(iban: str) -> IdentifiedTurkishIban` | `identifyBankFromIban` | IBAN ve kurulus sonucu |
| `format_iban(iban: str) -> str` | `formatIban` | Dordlu gruplu gosterim |
| `mask_iban(iban: str) -> str` | `maskIban` | Guvenli gosterim |

`provider_status` sonucu yalniz `"known"` veya `"unknown"` olabilir. `"known"`
kod eslesmesidir; hesap varligi, hesap sahibi, lisans statusu veya transfer
yapilabilirligi kaniti degildir.
Bu alan TypeScript API'deki `providerStatus` sonucunun Python karsiligidir.

## Veri Tuketimi

Ilk surum, `turkiye-iban` release `v0.2.1` assetlerini sabitler:

- `tr-banks.json`
- `tr-banks.schema.json`
- `valid.synthetic.json`
- `invalid.synthetic.json`
- `lookup.synthetic.json`
- `SHA256SUMS`

Paket release hazirliginda assetleri indirir, `SHA256SUMS` ile dogrular ve wheel
icine `turkiye_iban/data/` altinda gomulu olarak ekler. Runtime sirasinda ag
istegi yapmaz. Yeni veri surumu icin PR, once sabitlenen release tag'ini ve
checksum kayitlarini degistirir; pytest fixture kontrati gecmeden publish
yapilmaz.

## Test ve Kalite Kapilari

- pytest ortak sentetik fixture'lari calistirir.
- `valid.synthetic.json` icindeki tum kayitlar valid olmalidir.
- `invalid.synthetic.json` icindeki tum kayitlar invalid olmalidir.
- `lookup.synthetic.json` icindeki known ve unknown sonuclari TypeScript
  semantigiyle ayni olmalidir.
- `python -m build`, `twine check`, `pip install` clean venv smoke testi ve type
  check CI'da calisir.
- Gercek IBAN veya kisisel finansal veri fixture, README, issue veya testte
  kullanilmaz.

## Yayin

Uygulama repository'si [trugurpala/turkiye-iban-python](https://github.com/trugurpala/turkiye-iban-python)
adresindedir. GitHub release `v0.1.1` ve wheel/sdist assetleri yayinlanmistir;
PyPI index kaydi bu tarih itibariyla dogrulanmamistir.

PyPI yayini GitHub Actions OIDC trusted publishing ile yapilir. Yayindan once:

1. Release asset checksum dogrulamasi gecer.
2. pytest, type check ve build kontrolleri gecer.
3. Clean virtual environment icinde `pip install turkiye-iban` smoke testi
   planlanir.
4. Release notlari, tuketilen `turkiye-iban` release tag'ini ve checksum
   kaynagini belirtir.

PyPI provenance bilgisi ve trusted publishing durumu README, release notlari ve
workflow ciktisinda gorunur tutulur.

## Kapsam Disi

- Bu repository icine Python runtime paketi eklemek
- Runtime ag istegiyle canli TCMB kaynagi okumak
- Hesap varligini veya hesap sahibini dogrulamak
- TCMB onayli paket oldugunu ima etmek
