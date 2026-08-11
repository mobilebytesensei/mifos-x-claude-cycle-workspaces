# Multi-Language — Stitch Prompt Specification
**Feature**: multi-language | **Screen**: settings
**Requirement**: FR-010
**Stitch project**: MifosSave / mifos-x-group-banking
**Total sections**: 6

---

# SECTION 1: DESIGN SYSTEM CONTEXT

## Application Identity
MifosSave is a VSLA group banking app for rural communities across Kenya, West Africa, and South Asia. Multi-language support is a core accessibility feature: a member in Nairobi uses Kiswahili, a group in Dakar uses Français, and a community in rural Rajasthan uses हिन्दी. The settings screen must render all four languages correctly using Noto Sans (which supports Latin, Cyrillic, Arabic, and Devanagari scripts). Language switching must feel instant — no loading states.

## Material Design 3 Token System

### Color Palette (all hex values exact)

#### Primary — VSLA Green (TopAppBar, section headers, selected radio)
- primary: #2E7D32
- onPrimary: #FFFFFF
- primaryContainer: #A6F1A6
- onPrimaryContainer: #002106

#### Secondary — Amber
- secondary: #FF8F00
- secondaryContainer: #FFDDB3
- onSecondaryContainer: #2A1700

#### Error (logout button background, PIN error text)
- error: #D32F2F
- errorContainer: #FFDAD6
- onErrorContainer: #410002

#### Neutral
- surface: #FAFAFA
- onSurface: #1C1C1C
- surfaceVariant: #DEE5DA
- onSurfaceVariant: #424942
- outline: #727971
- background: #FAFAFA
- onBackground: #1C1C1C

### Typography Scale (Noto Sans — supports all 4 languages)

| Style | Size (sp) | Weight | Usage |
|-------|-----------|--------|-------|
| titleLarge | 22 | 500 | TopAppBar title (localized) |
| labelLarge | 14 | 500 | Section headers (Language, Appearance, Security...) |
| bodyLarge | 16 | 400 | Radio option label (language name in target language) |
| bodySmall | 12 | 400 | Radio option sublabel (English descriptor), settings row sublabels |
| labelSmall | 11 | 500 | Disabled hint text, badge text |

**Font handling for Devanagari (Hindi)**:
Noto Sans automatically selects `Noto Sans Devanagari` subset when rendering Hindi characters (Unicode range U+0900–U+097F). No explicit font override needed in Compose.

### Spacing Scale
| Token | dp | Usage |
|-------|----|-------|
| sm | 8 | Dialog inner gaps |
| md | 12 | Row vertical padding |
| lg | 16 | Page margins, section header padding |
| xl | 24 | Section gap |

### Shape Scale
| Token | Corner Radius | Usage |
|-------|--------------|-------|
| medium | 12dp | RadioGroup card, LogoutButton |
| large | 16dp | AlertDialog |
| full | 9999dp | Role pills |

### Elevation
| Level | dp | Usage |
|-------|----|-------|
| level_0 | 0dp | Flat surface rows |
| level_1 | 1dp | RadioGroup card subtle shadow |
| level_2 | 3dp | AlertDialog (dialog elevation) |

### Motion Timing
| Token | Duration | Easing | Usage |
|-------|----------|--------|-------|
| short_4 | 200ms | Standard | RadioButton selection animation |
| medium_1 | 250ms | Emphasized | Language switch option highlight fade |
| medium_2 | 300ms | Emphasized | Theme switch (dark/light transition) |
| medium_3 | 350ms | Decelerated | AlertDialog enter |
| shimmer_cycle | — | — | Not applicable (no loading states) |

### Accessibility
- Min touch target: 56dp for all radio options and settings rows
- Flag icons: contentDescription set (decorative but language-meaningful)
- Radio group: role=radiogroup with proper semantics
- Screen reader: TalkBack reads Devanagari, Kiswahili, French correctly
- Contrast: all text at 4.5:1 minimum against backgrounds

### Breakpoints
| Name | Range | Behavior |
|------|-------|----------|
| compact | 0–599dp | Single column, full width |
| medium | 600–839dp | Max 560dp, centered |
| expanded | 840dp+ | Two-column: language/theme left, security/notif right |

---

# SECTION 2: SCREEN COMPONENT TREES

## Settings Screen — Full Component Tree (English selected, SYSTEM theme)

