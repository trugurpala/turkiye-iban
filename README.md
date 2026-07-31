# turkiye-iban

[![CI](https://github.com/trugurpala/turkiye-iban/actions/workflows/ci.yml/badge.svg)](https://github.com/trugurpala/turkiye-iban/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/tr-iban)](https://www.npmjs.com/package/tr-iban)
[![GitHub Release](https://img.shields.io/github/v/release/trugurpala/turkiye-iban)](https://github.com/trugurpala/turkiye-iban/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Türkiye IBAN doğrulaması ve TCMB kaynaklı ödeme hizmeti sağlayıcı kodu eşlemesi
için dil bağımsız açık kaynak veri kümesi ve sıfır runtime bağımlılıklı
TypeScript/JavaScript paketi.

> [!IMPORTANT]
> Bu proje IBAN biçimini ve MOD 97-10 kontrol basamaklarını doğrular; IBAN'daki
> beş haneli sağlayıcı kodunu veri kümesiyle eşleştirir. Hesabın varlığını,
> hesap sahibini, ad-soyad eşleşmesini veya transfer yapılabilirliğini doğrulamaz.

## İçindekiler / What's Included

- `data/tr-banks.json`: şemalı ana veri çıktısı.
- `data/tr-banks.csv`: elektronik tablo ve ETL kullanımı.
- `data/tr-banks.sql`: doğrudan veritabanına aktarılabilir SQLite uyumlu çıktı.
- `fixtures/`: yalnız sentetik geçerli, geçersiz ve lookup örnekleri.
- `tr-iban`: ESM ve CommonJS destekli NPM paketi.
- Kaynak hash manifesti, çevrimdışı testler, gizlilik taraması ve release
  checksum'ları.

JSON, CSV ve SQL aynı üreticiden çıkar. JavaScript kullanmayan projeler paket
runtime'ına ihtiyaç duymadan bu dosyaları tüketebilir.

## Kurulum / Installation

NPM registry'den standart kurulum:

```bash
npm install tr-iban
```

Sürüme sabitlenmiş GitHub Release tarball'ı da doğrudan kurulabilir:

```bash
npm install https://github.com/trugurpala/turkiye-iban/releases/download/v0.1.0/tr-iban-0.1.0.tgz
```

Node.js 22 veya üzeri gerekir. Paketin runtime bağımlılığı yoktur.

## Kullanım / Usage

Aşağıdaki IBAN yalnız test amacıyla üretilmiş sentetik bir fixture'dır.

```ts
import {
  formatIban,
  identifyBankFromIban,
  maskIban,
  validateTurkishIban,
} from "tr-iban";

const iban = "TR510004609999000000000011";

validateTurkishIban(iban); // true
formatIban(iban); // "TR51 0004 6099 9900 0000 0000 11"
maskIban(iban); // "TR51 **** **** **** **** **00 11"

const result = identifyBankFromIban(iban);
result.providerCode; // "00046"
result.providerStatus; // "known"
result.provider?.nameOfficial; // "AKBANK T.A.Ş."
result.dataVersion; // "YYYY-MM-DD"
```

`providerStatus: "unknown"`, IBAN'ın biçim/checksum bakımından otomatik olarak
geçersiz olduğu anlamına gelmez. Yalnız kodun bu sürümdeki doğrulanmış TCMB
katılımcı kümesinde bulunmadığını söyler. Uygulamalar kendi risk politikalarını
ayrıca uygular; örneğin Yonetim-Paneli bu durumda banka seçmez ve kaydı engeller.

## API

| Fonksiyon | Sonuç |
| --- | --- |
| `parseIban` | TR IBAN alanlarını, normalize edilmiş değeri ve hata kodlarını döndürür. |
| `validateTurkishIban` | Biçim, uzunluk, rezerv alan ve MOD 97-10 kontrolünü yapar. |
| `getBankCodeFromIban` | Beş haneli sağlayıcı kodunu çıkarır. |
| `findBankByCode` | Doğrulanmış katılımcı kodunu veri kümesinde arar. |
| `identifyBankFromIban` | Parse ve lookup sonucunu `known/unknown` olarak birleştirir. |
| `formatIban` | IBAN'ı dörtlü gruplar halinde biçimler. |
| `maskIban` | İlk ve son dört karakter dışını maskeler. |

Ayrıntılı sözleşme: [docs/API.md](docs/API.md).

## Veri ve Kanıt Politikası

Otomatik eşleme kümesine yalnız TCMB Ödeme Sistemleri Katılımcıları listesinde
koduyla yayımlanan kuruluşlar girer. TCMB aktif ödeme kuruluşu ve elektronik para
kuruluşu listeleri tür/statü zenginleştirmesi için kullanılır; bu listelerde yer
almak tek başına IBAN sağlayıcı kodu kanıtı değildir.

Her kayıt kaynak URL'sini, erişim tarihini ve `codeEvidence` alanını taşır.
İndirilen resmî kaynakların SHA-256 değerleri `data/source-manifest.json` içinde
sürümle birlikte saklanır. Ayrıntılar için [DATA_SOURCES.md](DATA_SOURCES.md) ve
[DATA_UPDATE_POLICY.md](DATA_UPDATE_POLICY.md) dosyalarına bakın.

Schwifty yalnız MIT lisanslı karşılaştırma/test oracle'ı olabilir; ana veri
kaynağı değildir.

## Güvenlik ve Gizlilik

Gerçek IBAN, müşteri adı, hesap sahibi, telefon, bordro kaydı, banka dekontu veya
kişisel finansal veri issue, pull request, fixture, test ve örneklere kabul
edilmez. Güvenlik açığını public issue ile bildirmeyin; [Security
Policy](SECURITY.md) içindeki özel bildirim kanalını kullanın.

## Geliştirme / Development

```bash
python -m pip install -r tools/requirements.txt
npm ci
npm test
```

Veri güncellemesi ağ erişimi gerektirir ve normal testlerden ayrıdır:

```bash
npm run data:check-remote
npm run data:update
npm test
```

Katkı kuralları [CONTRIBUTING.md](CONTRIBUTING.md), yönetişim
[GOVERNANCE.md](GOVERNANCE.md), yayın süreci
[docs/RELEASE_PROCESS.md](docs/RELEASE_PROCESS.md) içindedir.

## Yol Haritası / Roadmap

İlk sürüm TypeScript/NPM ve dil bağımsız veriye odaklanır. PHP/Composer ikinci,
Python paketi sonraki fazdır. Tüm dil paketleri aynı kök veri ve fixture
sözleşmesini kullanacaktır. Bkz. [docs/ROADMAP.md](docs/ROADMAP.md).

## Divan ile Üretildi / Built with Divan

Bu proje Divan ile tasarlandı ve üretildi. Divan; araştırma, tasarım, planlama ve
geliştirme sürecinde kullanılmıştır, paketin runtime bağımlılığı değildir.

## Lisans / License

Kod ve proje belgeleri [MIT Lisansı](LICENSE) ile yayımlanır. Kaynak ve atıf
notları [NOTICE](NOTICE) dosyasındadır.
