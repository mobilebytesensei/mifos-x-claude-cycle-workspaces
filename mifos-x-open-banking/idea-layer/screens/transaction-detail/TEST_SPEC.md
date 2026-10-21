# TEST SPEC — Transaction Detail

| Field      | Value                                   |
|------------|-----------------------------------------|
| Feature    | transaction-detail                      |
| Source     | `screens/transaction-detail/tests.yaml` |
| Scenarios  | 11                                      |
| Priorities | critical 1 · high 1 · not declared 9    |
| States     | content 5 · error 4 · loading 1 · empty 1 |
| Module     | `feature/transaction-detail`            |
| Fixtures   | 7 named (`transaction_debit`, `transaction_credit`, `transaction_pending`, `error_not_found`, `error_token_expired`, `error_consent_withdrawn`, `error_network`) |

---

## Coverage

Contiguous ids; all four declared states covered.

**Only 2 of 11 scenarios declare a `priority`** — TC-TXNDTL-010 (`critical`) and TC-TXNDTL-011
(`high`), the two most recently added. The other 9 declare none. Same shape as home, where only the
two appended scenarios carry the field.

This is the only screen in the corpus that declares a **named fixture per scenario**. That is a
better convention than the corpus norm of inlining fixture values into `given`, and it is what
lets the four error scenarios differ by fixture alone rather than by re-described preconditions.

---

## Four errors, an empty, and the distinction between them

This screen draws the sharpest error taxonomy in the project — and the pair that matters most is
TC-TXNDTL-004 and TC-TXNDTL-010, which describe **almost the same situation** and resolve
differently:

| | TC-TXNDTL-004 (`error`) | TC-TXNDTL-010 (`empty`) |
|---|---|---|
| Condition | id not present in the returned list | HTTP 200, id not in the result set |
| Renders | `error_state` + `error_outline` | `transaction_empty_state` + `receipt_long` |
| Title | "Could not load transaction" | "Transaction not found" |
| Retry | no | no |
| Go back | yes | yes |

Both assert the *other* component is not rendered, which is what keeps them from collapsing into
one. Whether they should remain two scenarios is a fair question — the customer-visible difference
is an icon and a title — but the distinction is deliberate and the mutual-exclusion assertions
enforce it.

The Retry/Go-back split across all four errors is cleaner than most screens here:

| Scenario | Condition | Retry | Go back |
|---|---|---|---|
| TC-TXNDTL-004 | not found in list | — | ✓ |
| TC-TXNDTL-006 | 401 token expired | ✓ | — |
| TC-TXNDTL-007 | 403 consent withdrawn | — | ✓ |
| TC-TXNDTL-011 | network unreachable | ✓ | — |

Exactly one exit per error, never both, never neither. Recoverable failures get Retry;
non-recoverable ones get the way out.

---

## TC-TXNDTL-001 — Full Tesco Stores debit transaction (Booked)

**State:** content · **Fixture:** `transaction_debit`

- **Given** Valid PSU access token; `transactionId=TX-20260626-0001` in the cached list for account 40051512345678
- **When** Screen mounts with that `transactionId` and `accountId=40051512345678`
- **Then**
  - Amount header shows "−£42.17" in `error` colour (`CreditDebitIndicator=Debit`)
  - Currency meta label shows "GBP" in `onSurfaceVariant`
  - Merchant name shows "Tesco Stores"
  - Status badge shows "Booked" with `primaryContainer`
  - Header divider visible
  - Detail card header shows "Details" in `titleSmall`
  - Booking date row shows "2026-06-26T11:22:00Z"
  - Value date row shows "2026-06-26T11:22:00Z"
  - Category row shows "Groceries"
  - MCC row shows "5411" (visible — `MerchantCategoryCode` present)
  - Balance after shows "£447.63"
  - Reference row shows "TESCO STORES 3476 LONDON" with a copy icon
  - Bank code row shows "DR · HSBC"

Booking and value date are asserted separately even though they are identical here — TC-TXNDTL-009
is the case where they diverge, and having both rows pinned on a settled transaction is what makes
that divergence visible rather than a rendering accident.

---

## TC-TXNDTL-002 — Credit transaction in primary colour; MCC row hidden when null

**State:** content · **Fixture:** `transaction_credit`

- **Given** `transactionId=TX-20260625-0001` (ACME LTD salary credit, `MerchantCategoryCode` null) for account 40051512345678
- **When** Screen mounts with that `transactionId`
- **Then**
  - Amount header shows "+£2400.00" in `primary` (`CreditDebitIndicator=Credit`)
  - Currency meta label shows "GBP"
  - Merchant name shows "ACME LTD"
  - Status badge shows "Booked"
  - Category row shows "Salary"
  - **MCC row is NOT visible** (`MerchantCategoryCode` is null)
  - Balance after shows "£2847.63"
  - Reference row shows "SALARY JUN ACME LTD" with a copy icon
  - Bank code row shows "CR · HSBC"

The hidden MCC row is the assertion 001 cannot make. A salary credit has no merchant category, and
rendering the row with a blank or "—" value would present an absent field as an empty one.

---

## TC-TXNDTL-003 — Loading state while the transaction resolves

**State:** loading

