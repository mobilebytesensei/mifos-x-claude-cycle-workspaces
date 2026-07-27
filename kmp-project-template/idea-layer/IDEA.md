# Product Vision: Money Toolkit (kmp-project-template)

> **SoT note:** Reverse-engineered from shipped source on 2026-07-25 via `/idea import`.
> These foundation docs are a faithful read-only synthesis of 15 feature sibling-sets
> plus an infrastructure analysis — the running source is the ground truth, and the
> idea-layer mirrors it. No features are invented here; every entry traces to a shipped
> module (or a shipped data layer with a documented UI intent).

---

## Vision Statement

**Money Toolkit** is a white-label Kotlin Multiplatform finance-utility template — a
production-ready starting point that ships as a runnable demo showcase of 15 feature
modules and doubles as the **reference implementation of every `core-base/store`
persistence archetype**. It runs shared business logic and Compose Multiplatform UI
across **five targets — Android, iOS, macOS, Desktop (JVM), and Web (Kotlin/JS + WASM)** —
with **no login and no backend of its own** (the app consumes only public, mostly
keyless APIs).

## Problem

Two distinct audiences are underserved by existing KMP starters:

1. **Fork authors / teams** adopting Kotlin Multiplatform face weeks of boilerplate —
   CI/CD, testing, design system, navigation, DI, offline-first persistence, and
   platform-specific code — before they can build anything real. Generic "hello world"
   templates don't demonstrate the hard parts (offline caching, Store5 archetypes,
   expect/actual platform bridges, multi-platform release).
2. **End users of forks** want small, private, offline-first finance utilities
   (loan math, bill reminders, rate tracking, crypto watchlists) that work on any
   device without an account, a sign-in, or a server holding their data.

## Solution

A comprehensive, multi-module KMP template that:

- Ships **15 working feature modules** grouped into four domains (banking/local,
  economic/network, crypto, app-shell) — every one a live, on-device demo.
- Is a **living catalogue of the 8 `core-base/store` Store5 archetypes**
  (OFFLINE_LOCAL_ONLY, NETWORK_WITH_CACHE, NETWORK_ONLY, CACHE_ONLY, PERIODIC,
  MEMORY_ONLY, LOAD_ONCE, MUTABLE) — each feature is chosen to demonstrate one.
- Is **offline-first by default** — a shared `core-base/store` DecisionEngine drives
  loading/error/empty/content per screen with **zero per-screen state code**.
- Is **fork-and-brand ready** — `customizer.sh` renames namespaces and, **by default,
  REMOVES the entire demo showcase** (a fork opts back in with `--keep-demo`), leaving
  a clean, production-wired shell (nav, DI, design system, CI, release ladder) for the
  fork to fill.

## Target Users

| Audience | What they get |
|---|---|
| **Fork authors / KMP teams** | A production-wired 5-platform shell + a reference implementation of every store archetype, offline-first pattern, and release rung. Delete the demo, keep the machinery. |
| **End users of forks** | Small, private, offline-first finance utilities — loan tracking/math, bill reminders, interest-rate & FX & macro dashboards, crypto markets/watchlist/alerts — with no account and no server. |
| **OSS contributors (Mifos/openMF)** | A canonical, well-tested example codebase to learn Compose Multiplatform, MVI, Koin, Store5, and the multi-platform release pipeline from. |

## Value Propositions

1. **Offline-first, zero per-screen state code** — `core-base/store` DecisionEngine +
   Room + Store5 give every screen loading/error/empty/content/stale handling for free.
2. **Five platforms, one codebase** — Android, iOS, macOS, Desktop, Web via expect/actual;
   shared business logic + shared Compose UI.
3. **Fork-and-brand in minutes** — `customizer.sh` renames + strips the demo by default;
   a fork keeps the infrastructure and adds its own features.
4. **Reference-grade patterns** — real MVI (`BaseViewModel<S,E,A>`), Koin DI, Ktorfit/Ktor
   networking, all 8 store archetypes, offline draft outbox, and a full CI + multi-platform
   release ladder — not toy code.
5. **No account, no server, private by default** — the app itself has no backend; user data
   (loans, bills, watchlist, alerts) lives only on-device.

---

## Domain Context

The demo app is a **personal finance toolkit** organized into four domains. Each domain
was chosen to exercise a different persistence/networking archetype:

