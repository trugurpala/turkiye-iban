# Proje Hedefi

`turkiye-iban`, Türkiye IBAN'ını doğrulama ve içindeki kuruluş kodunu resmî kanıta dayalı açık veriyle eşleştirme işini her geliştiricinin yeniden çözmek zorunda kalmamasını amaçlar.

Proje tek bir doğrulanabilir kaynaktan dört kullanım biçimi üretir:

- Next.js, NestJS, Node.js ve TypeScript için `tr-iban` NPM paketi
- PHP, Python ve diğer diller için sürümlenmiş JSON verisi
- Elektronik tablo ve veri aktarımı için CSV çıktısı
- Doğrudan veritabanı kullanan uygulamalar için taşınabilir SQL çıktısı

## Ürün sözleşmesi

Paket ülke kodu, uzunluk, izin verilen karakterler, rezerv alanı ve kontrol rakamlarını doğrular. Kuruluş kodu veri kümesinde bulunamazsa IBAN'ı yalnız bu nedenle geçersiz ilan etmez; `providerStatus: "unknown"` döndürür.

Kuruluş eşleştirmesi hesabın gerçekten var olduğunu, kime ait olduğunu, isim eşleşmesini veya para transferine açık olduğunu kanıtlamaz. Proje gerçek IBAN ya da kişisel finansal veri toplamaz; testlerde yalnız sentetik fixture kullanır.

## Tamamlanan temel

- TCMB katılımcı kanıtlı 70 kuruluş kaydının JSON, CSV, SQL ve TypeScript çıktıları
- Kaynak adresi, erişim tarihi, kod kanıtı ve SHA-256 manifesti
- ESM ve CommonJS destekli, sıfır runtime bağımlılıklı `tr-iban` paketi
- Sentetik fixture, privacy scan, veri kalite kontrolleri ve Node 22/24 CI
- Korumalı `main`, GitHub Release artifact'ları, SBOM ve NPM trusted publishing
- Topluluk, güvenlik, yönetişim, katkı ve veri güncelleme politikaları

## v0.1.1 hedefi

`v0.1.1`, algoritmayı değiştirmeden projenin anlaşılabilirliğini ve katkıya açıklığını tamamlar. GitHub ile NPM anlatımı eşitlenir; Figma kaynaklı lansman varlıkları, sosyal önizleme, Discussions, başlangıç issue'ları, tanıtım metinleri ve telemetrisiz ölçüm planı yayımlanır.

## Yonetim-Paneli entegrasyonu

Personel ekranında IBAN girildiğinde paket biçim ve kontrol rakamlarını doğrular, ardından kuruluş kodunu eşleştirir. Sonuç `known` ise banka veya kuruluş otomatik seçilir. Sonuç `unknown` ise panel kuruluş seçmez ve kendi iş kuralı olarak kaydın tamamlanmasını engeller. Backend aynı kontrolleri tekrarlar; loglarda yalnız maskelenmiş IBAN kullanılır.

## Divan

Bu proje Divan ile tasarlandı ve üretildi. Divan araştırma, tasarım, planlama ve geliştirme sürecinde kullanılmıştır; paketin runtime bağımlılığı değildir.
