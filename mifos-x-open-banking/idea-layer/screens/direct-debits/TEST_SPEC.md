# TEST SPEC — Direct Debits

| Field      | Value                              |
|------------|------------------------------------|
| Feature    | direct-debits                      |
| Source     | `screens/direct-debits/tests.yaml` |
| Scenarios  | 10                                 |
| Priorities | P0 3 · P1 6 · P2 1                 |
| States     | error 4 · content 3 · loading 1 · empty 1 · unsupported 1 |
| Module     | `feature/direct-debits`            |

---

## Coverage

All six declared states covered, including `unsupported` — one of the three `unsupported` states
in the corpus (with scheduled-payments and standing-orders) that `/idea-sync` closed on
2026-08-02 as part of ST-1. TC-DD-010 is that closure.

Four of ten scenarios are error cases, and they exist to pin one decision per HTTP code:

| Scenario | Condition | `error.isRetriable` | Retry button |
|----------|-----------|---------------------|--------------|
| TC-DD-004 | 401 token expired | true | visible |
| TC-DD-006 | 403 consent revoked | **false** | hidden |
| TC-DD-007 | 429 rate limited | true | visible |
| TC-DD-008 | network / IOException | true | visible |

403 is the only one that hides Retry, and the scenario states why in its own text: retry cannot
help, the consent must be re-authorised. That single exception is what the other three exist to
contrast against.

---

## `unsupported` is not an error, and TC-DD-010 is careful about it

The distinction this screen draws is worth stating plainly. A 403 means the call was made and
refused; `unsupported` means **no network request happens at all** — the capability registry
refuses before dispatch, emitting `DirectDebitsUiState.Unsupported(message)`.

That is why TC-DD-010 asserts no Retry button. Retry implies a transient condition; an account
type that does not expose direct debits will never start doing so on a second attempt.

It is also why the body copy is asserted as a **dynamic string, not an i18n key** — the capability
registry supplies the reason, which varies by account type, while the title and accessibility
label stay static and localised. That mixed-provenance rule is unusual enough in this corpus to be
worth the explicit assertion it gets.

---

## TC-DD-001 — List loads and renders all mandates with correct status variants

**Priority:** P0 · **State:** content

- **Given** Valid PSU access token; HSBC sandbox returns 4 direct debits for account 40051512345678 (3 Active, 1 Inactive)
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - Four cards render (British Gas, Vodafone, Aviva Insurance, TV Licensing) sorted **Active-first**
  - Active mandates show a `primary` badge; TV Licensing shows an `outline` badge (not `secondary`)
  - Summary chips show "Active (3)" and "Inactive (1)"
  - Each card shows previous payment amount, date, and mandate identifier
  - **Amount text is neutral colour (not red/error)**
  - Data matches demo-data values

Two assertions carry real design intent. The `outline`-not-`secondary` badge keeps an inactive
mandate visually recessed without reading as a second live category. And the neutral amount colour
is the deliberate contrast with home and transactions, where debits render in `error`: a scheduled
direct debit is a normal arrangement, not money lost.

---

## TC-DD-002 — Skeleton loading shown during the fetch

**Priority:** P0 · **State:** loading

- **Given** Slow network; API call in flight
- **When** Screen mounts
- **Then**
  - Skeleton `list_card` placeholder (4 items) visible — **not** a progress spinner
  - Direct debits list and chip group not rendered

The "not a spinner" clause is a real assertion, not phrasing. This screen and accounts use
skeletons; beneficiaries and consent-detail use spinners. Both conventions are live in the corpus,
so each screen has to state which one it is.

---

## TC-DD-003 — Empty state when no direct debits are registered

**Priority:** P1 · **State:** empty

- **Given** HSBC returns an empty `Data.DirectDebit[]` for the account
- **When** Screen mounts
- **Then**
  - Empty state renders with `subscriptions` icon
  - Title and body from i18n keys (`direct_debits.empty_title` / `direct_debits.empty_body`)
  - No list or chip group rendered

