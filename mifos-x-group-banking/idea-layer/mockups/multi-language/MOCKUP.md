# Multi-Language — Mockup Specification
**Feature**: multi-language | **Screen**: settings
**Requirement**: FR-010

---

## Design Language

**System**: Material Design 3, comfortable density
**Font**: Noto Sans (supports all 4 languages including Devanagari for Hindi)
**Primary**: #2E7D32 — TopAppBar, section headers, selected radio indicator
**Error container**: errorContainer #FFDAD6 — Logout button
**Min touch target**: 56dp for all settings rows and radio options

---

## Screen: Settings — Full Layout (English, SYSTEM theme selected)
```
┌─────────────────────────────────────────┐
│  Settings                               │  TopAppBar — primary #2E7D32 bg, onPrimary
│                                         │  No back navigation — bottom nav
├─────────────────────────────────────────┤
│  Language                               │  Section header — primary text, labelLarge, 16dp pad
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │  RadioGroup card — surface, cornerRadius 12dp
│ │ [🇬🇧] English        ● (selected)   │ │  RadioOption row — 56dp min, primaryContainer bg
│ │       English                       │ │  label: bodyLarge; sublabel: bodySmall onSurfaceVariant
│ │ ─── ─── ─── ─── ─── ─── ─── ───    │ │  Divider 1dp outline
│ │ [🇰🇪] Kiswahili      ○              │ │  Unselected — surface bg
│ │       Swahili                       │ │
│ │ ─── ─── ─── ─── ─── ─── ─── ───    │ │
│ │ [🇫🇷] Français       ○              │ │
│ │       French                        │ │
│ │ ─── ─── ─── ─── ─── ─── ─── ───    │ │
│ │ [🇮🇳] हिन्दी          ○              │ │  Noto Sans Devanagari rendering
│ │       Hindi                         │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Appearance                             │  Section header — primary text
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │ [☀️] Light            ○              │ │
│ │ [🌙] Dark             ○              │ │
│ │ [◑] System Default    ● (selected)  │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Security                               │  Section header
├─────────────────────────────────────────┤
│ [🔬] Biometric Unlock         [○–]     │  SettingsRow — biometric toggle OFF
│      Use fingerprint or face ID         │  Switch enabled (hardware available)
│ ─── ─── ─── ─── ─── ─── ─── ─── ───  │
│ [🔒] Change PIN               [›]      │  SettingsRow — chevron trailing
│      Update your 4-digit security PIN   │
├─────────────────────────────────────────┤
│  Notifications                          │  Section header
├─────────────────────────────────────────┤
│ [🔔] Push Notifications       [●–]     │  SettingsRow — notifications toggle ON
│      Receive alerts for meetings...     │
├─────────────────────────────────────────┤
│  About                                  │  Section header
├─────────────────────────────────────────┤
│ [ℹ] App Version                        │  SettingsRow — no trailing
│      1.0.0 (Build 42)                   │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │  [→] Logout                         │ │  Button — errorContainer bg #FFDAD6
│ └─────────────────────────────────────┘ │  onErrorContainer text #410002, 16dp margin
└─────────────────────────────────────────┘
```

---

## Screen: Settings — Kiswahili Language Selected
```
┌─────────────────────────────────────────┐
│  Mipangilio                             │  Title in Kiswahili
├─────────────────────────────────────────┤
│  Lugha                                  │  "Language" in Swahili
├─────────────────────────────────────────┤
│ [🇬🇧] Kiingereza       ○               │  "English" in Swahili
│ [🇰🇪] Kiswahili        ● (selected)    │
│ [🇫🇷] Kifaransa        ○               │  "French" in Swahili
│ [🇮🇳] Kihindi          ○               │  "Hindi" in Swahili
├─────────────────────────────────────────┤
│  Usalama                                │  "Security" in Swahili
├─────────────────────────────────────────┤
│ [🔬] Ufunguzi wa Biometric    [○–]     │
│ [🔒] Badilisha PIN            [›]      │  "Change PIN" in Swahili
│ ─── ─── ─── ─── ─── ─── ─── ─── ───  │
│ [→] Toka                               │  "Logout" in Swahili
└─────────────────────────────────────────┘
```

---

## Screen: Settings — Hindi (हिन्दी) Selected
```
┌─────────────────────────────────────────┐
│  सेटिंग्स                               │  Devanagari title
├─────────────────────────────────────────┤
│  भाषा                                   │  "Language" in Hindi
├─────────────────────────────────────────┤
│ [🇬🇧] अंग्रेज़ी         ○              │
│ [🇰🇪] स्वाहिली          ○              │
│ [🇫🇷] फ्रेंच            ○              │
│ [🇮🇳] हिन्दी             ● (selected)   │  Noto Sans Devanagari
├─────────────────────────────────────────┤
│  सुरक्षा                                │  "Security" in Hindi
│ [🔬] बायोमेट्रिक अनलॉक    [○–]        │
│ [🔒] PIN बदलें             [›]         │
│ [→] लॉग आउट                            │
└─────────────────────────────────────────┘
```

