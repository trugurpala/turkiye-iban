# Veri Güncelleme Politikası

Canlı bir kaynağın değişmesi, canonical verinin otomatik değişeceği anlamına
gelmez. Kaynak kontrolü yalnız değişikliği tespit eder ve inceleme raporu üretir.

## Güvenli Akış

1. `npm run data:check-remote` resmî kaynakları indirir.
2. Hashler canonical katalogla karşılaştırılır.
3. Birincil katılımcı kaynağı normalize edilir.
4. Mevcut snapshot ile eklenen, kaldırılan ve değişen kayıt farkı çıkarılır.
5. Kaynak değişimi, parser hatası veya kayıt farkı varsa kontrol başarısız olur.
6. Scheduled workflow açık bir inceleme issue'su oluşturur veya mevcut issue'yu günceller.
7. Maintainer resmî belgeyi ve farkı doğruladıktan sonra canonical dosyayı elle günceller.
8. `npm run generate:data && npm test` bütün dağıtım dosyalarını yeniden üretir ve doğrular.
9. CHANGELOG ve release etkisi belgelendikten sonra PR normal incelemeden geçer.

Otomasyon canonical veriyi, NPM paketini veya GitHub Release'i kendi başına
değiştiremez.

## Canonical Değişiklik Kuralları

- Yalnız `data/source/institutions.json` elle düzenlenir.
- `data/tr-banks.*`, package data, TypeScript generated data ve fixture'lar elle düzenlenmez.
- Kodlar beş haneli ve benzersiz, kayıtlar kod sırasındadır.
- Her kayıt en az bir geçerli `sourceIds` referansı taşır.
- `monitor_only` kaynak tek başına yeni provider kodu üretemez.
- `active` veya `inactive` statüsü, kayda bağlı açık `institution_status`
  kanıtı olmadan yayımlanamaz; bu durumda değer `unknown` kalır.
- Silinen kayıt sessizce kaybolmaz; gerekçe CHANGELOG ve PR'da açıklanır.
- Şüpheli veya çelişkili kanıt `unknown` veya ertelenmiş inceleme olarak kalır.

## Deterministik Üretim

Normal üretim ağ kullanmaz ve sistem saatini çıktıya yazmaz. Aynı canonical
snapshot aynı JSON, CSV, SQL, SQLite, TypeScript ve fixture içeriğini üretir.
`npm run check:generated` geçici dizinde tekrar üretip byte düzeyinde drift
kontrolü yapar.

## Veri Release Sürümü

Yeni kuruluş kaydı veya yeni çıktı formatı MINOR; yalnız metadata düzeltmesi
PATCH; kırıcı şema veya anlam değişikliği MAJOR sürüm gerektirir. Ayrıntılı
politika `RELEASE.md` içindedir.

## Gizlilik

Kaynak doğrulamak için gerçek IBAN, müşteri adı, hesap sahibi, bordro, telefon,
dekont veya üretim logu kullanılmaz. Yalnız `TEST_DATA.md` içinde açıklanan
sentetik fixture'lar kabul edilir.
