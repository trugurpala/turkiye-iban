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

Girdi 1.024 karakterden uzunsa API bunu `INVALID_LENGTH` olarak reddeder.
Bu sınır, HTTP gibi bir dış giriş noktasında büyük metinlerin gereksiz bellek
kullanmasına karşı istemci tarafındaki son savunmadır; sunucu uygulamaları
ayrıca kendi request-body limitlerini koymalıdır.

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

`providerStatus`, yalnız kod eşleşmesinin `known` veya `unknown` sonucudur.
`provider.status` ise kuruluşun güncel faaliyet statüsüne ilişkin ayrı veri
alanıdır. Açık statü kanıtı yoksa bu alan `unknown` kalır.

> Önce `parsed.isValid` alanını kontrol edin. Geçersiz bir IBAN içinde biçimsel
> olarak çıkarılabilen beş haneli kod veri kümesinde bulunabilir; bu durumda
> kuruluş eşleşmesi IBAN'ı geçerli hâle getirmez ve otomatik seçim yapılmamalıdır.

## `formatIban(input: string): string`

Normalize edilmiş değeri dörtlü gruplar halinde döndürür.

1.024 karakterden uzun girdiler için boş metin döndürür.

## `maskIban(input: string): string`

İlk ve son dört karakteri korur, orta alanı `*` ile maskeler. Ham IBAN'ı loglamak
yerine bu fonksiyonu kullanın.

1.024 karakterden uzun girdiler için boş metin döndürür. Bu durumda ham girdiyi
loglamayın; isteği uygulamanızın güvenli hata akışında reddedin.

## Doğrulama Sınırı

API hesabın varlığını, sahibini, ad eşleşmesini, bakiyeyi veya transfer
yapılabilirliğini doğrulamaz. `known` yalnız sağlayıcı kodu eşleşmesidir.

## Geriye Uyumluluk

`parseIban`, `validateTurkishIban`, `getBankCodeFromIban`, `findBankByCode`,
`identifyBankFromIban`, `formatIban` ve `maskIban` ile mevcut package export
yolları major release olmadan kaldırılmaz. Bir alan önce dokümantasyonda ve
CHANGELOG'da deprecated ilan edilir, migration yolu verilir ve en erken sonraki
major sürümde kaldırılır. v0.x alias'ları ilk 1.x major serisi boyunca korunacak
ve kaldırma planı ayrıca duyurulacaktır.
