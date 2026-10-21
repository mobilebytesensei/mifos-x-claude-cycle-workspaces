# SPEC — About

| Field         | Value          |
|---------------|----------------|
| Feature       | about          |
| Flavor        | shared         |
| Status        | enriched       |
| Quality Score | 95             |
| ViewModel     | AboutViewModel |

---

## Overview

The About screen is a shared-flavor informational screen accessible from any persona's Settings or Profile flow. It provides app identity (Mifos X Open Banking logo — 80×80dp, tinted #4C662B; app name "Mifos X Open Banking" in headline_small #4C662B; tagline "Open Banking for Everyone" in body_medium #44483D), build provenance (Version 1.0.0 / Build 2026.05.001 drawn from `BuildConfig.VERSION_NAME` / `BuildConfig.VERSION_CODE`), and legal navigation links (Terms of Service → open_external, Privacy Policy → open_external, Open Source Licenses → push). An outlined "Rate This App" button at the bottom triggers the Google Play / AppStore in-app review flow via the `ReviewManager` API. A top app bar with back arrow provides the only navigation chrome — no bottom navigation bar is shown. The screen has four states: `loading` (shimmer skeleton while `BuildConfig` resolves — 200ms, 3 skeleton items); `content` (full layout); `empty` (logo + Legal card always visible, App Info card and Rate App button hidden when version data unavailable); and `error` (centered `info_outline` icon + message when version-info retrieval fails entirely). No OBP backend API calls are made — all data is sourced from `BuildConfig` at compile time.

---

## Screens

| ID    | Name  | Route   | Layout | Scroll   |
|-------|-------|---------|--------|----------|
| about | About | /about  | Column | Vertical |

**Shell:** Top app bar with back arrow ("About" title, `navigation_icon: arrow_back`). No bottom navigation bar.

| Shell Element  | ID             | Configuration                                   |
|----------------|----------------|-------------------------------------------------|
| top_app_bar    | —              | title "About", navigation_icon `arrow_back`, navigate_back action |
| bottom_nav     | —              | hidden (false)                                  |

---

## Components

| ID                     | Type     | Description                                                                                                    |
|------------------------|----------|----------------------------------------------------------------------------------------------------------------|
| about_root             | stack    | Root column — background #F9FAEF, padding spacing.lg (24dp)                                                   |
| about_logo_section     | stack    | Centered column — padding_top + padding_bottom spacing.xl (32dp); children: logo, app name, tagline            |
| about_logo_image       | image    | `mifos_logo` asset — 80×80dp, tint #4C662B, centered; a11y label "Mifos X Open Banking logo"                  |
| about_app_name_text    | text     | "Mifos X Open Banking" — Outfit/headline_small (24sp/600), color #4C662B, centered, heading role               |
| about_tagline_text     | text     | "Open Banking for Everyone" — Outfit/body_medium (14sp/400), color #44483D, centered                          |
| about_app_info_card    | card     | filled, #FFFFFF, radius 12dp, padding 16dp, margin_bottom 16dp — wraps version + build rows                    |
| about_version_row      | stack    | Row, space-between, padding_top + padding_bottom 8dp                                                          |
| about_version_label    | text     | "Version" — Outfit/body_large (16sp/400), color #1A1C16                                                       |
| about_version_value    | text     | "1.0.0" — Outfit/body_medium (14sp/400), color #44483D; data_driven: BuildConfig.VERSION_NAME                 |
| about_divider_1        | divider  | color #E1E4D5, margin_top + margin_bottom 4dp — separates Version and Build rows                              |
| about_build_row        | stack    | Row, space-between, padding_top + padding_bottom 8dp                                                          |
| about_build_label      | text     | "Build" — Outfit/body_large (16sp/400), color #1A1C16                                                         |
| about_build_value      | text     | "2026.05.001" — Outfit/body_medium (14sp/400), color #44483D; data_driven: BuildConfig.VERSION_CODE           |
| about_legal_card       | card     | filled, #FFFFFF, radius 12dp, padding 16dp, margin_bottom 16dp — wraps Legal header + 3 link rows             |
| about_legal_header     | text     | "Legal" — Outfit/title_medium (16sp/500), color #4C662B, padding_bottom 8dp; heading role                     |
| about_tos_row          | stack    | Row, space-between, padding_top + padding_bottom 8dp                                                          |
| about_tos_link         | link     | "Terms of Service" — Outfit/body_large, color #1A1C16, inline; `open_external → terms-of-service`             |
| about_tos_chevron      | icon     | `open_in_new` — #C5C8BA, 18dp; decorative (empty a11y label)                                                  |
| about_divider_2        | divider  | color #E1E4D5, margin_top + margin_bottom 4dp — separates Terms of Service and Privacy Policy rows             |
| about_privacy_row      | stack    | Row, space-between, padding_top + padding_bottom 8dp                                                          |
| about_privacy_link     | link     | "Privacy Policy" — Outfit/body_large, color #1A1C16, inline; `open_external → privacy-policy`                 |
| about_privacy_chevron  | icon     | `open_in_new` — #C5C8BA, 18dp; decorative                                                                     |
| about_divider_3        | divider  | color #E1E4D5, margin_top + margin_bottom 4dp — separates Privacy Policy and Open Source Licenses rows         |
| about_licenses_row     | stack    | Row, space-between, padding_top + padding_bottom 8dp                                                          |
| about_licenses_link    | link     | "Open Source Licences" — Outfit/body_large, color #1A1C16, inline; `push → licences`                          |
| about_licenses_chevron | icon     | `chevron_right` — #C5C8BA, 20dp; decorative                                                                   |
| about_rate_button      | button   | "Rate This App" — outlined, border + text #4C662B, Outfit/label_large (14sp/500), padding_horizontal 32dp, centered, margin_top 24dp; `rate_app` action via ReviewManager API |
| about_loading_skeleton | skeleton | settings variant — background #F9FAEF, padding 24dp; shimmer_duration short4 (200ms), reduced_motion: static_placeholder; 3 items; a11y "Loading app information" |
| about_error_state      | stack    | Centered column, padding 32dp; children: error icon + error message                                           |
| about_error_icon       | icon     | `info_outline` — #BA1A1A (error), 48dp, centered, padding_bottom 16dp                                         |
| about_error_message    | text     | "Unable to load app information. Please restart the app." — Outfit/body_medium, #44483D, centered             |

