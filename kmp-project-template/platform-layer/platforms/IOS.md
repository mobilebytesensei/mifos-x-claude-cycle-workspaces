# iOS Platform — kmp-project-template

## Actual Implementations

| Expect | Actual | Module |
|--------|--------|--------|
| AppDatabase | SQLite (KMP Native) | core:database |
| AppContext | NSObject context | core-base:platform |
| KtorHttpClient | Darwin engine | core-base:network |
| AnalyticsHelper | FirebaseAnalyticsHelper | core-base:analytics |
| IntentManager | UIApplication.open | core-base:platform |
| AppReviewManager | SKStoreReviewController | core-base:platform |
| AppUpdateManager | No-op (App Store handles) | core-base:platform |
| GarbageCollectionManager | No-op | core-base:platform |
| ViewController | iOS ViewController integration | cmp-shared |

## Build Configuration

- Module: `cmp-ios` (Xcode project)
- Deployment Target: iOS 16+
- Framework: Compose Multiplatform (UIKit bridge)
- Deployment: Fastlane + TestFlight
