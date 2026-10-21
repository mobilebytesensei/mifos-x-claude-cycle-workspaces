# SPEC — Beneficiaries

| Field         | Value                     |
|---------------|---------------------------|
| Feature       | beneficiaries             |
| Flavor        | consumer                  |
| Status        | approved                  |
| Quality Score | 95                        |
| ViewModel     | BeneficiariesViewModel    |
| Archetype     | index_list                |

---

## Overview

The saved payees authorised under the PSU consent for one account, reached from account-detail.
A search bar filters the loaded list; rows are read-only — this screen lists payees, it does not
create or edit them.

Its distinguishing design decision is in the error state: alongside Retry it offers **View
Consents**. Most failures here are consent failures rather than transport failures — the payee list
needs `ReadBeneficiariesDetail` in the active consent, and if that permission was never granted or
has been revoked, retrying cannot help. The second CTA routes to `consent-list` where the customer
can actually resolve it.

Two empty states exist and they are not interchangeable: `empty_beneficiaries` means the account has
no saved payees, `search_no_results` means the filter matched none of the payees that do exist.

---

## Screens

| ID            | Name          | ViewModel              | Archetype  | Entry point    |
|---------------|---------------|------------------------|------------|----------------|
| beneficiaries | Beneficiaries | BeneficiariesViewModel | index_list | account-detail |

**Shell:** top app bar, title `{strings.beneficiaries.screen_title}`, `back` leading icon. Bottom
navigation visible. No FAB — no create path exists.

---

## Components

| ID                   | Type        | Description                                             |
|----------------------|-------------|----------------------------------------------------------|
| back_button          | icon_button | Returns to account-detail                               |
| beneficiary_search   | search_bar  | Filters the loaded list — no refetch                    |
| beneficiaries_list   | list        | Semantic list of saved payees                           |
| └ beneficiary_row    | list_item   | One payee                                               |
| └ beneficiary_avatar | avatar      | Payee initial/avatar                                    |
| search_no_results    | empty_state | Filter matched nothing — payees exist                   |
| empty_beneficiaries  | empty_state | Account has no saved payees at all                      |
| error_state          | error_state | Load failure — `role: alert`                            |
| └ retry_button       | button      | `{strings.beneficiaries.retry}` → `RetryLoad`           |
| └ view_consents_button | button    | `{strings.beneficiaries.view_consents}` → consent-list  |

---

## States

Initial state: `loading`. Four states, matching `BeneficiariesUiState` one-for-one.

| State   | Rendering                                                       |
|---------|------------------------------------------------------------------|
| loading | Fetching                                                        |
| content | Search bar + payee rows (or `search_no_results` when filtered)   |
| empty   | `empty_beneficiaries` — no saved payees                         |
| error   | `error_state` + Retry + View Consents                           |

`search_no_results` renders **within** `content` — a filter that matches nothing has not emptied
the account, so the search bar must stay on screen for the customer to clear it.

---

## State Model

**ViewModel:** `BeneficiariesViewModel`.

**State:** `BeneficiariesState` — `accountId: String`, `uiState: BeneficiariesUiState`.

**Screen state:** sealed `BeneficiariesUiState` — `Loading`, `Content`, `Empty`, `Error`.

**Error types:** `TokenExpiredError`, `ConsentRevokedError`, `RateLimitedError`, `NetworkError`,
`ServerError`.

`ConsentRevokedError` is why the error state carries a second CTA — it is not recoverable by retry.

**Actions:** `RetryLoad`, `Search`.

**Nav callbacks:** `onBack -> popBackStack()` returning to account-detail ·
`onNavigateToConsents -> navigate(ConsentListRoute)`.

**DI:** `SavedStateHandle` (carries `accountId`), `BeneficiariesRepository`.

---

## Navigation

| From          | To             | Trigger                 | Type |
|---------------|----------------|-------------------------|------|
| beneficiaries | consent-list   | `view_consents_button`  | push |
| beneficiaries | account-detail | `onBack`                | pop  |

The consent-list route from an error state is unusual and deliberate: it turns a dead end into a
path to the actual fix.

---

## API Endpoints

| ID                 | Endpoint                                    | DTO               | Permission                   |
|--------------------|---------------------------------------------|-------------------|------------------------------|
| beneficiaries-list | `GET /accounts/{AccountId}/beneficiaries`   | `BeneficiaryItem` | `ReadBeneficiariesDetail`    |

Full detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. Avatars sit on
`primaryContainer`; the search bar uses the M3 `search_bar` surface role. Components reference
semantic roles, so both theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is
the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/beneficiaries/{ui,api,flow,docs}.yaml. -->
