# Cross-language conformance

Bu klasör, TypeScript/NPM, PHP ve Python istemcilerinin aynı davranış
sözleşmesine uyduğunu makine tarafından doğrulamak için kullanılır.

## Sözleşme

- `manifest.json`: contract sürümü, veri sürümü, fixture dosyaları ve SHA-256
  özetleri.
- `schema.json`: manifest JSON Schema'sı.
- `../fixtures/*.synthetic.json`: tek kanonik sentetik fixture kümesi.

Fixture dosyaları elle düzenlenmez. `data/source/institutions.json` değiştiğinde
`npm run generate:data` ile yeniden üretilir. `npm run validate:data` manifesti,
fixture checksum'larını ve sentetiklik kurallarını doğrular.

## İstemci kuralı

İstemci repository'leri yayınladıkları sürümde ana repo release'inin fixture
dosyalarını ve `manifest.json` kaydını kullanmalıdır. Her dil şu davranışları
aynı anlamla uygulamalıdır:

- IBAN yapısı ve MOD 97-10 kontrolü
- kuruluş kodu çıkarma ve kuruluş eşleştirme
- bilinmeyen kodda `unknown` sonucu
- formatlama ve maskeleme
- hesabın varlığını veya transfer yapılabilirliğini doğrulamama

Yeni bir fixture veya davranış eklenirse `contractVersion` değerlendirilir;
geriye dönük uyumlu eklemeler minor, kırıcı sözleşme değişiklikleri major sürüm
gerektirir.
