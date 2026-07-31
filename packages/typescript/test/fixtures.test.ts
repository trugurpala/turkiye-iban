import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  getBankCodeFromIban,
  identifyBankFromIban,
  type IbanValidationError,
  parseIban,
  validateTurkishIban,
} from "../src/index.js";

interface ValidFixture {
  iban: string;
  providerCode: string;
  rawCode: string;
  providerName: string;
  synthetic: true;
}

interface InvalidFixture {
  iban: string;
  reason:
    | "invalid_check_digits"
    | "invalid_country"
    | "invalid_length"
    | "invalid_character"
    | "invalid_reserve_digit";
}

interface LookupFixture {
  iban: string;
  providerCode: string;
  providerStatus: "known" | "unknown";
  synthetic: true;
}

function loadJsonFixture<T>(relativePath: string): T {
  return JSON.parse(readFileSync(new URL(relativePath, import.meta.url), "utf8")) as T;
}

describe("synthetic fixture contract", () => {
  const validFixtures = loadJsonFixture<ValidFixture[]>("../../../../fixtures/valid.synthetic.json");
  const invalidFixtures = loadJsonFixture<InvalidFixture[]>("../../../../fixtures/invalid.synthetic.json");
  const lookupFixtures = loadJsonFixture<LookupFixture[]>("../../../../fixtures/lookup.synthetic.json");

  it("validates every generated valid fixture", () => {
    assert.ok(validFixtures.length >= 50);

    for (const fixture of validFixtures) {
      const identified = identifyBankFromIban(fixture.iban);

      assert.equal(fixture.synthetic, true);
      assert.equal(validateTurkishIban(fixture.iban), true, fixture.iban);
      assert.equal(getBankCodeFromIban(fixture.iban), fixture.providerCode);
      assert.equal(identified.isKnownProvider, true, fixture.iban);
      assert.equal(identified.bank?.rawCode, fixture.rawCode, fixture.iban);
    }
  });

  it("keeps unknown provider fixtures format-valid but lookup-unknown", () => {
    const fixture = lookupFixtures.find((item) => item.providerStatus === "unknown");
    assert.ok(fixture);

    const identified = identifyBankFromIban(fixture.iban);

    assert.equal(identified.parsed.isValid, true);
    assert.equal(identified.providerCode, fixture.providerCode);
    assert.equal(identified.providerStatus, "unknown");
    assert.equal(identified.provider, null);
    assert.match(identified.dataVersion, /^\d{4}-\d{2}-\d{2}$/);
  });

  it("rejects invalid fixtures for their documented reason", () => {
    const expectedErrors = new Map<InvalidFixture["reason"], IbanValidationError>([
      ["invalid_check_digits", "INVALID_CHECK_DIGITS"],
      ["invalid_country", "INVALID_COUNTRY_CODE"],
      ["invalid_length", "INVALID_LENGTH"],
      ["invalid_character", "INVALID_CHARACTERS"],
      ["invalid_reserve_digit", "INVALID_RESERVE_DIGIT"],
    ]);

    for (const fixture of invalidFixtures) {
      const parsed = parseIban(fixture.iban);
      const expectedError = expectedErrors.get(fixture.reason);

      assert.equal(parsed.isValid, false, fixture.iban);
      assert.ok(expectedError && parsed.errors.includes(expectedError), fixture.iban);
    }
  });
});
