# turkiye-iban v0.1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use core-pack:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** TCMB kaynaklı kuruluş kodlarını dil bağımsız veri olarak ve Türkiye IBAN araçlarını `tr-iban` NPM paketi olarak yayımlayan GitHub-ready v0.1.0 sürümünü tamamlamak.

**Architecture:** Veri öncelikli küçük monorepo. Ağ kullanan resmî kaynak güncellemesi ile ağsız test/release doğrulaması ayrıdır. TypeScript paketi aynı API'yi ESM ve CommonJS olarak yayımlar.

**Tech Stack:** Python 3.12+, Node.js 22/24, TypeScript, npm workspaces, node:test, JSON Schema 2020-12, SQLite, GitHub Actions.

## Global Constraints

- Runtime paketinde ağ çağrısı ve runtime bağımlılığı olmayacak.
- Gerçek IBAN veya kişisel finansal veri hiçbir fixture, issue, PR ya da örnekte bulunmayacak.
- `validateTurkishIban` biçim/checksum sonucunu sağlayıcı eşleşmesinden ayrı tutacak.
- TCMB aktif kuruluş statüsü IBAN düzenleme yetkisi olarak sunulmayacak.
- Divan yalnız süreç atfıdır; runtime bağımlılığı değildir.
- Yonetim-Paneli entegrasyonu belge ve tüketici sözleşmesi düzeyinde kalacak.

---

### Task 1: Temiz Repo ve Onaylı Belgeler

**Files:** `PROJECT_GOAL.md`, tasarım belgesi, bu plan, `.gitignore`

- [x] Prototipin izlenen dosyalarını gerçek proje klasörüne aktar.
- [x] `agent/turkiye-iban-v0.1.0` geliştirme dalını oluştur.
- [x] Hedef ve tasarımı son `known/unknown` sağlayıcı kararıyla güncelle.
- [x] `git diff --check` ve placeholder taramasını çalıştır.
- [x] İlk belge/baseline commit'ini oluştur.

### Task 2: Test-First IBAN ve Provider API Düzeltmesi

**Files:** `packages/typescript/test/*.test.ts`, `packages/typescript/src/index.ts`

- [x] Alfasayısal hesap alanı için başarısız regresyon testi yaz ve çalıştır.
- [x] Tireli girdinin reddedilmesi için başarısız test yaz ve çalıştır.
- [x] Bilinmeyen sağlayıcının checksum geçerliliğini bozmadan `unknown` dönmesi sözleşmesini test et.
- [x] `provider`, `providerCode`, `providerStatus` ve `dataVersion` alanlarını test-first uygula.
- [x] Tüm TypeScript testlerini çalıştır.

### Task 3: Kanıtlı Veri Modeli ve Ağsız Doğrulama

**Files:** generator, schema, validator, JSON/CSV/SQL, fixture'lar

- [x] `ibanEligible` alanının bulunmamasını ve `codeEvidence` alanını zorunlu kılan başarısız araç testleri yaz.
- [x] Generator ve schema'yı katılımcı kanıtı modeline geçir.
- [x] Lisans sicil kodlarının lookup kümesine yükseltilmemesini test et.
- [x] Fixture'ları `format-valid`, `format-invalid` ve provider lookup beklentileriyle yeniden üret.
- [x] JSON/CSV/SQL eşliği, kod tekilliği, kaynak HTTPS/tarih kontrolü ve SQLite uygulama testlerini ekle.
- [x] `npm test` komutunu tamamen ağsız hale getir; canlı indirmeyi `npm run data:update` altında tut.

### Task 4: Çift Modül NPM Paketi

**Files:** TypeScript build config, package manifest, tüketici smoke testleri

- [x] ESM ve CommonJS tüketici smoke testlerini önce başarısız çalıştır.
- [x] Koşullu `exports`, tip bildirimi ve JSON alt-yol export'unu uygula.
- [x] Node `>=22` engine ve Node 22/24 test matrisini ayarla.
- [x] Gerçek tarball allowlist ve tüketici testini geçir.

### Task 5: Topluluk, Güvenlik ve Release Otomasyonu

**Files:** `.github/**`, README ve politika belgeleri

- [x] GitHub issue form/PR template sözdizimini ve gerçek repo bağlantılarını doğrula.
- [x] `CODEOWNERS`, Dependabot, CI, data-check ve release/publish workflow'larını ekle.
- [x] Workflow izinlerini minimum kapsamda tanımla; release dışında `contents: read` kullan.
- [x] README, API, veri politikası, release ve Yonetim-Paneli belgelerini güncelle.

### Task 6: Release Artefact ve Temiz Tüketici Doğrulaması

**Files:** release hazırlama araçları ve kalite testleri

- [x] JSON, CSV, SQL, schema, fixture, SHA-256, SBOM ve tarball üret.
- [x] Temiz geçici klasörde tarball'ı ESM ve CommonJS ile tüket.
- [x] Gizlilik taraması, schema, SQLite, tam test ve build komutlarını çalıştır.
- [x] `git diff --check`, tracked-file hijyeni ve placeholder taramasını çalıştır.

### Task 7: GitHub ve NPM Yayını

**External interfaces:** `trugurpala/turkiye-iban`, npm `tr-iban`

- [x] Doğrulanmış değişiklikleri amaçlı commit'lere ayır.
- [x] Public GitHub reposunu oluştur, dalı push et ve CI sonucunu doğrula.
- [x] Repo açıklaması, topics, merge ayarları, branch koruması ve private vulnerability reporting'i yapılandır.
- [x] `v0.1.0` tag ve GitHub Release'i artefact/checksumlarla yayımla.
- [ ] NPM kimlik doğrulaması mevcutsa `tr-iban@0.1.0` yayımla ve kurulumla doğrula.
- [x] NPM kimlik doğrulaması yoksa tarball/provenance workflow'unu tamamlayıp tek dış bağımlılığı açıkça raporla.
