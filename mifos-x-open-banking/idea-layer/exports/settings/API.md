# API — Settings

**No backend API dependencies.** `api.yaml` declares `endpoints: []` with
`gap_strategy: client_only` — every value on this screen is local, and no HTTP request is issued
from it.

---

## Local data sources

| Value        | Source                | Notes                                              |
|--------------|-----------------------|-----------------------------------------------------|
| theme        | `UserDataRepository`  | Read and written locally; drives token resolution   |
| app version  | `SettingsAppVersion`  | Injected version string                             |

That is the whole surface. `SettingsUiState` has no `Loading` member because both values resolve
synchronously — there is nothing to wait on, so the screen opens at `content`.

The only failure mode is local: `SettingsErrorKind.PreferencesUnavailable` when preference storage
cannot be read, and `SettingsErrorKind.Unknown`. Neither is a network error, and the retry re-reads
local storage rather than re-issuing a request.

---

## Navigation carries no parameters

| Row            | Destination      |
|----------------|------------------|
| `consents_row` | `consent-list`   |
| `privacy_row`  | `privacy-policy` |
| `licences_row` | `licences`       |

Each destination loads its own data independently; nothing is passed from this screen.

`consents_row` is worth noting as an architectural point rather than a data one: it is the stable,
discoverable entry to consent management. Other screens reach `consent-list` only from error states
(`beneficiaries` when a permission is missing, `consent-list`'s own re-auth path), so this row is
the route a customer can find without first hitting a failure.

---

<!--
Regenerated 2026-08-04 by /idea-feature-export --all --force from screens/settings/api.yaml.

The previous revision correctly stated there were no backend dependencies, but its detail had gone
stale: it documented eight preferences (isDarkModeEnabled, selectedLanguage,
isPushNotificationsEnabled, isTransactionAlertsEnabled, isMarketingEnabled, isBiometricLoginEnabled,
isBiometricAvailableOnDevice, appVersion), a cascading push/transaction-alerts disable rule, a
`SettingsRepository` wrapping Jetpack DataStore, and navigation to about, consent-manager,
change-password and terms-of-service. The shipped screen carries ONE preference (theme) via
UserDataRepository plus SettingsAppVersion, and three navigation rows (consent-list, privacy-policy,
licences). None of the notification, language or biometric preferences exist on it.
-->