```
SettingsScreen(selectedLanguage=ENGLISH, selectedTheme=SYSTEM)
├── Scaffold
│   ├── TopAppBar
│   │   ├── title: Text(i18n.screen_title, titleLarge, onPrimary)  // "Settings"
│   │   ├── colors: TopAppBarDefaults.topAppBarColors(containerColor=primary)
│   │   └── [no navigation icon — accessed via bottom nav]
│   │
│   └── content: LazyColumn(fillMaxSize, contentPadding=PaddingValues(bottom=16dp))
│       │
│       ├── item: SectionHeader("Language")
│       │   └── Text(i18n.section_language, labelLarge, primary, padding=PaddingValues(start=16dp, top=16dp, end=16dp, bottom=8dp))
│       │
│       ├── item: LanguageRadioGroup
│       │   └── Card(bg=surface, cornerRadius=12dp, elevation=1dp, margin=PaddingValues(horizontal=16dp))
│       │       └── Column
│       │           ├── RadioOptionRow(ENGLISH, selected=true)
│       │           │   ├── Row(minHeight=56dp, padding=horizontal 16dp vertical 12dp, bg=primaryContainer)
│       │           │   ├── FlagIcon(flag_gb, 24dp)
│       │           │   ├── Spacer(12dp)
│       │           │   ├── Column(weight=1f)
│       │           │   │   ├── Text("English", bodyLarge, onPrimaryContainer)
│       │           │   │   └── Text("English", bodySmall, onPrimaryContainer alpha 0.7)
│       │           │   └── RadioButton(selected=true, color=primary)
│       │           ├── Divider(1dp, outline)
│       │           ├── RadioOptionRow(SWAHILI, selected=false)
│       │           │   ├── Row(minHeight=56dp, padding=horizontal 16dp vertical 12dp, bg=surface)
│       │           │   ├── FlagIcon(flag_ke, 24dp)
│       │           │   ├── Column(weight=1f)
│       │           │   │   ├── Text("Kiswahili", bodyLarge, onSurface)
│       │           │   │   └── Text("Swahili", bodySmall, onSurfaceVariant)
│       │           │   └── RadioButton(selected=false)
│       │           ├── Divider
│       │           ├── RadioOptionRow(FRENCH, selected=false)
│       │           │   ├── FlagIcon(flag_fr, 24dp)
│       │           │   ├── Text("Français", bodyLarge, onSurface)
│       │           │   └── Text("French", bodySmall, onSurfaceVariant)
│       │           ├── Divider
│       │           └── RadioOptionRow(HINDI, selected=false)
│       │               ├── FlagIcon(flag_in, 24dp)
│       │               ├── Text("हिन्दी", bodyLarge, onSurface)  // Devanagari
│       │               └── Text("Hindi", bodySmall, onSurfaceVariant)
│       │
│       ├── item: SectionHeader("Appearance")
│       │
│       ├── item: ThemeRadioGroup
│       │   └── Card (same structure, 3 options: Light/Dark/System)
│       │       ├── RadioOptionRow(LIGHT, icon=light_mode)
│       │       ├── RadioOptionRow(DARK, icon=dark_mode)
│       │       └── RadioOptionRow(SYSTEM, selected=true, icon=contrast)
│       │
│       ├── item: SectionHeader("Security")
│       │
│       ├── item: SecuritySection
│       │   └── Card(bg=surface, cornerRadius=12dp, elevation=1dp, margin=horizontal 16dp)
│       │       ├── BiometricToggleRow
│       │       │   └── Row(minHeight=56dp, padding=horizontal 16dp)
│       │       │       ├── Icon(fingerprint, 24dp, onSurfaceVariant)
│       │       │       ├── Spacer(12dp)
│       │       │       ├── Column(weight=1f)
│       │       │       │   ├── Text("Biometric Unlock", bodyLarge, onSurface)
│       │       │       │   └── Text("Use fingerprint or face ID", bodySmall, onSurfaceVariant)
│       │       │       └── Switch(checked=false, enabled=isBiometricAvailable, thumbColor=primary)
│       │       ├── Divider(1dp, outline)
│       │       └── ChangePinRow
│       │           └── Row(minHeight=56dp, padding=horizontal 16dp, clickable)
│       │               ├── Icon(lock_reset, 24dp, onSurfaceVariant)
│       │               ├── Spacer(12dp)
│       │               ├── Column(weight=1f)
│       │               │   ├── Text("Change PIN", bodyLarge, onSurface)
│       │               │   └── Text("Update your 4-digit PIN", bodySmall, onSurfaceVariant)
│       │               └── Icon(chevron_right, 20dp, onSurfaceVariant)
│       │
│       ├── item: SectionHeader("Notifications")
│       │
│       ├── item: NotificationsSection
│       │   └── Card
│       │       └── NotificationsToggleRow
│       │           ├── Icon(notifications, 24dp, onSurfaceVariant)
│       │           ├── Text("Push Notifications", bodyLarge)
│       │           ├── Text("Receive alerts for meetings...", bodySmall, onSurfaceVariant)
│       │           └── Switch(checked=true, thumbColor=primary)
│       │
│       ├── item: SectionHeader("About")
│       │
│       ├── item: AppVersionRow
│       │   └── Row(minHeight=48dp, padding=horizontal 16dp)
│       │       ├── Icon(info_outline, 24dp, onSurfaceVariant)
│       │       ├── Column(weight=1f)
│       │       │   ├── Text("App Version", bodyLarge)
│       │       │   └── Text("1.0.0 (Build 42)", bodySmall, onSurfaceVariant)
│       │       └── [no trailing]
│       │
│       └── item: LogoutButton
│           └── Button(
│               text=i18n.logout_button,  // "Logout"
│               leadingIcon=logout 18dp,
│               containerColor=errorContainer,
│               contentColor=onErrorContainer,
│               cornerRadius=12dp,
│               height=56dp,
│               fillMaxWidth=true,
│               margin=16dp horizontal,
│               onClick=OnLogout
│               )
│
└── [ChangePinDialog — shown when isChangingPin=true]
    └── AlertDialog(
        title="Change PIN",
        confirmButton=FilledButton("Update PIN", onClick=OnSubmitPinChange),
        dismissButton=TextButton("Cancel"),
        shape=RoundedCornerShape(16dp)
        )
        content:
          Column(verticalArrangement=spacedBy(8dp))
            OutlinedTextField(label="Current PIN", inputType=Password, keyboard=Number, height=56dp)
            OutlinedTextField(label="New PIN (min 4 digits)", inputType=Password, keyboard=Number)
            if pinChangeError != null:
              Text(pinChangeError, bodySmall, error)
```

---

# SECTION 3: COMPONENT SPECIFICATIONS

## LanguageRadioGroup

```kotlin
@Composable
fun LanguageRadioGroup(
  selectedLanguage: AppLanguage,
  onLanguageSelected: (AppLanguage) -> Unit
) {
  Card(
    shape = RoundedCornerShape(12.dp),
    elevation = CardDefaults.cardElevation(1.dp),
    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)
  ) {
    Column {
      AppLanguage.entries.forEachIndexed { index, language ->
        val isSelected = selectedLanguage == language
        RadioOptionRow(
          language = language,
          isSelected = isSelected,
          onClick = { onLanguageSelected(language) }
        )
        if (index < AppLanguage.entries.lastIndex) {
          Divider(color = MaterialTheme.colorScheme.outline, thickness = 1.dp)
        }
      }
    }
  }
}
```

## RadioOptionRow (Language)

```kotlin
@Composable
fun LanguageOptionRow(
  language: AppLanguage,
  isSelected: Boolean,
  onClick: () -> Unit
) {
  val backgroundColor by animateColorAsState(
    targetValue = if (isSelected) primaryContainer else surface,
    animationSpec = tween(durationMillis = 200)
  )
  val textColor = if (isSelected) onPrimaryContainer else onSurface
  val subtextColor = if (isSelected) onPrimaryContainer.copy(alpha = 0.7f) else onSurfaceVariant

  Row(
    modifier = Modifier
      .fillMaxWidth()
      .heightIn(min = 56.dp)
      .background(backgroundColor)
      .clickable(onClick = onClick)
      .padding(horizontal = 16.dp, vertical = 12.dp),
    verticalAlignment = Alignment.CenterVertically
  ) {
    // Flag icon (24dp, flag colors preserved — no tint)
    Image(
      painter = painterResource(language.flagResId),
      contentDescription = "${language.displayName} flag",
      modifier = Modifier.size(24.dp)
    )

    Spacer(modifier = Modifier.width(12.dp))

    Column(modifier = Modifier.weight(1f)) {
      Text(
        text = language.displayName,  // In target language: "Kiswahili", "Français", "हिन्दी"
        style = MaterialTheme.typography.bodyLarge,
        color = textColor,
        fontFamily = NotoSans  // supports Devanagari automatically
      )
      Text(
        text = language.englishDescriptor,  // Always in English: "Swahili", "French", "Hindi"
        style = MaterialTheme.typography.bodySmall,
        color = subtextColor
      )
    }

    RadioButton(
      selected = isSelected,
      onClick = onClick,
      colors = RadioButtonDefaults.colors(
        selectedColor = primary,
        unselectedColor = outline
      )
    )
  }
}
```

