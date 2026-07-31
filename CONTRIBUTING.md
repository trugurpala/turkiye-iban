# Contributing

`turkiye-iban` katkılarına teşekkürler. Küçük, kaynaklandırılmış ve test edilmiş
değişiklikler incelemeyi kolaylaştırır.

## Değişmez Gizlilik Kuralı

Gerçek IBAN, hesap sahibi/müşteri adı, telefon, bordro, dekont, banka ekranı veya
kişisel finansal veri issue, PR, commit, fixture ve testlerde kullanılamaz.
Yalnız sentetik örnek kullanın. Güvenlik açıklarını [SECURITY.md](SECURITY.md)
üzerinden özel bildirin.

## Kurulum

```bash
python -m pip install -r tools/requirements.txt
npm ci
npm test
```

Normal testler çevrimdışıdır. Resmî kaynakları yalnız veri değişikliğinde çekin:

```bash
npm run data:check-remote
npm run data:update
npm test
```

## Veri Katkıları

Veri PR'ı şunları içermelidir:

- Resmî TCMB kaynak URL'si ve kontrol tarihi.
- Değişikliğin kısa gerekçesi.
- Birincil katılımcı kodu kanıtı ile lisans/statü bilgisinin açık ayrımı.
- Birlikte üretilmiş JSON, CSV, SQL, TypeScript verisi ve fixture diff'i.

Üretilen dosyaları elle düzenlemeyin. Üreticinin ifade edemediği bir düzeltme
varsa önce üreticiyi değiştirin. Schwifty karşılaştırma için kullanılabilir ama
birincil kaynak değildir.

## Kod Katkıları

- API deterministik kalmalı ve runtime ağ çağrısı yapmamalıdır.
- Yeni runtime bağımlılığı maintainer kararı gerektirir.
- Davranış değişikliğini önce başarısız bir testle belgeleyin.
- ESM ve CommonJS tüketici testlerini koruyun.
- Ham IBAN loglamayın.

## Pull Request Kontrolü

```bash
npm test
npm pack --workspace packages/typescript --dry-run
```

PR şablonundaki gizlilik onayı zorunludur. Maintainerlar kaynak veya güvenlik
kanıtı yetersiz değişiklikleri reddedebilir.
