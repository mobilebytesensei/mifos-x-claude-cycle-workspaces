# SPEC — Connected Apps

| Field         | Value                     |
|---------------|---------------------------|
| Feature       | consent-manager           |
| Flavor        | consumer                  |
| Status        | approved                  |
| Quality Score | 95                        |
| ViewModel     | ConsentManagerViewModel   |
| Archetype     | index_list                |

---

## Overview

The mirror image of `consent-list`. That screen shows consents **this app holds at banks**; this one
shows consents **third-party apps hold at this bank** — MoneyManager Pro, TaxHelper, BudgetWise —
and lets the customer revoke them.

Each card names the app, when access was granted and when it expires, a status badge, the specific
scopes granted, and the action available. The action differs by status and that distinction is the
screen's core idea:

- an **ACTIVE** consent offers **Revoke Access** — a destructive call behind a confirmation dialog
- an **EXPIRED** consent offers **Remove** — access is already gone, so this only clears the row

Offering "Revoke" on an expired consent would imply access is still live; offering "Remove" on an
active one would understate what the button does.

Scopes are rendered per consent rather than summarised, because "Read Accounts" and "View
Transactions" are materially different disclosures and the customer is being asked to judge them.

---

## Screens

| ID              | Name           | ViewModel               | Archetype  |
|-----------------|----------------|-------------------------|------------|
| consent-manager | Connected Apps | ConsentManagerViewModel | index_list |

**Shell:** top app bar shown, title "Connected Apps", `arrow_back` navigation icon →
`navigate_back`, with an `info_outlined` action opening the PSD2 consent-information sheet.

---

## Components

| ID                                   | Type   | Description                                        |
|--------------------------------------|--------|-----------------------------------------------------|
| consent_title                        | text   | "Connected Apps"                                   |
| consent_subtitle                     | text   | "Manage third-party apps that can access your data" |
| consent_moneymanager                 | box    | MoneyManager Pro card — opens the detail sheet     |
| └ moneymanager_header_row            | stack  | Header row                                         |
| &nbsp;&nbsp;└ moneymanager_logo      | image  | App logo                                           |
| &nbsp;&nbsp;└ moneymanager_info      | stack  | Name + dates                                       |
| &nbsp;&nbsp;&nbsp;&nbsp;└ moneymanager_name | text | "MoneyManager Pro"                          |
| &nbsp;&nbsp;&nbsp;&nbsp;└ moneymanager_dates | text | "Granted 1 Mar 2026 · Expires 1 Mar 2027"  |
| &nbsp;&nbsp;└ moneymanager_active_badge | box | "ACTIVE"                                          |
| └ moneymanager_scopes_row            | stack  | Granted scopes                                     |
| &nbsp;&nbsp;└ moneymanager_scope_read_accounts | box | "Read Accounts"                          |
| &nbsp;&nbsp;└ moneymanager_scope_view_transactions | box | "View Transactions"                  |
| &nbsp;&nbsp;└ moneymanager_scope_check_balances | box | "Check Balances"                        |
| └ moneymanager_revoke_button         | button | "Revoke Access"                                    |
| consent_taxhelper                    | box    | TaxHelper card (same structure, 2 scopes)          |
| consent_budgetwise                   | box    | BudgetWise card — **EXPIRED**                      |
| └ budgetwise_expired_badge           | box    | "EXPIRED"                                          |
| └ budgetwise_scope_check_balances    | box    | "Check Balances"                                   |
| └ budgetwise_remove_button           | button | "Remove" — not "Revoke"                            |
| revoke_confirm_dialog                | box    | Destructive confirmation overlay                   |
| └ revoke_dialog_title                | text   | "Revoke access?"                                   |
| └ revoke_dialog_body                 | text   | "This will immediately remove…"                    |
| └ revoke_dialog_actions              | stack  | Action row                                         |
| &nbsp;&nbsp;└ revoke_dialog_cancel_button | button | "Cancel" — dismiss, no side effect            |
| &nbsp;&nbsp;└ revoke_dialog_confirm_button | button | "Revoke"                                     |
| empty_state_icon                     | image  | No-connected-apps illustration                     |
| empty_state_title                    | text   | "No apps connected"                                |
| empty_state_body                     | text   | "Third-party apps you authorise will appear here"  |

