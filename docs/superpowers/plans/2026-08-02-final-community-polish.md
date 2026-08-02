# Final Community Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `core-pack:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Safely reject non-string JavaScript IBAN inputs and polish the public Turkish risk register without changing data or public API semantics.

**Architecture:** The TypeScript runtime retains its existing public `string` signatures but hardens the internal normalizer, which is the one entry point used by all input-handling helpers. A focused runtime-cast regression test proves that JavaScript misuse produces the existing invalid/unknown result. The public risk register receives language-only corrections protected by the repository's quality test.

**Tech Stack:** TypeScript, Node.js built-in test runner, Python `unittest`, npm workspaces, GitHub Actions.

## Global Constraints

- Preserve `parseIban`, `validateTurkishIban`, `getBankCodeFromIban`, `findBankByCode`, `identifyBankFromIban`, `formatIban`, and `maskIban` exports and TypeScript signatures.
- Do not change `data/source/`, fixtures, schemas, or generated data.
- Do not introduce runtime dependencies or network access.
- Only synthetic IBAN values may appear in tests and documentation.
- This is an Unreleased maintenance patch; do not tag, publish, or change the NPM version.

---

### Task 1: Add the non-string input regression test

**Files:**
- Modify: `packages/typescript/test/index.test.ts`

**Interfaces:**
- Consumes: existing public functions accepting `string` at compile time.
- Produces: a runtime regression contract for JavaScript values that bypass TypeScript.

- [ ] **Step 1: Add the failing test**

```ts
it("rejects non-string JavaScript input without throwing", () => {
  const input = null as unknown as string;

  assert.equal(validateTurkishIban(input), false);
  assert.equal(getBankCodeFromIban(input), null);
  assert.equal(formatIban(input), "");
  assert.equal(maskIban(input), "");
  assert.equal(parseIban(input).isValid, false);
  assert.equal(identifyBankFromIban(input).providerStatus, "unknown");
});
```

- [ ] **Step 2: Run the focused test and confirm the current runtime throws**

Run: `npm -w packages/typescript run test:unit`

Expected before the implementation: failure caused by calling a string method
on `null`.

- [ ] **Step 3: Commit the test with the implementation task**

No separate commit is needed for a small regression fix; include the test and
the narrow implementation in one reviewable commit.

### Task 2: Harden the internal input boundary

**Files:**
- Modify: `packages/typescript/src/index.ts`
- Test: `packages/typescript/test/index.test.ts`

**Interfaces:**
- Consumes: `normalizeIban` used by formatting, masking, parsing, and provider-code extraction.
- Produces: empty normalization for non-string runtime inputs; all existing string paths are unchanged.

- [ ] **Step 1: Implement string-only normalization**

```ts
function normalizeIban(input: unknown): string {
  if (typeof input !== "string" || isOversizedInput(input)) {
    return "";
  }
  return input.replace(/\s/g, "").toUpperCase();
}
```

At the start of `parseIban`, derive `rawInput` from `typeof input === "string"`
before returning its typed `input` field. Keep the existing errors, including
the empty-input path, rather than adding a new public error enum member.

- [ ] **Step 2: Run focused tests**

Run: `npm -w packages/typescript run test:unit`

Expected: 13 tests pass and no existing string-input expectation changes.

### Task 3: Polish the Turkish public documents and their quality guards

**Files:**
- Modify: `docs/RISK_REGISTER.md`
- Modify: `docs/clients/PHP_CLIENT.md`
- Modify: `docs/clients/PYTHON_CLIENT.md`
- Modify: `tools/test_quality_scripts.py`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: the risk-register quality test's required prohibited-claim phrases.
- Produces: correctly spelled Turkish public documentation and an Unreleased
  entry that accurately describes both improvements.

- [ ] **Step 1: Replace ASCII-only Turkish with correct Turkish spelling**

Correct headings, prose, risk-table cells, prohibited phrases, and the linked
PHP/Python client decision records. Keep technical decisions, version claims,
URLs, API identifiers, and the meaning of the following explicit prohibitions
intact:

```text
"TCMB onaylı"
"hesabı doğrular"
"transfer garantisi verir"
"her dilde paket hazır"
```

- [ ] **Step 2: Update the matching quality assertions**

Replace the corresponding ASCII literals in
`QualityScriptsTest.test_residual_risk_register_is_linked_from_public_surfaces`
and the Packagist risk phrase in
`QualityScriptsTest.test_separate_language_client_designs_are_decision_records`
with their exact UTF-8 public wording.

- [ ] **Step 3: Add the Unreleased changelog entry**

Under `## [Unreleased]`, add a `### Fixed` entry that states non-string runtime
inputs are rejected safely, and a `### Changed` entry that records the Turkish
risk-register copy correction.

- [ ] **Step 4: Run the targeted quality test**

Run: `python -m unittest tools.test_quality_scripts.QualityScriptsTest.test_residual_risk_register_is_linked_from_public_surfaces`

Expected: `OK`.

### Task 4: Verify the maintenance patch and prepare its PR

**Files:**
- Verify: repository-wide public surfaces and generated-data status.

**Interfaces:**
- Consumes: completed runtime, test, and documentation changes.
- Produces: evidence for a documentation/runtime maintenance PR with no release.

- [ ] **Step 1: Run the complete quality suite**

Run: `npm test`

Expected: format, lint, typecheck, generated-data drift, data parity, privacy,
unit, integration, examples, and release-asset tests pass.

- [ ] **Step 2: Inspect publication contents and dependency advisories**

Run:

```bash
npm pack --workspace packages/typescript --dry-run
npm audit --json
python -m pip_audit -r tools/requirements.txt
```

Expected: package contains only intended public files and no known advisories
are reported.

- [ ] **Step 3: Review the diff and public surfaces**

Run:

```bash
git diff --check
git status --short
```

Confirm README, API docs, data schema, data sources, SECURITY, CONTRIBUTING,
RELEASE, package metadata, issue forms, and PR template were reviewed; only
the surfaces identified in the design change.

- [ ] **Step 4: Commit and open a ready-for-review PR**

Run:

```bash
git add CHANGELOG.md docs/RISK_REGISTER.md docs/superpowers/specs/2026-08-02-final-community-polish-design.md docs/superpowers/plans/2026-08-02-final-community-polish.md packages/typescript/src/index.ts packages/typescript/test/index.test.ts tools/test_quality_scripts.py
git commit -m "fix: harden public input boundary"
git push -u origin codex/final-community-polish
```

Create a PR whose description reports the tested runtime fix, Turkish copy
polish, unchanged data/API status, and the reviewed public surfaces.

## Self-Review

- Scope coverage: runtime boundary, regression test, language quality, changelog,
  full verification, and PR evidence each have a task.
- No placeholder scan: no TODO/TBD or deferred implementation steps appear.
- Contract consistency: all behavior remains behind the existing public
  string-typed API and maps non-string runtime values to the already-supported
  empty invalid-input path.
