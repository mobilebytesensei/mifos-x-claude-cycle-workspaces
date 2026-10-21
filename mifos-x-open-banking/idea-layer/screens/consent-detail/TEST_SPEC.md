# TEST SPEC — Consent Detail

| Field      | Value                               |
|------------|-------------------------------------|
| Feature    | consent-detail                      |
| Source     | `screens/consent-detail/tests.yaml` |
| Scenarios  | 11                                  |
| Priorities | high 6 · medium 4 · low 1           |
| States     | content 5 · error 2 · loading 1 · revoke_confirm 1 · revoking 1 · empty 1 |
| Module     | `feature/consent-detail`            |

---

## Coverage

All six declared states covered, one scenario minimum each. This is the only screen in the corpus
whose revoke path is modelled as three distinct states — `content → revoke_confirm → revoking` —
and the scenarios walk that path in order (003 → 004/005), including the branch that backs out.

---

## Design drift — RESOLVED 2026-08-03

TC-CDETAIL-009 asserted the `Expired` status chip renders in `warning`. Two faults in one token:

1. **`warning` is not a colour role in this design system.** `design-tokens.yaml` 2.1.0 ships the
   M3 role set (primary, secondary, tertiary, error, …). There is no `warning` role, and no amber.
   TC-CDETAIL-010 — the sibling scenario, three rows further down this same file — already spelled
   the warning semantic correctly as `tertiaryContainer`.
2. **Even read charitably as "the warning tone", it pointed the wrong way.** `Expired` means access
   is gone, which is `error`. `tertiary` is the *expiring* tone: act soon, still live.

| Scenario | Was | Now (corrected in `tests.yaml`) |
|----------|-----|----------------------------------|
| TC-CDETAIL-009 | `Expired` chip → `warning` | → **`error`** (not primary, and not the tertiary expiring tone) |

Corrected at source by `/idea-sync` on 2026-08-03. This is the same defect class consent-list took
on the same date (TC-CLIST-006/007) and statement-detail took for its green/tertiary money roles;
neither of those passes reached this file, which is why it stayed open one run longer.

---

## TC-CDETAIL-001 — Content state renders status header, 10 permissions, all four dates, and CTAs

**Priority:** high · **State:** content

- **Given** consent-status GET returns `OBReadConsentResponse1` with `Status=Authorised`, 10 `Permissions[]`, all date fields present
- **When** Screen mounts with `consentId=aac-fb2c4e8a-7d31-4c9e-9f2a-1b3c5d7e9f01`
- **Then**
  - Status chip shows "Authorised" in `primary` colour
  - ConsentId label shows `aac-fb2c4e8a-7d31-4c9e-9f2a-1b3c5d7e9f01`
  - 10 permission rows render with label and description
  - "Connected on 2026-06-28T18:25:00Z" list item visible
  - "Expires on 2026-09-26T00:00:00Z" list item visible
  - "Transaction data from 2026-03-30T00:00:00Z" list item visible
  - "Transaction data to 2026-06-28T23:59:59Z" list item visible
  - "Reconfirm before expiry" button visible
  - "Revoke access" button visible in `error` colour
  - Expiry warning banner NOT visible (expiry > 7 days)

All four dates are asserted individually because they are four different questions — when access
started, when it ends, and the independent transaction window it covers. The four map to a private
`DateSlot` enum in source (`connected / expires / txnFrom / txnTo`), whose slugs are the per-row
test-tag suffixes recorded in `TRAINING_MASTER#test_tags.builder_keys`.

---

## TC-CDETAIL-002 — Loading state while consent-status GET is in flight

**Priority:** high · **State:** loading

- **Given** consent-status GET request is pending
- **When** Screen mounts
- **Then**
  - Circular progress indicator visible with accessibility label
  - No content components rendered

---

## TC-CDETAIL-003 — "Revoke access" transitions to revoke_confirm with a dialog

**Priority:** high · **State:** revoke_confirm

- **Given** Content state is active
- **When** User taps "Revoke access"
- **Then**
  - Confirmation dialog renders with title matching `{strings.consent_detail.revoke_dialog.title}`
  - "Keep access" and "Yes, revoke" buttons visible in the dialog
  - **No DELETE API call made**

The negative assertion is the substance. Revocation is irreversible from the app's side, so the
confirm step has to be a real gate rather than a dialog rendered alongside a request already in
flight.

---

## TC-CDETAIL-004 — "Keep access" returns to content with no API call

**Priority:** medium · **State:** content

- **Given** `revoke_confirm` state is active
- **When** User taps "Keep access"
- **Then**
  - Dialog dismissed; content state restored
  - No API call made

---

## TC-CDETAIL-005 — Confirming revoke calls DELETE, then navigates to consent-list

**Priority:** high · **State:** revoking