---

## States

| ID      | Trigger                                                    | Description                                                                                               |
|---------|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| loading | Screen entry — cold start while BuildConfig values resolve | Shows `about_loading_skeleton` (settings variant, 3 skeleton items); shimmer 200ms; static fallback on reduced motion; no interactive elements |
| content | BuildConfig values resolved successfully                   | Full layout: `about_logo_section` + `about_app_info_card` (version + build rows) + `about_legal_card` (3 links) + `about_rate_button` |
| empty   | Version data unavailable (partial build metadata)          | Logo section + Legal card visible; App Info card and Rate App button hidden; legal navigation always accessible |
| error   | Version-info retrieval fails (corrupted build metadata)    | Centered `about_error_state`: `info_outline` icon (#BA1A1A, 48dp) + "Unable to load app information. Please restart the app."; no retry button |

---

## State Model

**ViewModel:** `AboutViewModel`
**Screen State Type:** `AboutUiState`

| Field       | Type   | Default          | Source                              |
|-------------|--------|------------------|-------------------------------------|
| appVersion  | String | `"1.0.0"`        | `BuildConfig.VERSION_NAME`          |
| buildNumber | String | `"2026.05.001"`  | `BuildConfig.VERSION_CODE` (stamp)  |

**Events:** `OnRateAppClicked`, `OnTermsClicked`, `OnPrivacyClicked`, `OnLicensesClicked`

**Actions:** `onRateAppClicked()`, `onTermsClicked()`, `onPrivacyClicked()`, `onLicensesClicked()`

**DI Dependencies:** `AppInfoProvider`, `ReviewManager`

**Errors:**
- No network errors — all data from `BuildConfig`. `AppInfoProvider` read failures surface as `error` state (no retry button — user prompted to restart the app).

---

## Navigation

| From  | To                      | Trigger                           | Type     |
|-------|-------------------------|-----------------------------------|----------|
| about | terms-of-service        | `about_tos_link` tap              | external |
| about | privacy-policy          | `about_privacy_link` tap          | external |
| about | licences                | `about_licenses_link` tap         | push     |
| about | (previous screen)       | Top app bar `arrow_back` tap      | pop      |
| about | (Play Store / App Store)| `about_rate_button` tap           | system   |

---

## API Endpoints

No backend API dependencies — static content screen. All data (`appVersion`, `buildNumber`) is sourced from `BuildConfig` at compile time via `AppInfoProvider`. The `ReviewManager` integration for "Rate This App" is a platform system API (Google Play In-App Review / Apple StoreKit) and makes no OBP calls.

---

## Design Tokens

| Token                           | Value         | Usage                                                                                     |
|---------------------------------|---------------|-------------------------------------------------------------------------------------------|
| colors.light.primary            | #4C662B       | Logo tint, app name text (#4C662B), "Legal" section header, rate button border + text, back-arrow |
| colors.light.background         | #F9FAEF       | Screen background (`about_root`), skeleton background                                     |
| colors.light.surface            | #FFFFFF       | App Info card fill, Legal card fill                                                       |
| colors.light.on_surface         | #1A1C16       | Version/Build label text, ToS / Privacy / Licenses link text                              |
| colors.light.on_surface_variant | #44483D       | Tagline text, version value, build value, error message                                   |
| colors.light.surface_variant    | #E1E4D5       | Divider color (about_divider_1/2/3)                                                       |
| colors.light.outline_variant    | #C5C8BA       | Chevron icon color (`open_in_new` + `chevron_right` trailing icons)                       |
| colors.light.error              | #BA1A1A       | Error state icon color                                                                    |
| typography.headline_small       | Outfit 24sp/600 | App name text (`about_app_name_text`)                                                   |
| typography.title_medium         | Outfit 16sp/500 | "Legal" section header                                                                  |
| typography.body_large           | Outfit 16sp/400 | Version label, Build label, ToS / Privacy / Licenses link labels                       |
| typography.body_medium          | Outfit 14sp/400 | Tagline, version value, build value, error message                                      |
| typography.label_large          | Outfit 14sp/500 | Rate App button label                                                                   |
| spacing.xs                      | 4dp           | Divider vertical margins (about_divider_1/2/3)                                            |
| spacing.sm                      | 8dp           | Row internal padding (version/build/link rows — padding_top + padding_bottom)             |
| spacing.md                      | 16dp          | Card padding, card margin_bottom, Legal header bottom padding                             |
| spacing.lg                      | 24dp          | Root screen padding, rate button top margin                                               |
| spacing.xl                      | 32dp          | Logo section top/bottom padding, rate button horizontal padding, error state padding      |
| radius.md                       | 12dp          | App Info card + Legal card border radius                                                  |
| motion.duration.short4          | 200ms         | Loading skeleton shimmer duration                                                         |
| touchTargets.min_touch_target   | 48dp          | Minimum for all link rows and rate button                                                 |

---

_Generated by /idea export | 2026-05-30_
