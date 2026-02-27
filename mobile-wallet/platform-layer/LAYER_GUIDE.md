# Platform Layer Guide - mobile-wallet

> Platform-specific implementation documentation

---

## Supported Platforms

| Platform | Status | Path |
|----------|:------:|------|
| Android | ✅ | `cmp-android/` |
| iOS | ✅ | `cmp-ios/` |
| Desktop | ✅ | `cmp-desktop/` |
| Web | ✅ | `cmp-web/` |

---

## Directory Structure

```
platform-layer/
├── LAYER_GUIDE.md         # This file
└── platforms/
    ├── android/           # Android-specific docs
    ├── ios/               # iOS-specific docs
    ├── desktop/           # Desktop-specific docs
    └── web/               # Web-specific docs
```

---

## Platform-Specific Components

### Android (`cmp-android/`)
- MainActivity
- AndroidManifest.xml
- Gradle configuration
- Push notifications (Firebase)

### iOS (`cmp-ios/`)
- iOSApp.swift
- Info.plist
- Xcode project
- Push notifications (APNs)

### Desktop (`cmp-desktop/`)
- Main.kt (JVM)
- Window configuration
- Native menus

### Web (`cmp-web/`)
- index.html
- Web workers
- PWA configuration

---

## Shared Code

| Module | Purpose |
|--------|---------|
| cmp-shared | Navigation, shared UI |
| core | Business logic, data |
| feature | Feature modules |

---

## Commands

| Command | Purpose |
|---------|---------|
| `/platform [platform]` | Document platform |
| `/gap-analysis platform` | Check gaps |
