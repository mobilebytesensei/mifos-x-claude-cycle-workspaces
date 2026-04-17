# Modules Index — kmp-project-template

| Module | Category | Screens | ViewModels | DI Module |
|--------|----------|:-------:|:----------:|-----------|
| feature:home | Core | 2 | 3 | HomeModule |
| feature:profile | Core | 1 | 0 | (shared) |
| feature:settings | Core | 2 | 1 | SettingsModule |
| cmp-navigation | Navigation | 3 | 3 | KoinModules |

---

## Screen → ViewModel Mapping

| Screen | Feature | ViewModel | Platform |
|--------|---------|-----------|----------|
| TasksScreen | home | TasksViewModel | All |
| EditTaskScreen | home | EditTaskViewModel | All |
| ProfileScreen | profile | - | All |
| SettingsScreen | settings | SettingsViewmodel | All |
| NotificationScreen | settings | - | All |
| SplashScreen | navigation | - | All |
| RootNavScreen | navigation | RootNavViewModel | All (platform-specific) |
| AuthenticatedNavbarScreen | navigation | AuthenticatedNavbarNavigationViewModel | All |
