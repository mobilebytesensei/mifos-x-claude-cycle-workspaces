# API — Transaction Detail

Client contract for `transaction-detail`. This project owns no backend: this is a Ktorfit contract
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `TransactionDetailRepository`.

---

## There is no single-transaction endpoint

**OBIE v4.0 AIS provides none.** This is the single most important fact about the screen, and the
reason its data flow looks indirect.

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/transactions` |
| Permission | `ReadTransactionsDetail` |

The client resolves the transaction by **filtering the account's transaction list** by the
`transactionId` passed as a route param. If the list is already cached, it is reused; otherwise it is
fetched fresh.

### What follows from that

**`TransactionNotFoundError` is reachable, not defensive.** An id that no longer appears in the
list — because the window moved, a filter narrowed it, or a pending entry settled under a new id —
has nothing to render. That maps to the `empty` state, and it is why the empty state offers a way
back to the list rather than a retry.

**Freshness is inherited.** The screen is exactly as current as the list it reads. It cannot
independently refresh one transaction, so a stale list yields a stale detail view.

**Deep-linking is constrained.** Anything opening this screen must supply an `accountId` as well as
a `transactionId`, because the account is what actually gets fetched. Notifications and list rows
both pass the pair.

---

## Errors

| Type                       | Cause                              | Recoverable by retry |
|----------------------------|------------------------------------|----------------------|
| `TokenExpiredError`        | PSU token expired                  | after re-auth        |
| `ConsentWithdrawnError`    | Consent revoked or scope lost      | **no**               |
| `TransactionNotFoundError` | Id absent from the resolved list   | **no** — renders `empty` |
| `NetworkError`             | Offline / transport                | yes                  |

Two of the four cannot be fixed by retrying, which is why the error state pairs Retry with a Go Back
CTA. A screen whose only affordance is a retry that cannot succeed is a dead end.

---

## CopyReference

`CopyReference` copies the payment reference to the clipboard. It is a declared action rather than
an incidental long-press because the reference is the value customers most often need to quote — to
a merchant, a landlord, or their own bank — and it must be reliably copyable rather than
transcribed by eye.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/transaction-detail/api.yaml. -->
