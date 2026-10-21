# API — Accounts

Client contracts for `accounts`. This project owns no backend: these are Ktorfit contracts against
the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `AccountsOverviewRepository`.

---

## accounts-list

| | |
|---|---|
| Endpoint | `GET /accounts` |
| Response DTO | `BankAccount` (path `Data.Account[]`) |
| Permission | **ReadAccountsDetail** |
| Requires auth | yes |
| Network policy | `cellular_allowed` |

Returns every account the PSU authorised. **Always the first resource call after consent** — the
whole account journey is keyed off the `AccountId`s it returns.

An empty `Data.Account[]` is a successful response and renders `empty_accounts`, not an error: the
consent was granted, it simply covers no accounts.

**Errors**

| Code | Cause | Recovery |
|------|-------|----------|
| 401 | Access token expired or invalid | Clear token store → navigate to login |
| 403 | Consent rejected/revoked, or `ReadAccountsDetail` absent | Navigate to consent-list for re-authorisation |
| 429 | HSBC rate-limit exceeded (OBIE mandates a 500-calls/5-min PSU limit) | Exponential back-off + retry CTA |
| 503 | HSBC sandbox unavailable | Retry CTA after a brief delay |

The 429 recovery is back-off *before* the CTA, not a bare retry button — an immediate retry against
a PSU rate limit makes the situation worse.

---

## balances

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/balances` |
| Response DTO | `AccountBalance` (path `Data.Balance[]`) |
| Permission | **ReadBalances** |
| Requires auth | yes |
| Network policy | `cellular_allowed` |
| Path param | `AccountId` — `OBAccount6.AccountId`, from `accounts-list` |

**Called once per account**, fanned out in parallel via `coroutineScope` async/awaitAll. This is
why a card can render before its balance arrives, and why one account's balance failure does not
take down the list.

### Balance type preference

OBIE returns several balance types per account. This screen must show one figure per card, so it
takes the first available in order:

`InterimAvailable → InterimBooked → OpeningBooked`

Available is preferred over booked because it is the figure a customer can actually spend.
(`account-detail` makes the opposite choice and lists *all* types — one account in depth warrants
the distinction; a list does not.)

### Multi-currency accounts

`GlobalWallet` accounts return a **native-currency** balance. Display as-is — **no GBP conversion**.
Converting would invent a rate the bank did not quote and put a number on screen the customer
cannot reconcile against their statement.

**Errors — all degrade per-account, none is fatal to the list**

| Code | Cause | Recovery |
|------|-------|----------|
| 401 | Access token expired | Mark all accounts `balance_unavailable`; surface session-expired error |
| 403 | `ReadBalances` not granted in consent | Show the account card **without** a balance row; surface an advisory chip |
| 404 | `AccountId` not found — stale reference (consent revoked mid-session) | Remove the stale card; snackbar advisory |

The 403 path is the important one: a consent can authorise accounts without authorising balances.
The cards still render with identity and type; only the balance column is withheld. Treating that
as a load failure would hide accounts the customer is entitled to see.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/accounts/api.yaml. -->
