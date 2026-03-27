# Android Platform — kmp-project-template

## Actual Implementations

| Expect | Actual | Module |
|--------|--------|--------|
| AppDatabase | Room.databaseBuilder | core:database |
| AppContext | Android Context | core-base:platform |
| KtorHttpClient | OkHttp engine | core-base:network |
| AnalyticsHelper | FirebaseAnalyticsHelper | core-base:analytics |
| IntentManager | Android Intent | core-base:platform |
| AppReviewManager | Google Play Review API | core-base:platform |
| AppUpdateManager | Google Play In-App Update | core-base:platform |
| GarbageCollectionManager | Android GC | core-base:platform |
| DispatcherManager | Dispatchers.IO | core-base:common |
| ShareUtils | Android Share Intent | core-base:ui |
| RootNavScreen | Android-specific scaffold | cmp-navigation |

## Build Configuration

- Module: `cmp-android`
- Min SDK: 24
- Target SDK: 34
- Compose: Multiplatform Compose
- Deployment: Fastlane + GitHub Actions
