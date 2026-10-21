# API — Account Detail

Client contracts for `account-detail`. This project owns no backend: these are Ktorfit contracts
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `AccountDetailRepository`.

Both calls are account-scoped and take `AccountId` — supplied by `SavedStateHandle` from the
navigation argument, originally sourced from `accounts-list`.

---

## account-detail

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}` |
| Response DTO | `AccountDetail` |
| Permission | **ReadAccountsDetail** |
| Requires auth | yes |
| Path params | `AccountId: string` |

Returns single-account metadata: subtype, identification, currency, servicer.

These populate the header card — `AccountSubType`, `Nickname`, `Account.Identification`,
`Currency`, `Servicer.Identification` and `Description`.

Note the permission is the **detail** scope. `ReadAccountsBasic` would return the account without
the identification and servicer fields the header renders, so a consent granted at basic scope
leaves this screen underpopulated rather than failing outright.

---

## balances

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/balances` |
| Response DTO | `AccountBalanceLine` |
| Permission | **ReadBalances** |
| Requires auth | yes |
| Path params | `AccountId: string` |

Returns **all** balance types for the account — `InterimAvailable`, `InterimBooked`,
`OpeningBooked` and others.

This screen renders every type as its own `balance_row`, rather than selecting one. That is a
deliberate difference from the `accounts` list, which must pick a single figure per card and
applies a preference order (`InterimAvailable → InterimBooked → OpeningBooked`). Here the customer
is looking at one account in depth, so the distinction between available and booked is information
worth showing rather than collapsing.

An account that returns no balances renders `balances_empty_state` **within** the loaded screen —
the balances section is empty, the screen is not.

---

## Permissions summary

| Endpoint       | Permission           | If absent                                              |
|----------------|----------------------|--------------------------------------------------------|
| account-detail | `ReadAccountsDetail` | Header fields unavailable                              |
| balances       | `ReadBalances`       | Balances section cannot populate                       |

Both are distinct from `ReadParty`, which gates the `chip_party` destination (`account-holder`) —
a consent can satisfy this screen fully and still refuse the account holder.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/account-detail/api.yaml. -->
