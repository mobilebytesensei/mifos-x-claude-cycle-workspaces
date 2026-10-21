# TEST SPEC — Consent Manager

| Field      | Value                                                          |
|------------|----------------------------------------------------------------|
| Feature    | consent-manager                                                |
| Source     | `screens/consent-manager/tests.yaml`                           |
| Scenarios  | 17                                                             |
| Priorities | high 12 · medium 3 · low 2                                     |
| States     | populated 9 · revoke_confirm 5 · loading 1 · empty 1 · error 1  |
| Module     | _none yet — spec-only feature_                                 |

> No source module exists. These are **forward specs** derived from the feature's idea-layer
> siblings, not reverse-synced from a shipped suite. Note the shipped `consent-list` and
> `consent-detail` features **do** have modules — this screen overlaps both, see below.

---

## Coverage

| State          | Scenarios | Covered |
|----------------|-----------|---------|
| loading        | 1 | TC-CMGR-001 |
| populated      | 9 | TC-CMGR-002 … -006, -012, -013, -016, -017 |
| revoke_confirm | 5 | TC-CMGR-007 … -011 |
| empty          | 1 | TC-CMGR-014 |
| error          | 1 | TC-CMGR-015 |

All five states covered. Nearly a third of the spec (TC-CMGR-007 … -011) sits on the revoke
confirmation, which is proportionate: revocation is the one irreversible action on the screen and
each step of the dialog — open, read, cancel, confirm, settle — is asserted separately.

---

## Overlap with the shipped consent screens

`consent-list` and `consent-detail` exist in source; this feature does not. TC-CMGR-006 navigates
to "the consent detail for that consentId", so the two are intended to compose rather than
compete — but `consent-list` covers the same listing surface. Recorded here because a reader
comparing the three specs will otherwise assume one supersedes another.

---

## Revoke, step by step

| Step | Scenario | Server call |
|------|----------|:-----------:|
| Tap revoke → dialog opens | TC-CMGR-007 | none |
| Dialog states the consequence | TC-CMGR-008 | none |
| Cancel → nothing changes | TC-CMGR-009 | none |
| Confirm → DELETE issued | TC-CMGR-010 | `DELETE …/consents/{consentId}` |
| Completion is final | TC-CMGR-011 | — |
| Failure leaves it active | TC-CMGR-012 | — |

Three of the six steps assert that **no** DELETE has happened yet. That is the shape you want
around an irreversible write.

---

## TC-CMGR-001 — Loading state shows the header while consents resolve

**Priority:** medium · **State:** loading

- **Given** `GET /obie/open-banking/v4.0/aisp/account-access-consents/{ConsentId}` is in flight (`initial_state: loading`)
- **When** Screen mounts
- **Then**
  - `consent_title` and `consent_subtitle` visible
  - No consent cards rendered

---

## TC-CMGR-002 — Populated state renders one card per granted consent

**Priority:** high · **State:** populated

- **Given** Two `ACCEPTED` consents and one `EXPIRED` consent
- **When** Screen renders
- **Then**
  - `consent_moneymanager`, `consent_taxhelper` and `consent_budgetwise` cards visible
  - Each card shows its logo, app name, dates, status badge and scope chips
  - The two active cards show a revoke button; the expired card shows a Remove button

The fixture deliberately mixes active and expired so the button divergence is exercised in the
same render — revoke and remove are different operations (TC-CMGR-013) and must not both appear
on the same card.

---

## TC-CMGR-003 — Each card lists the scopes actually granted

**Priority:** high · **State:** populated

- **Given** MoneyManager holds read-accounts, view-transactions and check-balances; TaxHelper holds only two
- **When** The scope rows render
- **Then**
  - `moneymanager_scopes_row` renders all three scope chips
  - `taxhelper_scopes_row` renders exactly its two chips
  - `budgetwise_scopes_row` renders its single chip
  - No card lists a scope the consent did not grant

Three cards with three different scope counts, which is what makes the last assertion testable. A
screen that renders a fixed scope list would pass a single-card fixture and fail this one.

This is the screen's core claim to the customer: it tells them what a third party can see. An
over-stated chip is alarming; an under-stated one is a privacy misrepresentation.

---

## TC-CMGR-004 — Status badges distinguish active from expired

**Priority:** high · **State:** populated

- **Given** Two `ACCEPTED` consents and one `EXPIRED` consent
- **When** The badges render
- **Then**
  - `moneymanager_active_badge` and `taxhelper_active_badge` render the active treatment
  - `budgetwise_expired_badge` renders the expired treatment
  - Status is carried by the badge text, not by colour alone

---

## TC-CMGR-005 — Consent dates are shown per card

**Priority:** medium · **State:** populated

- **Given** Consents carry `created_at` and `valid_until`
- **When** The date rows render
- **Then**
  - Each card shows its granted and expiry dates derived from `created_at` and `valid_until`
  - Dates render as formatted values, not raw ISO-8601 strings

---

## TC-CMGR-006 — Tapping a card opens its detail

**Priority:** high · **State:** populated

- **Given** Populated state
- **When** User taps `consent_moneymanager` (`view_consent_detail`)
- **Then**
  - The app opens the consent detail for that `consentId`
  - No revoke is triggered by the card tap itself

The second assertion matters because the revoke button lives inside the card. A tap target that
swallows its child's tap, or a card tap that falls through to the button, both fail here.

---

## TC-CMGR-007 — Revoke opens a confirmation dialog without revoking

**Priority:** high · **State:** revoke_confirm

- **Given** Populated state
- **When** User taps `moneymanager_revoke_button` (`revoke_consent`)
- **Then**
  - `RevokeConsentClicked` fires with the `consentId` and `appName`
  - `showRevokeDialog` becomes true and `pendingRevokeConsent` is set
  - `revoke_confirm_dialog` overlays the content with a scrim
  - No DELETE has been issued at this point

