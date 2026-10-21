# TEST SPEC — Account Holder

| Field      | Value                                |
|------------|--------------------------------------|
| Feature    | account-holder                       |
| Source     | `screens/account-holder/tests.yaml`  |
| Scenarios  | 7                                    |
| Priorities | critical 4 · normal 3                |
| States     | content 2 · loading 1 · error 3 · empty 1 |
| Module     | `feature/account-holder`             |

---

## Coverage

| State   | Scenarios | Covered |
|---------|-----------|---------|
| loading | 1 | TC-ACCOUNT-HOLDER-002 |
| content | 2 | TC-ACCOUNT-HOLDER-001, -004 |
| empty   | 1 | TC-ACCOUNT-HOLDER-005 |
| error   | 3 | TC-ACCOUNT-HOLDER-003, -006, -007 |

All four declared states are covered. The error state carries three scenarios because the
feature's value is in *discriminating* error kinds — one retriable, two not.

---

## TC-ACCOUNT-HOLDER-001 — Account holder details load and render Priya Sharma's profile

**Priority:** critical · **State:** content

- **Given** Valid PSU access token with `ReadParty` in consent; party store emits a `PartyProfile` for account 40051512345678
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - `accountHolder:content` is displayed
  - `accountHolder:identityCard` renders
  - `accountHolder:avatar` shows initials `PS`
  - `accountHolder:displayName` shows `Priya Sharma`
  - `accountHolder:roleLabel` shows `Sole account holder`
  - `accountHolder:identitySection` renders
  - `accountHolder:emailRow` shows `priya.sharma@example.co.uk`
  - `accountHolder:mobileRow` shows `+44 7700 900482`
  - `accountHolder:addressRow` shows the flattened address line

---

## TC-ACCOUNT-HOLDER-002 — Loading state shown while the party stream has not emitted

**Priority:** critical · **State:** loading

- **Given** `ScreenState.Loading` from the party stream
- **When** Screen mounts
- **Then**
  - `accountHolder:loading` is displayed
  - `accountHolder:loadingCaption` is displayed
  - `accountHolder:identityCard` and `accountHolder:identitySection` are absent

---

## TC-ACCOUNT-HOLDER-003 — Retriable error shows the Retry CTA and RetryLoad refreshes the stream

**Priority:** critical · **State:** error

- **Given** Party fetch fails with `NetworkError.Client.Unauthorized` → `AccountHolderErrorKind.TokenExpired`
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - `accountHolder:errorState` renders
  - `accountHolder:errorTitle` and `accountHolder:errorBody` are displayed
  - `accountHolder:retryButton` is visible (`kind.isRetriable = true`)
  - Tapping it dispatches `AccountHolderAction.RetryLoad`, which calls `stream.refresh()`

---

## TC-ACCOUNT-HOLDER-004 — Back navigation returns to account-detail

**Priority:** normal · **State:** content

- **Given** Content state rendered for account 40051512345678
- **When** User taps the leading back icon in the top app bar
- **Then** `onBack` fires `popBackStack()`, returning to `account-detail`

---

## TC-ACCOUNT-HOLDER-005 — Empty state shown when the mapped profile has a blank display name

**Priority:** normal · **State:** empty

- **Given** Party store emits a `PartyProfile` whose `displayName` is blank for business account 40051999000001
- **When** Screen mounts with `accountId=40051999000001`
- **Then**
  - `emptyIfContent` collapses `Content` to `AccountHolderUiState.Empty`
  - `accountHolder:emptyState` renders
  - `accountHolder:emptyTitle` and `accountHolder:emptyBody` are displayed
  - No retry CTA present

---

## TC-ACCOUNT-HOLDER-006 — Missing ReadParty consent renders on the error surface with retry suppressed

**Priority:** critical · **State:** error

- **Given** Active consent does not include `ReadParty`; `/party` returns 403 → `NetworkError.Client.Forbidden`
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - `classifyAccountHolderError` maps `Forbidden` to `AccountHolderErrorKind.ConsentMissingParty`
  - `accountHolder:errorState` renders with consent-specific body copy
  - `accountHolder:retryButton` is **NOT** displayed (`isRetriable = false`)
  - No navigation to `consent-list` occurs — source models no re-authorise route from this screen

The keystone scenario. It pins both halves of the permission contract: retry is withheld because
re-issuing a request the consent does not authorise cannot succeed, **and** the screen does not
invent a re-authorise route that source does not have.

---

## TC-ACCOUNT-HOLDER-007 — Unknown account id maps to a non-retriable not-found error

**Priority:** normal · **State:** error

- **Given** `/party` returns 404 → `NetworkError.Client.NotFound`
- **When** Screen mounts with an `accountId` that has no party record
- **Then**
  - `AccountHolderErrorKind.ProfileNotFound` is emitted
  - `accountHolder:retryButton` is **NOT** displayed (`isRetriable = false`)

---

## Traceability

| Error kind | Scenario | Retriable |
|------------|----------|-----------|
| `TokenExpired` | TC-ACCOUNT-HOLDER-003 | yes |
| `ConsentMissingParty` | TC-ACCOUNT-HOLDER-006 | no |
| `ProfileNotFound` | TC-ACCOUNT-HOLDER-007 | no |

Every kind declared in `state_model.errors.types` has exactly one covering scenario.

---

_Generated by /idea-feature-test-export | 2026-08-03_
