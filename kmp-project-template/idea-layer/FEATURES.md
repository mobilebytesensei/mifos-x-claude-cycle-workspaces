# Features — Money Toolkit (kmp-project-template)

> **SoT note:** Reverse-engineered fresh from shipped source at HEAD on 2026-08-01 via
> `/idea import`. 15 feature modules across 4 domains. Status legend: **shipped** (feature
> + UI in-tree), **partial** (some screens shipped, others data-wired/UI-pending),
> **ui-pending** (data layer + DI shipped, ViewModels/screens not yet in-tree). The demo
> showcase is **removed by default** by `customizer.sh` (a fork opts in with `--keep-demo`).
> `core/auth` was removed — there is deliberately **no auth feature**.

---

## Feature Registry

| ID | Name | feature_id | Domain | Priority | Phase | Store archetype | Status |
|:--:|------|-----------|--------|:--:|:--:|-----------------|:------:|
| F-001 | Money Toolkit Home Dashboard | feat-home | App shell | P0 | Shipped | composite (2 Room + 2 Store5, PERIODIC) | ✅ shipped |
| F-002 | App Settings | feat-settings | App shell | P0 | Shipped | preferences (multiplatform-settings) | ✅ shipped |
| F-003 | Profile | feat-profile | App shell | P0 | Shipped | none (pure-static) | ✅ shipped |
| F-004 | Component & Transition Gallery | feat-showcase | App shell | P0 | Shipped | none (dev-only) | ✅ shipped (dev-only) |
| F-005 | B1 Loan Tracker | feat-loans | Banking/local | P0 | Shipped | OFFLINE_LOCAL_ONLY (+LOAD_ONCE, MUTABLE) | ✅ shipped |
| F-006 | B2 EMI Calculator | feat-emi-calculator | Banking/local | P0 | Shipped | none (pure-local) | ✅ shipped |
| F-007 | Loan Calculators (Affordability/Amort/Compare/Wizard) | feat-calculators | Banking/local | P0 | Shipped | none (+ local Room read/write) | ✅ shipped |
| F-008 | B5 Amortization Schedule | feat-amortization | Banking/local | P0 | Shipped | OFFLINE_LOCAL_ONLY (read-projection) | ✅ shipped |
| F-009 | B4 Bill Reminders | feat-bills | Banking/local | P0 | Shipped | OFFLINE_LOCAL_ONLY + notifications | ✅ shipped ⚠ gap |
| F-010 | B7 Interest Rate Tracker | feat-rates | Economic/network | P0 | Shipped | NETWORK_WITH_CACHE (FRED, needs key) | ✅ shipped |
| F-011 | Currency Rates | feat-currency-rates | Economic/network | P0 | Shipped | NETWORK_WITH_CACHE / NETWORK_ONLY / CACHE_ONLY | ✅ shipped |
| F-012 | B8 Country Macro Snapshot | feat-country-macro | Economic/network | P0 | Shipped | MEMORY_ONLY (World Bank) | ✅ shipped |
| F-013 | Crypto Coin Markets | feat-crypto | Crypto | P0/P1 | Shipped + P1 | NETWORK_WITH_CACHE (CoinGecko, paged) | ⚠ partial (detail UI-pending) |
| F-014 | Personal Crypto Watchlist | feat-watchlist | Crypto | P1 | P1 | OFFLINE_LOCAL_ONLY + crypto network | ⏳ ui-pending |
| F-015 | Price Alerts | feat-alerts | Crypto | P1 | P1 | OFFLINE_LOCAL_ONLY | ⏳ ui-pending ⚠ bug |

