# PLAN-security-hardening-260501: Data Layer Security Hardening

| Field | Value |
|-------|-------|
| ID | security-hardening-260501 |
| Status | Draft |
| Priority | P0 |
| Scope | `core-base/security` (new) + `core-base/datastore` (new) + `core-base/store` + `core-base/network` + `core/database` + `core/datastore` + `core/data` + `cmp-android` |
| Created | 2026-05-01 |
| Updated | 2026-05-01 (v7 — 19 additional gaps fixed: TypeConverter wiring, DI ordering, migration atomicity, platform key storage, debug gate) |
| Prerequisites | PLAN-storedata-api-260430 (completed), PLAN-storedata-gaps-260430 (completed) |
| Effort | ~40 hours (4 phases) |
| Parent Plan | — |

---

## Problem Statement

Two rounds of security audit (initial + end-to-end deep dive) of Room 3 + Store 5 offline data layer found **31 gaps** (6 critical, 14 high, 11 medium). The entire data pipeline operates in plaintext — Network → Store 5 → Room 3 → DataStore → UI. No encryption at any layer. Token refresh has race conditions.

**Note:** Credentials in git (SEC-18, SEC-19, SEC-22, SEC-35) are **intentional demo/build-only values** — real secrets are never in code. These 5 gaps are removed from scope.

**Design Principle — Debug vs Release:**
Security hardening applies to **release builds only**. Debug builds retain full visibility for development:
- Logging: `LogLevel.ALL` in debug, `LogLevel.HEADERS` with redacted `toString()` in release
- Root/jailbreak detection: disabled in debug, active in release
- Clipboard auto-wipe: disabled in debug, 60s wipe in release
- Tamper detection: disabled in debug, active in release
- HTTP cache: encrypted in both (centralized via security module)

**Threat model:**
- Physical device access (stolen/seized device)
- Rooted/jailbroken device with debugger
- MITM proxy on untrusted network
- APK/IPA reverse engineering
- ADB backup extraction (`android:allowBackup="true"`)
- Brute-force passcode attack (no lockout)
- Memory forensics on running process
- Clipboard sniffing by malicious apps (release only)
- Stale data replay after logout

---

## Complete Gap Registry (36 Gaps)

### CRITICAL (6)

| ID | Gap | File | Issue |
|----|-----|------|-------|
| SEC-1 | No database encryption | `core/database/src/{platform}Main/…/DatabaseModule.*.kt:26-27` | Room 3 uses `BundledSQLiteDriver()`. Sensitive fields stored plaintext. Fix: Application-layer encryption via `FieldEncryptor` (SQLCipher incompatible with Room 3 KMP — see GAP-B1). |
| SEC-2 | Passcode stored plaintext | `core/datastore/…/UserPreferencesRepositoryImpl.kt:145` | `multiplatform-settings` `Settings()` stores passcode unencrypted. Fix: `SecureSettingsFactory` in `core-base/datastore` provides encrypted `Settings` backed by platform secure storage. |
| SEC-3 | No secure credential storage | (none exists) | No encrypted `Settings` variant. Fix: `core-base/datastore` provides `SecureSettingsFactory` — same `Settings` interface, encrypted backend per platform (EncryptedSharedPreferences / Keychain / JVM KeyStore). |
| SEC-4 | No certificate pinning | `core-base/network/src/{platform}Main/…/KtorHttpClient.*.kt:16` | OkHttp/Darwin engines use system TLS only. No pinning. |
| SEC-5 | `android:allowBackup="true"` | `cmp-android/…/AndroidManifest.xml:31` | ADB backup extracts entire app data including DB. |
| SEC-20 | ~~WAL file bypasses SQLCipher~~ | `core/database/src/{platform}Main/…/DatabaseModule.*.kt` | **Resolved by GAP-B1 strategy change:** Application-layer encryption encrypts data BEFORE Room stores it. WAL/SHM files only contain already-encrypted field values. No WAL bypass possible. |

### REMOVED FROM SCOPE (5) — Intentional Demo/Build Credentials

| ID | Gap | Reason |
|----|-----|--------|
| ~~SEC-18~~ | Hardcoded keystore password | Intentional demo creds for build only; real secrets not in code |
| ~~SEC-19~~ | Committed secrets directory | Demo-only build creds in `secrets_demo/` |
| ~~SEC-22~~ | google-services.json committed | Build-time config, not production secrets |
| ~~SEC-35~~ | Placeholder API credentials | Demo placeholders `RblClientIdProp=a/b` |
| ~~SEC-21~~ | Token refresh race condition | Moved to HIGH — not credential-related |

### HIGH (14)

| ID | Gap | File | Issue | Debug/Release |
|----|-----|------|-------|---------------|
| SEC-21 | Token refresh race condition | `core-base/network/…/KtorHttpClient.kt:89-97` | No Mutex on `refreshTokens{}`. Concurrent 401s cause stale token. | Both |
| SEC-6 | No root/jailbreak detection | (none exists) | App runs identically on compromised devices. | **Release only** — disabled in debug |
| SEC-7 | Sensitive data in logs | `core-base/network/…/KtorHttpClient.kt:74` | `LogLevel.ALL` + data class `toString()` exposes tokens in release. | **Release only** — `LogLevel.ALL` kept in debug, `LogLevel.HEADERS` + redacted `toString()` in release |
| SEC-8 | No tamper detection | (none exists) | No APK/IPA integrity verification at runtime. | **Release only** — disabled in debug |
| SEC-9 | No memory scrubbing | `core-base/store/…/InMemoryBookkeeper.kt` | Plain `MutableMap`, Store cache unprotected. | Both |
| SEC-10 | Missing `network_security_config.xml` | `cmp-android/` | No Android network security policy file. | Both |
| SEC-11 | Insufficient ProGuard rules | `cmp-android/proguard-rules.pro` | No obfuscation of UserData, AuthState, data models. | Release only |
| SEC-12 | `prettyPrint = true` in JSON | `core-base/network/…/KtorHttpClient.kt:78` | Exposes API structure in release. | **Release only** — `prettyPrint = true` kept in debug |
| SEC-23 | Clipboard no auto-wipe | `core-base/ui/…/ShareUtils.android.kt:168-172` | `copyText()` indefinite clipboard. No timeout. | **Release only** — disabled in debug |
| SEC-24 | FileProvider path="." too permissive | `cmp-android/…/provider_paths.xml:12-28` | All 5 path elements use `path="."`. Entire storage exposed. | Both |
| SEC-25 | HTTP cache not encrypted | `core-base/network/src/{platform}Main/…/KtorHttpClient.*.kt:16` | OkHttp disk cache stores responses in plaintext. | **Both** — centralized encrypted cache via security module (not disabled) |
| SEC-26 | Error messages via println() | `core-base/network/…/ResultSuspendConverterFactory.kt:80,95,107` | Raw `println()` instead of proper logging. | **Both** — convert to Kermit debug logger (visible in debug, stripped in release) |
| SEC-27 | TypeConverter crashes on malformed JSON | `core/database/…/ChargeTypeConverters.kt:27-47` | No try-catch. Corrupted DB = crash loop (DoS). | Both |
| SEC-28 | Flow stateIn replay leaks stale data | `feature/home/…/TasksViewModel.kt:69-73` | After logout, UI recreation replays stale user data. | Both |
| SEC-29 | Store has no explicit cache eviction | `core-base/store/…/StoreFactory.kt` | No `clearStore()`. Old sensitive data persists indefinitely. | Both |
| SEC-30 | Session timeout missing | `core/data/…/UserLogoutManagerImpl.kt:39-56` | No inactivity timer, no background timeout. | Both |

### MEDIUM (10)

| ID | Gap | File | Issue | Debug/Release |
|----|-----|------|-------|---------------|
| SEC-13 | No biometric auth implementation | `core/model/…/UserData.kt:28` | Flag exists but no actual BiometricPrompt/LAContext. | Both |
| SEC-14 | No self-destruct / wipe mechanism | (none exists) | No brute-force lockout, no remote wipe. | Both |
| SEC-15 | Schema export enabled | `core/database/…/AppDatabase.kt:50` | JSON schema committed. | Release only |
| SEC-16 | No field-level encryption | `core/database/…/ChargeTypeConverters.kt` | Type converters serialize plaintext JSON. | Both |
| SEC-17 | Desktop DB in user-accessible path | `core-base/database/…/AppDatabaseFactory.kt` | No OS-level protection. | Both |
| SEC-31 | Passcode as immutable String | `core/model/…/UserData.kt:25` | Kotlin String can't be zeroed from JVM memory. | Both |
| SEC-32 | No SecureRandom implementation | (none exists) | No expect/actual for crypto-quality RNG. | Both |
| SEC-33 | Firebase analytics without consent | `cmp-android/src/prod/AndroidManifest.xml:14-30` | No opt-out, no consent mechanism. | Release only |
| SEC-34 | Room 3.0.0-alpha03 in production | `gradle/libs.versions.toml:114` | Alpha — undiscovered vulns, unstable migration API. | Both |
| SEC-36 | No deep link validation | `cmp-android/…/AndroidManifest.xml:39-49` | No App Links verification framework. | Both |

---

## Plan Gaps Found (v6 Audit — 13 gaps)

### BLOCKER: SQLCipher has NO `SQLiteDriver` for Room 3 KMP (GAP-B1)

Room 3 KMP uses `SQLiteDriver` (from `androidx.sqlite`). SQLCipher only provides `SupportSQLiteOpenHelper.Factory` — the **Room 2 legacy API**. No published library implements Room 3's `SQLiteDriver` interface with SQLCipher encryption. This affects ALL platforms.

**Resolution — Application-layer encryption via `FieldEncryptor`:**

Since driver-level encryption is not available for Room 3 KMP, we use **application-layer encryption** instead:

1. **`FieldEncryptor`** (in `core-base/security`) encrypts sensitive data BEFORE Room stores it
2. Room TypeConverters call `FieldEncryptor.encrypt()`/`decrypt()` transparently
3. Non-sensitive data (UI state, cached lists) stays plaintext for query performance
4. Platform-specific AES-256-GCM via expect/actual (Android: `javax.crypto`, iOS: `CommonCrypto`, Desktop: BouncyCastle, Web: `SubtleCrypto`)
5. Encryption key stored in Android Keystore / iOS Keychain / JVM KeyStore (via `SecureKeyProvider`)

