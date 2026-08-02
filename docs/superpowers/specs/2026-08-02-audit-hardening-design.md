# Audit Hardening Design

**Goal:** Remove the proven developer-experience, data-import, privacy-scan,
and oversized-input risks without changing the public Turkish IBAN API or the
canonical institution dataset.

## Approaches considered

1. **Documentation-only mitigation.** Explain the risks and leave the runtime,
   generator, and test tooling unchanged. This is insufficient because the
   audit reproduced destructive cleanup, non-idempotent SQL, and unbounded
   work on large strings.
2. **Focused hardening of the existing architecture.** Keep the public API and
   canonical source stable; add small guards, deterministic SQL refresh
   semantics, narrower cleanup, and regression tests. This is selected because
   it fixes the observed behavior while preserving every consumer contract.
3. **New validation layer or package major version.** Add new result types or a
   separate server-oriented API. This would create unnecessary public surface
   and is outside the patch-level risk-reduction scope.

## Design

The TypeScript package continues to expose the same functions and result
types. A shared input boundary rejects inputs longer than 1,024 characters
before normalization and returns the existing validation/error shape. The
existing normal 26-character Turkish IBAN flow remains unchanged.

The generator emits SQL as a transaction that replaces the reference table
contents deterministically, with explicit insert column names. Applying the
same generated SQL twice to the same SQLite database therefore succeeds and
leaves exactly the canonical rows.

The privacy scanner recognizes compact, whitespace-separated, hyphen-separated,
and line-wrapped Turkish IBAN-like strings. It compares a separator-normalized
value to the existing synthetic-fixture allowlist. It remains a text-file
heuristic and documentation states that images and issue/PR submissions still
need human review.

Developer tooling ignores in-repository Python virtual environments and only
cleans test-owned temporary release artifact directories. The quality suite
contains regressions for these contracts.

## Compatibility and release

- No exported TypeScript function, import path, provider field, or canonical
  record changes.
- Existing valid and invalid IBAN results are preserved; only oversized inputs
  stop allocating formatted/masked output proportional to the supplied text.
- Generated data contents stay identical; generated SQL syntax changes to gain
  safe repeatability.
- This is a patch-level release candidate after full verification.

## Acceptance criteria

1. A `.venv` in the repository does not make `npm run format:check` inspect
   third-party files.
2. The release-artifact quality test never deletes a pre-existing repository
   `release-artifacts` directory.
3. Generated SQL can be executed twice against one SQLite database and retains
   JSON parity.
4. Privacy scanning rejects unapproved IBAN-like values using spaces, hyphens,
   or line breaks while allowing only declared synthetic fixtures.
5. A 1,025-character runtime input returns existing validation errors without
   allocating a 1,025-character formatted or masked value.
6. Full repository verification, package build, generated-data drift checks,
   and audit commands succeed.
