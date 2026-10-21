# TEST SPEC — Statement Detail

| Field      | Value                                 |
|------------|---------------------------------------|
| Feature    | statement-detail                      |
| Source     | `screens/statement-detail/tests.yaml` |
| Scenarios  | 9                                     |
| Priorities | critical 6 · normal 3                 |
| States     | content 4 · error 3 · loading 1 · empty 1 |
| Module     | `feature/statement-detail`            |

---

## Coverage

Contiguous ids; all four declared states covered. Three error scenarios (404, 403, 401), all
offering Retry, plus a **separate** download-failure path (TC-STMTD-008) that deliberately does
*not* enter the error state — see below.

---

## Colour drift — RESOLVED 2026-08-03

TC-STMTD-001 originally read "green/tertiary" for positive money at three sites. Both halves were
wrong:

- **This palette ships no green.** "Open Banking — Trust Blue" (seed `#266489`, tokens 2.1.0) has
  no green role in either mode.
- **`tertiary` means warning / attention-needed** in DESIGN.md 1.3.0 — the same role consent-list
  uses for an *expiring* consent.

The declared money pair is **positive/credit → `primary`**, **negative/debit → `error`**, chosen
explicitly to be "never green-on-red, to stay calm and colour-blind-safe". A credited closing
balance or in-credit interest is positive money, not a warning about it.

Corrected at source by `/idea-sync` on 2026-08-03; the assertions below reflect the corrected
roles. Same defect family as the consent-list correction (TC-CLIST-006/007) landed the same day —
and the one still open on consent-detail (TC-CDETAIL-009), which this file's fix did not reach.

---

## Download is a sub-state, not a screen state

Four scenarios touch the PDF download, and all four keep it **inside** `content`:

| Scenario | Outcome | Screen state |
|---|---|---|
| TC-STMTD-004 | file served | `content` + `downloadState=Downloaded` + snackbar |
| TC-STMTD-008 | 404, no file generated | `content` + `downloadState=DownloadError` + snackbar, button re-enabled |
| TC-STMTD-007 | statement has no transactions | `empty`, download button **still enabled** |
| TC-STMTD-001 | happy path | button visible and enabled |

A failed download must not replace a statement the customer is successfully reading. The button
re-enabling in 008 is the other half of that: a transient file-generation gap should leave them
able to try again, not stranded on a dead affordance.

---

## TC-STMTD-001 — Loads with period, balances, fees, interest, and 6 transactions

**Priority:** critical · **State:** content

- **Given** Valid PSU access token; HSBC sandbox returns MAY-2026-STMT with 6 transactions
- **When** Screen mounts with `accountId=40051512345678` and `statementId=STMT-2026-05-40051512345678`
- **Then**
  - Top app bar title shows the statement reference MAY-2026-STMT
  - Period header shows 1 May 2026 – 31 May 2026
  - Statement type "RegularPeriodic" visible
  - **Balances:** Opening Balance £2,610.40 (neutral), Closing Balance £2,847.63 (`primary`)
  - **Fees:** "Monthly maintenance fee £0.00" renders
  - **Interest:** "In-credit interest £0.21" renders in `primary`
  - 6 transaction rows render with date overline, description, and sign-prefixed amount
  - Credit transactions show "+" and `primary`; debits show "−" and `error`
  - Download PDF button visible and enabled

Opening balance is **neutral** while closing is `primary` — a deliberate asymmetry. The opening
figure is a starting point, not an outcome, and colouring both would make the section read as two
results rather than a movement between them.

Sign prefix and colour are asserted together, as on home (TC-HOME-015). Either alone leaves a
colour-blind customer or a greyscale screenshot with no direction.

---

## TC-STMTD-002 — Loading state during the parallel fetch

**Priority:** critical · **State:** loading

- **Given** Slow network; both API calls (statement-detail and statement-txns) in flight
- **When** Screen mounts
- **Then**
  - Circular progress indicator visible with an accessible label
  - Content sections not rendered
  - Top app bar title falls back to the localised "Statement"

The title fallback is the detail worth keeping. The bar renders before the statement reference
exists, so without a fallback it shows an empty or placeholder title for the duration of the
fetch.

---

## TC-STMTD-003 — Error with Retry on 404 statement not found

**Priority:** critical · **State:** error

