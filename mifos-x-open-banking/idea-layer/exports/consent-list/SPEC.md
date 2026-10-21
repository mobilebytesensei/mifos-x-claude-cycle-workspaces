# SPEC — Consent List

| Field         | Value                  |
|---------------|------------------------|
| Feature       | consent-list           |
| Flavor        | consumer               |
| Status        | approved               |
| Quality Score | 95                     |
| ViewModel     | ConsentListViewModel   |
| Archetype     | index_list             |

---

## Overview

Every consent this app knows about, split into **Active** and **History**. It is the customer's
answer to "which banks am I connected to, and what have I connected to before" — and the
destination the rest of the app routes to when a permission problem needs resolving.

The split is not cosmetic. In the HSBC sandbox a PSU can hold **only one active consent at a
time**, so the Active section is effectively a single card while History accumulates. Expired and
revoked consents are fetched deliberately rather than discarded, because a consent's history is
part of what PSD2 transparency requires the customer be able to see.

It carries a **fifth state, `ErrorAuth`**, distinct from `Error`. A generic failure offers Retry; an
auth failure offers Re-authenticate, because retrying an expired session gets the same refusal. The
two error states have different CTAs for that reason.

---

## Screens

| ID           | Name         | ViewModel            | Archetype  |
|--------------|--------------|----------------------|------------|
| consent-list | Consent List | ConsentListViewModel | index_list |

**Shell:** top app bar, title `{strings.consent_list_title}`, no leading icon. Bottom navigation
visible. No FAB.

---

## Components

| ID                        | Type        | Description                                            |
|---------------------------|-------------|---------------------------------------------------------|
| reconfirm_banner          | banner      | Prompts re-authorisation when a consent needs it        |
| active_section_label      | text        | "Active" section heading                                |
| active_consents_list      | list        | Live consents                                           |
| └ consent_card            | card        | One active consent — opens consent-detail               |
| &nbsp;&nbsp;└ consent_card_header_row | row | Bank identity + status                             |
| &nbsp;&nbsp;&nbsp;&nbsp;└ bank_logo | image | Bank mark                                            |
| &nbsp;&nbsp;&nbsp;&nbsp;└ status_chip | chip | `{item.Data.Status}`                                |
| &nbsp;&nbsp;└ reconfirm_urgency_chip | chip | Flags a consent needing reconfirmation             |
| &nbsp;&nbsp;└ permission_summary | text | What the consent grants, summarised                     |
| &nbsp;&nbsp;└ expiry_countdown | text  | Time remaining                                          |
| &nbsp;&nbsp;└ granted_since   | text  | When it was connected                                   |
| section_divider           | divider     |                                                         |
| history_section_label     | text        | "History" section heading                               |
| history_consents_list     | list        | Expired / revoked consents                              |
| └ history_consent_card    | card        | One past consent                                        |
| &nbsp;&nbsp;└ history_card_header_row | row | Bank identity + status                             |
| &nbsp;&nbsp;&nbsp;&nbsp;└ bank_logo_history | image | Bank mark                                      |
| &nbsp;&nbsp;&nbsp;&nbsp;└ history_status_chip | chip | `{item.Data.Status}`                         |
| &nbsp;&nbsp;└ history_expiry_label | text | When it lapsed                                     |
| &nbsp;&nbsp;└ history_connected_on | text | When it was connected                              |
| empty_state               | empty_state | No consents known at all                                |
| └ connect_button          | button      | → `LoginRenewRoute`                                     |
| error_state               | error_state | Generic load failure — Retry                            |
| └ retry_button            | button      | `RetryLoad`                                             |
| auth_error_state          | error_state | Session expired — Re-authenticate                       |
| └ reauth_button           | button      | → `LoginRenewRoute`                                     |

Two `error_state` components, not one styled two ways — they offer different recoveries and are
bound to different states.

---

## States

Initial state: `loading`. Five states, matching `ConsentListUiState` one-for-one.

| State      | Rendering                                       | Recovery         |
|------------|--------------------------------------------------|------------------|
| loading    | Fetching                                        | —                |
| content    | Active + History sections                       | —                |
| empty      | `empty_state` + Connect                         | connect a bank   |
| error      | `error_state` + Retry                           | retry            |
| error_auth | `auth_error_state` + Re-authenticate            | **re-auth**      |

---

## State Model

**ViewModel:** `ConsentListViewModel`.

**State:** `ConsentListState` — `consents: List<OBReadConsentResponse1>`, `uiState: ConsentListUiState`.

**Screen state:** sealed `ConsentListUiState` — `Loading`, `Content`, `Empty`, `Error`, `ErrorAuth`.

**Error types:** `NetworkError`, `TokenExpiredSession`, `ConsentStatusServerError`.

`TokenExpiredSession` is what lands `ErrorAuth`; the other two land `Error`.

**Actions:** `RetryLoad`.

**Nav callbacks**
- `onBack -> popBackStack()`
- `onNavigateToDetail(consentId) -> navigate(ConsentDetailRoute(consentId))`
- `onConnectBank -> navigate(LoginRenewRoute)`
- `onReauthenticate -> navigate(LoginRenewRoute)`

Connect and Re-authenticate both route to `LoginRenewRoute` — the login screen *without* the
onboarding intro. They are separate callbacks because they mean different things to the customer
even though they land in the same place.

**DI:** `ConsentDetailRepository`, `ConsentSession`.

---

## Navigation

| From         | To                        | Trigger                                 | Type |
|--------------|---------------------------|-----------------------------------------|------|
| consent-list | consent-detail            | `consent_card` tap                      | push |
| consent-list | login (`LoginRenewRoute`) | `connect_button` / `reauth_button`      | push |
| consent-list | (previous)                | `onBack`                                | pop  |

This screen is also an inbound destination from `beneficiaries`' error state, where a missing
`ReadBeneficiariesDetail` permission can only be fixed by re-consenting.

---

## API Endpoints

| ID             | Endpoint                                   | DTO             |
|----------------|--------------------------------------------|-----------------|
| consent-status | `GET /account-access-consents/{ConsentId}` | `ConsentSummary`|

Called **per locally-stored ConsentId** to refresh status. Full detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. Status chips follow the design
system's role mapping — `error` is reserved for Revoked/Rejected/Expired where access is actually
gone; an approaching expiry uses `tertiaryContainer` since the consent is still live. This design
system ships no `warning` role, so an amber treatment is unavailable by design. Components
reference semantic roles, so both theme modes resolve from `design-system/design-tokens.yaml`;
`DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/consent-list/{ui,api,flow,docs}.yaml. -->
