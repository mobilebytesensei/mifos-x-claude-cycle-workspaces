# SPEC — HSBC Connection Detail

| Field         | Value                    |
|---------------|--------------------------|
| Feature       | consent-detail           |
| Flavor        | consumer                 |
| Status        | approved                 |
| Quality Score | 95                       |
| ViewModel     | ConsentDetailViewModel   |
| Archetype     | detail_screen            |

---

## Overview

One consent in full: its status, the dates that bound it, the permissions it grants, and the two
things a customer can do about it — reconfirm or revoke.

The screen is the PSD2 transparency surface. Everything on it exists so the customer can answer
"what did I agree to, until when, and how do I stop it" without leaving the app.

Revocation is modelled as **two states, not a boolean**: `RevokeConfirm` (dialog up, nothing sent)
and `Revoking` (DELETE in flight). Separating them means the confirm dialog can be dismissed with
no side effect, and the in-flight period has its own progress affordance — revoking access is
destructive and irreversible from the app's side, so it is deliberately not a single tap.

`Reconfirm` routes to `LoginRenewRoute` — the same login screen reached *without* the onboarding
intro. Re-authorising is a fresh FAPI journey, not an in-place refresh.

---

## Screens

| ID             | Name                   | ViewModel              | Archetype     |
|----------------|------------------------|------------------------|---------------|
| consent-detail | HSBC Connection Detail | ConsentDetailViewModel | detail_screen |

**Shell:** top app bar, title `{strings.consent_detail.top_bar_title}`, `back` leading icon. Bottom
navigation visible. No FAB.

---

## Components

| ID                      | Type              | Description                                             |
|-------------------------|-------------------|----------------------------------------------------------|
| load_progress           | progress_circular | Initial load                                            |
| revoke_progress         | progress_circular | `Revoking` — DELETE in flight                           |
| status_header_card      | card              | Identity + status block                                 |
| └ bank_identity_row     | row               | Bank identity                                           |
| &nbsp;&nbsp;└ bank_logo | image             | HSBC mark                                               |
| &nbsp;&nbsp;└ status_chip | chip            | `{consent.Data.Status}`                                 |
| └ consent_id_label      | text              | The ConsentId — the customer's reference                |
| expiry_warning_banner   | card              | Shown as expiry approaches                              |
| └ expiry_warning_row    | row               |                                                         |
| &nbsp;&nbsp;└ expiry_warning_icon | icon    | Warning glyph                                           |
| &nbsp;&nbsp;└ expiry_warning_text | text    | Expiry advisory                                         |
| dates_header            | section_header    | Dates section                                           |
| dates_list              | list              | The four bounding dates                                 |
| └ created_date_row      | list_item         | When consent was granted                                |
| └ expiry_date_row       | list_item         | When it lapses                                          |
| └ transaction_from_row  | list_item         | `TransactionFromDateTime` — history window start        |
| └ transaction_to_row    | list_item         | `TransactionToDateTime` — history window end            |
| reconfirm_button        | button            | → `LoginRenewRoute`                                     |
| permissions_header      | section_header    | Permissions section                                     |
| permissions_list        | list              | One row per granted OBIE permission                     |
| └ permission_row        | list_item         | Human-readable permission                               |
| revoke_button           | button            | Opens the confirm dialog                                |
| revoke_confirm_dialog   | dialog            | Destructive confirmation                                |
| └ dialog_cancel_button  | button            | Dismiss — no side effect                                |
| └ dialog_confirm_button | button            | `ExecuteRevoke`                                         |
| error_state             | error_state       | Load failure — `role: alert`                            |
| └ retry_button          | button            | `RetryLoad`                                             |
| empty_state             | empty_state       | Consent resolved with nothing to show                   |
| └ empty_go_back_button  | button            | Return to the consent list                              |

The four date rows matter as a set: `transaction_from`/`transaction_to` define **how far back** the
consent lets a TPP read, which is a different question from when the consent expires, and OBIE
requires both be disclosed.

---

## States

Initial state: `loading`. Six states, matching `ConsentDetailUiState` one-for-one.

| State           | Meaning                                                    |
|-----------------|-------------------------------------------------------------|
| loading         | Fetching the consent resource                              |
| content         | Status, dates, permissions, both CTAs                      |
| revoke_confirm  | Dialog visible — **nothing sent yet**                      |
| revoking        | DELETE in flight — `revoke_progress`                       |
| empty           | Consent resolved but carries nothing renderable            |
| error           | Load failed — retry offered                                |

---

## State Model

**ViewModel:** `ConsentDetailViewModel`.

**State:** `ConsentDetailState` — `consentId: String`, `uiState: ConsentDetailUiState`.

**Screen state:** sealed `ConsentDetailUiState` — `Loading`, `Content`, `RevokeConfirm`,
`Revoking`, `Empty`, `Error`.

**Error types:** `ConsentNotFoundError`, `ConsentRevokedError`, `ConsentExpiredError`,
`TokenExpiredError`, `NetworkError`, `RevokeServerError`.

`RevokeServerError` is separate from `NetworkError` on purpose — a failed revoke is more serious
than a failed read, because the customer believes they have withdrawn access.

**Actions:** `RetryLoad`, `ConfirmRevoke`, `DismissRevokeConfirm`, `ExecuteRevoke`.

Four actions for revocation, not one: open, dismiss, execute, and the reload that follows.

**Nav callbacks**
- `onBack -> popBackStack()`
- `onReconfirm -> navigate(LoginRenewRoute)` — re-runs authorisation on the login screen
- `onLoggedOut` — bubbles to the root navigator, which returns the user to onboarding

**DI:** `SavedStateHandle` (carries `consentId`), `ConsentDetailRepository`, `AppLogout`.

`AppLogout` is injected because revoking the *active* consent ends the session — there is nothing
left to authorise reads with, so the app must log out rather than sit on a dead token.

---

## Navigation

| From           | To                          | Trigger              | Type    |
|----------------|-----------------------------|----------------------|---------|
| consent-detail | login (`LoginRenewRoute`)   | `reconfirm_button`   | push    |
| consent-detail | (previous)                  | `onBack`             | pop     |
| consent-detail | onboarding                  | `onLoggedOut` after revoking the active consent | root reset |

---

## API Endpoints

| ID             | Endpoint                                        | Method | Auth                |
|----------------|-------------------------------------------------|--------|---------------------|
| consent-status | `/account-access-consents/{ConsentId}`          | GET    | client_credentials  |
| consent-revoke | `/account-access-consents/{ConsentId}`          | DELETE | client_credentials  |

Full detail including the 204/404 handling and local-token cleanup: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. Status uses the design system's
role set — `error` is reserved for Revoked/Rejected/Expired where access is actually gone, while
an approaching expiry uses `tertiaryContainer`, since the consent is still live. There is no
`warning` role in this design system, so an amber treatment is not available and must not be
improvised. Components reference semantic roles, so both theme modes resolve from
`design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/consent-detail/{ui,api,flow,docs}.yaml. -->
