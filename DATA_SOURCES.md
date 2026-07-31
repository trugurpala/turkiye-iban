# Veri Kaynakları

Kanonik kaynak kataloğu `data/source/institutions.json` içindedir. Her kaynak;
yayıncı, başlık, doğrudan URL, erişim tarihi, SHA-256, sınıflandırma, kullanım
amacı, kanıt kapsamı, çıkarma yöntemi ve bilinen yeniden dağıtım yaklaşımıyla
kaydedilir.

## Kullanılan ve İzlenen Kaynaklar

| Kaynak | Sınıf | Kullanım | Erişim | Güven düzeyi |
| --- | --- | --- | --- | --- |
| [TCMB Ödeme Sistemleri Katılımcıları (2025)](https://www.tcmb.gov.tr/wps/wcm/connect/9fa62a85-5b6d-46c5-9b01-eb461d43723d/TCMB%2B%C3%96deme%2BSistemleri%2BKat%C4%B1l%C4%B1mc%C4%B1lar%C4%B1%2B%282025%29.pdf?MOD=AJPERES) | `official` | `primary_code_evidence` | 2026-07-31 | Kuruluş kodunun birincil kanıtı |
| [TCMB Aktif Ödeme Kuruluşları](https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb%2Btr/main%2Bmenu/temel%2Bfaaliyetler/odeme%2Bhizmetleri/odeme%2Bkuruluslari) | `official` | `monitor_only` | 2026-07-31 | Lisans/statü izleme; mevcut snapshotta kayıt üretmiyor |
| [TCMB Aktif Elektronik Para Kuruluşları](https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb%2Btr/main%2Bmenu/temel%2Bfaaliyetler/odeme%2Bhizmetleri/elektronik%2Bpara%2Bkuruluslari) | `official` | `monitor_only` | 2026-07-31 | Lisans/statü izleme; mevcut snapshotta kayıt üretmiyor |
| [TCMB IBAN Hakkında Tebliğ](https://www.tcmb.gov.tr/wps/wcm/connect/c8357e06-1ab6-4c49-8352-7b9c19fcb77e/Teblig%2B2021_5.pdf?MOD=AJPERES) | resmî düzenleme | IBAN biçimi | belge referansı | Veri kataloğundan ayrı biçim kanıtı |

Aktif lisans sicilinde bulunmak, tek başına belirli bir IBAN kuruluş koduna
sahip olunduğunu kanıtlamaz. Bu nedenle monitor-only kaynaklardaki kodlar
katılımcı kanıtı olmadan lookup veri kümesine eklenmez.

## Çıkarma ve Doğrulama

Katılımcı PDF'i metin tablosu olarak ayrıştırılır. Dört haneli `rawCode`, Türkiye
IBAN alanındaki beş haneye yalnız soldan `0` eklenerek dönüştürülür. HTML lisans
sayfaları hash düzeyinde izlenir. Parser çıktısı canonical dosyaya otomatik
yazılmaz; eklenen, silinen ve değişen kayıt raporu maintainer incelemesi ister.

PDF veya HTML biçiminin değişmesi parser'ı bozabilir. Böyle bir hata veri
değişikliği olarak kabul edilmez ve otomatik release yapılmaz. Kaynağın resmî
olması, ayrıştırıcının her zaman doğru olduğu anlamına gelmez.

## Güncellik

GitHub Actions kaynakları ayda bir kontrol eder. Maintainer ayrıca her veri
release'i öncesinde kontrolü çalıştırır. `retrievedAt` kaynağın indirildiği,
`lastVerifiedAt` ise ilgili kayıt ilişkisinin insan tarafından gözden geçirildiği
tarihtir. Güncelleme adımları `DATA_UPDATE_POLICY.md` içindedir.

## Lisans ve Yeniden Dağıtım

Proje TCMB sayfa veya PDF dosyalarını release asset olarak yeniden dağıtmaz;
kuruluş kodu, ad ve kanıt ilişkisi gibi çıkarılmış olgusal alanları ve kaynak
atıflarını yayımlar. Kod ve proje belgeleri MIT lisanslıdır. Resmî kaynakların
kendi kullanım koşulları ilgili yayıncıya aittir; bu proje TCMB tarafından
onaylanmış veya desteklenmiş değildir.

Schwifty yalnız MIT lisanslı karşılaştırma/test oracle'ı olabilir. Birincil veri
kaynağı değildir. Blog, forum, gerçek IBAN, müşteri kaydı ve banka ekranı veri
kanıtı olarak kabul edilmez.
