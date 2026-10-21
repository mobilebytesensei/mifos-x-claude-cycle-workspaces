# /idea verify --rule RULE-DTO-REGISTRY-001
# Project: mifos-x-open-banking
# Run at: 2026-05-28T00:00:00Z
# DTOs scanned: 45
# Consumer api.yaml files scanned: 37 (6 screens exempt: about/settings/splash/licenses/privacy-policy/terms-of-service)

## Sub-check Results

| Check | Status | Count |
|-------|--------|-------|
| D1 schema complete | PASS | 0 violations |
| D2 refs resolve | PASS | 0 unresolved |
| D3 no collisions | PASS | — |
| D4 no shadow baseline | PASS | — |
| D5 pii_fields declared | FAIL | 12 violations |
| D6 origin matches | PASS | 0 drift |
| D7 INDEX.md accurate | PASS | — |

## D5 Violations — pii_fields[] missing

DTOs with `pii: true` fields but no `pii_fields[]` top-level declaration:

| DTO | pii fields missing from pii_fields[] |
|-----|--------------------------------------|
| Agent | phone_number |
| Card | bank_card_number, name_on_card |
| ChangePasswordRequest | current_password, new_password |
| Counterparty | name, other_account_routing_address |
| Customer | legal_name, mobile_phone_number, email, date_of_birth |
| CustomerMessage | from_person |
| KycDocument | number, date_of_birth |
| MandateDetail | counterparty_name |
| OidcToken | access_token, id_token, refresh_token |
| SepaTransactionRequest | to_iban, to_name |
| StandingOrder | to_iban, to_name |
| TransactionCounterparty | holder_name |

## Fix

Add `pii_fields:` block to each violating DTO, listing the field names that have `pii: true`.
Example:
```yaml
pii_fields:
  - phone_number
```

## Compliant DTOs (pii_fields present)

- UserProfile: email, display_name
- PasswordResetRequest: email
- PasswordResetConfirmRequest: token, new_password
- StandingOrderDetail: beneficiary_name, beneficiary_iban
- StandingOrderExecution: [] (no pii fields — correct)
- StandingOrderStatusResponse: [] (no pii fields — correct)

## RESULT: FAIL (12 violations — all D5)
