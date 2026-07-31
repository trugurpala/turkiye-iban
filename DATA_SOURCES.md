# Data Sources

Bu proje resmî ve kurumsal kaynakları önceliklendirir. Üretilen dosyadaki her
kayıt kaynak kimliği, URL, erişim tarihi ve kod kanıtını taşır; indirilen kaynak
içeriğinin SHA-256 özeti `data/source-manifest.json` içinde tutulur.

## Birincil Kod Kaynağı

- [TCMB Ödeme Sistemleri Katılımcıları](https://www.tcmb.gov.tr/wps/wcm/connect/9fa62a85-5b6d-46c5-9b01-eb461d43723d/TCMB%2B%C3%96deme%2BSistemleri%2BKat%C4%B1l%C4%B1mc%C4%B1lar%C4%B1%2B%282025%29.pdf?MOD=AJPERES)

Bu listedeki dört haneli katılımcı kodu, Türkiye IBAN'ındaki beş haneli alana sol
taraftan sıfır eklenerek yazılır. `codeEvidence: payment_system_participant`
yalnız bu kaynaktan üretilir.

## Statü ve Tür Kaynakları

- [TCMB aktif ödeme kuruluşları](https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb%2Btr/main%2Bmenu/temel%2Bfaaliyetler/odeme%2Bhizmetleri/odeme%2Bkuruluslari)
- [TCMB aktif elektronik para kuruluşları](https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb%2Btr/main%2Bmenu/temel%2Bfaaliyetler/odeme%2Bhizmetleri/elektronik%2Bpara%2Bkuruluslari)

Bu listeler yalnız ödeme sistemleri katılımcı kümesinde zaten bulunan bir kaydı
tür/statü ve kaynak bilgisiyle zenginleştirir. Aktif lisans kaydı veya sayfadaki
kuruluş kodu tek başına IBAN düzenleme yetkisinin ya da belirli bir IBAN
sağlayıcı kodunun kanıtı değildir.

## IBAN Düzenlemesi

- [TCMB Uluslararası Banka Hesap Numarası Hakkında Tebliğ](https://www.tcmb.gov.tr/wps/wcm/connect/c8357e06-1ab6-4c49-8352-7b9c19fcb77e/Teblig%2B2021_5.pdf?MOD=AJPERES)

Tebliğ biçim/doğrulama politikasının ana kaynağıdır; kuruluş dizini olarak
kullanılmaz.

Kaynaklar 2026-07-31 tarihinde çekilmiş ve hash manifestine kaydedilmiştir.

## İkincil Kaynaklar

Schwifty MIT lisanslı referans veya test oracle'ı olarak karşılaştırmada
kullanılabilir. Veri üreticisinin ana kaynağı olamaz. Blog, forum, müşteri
kaydı, banka ekran görüntüsü veya gerçek IBAN veri kaynağı olarak kabul edilmez.
