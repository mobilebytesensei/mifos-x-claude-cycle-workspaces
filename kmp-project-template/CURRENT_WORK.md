# Current Work

**Last Updated**: 2026-09-06
**Active Project**: mifos-x/kmp-project-template
**Branches**: framework=`session-framework-20260902131157236` · workspace=`session-mifos-x-20260811121518547` · source=`session-kmp-project-template-20260904215046837`
**Source HEAD**: `bc6e7358` + UNCOMMITTED legacy-Supabase removal (6 paths)
**PR**: https://github.com/openMF/kmp-project-template/pull/300 (DRAFT, base `dev`)

---

## Session Resumption

- **Current task**: Legacy Supabase single-project path REMOVED and verified — uncommitted. Awaiting the user's call on `/git-session-commit --source`.
- **Next step**: Commit the removal, then ship PR #300 (`/git-session-merge --source`).
- **Resume command**: `/context-start mifos-x/kmp-project-template`
- **written_at**: 2026-09-06T09:20:00Z

### Nothing outstanding — the last residual is closed

The earlier doubt (which version of `SyncForkConfigPlugin.kt` the 8-minute run compiled) was settled
by re-running `./gradlew syncForkConfig` at `bc6e7358`: **BUILD SUCCESSFUL**, all codegen passes ran,
and `git status` was **empty afterwards** — regeneration is idempotent against what is committed, so
the generated files in the commit are exactly what today's generator produces.

---

## What this session built

