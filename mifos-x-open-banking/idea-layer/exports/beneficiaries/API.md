# API — Beneficiaries

Client contract for `beneficiaries`. This project owns no backend: this is a Ktorfit contract
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `BeneficiariesRepository`.

---

## beneficiaries-list

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/beneficiaries` |
| Response DTO | `BeneficiaryItem` |
| Permission | **ReadBeneficiariesDetail** |

Returns the saved payees authorised under the PSU consent for the given account.

`AccountId` arrives via `SavedStateHandle` from the navigation argument, originally sourced from
`accounts-list`.

---

## Errors

| Type                  | Cause                                              | Recoverable by retry |
|-----------------------|----------------------------------------------------|----------------------|
| `TokenExpiredError`   | PSU access token expired                           | after re-auth        |
| `ConsentRevokedError` | Consent revoked, or lacks `ReadBeneficiariesDetail`| **no**               |
| `RateLimitedError`    | Bank throttling                                    | yes, after back-off  |
| `NetworkError`        | Offline / transport                                | yes                  |
| `ServerError`         | Bank-side failure                                  | yes                  |

### Why the error state offers two CTAs

`ConsentRevokedError` is the common case here, and it is **not** a transient fault. The payee list
requires `ReadBeneficiariesDetail` in the active account-access-consent; a consent that was granted
without it, or has since been revoked, will refuse this call identically on every attempt.

So the error state pairs `retry_button` (`RetryLoad`) with `view_consents_button`
(`onNavigateToConsents -> ConsentListRoute`). Retry covers the transport cases; View Consents is the
only route that resolves the permission case. Offering Retry alone would leave the customer looping
against a refusal they cannot clear from this screen.

---

## Search

Search is a **local filter** over the already-loaded rows — the `Search` action issues no request.
A filter that matches nothing renders `search_no_results` inside the loaded content, distinct from
`empty_beneficiaries` which means the account genuinely has no saved payees.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/beneficiaries/api.yaml. -->