The three app cards are demo instances of one repeating pattern — a real implementation renders one
card per `ConsentItem`, not three hardcoded blocks.

---

## States

Initial state: `loading`. Six states.

| State          | Meaning                                                  |
|----------------|-----------------------------------------------------------|
| loading        | Fetching connected apps                                  |
| content        | Cards rendered (canonical loaded state)                  |
| populated      | Loaded alias of `content`                                |
| empty          | No third-party apps connected                            |
| revoke_confirm | Dialog visible over the list — **nothing sent yet**      |
| error          | Load failed                                              |

`revoke_confirm` is a state rather than a local boolean so the pending target survives
recomposition — `pendingRevokeConsent` and `showRevokeDialog` are both in the ViewModel.

---

## State Model

**ViewModel:** `ConsentManagerViewModel`.

**State fields**

| Field                  | Type                     | Default      |
|------------------------|--------------------------|--------------|
| `consents`             | `List<ConsentItem>`      | `emptyList()`|
| `uiState`              | `ConsentManagerUiState`  | `Loading`    |
| `revokingConsentId`    | `String?`                | `null`       |
| `showRevokeDialog`     | `Boolean`                | `false`      |
| `pendingRevokeConsent` | `ConsentItem?`           | `null`       |
| `error`                | `UiError?`               | `null`       |

`revokingConsentId` is per-consent, so a revoke in flight affects one card rather than freezing the
whole list.

**Errors**

| Field  | Code           | Message                                            |
|--------|----------------|-----------------------------------------------------|
| global | `LOAD_FAILED`  | "Unable to load connected apps. Please try again."  |
| revoke | `REVOKE_FAILED`| "Could not revoke access. Please try again."        |

A failed revoke is scoped to the revoke action, not the screen — the list stays usable.

**Events:** `ConsentsLoaded`, `RevokeConsentClicked(consentId, appName)`,
`RevokeConsentConfirmed(consentId)`, `RevokeConsentCancelled`, `RevokeConsentComplete(consentId)`,
`RemoveExpiredConsentClicked(consentId)`, `RetryLoad`, `ConsentInfoOpened`.

`RevokeConsentClicked` carries `appName` as well as the id so the dialog can name the app the
customer is about to cut off.

**Actions:** `revoke_consent`, `confirm_revoke_consent`, `dismiss_revoke_dialog`,
`open_consent_info`, `view_consent_detail`.

**DI:** `ConsentRepository`.

---

## Navigation

| Action                   | Effect                                                        |
|--------------------------|----------------------------------------------------------------|
| `revoke_consent`         | Opens the confirmation dialog (`revoke_confirm` overlay)       |
| `confirm_revoke_consent` | DELETE, dismiss dialog, refresh list                           |
| `dismiss_revoke_dialog`  | Return to the loaded state, no side effect                     |
| `view_consent_detail`    | Opens the consent detail bottom sheet — an overlay, not a route |
| `open_consent_info`      | Opens the PSD2 consent-information sheet                       |

All five stay on this screen. `view_consent_detail` is a bottom sheet rather than a route change so
the list keeps its scroll position when dismissed.

---

## API Endpoints

| ID                 | Endpoint                                                          | Method |
|--------------------|-------------------------------------------------------------------|--------|
| obp_my_consents    | `/obp/v4.0.0/consumers/{consumerId}/consents`                     | GET    |
| obp_revoke_consent | `/obp/v4.0.0/consumers/{consumerId}/consents/{consentId}`         | DELETE |

Note these are **OBP consumer-scoped** endpoints, not the OBIE `account-access-consents` resource
used by `consent-list` / `consent-detail`. The two screens manage different objects. Full detail:
`API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. The ACTIVE badge uses
`primaryContainer` and EXPIRED uses `error` — per the design system, `error` is reserved for states
where access is actually gone. Scope pills use `secondaryContainer`: they are disclosures, not
statuses. Components reference semantic roles, so both theme modes resolve from
`design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/consent-manager/{ui,api,flow,docs}.yaml. -->