---

## TC-DD-004 — 401 token expired shows message and Retry

**Priority:** P0 · **State:** error

- **Given** Access token is expired; direct-debits endpoint returns 401
- **When** Screen mounts
- **Then**
  - Error state renders with `error_outline` icon
  - `error.userMessage` = "Session expired. Please log in again."
  - Retry button visible (`error.isRetriable = true`)
  - Tapping Retry re-triggers `direct_debits_load`

---

## TC-DD-005 — Back button navigates to account-detail

**Priority:** P1 · **State:** content

- **Given** Direct debits rendered for account 40051512345678, reached from the account-detail DirectDebits chip
- **When** User taps the back button **in any state**
- **Then** Navigates to account-detail with `accountId=40051512345678`

"In any state" is the assertion. The back edge has to survive `error`, `empty` and `unsupported` —
TC-DD-006 and TC-DD-010 both remove the Retry button, so back is the only exit left on those
screens.

---

## TC-DD-006 — 403 consent revoked shows message without Retry

**Priority:** P1 · **State:** error

- **Given** `ReadDirectDebits` permission not in the active consent; endpoint returns 403
- **When** Screen mounts
- **Then**
  - Error state renders with `error.userMessage` = "Account access consent has been revoked. Re-authorise in Consents."
  - Retry button **NOT** visible (`error.isRetriable = false` — retry cannot help; the consent must be re-authorised)

---

## TC-DD-007 — 429 rate limited shows message with Retry

**Priority:** P1 · **State:** error

- **Given** HSBC AIS rate limit exceeded; endpoint returns 429
- **When** Screen mounts
- **Then**
  - Error state renders with `error.userMessage` = "Too many requests. Please wait a moment and try again."
  - Retry button visible (`error.isRetriable = true`)
  - Tapping Retry re-triggers `direct_debits_load`

---

## TC-DD-008 — Network error shows message with Retry

**Priority:** P1 · **State:** error

- **Given** Device is offline or DNS fails; `IOException` thrown by Ktorfit
- **When** Screen mounts
- **Then**
  - Error state renders with `error.userMessage` = "No network connection. Check your connection and retry."
  - Retry button visible (`error.isRetriable = true`)

---

## TC-DD-009 — i18n coverage, all static labels come from strings keys

**Priority:** P2 · **State:** content

- **Given** Default locale (en-GB)
- **When** Screen renders in content state
- **Then**
  - Top app bar title resolves from `strings.direct_debits.title` = "Direct Debits"
  - Back button accessible name resolves from `strings.direct_debits.back_a11y`
  - Last-collected prefix resolves from `strings.direct_debits.last_collected_prefix`
  - Mandate prefix resolves from `strings.direct_debits.mandate_prefix`
  - Chip labels resolve from `strings.direct_debits.active_count_label` / `inactive_count_label`

A dedicated i18n scenario is rare in this corpus — most screens rely on the project-level
`{strings.*}` gate. Keeping it here is worthwhile because the two *prefix* keys are the kind of
label that gets inlined during a hurried edit and never noticed in the default locale.

---

## TC-DD-010 — Unsupported state when the servicer does not expose direct debits

**Priority:** P1 · **State:** unsupported

- **Given** Account type does not support the direct-debits resource; the capability registry refuses the call before any network request is made, emitting `DirectDebitsUiState.Unsupported(message)`
- **When** Screen mounts with an `accountId` for an account whose type excludes the direct-debits capability
- **Then**
  - `unsupported_direct_debits` component renders (test tag `directDebits:unsupportedState`)
  - Title resolves from `strings.direct_debits.unsupported_title` ("Direct debits unavailable")
  - Body shows the dynamic `uiState.message` supplied by the capability registry — **not** a static i18n key
  - **No retry button** — the capability is absent, not a retriable network failure
  - No mandate list or summary chips rendered
  - Component accessibility label resolves from `strings.direct_debits.unsupported_a11y`

---

_Generated by /idea-feature-test-export | 2026-08-03_
