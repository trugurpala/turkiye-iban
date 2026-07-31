# Changelog

Tüm önemli değişiklikler bu dosyada belgelenir. Biçim Keep a Changelog ve sürüm
numaraları Semantic Versioning yaklaşımını izler.

## [Unreleased]

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

[Unreleased]: https://github.com/trugurpala/turkiye-iban/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/trugurpala/turkiye-iban/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/trugurpala/turkiye-iban/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/trugurpala/turkiye-iban/releases/tag/v0.1.0
