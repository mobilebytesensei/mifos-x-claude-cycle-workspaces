# TEST SPEC — About

| Field      | Value                              |
|------------|------------------------------------|
| Feature    | about                              |
| Source     | `screens/about/tests.yaml`         |
| Scenarios  | 14                                 |
| Priorities | high 8 · medium 5 · low 1          |
| States     | content 14                         |
| Module     | _none yet — spec-only feature_     |

> No `AboutScreen.kt` exists in source. These scenarios are **forward specs** derived from the
> feature's own idea-layer siblings, not reverse-synced from a shipped suite — unlike
> `account-holder` or `licences`, whose specs describe tests that already run.

---

## Coverage

| State   | Scenarios | Covered |
|---------|-----------|---------|
| content | 14 | TC-ABOUT-001 … -014 |

Single-state coverage is correct rather than a gap. TC-ABOUT-012 pins the reason:
`state_model` is `static_content` — no ViewModel, no DI, no repository, no events — so there is
no loading, empty or error state to reach. TC-ABOUT-001 asserts that absence directly.

Four of the fourteen scenarios (TC-ABOUT-004, -010, -012, -014) assert what the screen **does
not** do. That ratio is deliberate for a static screen: with no state machine to exercise, the
regressions worth catching are additions — an invented build-number row, an in-app web view, a
rate-this-app button, a navigation edge that belongs to Settings.

---

## TC-ABOUT-001 — Content state renders all five sections

**Priority:** high · **State:** content

- **Given** `AboutScreen` composed with the default `appVersion` `1.0.0`
- **When** Screen renders
- **Then**
  - Top app bar shows "About" with an `arrow_back` navigation icon; no bottom nav
  - `about_logo_section`, `about_app_info_card`, `about_project_card`, `about_legal_card` and `about_attribution` all visible
  - Content is the only declared state — there is no loading, empty or error state to reach

---

## TC-ABOUT-002 — Identity block renders logo, name, tagline and inline version

**Priority:** high · **State:** content

- **Given** Content state
- **When** `about_logo_section` renders
- **Then**
  - `about_logo_image` visible as an 80dp `account_balance` mark tinted `primary`
  - `about_app_name_text` "Mifos X Open Banking" visible as a heading
  - `about_tagline_text` "Open Banking for Everyone" visible
  - `about_version_inline` shows "Version 1.0.0"

---

## TC-ABOUT-003 — Version is bound to the host-supplied parameter, not hardcoded

**Priority:** high · **State:** content

- **Given** `AboutScreen` is composed with `appVersion = "2.4.1"`
- **When** The version surfaces render
- **Then**
  - `about_version_inline` shows "Version 2.4.1"
  - `about_version_value` in the app-info card shows "2.4.1"
  - Neither surface still reads `1.0.0`

The screen renders the version in **two** places, so the third assertion is what makes this test
worth writing — a binding fix applied to one surface and missed on the other leaves the app
reporting two different versions of itself.

---

## TC-ABOUT-004 — App info card lists exactly version, license and platform

**Priority:** high · **State:** content

- **Given** Content state
- **When** `about_app_info_card` renders
- **Then**
  - `about_app_info_header` "App" visible as a heading
  - `about_version_row`, `about_license_row` and `about_platform_row` visible, separated by dividers
  - `about_license_value` reads "MPL-2.0"
  - `about_platform_value` reads "Kotlin Multiplatform"
  - No build-number row is rendered — it was removed as invented

---

## TC-ABOUT-005 — Project card carries the app description and both attributions

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `about_project_card` renders
- **Then**
  - `about_project_header` "About this app" visible as a heading
  - `about_project_body` prose visible
  - `about_mifos_subheading` "The Mifos Initiative" and `about_mifos_body` visible
  - `about_openbanking_subheading` "HSBC UK Open Banking sandbox" and `about_openbanking_body` visible
  - The prose states that no real money moves and no real customer data is used
  - No rendered string names "Open Bank Project"

The last assertion is a disclosure, not decoration. This app talks to a sandbox; a customer who
believes otherwise may act on a balance that is fiction.

---

## TC-ABOUT-006 — Mifos link opens mifos.org externally

**Priority:** high · **State:** content

- **Given** Content state
- **When** User taps `about_mifos_link`
- **Then**
  - `LocalUriHandler.openUri` is called with `https://mifos.org`
  - The app is left entirely — no in-app back stack entry is created
  - No in-app web view is used

---