```kotlin
// core-base/security/src/commonMain/…/FieldEncryptor.kt
expect class FieldEncryptor {
    fun encrypt(plaintext: String): String   // Returns Base64-encoded ciphertext
    fun decrypt(ciphertext: String): String  // Returns original plaintext
    fun encrypt(data: ByteArray): ByteArray
    fun decrypt(data: ByteArray): ByteArray
}

// Usage in Room TypeConverters:
class SecureChargeTypeConverters(private val encryptor: FieldEncryptor) {
    @TypeConverter
    fun fromChargeList(charges: List<Charge>): String {
        val json = Json.encodeToString(charges)
        return encryptor.encrypt(json)  // Encrypted before Room stores it
    }
    @TypeConverter
    fun toChargeList(encrypted: String): List<Charge> {
        val json = encryptor.decrypt(encrypted)
        return Json.decodeFromString(json)
    }
}
```

**Trade-offs vs driver-level (SQLCipher):**

| | Driver-level (SQLCipher) | Application-layer (FieldEncryptor) |
|---|---|---|
| Coverage | Entire DB file encrypted | Only marked fields encrypted |
| Query perf | Can query encrypted fields | Cannot query encrypted content |
| Room 3 KMP | NOT AVAILABLE | Works today |
| APK size | +3MB (native lib) | ~0 (uses platform crypto APIs) |
| WAL issue | Needs TRUNCATE journal | Not applicable — data encrypted before storage |
| Migration | Encrypt-in-place complex | Per-field, incremental |

**What changes:**
- ~~D1: SQLCipher for DB encryption~~ → D1: Application-layer field encryption via `FieldEncryptor`
- ~~D5: Encrypt at Room driver level~~ → D5: Encrypt at TypeConverter/Repository level
- ~~D9: Disable WAL mode~~ → D9: WAL mode stays (no plaintext leak since data is encrypted before storage)
- SEC-20 (WAL bypass) is **automatically resolved** — WAL/SHM files only contain already-encrypted field values
- T7 changes scope: no driver swap, instead wire `FieldEncryptor` into TypeConverters and Repositories

### CRITICAL Gaps (3)

**GAP-C1: No migration from unencrypted to encrypted DB**

**v7 update — encrypt-on-write strategy (replaces batch migration):**

TypeConverters use `"ENC:"` prefix to distinguish plaintext from encrypted data. Read path handles both formats. Write path always encrypts with prefix. This eliminates the batch migration entirely — data encrypts gradually as rows are updated. Benefits:
1. **Crash-safe by design** — no partially migrated state possible
2. **Downgrade-safe** — old app versions see `"ENC:..."` → try-catch returns empty (T4.3)
3. **Zero migration time** — no first-launch delay
4. Optional background job can bulk-encrypt remaining plaintext rows. Added as T7.1.

**GAP-C2: UserData is ONE serialized blob — needs two data classes**

Current `UserData` is serialized as a single JSON blob. Splitting across plain/secure Settings requires:

```kotlin
// Sensitive — stored in Settings(named("secure"))
@Serializable
data class SecureUserData(
    val passcode: String,
    val activeUserId: String,
    val isAuthenticated: Boolean,
    val authToken: String? = null,
)

// Non-sensitive — stored in Settings(named("plain"))
@Serializable
data class UserPreferences(
    val themeBrand: ThemeBrand,
    val darkThemeConfig: DarkThemeConfig,
    val useDynamicColor: Boolean,
    val appLanguage: LanguageConfig,
    val showOnboarding: Boolean,
    val firstTimeUser: Boolean,
    val enableScreenCapture: Boolean,
    val isPasscodeEnabled: Boolean,
    val isBiometricsEnabled: Boolean,
    val isUnlocked: Boolean,
)

// UserData stays as the merged view (read-only)
data class UserData(/* all fields */) {
    companion object {
        fun from(prefs: UserPreferences, secure: SecureUserData): UserData = ...
    }
}
```

`UserPreferencesRepositoryImpl` merges both via `combine(prefsFlow, secureFlow) { p, s -> UserData.from(p, s) }`.

**GAP-C3: No migration for Settings split**

**v7 update — crash-safe write-before-delete order:**

T8.1 — one-time migration on first launch:
1. Read old `user_data_key` from plain Settings
2. Write `SecureUserData` to secure Settings under new key **FIRST**
3. Write `UserPreferences` to plain Settings under new key **SECOND**
4. Delete old `user_data_key` **LAST** (ensures old key persists until both writes succeed)
5. On crash: next launch detects old key still present → retries migration idempotently

### IMPORTANT Gaps (5)

**GAP-I1: `BuildConfig.DEBUG` doesn't exist in commonMain**

Fixed. `SecurityConfig.isReleaseBuild` is set per-platform:

```kotlin
// core-base/security/src/commonMain/…/SecurityConfig.kt
data class SecurityConfig(val isReleaseBuild: Boolean, ...)

// Provided via expect/actual at app level:
// cmp-android: SecurityConfig(isReleaseBuild = !BuildConfig.DEBUG)
// cmp-desktop: SecurityConfig(isReleaseBuild = System.getProperty("app.release") == "true")
// cmp-ios: SecurityConfig(isReleaseBuild = !Platform.isDebugBinary) // Kotlin/Native
// cmp-web: SecurityConfig(isReleaseBuild = js("process.env.NODE_ENV") == "production")
```

`SecurityConfig` is created in each **app module** (cmp-android, cmp-desktop, etc.), not in commonMain. SecurityModule receives it via Koin.

**GAP-I2: Koin `singleOf()` doesn't support `@Named`**

Fixed. Use manual `single { }` lambda:

```kotlin
// core/datastore/…/DatastoreModule.kt
val DatastoreModule = module {
    includes(CommonModule, DatastoreBaseModule)
    single<UserPreferencesRepository> {
        UserPreferencesRepositoryImpl(
            settings = get(named("plain")),
            secureSettings = get(named("secure")),
            dispatcher = get(),
        )
    }
}
```

**GAP-I3: Darwin cert pinning code missing**

Added. iOS/macOS uses Ktor Darwin engine's `handleChallenge`:

```kotlin
// core-base/network/src/nativeMain/…/KtorHttpClient.native.kt
actual fun httpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient {
    return HttpClient(Darwin) {
        engine {
            val pinConfig = KoinPlatform.getKoin().getOrNull<CertificatePinConfig>()
            if (pinConfig != null && pinConfig.pins.isNotEmpty()) {
                handleChallenge { session, task, challenge, completionHandler ->
                    if (challenge.protectionSpace.authenticationMethod ==
                        NSURLAuthenticationMethodServerTrust) {
                        val serverTrust = challenge.protectionSpace.serverTrust
                        val host = challenge.protectionSpace.host
                        if (pinConfig.validate(host, serverTrust)) {
                            completionHandler(
                                NSURLSessionAuthChallengeUseCredential,
                                NSURLCredential.credentialForTrust(serverTrust!!)
                            )
                        } else {
                            completionHandler(
                                NSURLSessionAuthChallengeCancelAuthenticationChallenge, null
                            )
                        }
                    }
                }
            }
        }
        config(this)
    }
}
```

**GAP-I4: JS/WasmJS missing `actual` for BiometricAuth, TamperDetection**

