# Veri güncelleme politikası

Resmî bir sayfanın değişmesi, projenin veriyi otomatik kabul ettiği anlamına gelmez. Kaynak değişikliği önce tespit edilir, üretilen veri farkı incelenir ve yalnız doğrulanmış değişiklik bir pull request ile yayımlanır.

## Otomatik kaynak kontrolü

GitHub Actions ayda bir canlı TCMB kaynaklarının SHA-256 dijital parmak izlerini `data/source-manifest.json` ile karşılaştırır. Yayın kontrol listesi aynı komutu her sürüm öncesinde yeniden çalıştırır.

- Değerler aynıysa kaynak kontrolü geçer
- Bir değer değiştiyse kontrol başarısız olur
- Başarısız kontrol veri dosyalarını otomatik güncellemez
- Maintainer resmî kaynağı ve üretilen farkı incelemeden yeni sürüm hazırlanmaz

## Güncelleme adımları

Bakım yapan kişi şu komutları sırayla çalıştırır:

```bash
npm run data:check-remote
npm run data:update
npm test
```

Komutların ardından şu kontroller yapılır:

1. Canlı resmî kaynaklar ile kayıtlı dijital parmak izleri karşılaştırılır
2. JSON, CSV, SQL, TypeScript verisi ve sentetik fixture'lar birlikte üretilir
3. Eklenen, silinen, yeniden adlandırılan ve türü değişen kayıtlar incelenir
4. Lisans listesine eklenen fakat katılımcı listesinde bulunmayan kodların eşleştirme kümesine girmediği doğrulanır
5. Şema, SQLite, gizlilik, TypeScript ve araç testleri çalıştırılır
6. PR açıklamasına resmî kaynak adresi, kontrol tarihi ve değişiklik gerekçesi yazılır
7. Zorunlu CI kontrolleri geçtikten sonra değişiklik birleştirilir

## Değişmemesi gereken kurallar

Her veri güncellemesi şu sözleşmeleri korur:

- `rawCode` resmî katılımcı kaynağındaki değeri değiştirmeden saklar
- `code` yalnız ödeme sistemleri katılımcı kodunun soldan `0` ile beş haneye tamamlanmış halidir
- Aktif lisans listeleri yeni bir IBAN kuruluş kodu üretmez
- JSON, CSV ve SQL aynı kuruluşları aynı sırada içerir
- Her kayıtta `payment_system_participant` kod kanıtı bulunur
- Test IBAN'larının tamamı sentetiktir
- Gerçek IBAN veya kişisel finansal veri repoya girmez

## Silinen veya çelişen kayıtlar

Bir kuruluş resmî katılımcı listesinden kaybolursa kayıt sessizce silinmez. Maintainer önceki veri sürümüyle farkı inceler ve gerekçeyi PR ile CHANGELOG içinde açıklar.

Kaynaklar birbiriyle çelişirse belirli konu için daha özel ve güncel TCMB kaynağı tercih edilir. Katılımcı kodu için Ödeme Sistemleri Katılımcıları listesi, IBAN biçimi için IBAN Hakkında Tebliğ esas alınır.

## Gizlilik sınırı

Veri doğrulamak için gerçek IBAN, müşteri adı, telefon numarası, hesap sahibi veya banka dekontu kullanılamaz. Üretici yalnızca sentetik fixture oluşturur; gizlilik taraması repodaki IBAN benzeri değerleri izin verilen sentetik listeyle karşılaştırır.
