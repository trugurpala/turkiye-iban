# Lansman Ölçüm Planı

Amaç popülerlik yarışması değil; belgelerin anlaşılır olup olmadığını, paketin kullanılmaya başlanıp başlanmadığını ve hangi katkı alanlarının ilgi gördüğünü öğrenmektir. Pakete analitik, çerez veya telemetri eklenmez.

## Başlangıç değeri

`2026-07-31` lansman öncesi GitHub değerleri:

| Ölçü | Başlangıç |
| --- | ---: |
| Star | 0 |
| Fork | 0 |
| Açık issue | 0 |
| Görüntüleme | 0 |
| Benzersiz ziyaretçi | 0 |
| Clone | 0 |
| Benzersiz clone | 0 |

## Takip tablosu

| Ölçü | Başlangıç | 7. gün | 30. gün |
| --- | ---: | ---: | ---: |
| GitHub star | 0 | - | - |
| GitHub fork | 0 | - | - |
| Açılan issue | 0 | - | - |
| Dış katkıcı | 0 | - | - |
| Benzersiz ziyaretçi | 0 | - | - |
| Benzersiz clone | 0 | - | - |
| NPM haftalık indirme | 0 | - | - |

## Komutlar

Repo ve topluluk sayıları:

```bash
gh repo view trugurpala/turkiye-iban --json stargazerCount,forkCount,issues
gh api repos/trugurpala/turkiye-iban/contributors
```

Son 14 günlük GitHub trafiği yalnız maintainer yetkisiyle alınabilir:

```bash
gh api repos/trugurpala/turkiye-iban/traffic/views
gh api repos/trugurpala/turkiye-iban/traffic/clones
```

NPM haftalık indirme sayısı:

```bash
curl https://api.npmjs.org/downloads/point/last-week/tr-iban
```

## Yorumlama

- Ziyaret var, kurulum yoksa NPM README ve ilk kullanım örneği yeniden incelenir.
- Kurulum var, issue yoksa bu tek başına sorun sayılmaz; küçük kütüphaneler sessizce kullanılabilir.
- Aynı soru tekrarlanıyorsa README veya API belgesine açıklama eklenir.
- Veri düzeltme talepleri artarsa kaynak kanıtı ve güncelleme otomasyonu önceliklendirilir.
- PHP veya Python talebi somut kullanımla gelirse ilgili roadmap fazı öne alınır.

Kişi bazlı takip yapılmaz ve kullanıcıdan kullanım verisi istenmez.
