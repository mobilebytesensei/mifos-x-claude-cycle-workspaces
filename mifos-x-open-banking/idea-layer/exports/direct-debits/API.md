# API — Direct Debits

Client contract for `direct-debits`. This project owns no backend: this is a Ktorfit contract
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `DirectDebitsRepository`.

---

## direct-debits-list

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/direct-debits` |
| Response DTO | `DirectDebitsSummary` |
| Permission | **ReadDirectDebits** |

Returns the direct-debit mandates on the account.

**`ReadDirectDebits` must be declared in the AIS consent permissions list** at consent creation
(`POST /account-access-consents`). It cannot be added later to an existing consent — a consent
granted without it will refuse this call for its whole life, which is why the failure is modelled as
`ConsentRevoked` rather than something a retry could clear.

**Inactive mandates are included in the response.** The list renders them rather than filtering:
a cancelled direct debit still carries a reference and a last-collection record the customer may
need. The `active_count_chip` / `inactive_count_chip` pair exists to keep the mix legible instead of
hiding half of it.

**No pagination.** The OBIE AIS v4.0 direct-debits endpoint returns the full list in one response —
there is no cursor to follow and no page size to tune. Client code should not implement paging
against it.

---

## Errors

| Kind             | Cause                             | Recoverable by retry |
|------------------|-----------------------------------|----------------------|
| `TokenExpired`   | PSU token expired                 | after re-auth        |
| `ConsentRevoked` | Consent revoked, or `ReadDirectDebits` never granted | **no** |
| `RateLimited`    | Bank throttling                   | yes, after back-off  |
| `ServerError`    | Bank-side failure                 | yes                  |
| `NetworkError`   | Offline / transport               | yes                  |

### `U000` — unsupported, not an error

An OBIE `U000` refusal means the bank does not support direct debits for this account. It is not in
the table above because it is not recoverable and not a fault.

Source handles it: `directDebitsStore:234` calls `recordIfUnsupported` before rethrowing — the same
pattern as `standingOrdersStore:344` and `scheduledPaymentsStore:377`. It maps to
`DirectDebitsUiState.Unsupported` and renders `unsupported_direct_debits`, a separate component from
`empty_direct_debits`.

The distinction matters to the customer: `empty` says "you have no direct debits", `unsupported`
says "this bank will not tell us". Only one of those is a statement about their money.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/direct-debits/api.yaml. -->
