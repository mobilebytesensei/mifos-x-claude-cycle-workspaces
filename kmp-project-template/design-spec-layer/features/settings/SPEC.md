# Feature Spec: settings

## Overview

App configuration including theme, language, notification preferences, and platform information.

## Screens

### SettingsScreen
- **ViewModel**: SettingsViewmodel
- **Layout**:
  - Top bar with title "Settings"
  - Theme section: Light/Dark/System toggle
  - Dynamic color toggle (Material You)
  - Language selector (opens LanguageDialog)
  - Notification settings link
  - Platform info display (via expect/actual Platform.kt)
  - About section
- **Dialogs**: LanguageDialog, SettingsDialog
- **Navigation**: Notification item → NotificationScreen
- **Requirements**: FR-006, FR-007, FR-009, FR-010

### NotificationScreen
- **Layout**:
  - Top bar with back navigation
  - Notification category toggles
  - Sound/vibration preferences
- **Navigation**: Back → SettingsScreen
- **Requirements**: FR-008

## Platform-Specific

- Platform.kt with expect/actual for: android, desktop, native, js, wasmJs
- Each provides platform name, version, device info

## DI

- SettingsModule provides: SettingsViewmodel