- **Given** HSBC sandbox returns 204 on `DELETE /account-access-consents/{ConsentId}`
- **When** User taps "Yes, revoke" in the confirm dialog
- **Then**
  - Screen transitions to `revoking` with a labelled progress indicator
  - `DELETE /account-access-consents/aac-fb2c4e8a-7d31-4c9e-9f2a-1b3c5d7e9f01` called **once**
  - Local `ConsentId` and PSU token cleared from storage
  - App navigates to consent-list

"Called once" is not pedantry on a DELETE — a double-fire produces a 404 on the second call, which
TC-CDETAIL-008 then has to absorb as success. Asserting the count keeps the two scenarios from
covering for each other.

---

## TC-CDETAIL-006 — Error state on consent-status GET failure (404)

**Priority:** high · **State:** error

- **Given** consent-status GET returns 404 (consent not found)
- **When** Screen mounts
- **Then**
  - `error_outline` icon visible
  - "Could not load consent" title visible
  - Error message body reflects `ConsentNotFound`
  - Retry button visible

---

## TC-CDETAIL-007 — Revoke network failure surfaces error state with retry

**Priority:** high · **State:** error

- **Given** Network is unreachable when the user taps "Yes, revoke"
- **When** `ExecuteRevoke` is dispatched
- **Then**
  - Screen transitions through `revoking` then to `error`
  - Error body reflects `ConsentDetailErrorCode.NetworkError`
  - Retry button present (re-triggers the GET on tap)
  - **Local PSU token NOT cleared** (the revoke did not succeed)

The last assertion is the one that matters most on this screen. Clearing local credentials on a
*failed* revoke would sign the customer out while leaving the bank-side consent live — the worst
of both outcomes, and invisible until they check their bank app.

---

## TC-CDETAIL-008 — 404 on DELETE treated as already-revoked

**Priority:** medium · **State:** content

- **Given** HSBC returns 404 on `DELETE /account-access-consents/{ConsentId}` (consent already gone server-side)
- **When** User taps "Yes, revoke"
- **Then**
  - No error state shown
  - Local `ConsentId` and PSU token cleared
  - App navigates to consent-list

The exact mirror of TC-CDETAIL-007: there, the goal failed and local state must survive; here, the
goal is already achieved and local state must go. Both are non-2xx responses, so the code cannot
branch on status class alone.

---

## TC-CDETAIL-009 — Expired consent renders status chip in the error colour

**Priority:** medium · **State:** content

- **Given** consent-status GET returns `Status=Expired`
- **When** Screen mounts
- **Then**
  - Status chip label shows "Expired"
  - Status chip colour is `error` (not `primary`, and not the `tertiary` expiring tone)
  - "Reconfirm before expiry" button still visible

The three-way contrast is the point, and it is why the corrected assertion names two roles it must
*not* be: `primary` is a live authorised consent, `tertiary` is one expiring soon, `error` is one
whose access is gone. Collapsing any two of those loses the distinction consent-list exists to draw.

Keeping the Reconfirm button on an already-expired consent is correct and deliberate — expiry is
precisely when re-authorisation is the action the customer needs.

---

## TC-CDETAIL-010 — Expiry warning banner when expiry is within 7 days

**Priority:** low · **State:** content

- **Given** `ExpirationDateTime` is 3 days from today
- **When** Screen enters content state
- **Then**
  - Expiry warning banner rendered above the dates section
  - Banner colour is `tertiaryContainer` (the warning semantic — see `semantic.status`)
  - Banner text references the expiry-warning strings key

This scenario names the warning tone correctly, which is the internal evidence that
TC-CDETAIL-009's `warning` is a slip rather than a second convention.

Note the threshold: 7 days here, against consent-list's 14-day `reconfirm_urgency_chip`
(TC-CLIST-006). Two different windows for the same concept, in two files. Not flagged as drift —
a list-level nudge landing earlier than a detail-level banner is defensible — but worth a decision
if the two are meant to be one rule.

---

## TC-CDETAIL-011 — Empty state when the consent resolves but carries no record

**Priority:** medium · **State:** empty

- **Given** `GET /account-access-consents/{ConsentId}` returns 200 with no `Data` block
- **When** Screen mounts
- **Then**
  - `empty_state` rendered with `link_off` icon
  - Title matches `{strings.consent_detail.empty.title}`
  - Body matches `{strings.consent_detail.empty.body}`
  - "Back to connections" button visible, navigates to consent-list
  - Revoke access and Reconfirm buttons NOT visible

A 200 with no body is not an error, which is why this is `empty` and not a fifth error case. The
two hidden CTAs are the assertion: there is nothing to revoke and nothing to reconfirm, and
offering either would fail against a consent that does not exist.

---

_Generated by /idea-feature-test-export | 2026-08-03_
