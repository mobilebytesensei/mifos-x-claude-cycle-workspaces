# API — Standing Orders

Client contract for `standing-orders`. This project owns no backend: this is a Ktorfit contract
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `StandingOrdersRepository`.

---

## standing-orders-list

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/standing-orders` |
| Response DTO | `StandingOrdersSummary` |
| Permission | **ReadStandingOrdersDetail** |
| Requires auth | yes |
| Path param | `AccountId: string` |

Returns all standing orders for the account.

### The detail scope is not optional

`ReadStandingOrdersDetail` is required. **`ReadStandingOrders` alone omits `NextPaymentAmount` and
`Reference`** — two fields the card renders. A consent granted at the narrower scope produces cards
missing their amount and reference rather than an outright failure, which is a quieter and more
confusing outcome than a refusal.

### Frequency is an ISO 20022 code

The `Frequency` field carries OBIE ISO 20022 values — for example `IntrvlMnthDay:01:01`, meaning
monthly on the 1st. The ViewModel maps these to `frequency_label`.

The raw code must never reach the UI. Mapping it is the substantive transform this feature performs,
alongside `status_variant` and the `hasFinalPayment` flag.

### Response headers

| Header                  | Purpose                                                     |
|-------------------------|-------------------------------------------------------------|
| `x-fapi-interaction-id` | Echoed request/response correlation UUID — **log it** for support triage |

This is the id a bank's support team will ask for when a call behaved unexpectedly. It is worth
capturing in logs even on success.

---

## Errors

| Status | OBIE code                | Cause                                              | VM error type   |
|--------|--------------------------|-----------------------------------------------------|-----------------|
| 401    | `UK.OBIE.Unauthorized`   | Access token expired or invalid — re-authenticate  | `TokenExpired`  |
| 403    | `UK.OBIE.Field.Missing`  | Consent lacks `ReadStandingOrdersDetail`           | `ConsentRevoked`|
| 429    | `UK.OBIE.RateLimit`      | Rate limit exceeded — honour the `Retry-After` header | `RateLimited`|
| 500    | —                        | Bank-side failure                                   | `ServerError`   |

The 429 carries a `Retry-After` header; back-off should honour it rather than applying a fixed
delay.

The `Retry` button is present in **every** error case — but note that a 403 will refuse identically
on retry until the consent is replaced, so it is the one case where retry cannot help.

### `U000` — unsupported, not an error

An OBIE `U000` refusal means the bank does not support standing orders for this account. Source
records it: `standingOrdersStore:344` calls `recordIfUnsupported` before rethrowing — the same
pattern as `directDebitsStore:234` and `scheduledPaymentsStore:377`.

It maps to `StandingOrdersUiState.Unsupported` and renders `unsupported_standing_orders`, distinct
from `empty_standing_orders`. The empty state offers a create CTA; the unsupported state does not,
because creating something the bank will not serve is not an option to present.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/standing-orders/api.yaml. -->
