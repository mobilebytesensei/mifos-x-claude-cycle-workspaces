# TEST SPEC — Settings

| Field      | Value                          |
|------------|--------------------------------|
| Feature    | settings                       |
| Source     | `screens/settings/tests.yaml`  |
| Scenarios  | 9                              |
| Priorities | critical 4 · normal 5          |
| States     | content 7 · error 1 · empty 1  |
| Module     | `feature/settings`             |

---

## Coverage

Contiguous ids; all three declared states covered. `SettingsUiState` declares only `Content`,
`Empty` and `Error` — there is no `loading` state to test, which is correct for a screen whose data
source is a local preferences stream rather than a network call.

---

## This suite was reverse-synced from source, and 12 scenarios were deleted

`tests.yaml` was rebuilt on 2026-07-28 against the shipped test suite:

```
commonTest/ui/SettingsViewModelTest.kt
commonTest/SettingsScreenUiTest.kt
androidUnitTest/SettingsScreenRobolectricTest.kt
androidInstrumentedTest/SettingsScreenInstrumentedTest.kt
```

The previous 21-scenario suite tested a **Security** section (biometric lock, session timeout), a
**Notifications** section, a **Storage** section (PFM cache location + clear), a
**Location-permission** row, a **Clear-Local-Data** confirm sheet, a **Profile** row, and a loading
skeleton. None of them exist in source.

That is 12 scenarios describing seven surfaces that were never built — the largest single block of
phantom coverage the corpus has carried. It is worth recording rather than quietly forgetting,
because a suite that green-lights features which do not exist is worse than no suite: it reports
confidence about the parts of the app nobody wrote.

Two of the removed surfaces are still reachable *concepts* elsewhere — PFM was removed from the
project entirely on 2026-08-02, and change-password ships deliberately disabled with
`disabled_until: "change-password screen implemented"`. Neither belongs here.

---

## Test tags are asserted verbatim, in two conventions

This screen's assertions name source `TestTags` directly (`settings:content`,
`settings:row:consents`, `settings:themeValue`). Per `TRAINING_MASTER#test_tags`, those strings are
**source truth copied verbatim** — a tidied string silently breaks every Robolectric and
instrumented test for the screen.

Note `settings:section` and `settings:row` are recorded in `TRAINING_MASTER#test_tags.unbound_class`
as generic **base** constants never applied on their own; the applied tags are always the
qualified forms (`settings:section:appearance`, `settings:row:theme`) that the scenarios below use.

---

## TC-SET-001 — Three sections render with current preference values

**Priority:** critical · **State:** content

- **Given** `UserDataRepository` emits user data with `darkThemeConfig = FOLLOW_SYSTEM`
- **When** The screen composes
- **Then**
  - `settings:content` is displayed
  - `settings:section:appearance` renders with a theme dropdown row (`settings:row:theme`)
  - `settings:themeValue` reflects the resolved theme label
  - `settings:section:account` renders a single Consents row (`settings:row:consents`) with a chevron
  - `settings:section:about` renders Privacy, Licences and App Version rows
  - `settings:appVersionValue` is non-empty

"A **single** Consents row" is the assertion that guards the two-generations problem: `settings`
currently points at `consent-list`, while the newer `consent-manager` screen declares an outbound
edge to settings that settings does not reciprocate. If that product decision lands, this
assertion is the one that has to change, and it will fail loudly rather than silently render two
consent entry points.

---

## TC-SET-002 — Theme dropdown opens, selects and persists

**Priority:** critical · **State:** content

- **Given** Content state with `isThemeMenuExpanded = false`
- **When** User taps the theme row, then picks Dark
- **Then**
  - `ToggleThemeMenu` sets `isThemeMenuExpanded = true`; `settings:themeMenu` is displayed
  - `SelectTheme(DarkThemeConfig.DARK)` writes through `UserDataRepository`
  - The stream re-emits and `settings:themeValue` updates to the Dark label
  - The app retints immediately