## SettingsRowWithSwitch

```kotlin
@Composable
fun SettingsToggleRow(
  icon: ImageVector,
  label: String,
  sublabel: String,
  checked: Boolean,
  enabled: Boolean = true,
  disabledHint: String? = null,
  onCheckedChange: (Boolean) -> Unit
) {
  Row(
    modifier = Modifier
      .fillMaxWidth()
      .heightIn(min = 56.dp)
      .alpha(if (enabled) 1f else 0.38f)
      .padding(horizontal = 16.dp),
    verticalAlignment = Alignment.CenterVertically
  ) {
    Icon(icon, contentDescription = null, tint = onSurfaceVariant, modifier = Modifier.size(24.dp))
    Spacer(12.dp)
    Column(modifier = Modifier.weight(1f)) {
      Text(label, bodyLarge, onSurface)
      Text(if (!enabled && disabledHint != null) disabledHint else sublabel, bodySmall, onSurfaceVariant)
    }
    Switch(
      checked = checked,
      onCheckedChange = if (enabled) onCheckedChange else null,
      colors = SwitchDefaults.colors(
        checkedThumbColor = onPrimary,
        checkedTrackColor = primary,
        uncheckedThumbColor = outline,
        uncheckedTrackColor = surfaceVariant
      )
    )
  }
}
```

## LogoutButton

```kotlin
Button(
  onClick = onLogout,
  modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp).height(56.dp),
  shape = RoundedCornerShape(12.dp),
  colors = ButtonDefaults.buttonColors(
    containerColor = errorContainer,
    contentColor = onErrorContainer
  )
) {
  if (isLoggingOut) {
    CircularProgressIndicator(
      modifier = Modifier.size(18.dp),
      strokeWidth = 2.dp,
      color = onErrorContainer
    )
  } else {
    Icon(Icons.AutoMirrored.Filled.Logout, contentDescription = null, modifier = Modifier.size(18.dp))
  }
  Spacer(8.dp)
  Text(i18n.logout_button, labelLarge)
}
```

## ChangePinDialog

```kotlin
AlertDialog(
  onDismissRequest = onDismiss,
  title = { Text("Change PIN", titleMedium) },
  text = {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
      OutlinedTextField(
        value = currentPin,
        onValueChange = { currentPin = it },
        label = { Text("Current PIN") },
        visualTransformation = PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.NumberPassword),
        singleLine = true,
        modifier = Modifier.fillMaxWidth().height(56.dp)
      )
      OutlinedTextField(
        value = newPin,
        onValueChange = { newPin = it },
        label = { Text("New PIN (min 4 digits)") },
        visualTransformation = PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.NumberPassword),
        singleLine = true,
        modifier = Modifier.fillMaxWidth().height(56.dp)
      )
      AnimatedVisibility(visible = pinChangeError != null) {
        Text(
          text = pinChangeError ?: "",
          style = MaterialTheme.typography.bodySmall,
          color = MaterialTheme.colorScheme.error
        )
      }
    }
  },
  confirmButton = {
    FilledButton(
      text = "Update PIN",
      onClick = { onSubmitPinChange(currentPin, newPin) },
      enabled = currentPin.length >= 4 && newPin.length >= 4
    )
  },
  dismissButton = { TextButton("Cancel", onClick = onDismiss) },
  shape = RoundedCornerShape(16.dp)
)
```

---

# SECTION 4: INTERACTION FLOWS

## Flow 1: Language Selection (EN → SW) — FR-010

```
User taps "Kiswahili" row
  ↓
RadioButton animates to selected state (100ms)
Background color transitions: surface → primaryContainer #A6F1A6 (200ms)
English row background transitions: primaryContainer → surface (200ms)
  ↓
OnLanguageSelected(AppLanguage.SWAHILI) dispatched
  ↓
ViewModel:
  selectedLanguage = AppLanguage.SWAHILI
  preferencesRepository.setLanguage(AppLanguage.SWAHILI)  // DataStore write
  emit RestartComposableTree(AppLanguage.SWAHILI)
  ↓
Activity.setContent {} re-executes:
  currentLanguage flow emits SWAHILI
  collectAsState updates → Compose recomposition triggered
  ↓
Full composable tree re-renders with sw locale:
  TopAppBar title: "Settings" → "Mipangilio"
  Section headers: "Language" → "Lugha", "Security" → "Usalama"
  Radio labels: "English" → "Kiingereza", "Français" → "Kifaransa"
  Logout button: "Logout" → "Toka"
  ↓
Transition: CrossfadeAnimation (300ms) between old and new text
// Note: no Activity.recreate() — pure Compose recomposition
```

## Flow 2: Language Selection (EN → HI — Hindi/Devanagari)

```
User taps "हिन्दी" row
  ↓
RadioButton selected (100ms)
Background: primaryContainer fade in (200ms)
  ↓
OnLanguageSelected(AppLanguage.HINDI)
PreferencesRepository.setLanguage("hi")
  ↓
Tree re-renders:
  TopAppBar: "Settings" → "सेटिंग्स" (Devanagari)
  Section: "Language" → "भाषा"
  Labels: all switch to Hindi
  ↓
Noto Sans Devanagari subset loaded (already preloaded — no font fetch delay)
Text renders correctly in Devanagari RTL-friendly layout
  // Kiswahili and French are LTR; Hindi Devanagari is also LTR
```

## Flow 3: Theme Switch (SYSTEM → DARK)

