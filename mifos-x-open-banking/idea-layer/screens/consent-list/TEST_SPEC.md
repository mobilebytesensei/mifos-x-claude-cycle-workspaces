# TEST SPEC — Consent List

| Field      | Value                              |
|------------|------------------------------------|
| Feature    | consent-list                       |
| Source     | `screens/consent-list/tests.yaml`  |
| Scenarios  | 8                                  |
| Priorities | high 5 · medium 3                  |
| States     | content 4 · loading 1 · empty 1 · error 1 · error_auth 1 |
| Module     | `feature/consent-list`             |

---

## Coverage

All five declared states covered. `error` and `error_auth` are separately exercised
(TC-CLIST-004 / TC-CLIST-008), which is the point of modelling them apart — one offers Retry,
the other must not.

---

## Design drift — RESOLVED 2026-08-03

When this spec was first exported, TC-CLIST-006 and TC-CLIST-007 asserted status colours that
contradicted DESIGN.md 1.3.0 **in opposite directions** — the live consent coloured as failed,
the dead one as neutral:

| Scenario | Was | Now (corrected in `tests.yaml`) |
|----------|-----|----------------------------------|
| TC-CLIST-006 | expiring (7 days) → `error` colour, `warning_amber` icon | → **`tertiary`** + `schedule`. A consent 7 days out has not failed; access is live and reconfirm works. This palette also ships no amber. |
| TC-CLIST-007 | `Expired` chip → `onSurfaceVariant` + `schedule` | → **`error`** + `error` icon. "Error stays reserved for Revoked, Rejected and Expired, where access is actually gone." |

Both were corrected at source by `/idea-sync` on 2026-08-03, and the scenarios below reflect the
corrected assertions. The two rules exist precisely so that "act soon" and "too late" do not
share a colour.

---

## TC-CLIST-001 — Authorised consent card renders with all required fields

**Priority:** high · **State:** content

- **Given** One `Authorised` consent (`aac-fb2c4e8a`) with 89 `days_until_expiry` in local store; consent-status returns `Authorised`
- **When** Screen mounts
- **Then**
  - Card visible under the "Active" section label
  - HSBC logo visible with `accessibility_label` "HSBC"
  - Status chip shows "Authorised" in `primary` colour with `check_circle` icon
  - "10 data types shared" text visible
  - "Expires in 89 days" text visible in `onSurfaceVariant` colour
  - "Connected 28 Jun 2026" label visible
  - `reconfirm_urgency_chip` NOT visible (89 days > 14)

Consistent with DESIGN.md — `Authorised` → `primary` + `check_circle`.

---

## TC-CLIST-002 — Loading state shown while consent-status is being fetched

**Priority:** high · **State:** loading

- **Given** consent-status GET in flight
- **When** Screen mounts
- **Then**
  - Circular progress indicator visible with `accessibility_label` matching `{strings.consent_list_loading}`
  - Consent list not rendered; "Active" section label not visible

---

## TC-CLIST-003 — Empty state shown when no local consent IDs found

**Priority:** high · **State:** empty

- **Given** No `ConsentId`s in local storage
- **When** Screen mounts
- **Then**
  - `link_off` icon visible
  - Title matching `{strings.consent_list_empty_title}` visible
  - Body matching `{strings.consent_list_empty_body}` visible
  - "Connect HSBC" button visible; tap navigates to login (`LoginRenewRoute`)
  - "Active" and "History" section labels NOT rendered

---

## TC-CLIST-004 — Generic error state shown on non-auth API failure

**Priority:** medium · **State:** error

- **Given** consent-status GET returns HTTP 500
- **When** Screen mounts
- **Then**
  - `error_outline` icon visible
  - Title matching `{strings.consent_list_error_title}` visible
  - Retry button visible; tap triggers `retry_load` action
  - Auth error state (`lock_open` icon / "Sign in again" button) NOT shown

---

## TC-CLIST-005 — Tapping an active consent card navigates to consent-detail

**Priority:** high · **State:** content

- **Given** `Authorised` consent `aac-fb2c4e8a-7d31-4c9e-9f2a-1b3c5d7e9f01` rendered in the Active section
- **When** User taps the consent card
- **Then** App navigates to `consent-detail` with `consentId=aac-fb2c4e8a-7d31-4c9e-9f2a-1b3c5d7e9f01`

---

## TC-CLIST-006 — Near-expiry consent (≤14 days) shows reconfirm urgency chip and top banner

**Priority:** high · **State:** content

- **Given** Two active consents — one with 89 `days_until_expiry`, one with 7 (`aac-d4e5f6a7`)
- **When** Screen renders
- **Then**
  - `reconfirm_banner` visible at top of content area (`has_near_expiry_consents=true`)
  - `reconfirm_urgency_chip` with `schedule` icon visible on the 7-day card, in `tertiary`
  - Expiry text "Expires in 7 days" renders in `tertiary` colour on the 7-day card
  - 89-day card does NOT show `reconfirm_urgency_chip`
  - 89-day card expiry text renders in `onSurfaceVariant` colour

The two-signal design (banner **and** chip) is the part worth protecting — a customer scrolling
past one indicator still sees the other. `tertiary` is the warning role: the consent is live and
reconfirmable, so it must not read as broken. The 89-day card stays neutral, which is the
control case proving the ≤14-day threshold actually gates.

---

## TC-CLIST-007 — Expired consent appears in History section below divider

**Priority:** medium · **State:** content

- **Given** Two `Authorised` consents in `active_consents` and one `Expired` (`aac-a1b2c3d4`) in `history_consents`
- **When** Screen renders
- **Then**
  - "Active" section label and two active cards visible at top
  - Horizontal divider visible between active and history sections
  - "History" section label visible below divider
  - Expired consent card visible with "Expired" status chip in `error` colour and `error` icon
  - History card shows "Expired on 26 Jun 2026" and "Connected 12 Mar 2026"
  - History card has `elevation=0` (flat, visually subordinate)

Two independent signals for a dead consent: `error` tone says access is gone, and the flat
elevation plus History placement say it is history. Tone recession alone would have been
ambiguous with the merely-expiring case above — which is exactly why the two must not share a
colour.

---

## TC-CLIST-008 — HTTP 401 on consent-status shows dedicated auth error state with re-auth CTA

**Priority:** medium · **State:** error_auth

- **Given** consent-status GET returns HTTP 401 Unauthorized (PSU access token expired)
- **When** Screen mounts
- **Then**
  - `lock_open` icon visible
  - Title matching `{strings.consent_list_auth_error_title}` visible
  - Body matching `{strings.consent_list_auth_error_body}` visible
  - "Sign in again" button visible; tap triggers `navigate_reauth` → navigates to login
  - Generic Retry button NOT shown (avoids misleading retry of an auth-expired session)

The final assertion is the reason `error_auth` exists as its own state. Offering Retry on an
expired session invites the customer to fail repeatedly at something that cannot succeed.

---

_Generated by /idea-feature-test-export | 2026-08-03_
