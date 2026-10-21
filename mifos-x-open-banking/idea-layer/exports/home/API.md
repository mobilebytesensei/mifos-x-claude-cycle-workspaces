# API — Home

Client contracts for `home`. This project owns no backend: these are Ktorfit contracts against the
HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.

Three calls, in two stages: `accounts-list` on mount, then **balances and transactions in parallel**
(`coroutineScope` async/awaitAll) for the selected account.

---

## accounts-list

| | |
|---|---|
| Endpoint | `GET /accounts` |
| Permission | `ReadAccountsDetail` |
| Trigger | On mount — populates the account-switcher |

**Same resource as the Accounts screen, cached in memory** to avoid redundant round-trips when
navigating back and forth. Home and Accounts should not each issue their own fetch.

Empty `Data.Account[]` → `empty` state with `reason=no_accounts`.

| Code | Cause | Recovery |
|------|-------|----------|
| 401 | Access token expired | Clear token store → login |
| 403 | `ReadAccountsDetail` absent from consent | **Non-recoverable** — navigate to consent-list |
| 429 | Rate-limit exceeded | Exponential back-off + retry CTA |
| 503 | Sandbox unavailable | Retry CTA after a delay |

---

## selected-account-balances

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/balances` |
| Permission | `ReadBalances` |
| Fetched | In parallel with transactions |

**Balance preference:** `InterimAvailable → InterimBooked → OpeningBooked`.

Unlike the Accounts list, home surfaces **two** figures: the preferred type as the hero balance, and
the second-best type as the "available" label. Where booked and available differ, that difference is
exactly what a customer opens the app to see.

**Credit accounts invert the meaning of a balance.** `CreditCard` with
`CreditDebitIndicator=Debit` renders in the error colour — on a credit account the figure is money
owed, and showing it in the same treatment as a positive current-account balance would misread as
funds available.

**Multi-currency (`GlobalWallet`) displays the native currency code with no GBP conversion** —
converting would put a rate on screen the bank never quoted.

| Code | Cause | Recovery |
|------|-------|----------|
| 401 | Access token expired | Error state → login |
| 403 | `ReadBalances` not in consent | **Non-recoverable**; message directs the PSU to consent-list |
| 404 | `AccountId` stale — consent revoked mid-session | Clear selected account; reload `/accounts` |

---

## recent-transactions

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/transactions` |
| Permission | `ReadTransactionsDetail` |
| Fetched | In parallel with balances |

**Only the 5 most-recent Booked transactions**, sorted descending by `BookingDateTime`, sliced
client-side.

**Pending transactions are excluded here** — deliberately, and only here: they remain visible on the
full transactions screen. A pending amount has not moved yet, so listing it beside a balance invites
the customer to reconcile two numbers that are not meant to agree. The full list is the place where
pending status can be labelled and understood.

`View all` routes to the transactions screen, where the unsliced list lives.

Category icon derives from `ProprietaryBankTransactionCode.Code`, falling back to
`MerchantCategoryCode`.

| Code | Cause | Recovery |
|------|-------|----------|
| 401 | Access token expired | Error state → login |
| 403 | `ReadTransactionsDetail` not in consent | **Non-recoverable**; advisory shown in the recent-transactions section only |
| 429 | Rate-limit exceeded | Recoverable; retry CTA |

The 403 here degrades **within** the screen: the hero balance still renders and only the
transactions section carries the advisory. A consent can permit balances without permitting
transaction detail, and losing the whole dashboard to that would be wrong.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/home/api.yaml. -->
