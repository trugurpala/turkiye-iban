# GitHub Community Files

GitHub Community Profile, desteklenen konumlardaki README, LICENSE,
CODE_OF_CONDUCT, CONTRIBUTING, SECURITY ve issue template dosyalarını denetler.
Bu repo proje-özel politika gerektiği için dosyaları kendi kökünde ve `.github`
altında tutar.

## Repo Yapısı

- Kök: `README.md`, `LICENSE`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`,
  `SECURITY.md`, `SUPPORT.md`, `GOVERNANCE.md`, `MAINTAINERS.md`, `CHANGELOG.md`.
- `.github/ISSUE_TEMPLATE/*.yml`: şemalı bug, veri ve özellik issue formları.
- `.github/ISSUE_TEMPLATE/config.yml`: boş issue'ları kapatır, güvenlik
  bildirimini Private Vulnerability Reporting'e yönlendirir.
- `.github/pull_request_template.md`: kaynak, gizlilik ve test kontrolü.
- `.github/CODEOWNERS`: genel ve veri-kritik dosya sahipliği.
- `.github/dependabot.yml`: NPM ve GitHub Actions güncellemeleri.
- `.github/workflows/`: CI, kaynak kontrolü, release ve NPM yayını.

GitHub'ın community profile API sonucu public yayın sonrası kontrol edilir.
Private Vulnerability Reporting ayrıca repository ayarından etkinleştirilir.

## Resmî Referanslar

2026-07-31 tarihinde kontrol edilen GitHub belgeleri:

- https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms
- https://docs.github.com/en/actions/reference/security/secure-use
- https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference
