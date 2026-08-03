# Güvenlik Politikası

## Desteklenen sürümler

Yalnızca en güncel `tr-iban` sürümü güvenlik güncellemesi alır. Kullandığınız
sürümü `npm view tr-iban version` komutuyla veya
[son GitHub sürümünden](https://github.com/trugurpala/turkiye-iban/releases/latest)
kontrol edin. Eski sürümlere düzeltme geri taşınması garanti edilmez.

## Güvenlik açığını özel olarak bildirin

Güvenlik açığı veya gerçek finansal veri sızıntısı için public issue,
Discussion ya da pull request açmayın.
[Özel GitHub Security Advisory](https://github.com/trugurpala/turkiye-iban/security/advisories/new)
oluşturun.

Raporda yalnız sentetik örneklerle şunları belirtin:

- Etkilenen sürüm veya commit.
- Beklenen ve gerçekleşen davranış.
- Tekrarlama adımları.
- IBAN doğrulaması, kuruluş eşlemesi veya veri ifşası üzerindeki olası etki.

Proje yöneticisi ilk alındı bildirimini makul olarak 72 saat içinde vermeyi,
durum güncellemelerini özel kanalda paylaşmayı ve düzeltme yayımlanana kadar
ayrıntıları gizli tutmayı hedefler. Bu süre bir hizmet seviyesi taahhüdü
değildir.

## Gizlilik

Issue, PR, commit, fixture, ekran görüntüsü veya release içinde gerçek IBAN,
hesap sahibi, telefon, bordro ya da başka kişisel finansal veri paylaşmayın.
Bir gizlilik olayı fark ederseniz veriyi yeniden paylaşmadan özel advisory
üzerinden konumunu bildirin.

CI, metin dosyalarındaki Türkiye IBAN adaylarını tarar; bu kontrol görselleri
ve dış platformlardaki içeriği incelemez. Test ve örneklerde yalnızca
`TEST_DATA.md` içinde tanımlanan sentetik değerleri kullanın.

## Güvenlik sınırı

Kütüphane IBAN biçimini ve kontrol rakamlarını doğrular. Bir hesabın gerçekten
var olduğunu, sahibini, bakiyesini veya transfer yapılabilirliğini doğrulamaz.
Uygulamanızda istek boyutu, hız sınırı ve log maskeleme önlemlerini ayrıca
uygulamalısınız.
