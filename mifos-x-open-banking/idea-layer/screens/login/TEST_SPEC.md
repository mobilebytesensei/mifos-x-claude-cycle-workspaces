# TEST SPEC — Login (Consent Onboarding)

| Field      | Value                       |
|------------|-----------------------------|
| Feature    | login                       |
| Source     | `screens/login/tests.yaml`  |
| Scenarios  | 8                           |
| Priorities | high 4 · medium 4           |
| States     | content 2 · error 2 · authorising 2 · loading 1 · empty 1 |
| Module     | `feature/login`             |

---

## Coverage

Contiguous ids, all five states exercised by at least one scenario. This screen is the AIS consent
front door — it creates the account-access consent and hands off to HSBC's FAPI authorisation
endpoint — so the scenarios track a handoff rather than a data render.

`login` renders more states than this file exercises (its `prompts/` and `preview/` sets include
`idle`, `authenticating`, `oauth_redirecting`, `oauth_exchanging`). Those two artifact sets
disagree with each other on this screen as well, which is tracked project-wide as
`PREVIEW-PROMPT-STATE-DIVERGENCE`; both derive from `ui.yaml#states[]`, so the question of which
states are canonical belongs there, not here. This spec covers what `tests.yaml` declares.

---

## The ordering guarantee this screen is built around

TC-LOGIN-005 and TC-LOGIN-008 bracket the consent-create call from both sides:

- **008** asserts the POST is *never sent* when the requested-permissions list resolves empty — a
  zero-scope consent would be rejected by HSBC with a 400, so the screen refuses to spend the
  round trip.
- **005** asserts that on success, `ConsentId`, OAuth `state` and `nonce` are all persisted
  *before* the redirect launches.

The 005 persistence order is the load-bearing one. The app-to-app redirect can kill this process;
if `state` and `nonce` are not durable before the jump, consent-callback has nothing to verify the
return against and the customer's authorisation is unrecoverable. It is the same invariant
payment-consent asserts from the other end (TC-PCON-004, "app restarted mid-flow").

---

## TC-LOGIN-001 — Content state renders all 10 OBIE read permissions and consent validity

**Priority:** high · **State:** content

- **Given** User navigated from the onboarding screen; permissions loaded from local constants
- **When** Screen mounts (`on_mount` completes synchronously)
- **Then**
  - 10 permission rows render, each with label and description
  - "Continue to HSBC" button visible and enabled
  - Consent validity note mentioning 90 days visible
  - HSBC explainer card visible with logo, badge, headline, body, and security notice
  - Formatted consent expiry label visible (e.g. "Expires 26 Sep 2026")
  - UK Open Banking regulated badge visible

Each of the 10 permissions must show its *description*, not just its OBIE name. `ReadTransactionsDetail`
is not informed consent; "see the detail of your transactions" is. This is a regulated disclosure
surface, which is also why the expiry date renders as a formatted date rather than "90 days".

---

## TC-LOGIN-002 — Loading state while consent-create POST is in flight

**Priority:** high · **State:** loading

- **Given** User has tapped "Continue to HSBC"; consent-create POST is in flight
- **When** `start_oauth` fires and the API call is pending
- **Then**
  - Linear progress indicator visible
  - "Connecting to HSBC…" label visible
  - Content components hidden (card, permissions list, CTAs not visible)

A **linear** indicator here, against the **circular** one in `authorising` (TC-LOGIN-006). The two
waits are different in kind — one is a request the app controls, the other is a handoff it does
not — and the indicator shape is the only signal distinguishing them.

---

## TC-LOGIN-003 — Error state on consent-create failure

**Priority:** high · **State:** error

- **Given** HSBC sandbox returns 500 on consent-create POST
- **When** `start_oauth` fires and the API returns 500
- **Then**
  - Error state renders with `error_outline` icon
  - "Could not connect to HSBC" title visible
  - Message "HSBC is temporarily unavailable. Try again in a moment." visible
  - "Try again" button visible and triggers `start_oauth`

---

## TC-LOGIN-004 — Cancel navigates back to onboarding

**Priority:** medium · **State:** content

- **Given** Login screen is in content state
- **When** User taps "Cancel"
- **Then** App navigates back to user-onboarding

---

## TC-LOGIN-005 — Successful consent-create stores ConsentId and transitions to authorising

**Priority:** high · **State:** authorising

- **Given** HSBC sandbox returns 201 with `ConsentId aac-fb2c4e8a-7d31-4c9e-9f2a-1b3c5d7e9f01`
- **When** `start_oauth` fires successfully and `redirect_to_bank_authorize` is called
- **Then**
  - `ConsentId` stored in local storage
  - OAuth `state` and `nonce` stored for callback verification
  - FAPI `/authorize` URL constructed and app-to-app redirect launched
  - Screen transitions to `authorising`

---

## TC-LOGIN-006 — Authorising state shows the correct holding UI after redirect launch

**Priority:** medium · **State:** authorising

- **Given** Consent-create succeeded and the FAPI redirect has launched to HSBC
- **When** `on_redirect_launched` fires
- **Then**
  - Circular progress indicator visible
  - "Opening HSBC…" label visible
  - Hint text instructing the user to complete sign-in in HSBC then return
  - Content components hidden (permissions list and CTAs not visible)

The hint text is the substantive assertion. This state can persist for as long as the customer
spends in another app, with no progress the app can observe — without an instruction it reads as
a hang.

---

## TC-LOGIN-007 — Network error surfaces the correct user-friendly message

**Priority:** medium · **State:** error

- **Given** Device has no internet connectivity
- **When** `start_oauth` fires and consent-create throws `NetworkException`
- **Then**
  - Error state renders with "Could not connect to HSBC" title
  - Body reads "Unable to reach HSBC. Check your connection and try again."
  - "Try again" button visible

Shares a title with TC-LOGIN-003 but differs in body — "HSBC is unavailable" and "check your
connection" point at different things to fix, and the shared title is what keeps the two from
reading as unrelated failures.

---

## TC-LOGIN-008 — Empty state blocks consent-create when no OBIE permissions are configured

**Priority:** medium · **State:** empty

- **Given** `ConsentOnboardingViewModel.loadPermissionsConfig()` resolves an empty `requested_permissions` list (zero OBIE scopes)
- **When** Screen mounts and `loadPermissionsConfig` completes with an empty result
- **Then**
  - Empty state renders with `manage_search` icon
  - "Connection required" title visible
  - Body explaining that no active HSBC connection was found
  - "Go back" button visible, navigates to user-onboarding
  - "Continue to HSBC" CTA **NOT** visible (`state_binding: content` only)
  - **Consent-create POST is NOT triggered** — a zero-scope consent would be rejected by HSBC 400

Both negatives are needed. Hiding the CTA prevents the customer from firing the doomed request;
asserting the POST is not sent prevents an on-mount code path from firing it anyway.

---

_Generated by /idea-feature-test-export | 2026-08-03_
