# TEST SPEC — Beneficiaries

| Field      | Value                              |
|------------|------------------------------------|
| Feature    | beneficiaries                      |
| Source     | `screens/beneficiaries/tests.yaml` |
| Scenarios  | 10                                 |
| Priorities | p0 3 · p1 4 · p2 2 · (see note)    |
| States     | content 6 · error 2 · loading 1 · empty 1 |
| Module     | `feature/beneficiaries`            |

---

## Coverage

All five declared states covered — `content`, `loading`, `empty`, `error`, and the `searching`
behaviour exercised inside `content` (TC-BEN-006/007/010) rather than as a separate state row.

**Priority vocabulary differs here.** This screen uses `p0/p1/p2`; the rest of the project uses
`critical/high/medium/low`. Transcribed as declared rather than mapped — a silent normalisation
would hide that two vocabularies are live in one corpus.

Priorities as declared: p0 = 001, 002, 004 · p1 = 003, 005, 008, 010 · p2 = 007, 009.
TC-BEN-006 declares `p1`. That is 3 + 5 + 2 = 10.

---

## The two error scenarios are a matched pair

TC-BEN-004 (401) and TC-BEN-008 (403) each assert both the button that must appear **and** the one
that must not:

| Scenario | HTTP | OBIE code | Retry | View Consents |
|----------|------|-----------|-------|---------------|
| TC-BEN-004 | 401 | `UK.OBIE.Header.Invalid` | visible | **not** visible |
| TC-BEN-008 | 403 | `UK.OBIE.Resource.ConsentMismatch` | **not** visible | visible |

The exclusions carry the weight. A revoked consent cannot be retried into working, and an expired
token is not fixed by visiting the consent list — showing both buttons in both states would be
the easy implementation and the wrong one.

---

## TC-BEN-001 — Beneficiaries list loads and renders all five saved payees

**Priority:** p0 · **State:** content

- **Given** Valid PSU access token; HSBC sandbox returns 5 beneficiaries for account 40051512345678 across SortCodeAccountNumber and IBAN schemes
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - Five beneficiary rows render (Jameson Lettings, John Sharma, EDF Energy, Hargreaves Lansdown, Priya Rajan — N26 GmbH)
  - Each row shows avatar initials, creditor name as headline, scheme label + identifier as supporting text, reference as trailing label
  - BEN-005 row shows scheme label "IBAN" and identification "DE89370400440532013000"
  - Data matches demo-data values

The IBAN row is the reason five payees are fixtured rather than two — the list must render two
account-identification schemes side by side without one formatting the other.

---

## TC-BEN-002 — Loading state shown during the beneficiaries fetch

**Priority:** p0 · **State:** loading

- **Given** Slow network; API call in flight
- **When** Screen mounts
- **Then**
  - Circular progress indicator visible and labelled "Loading beneficiaries"
  - Beneficiary list and search bar not rendered

---

## TC-BEN-003 — Empty state when no beneficiaries are registered

**Priority:** p1 · **State:** empty

- **Given** HSBC sandbox returns an empty `Data.Beneficiary[]` for the account
- **When** Screen mounts
- **Then**
  - Empty state renders with `people_outline` icon
  - Title "No beneficiaries", body "No saved payees are registered for this account."
  - Search bar is NOT visible

Hiding the search bar is the assertion worth keeping. A search field over an empty set is an
invitation to conclude the search is broken.

---

## TC-BEN-004 — Error state with Retry on 401 token expired

**Priority:** p0 · **State:** error

- **Given** Access token is expired; HSBC AIS returns 401 `UK.OBIE.Header.Invalid`
- **When** Screen mounts
- **Then**
  - Error state renders with `error_outline` icon and typed error message
  - Retry button visible; View Consents button NOT visible
  - Tapping Retry re-triggers `beneficiaries_load`

---

## TC-BEN-005 — Back button navigates to account-detail

**Priority:** p1 · **State:** content

- **Given** Beneficiaries list rendered for account 40051512345678
- **When** User taps the back button
- **Then** Navigates to account-detail with `accountId=40051512345678`

---

## TC-BEN-006 — Search bar filters beneficiaries by creditor name

**Priority:** p1 · **State:** content

- **Given** Five beneficiaries loaded; user types "ener" into the search bar
- **When** `on_change` fires with `query='ener'`
- **Then**
  - Only the EDF Energy row is visible (BEN-003)
  - Remaining four rows are hidden
  - **No API call is made** (client-side filter)
  - Clearing the search bar restores all five rows

---

## TC-BEN-007 — Search yields a no-results empty state inside content

**Priority:** p2 · **State:** content

- **Given** Five beneficiaries loaded; user types "zzzmatch" into the search bar
- **When** `on_change` fires with `query='zzzmatch'`
- **Then**
  - `search_no_results` empty state renders with `search_off` icon
  - Beneficiary list is hidden
  - Title "No results", body "No payees match your search."

Note the state stays `content`, not `empty`. "You have no payees" and "your search matched
nothing" are different messages with different exits, and collapsing them would tell a customer
with five saved payees that they have none.

---

## TC-BEN-008 — Error state with View Consents on 403 consent revoked

**Priority:** p1 · **State:** error

- **Given** Consent has been revoked; HSBC AIS returns 403 `UK.OBIE.Resource.ConsentMismatch`
- **When** Screen mounts
- **Then**
  - Error state renders with `error_outline` icon and typed error message
  - View Consents button visible; Retry button NOT visible
  - Tapping View Consents navigates to consent-list

---

## TC-BEN-009 — Avatar initials derived from creditor name

**Priority:** p2 · **State:** content

- **Given** Beneficiaries list loaded
- **When** User views the list
- **Then**
  - Jameson Lettings row shows avatar "JL"
  - EDF Energy row shows avatar "EE"
  - N26 GmbH row shows avatar "PR" (from "Priya Rajan")
  - Avatars are marked `aria-hidden` and do not appear in the screen-reader tree

The N26 case is the interesting one: initials come from the *person*, not the servicing
institution, so the derivation cannot simply read the row's displayed creditor field. The
`aria-hidden` assertion pairs with it — initials are a visual shortcut, and a screen reader
announcing "P R" before the name it abbreviates is noise.

---

## TC-BEN-010 — Search bar filters beneficiaries by payment reference

**Priority:** p1 · **State:** content

- **Given** Five beneficiaries loaded; user types "ISA" into the search bar
- **When** `on_change` fires with `query='ISA'`
- **Then**
  - Only the Hargreaves Lansdown row is visible (BEN-004, `Reference='ISA-TOPUP'`)
  - Remaining four rows are hidden
  - No API call is made (the client-side filter applies to the `Reference` field too)
  - Clearing the search bar restores all five rows

Paired with TC-BEN-006 this pins the filter to *two* fields. A name-only implementation passes 006
and fails here, which is the point of keeping both.

---

_Generated by /idea-feature-test-export | 2026-08-03_
