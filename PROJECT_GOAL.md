# Proje Hedefi

`turkiye-iban`, Türkiye IBAN biçimini ve MOD 97-10 kontrol basamaklarını
doğrulayan; IBAN içindeki beş haneli ödeme hizmeti sağlayıcısı kodunu TCMB
ödeme sistemleri katılımcı kanıtıyla eşleştiren, dil bağımsız bir açık kaynak veri ve
paket projesidir.

Proje üç kullanım biçimini aynı kaynak üzerinden destekler:

- Next.js, NestJS ve Node.js uygulamaları için `tr-iban` NPM paketi.
- PHP, Python ve diğer diller için sürümlenmiş JSON ve CSV verisi.
- Doğrudan veritabanı kullanan uygulamalar için taşınabilir SQL çıktısı.

Paket IBAN'ın biçimini ve checksum değerini doğrular. Kuruluş kodu veri setinde
bulunamazsa IBAN'ı tek başına geçersiz ilan etmez; sağlayıcı sonucunu `unknown`
olarak döndürür. Kuruluş eşleştirmesi hesabın varlığını, hesap sahibini, isim
eşleşmesini veya transfer yapılabilirliğini kanıtlamaz.

## İlk Sürümün Başarı Ölçütleri

- JSON, CSV ve SQL aynı TCMB katılımcı kanıtlı kuruluş kayıtlarını içerir.
- Her veri kaydı kaynağını, erişim tarihini ve kanıt türünü taşır.
- TypeScript paketi ESM ve CommonJS tüketicilerinde çalışır.
- Yalnız sentetik IBAN fixture'ları kullanılır; gerçek kişisel finansal veri
  issue, PR, örnek veya testlere kabul edilmez.
- GitHub topluluk, güvenlik, yönetişim ve release yüzeyleri kullanıma hazırdır.
- `v0.1.0` GitHub Release ve `tr-iban@0.1.0` aynı kaynak commit'inden üretilir.

## Yonetim-Paneli Entegrasyonu

Personel ekranında IBAN girildiğinde paket biçim/checksum kontrolü yapar ve
sağlayıcı kodunu eşleştirir. Eşleşme `known` ise banka/kuruluş otomatik seçilir.
Eşleşme `unknown` ise otomatik veya manuel banka seçimi yapılmaz ve panel kendi
iş kuralı olarak kaydı engeller. Backend aynı kontrolleri tekrarlar; loglarda
yalnız maskelenmiş IBAN kullanılır.

## Divan

Bu proje Divan ile tasarlandı ve üretildi. Divan, paketin runtime bağımlılığı
değildir; araştırma, tasarım, planlama ve geliştirme sürecinde kullanılmıştır.
