# SPEC — Account Holder

| Field         | Value                    |
|---------------|--------------------------|
| Feature       | account-holder           |
| Flavor        | consumer                 |
| Status        | approved                 |
| Quality Score | 96                       |
| ViewModel     | AccountHolderViewModel   |
| Archetype     | detail_screen            |

---

## Overview

Shows the single party OBIE links to an account — who legally holds it — reached from
account-detail's party chip. It is a read-only identity card plus an contact-details section.

The screen exists because `ReadParty` is a **separate consent permission**. A customer can hold a
live consent that reads balances and transactions and still be unable to read the account holder,
so "no party data" is not necessarily an error: a 403 maps to
`AccountHolderErrorKind.ConsentMissingParty`, which is a distinguishable outcome rather than a
generic failure.

---

## Screens

| ID             | Name           | ViewModel              | Entry point                        |
|----------------|----------------|------------------------|------------------------------------|
| account-holder | Account Holder | AccountHolderViewModel | account-detail, via `nav_chip_party` |

**Shell:** top app bar, title `{strings.account_holder.screen_title}`, `back` leading icon with an
accessibility label. Bottom navigation visible.

---

## Components

| ID                      | Type              | Description                                        |
|-------------------------|-------------------|-----------------------------------------------------|
| loading_indicator       | progress_circular | Loading state spinner                              |
| loading_caption         | text              | `{strings.account_holder.loading_caption}`         |
| identity_card           | card              | The holder's identity block                        |
| └ avatar                | avatar            | Holder avatar                                      |
| └ display_name          | text              | `{profile.displayName}`                            |
| └ role_label            | text              | `{profile.roleLabel}` — the party's role on the account |
| identity_section_header | section_header    | `{strings.account_holder.section_identity}`        |
| identity_section        | stack             | Contact details group                              |
| └ email_row             | list_item         | Email address                                      |
| └ mobile_row            | list_item         | Mobile number                                      |
| └ address_row           | list_item         | Postal address                                     |
| empty_state_view        | empty_state       | Party resolved but carries no detail               |
| error_state             | error_state       | Load failure — `role: alert`                       |
| └ retry_button          | button            | `{strings.account_holder.action_retry}` → `RetryLoad` |

---

## States

Initial state: `loading`. Four states, matching `AccountHolderUiState` one-for-one.

| State   | Rendering                                          |
|---------|-----------------------------------------------------|
| loading | `loading_indicator` + `loading_caption`             |
| content | Identity card + contact rows                        |
| empty   | `empty_state_view` — a party exists but has no detail |
| error   | `error_state` + retry                               |

`empty` and the `ConsentMissingParty` error are deliberately different outcomes: the first means
the bank returned a party with nothing on it, the second means the consent never permitted reading
one.

---

## State Model

**ViewModel:** `AccountHolderViewModel`.

**State:** `AccountHolderState` — `accountId: String`, `uiState: AccountHolderUiState`.

**Screen state:** sealed `AccountHolderUiState` — `Loading`, `Content`, `Empty`, `Error`.

**Error kinds**

| Kind                   | Cause                                          |
|------------------------|------------------------------------------------|
| `TokenExpired`         | 401 — PSU token expired; retriable             |
| `ConsentMissingParty`  | 403 — the active consent lacks `ReadParty`     |
| `ProfileNotFound`      | The account has no linked party                |
| `LoadFailed`           | Transport or unexpected failure                |

**Actions:** `RetryLoad`.

**DI:** `SavedStateHandle` (carries `accountId`), `ProfileRepository`.

---

## Navigation

| From           | To             | Trigger                       | Type |
|----------------|----------------|-------------------------------|------|
| account-detail | account-holder | `nav_chip_party` tap          | push |
| account-holder | account-detail | back                          | pop  |

A leaf screen — it has no forward navigation of its own.

---

## API Endpoints

| ID    | Endpoint                              | Schema          | Permission  |
|-------|---------------------------------------|-----------------|-------------|
| party | `GET /accounts/{AccountId}/party`     | `PartyResponse` | `ReadParty` |

Returns the single account holder linked to the account (`Data.Party`). The mapper flattens the
OBIE wire shape into the `PartyProfile` domain model. Full field and error detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. The avatar sits on
`primaryContainer`; contact rows use standard list-item roles. Components reference semantic roles,
so both theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the canonical
brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/account-holder/{ui,api,flow,docs}.yaml. -->
