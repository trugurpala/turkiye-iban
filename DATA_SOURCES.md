# Veri kaynakları

Bu proje, Türkiye IBAN kuruluş kodlarını yalnızca resmî Türkiye Cumhuriyet Merkez Bankası (TCMB) kaynaklarından hazırlar. Her kayıtta kaynak adresi, erişim tarihi ve kodun hangi kanıta dayandığı bulunur.

![TCMB kaynaklarından açık veri çıktılarına uzanan doğrulanabilir üretim akışı](docs/assets/github/data-provenance.png)

## Kaynakların farklı görevleri

Bir kuruluşun aktif olması ile belirli bir IBAN kuruluş koduna sahip olması aynı bilgi değildir. Bu nedenle her kaynak yalnız kanıtladığı amaç için kullanılır:

| Kaynak | Projedeki görevi |
| --- | --- |
| [TCMB Ödeme Sistemleri Katılımcıları](https://www.tcmb.gov.tr/wps/wcm/connect/9fa62a85-5b6d-46c5-9b01-eb461d43723d/TCMB%2B%C3%96deme%2BSistemleri%2BKat%C4%B1l%C4%B1mc%C4%B1lar%C4%B1%2B%282025%29.pdf?MOD=AJPERES) | Kuruluş eşleştirmesine girecek katılımcı kodlarının birincil kanıtı |
| [TCMB aktif ödeme kuruluşları](https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb%2Btr/main%2Bmenu/temel%2Bfaaliyetler/odeme%2Bhizmetleri/odeme%2Bkuruluslari) | Mevcut katılımcı kayıtlarının tür ve statü bilgisi |
| [TCMB aktif elektronik para kuruluşları](https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb%2Btr/main%2Bmenu/temel%2Bfaaliyetler/odeme%2Bhizmetleri/elektronik%2Bpara%2Bkuruluslari) | Mevcut katılımcı kayıtlarının tür ve statü bilgisi |
| [TCMB IBAN Hakkında Tebliğ](https://www.tcmb.gov.tr/wps/wcm/connect/c8357e06-1ab6-4c49-8352-7b9c19fcb77e/Teblig%2B2021_5.pdf?MOD=AJPERES) | Türkiye IBAN yapısı ve doğrulama kuralları |

## Kod nasıl dönüştürülür?

Ödeme Sistemleri Katılımcıları PDF'indeki `rawCode` dört hanelidir. Türkiye IBAN'ındaki kuruluş alanı beş haneli olduğu için değer soldan `0` ile tamamlanır:

| Resmî katılımcı kodu | IBAN kuruluş alanı |
| --- | --- |
| `0046` | `00046` |
| `0010` | `00010` |

Bu dönüşüm yalnızca ödeme sistemleri katılımcı kodlarına uygulanır. Aktif ödeme veya elektronik para kuruluşu sayfasındaki bir lisans kodu, bu yöntemle otomatik olarak IBAN kuruluş koduna çevrilmez.

## Her kayıtta hangi kanıt bulunur?

`data/tr-banks.json` içindeki kuruluş kayıtları şu izlenebilir alanları taşır:

- `codeEvidence`: kodun ödeme sistemleri katılımcı listesinden geldiğini belirtir
- `sources`: kullanılan resmî kaynak kimliklerini ve adreslerini içerir
- `lastVerifiedAt`: kaydın en son kontrol edildiği tarihi gösterir
- `rawCode`: resmî listede yayımlanan kodu değiştirmeden saklar
- `code`: Türkiye IBAN alanında kullanılan beş haneli değeri içerir

İndirilen üç kuruluş kaynağının SHA-256 dijital parmak izleri `data/source-manifest.json` içinde tutulur. Bu değerler kaynak içeriğinin son kontrolden sonra değişip değişmediğini anlamak için kullanılır.

## Hangi kaynaklar kabul edilmez?

Blog, forum mesajı, müşteri kaydı, banka ekran görüntüsü, gerçek IBAN veya kişisel finansal veri kuruluş kodu kaynağı olarak kabul edilmez. Bir veri değişikliği PR'ı, resmî kaynak adresini ve kontrol tarihini göstermelidir.

Schwifty, MIT lisanslı karşılaştırma veya test referansı olabilir. Veri üreticisinin ana kaynağı olamaz.

Kaynak kopyaları 2026-07-31 tarihinde alınmış ve dijital parmak izleri kaynak manifestine kaydedilmiştir. Güncelleme kararı için [veri güncelleme politikasını](DATA_UPDATE_POLICY.md) okuyun.
