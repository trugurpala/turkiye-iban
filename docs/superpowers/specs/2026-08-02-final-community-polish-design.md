# Final Community Polish Design

## Goal

Make the public `turkiye-iban` repository a little safer and more polished for
real JavaScript consumers without changing its IBAN data contract, provider
lookup semantics, or published package API.

## Context

The final readiness review verified that the repository has no open pull
requests or issues, GitHub Community Health reports 100%, recent CI, GitHub
Release, and NPM publishing workflows succeeded, and `main` is protected by
the legacy GitHub branch-protection API. The API reports no rulesets because
the protection is not implemented as a ruleset; it still requires the Node 22
and Node 24 CI checks, disallows force pushes and deletion, enforces linear
history, and requires resolved conversations.

Two bounded improvements remain worthwhile:

1. JavaScript callers can bypass TypeScript's `string` annotations and pass a
   non-string value. The public helpers should reject that input safely instead
   of throwing while attempting string methods.
2. `docs/RISK_REGISTER.md` and the linked PHP/Python client decision records
   are public Turkish documentation but were written in ASCII-only Turkish.
   They should use correct Turkish spelling and preserve their claim-control
   tests.

## Options Considered

### 1. Documentation-only closeout

Record the review and make no runtime change. This avoids code churn but leaves
JavaScript callers exposed to a trivial type-error path.

### 2. Broad API/type redesign

Change every public signature to accept `unknown` and introduce new validation
errors. This is explicit but expands the public contract and is unnecessary
for the concrete runtime failure.

### 3. Recommended: defensive runtime boundary plus focused documentation polish

Keep all public TypeScript signatures and error values stable. Normalize only
runtime strings, treat non-string values as empty input, and cover the behavior
with a regression test. Correct the risk register's Turkish copy and adjust its
quality assertions to check the real public wording.

## Design

`normalizeIban` becomes the runtime boundary: it accepts `unknown` internally
and returns an empty normalized value for non-strings or oversized strings.
`parseIban` stores a string-only input value before constructing its typed
result, so a JavaScript `null` or object never escapes through a field declared
as `string`. Existing string behavior, including whitespace normalization,
MOD 97-10 validation, error names, provider lookup, formatting, and masking,
remains unchanged.

The regression test invokes all relevant public helpers through a runtime cast
with `null`. The expected result is a normal invalid/unknown response, not an
exception and not a new error type.

The risk register and linked client decision records receive Turkish characters
and spelling corrections only. The risk register's prohibited-claim list stays
explicit and the quality tests check those same visible phrases.

## Non-Goals

- No institution, source, schema, fixture, or generated-data changes.
- No public API name, TypeScript signature, export, or package-layout change.
- No Node-version support change.
- No new GitHub ruleset: existing branch protection already supplies the
  desired controls and replacing it would be unrelated configuration churn.
- No GitHub Release or NPM publish for this unshipped maintenance patch unless
  a maintainer explicitly selects a later patch release.

## Verification

- Run the focused TypeScript unit tests after adding the failing regression
  case and after the implementation.
- Run the complete `npm test` suite.
- Run `npm pack --workspace packages/typescript --dry-run` to inspect package
  contents.
- Run `npm audit --json` and `python -m pip_audit -r tools/requirements.txt`.
- Confirm generated data remains unchanged and the working tree contains only
  the intended runtime, test, documentation, changelog, and planning files.

## Public Surface Review

- README: reviewed; no change required because usage and API names remain the
  same.
- CHANGELOG: add an Unreleased fixed entry.
- API documentation: reviewed; no change required because the exported TypeScript
  contract remains stable.
- Risk register and linked client decision records: update Turkish spelling and
  retain claim boundaries.
- CONTRIBUTING, SECURITY, DATA_SCHEMA, DATA_SOURCES, RELEASE, package metadata,
  issue forms, and PR template: reviewed; no change required.
