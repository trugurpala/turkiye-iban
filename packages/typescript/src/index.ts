import { providers } from "./generated/banks.js";

export type ProviderType =
  | "bank"
  | "central_bank"
  | "payment_institution"
  | "electronic_money_institution"
  | "postal_operator"
  | "financial_market_infrastructure";

export interface TurkishIbanProvider {
  code: string;
  rawCode: string;
  nameOfficial: string;
  nameShort: string;
  type: ProviderType;
  status: "active" | "inactive" | "unknown";
  systems: readonly string[];
  ibanEligible: boolean;
  aliases: readonly string[];
  sources: readonly {
    id: string;
    url: string;
    retrievedAt: string;
  }[];
  lastVerifiedAt: string;
}

export type IbanValidationError =
  | "EMPTY_INPUT"
  | "INVALID_COUNTRY_CODE"
  | "INVALID_LENGTH"
  | "INVALID_CHARACTERS"
  | "INVALID_CHECK_DIGITS"
  | "INVALID_PROVIDER_CODE"
  | "INVALID_RESERVE_DIGIT"
  | "INVALID_ACCOUNT_NUMBER";

export interface ParsedTurkishIban {
  input: string;
  normalized: string;
  formatted: string;
  countryCode: string;
  checkDigits: string;
  bankCode: string;
  reserveDigit: string;
  accountNumber: string;
  isValid: boolean;
  errors: IbanValidationError[];
}

export interface IdentifiedTurkishIban {
  parsed: ParsedTurkishIban;
  bankCode: string | null;
  bank: TurkishIbanProvider | null;
  isKnownProvider: boolean;
}

export const turkishBanks: readonly TurkishIbanProvider[] = providers;

const providersByCode = new Map(turkishBanks.map((provider) => [provider.code, provider]));

function normalizeIban(input: string): string {
  return input.replace(/[\s-]/g, "").toUpperCase();
}

function normalizeProviderCode(code: string): string | null {
  const compact = code.replace(/\s/g, "");
  if (!/^\d{1,5}$/.test(compact)) {
    return null;
  }
  return compact.padStart(5, "0");
}

function hasMod97Checksum(iban: string): boolean {
  const rearranged = iban.slice(4) + iban.slice(0, 4);
  let remainder = 0;

  for (const char of rearranged) {
    if (char >= "0" && char <= "9") {
      remainder = (remainder * 10 + Number(char)) % 97;
      continue;
    }

    if (char >= "A" && char <= "Z") {
      const value = char.charCodeAt(0) - 55;
      for (const digit of String(value)) {
        remainder = (remainder * 10 + Number(digit)) % 97;
      }
      continue;
    }

    return false;
  }

  return remainder === 1;
}

export function formatIban(input: string): string {
  const normalized = normalizeIban(input);
  return normalized.match(/.{1,4}/g)?.join(" ") ?? "";
}

export function maskIban(input: string): string {
  const normalized = normalizeIban(input);
  if (normalized.length <= 8) {
    return "*".repeat(normalized.length);
  }

  const masked = normalized.slice(0, 4) + "*".repeat(normalized.length - 8) + normalized.slice(-4);
  return masked.match(/.{1,4}/g)?.join(" ") ?? "";
}

export function getBankCodeFromIban(input: string): string | null {
  const normalized = normalizeIban(input);
  if (!normalized.startsWith("TR") || normalized.length < 9) {
    return null;
  }

  const bankCode = normalized.slice(4, 9);
  return /^\d{5}$/.test(bankCode) ? bankCode : null;
}

export function findBankByCode(code: string): TurkishIbanProvider | null {
  const normalizedCode = normalizeProviderCode(code);
  if (normalizedCode === null) {
    return null;
  }

  return providersByCode.get(normalizedCode) ?? null;
}

export function parseIban(input: string): ParsedTurkishIban {
  const normalized = normalizeIban(input);
  const errors: IbanValidationError[] = [];

  if (normalized.length === 0) {
    errors.push("EMPTY_INPUT");
  }

  if (!/^[A-Z0-9]*$/.test(normalized)) {
    errors.push("INVALID_CHARACTERS");
  }

  if (normalized.length !== 26) {
    errors.push("INVALID_LENGTH");
  }

  const countryCode = normalized.slice(0, 2);
  const checkDigits = normalized.slice(2, 4);
  const bankCode = normalized.slice(4, 9);
  const reserveDigit = normalized.slice(9, 10);
  const accountNumber = normalized.slice(10, 26);

  if (countryCode !== "TR") {
    errors.push("INVALID_COUNTRY_CODE");
  }

  if (!/^\d{2}$/.test(checkDigits)) {
    errors.push("INVALID_CHECK_DIGITS");
  }

  if (!/^\d{5}$/.test(bankCode)) {
    errors.push("INVALID_PROVIDER_CODE");
  }

  if (reserveDigit !== "0") {
    errors.push("INVALID_RESERVE_DIGIT");
  }

  if (!/^\d{16}$/.test(accountNumber)) {
    errors.push("INVALID_ACCOUNT_NUMBER");
  }

  if (
    normalized.length === 26 &&
    /^[A-Z0-9]+$/.test(normalized) &&
    !hasMod97Checksum(normalized)
  ) {
    errors.push("INVALID_CHECK_DIGITS");
  }

  return {
    input,
    normalized,
    formatted: formatIban(normalized),
    countryCode,
    checkDigits,
    bankCode,
    reserveDigit,
    accountNumber,
    isValid: errors.length === 0,
    errors: [...new Set(errors)],
  };
}

export function validateTurkishIban(input: string): boolean {
  return parseIban(input).isValid;
}

export function identifyBankFromIban(input: string): IdentifiedTurkishIban {
  const parsed = parseIban(input);
  const bankCode = getBankCodeFromIban(input);
  const bank = bankCode === null ? null : findBankByCode(bankCode);

  return {
    parsed,
    bankCode,
    bank,
    isKnownProvider: bank !== null,
  };
}
