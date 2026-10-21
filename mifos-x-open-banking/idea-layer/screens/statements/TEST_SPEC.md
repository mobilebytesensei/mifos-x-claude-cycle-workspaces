# TEST SPEC — Statements

| Field      | Value                            |
|------------|----------------------------------|
| Feature    | statements                       |
| Source     | `screens/statements/tests.yaml`  |
| Scenarios  | 9                                |
| Priorities | critical 4 · normal 5            |
| States     | content 4 · error 3 · loading 1 · empty 1 |
| Module     | `feature/statements`             |

---

## Coverage

Contiguous ids; all four declared states covered. Three error scenarios, one per HTTP code, and
all three offer Retry — consistent within this screen, though TC-STMTS-009's 403 sits on the
Retry-offering side of the corpus-wide 403 split (with product, scheduled-payments and
standing-orders, against direct-debits and home).

---

## Two tap targets on one row (TC-STMTS-005 / TC-STMTS-007)

Each statement row carries a body tap **and** a download icon button, and the pair of scenarios
covering them is really one assertion split in two:

- **005** — tapping the row body navigates to statement-detail with both params.
- **007** — tapping the download icon fires the file request **and row-tap navigation does NOT
  fire** (event propagation stopped).

Nested clickables inside a list row are the classic Compose defect: the child handles the tap and
the parent handles it too, so the customer taps Download and lands on a different screen while a
download starts behind it. The negative assertion in 007 is the only thing that catches it.

---

## TC-STMTS-001 — Statement list loads and renders 6 rows

**Priority:** critical · **State:** content

- **Given** Valid PSU access token; HSBC sandbox returns 6 statements (Dec 2025 – May 2026) for account 40051512345678
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - Six rows render sorted **descending** by `StartDateTime` (May 2026 first)
  - Each headline shows a derived period label (e.g. "May 2026")
  - Each supporting text shows "Closing balance: £2,847.63" for MAY-2026-STMT
  - Each trailing shows a formatted date range (e.g. "1 May 2026 – 31 May 2026")
  - Each row has a download icon button

The period label is **derived**, not returned — OBIE gives `StartDateTime`/`EndDateTime`, and "May
2026" is the app's own rendering. Asserting the derived label and the raw range on the same row
keeps the derivation checkable against its input.

---

## TC-STMTS-002 — Skeleton loading state while the list is fetched

**Priority:** critical · **State:** loading

- **Given** Slow network; API call in flight
- **When** Screen mounts
- **Then**
  - Skeleton list with 3 shimmer rows visible
  - Statement list not rendered
  - Accessibility label "Loading statement list" announced

---

## TC-STMTS-003 — Error with Retry on 401 token expired

**Priority:** critical · **State:** error

- **Given** Access token is expired; statements endpoint returns HTTP 401
- **When** Screen mounts
- **Then**
  - Error state renders with `error_outline` icon
  - Title "Could not load statements"
  - Message "Session expired. Please re-authenticate."
  - Retry button visible, labelled "Retry"
  - Tapping Retry re-triggers `retry_load`, which delegates to `statementsLoad(accountId)`

---

## TC-STMTS-004 — Empty state when no statements are returned

**Priority:** normal · **State:** empty

- **Given** HSBC returns `OBReadStatement2` with an empty `Data.Statement[]`
- **When** Screen mounts
- **Then**
  - Empty state renders with `description` icon
  - Title "No statements yet"
  - Body explains statement history will appear once available

"Yet" is doing the work in that title. A new account with no statement history is in a normal,
temporary condition, and the body says so rather than leaving the customer to wonder whether
something failed.

---

## TC-STMTS-005 — Tapping a statement row navigates with the correct params

**Priority:** critical · **State:** content

- **Given** Statements list rendered in content state for account 40051512345678, including the "May 2026" row (MAY-2026-STMT)
- **When** User taps the "May 2026" row body
- **Then**
  - Navigates to statement-detail
  - `statementId` = "STMT-2026-05-40051512345678"
  - `accountId` = "40051512345678"

Note the row's display id (MAY-2026-STMT) and its route param (STMT-2026-05-40051512345678) are
**different strings**. Asserting the param explicitly is what stops the label being passed as the
key.

---

## TC-STMTS-006 — Closing balance displayed correctly on statement rows

**Priority:** normal · **State:** content

- **Given** `StatementAmount` includes `ClosingBalance` entries for each statement
- **When** Content state renders
- **Then**
  - MAY-2026-STMT shows "Closing balance: £2,847.63"
  - APR-2026-STMT shows "Closing balance: £2,610.40"
  - DEC-2025-STMT shows "Closing balance: £1,502.88"

Three rows rather than one. `StatementAmount` is an array of typed amounts — closing balance sits
alongside opening balance and others — so picking the right entry per statement is the thing being
tested, and a single row could pass on a first-element read.

---

## TC-STMTS-007 — Download icon triggers the file request for the correct StatementId

**Priority:** normal · **State:** content

- **Given** Statements list rendered in content state; the "May 2026" row (MAY-2026-STMT) shows its download affordance
- **When** User taps the download icon on that row
- **Then**
  - `GET /accounts/40051512345678/statements/STMT-2026-05-40051512345678/file` fires with `Accept: application/pdf, text/csv`
  - **Row-tap navigation does NOT fire** (event propagation stopped)
  - On success, the platform file handler receives the statement bytes
  - On HTTP 501 from HSBC, toast "Statement download not available for this account"

The 501 branch is worth keeping: OBIE lets a servicer implement the statement resource without
implementing the file resource, so "not available for this account" is a normal response, not a
fault. Handling it as a toast rather than an error state keeps the list usable.

---

## TC-STMTS-008 — Error on HTTP 429 rate-limit

**Priority:** normal · **State:** error

- **Given** HSBC AIS returns HTTP 429 for the statements endpoint
- **When** Screen mounts
- **Then**
  - Error state renders with "Too many requests. Please wait and retry."
  - Retry button visible

---

## TC-STMTS-009 — Error on HTTP 403 shows the consent-scope message

**Priority:** normal · **State:** error

- **Given** Consent does not include `ReadStatements`; HSBC returns HTTP 403
- **When** Screen mounts
- **Then**
  - Error state renders with "Consent does not include ReadStatements."
  - Retry button visible

Naming the missing scope is the right level of detail — it tells a customer which permission to
add when they re-authorise, rather than reporting a generic refusal they cannot act on.

---

_Generated by /idea-feature-test-export | 2026-08-03_