---

## Change PIN Dialog
```
┌─────────────────────────────────────────┐
│  Change PIN                 [×]         │  AlertDialog title, dismiss icon
├─────────────────────────────────────────┤
│  Current PIN                            │  OutlinedTextField
│  ┌─────────────────────────────────┐   │  input_type: password, keyboard: number
│  │  ● ● ● ●                       │   │  48dp height
│  └─────────────────────────────────┘   │
│                                         │
│  New PIN (min 4 digits)                 │  OutlinedTextField
│  ┌─────────────────────────────────┐   │
│  │  ● ● ● ● ● ● ● ●               │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ● PIN change failed. Check your        │  Error text — error color, bodySmall
│    current PIN and try again.           │  Visible when pinChangeError != null
│                                         │
│  ┌────────────┐  ┌──────────────────┐  │
│  │   Cancel   │  │   Update PIN     │  │  TextButton + FilledButton
│  └────────────┘  └──────────────────┘  │  FilledButton: primary green
└─────────────────────────────────────────┘
```

---

## Component Specifications

### TopAppBar
| Property | Value |
|----------|-------|
| Background | primary #2E7D32 |
| Title | screen_title (localized) — titleLarge, onPrimary #FFFFFF |
| No back navigation | bottom nav entry point, no back |
| Elevation | 0dp (colored bar) |

### SectionHeader
| Property | Value |
|----------|-------|
| Text style | labelLarge |
| Text color | primary #2E7D32 |
| Padding | 16dp top, 16dp horizontal, 8dp bottom |
| Background | background #FAFAFA (not a card) |

### RadioGroup Card
| Property | Value |
|----------|-------|
| Background | surface #FAFAFA |
| Corner radius | 12dp |
| Elevation | 0dp |
| Margin | 0 horizontal, 0 vertical (LazyColumn spacedBy handles gaps) |

### RadioOptionRow
| Property | Value |
|----------|-------|
| Min height | 56dp |
| Padding | 12dp vertical, 16dp horizontal |
| Background selected | primaryContainer #A6F1A6 |
| Background unselected | surface #FAFAFA |
| Flag icon | 24dp, no tint (flag color preserved) |
| Label | bodyLarge — in target language (e.g., "Kiswahili") |
| Sublabel | bodySmall, onSurfaceVariant — in English descriptor (e.g., "Swahili") |
| Radio button | MD3 RadioButton, selected color = primary |
| Divider | 1dp, outline color, between options |

### SettingsRow
| Property | Value |
|----------|-------|
| Min height | 56dp |
| Padding | 0dp vertical (56dp set by min height), 16dp horizontal |
| Leading icon | 24dp, onSurfaceVariant |
| Label | bodyLarge, onSurface |
| Sublabel | bodySmall, onSurfaceVariant |
| Trailing — Switch | enabled when isBiometricAvailable; checked color primary |
| Trailing — Chevron | chevron_right icon, 20dp, onSurfaceVariant |
| Disabled biometric | opacity 0.38, hint text below sublabel: "Hardware not available" |

### LogoutButton
| Property | Value |
|----------|-------|
| Background | errorContainer #FFDAD6 |
| Text color | onErrorContainer #410002 |
| Leading icon | logout, 18dp |
| Corner radius | 12dp |
| Height | 56dp |
| Width | fill-maxWidth, 16dp margin |
| Loading state | CircularProgressIndicator 18dp replaces icon when isLoggingOut=true |

---

## Interaction Patterns

1. **Language selection**: Tap radio option → RadioButton animates to selected → primaryContainer bg fades in (200ms) → OnLanguageSelected dispatched → DataStore write → RestartComposableTree event → all visible text updates to new locale
2. **Theme selection**: Tap radio option → OnThemeSelected dispatched → MaterialTheme dynamically reapplies (300ms transition) — NO tree restart needed
3. **Biometric toggle**: Tap switch → if enabling and hardware unavailable → Show snackbar "Biometric hardware not available on this device" → toggle reverts; if enabling and hardware available → show BiometricPrompt enrollment flow
4. **Change PIN**: Tap row → ShowPinChangeDialog event → AlertDialog appears; Submit → validate → PUT /self/user/updatePassword
5. **Logout**: Tap Logout → ConfirmDialog appears; Confirm → isLoggingOut=true → button shows spinner → clear session + SQLDelight + DataStore → NavigateToLogin

---

## Accessibility

- Language radio group: role=radiogroup, each option has contentDescription "{language} language option, {selected/not selected}"
- Flag icons: contentDescription "{country} flag" (decorative but meaningful for language identification)
- Section headers: role=heading
- Biometric toggle: "Biometric unlock switch, {on/off}. {biometric hardware available/not available}"
- Change PIN row: "Change PIN button — opens PIN change dialog"
- App version: contentDescription "App version 1.0.0 build 42"
- Logout button: "Logout button — clears session and returns to login"
- Hindi text: font=Noto Sans, Devanagari script — system accessibility TalkBack reads Devanagari correctly
