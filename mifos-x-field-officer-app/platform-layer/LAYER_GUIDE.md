# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/platform-layer/LAYER_GUIDE.md"
# last_modified: "2026-03-19"

# Platform Layer Guide - mifos-x-field-officer-app

> Conventions for platform-specific implementations.

---

## Purpose

The platform layer contains platform-specific code that cannot be shared across all targets.

---

## Directory Structure

```
platform-layer/
├── LAYER_STATUS.md       # Implementation status
├── LAYER_GUIDE.md        # This file
├── TESTING_STATUS.md     # Platform test coverage
├── expect-actual/        # Expect/actual template index
│   └── README.md         # Template catalog and status
└── platforms/
    ├── ANDROID.md        # Android-specific
    ├── IOS.md            # iOS-specific
    ├── DESKTOP.md        # Desktop-specific
    └── WEB.md            # Web-specific
```

---

## Platforms Overview

| Platform | App Module | Source Set | Notes |
|----------|------------|------------|-------|
| Android | `cmp-android` | `androidMain` | Compose + Android APIs |
| iOS | `cmp-ios` | `iosMain` | SwiftUI interop |
| Desktop | `cmp-desktop` | `desktopMain` | JVM + Swing/AWT |
| Web | `cmp-web` | `jsMain`/`wasmMain` | Browser APIs |

---

## expect/actual Pattern

> **Source**: `references/templates/kmp-project-template/` (multiple modules)

### HTTP Client Engine (per-platform Ktor engine)

```kotlin
// commonMain — core-base/network/KtorHttpClient.kt
expect fun httpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient

// androidMain — uses OkHttp engine
actual fun httpClient(config: HttpClientConfig<*>.() -> Unit) = HttpClient(OkHttp) { config(this) }

// nativeMain (iOS/macOS) — uses Darwin engine
actual fun httpClient(config: HttpClientConfig<*>.() -> Unit) = HttpClient(Darwin) { config(this) }

// desktopMain — uses OkHttp engine
actual fun httpClient(config: HttpClientConfig<*>.() -> Unit) = HttpClient(OkHttp) { config(this) }

// jsMain / wasmJsMain — uses Js engine
actual fun httpClient(config: HttpClientConfig<*>.() -> Unit) = HttpClient(Js) { config(this) }
```

### Database Driver (per-platform Room setup)

```kotlin
// commonMain — core/database/di/DatabaseModule.kt
expect val platformModule: Module

// androidMain — uses AppDatabaseFactory with Android context
actual val platformModule: Module = module {
    single {
        AppDatabaseFactory(androidApplication())
            .createDatabase(
                databaseClass = AppDatabase::class.java,
                databaseName = AppDatabase.DATABASE_NAME,
            )
            .fallbackToDestructiveMigrationOnDowngrade(false)
            .setQueryCoroutineContext(Dispatchers.IO as CoroutineContext)
            .build()
    }
}

// desktopMain — uses BundledSQLiteDriver
actual val platformModule: Module = module {
    single {
        AppDatabaseFactory()
            .createDatabase<AppDatabase>(databaseName = AppDatabase.DATABASE_NAME)
            .fallbackToDestructiveMigrationOnDowngrade(false)
            .setDriver(BundledSQLiteDriver())
            .setQueryCoroutineContext(Dispatchers.IO as CoroutineContext)
            .build()
    }
}

// nativeMain (iOS/macOS) — uses BundledSQLiteDriver
actual val platformModule: Module = module {
    single {
        AppDatabaseFactory()
            .createDatabase<AppDatabase>(databaseName = AppDatabase.DATABASE_NAME)
            .fallbackToDestructiveMigrationOnDowngrade(false)
            .setDriver(BundledSQLiteDriver())
            .setQueryCoroutineContext(get<CoroutineDispatcher>(named(AppDispatchers.IO.name)) as CoroutineContext)
            .build()
    }
}
```

### Dispatcher Module

```kotlin
// commonMain — core-base/common/di/CommonModule.kt
expect val dispatcherManagerModule: Module

// androidMain — Android-specific dispatchers
actual val dispatcherManagerModule: Module = module { /* Android dispatchers */ }

// nonAndroidMain — Default dispatchers for iOS/Desktop/Web
actual val dispatcherManagerModule: Module = module { /* Default dispatchers */ }
```

### Other Common expect/actual Declarations

```kotlin
// Platform identification
expect fun getPlatform(): Platform
expect fun supportsDynamicTheming(): Boolean

// Compose integration
expect fun LocalManagerProvider(content: @Composable () -> Unit)
expect fun TrackScrollJank(scrollableState: ScrollableState, stateName: String)

// Analytics
expect val analyticsModule: Module
```

---

## Platform DI Composition (Koin)

> **Source**: `references/templates/kmp-project-template/cmp-navigation/src/commonMain/kotlin/cmp/navigation/di/KoinModules.kt`

### KoinModules (central composition)

```kotlin
object KoinModules {
    private val dataModule = module { includes(DataModule) }
    private val dispatcherModule = module { includes(CommonModule) }

    private val AppModule = module {
        includes(platformModule)           // expect/actual per platform
        viewModelOf(::AppViewModel)
        viewModelOf(::RootNavViewModel)
    }

    private val featureModule = module {
        includes(HomeModule, SettingsModule)
    }

    val allModules = listOf(
        dataModule, dispatcherModule, analyticsModule,
        DatastoreModule, featureModule, AppModule,
    )
}
```

### initKoin (shared entry point)

```kotlin
// cmp-shared/src/commonMain/kotlin/.../KoinExt.kt
fun initKoin(config: KoinAppDeclaration? = null) {
    startKoin {
        config?.invoke(this)
        modules(KoinModules.allModules)
    }
}
```

### Per-Platform Koin Initialization

| Platform | Where | How |
|----------|-------|-----|
| Android | `AndroidApp.onCreate()` | `initKoin { androidContext(this); androidLogger() }` |
| iOS | `ViewController.kt configure` | `initKoin()` |
| Desktop | `main.kt` | `initKoin()` |
| Web | `Application.kt / Main.kt` | `initKoin()` |

> Android is the only platform that passes platform-specific config (`androidContext`, `androidLogger`). All other platforms call `initKoin()` with no arguments.

---

## Platform-Specific Features

### Android
- Permissions handling
- Background services
- Notifications (FCM)
- Deep linking
- Widgets

### iOS
- App delegate callbacks
- Push notifications (APNs)
- Universal links
- App extensions

### Desktop
- Window management
- System tray
- File system access
- Native menus

### Web
- Browser storage
- Service workers
- Web APIs
- Responsive design

---

## Platform Considerations

| Concern | Android | iOS | Desktop | Web |
|---------|---------|-----|---------|-----|
| Storage | DataStore | UserDefaults | Preferences | LocalStorage |
| Auth | BiometricPrompt | FaceID/TouchID | System keychain | WebAuthn |
| Network | OkHttp | URLSession | Java HTTP | Fetch API |
| UI | Compose | SwiftUI | Compose Desktop | DOM/Canvas |

---

## Expect/Actual Catalog

See [expect-actual/README.md](expect-actual/README.md) for the full template index and project status.

> **Framework templates**: `templates/instructions/platform-layer/expect-actual/`
> **Master catalog**: `templates/instructions/platform-layer/EXPECT_ACTUAL_CATALOG.md`

The `/implement` command auto-detects required expect/actual declarations from feature specs
and generates them from templates. See the README in `expect-actual/` for details.

---

## Commands

| Command | Purpose |
|---------|---------|
| `/gap-analysis platform` | Check platform gaps |
| `/implement [feature]` | Auto-generates platform code |
