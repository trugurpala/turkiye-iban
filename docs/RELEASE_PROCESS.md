# Release Process

## Sürümleme

Proje Semantic Versioning kullanır:

- Patch: düzeltme, belge ve geriye uyumlu veri yenilemesi.
- Minor: geriye uyumlu API veya veri alanı eklemesi.
- Major: API, JSON/CSV/SQL veya fixture sözleşmesinde kırıcı değişiklik.

## Ön Kontrol

```bash
python -m pip install -r tools/requirements.txt
npm ci
npm run data:check-remote
npm test
npm pack --workspace packages/typescript --dry-run
npm audit
```

Paket sürümü ile oluşturulacak `vX.Y.Z` etiketi aynı olmalıdır. `CHANGELOG.md`,
kaynak erişim tarihi ve veri farkı release öncesinde güncellenir.

## GitHub Release

İmzalanmış veya doğrulanmış maintainer etiketi `main` commit'ine gönderilir:

```bash
git tag -s v0.1.0 -m "v0.1.0"
git push origin v0.1.0
```

İmzalama anahtarı yoksa maintainer, GitHub'da korunan tag ve hesabının 2FA
korumasıyla annotated tag kullanabilir. `release.yml` iş akışı testleri tekrar
çalıştırır ve şu artifact'ları yayımlar:

- `tr-banks.json`, `tr-banks.csv`, `tr-banks.sql`
- Veri ve kaynak manifesti JSON Schema dosyaları
- Geçerli, geçersiz ve lookup sentetik fixture setleri
- `tr-iban-X.Y.Z.tgz`
- `tr-iban-X.Y.Z.cdx.json` CycloneDX SBOM
- Tüm dosyaları kapsayan `SHA256SUMS.txt`

## İlk NPM Yayını

NPM'de paket henüz yokken ilk yayın, 2FA etkin maintainer hesabıyla bir kez
bootstrap edilir:

```bash
npm login
npm publish --workspace packages/typescript --access public --provenance=false
```

Ardından npmjs.com paket ayarlarında Trusted Publisher şu değerlerle tanımlanır:

- Provider: GitHub Actions
- Organization or user: `trugurpala`
- Repository: `turkiye-iban`
- Workflow filename: `publish-npm.yml`
- Environment: `npm`
- Allowed action: `npm publish`

Sonraki yayınlar GitHub Actions içindeki `Publish NPM` workflow_dispatch akışıyla
OIDC üzerinden yapılır. Uzun ömürlü `NPM_TOKEN` saklanmaz; npm provenance
otomatik üretilir. Akış yalnız eşleşen GitHub Release varsa yayın yapar.

## Geri Alma

Yayımlanmış sürüm sessizce değiştirilmez. Hatalı paket mümkünse `npm deprecate`
ile işaretlenir ve düzeltme yeni patch sürümü olarak yayımlanır. Veri artifact'ı
değiştiyse eski release korunur; yeni sürümde fark ve gerekçe açıklanır.
