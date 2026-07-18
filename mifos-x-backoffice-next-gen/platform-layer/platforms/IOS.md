# template_meta
# template_version: "2.86.0"
# template_path: "templates/blueprints/workspace-project/platform-layer/platforms/IOS.md"
# last_modified: "2026-03-19"

# iOS Platform

## Module: cmp-ios

> iOS platform target using CocoaPods integration

---

## Setup

1. Install CocoaPods dependencies:
   ```bash
   cd cmp-ios
   pod install
   ```

2. Open Xcode workspace:
   ```bash
   open iosApp.xcworkspace
   ```

3. Build and run in Xcode

---

## Key Files

| File | Purpose |
|------|---------|
| `cmp-ios/Podfile` | CocoaPods dependencies |
| `cmp-ios/iosApp/iOSApp.swift` | App entry point (`@main struct`) |
| `cmp-ios/iosApp/ContentView.swift` | SwiftUI wrapper for Compose |
| `cmp-ios/iosApp/Info.plist` | App configuration |
| `cmp-shared/src/nativeMain/kotlin/.../ViewController.kt` | Compose entry via `ComposeUIViewController` |

---

## Build Commands

| Command | Action |
|---------|--------|
| `pod install` | Install dependencies |
| `pod update` | Update dependencies |
| Xcode Build (Cmd+B) | Build app |
| Xcode Run (Cmd+R) | Run on simulator/device |

### Terminal Build

```bash
xcodebuild -workspace iosApp.xcworkspace \
           -scheme iosApp \
           -sdk iphonesimulator \
           -configuration Debug \
           build
```

---

## iOS App Entry Point

> **Source**: `references/templates/kmp-project-template/cmp-ios/iosApp/iOSApp.swift`

```swift
import SwiftUI

@main
struct iOSApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### ContentView (SwiftUI Wrapper for Compose)

> **Source**: `references/templates/kmp-project-template/cmp-ios/iosApp/ContentView.swift`

```swift
import UIKit
import SwiftUI
import ComposeApp

struct ComposeView: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> UIViewController {
        ViewControllerKt.viewController()
    }

    func updateUIViewController(_ uiViewController: UIViewController, context: Context) {}
}

struct ContentView: View {
    var body: some View {
        ComposeView()
            .ignoresSafeArea(edges: .all)
            .ignoresSafeArea(.keyboard)
    }
}
```

### Kotlin-Side ViewController (nativeMain)

> **Source**: `references/templates/kmp-project-template/cmp-shared/src/nativeMain/kotlin/.../ViewController.kt`

```kotlin
fun viewController() = ComposeUIViewController(
    configure = {
        initKoin()
    },
) {
    SharedApp()
}
```

**Key elements:**
- iOS app uses `@main struct iOSApp: App` as the SwiftUI entry point
- `ContentView` wraps the Compose UI via `UIViewControllerRepresentable`
- The actual Compose UI is provided by `ComposeUIViewController` in `nativeMain`
- Koin is initialized in the `configure` block of `ComposeUIViewController`

---

## KMP Framework Integration

### Shared Framework

```ruby
# Podfile
target 'iosApp' do
  use_frameworks!
  pod 'cmp_shared', :path => '../cmp-shared'
end
```

---

## Xcode Project Structure

```
iosApp/
├── iosApp.xcodeproj/
├── iosApp.xcworkspace/
├── iosApp/
│   ├── Assets.xcassets/
│   ├── ContentView.swift
│   ├── Info.plist
│   └── iOSApp.swift
└── Podfile
```

---

## iOS-Specific Features

| Feature | Implementation |
|---------|----------------|
| Biometrics | LocalAuthentication |
| Push Notifications | APNs |
| Deep Links | URL Schemes |

---

## Requirements

| Requirement | Version |
|-------------|---------|
| iOS Deployment Target | 14.0+ |
| Xcode | 15.0+ |
| CocoaPods | 1.12+ |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pod install fails | Run `pod repo update` first |
| Framework not found | Clean build folder (Cmd+Shift+K) |
| Simulator issues | Reset simulator content |

---

## Related

- [LAYER_STATUS.md](../LAYER_STATUS.md) - Platform overview
- [LAYER_GUIDE.md](../LAYER_GUIDE.md) - Architecture patterns
