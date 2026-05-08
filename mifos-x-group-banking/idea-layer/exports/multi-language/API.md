# Multi-Language — API Reference
**Feature**: multi-language | **Requirement**: FR-010
**Backend**: Local DataStore (language preference) + Mifos Fineract (PIN change only)

---

## API Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| PUT | /fineract-provider/api/v1/self/user/updatePassword | Change user PIN/password | BasicAuth (self-service) |

**Language selection does NOT make any API calls.** Language preference is stored entirely in Android DataStore (local, device-scoped). No Fineract call needed for language changes.

---

## Language Preference — Local Storage (DataStore)

Language is persisted via `PreferencesRepository` backed by Android DataStore:

```kotlin
// DataStore key
val LANGUAGE_KEY = stringPreferencesKey("selected_language")

// Read
context.dataStore.data.map { preferences ->
  AppLanguage.fromCode(preferences[LANGUAGE_KEY] ?: "en")
}

// Write (on OnLanguageSelected action)
context.dataStore.edit { preferences ->
  preferences[LANGUAGE_KEY] = language.code
}
```

**Lifecycle**: Preference persists across:
- App restart
- Logout / Login (preference is device-scoped, not user-scoped)
- App background / foreground
- Not reset on Clear Data (uses EncryptedSharedPreferences backup in production)

---

## Request / Response Details

### PUT /self/user/updatePassword

**Purpose**: Change the logged-in user's PIN (triggered only from Change PIN dialog — separate from language feature, but part of settings screen).

**Request Body**:
```json
{
  "currentPassword": "1234",
  "newPassword": "5678"
}
```

**Response**:
```json
{
  "resourceId": 12
}
```

**Errors**:
- 400: Current password incorrect, or new password fails policy (min 4 digits)
- 401: Session expired — redirect to login
- 500: Server error — show retry snackbar

---

## RestartComposableTree — Implementation

Language change triggers a full composable tree restart so the Compose i18n provider re-renders all text:

```kotlin
// In Activity.onCreate:
setContent {
  val currentLanguage by preferencesRepository.getLanguage().collectAsState(initial = AppLanguage.ENGLISH)
  CompositionLocalProvider(
    LocalAppLanguage provides currentLanguage
  ) {
    MifosGroupBankingApp(language = currentLanguage)
  }
}

// RestartComposableTree event handling:
LaunchedEffect(Unit) {
  viewModel.events.collect { event ->
    when (event) {
      is SettingsEvent.RestartComposableTree -> {
        // No explicit action needed — DataStore flow update cascades to setContent {}
        // since currentLanguage collectAsState updates trigger recomposition
      }
      ...
    }
  }
}
```

**Effect**: When `PreferencesRepository.setLanguage()` writes to DataStore, the `Flow<AppLanguage>` emits, `collectAsState` updates, and Compose re-renders the full tree with new locale — no Activity.recreate() needed.

---

## DTOs

### AppLanguage (enum)
| Value | Code | Display | Flag |
|-------|------|---------|------|
| ENGLISH | "en" | "English" | flag_gb |
| SWAHILI | "sw" | "Kiswahili" | flag_ke |
| FRENCH | "fr" | "Français" | flag_fr |
| HINDI | "hi" | "हिन्दी" | flag_in |

```kotlin
enum class AppLanguage(val code: String, val displayName: String, val flagResId: Int) {
  ENGLISH("en", "English", R.drawable.flag_gb),
  SWAHILI("sw", "Kiswahili", R.drawable.flag_ke),
  FRENCH("fr", "Français", R.drawable.flag_fr),
  HINDI("hi", "हिन्दी", R.drawable.flag_in);

  companion object {
    fun fromCode(code: String): AppLanguage =
      entries.firstOrNull { it.code == code } ?: ENGLISH
  }
}
```

### AppTheme (enum)
| Value | Description |
|-------|-------------|
| LIGHT | Always light mode |
| DARK | Always dark mode |
| SYSTEM | Follow system/OS setting |

### ChangePasswordRequest
| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| currentPassword | String | Yes | Must match current Fineract password |
| newPassword | String | Yes | Min 4 characters, digits only (PIN) |

### ChangePasswordResponse
| Field | Type | Description |
|-------|------|-------------|
| resourceId | Long | Fineract user resource ID |

---

## Demo State (settings screen)

```kotlin
SettingsState(
  selectedLanguage = AppLanguage.ENGLISH,
  selectedTheme = AppTheme.SYSTEM,
  isBiometricEnabled = false,
  isBiometricAvailable = true,
  isNotificationsEnabled = true,
  appVersion = "1.0.0",
  buildNumber = "42",
  isChangingPin = false,
  pinChangeError = null,
  pinChangeSuccess = false,
  isLoggingOut = false
)
```

## Language Switch Analytics

| Event | Trigger | Params |
|-------|---------|--------|
| settings_language_changed | User selects different language | from_language: String, to_language: String |
| settings_theme_changed | User selects different theme | theme: String |
| settings_biometric_toggled | Toggle changed | enabled: Boolean |
| settings_notifications_toggled | Toggle changed | enabled: Boolean |
| settings_pin_changed | PIN changed successfully | — |
| settings_logout | Logout confirmed | — |