- **Given** Slow network; API call in flight
- **When** Screen mounts with any valid `transactionId`
- **Then**
  - Circular progress indicator visible
  - Amount header not rendered
  - Currency meta not rendered
  - Detail card not rendered
  - Error state not rendered

---

## TC-TXNDTL-004 — Error when the transaction is not in the list (non-recoverable)

**State:** error · **Fixture:** `error_not_found`

- **Given** `transactionId` not present in the returned `OBReadTransaction6` list
- **When** Screen mounts with an unknown `transactionId`
- **Then**
  - Error `empty_state` renders with `error_outline` icon
  - Title "Could not load transaction"
  - Body "Transaction not found. It may have been removed or the reference is invalid."
  - Retry button **NOT** visible (`error.recoverable=false`)
  - Go back button **IS** visible
  - Tapping Go back navigates to transactions

---

## TC-TXNDTL-005 — Back button navigates to transactions

**State:** content · **Fixture:** `transaction_debit`

- **Given** Transaction detail fully loaded
- **When** User taps the back button
- **Then** Navigates back to transactions, retaining `accountId` in the back-stack

---

## TC-TXNDTL-006 — 401 TokenExpired shows error with Retry (recoverable)

**State:** error · **Fixture:** `error_token_expired`

- **Given** PSU access token has expired; API returns 401
- **When** Screen mounts or retry is attempted
- **Then**
  - Error `empty_state` renders with `error_outline` icon
  - Body "Session expired. Please log in again."
  - Retry button **IS** visible (`error.recoverable=true`)
  - Go back button **NOT** visible
  - Tapping Retry re-triggers `transaction_detail_load`

---

## TC-TXNDTL-007 — 403 ConsentWithdrawn shows Go Back only (non-recoverable)

**State:** error · **Fixture:** `error_consent_withdrawn`

- **Given** PSU has revoked consent; API returns 403
- **When** Screen mounts
- **Then**
  - Body "Access to transactions has been withdrawn."
  - Retry button **NOT** visible (`error.recoverable=false`)
  - Go back button **IS** visible
  - Tapping Go back navigates to transactions

Consistent with its parent list (TC-TXN-004), which also hides Retry on 403 with the same body
text. The two screens agree, which is more than the corpus manages across features.

---

## TC-TXNDTL-008 — Copy reference writes TransactionInformation to the clipboard

**State:** content · **Fixture:** `transaction_debit`

- **Given** Transaction detail fully loaded; reference row visible with a copy icon
- **When** User taps the copy icon on the reference row
- **Then**
  - `copy_to_clipboard` fires with value "TESCO STORES 3476 LONDON"
  - System `ClipboardManager` receives the string
  - Snackbar confirmation appears

All three steps asserted, including the snackbar. A silent copy gives no feedback that anything
happened, and the customer taps again — which is harmless here, but the confirmation is the only
signal the action worked at all.

---

## TC-TXNDTL-009 — Pending transaction shows a secondaryContainer badge and a future ValueDateTime

**State:** content · **Fixture:** `transaction_pending`

- **Given** `transactionId=TX-20260629-0001` (Pret A Manger, Pending pre-auth)
- **When** Screen mounts with that `transactionId`
- **Then**
  - Status badge shows "Pending" with `secondaryContainer`
  - Amount header shows "−£6.45" in `error`
  - `ValueDateTime` differs from `BookingDateTime` (2026-06-30 vs 2026-06-29)
  - MCC row shows "5812"

`secondaryContainer` for pending against `primaryContainer` for booked. Both are container roles —
neither is `error` — which is the right read: a pending transaction is in progress, not failed.
This matches the semantic Trust Blue assigns `secondary` ("working, not done").

The date divergence is the substantive assertion. A card pre-authorisation books on one day and
settles on another, and a screen that renders one date for both hides the fact that the money has
not actually left yet.

---

## TC-TXNDTL-010 — Empty state when the id is absent from a successful response

**Priority:** critical · **State:** empty · **Fixture:** `transaction_debit`

- **Given** `OBReadTransaction6` fetch succeeds (HTTP 200) but the returned list contains no transaction matching the route-param `transactionId`
- **When** Screen mounts with a `transactionId` not present in the result set
- **Then**
  - `transaction_empty_state` renders (`state_binding: [empty]`)
  - `receipt_long` icon visible
  - Title "Transaction not found"
  - Body "This transaction is no longer available. It may have been removed or your consent has expired."
  - `transaction_empty_back_button` (outlined) visible
  - **No Retry button** — this is not an error state
  - **Error state `empty_state` component is NOT rendered**
  - Tapping Go back navigates to transactions

---

## TC-TXNDTL-011 — Network error shows a recoverable error state with Retry

**Priority:** high · **State:** error · **Fixture:** `error_network`

- **Given** Device offline or upstream network unreachable when the screen mounts
- **When** Screen mounts with any valid `transactionId` and **no cached list available**
- **Then**
  - `error_state` `empty_state` renders with `error_outline` icon
  - Body "No network connection. Please check your connection and retry."
  - Retry button **IS** visible (`error.recoverable=true`)
  - Go back button **NOT** visible
  - **Empty state component is NOT rendered**

"No cached list available" is the precondition that makes this distinct. With a cache the screen
would resolve from it and never reach an error state at all — this scenario is specifically the
cold-start offline case.

---

_Generated by /idea-feature-test-export | 2026-08-03_