**UI-pending / gap items (the P1 drive target):**
- **F-013 crypto-detail** — `CoinDetail` model, store, repo stream, DTO, DAO, Room table all wired; `CoinDetailScreen` UI NOT shipped; `onCoinClick` is an intentional-noop (confirmed in `CryptoNavigation.kt`).
- **F-014 watchlist** — data layer (`WatchlistEntity`/`WatchlistDao`/`WatchlistRepository`) + DI + `AppDatabase` v5→v6 migration shipped in `core/`; `WatchlistScreen`/`AddToWatchlistStar` ViewModels+screens NOT in-tree (`feature/watchlist/` is build-only).
- **F-015 alerts** — data layer (model/entity/dao/repo/store/DI/outbox/tests) shipped in `core/`; `PriceAlertsListScreen`/`AddOrEditAlertScreen` NOT in-tree (`feature/alerts/` is build-only).
- **F-015 alerts persistence bug** — `AlertEntity` cannot represent `PCT_CHANGE` (collapses to `BELOW`) nor a `disabled` flag (read-back hardcodes `true`); a save→reload round-trip silently degrades. A faithful impl must widen the entity.
- **F-009 bills gap** — `Delete` and `ToggleEnabled` exist as fully-tested ViewModel APIs but are NOT surfaced as row controls in the shipped list UI (only Paid + tap-to-edit are wired).

---

## Domain 1 — App shell

### F-001 · Money Toolkit Home Dashboard (`feat-home`) — ✅ shipped
- **One-liner:** The main landing tab — a composite dashboard fanning 4 independent reactive sources (local loans, upcoming bills, FRED rates, self-refreshing USD exchange) into one screen, plus an 8-tile Tools grid; every card loads/errors/retries independently.
- **Screens:** `HomeScreen` (wraps `HomeDashboard`, `HomeViewModel`) — states loading/content/empty/error per card.
- **Store archetype:** COMPOSITE — 2 local Room Flows (loans, bills) + 2 Store5 NETWORK_WITH_CACHE streams (rates via FRED, exchange via Frankfurter PERIODIC 5-min); `combineScreenStates` fuses the FRED series into one "Today's Rates" card.
- **Notable:** Needs `FRED_API_KEY` for the rates card only (unset → Error slot, not crash). `HomeScreen` Scaffold shell is framework-owned and survives `customizer --clean`; the `HomeDashboard` demo body is stripped.
- **Dependencies:** navigates outbound into loans, bills, rates, currency, emi-calculator, calculators (affordability/amortization/comparison/wizard), macro, and Settings.

### F-002 · App Settings (`feat-settings`) — ✅ shipped
- **One-liner:** On-device appearance + language settings (dark-mode, 41-locale language, and on Android theme-brand + Material You dynamic color); a companion Notification screen is a static placeholder.
- **Screens:** `SettingsScreen` (pure-UI host, no ViewModel) + `SettingsDialog`/`LanguageDialog`/`DevMenuDialog`; `NotificationScreen` (static empty).
- **Store archetype:** preferences — multiplatform-settings (plain `user_data_key` + secure `secure_data_key`); NOT Store5, NOT Room.
- **Dependencies:** leaf; drives `MifosTheme` (dark mode + dynamic color) and app localization app-wide.

### F-003 · Profile (`feat-profile`) — ✅ shipped
- **One-liner:** The Profile bottom-nav tab — a pure-static informational surface explaining the app runs fully on-device with no login/account; a single explanatory hero card.
- **Screens:** `ProfileScreen` (stateless `@Composable`, no ViewModel, takes only a Modifier).
- **Store archetype:** none. The minimal end of the archetype spectrum.
- **Dependencies:** leaf root-nav tab.

### F-004 · Component & Transition Gallery (`feat-showcase`) — ✅ shipped (DEV-ONLY)
- **One-liner:** A developer reference gallery rendering every `ScreenState` variant + component-scale state primitives, and all 9 navigation `TransitionVariant` factories running on-device.
- **Screens:** `StateGalleryScreen` + `TransitionGalleryScreen` (both stateless, no ViewModel).
- **Store archetype:** none.
- **Notable:** DEV-ONLY — entry points computed as `if (!isReleaseBuild())`; module + its two nav graphs + `include(":feature:showcase")` are cleanly fork-removable (only `cmp-navigation` references it, behind `demo:begin/demo:end`).

---

## Domain 2 — Banking / local (all offline Room, zero network)

