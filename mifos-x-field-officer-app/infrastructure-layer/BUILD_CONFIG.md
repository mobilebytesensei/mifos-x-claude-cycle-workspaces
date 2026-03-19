# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/infrastructure-layer/BUILD_CONFIG.md"
# last_modified: "2026-03-19"

# Build Configuration

> **Purpose**: Document Gradle module structure, build variants, and version catalog.
> **Project Type**: KMP (kmp-app, kmp-library)

---

## Gradle Modules

| Module | Type | Description | Dependencies |
|--------|------|-------------|--------------|
| :composeApp | Application | Main multiplatform app | :shared, :feature:*, :core:* |
| :shared | Library | Shared business logic | :core:network, :core:data |
| :core:network | Library | HTTP client, API services | Ktor, Kotlinx Serialization |
| :core:data | Library | Repositories, local storage | Room/SQLDelight |
| :core:ui | Library | Design system, components | Compose Multiplatform |
| :feature:{name} | Library | Feature modules | :shared, :core:ui |

---

## Build Variants

### Android

| Variant | Build Type | Flavor | Description | Use Case |
|---------|------------|--------|-------------|----------|
| devDebug | debug | dev | Development API, debug flags | Local development |
| devRelease | release | dev | Development API, optimized | Dev testing |
| prodDebug | debug | prod | Production API, debug flags | Production debugging |
| prodRelease | release | prod | Production API, optimized | Play Store release |

### iOS

| Variant | Configuration | Description |
|---------|--------------|-------------|
| Debug | Debug | Development build |
| Release | Release | App Store / TestFlight |

### Desktop

| Variant | Task | Description |
|---------|------|-------------|
| Debug | runDistributable | Development build |
| Release | createDistributable | Distribution package |

---

## Version Catalog

Reference: `gradle/libs.versions.toml`

### Core Versions

| Key | Version | Description |
|-----|---------|-------------|
| kotlin | 2.0.x | Kotlin language |
| compose | 1.6.x | Compose Multiplatform |
| ktor | 2.3.x | HTTP client |
| koin | 3.5.x | Dependency injection |
| kotlinx-serialization | 1.6.x | JSON serialization |
| kotlinx-coroutines | 1.8.x | Coroutines |

### Plugin Versions

| Key | Version | Description |
|-----|---------|-------------|
| agp | 8.3.x | Android Gradle Plugin |
| compose-multiplatform | 1.6.x | JetBrains Compose Plugin |

---

## Build Scripts

### Root build.gradle.kts

```kotlin
plugins {
    alias(libs.plugins.kotlin.multiplatform) apply false
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.compose.multiplatform) apply false
}
```

### Module build.gradle.kts

```kotlin
plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.compose.multiplatform)
}

kotlin {
    androidTarget()
    iosX64()
    iosArm64()
    iosSimulatorArm64()
    jvm("desktop")

    sourceSets {
        commonMain.dependencies {
            implementation(compose.runtime)
            implementation(compose.foundation)
            implementation(compose.material3)
        }
    }
}
```

---

## Build Commands

| Command | Description |
|---------|-------------|
| `./gradlew assembleDevDebug` | Android dev debug APK |
| `./gradlew assembleProdRelease` | Android prod release APK |
| `./gradlew iosArm64Binaries` | iOS binary |
| `./gradlew runDistributable` | Desktop run |
| `./gradlew :shared:allTests` | Run all tests |

---

## Signing Configuration

### Android

```kotlin
signingConfigs {
    create("release") {
        storeFile = file(keystorePath)
        storePassword = keystorePassword
        keyAlias = keyAlias
        keyPassword = keyPassword
    }
}
```

### iOS

- Automatic signing via Xcode
- Team ID in `project.pbxproj`

---

## ProGuard / R8

| File | Purpose |
|------|---------|
| `proguard-rules.pro` | Custom keep rules |
| `consumer-rules.pro` | Library consumer rules |

---

**Template Version:** 1.0.0
**Last Updated:** 2026-03-08