```
User taps "Dark" option in Appearance section
  ↓
RadioButton: SYSTEM deselects (200ms) → DARK selects (100ms)
  ↓
OnThemeSelected(AppTheme.DARK)
PreferencesRepository.setTheme(AppTheme.DARK)  // DataStore write
  ↓
MaterialTheme darkColorScheme applied immediately:
  Background: #FAFAFA → #1C1C1E (300ms transition via animateColorAsState)
  Surface: #FAFAFA → #2C2C2E
  TopAppBar: primary #2E7D32 → primary dark #48C454
  Section headers: primary → primary dark
  Radio options: surface → dark surface
  All text: onSurface → dark onSurface
  ↓
// No tree restart needed — MaterialTheme ColorScheme change triggers recomposition
```

## Flow 4: Change PIN

```
User taps "Change PIN" row
  ↓
Row ripple effect (48×56dp tap target)
OnChangePin action → ShowPinChangeDialog event
  ↓
AlertDialog appears (350ms decelerated enter animation)
  ↓
User enters current PIN: "1234"
User enters new PIN: "5678"
  ↓
Tap "Update PIN"
  ↓
OnSubmitPinChange("1234", "5678")
  ↓
Validate: "5678".length >= 4 && all digits → valid
  ↓
isChangingPin = true → button shows loading
  ↓
PUT /self/user/updatePassword { "currentPassword": "1234", "newPassword": "5678" }
  ↓
200 OK: { "resourceId": 12 }
  ↓
pinChangeSuccess = true
isChangingPin = false
AlertDialog closes
ShowSnackbar("PIN updated successfully")
```

## Flow 5: Logout

```
User taps "Logout" / "Toka" / "Se Déconnecter" button
  ↓
OnLogout action → ConfirmLogoutDialog appears:
  Title: "Logout?" / "Toka?"
  Body: "Your local data will be cleared."
  Actions: Cancel + Confirm
  ↓
User taps Confirm → OnConfirmLogout
  ↓
isLoggingOut = true → button shows spinner
  ↓
AuthRepository.logout():
  Clear JWT/session tokens
  SQLDelight: DROP all tables (or DELETE all rows)
  DataStore: clear auth data (preserve language preference)
  ↓
NavigateToLogin event
  ↓
App navigates to /login
Language preference preserved (device-scoped, not session-scoped)
```

## Flow 6: Biometric Toggle (Enable)

```
User taps biometric switch (enabled=true, isBiometricAvailable=true)
  ↓
OnBiometricToggle(enabled=true)
  ↓
isBiometricAvailable check: true → proceed
  ↓
BiometricManager.showBiometricEnrollment()
  → System biometric enrollment UI shown
  ↓
User completes enrollment:
  Success: PreferencesRepository.setBiometricEnabled(true)
           switch stays ON
  Failure: switch reverts to OFF
           ShowSnackbar("Biometric enrollment failed")
```

---

# SECTION 5: REAL DATA SPECIFICATION

## Demo Settings State

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

## Language Options Data

```kotlin
val languageOptions = listOf(
  AppLanguage.ENGLISH to LanguageOptionData(
    displayName = "English",       // shown in selected language
    englishDescriptor = "English", // always in English
    flagResId = R.drawable.flag_gb,
    localeCode = "en"
  ),
  AppLanguage.SWAHILI to LanguageOptionData(
    displayName = "Kiswahili",
    englishDescriptor = "Swahili",
    flagResId = R.drawable.flag_ke,
    localeCode = "sw"
  ),
  AppLanguage.FRENCH to LanguageOptionData(
    displayName = "Français",
    englishDescriptor = "French",
    flagResId = R.drawable.flag_fr,
    localeCode = "fr"
  ),
  AppLanguage.HINDI to LanguageOptionData(
    displayName = "हिन्दी",          // Devanagari
    englishDescriptor = "Hindi",
    flagResId = R.drawable.flag_in,
    localeCode = "hi"
  )
)
```

## I18n Keys — All 4 Languages

**English (en)**:
```
screen_title: "Settings"
section_language: "Language"
section_appearance: "Appearance"
section_security: "Security"
section_notifications: "Notifications"
section_about: "About"
biometric_label: "Biometric Unlock"
biometric_sublabel: "Use fingerprint or face ID to log in"
biometric_unavailable: "Biometric hardware not available on this device"
change_pin_label: "Change PIN"
change_pin_sublabel: "Update your 4-digit security PIN"
notifications_label: "Push Notifications"
notifications_sublabel: "Receive alerts for meetings, repayments, and sync events"
version_label: "App Version"
logout_button: "Logout"
```

**Kiswahili (sw)**:
```
screen_title: "Mipangilio"
section_language: "Lugha"
section_security: "Usalama"
biometric_label: "Ufunguzi wa Biometric"
change_pin_label: "Badilisha PIN"
logout_button: "Toka"
lang_english: "Kiingereza"
lang_swahili: "Kiswahili"
lang_french: "Kifaransa"
lang_hindi: "Kihindi"
```

**Français (fr)**:
```
screen_title: "Paramètres"
section_language: "Langue"
section_security: "Sécurité"
biometric_label: "Déverrouillage Biométrique"
biometric_sublabel: "Utiliser empreinte ou visage"
change_pin_label: "Changer le PIN"
logout_button: "Se Déconnecter"
lang_english: "Anglais"
lang_swahili: "Swahili"
lang_french: "Français"
lang_hindi: "Hindi"
```

**हिन्दी (hi)**:
```
screen_title: "सेटिंग्स"
section_language: "भाषा"
section_security: "सुरक्षा"
biometric_label: "बायोमेट्रिक अनलॉक"
biometric_sublabel: "फिंगरप्रिंट या फेस ID से लॉगिन"
change_pin_label: "PIN बदलें"
logout_button: "लॉग आउट"
lang_english: "अंग्रेज़ी"
lang_swahili: "स्वाहिली"
lang_french: "फ्रेंच"
lang_hindi: "हिन्दी"
```

## Change PIN API Demo

PUT /fineract-provider/api/v1/self/user/updatePassword

Request: `{ "currentPassword": "1234", "newPassword": "5678" }`
Response: `{ "resourceId": 12 }`

Error 400: `{ "defaultUserMessage": "Current password is incorrect." }`
→ Show: pinChangeError = "PIN change failed. Check your current PIN and try again."

---

# SECTION 6: RESPONSIVE LAYOUT + ADAPTIVE BEHAVIOR

## Compact Layout (0–599dp) — Primary target

