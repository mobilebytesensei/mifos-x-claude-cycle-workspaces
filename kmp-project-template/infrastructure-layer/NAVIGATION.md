# Navigation — kmp-project-template

## Route Registry

| Route | Type | Screen | Auth Required |
|-------|------|--------|:-------------:|
| SplashNavigation | @Serializable | SplashScreen | ❌ |
| RootNavNavigation | @Serializable | RootNavScreen | ❌ |
| AuthenticatedNavigation | @Serializable | AuthenticatedNavbarScreen | ✅ |
| TasksDestination | Feature route | TasksScreen | ✅ |
| EditTask | Feature route | EditTaskScreen | ✅ |
| SettingsRoute | Feature route | SettingsScreen | ✅ |
| ProfileRoute | Feature route | ProfileScreen | ✅ |

## Navigation Graph

```
SplashScreen → RootNavScreen → AuthenticatedNavbar
                                    ├── Home (TasksScreen)
                                    │     └── EditTaskScreen
                                    ├── Profile (ProfileScreen)
                                    └── Settings (SettingsScreen)
                                          └── NotificationScreen
```

## Adaptive Navigation

| Screen Size | Navigation Type | Component |
|-------------|----------------|-----------|
| Compact (phone) | Bottom Navigation Bar | KptBottomBar |
| Medium (tablet) | Navigation Rail | KptNavigationRail |
| Expanded (desktop) | Permanent Navigation Rail | AdaptiveNavigationSuiteScaffold |
