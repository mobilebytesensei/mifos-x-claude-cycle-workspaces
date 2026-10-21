# API — Scheduled Payments

Client contract for `scheduled-payments`. This project owns no backend: this is a Ktorfit contract
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `ScheduledPaymentsRepository`.

---

## scheduled-payments-list

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/scheduled-payments` |
| Data path | `Data.ScheduledPayment` |

Returns **future-dated** scheduled payments for the given account. Past executions are not in
scope — this is a forward-looking list, which is why there is no date filter and no pagination.

**Fields**

| Wire field                   | Maps to                       |
|------------------------------|-------------------------------|
| `ScheduledPaymentDateTime`   | `scheduledDateLabel`          |
| `ScheduledType`              | `scheduledType` → type chip   |
| `Reference`                  | `reference`                   |
| `InstructedAmount.Amount`    | `amountLabel`                 |
| `InstructedAmount.Currency`  | `amountLabel`                 |
| `CreditorAccount.Name`       | `payeeName`                   |
| `CreditorAccount.Identification` | `creditorIdentification`  |

### `ScheduledType` — the distinction that matters

| Value       | Meaning                                          |
|-------------|--------------------------------------------------|
| `Execution` | The payment **leaves the account** on that date  |
| `Arrival`   | The funds **arrive at the beneficiary** on that date |

These are different promises, and the difference is material to a customer planning around a
balance. It is surfaced as a per-row chip rather than folded into the date label.

---

## Errors

| Code          | Type            | Recovery      |
|---------------|-----------------|---------------|
| 401           | `TokenExpired`  | `show_retry`  |
| 403           | `ConsentRevoked`| `show_retry`  |
| 429           | `RateLimited`   | `show_retry`  |
| `IOException` | `NetworkError`  | `show_retry`  |

All four resolve to the `error` state with a retry CTA.

### `U000` — unsupported, not an error

An OBIE `U000` refusal means the bank does not support scheduled payments for this account. It is
**not** in the error table above because it is not a failure to recover from — retrying will get
the same refusal for as long as the consent and account remain the same.

Source already handles it: `BankingStores.kt:377` (`scheduledPaymentsStore`) calls
`result.error.recordIfUnsupported(endpoint = AccountEndpoint.ScheduledPayments)` before rethrowing —
the same pattern as `directDebitsStore:234` and `standingOrdersStore:344`.

It maps to `ScheduledPaymentsUiState.Unsupported` and renders
`unsupported_scheduled_payments`, which is a separate component from `empty_scheduled_payments`.
Conflating them would tell the customer they have nothing scheduled when in fact the bank simply
will not say.

**Implementation status:** the store-side detection ships; the UI branch that lands `Unsupported`
is owed by `/implement`. The state is declared spec-ahead-of-source on purpose — see the SPEC's
States section.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/scheduled-payments/api.yaml. -->