- **Given** `StatementId` does not exist; endpoint returns HTTP 404
- **When** Screen mounts
- **Then**
  - Error icon and localised "Could not load statement" title render
  - Body shows "Statement not found."
  - Retry button visible with the correct accessible label
  - Tapping Retry re-triggers `statementDetailLoad`

Note this screen treats 404 as an **error**, where product (TC-PROD-006) treats it as **empty**.
Both are right for their case, and the difference is worth stating: a product with no published
terms is a normal condition, whereas a statement the customer navigated to from a list that
contained it has genuinely gone missing.

---

## TC-STMTD-004 — Download PDF triggers the file call, shows progress, then a success snackbar

**Priority:** critical · **State:** content

- **Given** Statement MAY-2026-STMT rendered in content state for account 40051512345678; the bank serves a file for this statement (contrast TC-STMTD-008, where it 404s)
- **When** User taps Download PDF
- **Then**
  - statement-file endpoint called with the correct `AccountId` and `StatementId`
  - Download PDF button becomes **disabled** while Downloading
  - Linear progress indicator appears beneath the button
  - On success: `downloadState=Downloaded`; snackbar "Statement PDF saved" appears and auto-dismisses after 4s
  - Native share/save sheet presented with the PDF binary

Disabling the button during the download is the guard against a double request — the same reason
standing-order-edit puts its save button into a `loading` state (TC-SOE-003).

---

## TC-STMTD-005 — Back navigation returns to the statements list

**Priority:** normal · **State:** content

- **Given** Statement MAY-2026-STMT rendered in content state, reached from the statements list
- **When** User taps the back button in the top app bar
- **Then** Navigates back to the statements screen

---

## TC-STMTD-006 — Error with a specific message on 403 consent scope missing

**Priority:** critical · **State:** error

- **Given** PSU consent does not include `ReadStatementsDetail`
- **When** Screen mounts and the endpoint returns HTTP 403
- **Then**
  - Error state renders with "Could not load statement" title
  - Body shows "Consent does not include ReadStatementsDetail."
  - Retry button visible

**Corrected 2026-08-03** (`/idea-sync`). The body text previously said `ReadStatements` while the
`given` names the missing scope as `ReadStatementsDetail`. Those are two distinct OBIE
permissions — the detail scope is what this screen needs, the list scope is what statements
(TC-STMTS-009, unchanged and correct) needs. The message named the wrong permission to a customer
trying to re-authorise with the right scope.

---

## TC-STMTD-007 — Empty state when the statement has no transactions in period

**Priority:** normal · **State:** empty

- **Given** Valid HSBC response: `OBStatement2` with balances returned, statement-txns returns an empty `Data.Transaction[]`
- **When** Screen mounts
- **Then**
  - Period header card and Balances section render as normal
  - Transactions section header visible
  - Empty state component renders with "No transactions" title and explanatory body
  - Download PDF button **still visible and enabled**

A *partial* empty, like account-detail's TC-ACCTDTL-011. The statement exists and its balances are
real; only one section is empty. Collapsing the whole screen would hide a valid statement — and the
PDF, which is exactly what a customer wants for a quiet month.

---

## TC-STMTD-008 — Download error snackbar on statement-file 404

**Priority:** normal · **State:** content

- **Given** Statement PDF not yet generated by HSBC (HTTP 404 on the statement-file endpoint)
- **When** User taps Download PDF
- **Then**
  - Linear progress appears briefly
  - `downloadState` transitions to `DownloadError`
  - Snackbar "Download failed" appears and auto-dismisses
  - Download PDF button **re-enabled**

The same 404 that puts the *statement* fetch into an error state (TC-STMTD-003) is handled here as
a transient snackbar, because the failure is scoped to a file that may simply not be generated yet
while the statement it belongs to is on screen and fully readable.

---

## TC-STMTD-009 — Error with session-expired message on 401

**Priority:** critical · **State:** error

- **Given** PSU access token has expired; endpoint returns HTTP 401
- **When** Screen mounts with a valid `accountId` and `statementId`
- **Then**
  - Error icon and localised "Could not load statement" title render
  - Body shows "Session expired. Please re-authenticate."
  - Retry button visible with an accessible label matching `stmt_detail.a11y.retry`
  - Tapping Retry re-triggers `statementDetailLoad`

---

_Generated by /idea-feature-test-export | 2026-08-03_
