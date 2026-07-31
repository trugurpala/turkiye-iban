# Sosyal Paylaşım Metinleri

## X

Türkiye IBAN doğrulama ve kuruluş kodu eşleştirme için açık kaynak `tr-iban` yayında.

TCMB kaynaklı veri · JSON/CSV/SQL · TypeScript/NPM · sıfır runtime bağımlılığı

https://github.com/trugurpala/turkiye-iban

Görsel: `docs/assets/launch/launch-horizontal.png`

## LinkedIn

Türkiye IBAN doğrulama ve banka/ödeme kuruluşu kodu eşleştirme işini her projede yeniden kurmamak için `turkiye-iban` projesini açık kaynak olarak yayımladık.

Proje bugün şunları sunuyor:

- TypeScript/NPM için sıfır runtime bağımlılıklı `tr-iban`
- PHP, Python ve veri uygulamaları için ortak JSON, CSV ve SQL çıktıları
- TCMB Ödeme Sistemleri Katılımcıları listesine dayalı kod kanıtı
- Kaynak SHA-256 takibi, sentetik fixture'lar, gizlilik taraması ve Node 22/24 CI

Önemli sınır: Paket IBAN yazımını ve kontrol rakamlarını doğrular, kuruluş kodunu eşleştirir. Hesabın varlığını, hesap sahibini veya transfer yapılabilirliğini doğrulamaz.

Proje MIT lisanslı ve topluluk için ücretsizdir. PHP/Composer, Python, kullanım örnekleri ve veri araçları için katkıya açıktır.

GitHub: https://github.com/trugurpala/turkiye-iban
NPM: https://www.npmjs.com/package/tr-iban

Görsel: `docs/assets/launch/launch-horizontal.png`

## TurkDev / Reddit

### Başlık

TCMB kaynaklı Türkiye IBAN kuruluş kodlarını JSON, CSV, SQL ve NPM paketi olarak açık kaynak yayımladık

### Metin

Merhaba,

Personel ve ödeme formlarında Türkiye IBAN'ından banka veya ödeme kuruluşunu bulmak için aynı veri ve doğrulama kodunun tekrar tekrar yazıldığını gördük. Bunun için `turkiye-iban` adında ücretsiz ve MIT lisanslı bir proje hazırladık.

Teknik tarafta en çok uğraştığımız konu, “aktif ödeme kuruluşu” bilgisini doğrudan IBAN kuruluş kodu saymamak oldu. Eşleştirme kümesine yalnız TCMB Ödeme Sistemleri Katılımcıları listesinde kod kanıtı bulunan kayıtlar giriyor. Diğer TCMB listeleri yalnız mevcut kaydın tür ve statüsünü zenginleştiriyor. Kaynakların SHA-256 parmak izleri tutuluyor; JSON, CSV ve SQL eşitliği ile sentetik IBAN fixture'ları CI'da test ediliyor.

TypeScript kullananlar `npm install tr-iban` ile başlayabilir. JavaScript kullanmayanlar aynı 70 kuruluş kaydını JSON, CSV veya SQL olarak doğrudan indirebilir.

Proje hesabın varlığını veya sahibini doğrulamıyor; yalnız IBAN biçimini, kontrol rakamlarını ve kuruluş kodu eşleşmesini ele alıyor. Gerçek IBAN kabul etmiyoruz.

Kaynak kodu ve veri zinciri: https://github.com/trugurpala/turkiye-iban

Özellikle API dili, veri kanıt modeli ve PHP/Python yol haritası hakkında teknik geri bildirim duymak isteriz.

Görsel: `docs/assets/launch/community-square.png`

## Kısa mesaj

Türkiye IBAN doğrulama ve TCMB kaynaklı kuruluş kodu verisi için ücretsiz açık kaynak proje: JSON, CSV, SQL ve `tr-iban` NPM paketi. https://github.com/trugurpala/turkiye-iban
