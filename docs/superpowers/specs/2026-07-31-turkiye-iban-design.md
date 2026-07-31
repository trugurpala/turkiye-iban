# turkiye-iban Tasarım Belgesi

## Amaç ve Kapsam

`turkiye-iban`, Yonetim-Paneli'nden bağımsız yayımlanan açık kaynak bir veri ve
paket deposudur. Türkiye IBAN'ını ayrıştırır, biçim ve MOD 97-10 kontrolünü
yapar, beş haneli sağlayıcı kodunu çıkarır ve bu kodu TCMB kaynaklı kuruluş
verisiyle eşleştirir.

İlk sürüm dil bağımsız JSON/CSV/SQL, JSON Schema, sentetik fixture'lar ve
TypeScript/NPM paketi içerir. Composer ikinci, Python paketi sonraki fazdır.

## Kapsam Dışı

Hesabın gerçekten var olması, hesap sahibi, isim eşleşmesi, KYC, dolandırıcılık
riski, bakiye ve transfer yapılabilirliği doğrulanmaz. Runtime ağ çağrısı,
Yonetim-Paneli kod değişikliği ve gerçek müşteri verisi kapsam dışıdır.

## Mimari

Veri öncelikli küçük monorepo kullanılacaktır:

- `data/`: JSON, CSV, SQL, schema ve kaynak manifesti.
- `fixtures/`: yalnız sentetik geçerli/geçersiz örnekler.
- `packages/typescript/`: sıfır runtime bağımlılıklı ESM/CommonJS NPM paketi.
- `scripts/` ve `tools/`: veri güncelleme, doğrulama, gizlilik ve release araçları.
- `.github/`: CI, release, issue/PR şablonları ve güvenlik otomasyonu.

Canlı kaynak indiren `data:update` normal testlerden ayrıdır. CI commit edilmiş
veriyi ağsız doğrular. Aylık/manual kaynak kontrolü fark üretir fakat otomatik
veri commit'i yapmaz.

## Veri ve Kanıt Modeli

Her sağlayıcı kaydı şu alanları taşır: `code`, `rawCode`, `nameOfficial`,
`nameShort`, `type`, `status`, `systems`, `codeEvidence`, `aliases`, `sources`
ve `lastVerifiedAt`.

`codeEvidence`, kodun hangi resmî bağlamda yayımlandığını açıklar:

- `payment_system_participant`: TCMB ödeme sistemleri katılımcı kodu.
- `licensed_payment_institution`: TCMB aktif ödeme kuruluşu kodu.
- `licensed_electronic_money_institution`: TCMB aktif elektronik para kuruluşu
  kodu.

Aktif kuruluş statüsü veya kuruluş kodu, tek başına IBAN düzenleme yetkisi diye
sunulmaz. Eski `ibanEligible` alanı kaldırılır. Üç ve dört haneli kaynak kodlar
beş haneli IBAN sağlayıcı alanıyla karşılaştırılabilmesi için sola sıfırla
tamamlanır; hem ham hem normalize değer korunur.

## IBAN Sözleşmesi

Türkiye IBAN'ı `TR + 2 kontrol basamağı + 5 sağlayıcı kodu + 1 rezerv alanı +
16 alfasayısal hesap alanı` biçimindedir. Rezerv alanı sıfırdır. Elektronik
gösterimde ayraç yoktur; kullanıcı girdisinde boşluklar normalize edilir, tire
ve diğer ayraçlar reddedilir.

`validateTurkishIban` yalnız IBAN biçimi ve checksum geçerliliğini ölçer.
Sağlayıcı veri setinde yoksa geçerli checksum sonucu değiştirilmez.
`identifyBankFromIban` ayrıca `providerStatus: known | unknown` döndürür.

## Genel API

- `parseIban(input: string): ParsedTurkishIban`
- `validateTurkishIban(input: string): boolean`
- `getBankCodeFromIban(input: string): string | null`
- `findBankByCode(code: string): TurkishIbanProvider | null`
- `identifyBankFromIban(input: string): IdentifiedTurkishIban`
- `formatIban(input: string): string`
- `maskIban(input: string): string`

`IdentifiedTurkishIban`, `parsed`, `providerCode`, `provider`,
`providerStatus` ve `dataVersion` alanlarını taşır. Geriye dönük okunabilirlik
için v0.1.0'da `bankCode` ve `bank` alias'ları korunur.

## Güvenlik ve Gizlilik

Issue, PR, fixture, test, örnek ve belgelerde gerçek IBAN, müşteri adı, telefon,
hesap sahibi, bordro veya dekont kabul edilmez. Gizlilik taraması fixture
allowlist'i dışındaki IBAN benzeri değerlerde CI'ı durdurur. Güvenlik açıkları
GitHub Private Vulnerability Reporting üzerinden bildirilir.

## Yayın ve Entegrasyon

Her release JSON, CSV, SQL, schema, fixture, SHA-256 listesi, SBOM ve NPM
tarball yayımlar. NPM paketi GitHub Actions provenance ile oluşturulur.

Yonetim-Paneli `providerStatus: known` sonucunda kuruluşu otomatik seçer.
`unknown` sonucunda banka seçmez ve kendi iş kuralıyla kaydı engeller. Paket bu
panel politikasını genel IBAN geçerliliğinin içine gömmez.

## Test Stratejisi

Testler biçim, checksum, 16 karakterlik alfasayısal hesap alanı, rezerv alanı,
bilinen/bilinmeyen sağlayıcı, formatlama, maskeleme, ESM/CommonJS tüketimi,
JSON/CSV/SQL eşliği, schema, SQLite uygulanabilirliği, fixture sentetikliği,
gizlilik taraması ve NPM tarball içeriğini kapsar.

## Divan

Bu proje Divan ile tasarlandı ve üretildi. Divan runtime bağımlılığı değildir.
