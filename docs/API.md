# API Reference

`tr-iban`, Node.js 22+ üzerinde ESM ve CommonJS olarak yayımlanır. Runtime ağ
çağrısı veya runtime bağımlılığı yoktur.

## `parseIban(input: string)`

Boşlukları kaldırır, harfleri büyütür ve Türkiye IBAN alanlarını döndürür:
`countryCode`, `checkDigits`, `bankCode`, `reserveDigit`, `accountNumber`,
`normalized`, `formatted`, `isValid` ve `errors`.

Türkiye sözleşmesi: `TR` + 2 kontrol hanesi + 5 haneli sağlayıcı kodu + `0`
rezerv alanı + 16 alfasayısal hesap alanı. Tire gibi başka ayraçlar kabul
edilmez.

## `validateTurkishIban(input: string): boolean`

Uzunluk, karakterler, ülke, rezerv alan ve MOD 97-10 checksum kontrolünü yapar.
Sağlayıcı kodunun veri kümesinde bulunması bu doğrulamanın parçası değildir.

## `getBankCodeFromIban(input: string): string | null`

TR önekli yeterli uzunluktaki girdiden beş haneli sağlayıcı alanını çıkarır.
Adındaki `Bank` geriye uyumluluk içindir; alan ödeme hizmeti sağlayıcısını ifade
eder.

## `findBankByCode(code: string): TurkishIbanProvider | null`

`46`, `0046` ve `00046` değerlerini `00046` biçimine getirip doğrulanmış
katılımcı kümesinde arar. Yalnız lisans kaydı bulunan kodları eşleşme saymaz.

## `identifyBankFromIban(input: string): IdentifiedTurkishIban`

Parse ve lookup işlemini birleştirir:

```ts
{
  parsed: ParsedTurkishIban;
  providerCode: string | null;
  provider: TurkishIbanProvider | null;
  providerStatus: "known" | "unknown";
  dataVersion: string;
}
```

`bankCode`, `bank` ve `isKnownProvider` alanları v0.x geriye uyumluluk alias'larıdır.

## `formatIban(input: string): string`

Normalize edilmiş değeri dörtlü gruplar halinde döndürür.

## `maskIban(input: string): string`

İlk ve son dört karakteri korur, orta alanı `*` ile maskeler. Ham IBAN'ı loglamak
yerine bu fonksiyonu kullanın.

## Doğrulama Sınırı

API hesabın varlığını, sahibini, ad eşleşmesini, bakiyeyi veya transfer
yapılabilirliğini doğrulamaz. `known` yalnız sağlayıcı kodu eşleşmesidir.