---

## TC-CMGR-008 — The dialog states the consequence and that reconnection is possible

**Priority:** high · **State:** revoke_confirm

- **Given** The revoke dialog is visible
- **When** It renders
- **Then**
  - `revoke_dialog_title` reads "Revoke access?"
  - `revoke_dialog_body` states access is removed immediately and the app can be reconnected at any time
  - `revoke_dialog_cancel_button` and `revoke_dialog_confirm_button` are both present

Both halves of the body copy are asserted, and they balance each other: "removed immediately" is
what stops a casual confirm, "can be reconnected" is what stops a customer being too frightened to
revoke at all. Dropping the second assertion would let the dialog become purely a deterrent.

---

## TC-CMGR-009 — Cancelling leaves the consent untouched

**Priority:** high · **State:** revoke_confirm

- **Given** The revoke dialog is visible
- **When** User taps `revoke_dialog_cancel_button` (`dismiss_revoke_dialog`)
- **Then**
  - `RevokeConsentCancelled` fires and `showRevokeDialog` becomes false
  - `pendingRevokeConsent` is cleared
  - The consent remains listed and active — no DELETE is issued

Clearing `pendingRevokeConsent` is not housekeeping. A stale pending id left behind is what makes
the *next* revoke confirmation target the wrong app.

---

## TC-CMGR-010 — Confirming issues the revoke against the bank

**Priority:** high · **State:** revoke_confirm

- **Given** The revoke dialog is visible for a `consentId`
- **When** User taps `revoke_dialog_confirm_button` (`confirm_revoke_consent`)
- **Then**
  - `RevokeConsentConfirmed` fires and `revokingConsentId` is set
  - `DELETE /obie/open-banking/v4.0/aisp/account-access-consents/{ConsentId}` is issued
  - The write target is `consent-revoke`

---

## TC-CMGR-011 — Revocation is irreversible and is presented as such

**Priority:** high · **State:** revoke_confirm

- **Given** A confirmed revoke
- **When** `RevokeConsentComplete` is handled
- **Then**
  - The card leaves the active list
  - Re-granting requires the full authorise round trip — no undo affordance is offered

Deliberately no undo, and correctly so: an undo that silently re-granted access would be a consent
grant without an authorisation journey.

---

## TC-CMGR-012 — A failed revoke surfaces and leaves the consent in place

**Priority:** high · **State:** populated

- **Given** The DELETE fails
- **When** The error is handled
- **Then**
  - `REVOKE_FAILED` resolves to "Could not revoke access. Please try again."
  - `revokingConsentId` is cleared
  - The consent is still listed as active — the UI does not show it as revoked

The keystone scenario. Optimistically removing the card on a failed DELETE tells a customer their
data is no longer being shared when it still is — the one lie this screen must never tell.

---

## TC-CMGR-013 — Removing an expired consent clears only the local record

**Priority:** medium · **State:** populated

- **Given** An `EXPIRED` consent card
- **When** User taps `budgetwise_remove_button`
- **Then**
  - `RemoveExpiredConsentClicked` fires for that `consentId`
  - The expired record is removed from the list
  - This is distinct from revoking live access

Two buttons, similar placement, very different meaning — one is a server write against live
access, the other is tidying a dead row. The third assertion is what keeps them from being
merged during a later "simplification".

---

## TC-CMGR-014 — Empty state explains how apps get connected

**Priority:** high · **State:** empty

- **Given** The consent list resolves empty
- **When** Screen renders
- **Then**
  - `empty_state_icon` (`ic_link_off`) visible
  - `empty_state_title` "No apps connected" visible
  - `empty_state_body` points the user to the bank's app marketplace
  - No consent cards render

---

## TC-CMGR-015 — Load failure renders the error state with retry

**Priority:** high · **State:** error

- **Given** The consents call returns 401 `USER_NOT_LOGGED_IN` or 403 `INSUFFICIENT_AUTHORISATION`
- **When** Screen renders
- **Then**
  - `LOAD_FAILED` resolves to "Unable to load connected apps. Please try again."
  - An error state with a retry affordance is shown, wired to `RetryLoad`
  - `consent_title` and `consent_subtitle` remain visible

Keeping the header visible in the error state is worth the assertion — a customer who opened this
screen to check who has access needs to be sure they are looking at a failure, not at an empty
list of connected apps.

---

## TC-CMGR-016 — Consent info is reachable from the header

**Priority:** low · **State:** populated

- **Given** Populated state
- **When** The `open_consent_info` action is invoked
- **Then**
  - `ConsentInfoOpened` fires
  - The explanation is reachable without leaving the screen unexplained

The trigger component is not named, so this scenario asserts an event without a declared control
to fire it. A component id is owed before it can be bound.

---

## TC-CMGR-017 — ConsentRepository is the only injected dependency

**Priority:** low · **State:** populated

- **Given** `ConsentManagerViewModel` is constructed
- **When** Its contract is inspected
- **Then**
  - `ConsentRepository` is the sole dependency
  - Only `get_consent_status`, `revoke_consent` and `poll_revocation_events` are called by this screen

---

## Traceability

| Action | Scenario |
|--------|----------|
| `view_consent_detail` | TC-CMGR-006 |
| `revoke_consent` | TC-CMGR-007 |
| `dismiss_revoke_dialog` | TC-CMGR-009 |
| `confirm_revoke_consent` | TC-CMGR-010 |
| remove expired | TC-CMGR-013 |
| `RetryLoad` | TC-CMGR-015 |
| `open_consent_info` | TC-CMGR-016 (no declared control) |

---

_Generated by /idea-feature-test-export | 2026-08-04_
