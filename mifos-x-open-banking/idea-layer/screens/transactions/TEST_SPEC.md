# TEST SPEC — Transactions

| Field      | Value                              |
|------------|------------------------------------|
| Feature    | transactions                       |
| Source     | `screens/transactions/tests.yaml`  |
| Scenarios  | 12                                 |
| Priorities | **none declared** (see note)       |
| States     | content 8 · error 2 · loading 1 · empty 1 |
| Module     | `feature/transactions`             |

---

## Coverage

Contiguous ids; all five declared states covered — `content`, `loading`, `empty`, `error`, and the
`searching` behaviour exercised inside `content` (TC-TXN-008) rather than as its own state row.

**No scenario on this screen declares a `priority`** — 12 of the project's 41 priority-less
scenarios, the largest concentration after accounts. Surfaced rather than defaulted.

---

## Pagination is the part that is easy to get wrong (TC-TXN-011 / TC-TXN-012)

Transactions is the only paginated list in the corpus, and the two pagination scenarios cover
opposite halves of the same cursor:

- **011** walks the cursor forward: `Links.Next` present → Load more appends 5 rows → second
  response has no `Links.Next` → button disappears. Ten plus five equals fifteen, asserted
  explicitly, so an implementation that *replaces* rather than appends fails on the count.
- **012** resets it: applying a date filter must null the previous `next_link` **before** the new
  fetch.

012's reset assertion is the one that catches a real defect class. A stale cursor survives a filter
change and pages the *unfiltered* result set into a filtered list, producing rows that visibly
contradict the active date range. This is one of the five Store5 anti-patterns
(`pagination-race`) that RULE-IMPLEMENT-STORE5-001 exists to catch, asserted here at the spec level.

The ISO-8601 bounds are also pinned to the second — `fromBookingDateTime=2026-06-01T00:00:00Z`,
`toBookingDateTime=2026-06-28T23:59:59Z`. A `to` bound at midnight rather than end-of-day silently
drops the final day's transactions, which looks like missing data rather than an off-by-one.

---

## TC-TXN-001 — List loads and renders 10 transactions grouped by date

**State:** content

- **Given** Valid PSU access token; HSBC sandbox returns 10 transactions for account 40051512345678 across booking dates 2026-06-23 to 2026-06-28
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - Circular progress indicator replaced by the transaction list
  - Transactions grouped by `BookingDateTime` date (5 date-group headers visible)
  - Each row shows `TransactionInformation`, Category chip, and signed amount with currency symbol
  - Credit amounts in `primary`; debit amounts in `error`
  - Period summary strip shows `totalCredit=£2,400.00` and `totalDebit=£1,394.04`

Five date headers over ten transactions is the assertion that proves grouping actually groups —
ten headers would mean one per row, one header would mean none of it worked.

---

## TC-TXN-002 — Loading state while the fetch is in flight

**State:** loading

- **Given** Slow network; API call in flight
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - Circular progress indicator visible and centred
  - Transaction list, filter chips, search field, and summary strip not rendered

All four controls hidden, not just the list. Filter chips over an empty list invite a customer to
filter nothing and conclude the filter is broken.

---

## TC-TXN-003 — Error with Retry on 401 token expired

**State:** error

- **Given** Access token expired; `GET /accounts/{AccountId}/transactions` returns HTTP 401
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - Error state renders with `error_outline` icon and "Could not load transactions" title
  - Body reads "Session expired. Please log in again."
  - Retry button visible (`error.recoverable=true`)
  - Tapping Retry re-triggers `transactions_load`

---

## TC-TXN-004 — Error without Retry on 403 consent withdrawn

**State:** error

- **Given** PSU consent withdrawn; endpoint returns HTTP 403
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - Error state renders with body "Access to transactions has been withdrawn."
  - Retry button **NOT** visible (`error.recoverable=false`)

This screen sits on the *hide-Retry* side of the corpus-wide 403 split, with direct-debits and home
— and against statements, standing-orders, scheduled-payments and product, which show it. Both
transactions and statements are reached from the same account-detail chip row.

---

## TC-TXN-005 — Empty state when no transactions match the active filter

**State:** empty

- **Given** User activates the "Money in" filter; account 40051512345678 has zero Credit transactions in the current date range
- **When** User taps the "Money in" chip
- **Then**
  - Empty state renders with `receipt_long` icon
  - Title "No transactions found"
  - Body "Try adjusting your filters or date range."
  - "Clear filters" button visible
  - Tapping "Clear filters" resets the filter to all and transitions to content

