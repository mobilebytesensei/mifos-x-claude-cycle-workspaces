# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/platform-layer/platforms/ANDROID.md"
# last_modified: "2026-03-19"

# Android Platform

## Module: cmp-android

> Primary platform target for Mifos Mobile

---

## Build Flavors

| Flavor | API Base | Use Case |
|--------|----------|----------|
| demo | tt.mifos.community | Development/Testing |
| prod | Configurable | Production |

---

## Build Commands

| Command | Output |
|---------|--------|
| `./gradlew :cmp-android:assembleDemoDebug` | Demo debug APK |
| `./gradlew :cmp-android:assembleDemoRelease` | Demo release APK |
| `./gradlew :cmp-android:assembleProdDebug` | Prod debug APK |
| `./gradlew :cmp-android:assembleProdRelease` | Production release APK |
| `./gradlew :cmp-android:lintRelease` | Lint checks |
| `./gradlew :cmp-android:testDebug` | Run unit tests |

---

## Key Files

| File | Purpose |
|------|---------|
| `cmp-android/build.gradle.kts` | Module configuration |
| `cmp-android/src/main/AndroidManifest.xml` | App manifest |
| `cmp-android/src/main/kotlin/.../MainActivity.kt` | Entry point activity |
| `cmp-android/src/main/kotlin/.../AndroidApp.kt` | Application class (Koin init) |

---

## Gradle Configuration

```kotlin
android {
    namespace = "org.mifos.mobile"
    compileSdk = 34

    defaultConfig {
        applicationId = "org.mifos.mobile"
        minSdk = 24
        targetSdk = 34
    }

    productFlavors {
        create("demo") { ... }
        create("prod") { ... }
    }
}
```

---

## MainActivity Pattern

> **Source**: `references/templates/kmp-project-template/cmp-android/src/main/kotlin/cmp/android/app/MainActivity.kt`

```kotlin
class MainActivity : AppCompatActivity() {

    private lateinit var appUpdateManager: AppUpdateManager

    private val userPreferencesRepository: UserDataRepository by inject()
    private val networkMonitor: NetworkMonitor by inject()
    private val analyticsHelper: AnalyticsHelper by inject()

    override fun onCreate(savedInstanceState: Bundle?) {
        var shouldShowSplashScreen = true
        installSplashScreen().setKeepOnScreenCondition { shouldShowSplashScreen }

        super.onCreate(savedInstanceState)
        appUpdateManager = AppUpdateManagerImpl(this)

        setupEdgeToEdge(darkThemeConfigFlow)

        ShareUtils.setActivityProvider { return@setActivityProvider this }
        FileKit.init(this)

        setContent {
            SharedApp(
                onSplashScreenRemoved = {
                    shouldShowSplashScreen = false
                },
            )
        }
    }
}
```

**Key elements:**
- Extends `AppCompatActivity()` (or `ComponentActivity()` in simpler exemplars)
- Uses `installSplashScreen()` with keep-on-screen condition
- Injects dependencies via Koin (`by inject()` or `by viewModel()`)
- Initializes `FileKit.init(this)` and `ShareUtils.setActivityProvider`
- Calls `SharedApp()` composable from `cmp-shared` module in `setContent`

---

## Application Class Pattern

> **Source**: `references/templates/kmp-project-template/cmp-android/src/main/kotlin/cmp/android/app/AndroidApp.kt`

```kotlin
class AndroidApp : Application(), SingletonImageLoader.Factory, KoinComponent {

    private val userDataRepository: UserDataRepository by inject()

    override fun onCreate() {
        super.onCreate()
        initKoin {
            androidContext(this@AndroidApp)
            androidLogger()
        }
    }

    override fun newImageLoader(context: PlatformContext): ImageLoader =
        getDefaultImageLoader(context)
            .newBuilder()
            .diskCachePolicy(CachePolicy.ENABLED)
            .diskCache {
                DiskCache.Builder()
                    .directory(context.cacheDir.resolve("image_cache"))
                    .maxSizePercent(0.25)
                    .build()
            }
            .build()
}
```

**Key elements:**
- Declared in `AndroidManifest.xml` as `android:name=".AndroidApp"`
- Calls `initKoin { androidContext(...); androidLogger() }` in `onCreate`
- Implements `SingletonImageLoader.Factory` for Coil image loading
- Implements `KoinComponent` for dependency injection access

---

## Signing Configuration

### Debug
- Auto-generated debug keystore
- Location: `~/.android/debug.keystore`

### Release
- Requires `keystore.properties` file
- Keys: `storeFile`, `storePassword`, `keyAlias`, `keyPassword`

---

## Dependencies

| Category | Key Dependencies |
|----------|------------------|
| Compose | Compose BOM, Material3 |
| DI | Koin Android |
| Network | Ktor Android |
| Storage | DataStore, Room |

---

## Android-Specific Features

| Feature | Implementation |
|---------|----------------|
| Biometrics | AndroidX Biometric |
| Push Notifications | Firebase Cloud Messaging |
| Deep Links | Intent Filters |
| Splash Screen | SplashScreen API |

---

## ProGuard/R8

- Rules in `proguard-rules.pro`
- Keep rules for serialization
- Ktor client rules

---

## Related

- [LAYER_STATUS.md](../LAYER_STATUS.md) - Platform overview
- [LAYER_GUIDE.md](../LAYER_GUIDE.md) - Architecture patterns