### F-005 · B1 Loan Tracker (`feat-loans`) — ✅ shipped
- **One-liner:** Track personal loans locally (principal, EMI, rate, tenure, next due-date) with a summary tile, detail drill-down, and an offline-resilient add/edit/delete form.
- **Screens:** `PersonalLoansListScreen` (list) · `LoanDetailScreen` (detail) · `AddOrEditLoanScreen` (form, per-loan concurrent drafts).
- **Store archetype:** OFFLINE_LOCAL_ONLY (`LoansStore`, key=Unit → `List<LoanEntity>`) + LOAD_ONCE (detail) + multi-formKey `BaseDraftMutationViewModel` (concurrent offline drafts).
- **Data:** `Loan` / `banking_loans` table. No auth, no backend, no remote sync.
- **Notable:** Detail's "Schedule" button navigates to F-008 (amortization); loan reminder scheduling consumed cross-module via `WorkScheduler`.

### F-006 · B2 EMI Calculator (`feat-emi-calculator`) — ✅ shipped
- **One-liner:** A pure-local calculator computing monthly EMI, total payment, and total interest from principal/rate/tenure — instant, offline, no login, updates live.
- **Screens:** single EMI calculator screen (`BaseViewModel<State, Nothing, Action>`, transient UI state).
- **Store archetype:** none (pure-local) — the canonical "no Store" reference; pure-Kotlin `calculateEmi`.
- **Dependencies:** leaf; entered from home Tools hub.

### F-007 · Loan Calculators (`feat-calculators`) — ✅ shipped
- **One-liner:** A four-screen on-device loan-math toolkit: B3 Affordability (max borrowable), Amortization (full schedule), B6 Comparison (3 side-by-side, cheapest wins), and a 5-step Save-Loan Wizard.
- **Screens:** `AffordabilityCalculatorScreen` (graph start) · `AmortizationScreen` · `LoanComparisonScreen` · `LoanCalcWizardScreen` (5-step DraftSubmit state machine).
- **Store archetype:** none (pure-local) — plus a read-side projection of `LoanRepository` (amortization pre-fill) and a local Room write (wizard upserts a `Loan`) + `SubmitOutbox<LoanCalcScenario>` for resume-anywhere.
- **Dependencies:** `feat-loans` (shared `banking_loans` / `LoanRepository` / `Loan` — amortization reads, wizard writes). Distinct from F-006 (single-screen); same EMI math, richer archetypes, no duplicated screens.

### F-008 · B5 Amortization Schedule (`feat-amortization`) — ✅ shipped
- **One-liner:** The full month-by-month payment breakdown for one tracked loan — principal/interest/remaining balance per month + a summary total; a read-only terminal leaf reached from loan-detail.
- **Screens:** `AmortizationScheduleScreen` (`AmortizationScheduleViewModel`, `BaseViewModel<Unit, Nothing, Nothing>`) — states loading/content/empty.
- **Store archetype:** OFFLINE_LOCAL_ONLY read-projection — `observeById(loanId).map{computeSchedule}.stateIn(WhileSubscribed)`; owns no table (reuses `feat-loans` `LoansStore`); schedule recomputed on every emission, never persisted.
- **Notable:** READ-ONLY — no writes, no forward nav, only Back is interactive; Empty triggers on `loan == null` OR `monthsRemaining <= 0`. Carries a pre-existing `@Ignore`'d test (`computeSchedule_principalGrowsEachMonth`) flagged in source, not fixed by this import.

### F-009 · B4 Bill Reminders (`feat-bills`) — ✅ shipped ⚠ gap
- **One-liner:** Track recurring/one-time bills locally (name, amount, due-day, recurrence, category, reminder lead-time) with an "upcoming this month" tile, an offline-resilient form, and a best-effort per-platform OS notification.
- **Screens:** `BillRemindersListScreen` (list) · `AddOrEditBillReminderScreen` (form; a row short-tap opens edit directly — no separate detail screen).
- **Store archetype:** OFFLINE_LOCAL_ONLY (`BillRemindersStore`, key=Unit) + platform notification scheduling via expect/actual `BillReminderScheduler` behind a mockable `BillNotificationGateway` seam (WorkManager on Android, UNUserNotificationCenter on iOS, no-op stubs on Desktop/JS/WasmJS).
- **Data:** `BillReminder` / `banking_bill_reminders` table.
- **⚠ Gap:** `BillRemindersAction.Delete` and `.ToggleEnabled` are fully-tested ViewModel APIs but NOT surfaced as row controls in the shipped UI (only Paid + tap-to-edit wired) → **P1 surface-the-controls target.**

