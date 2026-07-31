# Data Update Policy

## Sıklık

Resmî kaynak hash'leri GitHub Actions ile ayda bir ve her release öncesinde
kontrol edilir. Değişiklik bulunduğunda otomatik olarak güvenilir kabul edilmez;
üretim diff'i maintainer tarafından incelenir.

## Güncelleme Akışı

```bash
npm run data:check-remote
npm run data:update
npm test
```

1. `data/source-manifest.json` ile canlı resmî kaynakların SHA-256 değerlerini
   karşılaştırın.
2. Üreticiyi çalıştırarak JSON, CSV, SQL, TypeScript verisi ve sentetik
   fixture'ları birlikte yenileyin.
3. Eklenen, silinen, yeniden adlandırılan ve türü değişen kayıtları inceleyin.
4. Lisans listesine yeni eklenen fakat katılımcı listesinde bulunmayan kodların
   lookup kümesine girmediğini doğrulayın.
5. `npm test` ve privacy taramasını çalıştırın.
6. PR açıklamasına resmî URL, kontrol tarihi ve değişiklik gerekçesini yazın.

## Kod Normalizasyonu

Katılımcı kaynağındaki `rawCode` olduğu gibi saklanır. IBAN alanında kullanılan
`code`, yalnız rakamlardan oluşan değerin beş haneye soldan sıfırla
tamamlanmasıdır. Lisans sicilindeki kuruluş kodları bu dönüşümle otomatik olarak
IBAN koduna çevrilmez.

## Silme ve Uyuşmazlık

Bir kayıt resmî katılımcı listesinden kaybolursa sessizce silinmez. İlgili
release/PR içinde kaynak değişikliği belirtilir ve önceki sürümle farkı
incelenir. Kaynaklar çatışırsa daha özel ve güncel TCMB kaynağı tercih edilir;
karar CHANGELOG ve PR'da belgelenir.

## Gizlilik

Gerçek IBAN veya kişisel finansal veri veri doğrulamak için kullanılamaz. Tüm
fixture'lar üretici tarafından sentetik olarak oluşturulur.