Note this is a **filtered** empty, and the body says so — it points at the filter, not at the
account. The "Clear filters" button is the exit that makes it recoverable, which is what
distinguishes it from beneficiaries' no-results state (TC-BEN-007), where clearing the search box
is the only route back.

---

## TC-TXN-006 — "Money in" filter shows only Credit transactions

**State:** content

- **Given** Transactions loaded for account 40051512345678
- **When** User taps the "Money in" chip
- **Then**
  - Only transactions with `CreditDebitIndicator=Credit` displayed
  - SALARY ACME LTD row visible
  - TESCO STORES row **not** visible
  - Period summary strip `totalCredit` updates to £2,400.00; `totalDebit` to £0.00

The summary strip updating with the filter is what stops a filtered list sitting under unfiltered
totals — a screen that would look complete and read wrong.

---

## TC-TXN-007 — "Money out" filter shows only Debit transactions

**State:** content

- **Given** Transactions loaded for account 40051512345678
- **When** User taps the "Money out" chip
- **Then**
  - Only transactions with `CreditDebitIndicator=Debit` displayed
  - TESCO STORES row visible
  - SALARY ACME LTD row **not** visible

Each of 006 and 007 names one row that must appear and one that must not. An inverted predicate
passes a presence-only check on both.

---

## TC-TXN-008 — Search filters by TransactionInformation text

**State:** content

- **Given** Transactions loaded for account 40051512345678
- **When** User types "Tesco" in the search field
- **Then**
  - Only the "TESCO STORES 3476 LONDON" row displayed
  - All other rows hidden

The query is "Tesco" against a stored "TESCO STORES 3476 LONDON" — case-insensitive substring
matching, asserted implicitly by the choice of input.

This screen's search component was retyped from `text_field` to `search_bar` on 2026-07-31, one of
two `search_bar` uses in the project (with beneficiaries).

---

## TC-TXN-009 — Tapping a row navigates to transaction-detail with the correct params

**State:** content

- **Given** Transactions loaded; Tesco Stores row visible
- **When** User taps the TESCO STORES row
- **Then** Navigates to transaction-detail with `transactionId=TX-20260626-0001` and `accountId=40051512345678`

Both params, for the reason recorded in `TRAINING_MASTER#test_tags.builder_keys`: OBIE makes
`TransactionId` optional, so this screen's row tags fall back to `txn-$index`. An id that may be
positional is not unique outside its account, which is why `accountId` travels with it.

---

## TC-TXN-010 — Pending transaction shows a badge; booked rows show none

**State:** content

- **Given** Transactions loaded; SPOTIFY AB row has `Status=Pending`
- **When** Transaction list renders
- **Then**
  - "Pending" warning badge visible on the SPOTIFY AB row
  - TESCO STORES, SALARY ACME LTD and all other booked rows have **no** badge
  - Screen reader announces a "Pending" suffix in the accessibility label for the Spotify row

A pending transaction may still be reversed and its amount may still change. The screen-reader
assertion matters more than usual here — a badge is a purely visual signal, and without the
announced suffix a customer using TalkBack hears a settled amount.

Note the badge colour is not asserted on this screen, while transaction-detail (TC-TXNDTL-009)
pins it to `secondaryContainer`. Only the detail view constrains the role.

---

## TC-TXN-011 — Load more appends the next page when Links.Next is present

**State:** content

- **Given** First-page response contains a `Links.Next` URL with 10 transactions; the second page has 5 more and no `Links.Next`
- **When** User taps "Load more"
- **Then**
  - Linear progress indicator appears at the list bottom during the next-page fetch
  - Load more button hidden while `is_paginating=true`
  - 5 new transactions **appended** to the existing list
  - Load more button disappears after the final page (`Links.Next` absent)
  - Total list now shows **15** transactions

---

## TC-TXN-012 — Date range filter re-fetches with ISO-8601 bounds and resets the cursor

**State:** content

- **Given** Transactions loaded; pagination cursor `next_link` points to page 2
- **When** User opens the date range picker, selects 2026-06-01 to 2026-06-28, and confirms
- **Then**
  - `GET /accounts/40051512345678/transactions` called with `fromBookingDateTime=2026-06-01T00:00:00Z` and `toBookingDateTime=2026-06-28T23:59:59Z`
  - Previous `next_link` cursor reset to null **before** the new fetch
  - Transaction list replaced with date-bounded results
  - `has_next_page` re-evaluated from the new response

---

_Generated by /idea-feature-test-export | 2026-08-03_
