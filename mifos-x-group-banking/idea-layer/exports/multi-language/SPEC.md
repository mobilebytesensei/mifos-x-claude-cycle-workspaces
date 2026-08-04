# Multi-Language — Feature Specification
**Project**: MifosSave (mifos-x-group-banking)
**Feature ID**: multi-language
**Requirement**: FR-010
**Version**: 1.0.0
**Status**: enriched

---

## Overview

Multi-language support allows members and field officers to use MifosSave in their preferred language. Four languages are supported: English (en), Kiswahili (sw), Français (fr), and हिन्दी (hi). Language is selected via a radio group in the Settings screen. On selection, the preference is persisted to DataStore, and the entire composable tree is restarted via `RestartComposableTree` event so the new locale takes effect immediately — no app restart required. The language selector is accessible to both admin and end-user client types.

---

## Acceptance Criteria

- **FR-010**: Users can switch between English, Kiswahili, French, and Hindi at any time via the Settings screen Language section. The selected language is persisted locally (DataStore). On selection, the full composable tree restarts with the new locale — all visible strings, section labels, button labels, and dialog text update immediately. No network call is made during language selection. The language persists across app restarts and logout/login cycles (preference is tied to device, not user account).

---

## Screens Table

| Screen ID | Route | Type | Role |
|-----------|-------|------|------|
| settings | /settings | settings | Both (admin + end user) |

---

## State Model

### SettingsViewModel (language-relevant fields)
| Field | Type | Default |
|-------|------|---------|
| selectedLanguage | AppLanguage | AppLanguage.ENGLISH |
| selectedTheme | AppTheme | AppTheme.SYSTEM |
| isBiometricEnabled | Boolean | false |
| isNotificationsEnabled | Boolean | true |
| isBiometricAvailable | Boolean | false |
| appVersion | String | "" |
| buildNumber | String | "" |
| isChangingPin | Boolean | false |
| pinChangeError | String? | null |
| pinChangeSuccess | Boolean | false |
| isLoggingOut | Boolean | false |

**Screen states**: Content, ChangingPin, LoggingOut

**Actions**:
- `OnLanguageSelected(language: AppLanguage)` — persists to DataStore, emits RestartComposableTree
- `OnThemeSelected(theme: AppTheme)` — persists, applies dynamically
- `OnBiometricToggle(enabled: Boolean)` — persists, checks hardware availability
- `OnNotificationsToggle(enabled: Boolean)` — persists
- `OnChangePin` — emits ShowPinChangeDialog
- `OnSubmitPinChange(currentPin, newPin)` — calls Fineract PUT /self/user/updatePassword
- `OnLogout` — shows confirm dialog, then clears session + local DB

**Events**:
- `RestartComposableTree(language: AppLanguage)` — triggers `Activity.setContent { MifosApp(language=...) }`
- `ShowPinChangeDialog`
- `ShowSnackbar(message: String)`
- `NavigateToLogin`

**DI**: PreferencesRepository, AuthRepository, BiometricManager

---

## AppLanguage Enum

| Value | Display Name | Locale Code | Flag Icon |
|-------|-------------|-------------|-----------|
| ENGLISH | English | en | flag_gb (UK flag) |
| SWAHILI | Kiswahili | sw | flag_ke (Kenya flag) |
| FRENCH | Français | fr | flag_fr (France flag) |
| HINDI | हिन्दी | hi | flag_in (India flag) |

---

## Settings Screen Layout (all sections)

The settings screen contains 5 sections:

1. **Language** — RadioGroup: English / Kiswahili / Français / हिन्दी (FR-010)
2. **Appearance** — RadioGroup: Light / Dark / System Default (FR-013)
3. **Security** — Biometric toggle + Change PIN row
4. **Notifications** — Push notifications toggle
5. **About** — App version row + Logout button

---

## Navigation Table

| From | Action | To |
|------|--------|----|
| bottom_nav | Settings tab | /settings |
| profile_menu | Settings | /settings |
| settings | Logout confirmed | /login |

settings is a terminal screen — no outbound navigation except after logout.

---

## API Endpoints Table

| Method | Path | Description |
|--------|------|-------------|
| PUT | /fineract-provider/api/v1/self/user/updatePassword | Change user PIN/password |

No API call on screen load. Language selection, theme, biometric, and notification toggles are all stored locally in Android DataStore. Only `OnSubmitPinChange` makes a network request.

---

## I18n Keys (full set across 4 languages)

| Key | en | sw | fr | hi |
|-----|----|----|----|----|
| screen_title | Settings | Mipangilio | Paramètres | सेटिंग्स |
| section_language | Language | Lugha | Langue | भाषा |
| section_appearance | Appearance | Muonekano | Apparence | दिखावट |
| section_security | Security | Usalama | Sécurité | सुरक्षा |
| section_notifications | Notifications | Arifa | Notifications | सूचनाएं |
| section_about | About | Kuhusu | À propos | के बारे में |
| biometric_label | Biometric Unlock | Ufunguzi wa Biometric | Déverrouillage Biométrique | बायोमेट्रिक अनलॉक |
| biometric_sublabel | Use fingerprint or face ID | Tumia alama ya kidole | Utiliser empreinte ou visage | फिंगरप्रिंट या फेस ID |
| change_pin_label | Change PIN | Badilisha PIN | Changer le PIN | PIN बदलें |
| logout_button | Logout | Toka | Se Déconnecter | लॉग आउट |
| lang_english | English | Kiingereza | Anglais | अंग्रेज़ी |
| lang_swahili | Kiswahili | Kiswahili | Swahili | स्वाहिली |
| lang_french | Français | Kifaransa | Français | फ्रेंच |
| lang_hindi | हिन्दी | Kihindi | Hindi | हिन्दी |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | TopAppBar background, section header labels, radio indicator |
| onPrimary | #FFFFFF | TopAppBar title |
| surface | #FAFAFA | Radio group card background, settings row background |
| onSurface | #1C1C1C | Radio option primary labels, settings row labels |
| onSurfaceVariant | #424942 | Radio option sublabels, settings row sublabels |
| errorContainer | #FFDAD6 | Logout button background |
| onErrorContainer | #410002 | Logout button text |
| outline | #727971 | Section dividers, radio option dividers |
| primaryContainer | #A6F1A6 | Selected radio option background |
| onPrimaryContainer | #002106 | Selected radio option text |