```
Screen width: 360dp

TopAppBar: fullWidth, 56dp single-line title
LazyColumn: fillMaxWidth, no horizontal padding (sections manage their own margins)

SectionHeader: padding(start=16dp, top=16dp, end=16dp, bottom=8dp)
RadioGroup Card: padding(horizontal=16dp)
  RadioOptionRow: fillMaxWidth, minHeight=56dp

SettingsSection Card: padding(horizontal=16dp)
  SettingsRow: fillMaxWidth, minHeight=56dp

LogoutButton: padding(horizontal=16dp), fillMaxWidth, height=56dp

Total content height: ~760dp (scrollable on all compact devices)
```

### Font Size at 360dp
All Noto Sans sizes at scale_style=large are appropriate for 360dp:
- titleLarge (22sp) at 360dp = visible and readable
- Devanagari (हिन्दी) at bodyLarge 16sp = comfortable for non-native readers

## Medium Layout (600–839dp)

```
LazyColumn: contentPadding=PaddingValues(horizontal=40dp)
  Sections centered, max card width = 520dp
  RadioOption rows: more padding, flag icons larger (28dp)
```

## Expanded Layout (840dp+)

```
Row(fillMaxSize, horizontalArrangement=spacedBy(24dp), padding=24dp)
  ├── Column(weight=0.5f)
  │   ├── SectionHeader("Language")
  │   ├── LanguageRadioGroup
  │   ├── SectionHeader("Appearance")
  │   └── ThemeRadioGroup
  │
  └── Column(weight=0.5f)
      ├── SectionHeader("Security")
      ├── SecuritySection
      ├── SectionHeader("Notifications")
      ├── NotificationsSection
      ├── SectionHeader("About")
      ├── AppVersionRow
      └── LogoutButton
```

## Dark Theme — Settings Screen

| Light | Dark | Element |
|-------|------|---------|
| primary #2E7D32 (TopAppBar bg) | primary dark #48C454 (dark enough for readability changes) → better: primaryDark = #1B5E20 | TopAppBar bg |
| surface #FAFAFA | #1C1C1E | Card backgrounds |
| onSurface #1C1C1C | #E6E1E5 | Label text |
| primaryContainer #A6F1A6 | #003910 | Selected radio bg |
| onPrimaryContainer #002106 | #A6F1A6 | Selected radio text |
| errorContainer #FFDAD6 | #410002 | Logout button bg |
| onErrorContainer #410002 | #FFDAD6 | Logout button text |
| outline #727971 | #8C9388 | Dividers |
| Switch checked track | primary #2E7D32 | → #48C454 (lightened) |

## Snackbar Messages

| Event | Message (en) | Message (sw) | Duration |
|-------|-------------|-------------|---------|
| PIN changed | "PIN updated successfully" | "PIN imebadilishwa" | short |
| PIN failed | "PIN change failed. Check current PIN." | "Imeshindwa kubadilisha PIN" | long |
| Language changed | (no snackbar — tree restarts visibly) | — | — |
| Biometric enabled | "Biometric unlock enabled" | "Biometric imewezeshwa" | short |
| Biometric failed | "Biometric enrollment failed" | "Usajili wa biometric umeshindwa" | long |
| Logout confirmed | "Logged out successfully" | "Umetoka" | short |

## Bottom Navigation Integration

Settings tab:
```kotlin
NavigationBarItem(
  icon = { Icon(Icons.Outlined.Settings, i18n.section_about) },
  label = { Text(i18n.screen_title) },  // localized
  selected = currentRoute == "settings"
)
```

Tab label updates automatically when language changes (collectAsState from DataStore).

---

# SECTION 7: COMPONENT STATE MATRIX