---

## Domain 3 — Economic / network (public APIs, graceful degradation)

### F-010 · B7 Interest Rate Tracker (`feat-rates`) — ✅ shipped
- **One-liner:** A live dashboard of 4 independent US interest-rate series (Fed Funds, Prime, 30Y Mortgage, 10Y Treasury) from FRED — each an independently-loading card with a 365-day sparkline + 1-day delta, plus a per-series drill-down.
- **Screens:** rates list (4 independent `ScreenState` slots) + per-series detail (area chart + observation table).
- **Store archetype:** NETWORK_WITH_CACHE (`InterestRateSeriesStore`, 24h TTL, Room SOT `interest_rate_series`); the "independent cards" pattern (one failed series never blanks the screen) + framework `FreshnessIndicator` (worst-of-4).
- **Data source:** FRED `fred/series/observations` — **needs a free `FRED_API_KEY`** (local.properties Path A or `mifos_x_fred_api_key` vault Path B); unset → "FRED_API_KEY is not configured" Error slot, not a crash.

### F-011 · Currency Rates (`feat-currency-rates`) — ✅ shipped
- **One-liner:** Live FX rates by base currency (USD at v1) from Frankfurter with a case-insensitive search filter + no-match Empty state, an embedded spot-converter facet, and a sibling rate-history chart.
- **Screens:** currency-rates list (search + `emptyIfContent`) · embedded spot-converter facet · rate-history (currency chips [INR,EUR,GBP,JPY,AUD] × period chips [7,14,30,90]).
- **Store archetype:** NETWORK_WITH_CACHE (list, Room SOT `exchange_rates`) · NETWORK_ONLY/CACHE_ONLY (spot converter, connectivity-routed) · dynamic-key NETWORK_WITH_CACHE (rate-history, Room SOT `rate_history`).
- **Data source:** Frankfurter `api.frankfurter.dev` — **no key required** (fully open).

### F-012 · B8 Country Macro Snapshot (`feat-country-macro`) — ✅ shipped
- **One-liner:** A per-country dashboard of 3 macro indicators (GDP, Inflation/CPI, Unemployment) from World Bank Open Data — independently-loading cards with trend sparkline + latest-year headline, a searchable country picker, and a per-indicator 25-year drill-down.
- **Screens:** macro dashboard (3 independent cards) + pure-UI searchable country picker + per-indicator detail.
- **Store archetype:** MEMORY_ONLY (`MacroIndicatorStore`, `createMemoryStore`, NO SourceOfTruth, 7-day TTL, in-memory only — cold start re-fetches; deliberate since World Bank data is public/cheap/annual).
- **Data source:** World Bank Open Data — **no key, no auth** (fully open).

---

## Domain 4 — Crypto (the half-built cluster — P1 completion target)

### F-013 · Crypto Coin Markets (`feat-crypto`) — ⚠ partial
- **One-liner:** An infinite-scroll list of top cryptocurrencies by market cap from CoinGecko — each row shows symbol, name, USD price, and up/down-coloured 24h change; scroll position + pages restored across tab-switch/rotation/process-death.
- **Screens:** `CoinMarketsScreen` (SHIPPED, paging list) · `CoinDetailScreen` (**UI-PENDING**).
- **Store archetype:** NETWORK_WITH_CACHE, page-keyed, 2-min TTL, Room SOT `coin_markets`; the canonical PAGING-LIST showcase (`PagingScreenContent` owns list + load-more + footer).
- **Data source:** CoinGecko `/coins/markets` — **no key** (public tier; 429 on rate-limit → stale cache/retry).
- **⏳ P1 gap:** coin-detail is FULLY data-wired at HEAD (`CoinDetail` model, `CoinDetailStore` 5-min TTL, `coinDetailStream`, `CoinDetailDto`, `CoinDetailDao`, `coin_detail` table) but `CoinDetailScreen` UI is NOT shipped; `onCoinClick` → intentional-noop (a tap does nothing today).

