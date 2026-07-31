# Data Sources

This project uses official and institutional sources first. If two sources
conflict, the most specific current TCMB source wins unless maintainers document
a different reason in the changelog.

## Primary Sources

- TCMB payment systems participants list:
  `https://www.tcmb.gov.tr/wps/wcm/connect/9fa62a85-5b6d-46c5-9b01-eb461d43723d/TCMB%2B%C3%96deme%2BSistemleri%2BKat%C4%B1l%C4%B1mc%C4%B1lar%C4%B1%2B%282025%29.pdf?MOD=AJPERES`
- TCMB active payment institutions list:
  `https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb%2Btr/main%2Bmenu/temel%2Bfaaliyetler/odeme%2Bhizmetleri/odeme%2Bkuruluslari`
- TCMB active electronic money institutions list:
  `https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb%2Btr/main%2Bmenu/temel%2Bfaaliyetler/odeme%2Bhizmetleri/elektronik%2Bpara%2Bkuruluslari`
- TCMB IBAN regulation:
  `https://tcmb.gov.tr/wps/wcm/connect/c8357e06-1ab6-4c49-8352-7b9c19fcb77e/Teblig%2B2021_5.pdf?MOD=AJPERES`

These sources were checked for the starter repository on 2026-07-31.

## Secondary Sources

Secondary sources may be used only for cross-checking, tests, or issue triage.
They must not replace official source data.

- Schwifty, MIT licensed, may be used as a reference or test oracle.

## Source Rules

- Every generated data record must keep at least one source identifier.
- Data updates must include the retrieval date.
- Real customer data is never an acceptable source.
- Screenshots from online banking or payroll systems are never acceptable.
