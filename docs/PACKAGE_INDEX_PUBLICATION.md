# Package Index Publication

Bu belge, ayrı PHP ve Python istemcilerinin GitHub release'lerinden ekosistem
indekslerine taşınma durumunu kaydeder. GitHub release'i ile Packagist/PyPI
indeks yayını aynı şey değildir.

## Current status

| Client | GitHub repository | Verified GitHub release | Package index | Current status |
| --- | --- | --- | --- | --- |
| NPM | [tr-iban](https://github.com/trugurpala/turkiye-iban/tree/main/packages/typescript) | [v0.2.1](https://github.com/trugurpala/turkiye-iban/releases/tag/v0.2.1) | [npmjs.com/package/tr-iban](https://www.npmjs.com/package/tr-iban) | Published; `latest` is `0.2.1` |
| PHP | [turkiye-iban-php](https://github.com/trugurpala/turkiye-iban-php) | [v0.1.5](https://github.com/trugurpala/turkiye-iban-php/releases/tag/v0.1.5) | Packagist `trugurpala/turkiye-iban` | Index entry not verified |
| Python | [turkiye-iban-python](https://github.com/trugurpala/turkiye-iban-python) | [v0.1.5](https://github.com/trugurpala/turkiye-iban-python/releases/tag/v0.1.5) | [PyPI `turkiye-iban`](https://pypi.org/project/turkiye-iban/) | Published `0.1.5` via OIDC; clean install verified |

## Verification record

The public indexes were checked on 2026-08-02:

- NPM returned `tr-iban@0.2.1` with the `latest` dist-tag.
- Packagist returned HTTP 404 for `trugurpala/turkiye-iban`.
- PyPI returned `turkiye-iban` version `0.1.5`.
- An unauthenticated Packagist submission was rejected; no package was
  created. Packagist requires the repository owner account or API token.
- GitHub environments `pypi` and `testpypi` exist in the Python client and
  require approval from `trugurpala` before the OIDC publish job can run.
- The protected `pypi` workflow for `v0.1.5` passed pytest, 98.18% coverage,
  mypy, build and Twine checks. A clean virtualenv install and synthetic IBAN
  smoke test passed.

## PHP / Packagist

The PHP repository already contains a public `composer.json` with package name
`trugurpala/turkiye-iban`, PSR-4 autoloading, PHP `>=8.2`, and MIT metadata.
After the repository owner submits the package to Packagist, the Packagist
GitHub webhook should be enabled so new Git tags are imported automatically.
The first public index page and a clean `composer require` installation must be
checked before README installation instructions claim Packagist availability.

Submit URL: <https://packagist.org/packages/submit>. Use the repository URL
`https://github.com/trugurpala/turkiye-iban-php`, then verify the package page
and `composer require trugurpala/turkiye-iban` from a clean temporary project.

## Python / PyPI

The Python repository contains a manual `publish-pypi.yml` workflow. It builds
the package, runs pytest, coverage, mypy, wheel/sdist build and `twine check`,
then uses OIDC Trusted Publishing in a protected `testpypi` or `pypi`
environment. The `pypi` Trusted Publisher is configured and published
`turkiye-iban==0.1.5`.

No long-lived PyPI token is required or stored in the repository.

The required PyPI Trusted Publisher values are: owner `trugurpala`, repository
`turkiye-iban-python`, workflow `publish-pypi.yml`, environment `pypi`, and
project `turkiye-iban`. TestPyPI uses the same values with environment
`testpypi`. The GitHub environments are protected by maintainer approval.

## Release language

Use these claims only after the corresponding public index has been verified:

- Before indexing: “GitHub release hazır; Packagist/PyPI indeks yayını bekliyor.”
- After indexing and clean install: “Python paketi PyPI'da yayımlandı; temiz
  kurulum doğrulandı.” Packagist için bu ifade henüz kullanılamaz.

Do not claim that a package is available on Packagist or PyPI from a GitHub
release URL alone. Neither client verifies account existence, account ownership,
licensing, or transferability.
