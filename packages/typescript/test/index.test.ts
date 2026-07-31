import { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  findBankByCode,
  formatIban,
  getBankCodeFromIban,
  identifyBankFromIban,
  maskIban,
  parseIban,
  turkishBanks,
  validateTurkishIban,
} from "../src/index.js";

describe("Turkish IBAN API", () => {
  it("validates a synthetic Akbank IBAN", () => {
    const iban = "TR510004609999000000000011";

    assert.equal(validateTurkishIban(iban), true);
    assert.equal(getBankCodeFromIban(iban), "00046");
    assert.equal(findBankByCode("0046")?.nameOfficial, "AKBANK T.A.Ş.");
    assert.equal(identifyBankFromIban(iban).bank?.rawCode, "0046");
  });

  it("parses all Turkish IBAN parts", () => {
    const parsed = parseIban("TR51 0004 6099 9900 0000 0000 11");

    assert.equal(parsed.countryCode, "TR");
    assert.equal(parsed.checkDigits, "51");
    assert.equal(parsed.bankCode, "00046");
    assert.equal(parsed.reserveDigit, "0");
    assert.equal(parsed.accountNumber, "9999000000000011");
    assert.deepEqual(parsed.errors, []);
  });

  it("formats and masks IBANs without changing validation semantics", () => {
    const iban = "tr510004609999000000000011";

    assert.equal(formatIban(iban), "TR51 0004 6099 9900 0000 0000 11");
    assert.equal(maskIban(iban), "TR51 **** **** **** **** **00 11");
  });

  it("separates unknown provider code from checksum validation", () => {
    const result = identifyBankFromIban("TR16999990ABC123DEF456GHIJ");
    const providerResult = result as unknown as {
      providerCode: string | null;
      provider: unknown;
      providerStatus: "known" | "unknown";
    };

    assert.equal(result.parsed.isValid, true);
    assert.equal(result.bankCode, "99999");
    assert.equal(result.isKnownProvider, false);
    assert.equal(result.bank, null);
    assert.equal(providerResult.providerCode, "99999");
    assert.equal(providerResult.provider, null);
    assert.equal(providerResult.providerStatus, "unknown");
  });

  it("accepts the alphanumeric account field allowed by the Turkish IBAN format", () => {
    const iban = "TR56000460ABC123DEF456GHIJ";
    const parsed = parseIban(iban);

    assert.equal(parsed.isValid, true);
    assert.equal(parsed.accountNumber, "ABC123DEF456GHIJ");
    assert.deepEqual(parsed.errors, []);
  });

  it("rejects hyphens instead of silently normalizing them", () => {
    const parsed = parseIban("TR51-0004-6099-9900-0000-0000-11");

    assert.equal(parsed.isValid, false);
    assert.ok(parsed.errors.includes("INVALID_CHARACTERS"));
  });

  it("reports invalid reserve digit", () => {
    const parsed = parseIban("TR510004619999000000000011");

    assert.equal(parsed.isValid, false);
    assert.ok(parsed.errors.includes("INVALID_RESERVE_DIGIT"));
  });

  it("loads the generated provider dataset", () => {
    assert.ok(turkishBanks.length >= 50);
    assert.equal(findBankByCode("46")?.code, "00046");
    assert.equal(findBankByCode("913"), null);
  });
});
