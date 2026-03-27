# Dependency Injection — kmp-project-template

## Framework: Koin

## Module Hierarchy

```
KoinModules (root — cmp-navigation)
├── DataModule (core:data)
│   ├── DatastoreModule (core:datastore)
│   │   └── UserPreferencesRepositoryImpl → UserPreferencesRepository
│   ├── platformModule (core-base:common)
│   ├── CommonModule (core-base:common)
│   │   └── DispatchManagerImpl → DispatcherManager
│   ├── NetworkMonitorImpl → NetworkMonitor
│   ├── UserDataRepositoryImpl → UserDataRepository
│   └── UserLogoutManagerImpl → UserLogoutManager
├── HomeModule (feature:home)
│   ├── StorageServiceImpl → StorageService
│   ├── viewModelOf(::TasksViewModel)
│   └── viewModelOf(::EditTaskViewModel)
├── SettingsModule (feature:settings)
│   └── viewModelOf(::SettingsViewmodel)
├── analyticsModule (core-base:analytics — platform-specific)
│   ├── Android: FirebaseAnalyticsHelper
│   ├── iOS/macOS: FirebaseAnalyticsHelper
│   └── Desktop/Web: NoOpAnalyticsHelper
├── platformModule (core-base:platform)
│   ├── IntentManagerImpl → IntentManager
│   ├── AppReviewManagerImpl → AppReviewManager
│   └── AppUpdateManagerImpl → AppUpdateManager
└── DatabaseModule (core:database — platform-specific)
    ├── Android: RoomDatabase.Builder
    ├── Desktop: RoomDatabase.Builder
    ├── iOS: getRoomDatabase()
    └── Web: (not supported)
```

## Platform DI Variants

| Module | Android | iOS | Desktop | Web |
|--------|---------|-----|---------|-----|
| analyticsModule | Firebase | Firebase | NoOp | NoOp |
| DatabaseModule | Room | SQLite | Room | N/A |
| platformModule | Android impl | Native impl | Desktop impl | JS impl |
| CommonModule | Android dispatchers | Default | Default | Default |
