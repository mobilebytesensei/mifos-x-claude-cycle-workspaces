# Features — kmp-project-template

---

## Feature Registry

| Feature | Screens | Status | Version | Requirements |
|---------|:-------:|:------:|:-------:|-------------|
| home | 2 | ✅ Implemented | v1 | FR-001, FR-002, FR-003, FR-004, SFR-001, DR-003 |
| profile | 1 | ✅ Implemented | v1 | FR-005 |
| settings | 2 | ✅ Implemented | v1 | FR-006, FR-007, FR-008, FR-009, FR-010 |
| navigation | 2 | ✅ Implemented | v1 | FR-011, FR-012, FR-013 |

---

## Feature Details

### home
- **Screens**: TasksScreen, EditTaskScreen
- **ViewModels**: TasksViewModel, EditTaskViewModel, TaskMinderViewModel
- **Services**: StorageService (task CRUD), CacheManager (LRU cache)
- **Dependencies**: core:model, core:ui, core-base:ui
- **DI Module**: HomeModule

### profile
- **Screens**: ProfileScreen
- **ViewModels**: (uses shared state)
- **Dependencies**: core:model, core:ui
- **DI Module**: (shared)

### settings
- **Screens**: SettingsScreen, NotificationScreen
- **ViewModels**: SettingsViewmodel
- **Dialogs**: LanguageDialog, SettingsDialog
- **Platform**: expect/actual Platform.kt (android, desktop, native, js, wasmJs)
- **Dependencies**: core:model, core:datastore, core-base:designsystem
- **DI Module**: SettingsModule

### navigation
- **Screens**: SplashScreen, RootNavScreen, AuthenticatedNavbarNavigationScreen
- **ViewModels**: AppViewModel, RootNavViewModel, AuthenticatedNavbarNavigationViewModel
- **Routes**: RootNavNavigation, SplashNavigation, AuthenticatedNavigation
- **Dependencies**: All feature modules, core:data, core-base:platform
- **DI Module**: KoinModules (root orchestrator)

---

## Feature Dependencies

```
navigation → home, profile, settings
home → core:model, core:ui, core-base:ui
settings → core:model, core:datastore, core-base:designsystem
profile → core:model, core:ui
```

---

## State Matrix

### home (TasksScreen)

| State | Loading | Error | Empty | Success |
|-------|:-------:|:-----:|:-----:|:-------:|
| TasksUiState | selectedYear, selectedMonthIndex, selectedDayInMonth, weekdaysAndDaysInMonth | - | No tasks for date | Task list displayed |

### settings (SettingsScreen)

| State | Loading | Error | Empty | Success |
|-------|:-------:|:-----:|:-----:|:-------:|
| SettingsUiState | - | - | - | Theme, language, notification prefs displayed |
