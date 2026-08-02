# Riskler ve Sınırlar

Bu belge, `turkiye-iban` projesinin bilinçli olarak taşıdığı kalan riskleri ve
bu risklerin nasıl yönetileceğini kaydeder. Amaç daha büyük iddia kurmak değil;
projenin sınırlarını açık tutmak, kullanıcıların doğru beklentiyle entegre
olmasını sağlamak ve gelecekteki PR'larda yanlış kamu iddialarını erken
yakalamaktır.

> [!IMPORTANT]
> Proje TCMB tarafından onaylanmış veya desteklenmiş resmî bir servis değildir.
> Hesap varlığını, hesap sahibini, bakiye bilgisini veya transfer
> yapılabilirliğini doğrulamaz.

## Onaylı Konumlandırma

Kullanılacak kısa ifade:

> `turkiye-iban`, Türkiye IBAN formatını ve kontrol basamaklarını doğrulayan;
> IBAN içindeki beş haneli kuruluş kodunu TCMB kaynaklı veriyle eşleştiren açık
> kaynak veri ve TypeScript/NPM paketidir. Hesap varlığını, hesap sahibi veya
> transfer yapılabilirliğini doğrulamaz.

Kamuya açık metinlerde şu ifadeleri kullanmayın:

- "TCMB onaylı"
- "hesabı doğrular"
- "transfer garantisi verir"
- "her dilde paket hazır"

## Risk Kaydı

| Risk | Seviye | Mevcut onlem | Kalan risk | Bakim aksiyonu | Tekrar gozden gecirme |
| --- | --- | --- | --- | --- | --- |
| Veri güncelliği ve kaynak değişimi | Yüksek | Zamanlanmış kaynak kontrolü, SHA-256 manifesti, insan incelemesi zorunluluğu | TCMB PDF veya HTML yapısı değişirse parser raporu bakım isteyebilir | `npm run data:check-remote` sonucunu incele, gerekirse canonical kaynağı PR ile güncelle | Her kaynak kontrolü başarısızlığında ve her veri release'i öncesinde |
| Resmî onay algısı | Yüksek | README, lansman rehberi ve bu belge resmî onay olmadığını söyler | Tanıtım metinleri dış kanallarda fazla iddialı yazılabilir | Paylaşımdan önce bu belgedeki onaylı konumlandırmayı kullan | Her public duyuru ve release notunda |
| Hesap doğrulama beklentisi | Yüksek | README ve API dokümanı hesap varlığını doğrulamadığını vurgular | Kullanıcı `isValid: true` sonucunu hesap varlığı sanabilir | Örneklerde `maskIban`, `providerStatus` ve sınır uyarısını birlikte göster | API, README veya örnek değiştiğinde |
| Node 22 sınırı | Orta | NPM paketi Node `>=22` ve Node 22/24 CI ile doğrulanır | Node 18/20 kullanan ekipler runtime paketi doğrudan kullanamayabilir | Eski Node desteği ancak test matrisiyle açılır; bugün JSON/CSV/SQL/SQLite alternatifi önerilir | Node sürüm desteği talebi geldiğinde |
| Packagist indeksinin henüz doğrulanmamış olması | Orta | PHP `v0.1.5` ve Python `v0.1.5` GitHub release'leri; Python PyPI OIDC yayını, istemci CI sonuçları ve yayınlama adımları belgelenir | Packagist kaydı olmadan Composer kurulumu garanti edilemez; GitHub release'i tek başına indeks yayını kanıtı değildir | Packagist kaydını maintainer hesabıyla tamamla, temiz Composer kurulumunu doğrula ve public belgeleri ancak bundan sonra güncelle | Her istemci release'inde ve indeks yayını sonrasında |
| Topluluk benimsenmesi | Orta | GitHub Discussions, issue formları, lansman metinleri ve görseller hazır | Yeni repo olduğu için star, fork, download ve dış katkı zamanla oluşur | Gerçek kullanım örnekleri ve framework dokümanları ekle; toplu spam yapma | Aylık lansman metrikleri incelemesinde |
| `providerStatus` ve `status` karışıklığı | Orta | README ve API dokümanı kod eşleşmesi ile faaliyet statüsünü ayırır | Hızlı okuyan kullanıcı `known` sonucunu lisans/faaliyet kanıtı sanabilir | Public metinlerde `providerStatus: "known"` yalnız kod eşleşmesidir ifadesini koru | API, veri şeması veya provider modeli değiştiğinde |
| Büyük veya kötü niyetli girdi | Orta | Runtime 1.024 karakterden uzun girdiyi `INVALID_LENGTH` ile erken reddeder | Bir HTTP uygulaması request-body veya rate-limit koymazsa daha erken katmanda kaynak tüketimi olabilir | Sunucu entegrasyonlarında request boyutu, rate-limit ve maskeli log politikasını zorunlu tut | Yeni framework örneği veya API giriş noktası eklendiğinde |
| Gizlilik taramasının kapsamı | Orta | CI bitişik, boşluklu, tireli ve satıra bölünmüş metin IBAN adaylarını tarar | Görseller, binary ekler ve dış platform mesajları otomatik taranmaz | PR/issue eklerini insan incelemesiyle kontrol et; gerçek veri görülürse `SECURITY.md` akışını uygula | Gizlilik olayı, yeni dosya türü veya katkı akışı değişikliğinde |

## PR Kontrol Kuralı

Public iddiaları, veri kaynağını, release notlarını, örnekleri veya onboarding
dokümanlarını etkileyen her PR bu belgeyi kontrol etmelidir. Belgeyi
değiştirmek gerekmiyorsa PR açıklamasında "no change required" olarak yazmak
yeterlidir.

## Release Etkisi

Bu belge tek başına release asset veya NPM publish gerektirmez. Ancak yeni veri
release'i, yeni runtime paketi veya kamuya açık konumlandırma değişikliği
yapıldığında release notlarıyla birlikte tekrar kontrol edilmelidir.
