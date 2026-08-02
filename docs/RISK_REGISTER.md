# Riskler ve Sinirlar

Bu belge, `turkiye-iban` projesinin bilincli olarak tasidigi kalan riskleri ve
bu risklerin nasil yonetilecegini kaydeder. Amac daha buyuk iddia kurmak degil;
projenin sinirlarini acik tutmak, kullanicilarin dogru beklentiyle entegre
olmasini saglamak ve gelecekteki PR'larda yanlis kamu iddialarini erken
yakalamaktir.

> [!IMPORTANT]
> Proje TCMB tarafindan onaylanmis veya desteklenmis resmi bir servis degildir.
> Hesap varligini, hesap sahibini, bakiye bilgisini veya transfer
> yapilabilirligini dogrulamaz.

## Onayli Konumlandirma

Kullanilacak kisa ifade:

> `turkiye-iban`, Turkiye IBAN formatini ve kontrol basamaklarini dogrulayan;
> IBAN icindeki bes haneli kurulus kodunu TCMB kaynakli veriyle eslestiren acik
> kaynak veri ve TypeScript/NPM paketidir. Hesap varligi, hesap sahibi veya
> transfer yapilabilirligi dogrulamaz.

Kamuya acik metinlerde su ifadeleri kullanmayin:

- "TCMB onayli"
- "hesabi dogrular"
- "transfer garantisi verir"
- "her dilde paket hazir"

## Risk Kaydi

| Risk | Seviye | Mevcut onlem | Kalan risk | Bakim aksiyonu | Tekrar gozden gecirme |
| --- | --- | --- | --- | --- | --- |
| Veri guncelligi ve kaynak degisimi | Yuksek | Zamanlanmis kaynak kontrolu, SHA-256 manifesti, insan incelemesi zorunlulugu | TCMB PDF veya HTML yapisi degisirse parser raporu bakim isteyebilir | `npm run data:check-remote` sonucunu incele, gerekirse canonical kaynagi PR ile guncelle | Her kaynak kontrolu basarisizliginda ve her veri release'i oncesinde |
| Resmi onay algisi | Yuksek | README, lansman rehberi ve bu belge resmi onay olmadigini soyler | Tanitim metinleri dis kanallarda fazla iddiali yazilabilir | Paylasimdan once bu belgedeki onayli konumlandirmayi kullan | Her public duyuru ve release notunda |
| Hesap dogrulama beklentisi | Yuksek | README ve API dokumani hesap varligini dogrulamadigini vurgular | Kullanici `isValid: true` sonucunu hesap varligi sanabilir | Orneklerde `maskIban`, `providerStatus` ve sinir uyarisini birlikte goster | API, README veya ornek degistiginde |
| Node 22 siniri | Orta | NPM paketi Node `>=22` ve Node 22/24 CI ile dogrulanir | Node 18/20 kullanan ekipler runtime paketi dogrudan kullanamayabilir | Eski Node destegi ancak test matrisiyle acilir; bugun JSON/CSV/SQL/SQLite alternatifi onerilir | Node surum destegi talebi geldiginde |
| Packagist indeksinin henuz dogrulanmamis olmasi | Orta | PHP `v0.1.5` ve Python `v0.1.5` GitHub release'leri; Python PyPI OIDC yayini, istemci CI sonuclari ve yayinlama adimlari belgelenir | Packagist kaydi olmadan Composer kurulumu garanti edilemez; GitHub release'i tek basina indeks yayini kaniti degildir | Packagist kaydini maintainer hesabiyla tamamla, temiz Composer kurulumunu dogrula ve public belgeleri ancak bundan sonra guncelle | Her istemci release'inde ve indeks yayini sonrasinda |
| Topluluk benimsenmesi | Orta | GitHub Discussions, issue formlari, lansman metinleri ve gorseller hazir | Yeni repo oldugu icin star, fork, download ve dis katki zamanla olusur | Gercek kullanim ornekleri ve framework dokumanlari ekle; toplu spam yapma | Aylik lansman metrikleri incelemesinde |
| `providerStatus` ve `status` karisikligi | Orta | README ve API dokumani kod eslesmesi ile faaliyet statusunu ayirir | Hizli okuyan kullanici `known` sonucunu lisans/faaliyet kaniti sanabilir | Public metinlerde `providerStatus: "known"` yalniz kod eslesmesidir ifadesini koru | API, veri semasi veya provider modeli degistiginde |

## PR Kontrol Kurali

Public iddialari, veri kaynagini, release notlarini, ornekleri veya onboarding
dokumanlarini etkileyen her PR bu belgeyi kontrol etmelidir. Belgeyi
degistirmek gerekmiyorsa PR aciklamasinda "no change required" olarak yazmak
yeterlidir.

## Release Etkisi

Bu belge tek basina release asset veya NPM publish gerektirmez. Ancak yeni veri
release'i, yeni runtime paketi veya kamuya acik konumlandirma degisikligi
yapildiginda release notlariyla birlikte tekrar kontrol edilmelidir.