## Language Selection Radio Button

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| LanguageRadioOption | default (unselected) | surface (#FAFAFA) | onSurface (#1C1C1C) | none | none | true | true |
| LanguageRadioOption | selected | surface (#FAFAFA) | primary (#2E7D32) | none | none | true | true |
| LanguageRadioOption | pressed | primaryContainer (#A6F1A6) | primary (#2E7D32) | primary 1dp (#2E7D32) | none | true | true |
| LanguageRadioOption | focused | surface (#FAFAFA) | primary (#2E7D32) | primary 2dp focus ring | none | true | true |
| LanguageRadioOption | disabled | surfaceVariant (#DEE5DA) | onSurfaceVariant 38% alpha | none | none | false | true |
| LanguageRadioOption | loading | surfaceVariant (#DEE5DA) | onSurfaceVariant (#424942) | none | none | false | true |

## Settings Section Header

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| SectionHeader | default | surface (#FAFAFA) | primary (#2E7D32) | bottom divider outline 1dp | none | N/A | true |
| SectionHeader | focused | surface (#FAFAFA) | primary (#2E7D32) | primary 2dp | none | N/A | true |

## PIN Change Button

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| PINChangeButton | default | surface (#FAFAFA) | onSurface (#1C1C1C) | outline 1dp (#727971) | none | true | true |
| PINChangeButton | pressed | surfaceVariant (#DEE5DA) | onSurface (#1C1C1C) | outline 2dp (#727971) | none | true | true |
| PINChangeButton | focused | surface (#FAFAFA) | onSurface (#1C1C1C) | primary 2dp focus ring | none | true | true |
| PINChangeButton | disabled | surfaceVariant (#DEE5DA) | onSurfaceVariant 38% alpha | none | none | false | true |
| PINChangeButton | loading | surfaceVariant (#DEE5DA) | onSurfaceVariant (#424942) | none | none | false | true |
| PINChangeButton | error | errorContainer (#FFDAD6) | onErrorContainer (#410002) | error 2dp (#D32F2F) | none | true | true |
| PINChangeButton | success | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | primary 1dp (#2E7D32) | none | false | true |

## Logout Button (Destructive)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| LogoutButton | default | error (#D32F2F) | onError (#FFFFFF) | none | elevation 1dp | true | true |
| LogoutButton | pressed | errorContainer (#FFDAD6) | onErrorContainer (#410002) | error 2dp | none | true | true |
| LogoutButton | focused | error (#D32F2F) | onError (#FFFFFF) | white 3dp focus ring | elevation 1dp | true | true |
| LogoutButton | disabled | surfaceVariant (#DEE5DA) | onSurfaceVariant 38% alpha | none | none | false | true |
| LogoutButton | loading | errorContainer (#FFDAD6) | onErrorContainer (#410002) | none | none | false | true |

## Theme Toggle Switch (Light/Dark/System)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| ThemeSwitch | default off | surfaceVariant (#DEE5DA) | outline (#727971) | none | none | true | true |
| ThemeSwitch | default on | primary (#2E7D32) | onPrimary (#FFFFFF) | none | none | true | true |
| ThemeSwitch | pressed | primaryContainer (#A6F1A6) | primary (#2E7D32) | none | none | true | true |
| ThemeSwitch | focused | primary (#2E7D32) | onPrimary (#FFFFFF) | primary 3dp focus ring | none | true | true |
| ThemeSwitch | disabled | surfaceVariant (#DEE5DA) 50% | onSurfaceVariant 38% alpha | none | none | false | true |

---

# SECTION 8: API FAILURE & RECOVERY PLAYBOOK

## Endpoint: PUT /users/{userId}/preferences (language change)

| Failure | UX Response | Recovery |
|---------|-------------|----------|
| Network timeout | Apply language change locally (DataStore) immediately; queue remote sync | Exponential backoff: 1s → 2s → 4s; show snackbar "Language saved locally — will sync when online" |
| 401 Unauthorized | Navigate to LoginScreen; preserve selected language in DataStore (not lost) | Post-login, re-attempt PUT with stored preference |
| 404 Not Found | Local preference saved; log warning `language_pref_404`; snackbar "Settings saved locally" | No user-facing recovery — local-first always wins |
| 500 Server Error | Snackbar "Language saved — couldn't sync to server. Try again." | Manual retry via Settings > Sync; auto-retry on next app launch |
| Offline | Apply change immediately from DataStore; amber banner in settings "Offline — preferences saved locally" | Auto-sync on reconnect via NetworkMonitor |

## Endpoint: PUT /users/{userId}/pin (PIN change)

| Failure | UX Response | Recovery |
|---------|-------------|----------|
| Network timeout | Show loading indicator for ≤5s; then error dialog "Request timed out. Try again." | Retry button in dialog; exponential backoff: 1s → 2s → 4s |
| 401 Unauthorized | Dismiss dialog; navigate to LoginScreen with message "Session expired — please log in again" | PIN change must be re-attempted after fresh login |
| 422 Validation error | Inline error under current PIN field: "Incorrect current PIN" (red, #D32F2F) | Focus current PIN field; clear entered text |
| 500 Server Error | Snackbar "PIN change failed. Please try again." (long, 8s) | Retry button; if 3 consecutive failures, show "Contact support" link |
| Offline | Dialog: "Cannot change PIN offline. Connect to internet and try again." | Disable PIN change flow when offline; re-enable on reconnect |

## Endpoint: POST /auth/logout (logout)

| Failure | UX Response | Recovery |
|---------|-------------|----------|
| Network timeout | Complete local logout (clear token, clear DataStore auth); navigate to LoginScreen regardless | No retry — local logout is always final |
| 401 Unauthorized | Token already invalid — treat as success; complete local logout | Navigate to LoginScreen |
| 500 Server Error | Complete local logout; snackbar on LoginScreen "You've been logged out (server error — session will expire automatically)" | No recovery needed — local state cleared |
| Offline | Complete local logout; clear all local auth tokens; navigate to LoginScreen | Server-side session will expire via TTL |

## Endpoint: GET /users/{userId}/preferences (settings load)

| Failure | UX Response | Recovery |
|---------|-------------|----------|
| Network timeout | Show cached preferences from DataStore | Retry silently in background; no user-visible indicator unless cache is empty |
| 401 Unauthorized | Navigate to LoginScreen | Standard auth recovery flow |
| 404 Not Found | Use app defaults (EN language, system theme, biometric off) | Log event `preferences_404`; do not show error to user |
| 500 Server Error | Use cached DataStore values; no error shown | Background retry on next app foreground |
| Offline | Load from DataStore cache; no error — local-first design | Auto-sync on reconnect |

## Language Switch Local-First Protocol

```
User selects language →
  1. Write new locale to DataStore<Preferences> immediately (synchronous-like via runBlocking scoped)
  2. Trigger Activity.recreate() via LocalContext
  3. Compose tree recomposes with new locale — all strings update in <100ms
  4. Queue remote preference sync (fire-and-forget coroutine)
  5. If remote sync fails: local value persists; retry on next launch
  6. No snackbar shown for successful language switch (visual restart is confirmation)
```

---

# SECTION 9: SCREEN READER & ACCESSIBILITY DEEP DIVE

## Settings Screen — Focus Order

1. TopAppBar title — role = Heading, text = localized screen title (e.g. "Mipangilio" in Swahili)
2. "Language" section header — role = Heading level 2
3. English radio option — role = RadioButton; "English, selected" or "English, not selected"
4. Kiswahili radio option — role = RadioButton; "Kiswahili" (in target language) / "Swahili" (English descriptor)
5. Français radio option — role = RadioButton; "Français" / "French"
6. हिन्दी radio option — role = RadioButton; "हिन्दी" / "Hindi"
7. "Appearance" section header — role = Heading level 2
8. Theme options: System / Light / Dark radio buttons
9. "Security" section header — role = Heading level 2
10. Biometric toggle switch — "Enable biometric unlock, switch, currently off/on"
11. "Change PIN" button — role = Button; "Change PIN"
12. "About" section header — role = Heading level 2
13. App version row — role = none; contentDescription = "App version 1.0.0"
14. Logout button — role = Button; "Log out of MifosSave, double-tap to confirm"

## TalkBack Announcement Strings

| Element | TalkBack String |
|---------|----------------|
| Language selection (on change) | "Language changed to {language_name}. App is restarting to apply changes." |
| Radio selected | "{language_name} selected" |
| Biometric toggle on | "Biometric unlock enabled" |
| Biometric toggle off | "Biometric unlock disabled" |
| PIN change success | "PIN updated successfully" |
| PIN change error | "PIN change failed. Check your current PIN and try again." |
| Logout confirmation dialog | "Are you sure you want to log out? You will need your credentials to sign back in." |
| Logout confirm button | "Log out, double-tap to confirm" |
| Logout cancel button | "Cancel logout" |
| Settings loading | "Loading your settings" (liveRegion = Polite) |
| Settings loaded | "Settings loaded" (liveRegion = Polite) |

## Content Descriptions — All Icons

| Icon | Composable | contentDescription |
|------|-----------|-------------------|
| Icons.Outlined.Settings | BottomNavItem | "Settings" (localized: "Mipangilio") |
| Icons.Outlined.Language | Language section header icon | "Language settings" |
| Icons.Outlined.Palette | Appearance section header icon | "Appearance settings" |
| Icons.Outlined.Security | Security section header icon | "Security settings" |
| Icons.Outlined.Info | About section header icon | "About MifosSave" |
| Icons.Outlined.Fingerprint | Biometric toggle icon | "Fingerprint" |
| Icons.Outlined.Lock | PIN section icon | "PIN security" |
| Icons.Outlined.Logout | Logout button icon | "Log out" |
| Icons.Outlined.CheckCircle | Radio selected indicator | "Selected" |
| Icons.Outlined.RadioButtonUnchecked | Radio unselected | "Not selected" |

## Live Region Announcements

```kotlin
// Language change triggers activity restart — announce before restart
LaunchedEffect(selectedLanguage) {
    if (previousLanguage != null && previousLanguage != selectedLanguage) {
        // Announce via AccessibilityManager before recreate()
        accessibilityManager.announceForAccessibility(
            "Language changed to $selectedLanguageName. App restarting."
        )
        delay(500) // Allow announcement to complete
        activity.recreate()
    }
}

// Settings save success
Text(
    text = saveSuccessMessage,
    modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite }
)
```

## WCAG AA Contrast Ratios

| Foreground | Background | Ratio | Pass AA |
|------------|------------|-------|---------|
| onPrimary #FFFFFF | primary #2E7D32 | 7.1:1 | Pass (AA + AAA) |
| onPrimaryContainer #002106 | primaryContainer #A6F1A6 | 8.2:1 | Pass (AA + AAA) |
| onSurface #1C1C1C | surface #FAFAFA | 16.1:1 | Pass (AA + AAA) |
| onSurfaceVariant #424942 | surfaceVariant #DEE5DA | 5.9:1 | Pass (AA) |
| onError #FFFFFF | error #D32F2F | 4.5:1 | Pass (AA) |
| onErrorContainer #410002 | errorContainer #FFDAD6 | 12.4:1 | Pass (AA + AAA) |
| outline #727971 | surface #FAFAFA | 4.6:1 | Pass (AA) |

## Multi-Script Rendering Notes (Accessibility)

- Noto Sans supports all four target scripts: Latin (EN/FR), Latin-extended (SW), Devanagari (HI)
- Font size minimum: 12sp (bodySmall) — no text smaller than 12sp used in settings
- Line height: auto (1.4× for Latin, 1.6× for Devanagari to accommodate ascenders/descenders)
- No custom font sizes in Devanagari — Noto Sans handles script-appropriate sizing automatically

---

# SECTION 10: ANIMATION & MOTION SPEC

## Screen Enter / Exit Animations

| Screen | Enter | Exit |
|--------|-------|------|
| SettingsScreen | fadeIn(tween(250)) + slideInVertically(+60px → 0, tween(250)) | fadeOut(tween(200)) |
| PINChangeDialog | scaleIn(0.85 → 1.0, tween(300, EmphasizedDecelerate)) + fadeIn(300ms) | scaleOut(1.0 → 0.85, tween(200)) + fadeOut(200ms) |
| LogoutConfirmDialog | fadeIn(200ms) + scaleIn(0.92 → 1.0, tween(200)) | fadeOut(150ms) |
| Language restart (Activity.recreate) | System default activity transition (no custom override — OS handles) | — |

## State Transition Animations

| Transition | Duration | Easing |
|------------|----------|--------|
| Radio button: unselected → selected | 200ms color fill | FastOutSlowIn |
| Toggle switch on → off | 150ms thumb slide + 150ms track color | LinearEasing |
| Section expand/collapse (future) | 250ms height + 200ms fade | EaseInOutCubic |
| Biometric toggle success ripple | 300ms radial ripple, primary color | EaseOutCubic |
| Save success checkmark | 400ms path draw animation | EaseOutCubic |

## Language Change Visual Transition

```
User taps language radio →
  Radio animates: 200ms fill to primary color
  Delay 300ms (user sees confirmation)
  Fade out entire screen: 200ms
  Activity.recreate() called
  New activity fades in: OS default (300ms)
  All strings render in new language
  DataStore write: async, non-blocking
```

## BottomSheet: PIN Change (if implemented as sheet)

- Enter: `slideInVertically(fullHeight → 0, tween(350, EmphasizedDecelerateEasing))`
- Drag handle: 32dp wide, 4dp tall, onSurfaceVariant color
- Scrim: black 32% alpha, fadeIn 200ms
- Exit: `slideOutVertically(0 → fullHeight, tween(300))`

## Pull-to-Refresh (Settings Screen)

Settings screen does not support pull-to-refresh. Data is loaded once on entry; manual refresh via Settings > tap "Refresh preferences" menu item (overflow menu, hidden by default unless offline banner visible).

---

# SECTION 11: TEST & QA ANNOTATIONS

## UI Test Tags

| Composable | testTag |
|-----------|---------|
| SettingsScreen root | `"SettingsScreen"` |
| Language section | `"LanguageSection"` |
| RadioOption English | `"LanguageOption_EN"` |
| RadioOption Swahili | `"LanguageOption_SW"` |
| RadioOption French | `"LanguageOption_FR"` |
| RadioOption Hindi | `"LanguageOption_HI"` |
| Appearance section | `"AppearanceSection"` |
| Theme System radio | `"ThemeOption_System"` |
| Theme Light radio | `"ThemeOption_Light"` |
| Theme Dark radio | `"ThemeOption_Dark"` |
| Biometric toggle | `"BiometricToggle"` |
| PIN change button | `"PINChangeButton"` |
| Logout button | `"LogoutButton"` |
| Logout confirm dialog | `"LogoutConfirmDialog"` |
| Logout confirm action | `"LogoutConfirm_Yes"` |
| Logout cancel action | `"LogoutConfirm_Cancel"` |
| OfflineBanner | `"SettingsOfflineBanner"` |

## Required Test Scenarios

### Screen: SettingsScreen — Language Switching

**Given** the user is on the Settings screen with English selected  
**When** they tap the Kiswahili radio button  
**Then** the radio animates to selected, the activity restarts, and all visible strings render in Swahili within 1s

---

**Given** the user is offline  
**When** they change language from English to Français  
**Then** the language change applies locally and immediately; offline banner remains visible; no error snackbar shown

---

**Given** the language preference server endpoint returns HTTP 500  
**When** the user changes language to Français  
**Then** the language change is applied locally; snackbar shows "Language saved — couldn't sync to server"; no crash

---

**Given** the user selects Hindi (हिन्दी)  
**When** the activity restarts  
**Then** all UI strings render in Hindi using Noto Sans Devanagari; no missing glyphs; no layout overflow

---

**Given** the user is on the Settings screen  
**When** a screen reader (TalkBack) is active and the user navigates by swipe  
**Then** all interactive elements are reachable in documented focus order; all radio options announce their state

### Screen: SettingsScreen — Security

**Given** the user taps "Change PIN"  
**When** they enter the wrong current PIN  
**Then** inline error "Incorrect current PIN" appears below the current PIN field in error color #D32F2F

---

**Given** the user taps Logout and the confirmation dialog appears  
**When** they tap "Log out" in the dialog  
**Then** all local tokens are cleared, DataStore auth is cleared, and navigation goes to LoginScreen

---

**Given** a member name is 50+ characters in the About section (e.g. very long organization name)  
**When** the about row renders  
**Then** text wraps correctly (max 2 lines) without overflow, no clipping

## Edge Cases

- Device language set to unsupported locale (e.g. Arabic): app defaults to English; no crash
- DataStore corrupted: app falls back to default EN + system theme; no crash
- Biometric hardware absent: Biometric toggle row is hidden (not disabled); testTag="BiometricToggle" returns not found
- PIN field: 4–6 digit numeric only; paste of non-numeric content silently stripped
- Logout during offline: completes locally; server session expires via TTL (no partial state)

---

# SECTION 12: i18n / LOCALIZATION SPEC

## String Keys with Translations

| Key | EN | SW (Swahili) | FR (French) |
|-----|----|--------------|-------------|
| `settings_screen_title` | "Settings" | "Mipangilio" | "Paramètres" |
| `settings_section_language` | "Language" | "Lugha" | "Langue" |
| `settings_section_appearance` | "Appearance" | "Muonekano" | "Apparence" |
| `settings_section_security` | "Security" | "Usalama" | "Sécurité" |
| `settings_section_about` | "About" | "Kuhusu" | "À propos" |
| `settings_language_en` | "English" | "Kiingereza" | "Anglais" |
| `settings_language_sw` | "Kiswahili" | "Kiswahili" | "Swahili" |
| `settings_language_fr` | "Français" | "Kifaransa" | "Français" |
| `settings_language_hi` | "Hindi" | "Kihindi" | "Hindi" |
| `settings_theme_system` | "System default" | "Mfumo chaguo-msingi" | "Système par défaut" |
| `settings_theme_light` | "Light" | "Mwanga" | "Clair" |
| `settings_theme_dark` | "Dark" | "Giza" | "Sombre" |
| `settings_biometric_label` | "Biometric Unlock" | "Kufungua kwa alama ya kidole" | "Déverrouillage biométrique" |
| `settings_biometric_sublabel` | "Use fingerprint or face to unlock" | "Tumia alama ya kidole au uso kufungua" | "Utiliser l'empreinte ou le visage" |
| `settings_pin_change` | "Change PIN" | "Badilisha PIN" | "Modifier le PIN" |
| `settings_pin_current` | "Current PIN" | "PIN ya sasa" | "PIN actuel" |
| `settings_pin_new` | "New PIN" | "PIN mpya" | "Nouveau PIN" |
| `settings_pin_confirm` | "Confirm new PIN" | "Thibitisha PIN mpya" | "Confirmer le nouveau PIN" |
| `settings_pin_success` | "PIN updated successfully" | "PIN imebadilishwa" | "PIN modifié avec succès" |
| `settings_pin_error` | "PIN change failed. Check current PIN." | "Imeshindwa kubadilisha PIN" | "Échec du changement de PIN" |
| `settings_logout_label` | "Log Out" | "Toka" | "Se déconnecter" |
| `settings_logout_confirm_title` | "Log out of MifosSave?" | "Toka kwenye MifosSave?" | "Se déconnecter de MifosSave ?" |
| `settings_logout_confirm_body` | "You will need your credentials to log back in." | "Utahitaji neno lako la siri kuingia tena." | "Vous aurez besoin de vos identifiants pour vous reconnecter." |
| `settings_logout_confirm_yes` | "Log Out" | "Toka" | "Se déconnecter" |
| `settings_logout_confirm_cancel` | "Cancel" | "Ghairi" | "Annuler" |
| `settings_app_version` | "Version {version}" | "Toleo {version}" | "Version {version}" |
| `settings_offline_banner` | "Offline — preferences saved locally" | "Nje ya mtandao — mipangilio imehifadhiwa" | "Hors ligne — préférences sauvegardées" |

## Number Formatting — KES (not applicable to Settings, but for consistency)

Settings screen does not display KES amounts directly. All amounts in reports and savings screens use:

| Amount | Formatted (en-KE) |
|--------|-------------------|
| 1000 | KES 1,000.00 |
| 48500 | KES 48,500.00 |
| 1234.5 | KES 1,234.50 |

```kotlin
val numberFormat = NumberFormat.getCurrencyInstance(Locale("en", "KE"))
// Returns: KES 48,500.00
```

## Date Formatting — en-KE Locale

| Format | Pattern | Example |
|--------|---------|---------|
| Short date | dd/MM/yyyy | 06/05/2026 |
| Long date | d MMMM yyyy | 6 May 2026 |
| App version date | yyyy | 2026 |

```kotlin
val dateFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy", Locale("en", "KE"))
```

## Font Loading Strategy (Multi-Script)

```kotlin
// Noto Sans with Devanagari support
val notoSans = FontFamily(
    Font(R.font.noto_sans_regular, FontWeight.Normal),
    Font(R.font.noto_sans_medium, FontWeight.Medium),
    Font(R.font.noto_sans_bold, FontWeight.Bold),
    Font(R.font.noto_sans_devanagari_regular, FontWeight.Normal),
    Font(R.font.noto_sans_devanagari_medium, FontWeight.Medium),
)
// Android's TextPaint automatically selects the correct font for each Unicode range
// No manual script selection needed — Noto Sans handles fallback internally
```

## Locale Resolution at Runtime

```kotlin
object LocaleManager {
    fun applyLocale(context: Context, languageCode: String): Context {
        val locale = Locale(languageCode)
        Locale.setDefault(locale)
        val config = context.resources.configuration
        config.setLocale(locale)
        return context.createConfigurationContext(config)
    }
}
// Called in Application.attachBaseContext() and Activity.attachBaseContext()
// Language code stored in DataStore<Preferences> key = "selected_language"
```
