# turkiye-iban

[![CI](https://github.com/trugurpala/turkiye-iban/actions/workflows/ci.yml/badge.svg)](https://github.com/trugurpala/turkiye-iban/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/tr-iban)](https://www.npmjs.com/package/tr-iban)
[![GitHub Release](https://img.shields.io/github/v/release/trugurpala/turkiye-iban)](https://github.com/trugurpala/turkiye-iban/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Bu proje, Türkiye'de kullanılan Uluslararası Banka Hesap Numaralarının (IBAN) yazımını kontrol eder ve IBAN içindeki beş haneli kuruluş kodunu Türkiye Cumhuriyet Merkez Bankası (TCMB) verileriyle eşleştirir. Bir kod veri kümesinde bulunduğunda uygulamanız banka veya ödeme kuruluşu alanını otomatik doldurabilir.

> [!IMPORTANT]
> Paket bir hesabın gerçekten var olduğunu, kime ait olduğunu veya para transferine açık olduğunu doğrulamaz. Yalnızca IBAN'ın kurallara uygun yazıldığını ve içindeki kuruluş kodunun doğrulanmış veri kümesinde bulunup bulunmadığını kontrol eder.

## Ne işe yarar?

Paket bir Türkiye IBAN'ı için şu işlemleri yapar:

- IBAN'ın `TR` ile başladığını ve 26 karakterden oluştuğunu kontrol eder
- Eksik, fazla veya hatalı yazılmış karakterleri tespit eder
- IBAN'ın kontrol rakamlarını matematiksel olarak doğrular
- Beş haneli banka veya ödeme kuruluşu kodunu çıkarır
- Kodu doğrulanmış TCMB katılımcı verisiyle eşleştirir
- IBAN'ı okunabilir biçimde gruplar veya güvenli gösterim için maskeler

## Türkiye IBAN'ı nasıl okunur?

Türkiye IBAN'ı beş bölümden oluşur. Aşağıdaki sentetik örnekte bölümler `TR | 51 | 00046 | 0 | 9999000000000011` şeklinde ayrılır:

| Bölüm | Uzunluk | Örnekteki değer | Açıklama |
| --- | ---: | --- | --- |
| Ülke kodu | 2 karakter | `TR` | IBAN'ın Türkiye'ye ait olduğunu gösterir |
| Kontrol rakamları | 2 rakam | `51` | Yazım hatalarını matematiksel olarak kontrol eder |
| Kuruluş kodu | 5 rakam | `00046` | Banka veya ödeme kuruluşunu tanımlar |
| Rezerv alanı | 1 rakam | `0` | Türkiye IBAN standardında `0` olmalıdır |
| Hesap alanı | 16 karakter | `9999000000000011` | Kuruluşun kendi hesap tanımlama alanıdır ve harf içerebilir |

Paket hesap alanının bankada kayıtlı olup olmadığını kontrol etmez. Yalnızca alanın uzunluğunu ve izin verilen karakterleri doğrular.

## MOD 97-10 ne demek?

MOD 97-10, IBAN standardının yazım hatalarını yakalamak için kullandığı matematiksel kontrolün teknik adıdır. Paket bu hesabı sizin yerinize yapar; formülü bilmeniz gerekmez.

Kontrol başarılıysa IBAN'daki harf ve rakamlar birbiriyle matematiksel olarak uyumludur. Bu kontrol yanlış yazılmış bir rakamı yakalayabilir, ancak hesabın bankada gerçekten bulunduğunu kanıtlamaz.

## Sonuçları nasıl yorumlamalısınız?

IBAN doğrulaması ile kuruluş eşleştirmesi iki ayrı sonuçtur:

| Sonuç | Anlamı | Uygulama davranışı |
| --- | --- | --- |
| `isValid: false` | IBAN'ın ülkesi, uzunluğu, karakterleri, `0` olması gereken rezerv alanı veya kontrol rakamları hatalıdır | IBAN'ı kabul etmeyin |
| `isValid: true`, `providerStatus: "known"` | IBAN yazım kurallarına uygundur ve kuruluş kodu veri kümesinde bulunur | Kuruluş alanını otomatik doldurabilirsiniz |
| `isValid: true`, `providerStatus: "unknown"` | IBAN yazım kurallarına uygundur, ancak kuruluş kodu bu veri sürümünde bulunmaz | Kuruluşu otomatik seçmeyin; veri sürümünü ve kendi iş kuralınızı kontrol edin |

`unknown`, hesabın var olduğu anlamına gelmez. Yalnızca beş haneli kodun kullanılan veri sürümünde eşleşmediğini belirtir.

## Hangi çıktıyı kullanmalısınız?

JavaScript kullanmayan uygulamalar da aynı kuruluş listesinden yararlanabilir:

| Kullanım alanı | Önerilen çıktı |
| --- | --- |
| TypeScript, Next.js, NestJS veya Node.js | NPM paketi `tr-iban` |
| PHP veya Python | `data/tr-banks.json` |
| Excel, veri aktarımı veya raporlama | `data/tr-banks.csv` |
| Doğrudan veritabanı kullanımı | `data/tr-banks.sql` |

PHP/Composer ve Python paketleri yol haritasındadır. JSON, CSV ve SQL dosyaları bugün doğrudan kullanılabilir.

## Kurulum

Node.js 22 veya üzeriyle paketi NPM paket deposundan kurun:

```bash
npm install tr-iban
```

Belirli bir sürümün GitHub Release paketini doğrudan kurmak için:

```bash
npm install https://github.com/trugurpala/turkiye-iban/releases/download/v0.1.0/tr-iban-0.1.0.tgz
```

Paketin çalışırken yüklediği başka bir NPM bağımlılığı yoktur.

## İlk kullanım

Aşağıdaki IBAN yalnızca test için üretilmiştir ve gerçek bir hesaba ait değildir:

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

Önce `result.parsed.isValid` değerini kontrol edin. Değer `true` ise `providerStatus` sonucuna göre kuruluşu otomatik seçip seçmeyeceğinize karar verin.

## Biçimlendirme ve maskeleme

Gerçek IBAN'ları loglara veya hata mesajlarına açık biçimde yazmayın. Ekranda gösterirken `maskIban` kullanın:

```ts
import { formatIban, maskIban } from "tr-iban";

const iban = "TR510004609999000000000011";

formatIban(iban); // "TR51 0004 6099 9900 0000 0000 11"
maskIban(iban); // "TR51 **** **** **** **** **00 11"
```

`formatIban` yalnızca okunabilirliği artırır. `maskIban`, IBAN'ın büyük bölümünü gizleyerek ekranda veya hata mesajında gereksiz kişisel veri gösterilmesini önler.

## Kullanabileceğiniz fonksiyonlar

| Fonksiyon | Ne yapar? |
| --- | --- |
| `parseIban` | IBAN'ı bölümlerine ayırır ve bulunan hataları listeler |
| `validateTurkishIban` | Türkiye IBAN yazım kurallarının ve kontrol rakamlarının geçerli olup olmadığını döndürür |
| `getBankCodeFromIban` | IBAN içindeki beş haneli kuruluş kodunu çıkarır |
| `findBankByCode` | Verilen kuruluş kodunu doğrulanmış veri kümesinde arar |
| `identifyBankFromIban` | IBAN kontrolünü ve kuruluş aramasını tek sonuçta birleştirir |
| `formatIban` | IBAN'ı dörder karakterlik gruplara ayırır |
| `maskIban` | IBAN'ın büyük bölümünü yıldız karakteriyle gizler |

Tüm alanlar, dönüş tipleri ve hata kodları için [API belgesine](docs/API.md) bakın.

## Veri dosyaları

Proje aynı kuruluş listesini farklı kullanım biçimleriyle yayımlar:

- `data/tr-banks.json`: uygulamalar için ana veri dosyası
- `data/tr-banks.csv`: elektronik tablo ve veri aktarımı için satır tabanlı çıktı
- `data/tr-banks.sql`: SQLite ile uyumlu veritabanı aktarımı
- `fixtures/`: yalnızca sentetik, yani gerçek kişilere ait olmayan test IBAN'ları
- `data/source-manifest.json`: kullanılan resmî kaynakların değişmediğini denetleyen dijital parmak izleri (SHA-256)

JSON, CSV ve SQL dosyaları aynı kaynaktan üretilir. Bu nedenle farklı dillerdeki uygulamalar aynı kuruluş kodlarını kullanır.

## Kuruluş kodları nereden geliyor?

Otomatik eşleştirmeye yalnızca TCMB Ödeme Sistemleri Katılımcıları listesinde koduyla birlikte yayımlanan kuruluşlar girer. Bir şirketin aktif ödeme veya elektronik para kuruluşu listesinde bulunması, tek başına IBAN kuruluş kodu kanıtı sayılmaz.

Her veri kaydı kaynak adresini, kaynağa erişilen tarihi ve kodun hangi kanıta dayandığını içerir. Ayrıntılar için [veri kaynaklarını](DATA_SOURCES.md) ve [veri güncelleme politikasını](DATA_UPDATE_POLICY.md) okuyun.

Schwifty projesi yalnızca karşılaştırma ve test amacıyla kullanılabilir. Ana veri kaynağı TCMB'dir.

## Güvenlik ve gizlilik

GitHub issue, pull request, test veya örneklere gerçek IBAN, müşteri adı, hesap sahibi, telefon numarası, bordro kaydı ya da banka dekontu eklemeyin. Bu proje yalnızca sentetik test verisi kabul eder.

Bir güvenlik açığı bulursanız public issue açmayın. [Güvenlik politikasındaki](SECURITY.md) özel bildirim kanalını kullanın.

## Projeye katkı

Geliştirme ortamını hazırlayıp tüm kontrolleri çalıştırmak için:

```bash
python -m pip install -r tools/requirements.txt
npm ci
npm test
```

Resmî kaynaklardan veri güncellemek ağ bağlantısı gerektirir:

```bash
npm run data:check-remote
npm run data:update
npm test
```

Katkı kuralları [CONTRIBUTING.md](CONTRIBUTING.md), proje yönetimi [GOVERNANCE.md](GOVERNANCE.md), yayın adımları ise [yayın süreci belgesinde](docs/RELEASE_PROCESS.md) açıklanır.

## Yol haritası

İlk sürüm TypeScript/NPM paketini ve dil bağımsız veri dosyalarını içerir. PHP/Composer ikinci, Python paketi sonraki aşamadır. Güncel planı [yol haritasında](docs/ROADMAP.md) görebilirsiniz.

## Divan ile üretildi

Bu proje Divan ile tasarlandı ve üretildi. Divan araştırma, tasarım, planlama ve geliştirme sürecinde kullanıldı; paketi kullanmak için Divan gerekmez.

## Lisans

Kod ve proje belgeleri [MIT Lisansı](LICENSE) ile yayımlanır. Kaynak ve atıf notları [NOTICE](NOTICE) dosyasındadır.