## TC-ABOUT-007 — The developer-portal link opens develop.hsbc.com externally

**Priority:** medium · **State:** content

- **Given** Content state
- **When** User taps `about_openbanking_link`
- **Then**
  - `LocalUriHandler.openUri` is called with `https://develop.hsbc.com`
  - `openbankproject.com` is not opened
  - `openbanking.org.uk` is not opened

Retargeted twice on 2026-08-06 — first off `openbankproject.com`, then off `openbanking.org.uk`,
which was also not a host this app relates to. `develop.hsbc.com` is the portal the HSBC
Implementation Guide was fetched from, so it is the one attribution target that is both correct
and verifiable. Both negative assertions are kept so a revert to either old host fails loudly.

---

## TC-ABOUT-008 — GitHub link opens the openMF organisation externally

**Priority:** medium · **State:** content

- **Given** Content state
- **When** User taps `about_github_link`
- **Then**
  - `LocalUriHandler.openUri` is called with `https://github.com/openMF`
  - This satisfies the source-availability disclosure the MPL notice requires

---

## TC-ABOUT-009 — Licence link keeps the MPL text reachable, not merely named

**Priority:** high · **State:** content

- **Given** Content state
- **When** User taps `about_mpl_link`
- **Then**
  - `LocalUriHandler.openUri` is called with `https://mozilla.org/MPL/2.0/`
  - The licence is reachable from the app, not only cited as a string

Note the division of labour with `licences`: that screen renders the **bundled** MPL text from a
Compose resource (TC-LICENCES-001); this link points at the canonical hosted copy. Both paths
exist, and neither substitutes for the other.

---

## TC-ABOUT-010 — Legal rows leave the app rather than navigating to sibling screens

**Priority:** high · **State:** content

- **Given** The app also ships `terms-of-service`, `privacy-policy` and `licences` screens
- **When** Any row in `about_legal_card` is tapped
- **Then**
  - An external URL is opened via `LocalUriHandler`
  - No in-app navigation to `terms-of-service`, `privacy-policy` or `licences` occurs — that navigation lives in Settings

The keystone scenario. Three sibling screens exist with names matching these rows, which is
exactly the condition under which someone "fixes" the links to point inward. The test records
that the outward behaviour is the intended one.

---

## TC-ABOUT-011 — Trailing open-in-new glyphs are decorative and readable

**Priority:** medium · **State:** content

- **Given** Content state
- **When** The four link rows render
- **Then**
  - Each row shows an `open_in_new` icon marked decorative with an empty a11y label
  - The adjacent link label already names the destination, so the icon is not announced twice
  - Icons use `onSurfaceVariant` (8.93:1) rather than `outlineVariant`, so the external-link cue is visible

Both halves matter and they pull in opposite directions: the icon must be *invisible* to a screen
reader and *visible* to an eye. Dropping either assertion loses one of the two audiences.

---

## TC-ABOUT-012 — Screen is static with no ViewModel or data layer

**Priority:** high · **State:** content

- **Given** `AboutScreen(onBack, modifier, appVersion)` is composed
- **When** Its contract is inspected
- **Then**
  - `state_model` type is `static_content` — no ViewModel, no DI, no repository, no events
  - `appVersion` is the only runtime input
  - No network call is issued by this screen

---

## TC-ABOUT-013 — Back returns to Settings

**Priority:** medium · **State:** content

- **Given** Screen entered from Settings → About
- **When** User taps the top app bar back icon
- **Then**
  - The `onBack` lambda is invoked
  - The user returns to settings (`nav_back`)

---

## TC-ABOUT-014 — Rate-this-app is absent

**Priority:** low · **State:** content

- **Given** Content state
- **When** The screen is inspected for a review affordance
- **Then**
  - No rate button is rendered — it was omitted as it requires a platform `ReviewManager`
  - No platform review API is invoked

---

## Traceability

| Link row | Destination | Scenario |
|----------|-------------|----------|
| `about_mifos_link` | `https://mifos.org` | TC-ABOUT-006 |
| `about_openbanking_link` | `https://develop.hsbc.com` | TC-ABOUT-007 |
| `about_github_link` | `https://github.com/openMF` | TC-ABOUT-008 |
| `about_mpl_link` | `https://mozilla.org/MPL/2.0/` | TC-ABOUT-009 |

All four are covered individually, and TC-ABOUT-010 covers the shared rule they obey.

---

_Generated by /idea-feature-test-export | 2026-08-04_
