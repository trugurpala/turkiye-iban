# Cross-Client Final Readiness Design

## Goal

Keep `turkiye-iban`, `turkiye-iban-python`, and `turkiye-iban-php` truthful,
easy to adopt, and consistent for public users without changing the canonical
Turkish IBAN dataset or making unsupported package-index claims.

## Evidence

- The main repository is healthy, protected, and publishes `tr-iban@0.2.2`.
- `turkiye-iban==0.1.5` is indexed on PyPI; the downloaded wheel SHA-256 and a
  clean virtual-environment synthetic smoke test match the published evidence.
- `trugurpala/turkiye-iban` is absent from Packagist's public p2 endpoint
  (HTTP 404). PHP documentation must continue to present GitHub Release as the
  verified route and Composer/Packagist as a future route.
- Both client repositories protect `main` with version-matrix CI, blocked
  force-push/deletion, and linear history. They do not yet require resolved
  review conversations.
- Windows checkouts with `core.autocrlf=true` turn JSON fixture line endings
  into CRLF. Both client conformance tests currently hash raw bytes, so they
  fail locally even though the canonical LF fixture content is correct.

## Chosen Design

The main repository records this coordinated maintenance decision. The Python
and PHP repositories each receive a focused, independently testable patch:

1. Normalize CRLF to LF only while calculating the conformance fixture digest.
   The manifest still verifies every meaningful fixture byte; the one Git
   checkout transport difference is made platform-neutral.
2. Make the main repository's Discussions page visible in each client README.
   Client repositories keep issues for reproducible defects while conceptual
   and cross-language discussion has one public home.
3. Correct Python's README to lead with the verified PyPI installation command
   for `0.1.5`, with the GitHub wheel retained as a pinned fallback.
4. Keep PHP's Packagist warning unchanged because its public index remains
   unverified.
5. Enable GitHub's resolved-conversation requirement on the protected client
   `main` branches to match the primary repository.

## Non-Goals

- No provider data, schema, fixture content, checksum manifest, or conformance
  version change.
- No unverified Packagist submission or Composer publication.
- No new client Discussions spaces, avoiding fragmented community support.
- No runtime API or package version change; this is source/test/documentation
  maintenance, not a package release.
- No claim that Dependabot alerts are enabled: the current GitHub credential
  cannot inspect or configure that feature.

## Verification

- Python: pytest, coverage gate, mypy, build, Twine check, and a clean PyPI
  install smoke test using a synthetic IBAN.
- PHP: Composer test, PHPStan, asset checksum preparation, and the published
  CI matrix. If the local PHP runtime lacks OpenSSL/Composer support, report
  that exact environmental limitation and rely on the verified GitHub matrix
  only for the unavailable local commands.
- All repositories: diff hygiene, live GitHub CI on the merge commit, and
  public README/release state re-read after merge.
