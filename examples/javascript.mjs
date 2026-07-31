import {
  formatIban,
  identifyBankFromIban,
  maskIban,
  validateTurkishIban,
} from "../packages/typescript/dist/esm/index.js";

const syntheticIban = "TR510004609999000000000011";
const result = identifyBankFromIban(syntheticIban);

if (!validateTurkishIban(syntheticIban) || result.providerStatus !== "known") {
  throw new Error("Synthetic JavaScript example failed");
}

console.log({
  formatted: formatIban(syntheticIban),
  masked: maskIban(syntheticIban),
  providerCode: result.providerCode,
  providerName: result.provider?.nameOfficial,
});
