# SPEC — Settings

| Field         | Value               |
|---------------|---------------------|
| Feature       | settings            |
| Flavor        | consumer            |
| Status        | approved            |
| Quality Score | 95                  |
| ViewModel     | SettingsViewModel   |
| Archetype     | settings            |

---

## Overview

A short preferences and about screen: theme selection, a route into consent management, and the
legal/version rows.

It is the app's only **local-preferences** surface — nothing here talks to a bank. `SettingsUiState`
has just three members and, notably, **no `Loading`**: preferences resolve from
`UserDataRepository` synchronously, so there is no fetch to wait on and the screen opens at
`content`.

The Consents row is the reason this screen sits in the account journey at all — it is the stable,
discoverable entry point to `consent-list`, which other screens reach only from error states.

---

## Screens

| ID       | Name     | ViewModel         | Archetype |
|----------|----------|-------------------|-----------|
| settings | Settings | SettingsViewModel | settings  |

**Shell:** top app bar, title `{strings.settings.title}`, **no leading icon** — a bottom-nav
destination, not a pushed screen. Bottom navigation visible.

---

## Components

| ID                 | Type           | Description                                       |
|--------------------|----------------|----------------------------------------------------|
| appearance_header  | section_header | Appearance section                                |
| theme_row          | select         | Theme selection — `SelectTheme`                   |
| account_header     | section_header | Account section                                   |
| consents_row       | list_item      | → consent-list                                    |
| about_header       | section_header | About section                                     |
| privacy_row        | list_item      | → privacy-policy                                  |
| licences_row       | list_item      | → licences                                        |
| app_version_row    | list_item      | App version, from `SettingsAppVersion`            |
| settings_empty     | empty_state    | Preferences unavailable                           |
| settings_error     | error_state    | Preferences failed to resolve — `role: alert`     |
| └ retry_button     | button         | `{strings.settings.error.retry}` → `RetryLoad`    |

`theme_row` is a `select`, not a navigation row — it opens a menu in place rather than pushing a
screen.

---

## States

Initial state: `content`. Three states, matching `SettingsUiState` one-for-one.

| State   | Rendering                                    |
|---------|-----------------------------------------------|
| content | All sections and rows                        |
| empty   | `settings_empty` — preferences unavailable   |
| error   | `settings_error` + retry                     |

**There is no `loading` state**, and that is correct: preferences come from local storage, not a
network call. Adding one would introduce a flash of empty chrome on every open for a read that has
already completed.

---

## State Model

**ViewModel:** `SettingsViewModel`.

**State:** `SettingsState` — `uiState: SettingsUiState`.

**Screen state:** sealed `SettingsUiState` — `Content`, `Empty`, `Error`.

**Error kinds:** `SettingsErrorKind.PreferencesUnavailable`, `SettingsErrorKind.Unknown`.

**Actions:** `SelectTheme`, `ToggleThemeMenu`, `DismissThemeMenu`, `RetryLoad`.

Three of the four actions serve the theme menu — open, dismiss, choose — because the menu's
visibility is ViewModel state rather than local composable state, so it survives recomposition.

**DI:** `UserDataRepository`, `SettingsAppVersion`.

---

## Navigation

| From     | To             | Trigger         | Type |
|----------|----------------|-----------------|------|
| settings | consent-list   | `consents_row`  | push |
| settings | privacy-policy | `privacy_row`   | push |
| settings | licences       | `licences_row`  | push |

`app_version_row` is display-only. Settings is reached via the bottom nav rather than a screen edge,
which is why orphan-route checks must count app-shell reachability and not nav edges alone.

---

## API Endpoints

**None.** `api.yaml` declares no operations — every value on this screen is local. Theme comes from
`UserDataRepository`, the version string from `SettingsAppVersion`, and the three navigation rows
carry no data of their own.

That is also why the error state is `PreferencesUnavailable` rather than a network error: the only
way this screen fails is if local preference storage cannot be read.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. Section headers use
`onSurfaceVariant` and rows the standard list-item roles. The theme selector is the one control that
changes token resolution itself — picking dark re-resolves every role through the dark scheme
declared in `design-system/design-tokens.yaml`. `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/settings/{ui,flow,docs}.yaml. No API.md — the feature declares no api[] operations. -->