### F-014 · Personal Crypto Watchlist (`feat-watchlist`) — ⏳ ui-pending
- **One-liner:** A private, device-local list of starred coins — membership (coinIds only) persisted locally via a raw Room DAO + invalidation bridge (NO Store5, NO sync); live values resolved on-demand by joining tracked coinIds against `feat-crypto`'s Store5 streams.
- **Screens (proposed from documented UI intent):** `WatchlistScreen` (`WatchlistViewModel`) · embedded `AddToWatchlistStar` (`AddToWatchlistViewModel`) — both status: pending.
- **Store archetype:** OFFLINE_LOCAL_ONLY via raw `WatchlistDao` + `daoFlow{}/notifyingWrite{}` invalidation bridge (the wasmJs Room-3-alpha05 workaround) + local-membership × network-value BLEND. Add/remove is the framework `SubmitHandler` "input simple" seam.
- **Data:** `WatchlistEntity` / `personal_watchlist` table (`coinId` PK + `addedAtMs`); `AppDatabase` v5→v6 migration ships.
- **⏳ P1 gap:** at HEAD `feature/watchlist/` contains only a `build/` dir — data layer + DI + migration shipped; UI documented verbatim in repo/entity KDoc but not in-tree → **P1 realize-the-UI target.**

### F-015 · Price Alerts (`feat-alerts`) — ⏳ ui-pending ⚠ bug
- **One-liner:** Configure price-threshold alerts for crypto coins ("notify me when <coin> goes ABOVE/BELOW <target>", or a 24h percent-change) — a list + an offline-resilient add/edit form + delete. Despite the name, NO notification is scheduled (an "alert" is a stored threshold row).
- **Screens (proposed from data contract):** `PriceAlertsListScreen` (`PriceAlertsListViewModel`) · `AddOrEditAlertScreen` (`EditAlertViewModel`) — both provenance: proposed.
- **Store archetype:** OFFLINE_LOCAL_ONLY (`AlertsStore`, `createOfflineStore`, key=Unit, no remote fetcher) + multi-formKey `DraftSubmitHandler` + `OfflineSubmitSyncer` (formKey="price_alert").
- **Data:** `PriceAlert` model (id, coinId, `AlertDirection` ABOVE|BELOW|PCT_CHANGE, targetValue, enabled, createdAtMs) → `AlertEntity` / `alerts` table.
- **⏳ P1 gap:** `feature/alerts/` is build-only — data layer (model/entity/dao/repo/store/DI/outbox/tests) ships; the two screens are modeled from the contract, not in-tree → **P1 realize-the-UI target.**
- **⚠ Persistence bug:** `AlertEntity` drops two model fields — `enabled` is never stored (read-back hardcodes `true`), and `PCT_CHANGE` has no entity encoding (collapses to `BELOW` via `conditionAbove=false`). A save→reload silently loses a disabled flag and degrades a %-change alert → **P1 widen-the-entity fix.**

---

## Feature Dependency Map

```
App shell:
  home ──navigates──▶ loans, bills, rates, currency-rates, macro,
                      emi-calculator, calculators(affordability/amortization/
                      comparison/wizard), settings
  settings ──drives──▶ MifosTheme (dark mode, dynamic color) + app localization
  profile, showcase ─ leaf tabs (showcase dev-only, fork-removable)

Banking (shared banking_loans domain):
  loans ◀──reads/writes── calculators (amortization pre-fill, wizard upsert)
  loans ──"Schedule"──▶ amortization (read-projection of LoansStore)
  emi-calculator ─ leaf (shares EMI math, no shared data)
  bills ─ leaf (own banking_bill_reminders table + platform notifications)

Crypto (shared CoinGecko domain):
  crypto (CoinMarkets) ──provides live values──▶ watchlist (coinId join)
  crypto ──▶ coinDetail (data-wired, UI-pending)
  watchlist, alerts ─ offline-local rows over crypto's coin universe
```
