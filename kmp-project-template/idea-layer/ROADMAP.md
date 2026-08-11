# Roadmap — Money Toolkit (kmp-project-template)

> **SoT note:** Reverse-engineered fresh from shipped source at HEAD on 2026-08-01 via
> `/idea import`. Phases reflect the ACTUAL shipped state: P0 is the shipped core (12
> features with in-tree UI + the crypto markets list), P1 is the half-built crypto cluster
> + two shipped-code gaps (the natural first `/idea-agent` drive target), P2 is
> forward-looking enhancement.

---

## P0 — Shipped Core ✅ (reverse-engineered as complete)

The demo showcase already ships and runs on all 5 platforms. Twelve features are fully
implemented with UI in-tree, plus the crypto coin-markets list.

### App shell
| Feature | feature_id | Status |
|---------|-----------|:------:|
| F-001 Home Dashboard (4-way composite fan-in) | feat-home | ✅ shipped |
| F-002 App Settings (dark-mode / 41-locale / theme-brand / dynamic-color) | feat-settings | ✅ shipped |
| F-003 Profile (pure-static, no-account) | feat-profile | ✅ shipped |
| F-004 Component & Transition Gallery | feat-showcase | ✅ shipped (dev-only, fork-removable) |

### Banking / local (offline Room, zero network)
| Feature | feature_id | Status |
|---------|-----------|:------:|
| F-005 B1 Loan Tracker | feat-loans | ✅ shipped |
| F-006 B2 EMI Calculator | feat-emi-calculator | ✅ shipped |
| F-007 Loan Calculators (Affordability/Amort/Compare/Wizard) | feat-calculators | ✅ shipped |
| F-008 B5 Amortization Schedule | feat-amortization | ✅ shipped |
| F-009 B4 Bill Reminders | feat-bills | ✅ shipped (with UI gap → P1) |

### Economic / network (public APIs)
| Feature | feature_id | Status |
|---------|-----------|:------:|
| F-010 B7 Interest Rate Tracker (FRED) | feat-rates | ✅ shipped |
| F-011 Currency Rates (Frankfurter) | feat-currency-rates | ✅ shipped |
| F-012 B8 Country Macro Snapshot (World Bank) | feat-country-macro | ✅ shipped |

### Crypto (partial — see P1)
| Feature | feature_id | Status |
|---------|-----------|:------:|
| F-013 Crypto Coin Markets (list) | feat-crypto | ✅ list shipped (detail → P1) |

### Infrastructure (shipped, `/release`·`/ci`·`/secrets`-owned)
- 5-platform build + expect/actual · offline-first `core-base/store` DecisionEngine
- Store5 archetypes · Room 3 + wasmJs invalidation bridge · multiplatform-settings
- CI quality gate (Spotless/Detekt/DependencyGuard/Kover) · multi-platform release ladder
- Dual-mode secrets (manual / SOPS+age vault) · `core-base/security` · fork-syncability

---

## P1 — Complete the half-built Crypto cluster + close the two gaps

> **This is the natural first `/idea-agent` drive target.** Everything in P1 has its
> data layer, DI, and (where relevant) Room migration ALREADY shipped — P1 is about
> realizing the pending UI and fixing two shipped-code defects, not new architecture.

| # | Work item | Feature | Nature |
|:--:|-----------|---------|--------|
| P1-1 | **Crypto coin-detail UI** — build `CoinDetailScreen` + ViewModel + `CoinDetailRoute`; wire `onCoinClick` (today an intentional-noop). `CoinDetail` model, `CoinDetailStore` (5-min TTL), `coinDetailStream`, `CoinDetailDto`, `CoinDetailDao`, `coin_detail` table all already ship. | feat-crypto | UI realization |
| P1-2 | **Watchlist UI** — build `WatchlistScreen` + `WatchlistViewModel` + embedded `AddToWatchlistStar` + `AddToWatchlistViewModel`. Data layer (`WatchlistRepository`/`WatchlistDao`/`WatchlistEntity`), DI, and `AppDatabase` v5→v6 migration already ship (module is build-only). UI documented verbatim in repo/entity KDoc. | feat-watchlist | UI realization |
| P1-3 | **Alerts UI** — build `PriceAlertsListScreen` + `AddOrEditAlertScreen` + ViewModels against the shipped `AlertsStore`/repository/outbox. Module is build-only today. | feat-alerts | UI realization |
| P1-4 | **Fix the alerts persistence bug** — widen `AlertEntity` so it can store `enabled` (currently read-back hardcodes `true`) and encode `AlertDirection.PCT_CHANGE` (currently collapses to `BELOW`). A save→reload round-trip must round-trip both fields. | feat-alerts | Bug fix (schema widen) |
| P1-5 | **Surface bills delete / toggle-enabled** — wire `BillRemindersAction.Delete` and `.ToggleEnabled` (fully-tested ViewModel APIs) as row controls in `BillRemindersListScreen` (today only Paid + tap-to-edit are surfaced). | feat-bills | UI gap close |

**P1 exit criteria:** all 15 features reach ✅ shipped (feature + UI in-tree, on-device
verified), the alerts entity round-trips `enabled` + `PCT_CHANGE`, and bills expose
delete/toggle from the list — driving the crypto cluster from partial/ui-pending to
matrix-green.

---

## P2 — Enhancements (forward-looking)

> New capability beyond faithful completion of the shipped demo. Candidates surfaced by
> the per-feature docs as declared future extensions or natural next steps.

| Work item | Feature(s) | Notes |
|-----------|-----------|-------|
| Price-alert evaluation + notifications | feat-alerts | Today an "alert" is a stored threshold row that nothing fires on. Add a background evaluator (reuse bills' expect/actual notification scheduler) so alerts actually notify. |
| Bill per-row `lastPaidAtMs` history | feat-bills | Declared future extension — recurring bills currently derive next-due from `dueDay`, not stored paid-state. |
| Cross-device watchlist / loan / bill sync | feat-watchlist, feat-loans, feat-bills | The `SubmitHandler`/repository seams are already in place — a fork swaps the local write for a remote call with zero ViewModel change. |
| Resolve the amortization `@Ignore`'d test | feat-amortization | `computeSchedule_principalGrowsEachMonth` is flagged in source as an unresolved fixture-vs-math question; carried over, not fixed by import. |
| Add FRED series / countries / indicators via catalog lists | feat-rates, feat-country-macro | Extensible by one-list edits (`RateSeriesCatalog`, `SupportedCountries`, `IndicatorKind`) — no data-layer change. |
| Multi-base-currency FX (beyond hard-coded USD v1) | feat-currency-rates | Base currency is pinned "USD" at v1. |
| Fork-authoring polish | infrastructure | Deeper `customizer.sh` demo-strip validation, more sync-dirs coverage, additional release rungs. |

---

## Phase Summary

```
P0  ✅  12 features + crypto-markets list shipped + full infrastructure (reverse-engineered as complete)
P1  ⏳  Complete crypto cluster (crypto-detail, watchlist, alerts UI)
        + fix alerts persistence bug + surface bills delete/toggle
        →→ the first /idea-agent drive target →→ all 15 features matrix-green
P2  🔮  Alert notifications, bill paid-history, cross-device sync, catalog/currency extensions
```
