# SPEC — User Profile

| Field         | Value             |
|---------------|-------------------|
| Feature       | profile           |
| Flavor        | consumer          |
| Status        | approved          |
| Quality Score | 99                |
| ViewModel     | ProfileViewModel  |
| Archetype     | profile           |

---

## Overview

A **read-only** account screen: avatar initials, display name, and three disabled fields showing
the identity OBP holds for the signed-in user. There is no editing, no save, and no avatar upload —
the pencil glyph and the Change Password button are both present but inert, the latter explicitly
`enabled: false` until a change-password screen ships.

Logout is the one live action and it is **reactive**: `onLogout()` sets
`UserDataRepository.setIsAuthenticated(false)` and `RootNavViewModel`, observing `userData`, routes
to the auth graph. The screen does not navigate itself.

Two content fields are worth knowing before implementing against this: `displayName` falls back to
the email local-part when `username` is blank, and `phone` is hardcoded `""` because OBP's
UserProfile carries no phone field — the row renders, permanently empty.

---

## Screens

| ID      | Name    | ViewModel        | Archetype |
|---------|---------|------------------|-----------|
| profile | Profile | ProfileViewModel | profile   |

---

## Components

| ID                            | Type              | Description                                                        |
|-------------------------------|-------------------|--------------------------------------------------------------------|
| profile_root                  | stack             | Column, `spacing.lg` padding — the state container                  |
| profile_avatar_section        | stack             | Avatar block                                                        |
| profile_avatar_initials       | box               | Up to two uppercase initials from `displayName` (`initialsOf`)      |
| profile_avatar_edit_icon      | icon              | `edit` glyph — decorative; no upload path exists                    |
| profile_display_name          | text              | `displayName`                                                       |
| profile_form_section          | stack             | Personal Information block                                          |
| profile_section_header        | text              | "Personal Information"                                              |
| profile_full_name_field       | input             | Full Name — **disabled**, bound to `fullName`, not focusable         |
| profile_email_field           | input             | Email Address — **disabled**, bound to `email`, not focusable        |
| profile_phone_field           | input             | Phone Number — **disabled**, bound to `phone` (always blank)         |
| profile_change_password_button| button            | `enabled: false` until the change-password screen ships; not focusable while disabled |
| profile_logout_button         | button            | The only live affordance — `onLogout()`                             |
| profile_error_icon            | icon              | `error_outline` (error state)                                       |
| profile_error_title           | text              | "Could not load your profile"                                       |
| profile_error_body            | text              | "Check your connection and try again."                              |
| profile_error_retry_button    | button            | Retry → `onRetry()`                                                 |
| profile_loading_spinner       | loading_indicator | `spinner` variant (loading state)                                   |

The three disabled inputs and the disabled button declare `focusable: false` — a permanently
disabled control must not sit in the tab order.

---

## States

Initial state: `loading`. Three states, matching `ScreenState<ProfileContent>` exactly.

| State   | Layout                                           | Rendering                                    |
|---------|--------------------------------------------------|----------------------------------------------|
| loading | column, `spacing.lg`, centred both axes          | `profile_loading_spinner`                    |
| content | column, `spacing.lg`                             | Avatar block + Personal Information + buttons |
| error   | column, `spacing.lg`, centred both axes          | icon + title + body + Retry                  |

There is no `empty` state: a signed-in user always has a profile, so an empty result is an error,
not an empty set.

---

## State Model

**ViewModel:** `ProfileViewModel`, extending `androidx.lifecycle.ViewModel`, exposing
`StateFlow<ScreenState<ProfileContent>>`.

**Wrapper variants:** `Loading` · `Content(ProfileContent, DataFreshness)` · `Error(throwable, isNetworkError)`.

**Content fields**

| Field         | Type   | Note                                                        |
|---------------|--------|-------------------------------------------------------------|
| `displayName` | String | `username`, or the email local-part when username is blank  |
| `initials`    | String | Up to two uppercase initials from `displayName`             |
| `fullName`    | String | Same as `displayName` in shipped — bound to the read-only Full Name field |
| `email`       | String |                                                             |
| `phone`       | String | Hardcoded `""` — OBP UserProfile has no phone field         |

**Actions**
- `onRetry()` — reloads via `load()`
- `onLogout()` — `UserDataRepository.setIsAuthenticated(false)`; routing is reactive via `RootNavViewModel`

**DI:** `ProfileRepository`, `UserDataRepository`.

---

## Navigation

| From    | To    | Trigger                                            | Type    |
|---------|-------|----------------------------------------------------|---------|
| profile | login | `onLogout()` → auth-state change observed by RootNavViewModel | reactive |

Flows: `app-main`, `consumer-banking`. Journey: `consumer-profile-settings`.

The transition is not a NavController call from this screen — the screen only flips auth state, and
the root nav graph reacts. Nothing else navigates away from here.

---

## API Endpoints

| ID                     | Endpoint                        | Trigger          | Wired |
|------------------------|---------------------------------|------------------|-------|
| obp_get_user_profile   | `GET /obp/v4.0.0/users/current` | `on_screen_load` | yes   |
| obp_update_user_profile| `PUT /obp/v4.0.0/users/current` | `deferred`       | **no** |

The PUT is declared but deferred — it is the endpoint an editable profile would need, and it is why
the screen is described as read-only rather than as missing a feature.

Full field and error detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. Disabled fields use the M3
disabled container/content roles rather than a bespoke grey; the avatar initials sit on
`primaryContainer`. Components reference semantic roles, so both theme modes resolve from
`design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/profile/{ui,api,flow,docs}.yaml. -->