The chain is asserted end to end — action, write, **re-emission**, repaint — rather than just the
final appearance. That middle step is the stream-first architecture's actual contract: the UI must
update because the repository emitted, not because the click handler also set local state. A
screen that does both looks identical and desynchronises the moment another writer touches the
preference.

---

## TC-SET-003 — Dismissing the theme menu leaves the selection unchanged

**Priority:** normal · **State:** content

- **Given** The theme dropdown is expanded
- **When** User dismisses without choosing
- **Then**
  - `DismissThemeMenu` sets `isThemeMenuExpanded = false`
  - **No write occurs** and `settings:themeValue` is unchanged

---

## TC-SET-004 — Consents row navigates to consent-list

**Priority:** critical · **State:** content

- **Given** Settings rendered in content state with the Account section visible
- **When** User taps `settings:row:consents`
- **Then** `onNavigateToConsents` fires → `navigate(ConsentListRoute)`

---

## TC-SET-005 — Licences row opens the in-app licences screen

**Priority:** normal · **State:** content

- **Given** Settings rendered in content state with the About section visible
- **When** User taps `settings:row:licences`
- **Then**
  - `onNavigateToLicences` fires → `navigate(LicencesRoute)`
  - The row carries a chevron and the **opens-in-app** accessibility description

---

## TC-SET-006 — Privacy row leaves the app for a browser

**Priority:** normal · **State:** content

- **Given** Settings rendered in content state with the About section visible; the privacy row is an external link (`settings:row:privacy:externalLink`)
- **When** User taps `settings:row:privacy`
- **Then**
  - `onOpenUrl` fires → `LocalUriHandler.openUri(url)`
  - The row carries the **external-link glyph** and the **opens-externally** accessibility description

005 and 006 are a deliberate pair: two adjacent rows in the same section that look alike and behave
completely differently. The chevron-versus-external-glyph and the two accessibility descriptions
are the only warning a customer gets before one of them leaves the app — which matters more here
than usual, since leaving a banking app mid-session is exactly the shape of a phishing prompt.

This is also why `privacy-policy` and `terms-of-service` appear as nav orphans in `APP_FLOW.mmd`:
the in-app screens exist, but settings reaches privacy via an external URL rather than a route.

---

## TC-SET-007 — App version row is inert

**Priority:** normal · **State:** content

- **Given** Content state with a resolved `appVersionLabel`
- **When** The About section renders
- **Then**
  - `settings:row:appVersion` shows the version as subtitle text
  - It has **no icon, no trailing affordance and no click handler**
  - Tapping it produces no navigation and no action

Three rows in one section, three different affordance treatments (chevron / external glyph /
nothing). Asserting the *absence* of an affordance is what keeps the other two meaningful — if
every row looked tappable, neither the chevron nor the glyph would carry information.

---

## TC-SET-008 — Preferences failure surfaces a retriable error

**Priority:** critical · **State:** error

- **Given** `UserDataRepository` fails to read preferences
- **When** The screen composes
- **Then**
  - `SettingsErrorKind.PreferencesUnavailable` is emitted
  - `settings:errorState` renders with `settings:errorTitle` and `settings:errorBody`
  - `settings:retryButton` is displayed (`isRetriable = true`)
  - Tapping it dispatches `SettingsAction.RetryLoad`

---

## TC-SET-009 — Empty state when no preferences resolve

**Priority:** normal · **State:** empty

- **Given** `SettingsUiState.Empty`
- **When** The screen composes
- **Then**
  - `settings:emptyState` renders with `settings:emptyTitle` and `settings:emptyBody`
  - **No section rows are rendered**

The distinction from TC-SET-008 is worth keeping: a preferences read that *fails* is retriable, a
preferences read that *resolves to nothing* is not. Collapsing the two would put a Retry button on
a state that has nothing to retry.

---

_Generated by /idea-feature-test-export | 2026-08-03_
