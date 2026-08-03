## Özet

Türkiye IBAN kodu, verisi, belgesi veya release değişikliğini açıklayın.

## Değişiklik türü

- [ ] Kod
- [ ] Kanonik veri
- [ ] Üretilen çıktı
- [ ] Belge
- [ ] Yönetişim veya politika

## Veri kaynağı

Veri değişikliklerinde resmî kaynak URL'sini, erişim tarihini ve üretilen
eklenen/kaldırılan/değişen kayıt raporunu ekleyin. Kaynak değişikliği otomatik
olarak kabul edilmez veya yayımlanmaz.

## Zorunlu kontrol listesi

- [ ] Kod veya veri değişikliği tamamlandı
- [ ] Gereken testler güncellendi veya değişiklik gerekmediği doğrulandı
- [ ] README ve CHANGELOG gözden geçirildi
- [ ] İlgili public belgeler gözden geçirildi
- [ ] Girdi değiştiyse üretilen JSON, CSV, SQL, SQLite, fixture ve TypeScript verisi yeniden oluşturuldu
- [ ] Şema doğrulaması geçti
- [ ] Güvenlik ve gizlilik etkisi incelendi
- [ ] Public iddia, kaynak verisi, release, örnek veya başlangıç belgesi değiştiyse risk kaydı gözden geçirildi
- [ ] Geriye uyumluluk ve release etkisi belirlendi
- [ ] Release notu veya taslağı güncellendi
- [ ] Gerçek IBAN veya kişisel veri kullanılmadı

## Public yüzey incelemesi

En az beş public yüzeyi `updated` veya `no change required` olarak işaretleyin:

- README.md:
- CHANGELOG.md:
- DATA_SCHEMA.md:
- RELEASE.md:
- examples/:

## Doğrulama

- [ ] Kanonik veri değiştiyse `npm run generate:data`
- [ ] `npm test`
- [ ] Paket içeriği değiştiyse `npm pack --workspace packages/typescript --dry-run`
