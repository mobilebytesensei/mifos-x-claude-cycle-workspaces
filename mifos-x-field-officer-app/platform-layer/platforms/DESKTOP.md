# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/platform-layer/platforms/DESKTOP.md"
# last_modified: "2026-03-19"

# Desktop Platform

## Module: cmp-desktop

> JVM-based desktop application using Compose for Desktop

---

## Build Commands

| Command | Action |
|---------|--------|
| `./gradlew :cmp-desktop:run` | Run desktop app |
| `./gradlew :cmp-desktop:packageDmg` | Package macOS DMG |
| `./gradlew :cmp-desktop:packageMsi` | Package Windows MSI |
| `./gradlew :cmp-desktop:packageDeb` | Package Linux DEB |
| `./gradlew :cmp-desktop:packageRpm` | Package Linux RPM |

---

## Key Files

| File | Purpose |
|------|---------|
| `cmp-desktop/build.gradle.kts` | Module configuration |
| `cmp-desktop/src/jvmMain/kotlin/main.kt` | Entry point (Koin init + Window) |
| `cmp-desktop/src/main/resources/` | Desktop resources |

---

## Gradle Configuration

```kotlin
compose.desktop {
    application {
        mainClass = "org.mifos.mobile.MainKt"

        nativeDistributions {
            targetFormats(
                TargetFormat.Dmg,
                TargetFormat.Msi,
                TargetFormat.Deb
            )
            packageName = "Mifos Mobile"
            packageVersion = "1.0.0"
        }
    }
}
```

---

## Entry Point

> **Source**: `references/templates/kmp-project-template/cmp-desktop/src/jvmMain/kotlin/main.kt`

```kotlin
fun main() {
    application {
        // Initialize Koin for dependency injection
        initKoin()

        val windowState = rememberWindowState()

        Window(
            onCloseRequest = ::exitApplication,
            state = windowState,
            title = "DesktopApp",
        ) {
            SharedApp()
        }
    }
}
```

**Key elements:**
- Calls `initKoin()` before creating the window (no Android-specific config needed)
- Uses `rememberWindowState()` for window state management
- Source set is `jvmMain/` (or `desktopMain/` in some exemplars)
- Calls `SharedApp()` composable from `cmp-shared` module

---

## Platform Support

| OS | Target Format | Status |
|----|---------------|:------:|
| macOS | DMG | ✅ |
| Windows | MSI | ✅ |
| Linux | DEB/RPM | ✅ |

---

## Desktop-Specific Features

| Feature | Status | Notes |
|---------|:------:|-------|
| Window Management | ✅ | Resize, minimize, maximize |
| System Tray | ⚠️ | Optional |
| Keyboard Shortcuts | ✅ | Standard shortcuts |
| File System Access | ✅ | Full access |

---

## Requirements

| Requirement | Version |
|-------------|---------|
| JVM | 17+ |
| Compose Desktop | 1.5+ |

---

## Development Notes

- Uses Compose for Desktop (Multiplatform)
- Shares UI code with Android/iOS
- Platform-specific code in `jvmMain/`

---

## Related

- [LAYER_STATUS.md](../LAYER_STATUS.md) - Platform overview
- [LAYER_GUIDE.md](../LAYER_GUIDE.md) - Architecture patterns
