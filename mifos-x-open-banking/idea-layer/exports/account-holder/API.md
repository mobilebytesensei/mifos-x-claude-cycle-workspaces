# API — Account Holder

Client contract for `account-holder`. This project owns no backend: this is a Ktorfit contract
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `ProfileRepository`.

---

## party

| | |
|---|---|
| Endpoint | `GET /accounts/{AccountId}/party` |
| Status | 200 |
| Schema | `PartyResponse` |
| Data path | `Data.Party` |
| Permission | **ReadParty** — a separate consent scope from balances/transactions |

Returns the single account holder linked to the account.

**Wire fields** (all optional except `PartyId`)

`PartyId: string` · `Name: string` · `FullLegalName: string` · `PartyType: string` ·
`EmailAddress: string` · `Phone: string` · `Mobile: string` · `Address: PartyAddress`

**Domain model — `PartyProfile`**

The mapper flattens the wire shape before it reaches the ViewModel:

| Field         | Derivation                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `partyId`     | `PartyId`                                                                   |
| `displayName` | `Party.resolveName()` — **blank routes the screen to `Empty`**              |
| `roleLabel`   | `Party.resolveRoleLabel()`                                                  |
| `initials`    | Derived from `displayName` via `toInitials()`                               |
| `email`       | `EmailAddress`                                                              |
| `mobile`      | `Party.resolveMobile()`                                                     |
| `addressLine` | `PartyAddress.toAddressLine()` — a single flattened string                   |

`addressLine` is deliberately one string: the source does **not** model an `OBPostalAddress8`
array, so there are no separate address lines to render and none should be invented.

---

## Error mapping

| Condition        | Maps to                                 | Retriable |
|------------------|------------------------------------------|-----------|
| `401`            | `AccountHolderErrorKind.TokenExpired`    | yes       |
| `403`            | `AccountHolderErrorKind.ConsentMissingParty` | **no — retry CTA suppressed** |
| `404`            | `AccountHolderErrorKind.ProfileNotFound` | **no**    |
| `200` + blank `displayName` | `AccountHolderUiState.Empty` via `emptyIfContent` | n/a |
| `500`            | `AccountHolderErrorKind.LoadFailed`      | yes       |
| network failure  | `AccountHolderErrorKind.LoadFailed` (from `ScreenState.NoNetwork`) | yes |

Two of these are worth calling out.

**403 suppresses the retry CTA.** The consent lacks `ReadParty` — retrying sends the identical
request and gets the identical refusal. Offering Retry would invite the customer to hammer a
permission they do not hold; the fix is a new consent, not another attempt.

**A 200 with a blank name is `Empty`, not an error.** The bank answered successfully and the party
simply carries no usable name, so the screen shows the empty view rather than a failure.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/account-holder/api.yaml. -->
