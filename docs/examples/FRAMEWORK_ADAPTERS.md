# Framework Adapter Örnekleri

Bu belge, paketi framework'e bağlayan küçük uygulama katmanını gösterir.
Framework pakete runtime bağımlılığı değildir; örneklerdeki IBAN değerleri
yalnızca sentetik fixture'lardır.

## Ortak karar

Her framework'te backend şu sırayı izlemelidir:

1. `identifyBankFromIban` ile biçim ve kontrol basamaklarını doğrula.
2. `providerStatus === "known"` ve `provider !== null` değilse otomatik kuruluş
   seçme.
3. Loglarda yalnız `maskIban` kullan.
4. `dataVersion` değerini kayıtla; hesap varlığı veya transfer yapılabilirliği
   iddiasında bulunma.

## Laravel

```php
use Illuminate\Validation\ValidationException;

use function identify_bank_from_iban;
use function mask_iban;

function resolvePayrollIban(string $iban): array
{
    $identified = identify_bank_from_iban($iban);

    if (!$identified['parsed']['isValid']) {
        throw ValidationException::withMessages(['iban' => 'IBAN biçimi geçersiz.']);
    }

    if ($identified['providerStatus'] !== 'known' || $identified['provider'] === null) {
        throw ValidationException::withMessages(['iban' => 'Kuruluş kodu tanınmıyor.']);
    }

    logger()->info('IBAN kuruluşu eşleştirildi', [
        'iban' => mask_iban($iban),
        'providerCode' => $identified['providerCode'],
        'dataVersion' => $identified['dataVersion'],
    ]);

    return $identified;
}
```

## Symfony

```php
use Symfony\Component\HttpKernel\Exception\UnprocessableEntityHttpException;

use function identify_bank_from_iban;

function identifyForEmployeeForm(string $iban): array
{
    $result = identify_bank_from_iban($iban);

    if (!$result['parsed']['isValid'] || $result['providerStatus'] !== 'known') {
        throw new UnprocessableEntityHttpException('IBAN veya kuruluş kodu geçersiz.');
    }

    return [
        'providerCode' => $result['provider']['code'],
        'providerName' => $result['provider']['nameOfficial'],
        'dataVersion' => $result['dataVersion'],
    ];
}
```

## FastAPI

```python
from turkiye_iban import identify_bank_from_iban, mask_iban


def resolve_employee_iban(iban: str) -> dict[str, str]:
    result = identify_bank_from_iban(iban)
    if not result["parsed"]["is_valid"]:
        raise ValueError("IBAN biçimi veya kontrol basamakları geçersiz.")
    if result["provider_status"] != "known" or result["provider"] is None:
        raise ValueError("Kuruluş kodu tanınmıyor.")
    return {
        "iban": result["parsed"]["normalized"],
        "provider_code": str(result["provider_code"]),
        "provider_name": str(result["provider"]["nameOfficial"]),
        "data_version": str(result["data_version"]),
        "masked_for_log": mask_iban(iban),
    }
```

## Django

```python
from django import forms
from turkiye_iban import identify_bank_from_iban


class EmployeeIbanForm(forms.Form):
    iban = forms.CharField()

    def clean_iban(self) -> str:
        value = self.cleaned_data["iban"]
        result = identify_bank_from_iban(value)
        if not result["parsed"]["is_valid"]:
            raise forms.ValidationError("IBAN biçimi geçersiz.")
        if result["provider_status"] != "known":
            raise forms.ValidationError("Kuruluş kodu tanınmıyor.")
        self.cleaned_data["provider"] = result["provider"]
        self.cleaned_data["data_version"] = result["data_version"]
        return value
```

## Ne test edilmelidir?

- Bilinen sentetik fixture: kuruluş otomatik seçilir.
- Unknown sentetik fixture: kuruluş otomatik seçilmez.
- Hatalı checksum: kayıt reddedilir.
- Log çıktısı: ham IBAN yerine maskeli değer kullanılır.
