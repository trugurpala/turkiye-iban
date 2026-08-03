# Katkı Rehberi

`turkiye-iban`; Türkiye IBAN doğrulaması, kuruluş kodu eşlemesi ve bunları
destekleyen dil bağımsız referans verisine odaklanır. Küçük, kaynaklı ve test
edilmiş katkılar memnuniyetle karşılanır. Adres, vergi, telefon, plaka veya
posta kodu gibi ilgisiz veri kümelerini bu depoya eklemeyin.

## Katkı yolları

- Tekrarlanabilir hata için [bug formunu](https://github.com/trugurpala/turkiye-iban/issues/new/choose)
  kullanın.
- Yeni davranış veya belge önerisini önce feature formunda açıklayın.
- Resmî kaynak değişikliği için `Data correction` formunu, kaynak URL'sini ve
  erişim tarihini ekleyerek kullanın.
- Kullanım sorularını [GitHub Discussions](https://github.com/trugurpala/turkiye-iban/discussions)
  bölümünde sorun.

Güvenlik açığı için issue açmayın; [SECURITY.md](SECURITY.md) içindeki özel
bildirim yolunu kullanın.

## Gizlilik

Issue, pull request, commit, fixture, örnek veya ekran görüntüsünde gerçek
IBAN, hesap sahibi, müşteri adı, telefon, bordro, dekont veya üretim finansal
verisi kullanmayın. Yalnızca `TEST_DATA.md` içinde belirtilen sentetik değerleri
kullanın.

## Geliştirme ortamı

Node.js 22+, npm ve Python 3 gereklidir:

```bash
python -m pip install -r tools/requirements.txt
npm ci
npm test
```

Normal üretim, test ve build adımları çevrimdışı ve deterministiktir. Odaklı
bir dal açın, her committe tek bir konuyu ele alın ve pull request'i `main`
dalına yöneltin.

## Kod değişiklikleri

- Public API'yi, paket exportlarını ve geriye uyumluluk aliaslarını koruyun.
- Davranış değişikliğini önce başarısız bir testle gösterin.
- Runtime kodunu deterministik, bağımlılıksız ve ağsız tutun.
- ESM ve CommonJS paket tüketicilerini birlikte kontrol edin.
- Ham IBAN'ı loglamayın; teşhislerde `maskIban` kullanın.
- Breaking change için major sürüm ve migration rehberi hazırlayın.

## Veri değişiklikleri

Önce uzak kaynak incelemesini çalıştırın:

```bash
npm run data:check-remote
```

Bu komut release verisini değiştirmez. Resmî kaynağı ve üretilen fark raporunu
insan gözüyle inceleyin. Kabul edilen değişikliği yalnızca
`data/source/institutions.json` dosyasına uygulayın:

```bash
npm run generate:data
npm test
```

Üretilen JSON, CSV, SQL, SQLite, TypeScript veri veya fixture dosyalarını elle
düzenlemeyin.

## Pull request kontrolü

```bash
npm test
npm pack --workspace packages/typescript --dry-run
```

PR açıklamasında yapılan değişikliği, çalıştırılan komutları ve güvenlik,
geriye uyumluluk ve release etkisini yazın. `AGENTS.md` uyarınca README,
CHANGELOG, ilgili teknik belgeler, testler, üretilen veriler ve release
notlarını gözden geçirip en az beş public yüzeyi `updated` veya
`no change required` olarak listeleyin.