| Domain | Features | Persistence character |
|---|---|---|
| **App shell** | home (composite dashboard), settings, profile, showcase (dev-only) | Preferences + framework-owned nav shell |
| **Banking / local** | loans, emi-calculator, calculators, amortization, bills | Offline Room + pure-local math; zero network |
| **Economic / network** | rates (FRED), currency-rates (Frankfurter), macro (World Bank) | Network-with-cache / memory-only over public APIs |
| **Crypto** | crypto (CoinGecko), watchlist, alerts | Network paging + offline-local membership/threshold rows |

**External data sources** are all public and mostly keyless: FRED (US interest rates,
needs a free `FRED_API_KEY`), Frankfurter (FX, no key), World Bank Open Data (macro, no
key), CoinGecko (crypto markets, no key). Missing keys degrade gracefully to an in-app
"key not configured" state, never a crash.

---

## Technical Context

### Platform & Stack

| Component | Choice |
|---|---|
| Language | Kotlin 2.x |
| UI Framework | Compose Multiplatform (Material Design 3) |
| Architecture | MVI — `BaseViewModel<State, Event, Action>` (unidirectional) |
| DI | Koin |
| Navigation | Compose Navigation (type-safe `@Serializable` routes) |
| Networking | Ktorfit / Ktor — `Result<T, RemoteError>` |
| Offline / cache | `core-base/store` Store5 (8 archetypes) + Room 3 (`RoomChangeBus` wasmJs invalidation bridge) |
| Preferences | multiplatform-settings (plain + secure) |
| CI/CD | GitHub Actions + Fastlane; multi-platform release ladder (mifos-x-actionhub v2) |
| Platforms | Android, iOS, macOS, Desktop (JVM), Web (Kotlin/JS + WASM) |

### Store Archetype Showcase (the template's teaching spine)

| Archetype | Demonstrated by |
|---|---|
| OFFLINE_LOCAL_ONLY | loans, bills, amortization (read-projection), watchlist, alerts |
| NETWORK_WITH_CACHE | rates (FRED), currency-rates (list), crypto (paged) |
| NETWORK_ONLY / CACHE_ONLY | currency-rates spot converter (connectivity-routed) |
| PERIODIC | home USD-exchange tile (5-minute auto-refresh) |
| MEMORY_ONLY | macro (World Bank, no SourceOfTruth) |
| LOAD_ONCE | loan-detail (edits not clobbered by background writes) |
| MUTABLE / SubmitOutbox | loans/bills/alerts offline draft submit |
| none (pure-local) | emi-calculator, calculators, profile, showcase |

### Third-Party Services

| Service | Purpose | Key required | Status |
|---|---|:---:|:---:|
| FRED (St. Louis Fed) | US interest-rate series | ✅ free key | Integrated (graceful "not configured" state) |
| Frankfurter | FX rates + history | ❌ open | Integrated |
| World Bank Open Data | Country macro indicators | ❌ open | Integrated |
| CoinGecko | Crypto coin markets | ❌ public tier | Integrated |
| Firebase (Analytics/Crashlytics/App-Distribution) | Observability | opt-in | Koin-swappable, opt-in |
| GitHub Actions + Fastlane | CI/CD + multi-platform release | — | Integrated |

---

## Success Metrics

- **Fork setup < 5 minutes** via `customizer.sh` (rename + demo strip by default).
- **5 platform builds green** in CI (Android, iOS, macOS, Desktop, Web).
- **High code-sharing ratio** — business logic + Compose UI shared across all targets;
  platform code only behind expect/actual.
- **Zero per-screen state boilerplate** — DecisionEngine drives every screen's states.
- **Graceful degradation** — every network feature renders offline/stale/"key-missing"
  states, never a crash.

## Constraints

- Requires Kotlin 2.x with Compose Multiplatform; iOS/macOS need Xcode; Web WASM target.
- The app has **no backend** — no auth, no sync; user data is device-local only.
- FRED-backed features need a free developer key; all other external sources are keyless.

## Assumptions

- Forks use Koin (not Hilt/Dagger) and Compose Navigation (not Voyager).
- The **demo showcase is removed by default** — a production fork opts in with
  `--keep-demo` or deletes demo modules cleanly (only `cmp-navigation` references them,
  behind `demo:begin/demo:end` markers, gated on `!isReleaseBuild()`).
