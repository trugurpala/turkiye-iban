# Package Index Publication

Bu belge, ayrı PHP ve Python istemcilerinin GitHub release'lerinden ekosistem
indekslerine taşınma durumunu kaydeder. GitHub release'i ile Packagist/PyPI
indeks yayını aynı şey değildir.

## Current status

| Client | GitHub repository | Verified GitHub release | Package index | Current status |
| --- | --- | --- | --- | --- |
| PHP | [turkiye-iban-php](https://github.com/trugurpala/turkiye-iban-php) | [v0.1.5](https://github.com/trugurpala/turkiye-iban-php/releases/tag/v0.1.5) | Packagist `trugurpala/turkiye-iban` | Index entry not verified |
| Python | [turkiye-iban-python](https://github.com/trugurpala/turkiye-iban-python) | [v0.1.2](https://github.com/trugurpala/turkiye-iban-python/releases/tag/v0.1.2) | PyPI `turkiye-iban` | Trusted Publisher not configured; index entry not verified |

## PHP / Packagist

The PHP repository already contains a public `composer.json` with package name
`trugurpala/turkiye-iban`, PSR-4 autoloading, PHP `>=8.2`, and MIT metadata.
After the repository owner submits the package to Packagist, the Packagist
GitHub webhook should be enabled so new Git tags are imported automatically.
The first public index page and a clean `composer require` installation must be
checked before README installation instructions claim Packagist availability.

## Python / PyPI

The Python repository contains a manual `publish-pypi.yml` workflow. It builds
the package, runs pytest, mypy, wheel/sdist build and `twine check`, then uses
OIDC Trusted Publishing in a protected `testpypi` or `pypi` environment. A
maintainer must register the pending publisher on the matching package index
before running it.

No long-lived PyPI token is required or stored in the repository.

## Release language

Use these claims only after the corresponding public index has been verified:

- Before indexing: “GitHub release hazır; Packagist/PyPI indeks yayını bekliyor.”
- After indexing and clean install: “Composer/PyPI paketi yayımlandı.”

Do not claim that a package is available on Packagist or PyPI from a GitHub
release URL alone. Neither client verifies account existence, account ownership,
licensing, or transferability.
