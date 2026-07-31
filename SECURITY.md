# Security Policy

## Desteklenen Sürümler

Yalnız en güncel minor sürüm güvenlik güncellemesi alır. Eski sürümde bulunan
bir açık mümkünse en güncel sürümde yeniden doğrulanmalıdır.

Desteklenen sürümü `npm view tr-iban dist-tags.latest` komutuyla veya GitHub'daki
son release sayfasından doğrulayın. Eski sürümler için güvenlik düzeltmesi
geriye taşınmaz; düzeltme yeni bir sürüm olarak yayımlanır.

## Özel Bildirim

Güvenlik açığı veya gerçek finansal veri sızıntısı için public issue açmayın.
[GitHub Private Vulnerability Reporting](https://github.com/trugurpala/turkiye-iban/security/advisories/new)
kanalını kullanın.

Raporda yalnız sentetik örneklerle şu bilgileri verin:

- Etkilenen sürüm veya commit.
- Kısa etki açıklaması.
- Tekrarlama adımları.
- IBAN doğrulaması, sağlayıcı eşlemesi veya veri ifşası üzerindeki etkisi.

Maintainer ilk alındı bildirimini makul olarak 72 saat içinde vermeyi, durum
güncellemelerini koordine etmeyi ve düzeltme yayımlanana kadar ayrıntıları özel
tutmayı hedefler. Bu süre garanti veya hizmet seviyesi sözleşmesi değildir.

## Gizlilik Olayları

Issue, PR, commit, fixture veya release içinde gerçek IBAN, hesap sahibi,
telefon, bordro ya da başka kişisel finansal veri görülürse içerik public
görünümden kaldırılır; gerekirse Git geçmişi ve release artifact'ları yeniden
oluşturulur. Böyle bir veriyi örnek olarak tekrar paylaşmayın.

CI, kompakt veya boşluklu Türkiye IBAN adaylarını tarar ve yalnız açıkça
`synthetic: true` olarak işaretlenmiş fixture değerlerine izin verir. Hata
çıktısı bilinmeyen adayları maskeler. Tarama bir veri kaynağı veya hukuki
uyumluluk garantisi değildir; katkı yapan kişi gerçek veri kullanmamakla
sorumludur.