Fixed. Add no-op actuals in `jsCommonMain` (shared by js and wasmJs via convention plugin's hierarchy):

```kotlin
// core-base/security/src/jsCommonMain/…/
actual class BiometricAuth {
    actual suspend fun authenticate(): BiometricResult = BiometricResult.NotAvailable
}
actual class TamperDetection {
    actual fun check(): TamperResult = TamperResult.Safe
}
```

**GAP-I5: SQLCipher version wrong**

Removed from dependencies. SQLCipher is no longer used (replaced by application-layer `FieldEncryptor`). No native crypto libraries needed — we use platform APIs directly.

### API/Logic Gaps (4)

**GAP-W1: OkHttp encrypted cache needs custom `okio.FileSystem`**

Fixed. `EncryptedCacheProvider` creates an OkHttp `Cache` with a custom encrypting `FileSystem`:

```kotlin
// androidMain/desktopMain
actual class EncryptedCacheProvider(private val encryptor: FieldEncryptor) {
    actual fun createEncryptedCache(cacheDir: File, maxSize: Long): Cache {
        return Cache(
            fileSystem = EncryptingFileSystem(encryptor, FileSystem.SYSTEM),
            directory = cacheDir.toOkioPath(),
            maxSize = maxSize,
        )
    }
}
```

**GAP-W2: `PropertiesSettings` missing persist callback**

Fixed. Desktop `SecureSettingsFactory` includes the persist callback:

```kotlin
actual class SecureSettingsFactory {
    actual fun create(): Settings {
        val props = loadEncryptedProperties()
        return PropertiesSettings(props) { updated ->
            saveEncryptedProperties(updated)  // AES-encrypt → write to disk
        }
    }
}
```

**GAP-L1: Phase 1 references SecurityConfig (created in Phase 2)**

Fixed. Phase 1 debug/release gates use platform-specific `BuildConfig.DEBUG` directly (Android) or equivalent. Phase 2 refactors to centralized `SecurityConfig`:

```kotlin
// Phase 1 — direct platform check (no SecurityConfig needed):
// Android: if (!BuildConfig.DEBUG) { prettyPrint = false }
// Phase 2 — refactored to: if (config.isReleaseBuild) { ... }
```

**GAP-L2: FailedAttemptTracker "uses SecureStorage" — removed**

Fixed. `FailedAttemptTracker` uses plain `Settings` (not secure). Failed attempt count is not a secret — it just needs to persist:

```kotlin
class FailedAttemptTracker(private val settings: Settings) {
    fun recordAttempt(): Int {
        val count = settings.getInt("failed_attempts", 0) + 1
        settings.putInt("failed_attempts", count)
        settings.putLong("last_attempt_ms", Clock.System.now().toEpochMilliseconds())
        return count
    }
    fun reset() { settings.putInt("failed_attempts", 0) }
}
```

---

## Plan Gaps Found (v7 Audit — 19 gaps)

Three parallel agents audited the v6 plan for API correctness, architecture consistency, and platform/migration safety.

### API Corrections (3)

| ID | Severity | Gap | Resolution |
|----|----------|-----|------------|
| GAP-W2/P7 | CRITICAL | Room TypeConverter — constructor injection not supported. Room instantiates via no-arg constructor. | Use `.addTypeConverter(instance)` on database builder. Updated injection point #1. |
| GAP-W4 | IMPORTANT | `KeychainSettings` param is `serviceName`, not `service` | Fixed all occurrences. |
| GAP-W9/A9 | IMPORTANT | `@Named` annotations on constructor params — Koin doesn't use them | Removed from `UserPreferencesRepositoryImpl`. Koin resolution is explicit in `DatastoreModule` via `get(named())`. |

### Architecture Corrections (4)

| ID | Severity | Gap | Resolution |
|----|----------|-----|------------|
| GAP-A2 | BLOCKER | Phase 1 T3/T4 use `BuildConfig.DEBUG` in commonMain — doesn't exist there | T3/T4 now add `isReleaseBuild: Boolean` param to `setupDefaultHttpClient()`. Each platform actual passes it. Phase 2 refactors to `SecurityConfig`. |
| GAP-A3 | CRITICAL | `FailedAttemptTracker` uses `singleOf()` but 2 `Settings` exist — Koin can't disambiguate | Changed to manual `single { FailedAttemptTracker(get(named("plain"))) }`. |
| GAP-A4 | CRITICAL | SecurityConfig init order — `SecurityModule` loads first but needs config from app module | `SecurityModule` changed to `securityModule(config: SecurityConfig)` function. Config passed as parameter, not from Koin graph. `allModules` is now `allModules(config)`. |
| GAP-A1 | IMPORTANT | Problem statement says "WAL files bypass SQLCipher" — stale | Removed stale language. |

### Platform & Migration (8)

| ID | Severity | Gap | Resolution |
|----|----------|-----|------------|
| GAP-P1 | CRITICAL | No key loss/rotation recovery — key loss = data unreadable | Added key loss detection in T7: `SecureKeyProvider.getKey()` returns null + encrypted data exists → trigger re-auth re-fetch. |
| GAP-P2 | CRITICAL | DB migration not atomic — crash = mixed plaintext/encrypted rows | Changed to **encrypt-on-write** with `"ENC:"` prefix. TypeConverters read both formats. No separate migration pass needed. Crash-safe by design. |
| GAP-P3 | HIGH | Settings migration not atomic — crash between writes = data loss | Reordered: write secure FIRST → write plain SECOND → delete old key LAST. Old key persists until success. Crash → retry idempotently. |
| GAP-P4 | HIGH | `EncryptedCacheProvider` on iOS fabricated — `NSURLCache` has NO encryption API | iOS removed from EncryptedCacheProvider. Darwin relies on OS-level `NSFileProtectionComplete` (encrypted when device locked). |
| GAP-P5 | HIGH | Desktop JVM KeyStore password chicken-and-egg | Documented in T18 — Desktop uses macOS Keychain (JNI), Linux libsecret, Windows DPAPI for key storage. BouncyCastle for AES operations only. |
| GAP-P6 | HIGH | Web/JS encryption key persistence unsolved | Documented limitation: web encryption keys stored via IndexedDB `CryptoKey` (non-extractable). XSS risk accepted — web is inherently less secure than native. |
| GAP-P9 | MEDIUM | `SessionManager` needs platform lifecycle hooks for inactivity timer | T14.1 updated: requires `AppLifecycleObserver` expect/actual (ProcessLifecycleOwner / UIApplication / window focus). |
| GAP-P12 | LOW | `SecureWipe` zero-fill meaningless on flash storage | T11 changed to key deletion + file deletion (no zero-fill). Key deletion makes encrypted data permanently unreadable. |

### Other (4)

| ID | Severity | Gap | Resolution |
|----|----------|-----|------------|
| GAP-A6 | MEDIUM | Effort math: ~39.5h actual vs ~35h header | Updated to ~40h. |
| GAP-P8 | MEDIUM | `ChargeTypeConvertersTest` will break (no-arg constructor) | Added to T7 scope: update test for new constructor. |
| GAP-P10 | MEDIUM | `CertificatePinConfig.default()` is empty/no-op | Intentional — consumer apps must configure pins for their API domains. Template provides infrastructure, not policy. |
| GAP-P11 | MEDIUM | No downgrade protection after DB encryption | Solved by `"ENC:"` prefix + T4.3 try-catch: old app versions see `"ENC:..."` → try-catch returns empty list (graceful degradation, not crash). |

---

## Wiring Architecture

### Current Module Graph (Before Security)

```
cmp-android / cmp-desktop / cmp-ios / cmp-web
    └── cmp-navigation/…/KoinModules.kt (allModules)
         ├── dataModule        → core/data (UserLogoutManager, repos)
         ├── DatabaseModule    → core/database (AppDatabase + DAOs)
         ├── dispatcherModule  → core-base/common (DispatcherManager)
         ├── analyticsModule   → core-base/analytics
         ├── DatastoreModule   → core/datastore (Settings + UserPreferences)
         ├── featureModule     → feature/* (ViewModels)
         └── AppModule         → cmp-navigation (Nav VMs)
```

### Target Module Graph (With Security + Datastore)

```
                      ┌──────────────────────────┐
                      │   core-base/security      │  ← NEW MODULE
                      │   (expect/actual per plat) │
                      │                            │
                      │   Provides:                │
                      │   - SecurityConfig          │
                      │   - FieldEncryptor          │
                      │   - CertificatePinConfig    │
                      │   - EncryptedCacheProvider  │
                      │   - SecureWipe              │
                      │   - BiometricAuth           │
                      │   - TamperDetection         │
                      │   - SessionManager          │
                      │   - FailedAttemptTracker    │
                      │   - SecureRandom            │
                      │   - SecurityPolicy          │
                      └──────┬───────┬────────┬────┘
                             │       │        │
              ┌──────────────┘       │        └──────────────┐
              ▼                      ▼                       ▼
    ┌──────────────────┐   ┌─────────────────────┐  ┌───────────────────┐
    │  core/database    │   │ core-base/datastore  │  │ core-base/network  │
    │                   │   │ ← NEW MODULE         │  │                    │
    │  Consumes:        │   │                      │  │  Consumes:          │
    │  FieldEncryptor   │   │ Provides:            │  │  CertPinConfig      │
    │  → encrypted      │   │ SecureSettingsFactory │  │  → OkHttp pinner    │
    │  TypeConverters   │   │ (plain + encrypted   │  │  EncryptedCache     │
    │                   │   │  Settings instances)  │  │  → encrypted disk   │
    └────────┬─────────┘   └──────────┬───────────┘  └────────┬──────────┘
             │                        │                        │
             │               ┌────────┴─────────┐             │
             │               ▼                   │             │
             │      ┌────────────────┐           │             │
             │      │ core/datastore  │           │             │
             │      │ (app-specific)  │           │             │
             │      │                 │           │             │
             │      │ Consumes:       │           │             │
             │      │ Settings(plain) │           │             │
             │      │ Settings(secure)│           │             │
             │      │ from core-base/ │           │             │
             │      │ datastore       │           │             │
             │      └───────┬────────┘           │             │
             │              │                     │             │
             └──────────────┼─────────────────────┘             │
                            ▼                                   │
                   ┌──────────────┐                             │
                   │   core/data   │  ←─────────────────────────┘
                   │               │
                   │  Consumes:    │
                   │  SecureWipe   │
                   │  (on logout)  │
                   │  SessionMgr   │
                   └──────┬───────┘
                          ▼
                   ┌──────────────┐
                   │  feature/*    │
                   │               │
                   │  Consumes:    │
                   │  BiometricAuth│
                   │  SessionMgr   │
                   └──────────────┘
```

### core-base/datastore — Shared Settings Infrastructure

**Why a new module?** `core/datastore` contains app-specific `UserData`/`UserPreferencesRepository`. The encrypted `Settings` infrastructure (factory, DI, platform backends) is generic — every consumer app needs it. Moving it to `core-base/` means consumer apps get encrypted settings automatically via `sync-dirs.sh`.

```
core-base/datastore/                         ← NEW MODULE (synced to all consumers)
├── src/commonMain/kotlin/template/core/base/datastore/
│   ├── SecureSettingsFactory.kt             ← expect class → returns Settings
│   ├── di/DatastoreBaseModule.kt            ← Koin: provides named("plain") + named("secure") Settings
│   └── SettingsQualifiers.kt                ← Koin named qualifiers
│
├── src/androidMain/kotlin/…/
│   └── AndroidSecureSettingsFactory.kt      ← actual: EncryptedSharedPreferences → SharedPreferencesSettings
│
├── src/nativeMain/kotlin/…/
│   └── IosSecureSettingsFactory.kt          ← actual: Keychain Services → KeychainSettings
│
├── src/desktopMain/kotlin/…/
│   └── DesktopSecureSettingsFactory.kt      ← actual: JVM KeyStore + AES-encrypted file
│
├── src/jsMain/kotlin/…/
│   └── WebSecureSettingsFactory.kt          ← actual: Web Crypto API wrapper
│
├── src/commonTest/kotlin/…/
│   └── SecureSettingsFactoryTest.kt         ← uses MapSettings for both plain/secure
│
└── build.gradle.kts
    plugins { alias(libs.plugins.kmp.core.base.library.convention) }
    dependencies:
      commonMain: core-base/common, core-base/security, multiplatform-settings
      androidMain: androidx-security-crypto
```

**Key design: Same `Settings` interface, zero API change**

```kotlin
// core-base/datastore/src/commonMain/…/SecureSettingsFactory.kt
expect class SecureSettingsFactory {
    fun create(): Settings  // Returns standard multiplatform-settings Settings
}

// androidMain — EncryptedSharedPreferences implements SharedPreferences
// → SharedPreferencesSettings(encryptedPrefs) returns a standard Settings!
actual class SecureSettingsFactory(private val context: Context) {
    actual fun create(): Settings {
        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()
        val encryptedPrefs = EncryptedSharedPreferences.create(
            context, "secure_prefs", masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
        )
        return SharedPreferencesSettings(encryptedPrefs)
    }
}

// nativeMain — Keychain-backed
actual class SecureSettingsFactory {
    actual fun create(): Settings = KeychainSettings(serviceName = "org.mifos.secure")
}

// desktopMain — JVM KeyStore encrypted file
actual class SecureSettingsFactory {
    actual fun create(): Settings {
        // AES-256 encrypted Properties file, key from JVM KeyStore
        val props = loadEncryptedProperties()
        return PropertiesSettings(props) { updated ->
            saveEncryptedProperties(updated)  // AES-encrypt → write to disk on every change
        }
    }
}
```

**DI module in core-base/datastore:**

```kotlin
// core-base/datastore/…/DatastoreBaseModule.kt
val DatastoreBaseModule = module {
    single<Settings>(named("plain")) { Settings() }
    single<Settings>(named("secure")) { get<SecureSettingsFactory>().create() }
}
```

**How core/datastore consumes it (app-specific):**

```kotlin
// core/datastore/build.gradle.kts — ADD:
commonMain.dependencies {
    implementation(projects.coreBase.datastore)  // Gets Settings(plain) + Settings(secure)
}

// core/datastore/…/UserPreferencesRepositoryImpl.kt — CHANGE:
class UserPreferencesRepositoryImpl(
    @Named("plain") private val settings: Settings,       // theme, language, onboarding
    @Named("secure") private val secureSettings: Settings, // passcode, authToken, userId
    private val dispatcher: DispatcherManager,
)
// Both are standard Settings — encodeValue/decodeValue/coroutines all work identically
```

### Dependency Direction (No Cycles)

```
core-base/security    ← depends on: core-base/common
core-base/datastore   ← depends on: core-base/common, core-base/security
                      ← NO dependency on core/datastore, core/model

core/database         → depends on: core-base/security (gets FieldEncryptor for TypeConverters)
core/datastore        → depends on: core-base/datastore (gets plain + secure Settings)
core-base/network     → depends on: core-base/security (gets CertPinConfig, EncryptedCache)
core/data             → depends on: core-base/security (gets SecureWipe, SessionManager)
feature/*             → depends on: core-base/security (gets BiometricAuth, SessionManager)
```

### DI Initialization Order (Updated)

```kotlin
// cmp-navigation/src/commonMain/kotlin/cmp/navigation/di/KoinModules.kt
// Each app module creates SecurityConfig and passes it as a function param:
//   Android: securityModule(SecurityConfig(isReleaseBuild = !BuildConfig.DEBUG))
//   Desktop: securityModule(SecurityConfig(isReleaseBuild = System.getProperty("app.release") == "true"))
//   iOS:     securityModule(SecurityConfig(isReleaseBuild = !Platform.isDebugBinary))
//   Web:     securityModule(SecurityConfig(isReleaseBuild = js("process.env.NODE_ENV") == "production"))
fun allModules(config: SecurityConfig) = listOf(
    securityModule(config), // ← NEW: FIRST — provides encryption keys/config + SecurityConfig
    DatastoreBaseModule,    // ← NEW: SECOND — provides Settings(plain) + Settings(secure)
    dataModule,          // core/data — UserLogoutManager now gets SecureWipe
    DatabaseModule,      // core/database — now gets FieldEncryptor from SecurityModule
    dispatcherModule,    // core-base/common
    analyticsModule,     // core-base/analytics
    DatastoreModule,     // core/datastore — now gets Settings from DatastoreBaseModule
    featureModule,       // feature/* — ViewModels get BiometricAuth, SessionManager
    AppModule,           // cmp-navigation
)
// Called from each app's Application/main:
// Android: startKoin { modules(allModules(SecurityConfig(!BuildConfig.DEBUG))) }
// Desktop: startKoin { modules(allModules(SecurityConfig(System.getProperty("app.release") == "true"))) }
```

**Initialization order rationale:**
1. `securityModule(config)` FIRST — receives `SecurityConfig` as a function parameter (avoids Koin graph lookup timing issue). Provides encryption keys, `FieldEncryptor`, `FailedAttemptTracker`.
2. `DatastoreBaseModule` SECOND — creates `SecureSettingsFactory` using keys from SecurityModule, provides `Settings(plain)` + `Settings(secure)`. `FailedAttemptTracker` resolves `Settings(named("plain"))` from here.
3. `DatabaseModule` — gets `FieldEncryptor` from SecurityModule for TypeConverters via `.addTypeConverter()`.
4. `DatastoreModule` — gets both `Settings` instances from DatastoreBaseModule.

---

## Injection Points (Exact Files + Lines)

### 1. Database Field Encryption (SEC-1) — Application-Layer

**Why not driver-level?** SQLCipher has NO `SQLiteDriver` implementation for Room 3 KMP (only Room 2's legacy `SupportSQLiteOpenHelper.Factory`). See GAP-B1.

**Strategy:** `FieldEncryptor` (from `core-base/security`) encrypts sensitive data BEFORE Room stores it. Non-sensitive data stays plaintext for query performance. `BundledSQLiteDriver()` remains unchanged on all platforms.

**File:** `core/database/src/commonMain/…/ChargeTypeConverters.kt` (and all TypeConverters with sensitive data)

**Important:** Room 3 instantiates `@TypeConverters` classes via **no-arg constructor**. Constructor injection is NOT supported. Must use `.addTypeConverter()` on the database builder to provide pre-constructed instances with `FieldEncryptor`.

```kotlin
// BEFORE:
class ChargeTypeConverters {
    @TypeConverter
    fun fromChargeList(charges: List<Charge>): String =
        Json.encodeToString(charges)
}

// AFTER:
class SecureChargeTypeConverters(private val encryptor: FieldEncryptor) {
    @TypeConverter
    fun fromChargeList(charges: List<Charge>): String =
        encryptor.encrypt(Json.encodeToString(charges))

    @TypeConverter
    fun toChargeList(data: String): List<Charge> {
        // Prefix-based detection: encrypted data starts with "ENC:" header
        val json = if (data.startsWith("ENC:")) {
            encryptor.decrypt(data.removePrefix("ENC:"))
        } else {
            data  // Legacy plaintext — still readable during migration
        }
        return Json.decodeFromString(json)
    }
}
```

**Database builder wiring** (in each platform's `DatabaseModule.*.kt`):

```kotlin
// Wire FieldEncryptor into TypeConverters via .addTypeConverter()
val encryptor = get<FieldEncryptor>()
Room.databaseBuilder<AppDatabase>(...)
    .addTypeConverter(SecureChargeTypeConverters(encryptor))
    .setDriver(BundledSQLiteDriver())  // Unchanged — no SQLCipher needed
    .build()
```

**Encrypted data prefix:** All encrypted field values are prefixed with `"ENC:"` to distinguish from legacy plaintext. This solves:
- Migration atomicity (GAP-P2): TypeConverters auto-detect plaintext vs encrypted per-row
- Downgrade safety (GAP-P11): Old app versions see `"ENC:..."` → try-catch returns empty (not crash)
- Crash-safe migration (GAP-P2): No separate migration pass needed — data encrypts on next write

**WAL is no longer a concern:** WAL/SHM files only contain already-encrypted field values. SEC-20 is automatically resolved.

### 2. Settings Plain/Secure Split via core-base/datastore (SEC-2, SEC-3)

`core-base/datastore` provides two `Settings` instances (plain + encrypted) using the **same `multiplatform-settings` API**. `core/datastore` consumes them via Koin named injection.

**File:** `core-base/datastore/src/commonMain/…/di/DatastoreBaseModule.kt` (NEW)

```kotlin
val DatastoreBaseModule = module {
    single<Settings>(named("plain")) { Settings() }
    single<Settings>(named("secure")) { get<SecureSettingsFactory>().create() }
}
```

**File:** `core/datastore/src/commonMain/…/di/DatastoreModule.kt` (MODIFIED)

```kotlin
// BEFORE (line 20-26):
val DatastoreModule = module {
    includes(CommonModule)
    single<Settings> { Settings() }
    singleOf(::UserPreferencesRepositoryImpl) bind UserPreferencesRepository::class
}

// AFTER:
val DatastoreModule = module {
    includes(CommonModule, DatastoreBaseModule)
    // Settings(plain) + Settings(secure) already provided by DatastoreBaseModule
    // NOTE: singleOf() does NOT support @Named params — must use manual single{}
    single<UserPreferencesRepository> {
        UserPreferencesRepositoryImpl(
            settings = get(named("plain")),
            secureSettings = get(named("secure")),
            dispatcher = get(),
        )
    }
}
```

**File:** `core/datastore/src/commonMain/…/UserPreferencesRepositoryImpl.kt` (MODIFIED)

```kotlin
// BEFORE (line 34-37):
class UserPreferencesRepositoryImpl(
    private val settings: Settings,
    private val dispatcher: DispatcherManager,
)

// AFTER:
class UserPreferencesRepositoryImpl(
    private val settings: Settings,         // plain: theme, language, onboarding, etc.
    private val secureSettings: Settings,   // secure: passcode, authToken, activeUserId
    private val dispatcher: DispatcherManager,
)
// NOTE: No @Named annotations — Koin doesn't use them for resolution.
// Injection is explicit in DatastoreModule via get(named("plain")) / get(named("secure")).
// ZERO API change — both are standard Settings
// encodeValue/decodeValue/serialization/coroutines all work identically
```

**Data split — what goes where:**

| Settings("plain") | Settings("secure") |
|-------------------|-------------------|
| `themeBrand` | `passcode` |
| `darkThemeConfig` | `activeUserId` |
| `useDynamicColor` | `isAuthenticated` |
| `appLanguage` | `authToken` |
| `showOnboarding` | |
| `firstTimeUser` | |
| `enableScreenCapture` | |
| `isPasscodeEnabled` | |
| `isBiometricsEnabled` | |
| `isUnlocked` | |

**Platform backends (all return standard `Settings`):**

| Platform | Plain | Secure |
|----------|-------|--------|
| Android | `SharedPreferencesSettings` | `SharedPreferencesSettings(EncryptedSharedPreferences)` |
| iOS | `NSUserDefaultsSettings` | `KeychainSettings(service)` |
| Desktop | `PreferencesSettings` | `PropertiesSettings` + AES-encrypted file |
| Web | `StorageSettings(localStorage)` | Web Crypto API wrapper |

### 3. Network Security (SEC-4, SEC-21, SEC-25)

Security provides `CertificatePinConfig` + `EncryptedCacheInterceptor` → core-base/network consumes them.

**File (each platform):** `core-base/network/src/{platform}Main/…/KtorHttpClient.*.kt`

```kotlin
// Android/Desktop (OkHttp) — BEFORE (line 16):
actual fun httpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient {
    return HttpClient(OkHttp) { config(this) }
}

// AFTER:
actual fun httpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient {
    return HttpClient(OkHttp) {
        engine {
            config {
                val pinConfig = KoinPlatform.getKoin().getOrNull<CertificatePinConfig>()
                if (pinConfig != null && pinConfig.pins.isNotEmpty()) {
                    certificatePinner(pinConfig.toOkHttpPinner())
                }
                // SEC-25: Centralized encrypted cache (NOT disabled — cached but encrypted)
                val encryptedCache = KoinPlatform.getKoin().getOrNull<EncryptedCacheProvider>()
                if (encryptedCache != null) {
                    cache(encryptedCache.createEncryptedCache())
                }
            }
        }
        config(this)
    }
}
```

**iOS/macOS (Darwin engine) — `core-base/network/src/nativeMain/…/KtorHttpClient.native.kt`:**

```kotlin
// Uses handleChallenge for cert pinning (NOT OkHttp's CertificatePinner)
actual fun httpClient(config: HttpClientConfig<*>.() -> Unit): HttpClient {
    return HttpClient(Darwin) {
        engine {
            val pinConfig = KoinPlatform.getKoin().getOrNull<CertificatePinConfig>()
            if (pinConfig != null && pinConfig.pins.isNotEmpty()) {
                handleChallenge { session, task, challenge, completionHandler ->
                    if (challenge.protectionSpace.authenticationMethod ==
                        NSURLAuthenticationMethodServerTrust) {
                        val serverTrust = challenge.protectionSpace.serverTrust
                        val host = challenge.protectionSpace.host
                        if (pinConfig.validate(host, serverTrust)) {
                            completionHandler(
                                NSURLSessionAuthChallengeUseCredential,
                                NSURLCredential.credentialForTrust(serverTrust!!)
                            )
                        } else {
                            completionHandler(
                                NSURLSessionAuthChallengeCancelAuthenticationChallenge, null
                            )
                        }
                    }
                }
            }
        }
        config(this)
    }
}
```

**SEC-25 — Encrypted HTTP Cache (centralized via security module):**

```kotlin
// core-base/security/src/commonMain/…/EncryptedCacheProvider.kt
expect class EncryptedCacheProvider {
    fun createEncryptedCache(): Cache  // OkHttp Cache with encrypted storage
}

// androidMain/desktopMain — OkHttp Cache with EncryptingFileSystem (AES-256 wrapper over okio.FileSystem)
// nativeMain — NOT applicable: Darwin engine uses NSURLSession with its own cache.
//              iOS/macOS rely on NSURLSessionConfiguration.urlCache with NSFileProtectionComplete
//              (OS-level encryption when device is locked). No custom cache encryption needed.
// jsMain/wasmJsMain — no disk cache on web (browser handles caching)
```

**Token refresh Mutex** — `core-base/network/…/KtorHttpClient.kt:89-97`:

```kotlin
// Add to setupDefaultHttpClient():
private val refreshMutex = Mutex()

bearer {
    loadTokens { bearerTokensProvider() }
    if (bearerRefreshProvider != null) {
        refreshTokens {
            refreshMutex.withLock {
                val currentTokens = bearerTokensProvider()
                if (currentTokens != oldTokens) currentTokens
                else bearerRefreshProvider()
            }
        }
    }
}
```

### 4. Logout / Wipe Hook (SEC-14, SEC-28, SEC-29)

Security provides `SecureWipe` + `SessionManager` → core/data consumes them.

**File:** `core/data/src/commonMain/kotlin/org/mifos/core/data/repositoryImpl/UserLogoutManagerImpl.kt`

```kotlin
// BEFORE (line 25-28):
class UserLogoutManagerImpl(
    private val repository: UserPreferencesRepository,
    private val dispatcher: DispatcherManager,
)

// AFTER:
class UserLogoutManagerImpl(
    private val repository: UserPreferencesRepository,
    private val secureWipe: SecureWipe,           // From SecurityModule
    private val sessionManager: SessionManager,   // From SecurityModule
    private val dispatcher: DispatcherManager,
)
```

**Logout wipe (lines 40-45):**
```kotlin
override fun logout(userId: Long, reason: LogoutReason) {
    scope.launch {
        when (reason) {
            LogoutReason.TooManyUnlockAttempts ->
                secureWipe.executeWipe(WipeReason.BRUTE_FORCE)
            LogoutReason.SecurityStamp ->
                secureWipe.executeWipe(WipeReason.TAMPER_DETECTED)
            else -> {
                repository.clearUserData()
                secureWipe.scrubSensitiveMemory()
                sessionManager.endSession()
            }
        }
        _logoutEventFlow.emit(LogoutEvent(userId))
    }
}
```

### 5. Gradle Dependency Wiring

```kotlin
// core-base/security/build.gradle.kts (NEW)
plugins { alias(libs.plugins.kmp.core.base.library.convention) }
kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation(projects.coreBase.common)  // DispatcherManager
        }
        androidMain.dependencies {
            implementation(libs.androidx.security.crypto)  // Android Keystore key management
            implementation(libs.androidx.biometric)
            implementation(libs.play.integrity)
        }
        desktopMain.dependencies {
            implementation(libs.bouncycastle)  // AES-256-GCM for JVM (FieldEncryptor)
        }
        // nativeMain: uses CommonCrypto (system framework, no dep needed)
        // jsCommonMain: uses SubtleCrypto (browser API, no dep needed)
    }
}

// core/database/build.gradle.kts — ADD:
commonMain.dependencies {
    implementation(projects.coreBase.security)  // Gets FieldEncryptor for TypeConverters
}

// core-base/datastore/build.gradle.kts (NEW)
plugins { alias(libs.plugins.kmp.core.base.library.convention) }
kotlin {
    sourceSets {
        commonMain.dependencies {
            implementation(projects.coreBase.common)
            implementation(projects.coreBase.security)
            implementation(libs.multiplatform.settings)
            implementation(libs.multiplatform.settings.serialization)
            implementation(libs.multiplatform.settings.coroutines)
        }
        androidMain.dependencies {
            implementation(libs.androidx.security.crypto)  // EncryptedSharedPreferences
        }
    }
}

// core/datastore/build.gradle.kts — CHANGE:
commonMain.dependencies {
    implementation(projects.coreBase.datastore)  // Gets Settings(plain) + Settings(secure)
    // Remove direct multiplatform-settings deps — provided transitively
}

// core-base/network/build.gradle.kts — ADD:
commonMain.dependencies {
    implementation(projects.coreBase.security)  // Gets CertPinConfig, EncryptedCache
}

// core/data/build.gradle.kts — ADD:
commonMain.dependencies {
    implementation(projects.coreBase.security)  // Gets SecureWipe, SessionManager
}

// settings.gradle.kts — ADD (after line 84):
include(":core-base:security")
include(":core-base:datastore")
```

---

## Architecture: `core-base/security` Module

```
core-base/security/
├── src/commonMain/kotlin/template/core/base/security/
│   ├── SecurityConfig.kt             ← data class: isReleaseBuild flag (debug/release gate)
│   ├── FieldEncryptor.kt             ← expect: AES-256-GCM per-field encryption
│   ├── SecureKeyProvider.kt          ← expect: platform key storage (Keystore/Keychain/JVM KeyStore)
│   ├── CertificatePinConfig.kt       ← data class: pin sets per hostname
│   ├── TamperDetection.kt            ← expect: integrity checks
│   ├── BiometricAuth.kt              ← expect: biometric gate
│   ├── SecureWipe.kt                 ← expect: self-destruct / remote wipe
│   ├── SecurityPolicy.kt             ← data class: configurable policy
│   ├── EncryptedCacheProvider.kt     ← expect: encrypted OkHttp disk cache
│   ├── FailedAttemptTracker.kt        ← common: brute-force counter (uses plain Settings, not a secret)
│   ├── SessionManager.kt             ← common: inactivity timeout + background lock
│   ├── SecureRandom.kt               ← expect: crypto-quality RNG
│   ├── SensitiveString.kt            ← common: zeroable credential wrapper
│   └── di/SecurityModule.kt          ← Koin module (includes platformSecurityModule)
│
├── src/androidMain/kotlin/template/core/base/security/
│   ├── AndroidFieldEncryptor.kt      ← javax.crypto AES-256-GCM (key from Android Keystore)
│   ├── AndroidSecureKeyProvider.kt   ← Android Keystore AES key generation/retrieval
│   ├── AndroidTamperDetection.kt     ← Play Integrity API + root checks
│   ├── AndroidBiometricAuth.kt       ← BiometricPrompt with CryptoObject
│   ├── AndroidSecureWipe.kt          ← Zero-fill DB + delete keys + clear prefs
│   ├── AndroidSecureRandom.kt        ← java.security.SecureRandom
│   ├── AndroidClipboardSecurity.kt   ← ClipboardManager auto-wipe
│   └── di/SecurityModule.android.kt  ← actual platformSecurityModule
│
├── src/nativeMain/kotlin/template/core/base/security/
│   ├── IosFieldEncryptor.kt          ← CommonCrypto AES-256-GCM (key from Keychain)
│   ├── IosSecureKeyProvider.kt       ← Keychain Services key generation/retrieval
│   ├── IosTamperDetection.kt         ← DeviceCheck + jailbreak heuristics
│   ├── IosBiometricAuth.kt           ← LAContext (Face ID / Touch ID)
│   ├── IosSecureWipe.kt              ← Keychain wipe + file overwrite
│   ├── IosSecureRandom.kt            ← SecRandomCopyBytes
│   └── di/SecurityModule.native.kt   ← actual platformSecurityModule
│
├── src/desktopMain/kotlin/template/core/base/security/
│   ├── DesktopFieldEncryptor.kt      ← BouncyCastle AES-256-GCM (key from JVM KeyStore)
│   ├── DesktopSecureKeyProvider.kt   ← JVM KeyStore key generation/retrieval
│   ├── DesktopSecureWipe.kt          ← Secure file deletion + key removal
│   ├── DesktopSecureRandom.kt        ← java.security.SecureRandom
│   └── di/SecurityModule.desktop.kt  ← actual platformSecurityModule
│
├── src/jsCommonMain/kotlin/template/core/base/security/
│   ├── WebFieldEncryptor.kt          ← SubtleCrypto AES-256-GCM
│   ├── WebSecureRandom.kt            ← crypto.getRandomValues
│   ├── WebBiometricAuth.kt           ← no-op (BiometricResult.NotAvailable)
│   ├── WebTamperDetection.kt         ← no-op (TamperResult.Safe)
│   └── di/SecurityModule.js.kt       ← actual platformSecurityModule
│
├── src/commonTest/kotlin/…/
│   ├── FailedAttemptTrackerTest.kt
│   ├── SessionManagerTest.kt
│   ├── SensitiveStringTest.kt
│   └── SecurityPolicyTest.kt
│
└── build.gradle.kts
```

---

## SecurityModule Koin Definition

```kotlin
// commonMain — di/SecurityModule.kt
fun securityModule(config: SecurityConfig) = module {
    includes(platformSecurityModule)

    // SecurityConfig provided by caller (each app module passes its own)
    // This avoids init-order issues — no get<SecurityConfig>() from Koin graph
    single { config }

    // Common singletons — use manual single{} to disambiguate named Settings
    single { FailedAttemptTracker(get(named("plain"))) }  // uses plain Settings (not secure)
    single { SessionManager(get(), get()) }               // config + dispatcher
    single { SecurityPolicy.default() }
}

expect val platformSecurityModule: Module

// androidMain — di/SecurityModule.android.kt
actual val platformSecurityModule: Module = module {
    single<SecureKeyProvider> { AndroidSecureKeyProvider() }
    single<FieldEncryptor> { AndroidFieldEncryptor(get()) }
    single<BiometricAuth> { AndroidBiometricAuth(androidContext()) }
    single<TamperDetection> { AndroidTamperDetection(androidContext()) }
    single<SecureWipe> { AndroidSecureWipe(androidContext(), get(), get()) }
    single<SecureRandom> { AndroidSecureRandom() }
    single<CertificatePinConfig> { CertificatePinConfig.default() }
    single<EncryptedCacheProvider> { AndroidEncryptedCacheProvider(get()) }
}

// nativeMain — di/SecurityModule.native.kt
actual val platformSecurityModule: Module = module {
    single<SecureKeyProvider> { IosSecureKeyProvider() }
    single<FieldEncryptor> { IosFieldEncryptor(get()) }
    single<BiometricAuth> { IosBiometricAuth() }
    single<TamperDetection> { IosTamperDetection() }
    single<SecureWipe> { IosSecureWipe(get(), get()) }
    single<SecureRandom> { IosSecureRandom() }
    single<CertificatePinConfig> { CertificatePinConfig.default() }
    // No EncryptedCacheProvider — Darwin engine uses NSURLSession with OS-level
    // NSFileProtectionComplete encryption. No custom cache encryption needed.
}

// desktopMain — di/SecurityModule.desktop.kt
actual val platformSecurityModule: Module = module {
    single<SecureKeyProvider> { DesktopSecureKeyProvider() }
    single<FieldEncryptor> { DesktopFieldEncryptor(get()) }
    single<SecureWipe> { DesktopSecureWipe(get(), get()) }
    single<SecureRandom> { DesktopSecureRandom() }
    single<CertificatePinConfig> { CertificatePinConfig.default() }
    single<EncryptedCacheProvider> { DesktopEncryptedCacheProvider(get()) }
    // BiometricAuth/TamperDetection: no-op on desktop
}

// jsCommonMain — di/SecurityModule.js.kt (shared by js + wasmJs)
actual val platformSecurityModule: Module = module {
    single<FieldEncryptor> { WebFieldEncryptor() }
    single<SecureRandom> { WebSecureRandom() }
    single<BiometricAuth> { WebBiometricAuth() }         // no-op
    single<TamperDetection> { WebTamperDetection() }     // no-op
    // No disk cache, secure wipe, or cert pinning on web
}
```

---

## Design Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Application-layer field encryption via `FieldEncryptor` | SQLCipher has NO `SQLiteDriver` for Room 3 KMP (only Room 2 legacy API). `FieldEncryptor` encrypts sensitive fields BEFORE Room stores them. Uses platform AES-256-GCM (Android Keystore / iOS Keychain / JVM KeyStore / SubtleCrypto). Zero native library overhead. |
| D2 | Hardware-backed key storage (Keystore/Keychain) | Hardware keys can't be extracted even on rooted device |
| D3 | Self-destruct: 10 failed attempts = local wipe + remote wipe | Prevents brute-force. Remote wipe covers theft. Configurable policy. |
| D4 | Field-level encryption for DB + field-level for DataStore/memory | `FieldEncryptor` encrypts sensitive TypeConverter fields in Room. Non-sensitive data (UI state, cached lists) stays plaintext for query performance. |
| D5 | Encrypt at TypeConverter/Repository level, NOT driver level | Driver-level (SQLCipher) is unavailable for Room 3 KMP. TypeConverter-level encryption targets only sensitive fields. Trade-off: not all data encrypted, but queryable columns remain fast. |
| D6 | Config-driven certificate pinning with backup pins | Hard-coded pins cause lockout on cert rotation. Config allows OTA pin updates. |
| D7 | Tiered biometric: app unlock + per-transaction | Balance security and UX. Browse = session, sensitive ops = per-transaction. |
| D8 | SecurityPolicy as configurable data class | Consumer apps have different risk profiles. Template provides sensible defaults. |
| D9 | WAL mode stays (no TRUNCATE needed) | With application-layer encryption, data is encrypted BEFORE Room stores it. WAL/SHM files only contain already-encrypted field values. No plaintext leak. No performance penalty from TRUNCATE mode. |
| D10 | Mutex-guarded token refresh | Prevents race where two concurrent 401s produce conflicting token states. |
| D11 | Passcode as SensitiveString (CharArray, zero-on-use) | JVM String is immutable, lingers in memory. CharArray can be zeroed. |
| D12 | Clipboard auto-wipe at 60s | Prevents clipboard sniffing. Android 13+ built-in; we add for older. |
| D13 | Store cache eviction on logout | Explicit clear that deletes from both in-memory cache AND Room SOT. |
| D14 | **SecurityModule initializes FIRST in Koin** | DB and DataStore need encryption keys at creation. Security must provide them before consumers request. |
| D15 | **Security module in core-base/ (not core/)** | core-base/ is the foundation layer. Security primitives are infrastructure, not business logic. Follows existing pattern: core-base/common, core-base/network, core-base/database. |
| D16 | **No circular dependencies** | Security depends ONLY on core-base/common. All other modules depend on security, never the reverse. |
| D17 | **Debug/Release gate via `SecurityConfig.isReleaseBuild`** | Single boolean controls all conditional hardening. Passed as function parameter to `securityModule(config)` — avoids Koin init-order issues. Phase 1 uses `isReleaseBuild` param on `setupDefaultHttpClient()` before SecurityConfig exists. Phase 2+ uses SecurityConfig from Koin. Debug builds retain full visibility. |
| D18 | **Encrypted HTTP cache, not disabled** | Disabling cache hurts performance and UX. Instead, `EncryptedCacheProvider` wraps OkHttp cache with AES-256 encrypted storage. Cache works normally but content is unreadable without app key. Centralized in security module. |
| D19 | **println() → Kermit logger, not removed** | Raw `println()` is unstructured and uncontrollable. Kermit logger provides: tagged output, severity levels, automatic stripping by ProGuard in release builds. Debug visibility preserved. |
| D20 | **Demo credentials are intentional** | `secrets_demo/`, `google-services.json`, `Wizard@123`, `RblClientIdProp` are build-only demo values. Real secrets never in code. No cleanup needed. |
| D21 | **`core-base/datastore` for encrypted Settings (not `core-base/security`)** | Secure storage is a datastore concern, not a security primitive. `SecureSettingsFactory` returns standard `multiplatform-settings` `Settings` interface — zero API change for consumers. `core-base/security` provides encryption keys, `core-base/datastore` provides encrypted settings. Clean separation. |
| D22 | **Same `Settings` API for plain and encrypted** | `EncryptedSharedPreferences` implements `SharedPreferences` → `SharedPreferencesSettings(encryptedPrefs)` returns a standard `Settings`. Koin `named("plain")` / `named("secure")` qualifiers differentiate (no `@Named` annotations — explicit `get(named())` in module). `encodeValue`/`decodeValue`/`serialization`/`coroutines` all work identically on both. No new abstraction needed. |
| D23 | **`securityModule(config)` function, not `SecurityModule` val** | SecurityConfig is passed as a function parameter, not resolved from Koin graph. Avoids init-order chicken-and-egg: SecurityModule loads first but needs config that would otherwise be registered by app modules loading later. |
| D24 | **Encrypt-on-write with `"ENC:"` prefix, not batch migration** | TypeConverters read both plaintext and `"ENC:"`-prefixed encrypted data. New writes always encrypt. No separate migration pass = no crash-safety concerns. Data migrates gradually as rows are updated. Old app versions see `"ENC:..."` → try-catch returns empty (graceful degradation). |
| D25 | **iOS cache: OS-level encryption, not custom** | NSURLCache has no encryption API. Darwin engine relies on iOS `NSFileProtectionComplete` — data encrypted when device is locked. Custom encrypted cache only needed for OkHttp (Android/Desktop). |
| D26 | **Desktop key storage: OS credential APIs** | JVM KeyStore requires a password (chicken-and-egg). Desktop uses OS-specific APIs: macOS Keychain (JNI), Linux libsecret, Windows DPAPI. BouncyCastle provides AES operations only, not key storage. |

---

## SecurityConfig — Debug vs Release Gate

All debug/release-conditional behavior is controlled by a single `SecurityConfig.isReleaseBuild` flag:

```kotlin
// core-base/security/src/commonMain/…/SecurityConfig.kt
data class SecurityConfig(
    val isReleaseBuild: Boolean,          // Set per-platform — NOT from BuildConfig in commonMain
    val maxFailedAttempts: Int = 10,
    val sessionTimeoutMinutes: Int = 30,
    val clipboardWipeSeconds: Int = 60,
    // ... other policy fields
)

// Usage pattern in any module:
val config = get<SecurityConfig>()
if (config.isReleaseBuild) {
    // hardened behavior (restrict logs, detect root, wipe clipboard, etc.)
} else {
    // debug: full visibility, no restrictions
}
```

**`SecurityConfig` is passed as a parameter to `securityModule(config)`** (NOT from Koin graph — avoids init-order issues). Each app module creates it at startup:

```kotlin
// cmp-android: allModules(SecurityConfig(isReleaseBuild = !BuildConfig.DEBUG))
// cmp-desktop: allModules(SecurityConfig(isReleaseBuild = System.getProperty("app.release") == "true"))
// cmp-ios:     allModules(SecurityConfig(isReleaseBuild = !Platform.isDebugBinary))
// cmp-web:     allModules(SecurityConfig(isReleaseBuild = js("process.env.NODE_ENV") == "production"))
```

---

## Phase 1: Immediate Fixes (No New Module Required)

**Effort: ~2 hours | Blocks: Any release**

| Task | Gap | File | Change | Debug/Release |
|------|-----|------|--------|---------------|
| T1 | SEC-5 | `cmp-android/…/AndroidManifest.xml` | `android:allowBackup="false"` | Both |
| T2 | SEC-10 | `cmp-android/src/main/res/xml/network_security_config.xml` | Create file + reference in manifest | Both |
| T3 | SEC-12 | `core-base/network/…/KtorHttpClient.kt:78` | Add `isReleaseBuild: Boolean` param to `setupDefaultHttpClient()`. Each platform actual passes it (`!BuildConfig.DEBUG` on Android, `!Platform.isDebugBinary` on iOS, etc.). `if (isReleaseBuild) prettyPrint = false`. Phase 2 refactors to `SecurityConfig`. | **Release only** — debug keeps `prettyPrint = true` |
| T4 | SEC-7 | `KtorHttpClient.kt:74`, `UserData.kt`, `AuthState.kt` | Same `isReleaseBuild` param → `if (isReleaseBuild) LogLevel.HEADERS` + redacted `toString()`. Phase 2 refactors to `SecurityConfig`. | **Release only** — debug keeps `LogLevel.ALL` for full visibility |
| T4.1 | SEC-24 | `cmp-android/…/provider_paths.xml` | Restrict to `path="images/"` and `path="shared/"` | Both |
| T4.2 | SEC-26 | `core-base/network/…/ResultSuspendConverterFactory.kt:80,95,107` | Replace `println()` → Kermit `co.touchlab.kermit.Logger.d { }` | **Both** — proper debug logging (visible in debug, stripped by ProGuard in release) |
| T4.3 | SEC-27 | `core/database/…/ChargeTypeConverters.kt` | Wrap `Json.decodeFromString` in try-catch | Both |
| T4.4 | SEC-23 | `core-base/ui/…/ShareUtils.android.kt` | `if (!BuildConfig.DEBUG) Handler.postDelayed(clearClipboard, 60_000)`. Phase 2 refactors to `SecurityConfig`. | **Release only** — debug keeps clipboard |

---

## Phase 2: core-base/security Module — Encrypted Storage

**Effort: ~17 hours | Depends on: Phase 1**

| Task | Gap | What | Where | Debug/Release |
|------|-----|------|-------|---------------|
| T5 | — | Security module scaffold + build.gradle.kts + settings.gradle.kts + `SecurityConfig` | `core-base/security/` | Both |
| T5.1 | — | Datastore module scaffold + `SecureSettingsFactory` expect/actual + `DatastoreBaseModule` | `core-base/datastore/` | Both |
| T6 | SEC-3 | `SecureSettingsFactory` platform impls (EncryptedSharedPreferences / Keychain / JVM KeyStore / WebCrypto) | `core-base/datastore/src/{platform}Main/` | Both |
| T7 | SEC-1, SEC-16, SEC-20 | `FieldEncryptor` + `SecureKeyProvider` expect/actual. Wire into Room TypeConverters via `.addTypeConverter()` on database builder. Prefix-based detection (`"ENC:"`) for plaintext/encrypted coexistence. | `core-base/security/` + `core/database/` | Both |
| T7.1 | SEC-1 | DB field migration: **encrypt-on-write** strategy (no separate migration pass). TypeConverters read both plaintext and `"ENC:"`-prefixed data. New writes always encrypt. Data migrates gradually as rows are updated. Optional background migration for bulk encryption. | `core/database/` | Both |
| T8 | SEC-2 | Split UserData into `SecureUserData` + `UserPreferences`, wire plain/secure Settings via Koin `get(named())` in DatastoreModule (no `@Named` annotations) | `core/datastore/` + `core/model/` | Both |
| T8.1 | SEC-2 | Settings migration: read old `user_data_key` blob → write secure first → write plain second → delete old key LAST. Order ensures crash-safety: old key persists until both writes succeed. On next launch, detect old key → retry migration. | `core/datastore/` | Both |
| T9 | SEC-4 | CertificatePinConfig + platform pinning (OkHttp/Darwin) | `core-base/security/` + `core-base/network/` | Both |
| T9.1 | SEC-21 | Token refresh Mutex in bearer auth | `core-base/network/…/KtorHttpClient.kt` | Both |
| T9.2 | SEC-32 | SecureRandom expect/actual per platform | `core-base/security/src/{platform}Main/` | Both |
| T9.3 | SEC-31 | SensitiveString (CharArray wrapper + zero-on-use) | `core-base/security/src/commonMain/` | Both |
| T9.4 | SEC-25 | EncryptedCacheProvider (Android/Desktop: OkHttp `EncryptingFileSystem`. iOS: rely on OS `NSFileProtectionComplete`. Web: no disk cache.) | `core-base/security/src/{android,desktop}Main/` | **Both** — cache is encrypted, not disabled |

---

## Phase 3: Advanced Protection

**Effort: ~13.5 hours | Depends on: Phase 2**

| Task | Gap | What | Where | Debug/Release |
|------|-----|------|-------|---------------|
| T10 | SEC-6 | TamperDetection expect/actual (root/jailbreak + Play Integrity) | `core-base/security/src/{platform}Main/` | **Release only** — `if (!config.isReleaseBuild) return TamperResult.Safe` |
| T11 | SEC-14 | SecureWipe expect/actual (encryption key deletion + DB file deletion + pref clear). Key deletion makes encrypted data permanently unreadable — no need for zero-fill on flash storage. | `core-base/security/src/{platform}Main/` | Both |
| T12 | SEC-14 | FailedAttemptTracker (5→lock, 10→wipe) | `core-base/security/src/commonMain/` | Both |
| T13 | SEC-13 | BiometricAuth expect/actual (BiometricPrompt/LAContext) | `core-base/security/src/{platform}Main/` | Both |
| T14 | SEC-9 | Memory scrubbing on logout | `core-base/store/` + `core/data/` | Both |
| T14.1 | SEC-30 | SessionManager (inactivity timeout + background lock). Requires `AppLifecycleObserver` expect/actual: Android `ProcessLifecycleOwner`, iOS `UIApplication` notifications, Desktop window focus listener. | `core-base/security/src/{platform}Main/` | Both |
| T14.2 | SEC-29 | Store cache eviction API (`clearAll()` on logout) | `core-base/store/…/StoreDataExtensions.kt` | Both |
| T14.3 | SEC-28 | Flow state clearing on logout (clear StateFlows before nav) | `core/data/…/UserLogoutManagerImpl.kt` | Both |

---

## Phase 4: Hardening

**Effort: ~7 hours | Depends on: Phase 3**

| Task | Gap | What | Where |
|------|-----|------|-------|
| T15 | SEC-11 | ProGuard/R8 rules for Room 3 + sensitive models + FieldEncryptor | `cmp-android/proguard-rules.pro` |
| T16 | SEC-15 | `exportSchema = false` | `core/database/…/AppDatabase.kt` |
| T17 | SEC-16 | FieldEncryptor for DataStore sensitive fields | `core-base/security/` + `core/datastore/` |
| T18 | SEC-17 | Desktop secure storage (macOS Keychain, Linux libsecret, Windows DPAPI) | `core-base/security/src/desktopMain/` |
| T18.1 | SEC-33 | Firebase consent mechanism (opt-in, disable until consent) | `core-base/analytics/` + `cmp-android/` |
| T18.2 | SEC-36 | Deep link validation framework (App Links verification) | `cmp-android/…/AndroidManifest.xml` |

---

## Execution Order

```
Phase 1 (immediate fixes, no new module)
├── T1: allowBackup=false                              [5 min]  Both
├── T2: network_security_config.xml                    [15 min] Both
├── T3: prettyPrint — add isReleaseBuild param to setupDefaultHttpClient [15 min] Release only
├── T4: LogLevel — isReleaseBuild gate + redacted toString [30 min] Release only
├── T4.1: Restrict FileProvider paths                  [10 min] Both
├── T4.2: println() → Kermit debug logger              [15 min] Both (stripped in release)
├── T4.3: TypeConverter error handling                 [10 min] Both
└── T4.4: Clipboard auto-wipe — release-only gate     [20 min] Release only

Phase 2 (core-base/security + core-base/datastore — ALL security wired centrally)
├── T5: Security module scaffold + DI + SecurityConfig [1.5 hrs] Both
│   ├── build.gradle.kts (convention plugin + platform deps)
│   ├── settings.gradle.kts (include :core-base:security)
│   ├── SecurityConfig.kt (isReleaseBuild flag — single debug/release gate)
│   ├── securityModule(config) function + expect platformSecurityModule
│   ├── FailedAttemptTracker: manual single{} with get(named("plain")) — not singleOf()
│   └── KoinModules.kt: allModules(config) function, each app passes SecurityConfig
├── T5.1: Datastore module scaffold                    [1 hr]   Both
│   ├── core-base/datastore/build.gradle.kts (convention plugin)
│   ├── settings.gradle.kts (include :core-base:datastore)
│   ├── SecureSettingsFactory.kt (expect class)
│   ├── DatastoreBaseModule.kt (Settings plain + secure)
│   └── KoinModules.kt (insert DatastoreBaseModule at position 1)
├── T6: SecureSettingsFactory platform impls           [3 hrs]  Both
│   ├── androidMain: EncryptedSharedPreferences → SharedPreferencesSettings
│   ├── nativeMain: Keychain Services → KeychainSettings
│   ├── desktopMain: JVM KeyStore + AES → PropertiesSettings
│   └── jsMain: Web Crypto API wrapper
├── T7: FieldEncryptor + TypeConverter wiring            [3 hrs]  Both
│   ├── core-base/security: FieldEncryptor expect/actual (AES-256-GCM per platform)
│   ├── core-base/security: SecureKeyProvider expect/actual (key generation/retrieval)
│   ├── core-base/security: Key loss detection — if SecureKeyProvider.getKey() returns null
│   │   and encrypted data exists → trigger re-auth flow (re-fetch from server)
│   ├── core/database: add dep on core-base/security (gets FieldEncryptor)
│   ├── core/database: wire FieldEncryptor via .addTypeConverter() on database builder
│   ├── core/database: "ENC:" prefix on all encrypted values for plaintext/encrypted detection
│   ├── core/database: update ChargeTypeConvertersTest for new constructor
│   └── BundledSQLiteDriver() stays unchanged — WAL mode stays (data encrypted before storage)
├── T7.1: DB field encrypt-on-write migration            [30 min] Both
│   ├── No separate migration pass — TypeConverters read both plaintext and "ENC:" data
│   ├── New writes always encrypt with "ENC:" prefix
│   ├── Data migrates gradually as rows are updated
│   └── Optional: background WorkManager/BGTaskScheduler job for bulk encryption
├── T8: Split UserData storage (plain/secure)          [1.5 hrs] Both
│   ├── core/model: add SecureUserData + UserPreferences data classes
│   ├── core/model: UserData.from(prefs, secure) factory method
│   ├── core/datastore: add dep on core-base/datastore
│   ├── DatastoreModule: includes(DatastoreBaseModule), manual single{} (Koin @Named not used)
│   ├── UserPreferencesRepositoryImpl: Settings(plain) + Settings(secure) — no @Named annotations
│   └── Merge via combine(prefsFlow, secureFlow) { p, s -> UserData.from(p, s) }
├── T8.1: Settings split migration (crash-safe)         [30 min] Both
│   ├── core/datastore: detect old user_data_key in plain Settings
│   ├── Write SecureUserData to secure Settings FIRST
│   ├── Write UserPreferences to plain Settings SECOND
│   ├── Delete old user_data_key LAST (ensures old key persists until both writes succeed)
│   └── On crash: next launch detects old key → retries migration idempotently
├── T9: Certificate pinning                            [2 hrs]  Both
│   ├── core-base/security: CertificatePinConfig data class
│   ├── core-base/network/androidMain: OkHttp CertificatePinner
│   ├── core-base/network/nativeMain: Darwin URLSession pinning
│   └── core-base/network/desktopMain: OkHttp CertificatePinner
├── T9.1: Token refresh Mutex                          [30 min] Both
├── T9.2: SecureRandom expect/actual                   [1 hr]   Both
├── T9.3: SensitiveString (CharArray)                  [30 min] Both
└── T9.4: EncryptedCacheProvider expect/actual          [2 hrs]  Both (encrypted, not disabled)

Phase 3 (advanced protection — all in core-base/security)
├── T10: TamperDetection expect/actual                 [2 hrs]  Release only
├── T11: SecureWipe expect/actual (key deletion, not zero-fill) [3 hrs] Both
│   └── core/data: wire SecureWipe into UserLogoutManagerImpl
├── T12: FailedAttemptTracker                          [1 hr]   Both
├── T13: BiometricAuth expect/actual                   [3 hrs]  Both
├── T14: Memory scrubbing                              [1 hr]   Both
├── T14.1: SessionManager + AppLifecycleObserver expect/actual [2.5 hrs] Both
├── T14.2: Store cache eviction API                    [30 min] Both
└── T14.3: Flow state clearing on logout               [30 min] Both

Phase 4 (hardening)
├── T15: ProGuard/R8 rules (Room 3 + FieldEncryptor)    [1 hr]   Release only
├── T16: Schema export=false                           [5 min]  Release only
├── T17: FieldEncryptor for DataStore                  [2 hrs]  Both
├── T18: Desktop secure storage                        [2 hrs]  Both
├── T18.1: Firebase consent mechanism                  [1 hr]   Release only
└── T18.2: Deep link validation                        [1 hr]   Both
```

---

## Verification Criteria

### Phase 1 Complete When:
- [ ] `adb backup` produces empty backup (allowBackup=false)
- [ ] **Release APK**: `adb logcat | grep -i "passcode\|token\|Bearer"` returns nothing
- [ ] **Debug APK**: `adb logcat` shows full `LogLevel.ALL` output (verified working)
- [ ] `grep -r "println" core-base/network/` returns zero results (all converted to Kermit)
- [ ] **Release APK**: Charles Proxy shows no prettified JSON bodies
- [ ] **Debug APK**: Charles Proxy shows prettified JSON (prettyPrint=true)
- [ ] **Release APK**: Clipboard auto-clears after 60s
- [ ] **Debug APK**: Clipboard persists normally
- [ ] Malformed JSON in DB column → graceful empty result (not crash)
- [ ] FileProvider only serves from `images/` and `shared/`

### Phase 2 Complete When:
- [ ] DB sensitive fields (e.g., ChargeTypeConverters output) are Base64-encoded ciphertext, not plaintext JSON (both builds)
- [ ] Non-sensitive DB fields remain queryable plaintext (performance preserved)
- [ ] DB field migration runs on first launch: existing plaintext → encrypted (both builds)
- [ ] Passcode not in plaintext `shared_prefs/` or NSUserDefaults (both builds)
- [ ] Passcode readable via `Settings(named("secure"))` — encrypted at rest
- [ ] Settings split migration runs on first launch: old `user_data_key` → `SecureUserData` + `UserPreferences`
- [ ] `Settings(named("plain"))` and `Settings(named("secure"))` both implement standard `Settings` interface
- [ ] `encodeValue`/`decodeValue` work identically on both Settings instances
- [ ] MITM proxy with custom CA cert fails TLS handshake (both builds, including Darwin/iOS)
- [ ] Two concurrent 401s → exactly one refresh call (both builds)
- [ ] All existing 25 Store tests still pass
- [ ] SecurityModule is first, DatastoreBaseModule is second in KoinModules.allModules
- [ ] `secureRandomBytes(32)` produces different output each call
- [ ] `core/database` depends on `core-base/security` (no reverse)
- [ ] `core/datastore` depends on `core-base/datastore` (no reverse)
- [ ] `core-base/datastore` depends on `core-base/security` (no reverse)
- [ ] HTTP cache exists but content is encrypted (not disabled)
- [ ] `SecurityConfig.isReleaseBuild` is `false` in debug, `true` in release
- [ ] Consumer apps get encrypted Settings automatically via `sync-dirs.sh` (core-base/datastore synced)
- [ ] JS/WasmJS targets compile with no-op BiometricAuth + TamperDetection actuals

### Phase 3 Complete When:
- [ ] **Release APK**: App detects rooted device and shows warning
- [ ] **Debug APK**: Root detection is skipped (no warning)
- [ ] 10 failed passcode attempts triggers data wipe (both builds)
- [ ] Remote wipe via FCM destroys all data (both builds)
- [ ] Biometric prompt on foreground when enabled (both builds)
- [ ] Memory dump after logout shows no tokens/passcodes (both builds)
- [ ] App locks after 30 min inactivity (both builds)
- [ ] Store caches empty after logout (both builds)
- [ ] StateFlow replays empty state after logout (both builds)

### Phase 4 Complete When:
- [ ] **Release APK**: decompilation doesn't show UserData/AuthState field names
- [ ] **Release APK**: Schema JSON not in APK resources
- [ ] Desktop DB unreadable without app key (both builds)
- [ ] **Release**: Firebase disabled until user consents
- [ ] Deep links validated before navigation (both builds)

---

## What's NOT in Scope

| Item | Reason |
|------|--------|
| Server-side encryption | Backend is Supabase — handles its own encryption |
| E2E message encryption | Not a messaging app — Store data is API responses |
| Custom crypto algorithms | Use proven standards (AES-256-GCM, PBKDF2, SHA-256) |
| Hardware security modules | Mobile devices don't have standalone HSMs |
| DRM/content protection | Not a media app |
| Git history rewriting (BFG) | Destructive — credentials in git are intentional demo/build-only |
| Demo credential removal | `secrets_demo/`, `google-services.json`, `Wizard@123`, `RblClientIdProp` are intentional build creds |
| Room version upgrade (alpha→stable) | Separate concern — track in its own plan |

---

## Dependencies (External Libraries)

| Library | Platform | Purpose | Add to `libs.versions.toml` |
|---------|----------|---------|---------------------------|
| `androidx.security:security-crypto:1.1.0-alpha06` | Android | EncryptedSharedPreferences + Android Keystore key management | `androidxSecurityCrypto = "1.1.0-alpha06"` |
| `androidx.biometric:biometric:1.2.0-alpha05` | Android | BiometricPrompt | `androidxBiometric = "1.2.0-alpha05"` |
| `com.google.android.play:integrity:1.3.0` | Android | Play Integrity API (tamper detection) | `playIntegrity = "1.3.0"` |
| `org.bouncycastle:bcprov-jdk18on:1.78` | Desktop | AES-256-GCM for `FieldEncryptor` + JVM KeyStore operations | `bouncycastle = "1.78"` |
| `kotlinx-datetime` | All | Session timeout | Already in project |
| ~~`net.zetetic:sqlcipher-android`~~ | — | **REMOVED** — SQLCipher has no `SQLiteDriver` for Room 3 KMP. Replaced by application-layer `FieldEncryptor`. | — |

---

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Not all DB data encrypted (field-level only) | Sensitive fields encrypted via FieldEncryptor. Non-sensitive cached data (UI state, lists) stays plaintext for query performance. Acceptable trade-off vs unavailable driver-level encryption. |
| Key loss = data re-fetch | `SecureKeyProvider.getKey()` returns null → app detects key loss, clears encrypted data, triggers re-authentication + server re-fetch. Keys are hardware-backed — loss only on factory reset/keystore clear. |
| Biometric false rejection | Always offer passcode fallback. Never biometric-only. |
| Pin rotation breaks users | Backup pins + 30-day overlap window |
| DB encrypt-on-write migration | No separate migration pass. TypeConverters read both plaintext and "ENC:"-prefixed data. New writes always encrypt. Crash-safe by design — no partially migrated state possible. |
| Settings split migration | Write-before-delete order: secure first → plain second → delete old LAST. Crash between writes → retry on next launch (old key still exists). Idempotent. |
| Clipboard wipe UX | Toast "Clipboard will clear in 60s" |
| Encrypted cache adds latency | AES encrypt/decrypt adds <1ms per response. Negligible. |
| Debug build less secure | Intentional — developers need full visibility. Release is hardened. |
| Token Mutex contention | Single-coroutine bottleneck on 401. Refresh is rare. |
| SecurityModule init failure | Fail-fast on startup. No fallback to unencrypted mode. |
| FieldEncryptor performance | AES-256-GCM encrypt/decrypt is ~microseconds per field. Platform hardware acceleration on all targets. Negligible overhead. |
