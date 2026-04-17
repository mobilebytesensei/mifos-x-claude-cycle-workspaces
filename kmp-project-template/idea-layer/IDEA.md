# Product Vision: KMP Project Template

## Vision Statement

The ultimate Kotlin Multiplatform project generator with production-ready setup — enabling shared business logic and UI components across Android, iOS, Desktop, and Web while retaining native platform functionality.

## Problem

Developers building cross-platform applications face fragmented tooling, inconsistent project structures, and significant boilerplate for each platform. Setting up a production-ready KMP project with CI/CD, testing, design system, navigation, DI, and platform-specific code takes weeks of configuration.

## Solution

A comprehensive KMP multi-module template generator that provides:
- Shared business logic across 4 platforms (Android, iOS, Desktop, Web)
- Compose Multiplatform UI with Material Design 3
- Production-ready CI/CD (GitHub Actions + Fastlane, 9 deployment targets)
- Modular architecture (feature/, core/, core-base/ layers)
- Platform-specific implementations via expect/actual pattern
- Built-in analytics, theming, database, networking, and navigation

## Target Users

- Kotlin developers building cross-platform applications
- Teams adopting Kotlin Multiplatform for shared code
- Open-source contributors to Mifos/openMF ecosystem

## Value Propositions

1. **Zero-to-production in minutes** — complete project structure with CI/CD
2. **True code sharing** — business logic, UI, and data layer shared across platforms
3. **Native when needed** — expect/actual pattern for platform-specific features
4. **Customizable** — `customizer.sh` renames namespaces for your project
5. **Production patterns** — real MVI architecture, Koin DI, Ktor networking

---

## Technical Context

### Platform & Stack

| Component | Choice |
|-----------|--------|
| Language | Kotlin 2.x |
| UI Framework | Compose Multiplatform |
| Architecture | MVI (Model-View-Intent) |
| DI | Koin |
| Navigation | Compose Navigation (Type-safe) |
| Networking | Ktor |
| Database | Room (Android/Desktop), SQLite (iOS) |
| DataStore | Multiplatform DataStore |
| CI/CD | GitHub Actions + Fastlane |
| Platforms | Android, iOS, Desktop (JVM), Web (Kotlin/JS + WASM) |

### Entities & Data Model

| Entity | Fields | Storage |
|--------|--------|---------|
| UserData | activeUserId, themeBrand, darkThemeConfig, useDynamicColor, appLanguage, showOnboarding, firstTimeUser, isAuthenticated, isUnlocked, passcode, enableScreenCapture, isPasscodeEnabled, isBiometricsEnabled | DataStore |
| AuthState | authentication state, token | DataStore |
| SampleEntity | id (Int, auto-gen), name (String) | Room DB |
| TaskEntity | task domain model | In-memory (StorageService) |
| Country | country info + flag | Model |
| DarkThemeConfig | dark mode settings | DataStore |
| LanguageConfig | language preferences | DataStore |
| ThemeBrand | theme brand selection | DataStore |

### Third-Party Services

| Service | Purpose | Status |
|---------|---------|:------:|
| Firebase Analytics | App analytics (Android) | ✅ Integrated |
| Ktor HTTP Client | Network requests | ✅ Integrated |
| Room Database | Local persistence | ✅ Integrated |
| Fastlane | iOS/Android deployment | ✅ Integrated |
| GitHub Actions | CI/CD pipelines | ✅ Integrated |

---

## Success Metrics

- Project setup time < 5 minutes (via customizer.sh)
- 4 platform builds passing in CI
- 70%+ code sharing ratio across platforms
- Zero platform-specific UI code for shared screens

## Constraints

- Requires Kotlin 2.x with Compose Multiplatform
- iOS requires Xcode + CocoaPods
- Web target is Kotlin/JS (WASM experimental)
- Desktop requires JVM 17+

## Assumptions

- Developers are familiar with Kotlin and Compose
- Project uses Koin for DI (not Hilt/Dagger)
- Navigation uses Compose Navigation (not Voyager)
