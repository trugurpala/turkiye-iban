# Changelog

Tüm önemli değişiklikler bu dosyada belgelenir. Biçim Keep a Changelog ve sürüm
numaraları Semantic Versioning yaklaşımını izler.

## [Unreleased]

## [0.2.0] - 2026-07-31

### Added

- Tek elle düzenlenen doğruluk kaynağı olarak şema doğrulamalı
  `data/source/institutions.json`.
- Canonical veriden deterministik üretilen `data/tr-banks.sqlite` release
  çıktısı ve tam JSON/CSV/SQL/SQLite kayıt eşliği kontrolleri.
- SQLite çıktısının sabit sürümlü `sql.js` WebAssembly aracıyla üretilmesi ve
  üretici sürümü header alanının platformlar arası aynı checksum için normalize
  edilmesi.
- Ağsız generated-file drift kontrolü, kaynak bazında eklenen/silinen/değişen
  kayıt raporu ve insan inceleme issue'su açan zamanlanmış workflow.
- `ARCHITECTURE.md`, `DATA_SCHEMA.md`, `RELEASE.md`, `ROADMAP.md`,
  `TEST_DATA.md` ve kalıcı görev standardı `AGENTS.md`.
- Format, lint, typecheck, unit, integration, örnek kullanım ve release asset
  kalite kapıları ile çalıştırılabilir JavaScript/veri dosyası örnekleri.

### Changed

- Normal veri üretimi canlı TCMB kaynaklarından ayrıldı; otomasyon artık
  canonical veriyi veya release dosyalarını doğrudan değiştiremiyor.
- Kaynaklar `official`, `secondary` veya `manually_verified`; kullanım amaçları
  ise `primary_code_evidence`, `enrichment` veya `monitor_only` olarak açıkça
  sınıflandırılıyor.
- Yanlış yıl içeren katılımcı kaynak kimliği `2025` yayınıyla eşleştirildi;
  aktif ödeme/elektronik para sicilleri mevcut snapshot için dürüstçe
  `monitor_only` olarak kaydedildi.
- Issue formları, PR kontrol listesi, katkı rehberi, README, API güvenlik notu,
  release politikası ve roadmap tek repository kapsamına göre güncellendi.

### Security

- Bütün fixture kayıtlarında `synthetic: true` zorunlu oldu; privacy scan
  boşluklu/küçük harfli adayları normalize ediyor ve bilinmeyen değeri loglarda
  maskeliyor.
- Mevcut yedi public API fonksiyonu, import yolları ve geriye uyumluluk alias'ları
  değiştirilmedi.

## [0.1.2] - 2026-07-31

### Changed

- GitHub ve NPM README yüzeylerine bağlantılı "Divan ile üretildi" atfı eklendi.
- NOTICE ve proje hedefi Divan'ın araştırma, şartname, planlama, uygulama, doğrulama ve yayın katkısını açıkça kaydedecek biçimde güncellendi.
- Runtime API ve kuruluş veri kümesi değişmedi.

## [0.1.1] - 2026-07-31

### Added

- Figma kaynaklı GitHub sosyal önizleme, yatay lansman ve kare topluluk görselleri.
- X, LinkedIn, TurkDev/Reddit ve topluluk e-postası için lansman metinleri.
- Telemetri eklemeden GitHub ve NPM benimsenmesini izleyen ölçüm planı.
- GitHub Discussions ve başlangıç katkı issue'ları için topluluk girişleri.

### Changed

- GitHub ve NPM README anlatımı kullanıcı dostu doğrulama, veri kaynağı ve `unknown` kuruluş açıklamalarında eşitlendi.
- Proje hedefi ve yol haritası lansman ile topluluk fazını gösterecek biçimde güncellendi.
- Runtime API, doğrulama davranışı ve 70 kayıtlı kuruluş veri kümesi değişmedi.

## [0.1.0] - 2026-07-31

### Added

- TCMB Ödeme Sistemleri Katılımcıları kanıtlı 70 sağlayıcı kaydı.
- Aynı kaynaktan üretilen JSON, CSV, SQL ve TypeScript verisi.
- Kaynak SHA-256 manifesti ve JSON Schema sözleşmeleri.
- Yalnız sentetik geçerli, geçersiz ve `known/unknown` lookup fixture'ları.
- `parseIban`, `validateTurkishIban`, `getBankCodeFromIban`, `findBankByCode`,
  `identifyBankFromIban`, `formatIban` ve `maskIban` API'leri.
- ESM/CommonJS NPM çıktıları ve gerçek tarball tüketici testleri.
- Privacy scan, veri kalite kontrolleri, CI, scheduled kaynak kontrolü, SBOM ve
  checksum'lı GitHub Release otomasyonu.
- GitHub community health, güvenlik, yönetişim ve katkı belgeleri.

### Security

- Aktif lisans sicilindeki kuruluş kodları, ödeme sistemi katılımcı kanıtı
  olmadan IBAN sağlayıcı kodu olarak yayımlanmaz.
- Gerçek IBAN ve kişisel finansal veri katkı yüzeylerinde yasaktır.

[Unreleased]: https://github.com/trugurpala/turkiye-iban/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/trugurpala/turkiye-iban/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/trugurpala/turkiye-iban/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/trugurpala/turkiye-iban/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/trugurpala/turkiye-iban/releases/tag/v0.1.0