**Goal (user's words):** *"automate the app.yaml:network using the codegen syncForkConfig, setup the
network client fully, setup the client in DI, and we only focus on writing the api interface for REST
and Supabase end to end."*

`app-profile/app.yaml#network.access_points` is now the sole declaration point for every endpoint.
`./gradlew syncForkConfig` projects that one list onto four surfaces, so adding an endpoint is
**declare it + write the API type** — there is no wiring step:

| Generated surface | Contents |
|---|---|
| `AppAccessPoints.points` | the registry list (pre-existing) |
| `AppUrlTypes` | one `UrlType` constant per endpoint — **newly generated** |
| `AppSupabaseAnonKeys` | one row per Supabase point, value via `BuildKonfig` — **newly generated** |
| `GeneratedApiBindings.kt` | the Koin binding per point declaring `api:` — **new file, fully generated** |

New per-entry `app.yaml` fields: `api:` (FQN of the API type — presence generates the binding) and
`anon_key_env:` (Supabase only — env/local.properties key, so no anon key is ever committed).

Factory conventions, both mechanical from the FQN:
- REST `a.b.XApi` → `restApi("id") { it.createXApi() }` (Ktorfit generates `create<Name>()`)
- Supabase `a.b.XApi` → `supabaseApi("id") { XApi(it) }` (single-arg ctor taking `SupabaseConfigClient`)

**Supabase is now genuinely end-to-end**, not just declared: added the `supabaseApi<T>("<id>")` DSL
(twin of `restApi`), `SupabaseClientFactory.requireClientFor` (throws naming every declared point
rather than injecting a null), and `AppConfigApi` — a reference Postgrest facade that stays safe on
an unconfigured fork (`client` is `by lazy`; calls return empty).

---

## Three real defects found and fixed (all were silent)

1. **`AppUrlTypes` had drifted** — 3 constants against 8 declared endpoints. No compile error:
   `AppMultiUrlConfigProvider.getBaseUrl` falls back to `UrlType.MAIN` for an unknown type, so a
   lookup for an undeclared endpoint returned MAIN's base URL instead of failing. Now generated.
2. **`AppSupabaseAnonKeys` cited a gate that did not exist** — its KDoc said "or NAP-7 will FAIL";
   `NAP-7` appeared nowhere else in the repo. The gate is now real.
3. **The two `fork.properties` writers stamped different headers** — `derive.rb` wrote
   `DERIVED from app-profile`, `syncForkConfig` wrote `GENERATED from app-profile/app.yaml`, and
   `white-label-derived.sh` greps for the former. So a `syncForkConfig`-written bridge read as
   *hand-authored* and the health verdict depended on which writer ran last. Headers now aligned.

Also caught during review, before it could ship: the generator sanitised the id into the constant's
**name** *and* its **key**, but `AccessPoint.type` is `UrlType(id.uppercase())` — unsanitised. A
hyphenated id like `pay-gw` would have declared `UrlType("PAY_GW")` against an access point carrying
`UrlType("PAY-GW")`, silently reintroducing defect #1. Only the identifier is sanitised now; NAP-3
checks the **key**, and canary cell `nap3-sanitized-key` pins it.

---

## New gate + canary

`scripts/product-health/checks/network-access-points.sh` — NAP-1…NAP-7. The generated files are
**committed** (a fresh clone must build without Gradle), so nothing otherwise forces them to still
match `app.yaml`; someone who edits app.yaml and forgets `syncForkConfig` gets a repo that compiles
and is wrong.

| Rule | Fails on |
|---|---|
| NAP-1 | endpoint declared in app.yaml but absent from `AppAccessPoints` (or vice versa) |
| NAP-2 | stale `kind` / `baseUrl` / `loggableHost` / `proxiedHost` for a declared id |
| NAP-3 | missing `UrlType` constant, **or one whose key ≠ `id.uppercase()`** |
| NAP-4 | `api:` declared with no generated binding, or a binding for an undeclared id |
| NAP-5 | Supabase point with no anon-key row |
| NAP-6 | an anon key committed as a string literal instead of a `BuildKonfig` read |
| NAP-7 | a hand-written `restApi(`/`supabaseApi(` outside the generated file |

Canary `scripts/product-health/tests/network-access-points-canary/` — 9 cells (1 GREEN + 8 RED),
each RED tree carrying exactly one defect. NAP-3 and NAP-6 are the cells that matter most: both
failure modes produce **no compile error at all**.

---

## Verification (all green at `bc6e7358`)

```
spotlessCheck + detekt + compile + :core:network:desktopTest   BUILD SUCCESSFUL (8m 8s)
canaries                                                       10 / 10
product-health (TEMPLATE_SELF_BUILD=1)                         16 passed · 1 warn · 0 failed
fork.properties header    "# gradle/fork.properties — DERIVED from app-profile by syncForkConfig. DO NOT EDIT."
```

The remaining 1 warn is pre-existing and unrelated: `deployment-whitelabel` B6, duplicate Android
metadata root (`deployment/fastlane/metadata/android/en-US` should be removed).

**Detekt was red before this session and is now green** — `source(files(rootDir))` means every
module's detekt task lints the whole repo, so it was linting the `fork-props-manifest-parity-canary`
fixtures added earlier this session. RED fixtures are deliberately malformed, so
`scripts/product-health/tests/**` is now excluded in `org/convention/Detekt.kt`. This may be what
was failing PR #300's checks.

---

## Files changed this session

| File | Why |
|---|---|
| `build-logic/.../SyncForkConfigPlugin.kt` | +3 codegen passes (`regenerateUrlTypes`, `regenerateSupabaseAnonKeys`, `regenerateApiBindings`) + `patchSentinel`/`accessPoints`/`isSupabase` helpers + header fix |
| `build-logic/.../org/convention/Detekt.kt` | exclude canary fixtures |
| `core-base/network/.../NetworkDsl.kt` | `supabaseApi<T>()` DSL |
| `core-base/network/.../SupabaseClientFactory.kt` | `requireClientFor()` |
| `core/network/.../config/AppUrlTypes.kt` | sentinel block, now generated |
| `core/network/.../config/AppSupabaseAnonKeys.kt` | generated rows; phantom-gate KDoc corrected |
| `core/network/.../demo/di/ProjectNetworkModule.kt` | hand-wired `restApi` lines → `includes(GeneratedApiBindings)` |
| `core/network/.../demo/di/GeneratedApiBindings.kt` | **new, generated** |
| `core/network/.../demo/appconfig/{api,dto}/` | **new** — `AppConfigApi` + `RemoteAppConfigDto` |
| `core/network/src/commonTest/.../SupabaseAccessPointTest.kt` | **new** — 5 tests, incl. inert-safety |
| `app-profile/app.yaml` | `api:` on 6 points, `anon_key_env:` documented, field docs |
| `customization-surface.yaml` | `GeneratedApiBindings.kt` carved out of `**/demo/**` |
| `CLAUDE.md` | Network section rewritten |
| `scripts/product-health/checks/network-access-points.sh` | **new gate** |
| `scripts/product-health/tests/network-access-points-canary/` | **new, 9 cells** |

---

## Working agreements learned this session

- **Never run `./gradlew` iteratively.** A PreToolUse hook redirects it to the `context-mode` MCP
  plugin; each call takes minutes and often backgrounds. Author everything first, then **one**
  build+verify at the end. User: *"this is running very frequently … it is wasting a lot of time."*
  Pure-bash gates (`product-health.sh`, `self-test-canaries.sh`, `checks/*.sh`) do NOT trip the hook —
  run those freely. Reason about likely compile/lint failures from neighbouring code instead of
  trial-compiling (e.g. `javap` the dependency jar to confirm a member vs. an extension).
- The plugin is disabled in `.claude/settings.local.json` but still enabled in `.claude/settings.json`,
  and hooks persist until the CLI restarts — it cannot be turned off mid-session.
- Canary fixtures carry **no `package` declaration** (existing repo convention) — a package makes
  detekt's `InvalidPackageDeclaration` fire on the fixture path.
- `:core-base:network` has **no** `spotlessApply` task; format via root `spotlessCheck`.

---

## Legacy Supabase path REMOVED (2026-09-06) — verified, uncommitted

Superseded by the registry-driven path. Nothing referenced the generated object, and the plugin could
only ever express ONE Supabase project, which the access-point registry made obsolete.

Removed (6 paths):
- `build-logic/.../SupabaseConfigConventionPlugin.kt` — **deleted** (184 lines)
- its `register("supabaseConfig")` block in `build-logic/convention/build.gradle.kts`
- the `kmp-supabase-config` alias in `gradle/libs.versions.toml`
- `alias(libs.plugins.kmp.supabase.config)` + the `supabaseConfig { }` block in `core/network/build.gradle.kts`
- `NetworkModule`: the `single<SupabaseCredentials> { … }` and unnamed `single { SupabaseConfigClient(…) }`
  bindings (both had zero consumers) + the now-unused import
- `core-base/.../SupabaseConfigClient.kt`: KDoc that still told readers to use the deleted generator

`NetworkModule` now exposes exactly one Supabase surface: `Map<String, SupabaseConfigClient>` keyed by
access-point id. The `SupabaseCredentials` INTERFACE in core-base stays — `SupabaseClientFactory`
implements it anonymously per point.

### End-to-end proof of "declare + write the interface, nothing else"

Ran live, then reverted. Added ONE endpoint to app.yaml and ONE Ktorfit interface (`ProbeApi`); a
deliberately **hyphenated** id (`demo-probe`) so the UrlType key-vs-identifier fix was exercised too.
`syncForkConfig` then wrote, with no further input:

```
+ AccessPoint(id = "demo-probe", kind = AccessPointKind.REST, baseUrl = …, loggableHost = …)
+ val DEMO_PROBE: UrlType = UrlType("DEMO-PROBE")      <- identifier sanitized, KEY is not
+ DEMO_PROBE,                                           (added to AppUrlTypes.all)
+ import kpt.core.network.demo.probe.api.createProbeApi
+ restApi("demo-probe") { it.createProbeApi() }
```

`:core:network:compileKotlinDesktop` BUILD SUCCESSFUL (KSP produced `createProbeApi`, so the generated
binding resolves) · NAP gate green at 9 declared / 7 bound · revert left the tree clean.

### Verification after removal

```
syncForkConfig                                          BUILD SUCCESSFUL (idempotent, clean tree)
spotlessCheck + detekt + compile + desktopTest          BUILD SUCCESSFUL (4m 24s)
canaries                                                10 / 10
product-health                                          16 passed · 1 warn · 0 failed
```

---

## Blockers

| # | Blocker | Impact | Resolution |
|---|---------|--------|------------|
| - | None | - | - |

---

## Session History

| Date | Focus | Outcome |
|------|-------|---------|
| 2026-09-06 | app.yaml `network:` → syncForkConfig codegen; REST + Supabase DI generated end-to-end | Shipped. 3 silent defects fixed, NAP-1…NAP-7 gate + 9-cell canary added. All green, committed `bc6e7358`, PR #300 synced. |
| 2026-09-05 | `fork.properties` single SoT — one reader per language, two-writer manifest parity | Shipped: `ForkProperties.kt`, `scripts/_shared/fork-props.sh`, `fork-props-{single-reader,manifest-parity}.sh` + canaries |
| 2026-09-04 | Store5 single read path; ViewModel tests; `@Preview`; locale coverage | 13 tests, 30 previews, 369 `strings.xml`, logout-purge privacy bug fixed |
