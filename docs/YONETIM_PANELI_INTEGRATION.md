# Yonetim-Paneli Entegrasyonu

`tr-iban`, Yonetim-Paneli deposuna kopyalanmayacak; sürümlenmiş dış NPM
bağımlılığı olarak kullanılacaktır.

## Personel Formu

```ts
import { formatIban, identifyBankFromIban } from "tr-iban";

const formatted = formatIban(inputValue);
const identified = identifyBankFromIban(formatted);

if (identified.parsed.isValid && identified.providerStatus === "known") {
  setSelectedBankCode(identified.provider!.code);
  setBankSelectionLocked(true);
} else {
  clearSelectedBank();
  setBankSelectionLocked(true);
}
```

- `known`: banka/kuruluş otomatik seçilir; kullanıcı farklı kuruluş seçemez.
- Geçersiz biçim/checksum: banka temizlenir, kayıt engellenir.
- `unknown`: banka temizlenir, manuel seçim açılmaz, kayıt engellenir ve veri
  sürümünün güncelliği incelenir.

Bu son madde panelin iş kuralıdır. Genel amaçlı paket `unknown` kodu checksum
geçerliliğinden ayrı raporlar.

## NestJS Backend

Frontend sonucu güvenlik sınırı değildir. Backend aynı kontrolü tekrarlar:

```ts
import { identifyBankFromIban, maskIban } from "tr-iban";

const identified = identifyBankFromIban(dto.iban);

if (!identified.parsed.isValid) {
  throw new BadRequestException("IBAN biçimi veya kontrol basamakları geçersiz.");
}

if (identified.providerStatus !== "known") {
  throw new UnprocessableEntityException("IBAN sağlayıcı kodu tanınmıyor.");
}

logger.info(
  {
    iban: maskIban(dto.iban),
    providerCode: identified.providerCode,
    dataVersion: identified.dataVersion,
  },
  "IBAN sağlayıcısı doğrulandı",
);
```

Veritabanına seçilen kuruluşun `code` değeri ve kullanılan `dataVersion`
yazılabilir. Ham IBAN uygulama loglarına, hata izleme etiketlerine veya analitik
olaylarına eklenmemelidir.

## NPM Olmayan Servisler

`data/tr-banks.sql` içindeki `tr_iban_providers` tablosu içe aktarılır veya hazır
`data/tr-banks.sqlite` veritabanı açılır ve beş haneli `code` alanıyla sorgulanır.
JSON, CSV, SQL ve SQLite aynı kayıtları taşır.
