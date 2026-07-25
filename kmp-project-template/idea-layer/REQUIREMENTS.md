# Requirements — Money Toolkit (kmp-project-template)

> **SoT note:** Reverse-engineered from shipped source on 2026-07-25 via `/idea import`.
> FR = user-visible functional behavior, NFR = per-feature non-functional
> (perf/offline/a11y), DR = per-feature data (tables/DTOs/external APIs). The final
> **Infrastructure / Non-Functional** section folds the infra analysis — those rows are
> **driven by `/release` · `/ci` · `/secrets`** and **tracked-not-generated** by `/idea-agent`.

---

## Functional Requirements (FR)

### App shell

| ID | Description | Feature | Status |
|:--:|-------------|---------|:------:|
| FR-001 | User sees a single landing dashboard with loans owed, bills due this week, today's rates, and a live USD exchange tile | feat-home | ✅ |
| FR-002 | Each home card loads, errors, and retries independently — one flaky source never blanks the screen | feat-home | ✅ |
| FR-003 | The home USD-exchange tile self-refreshes on a 5-minute cadence without user pull | feat-home | ✅ |
| FR-004 | An 8-tile Tools grid jumps into loan calculators, rate history, and macro indicators | feat-home | ✅ |
| FR-005 | User switches dark-mode preference (System/Light/Dark) app-wide | feat-settings | ✅ |
| FR-006 | User changes app language from a 41-entry locale list | feat-settings | ✅ |
| FR-007 | Android user selects a theme brand (Default/Android) and toggles Material You dynamic color | feat-settings | ✅ |
| FR-008 | Appearance + language choices persist across restarts with no account | feat-settings | ✅ |
| FR-009 | User sees a Profile tab explaining the app runs on-device with no login | feat-profile | ✅ |
| FR-010 | (dev-only) Engineer views every ScreenState variant + all 9 nav transitions on-device | feat-showcase | ✅ (dev) |

### Banking / local

| ID | Description | Feature | Status |
|:--:|-------------|---------|:------:|
| FR-011 | User sees all loans with outstanding balance, monthly EMI, and active count | feat-loans | ✅ |
| FR-012 | User adds/edits/deletes a loan and sees computed EMI + total interest before saving | feat-loans | ✅ |
| FR-013 | Loan edits survive being offline — nothing lost across concurrent offline drafts | feat-loans | ✅ |
| FR-014 | User computes monthly EMI, total payment, and total interest live from principal/rate/tenure | feat-emi-calculator | ✅ |
| FR-015 | User computes the maximum affordable loan from income, DTI, and existing obligations | feat-calculators | ✅ |
| FR-016 | User compares 3 loan scenarios side-by-side; the cheapest by total payable is badged | feat-calculators | ✅ |
| FR-017 | A guided 5-step wizard saves a scenario as a tracked loan and resumes after interruption | feat-calculators | ✅ |
| FR-018 | User sees the full month-by-month amortization schedule (principal/interest/balance) for a loan | feat-amortization | ✅ |
| FR-019 | A fully-paid or unknown loan shows a "nothing to amortize" empty state, not an empty table | feat-amortization | ✅ |
| FR-020 | User sees all bills with amount, due-soon urgency, and an "upcoming this month" summary | feat-bills | ✅ |
| FR-021 | User adds a bill with recurrence (monthly/quarterly/annually/one-time), category, and reminder lead-time | feat-bills | ✅ |
| FR-022 | User marks a bill paid | feat-bills | ✅ |
| FR-023 | A best-effort OS notification fires `reminderDaysBefore` days before a bill's due-date (per-platform) | feat-bills | ✅ |
| FR-024 | User deletes a bill or disables its reminder without deleting it, from the list row | feat-bills | ⚠ VM API tested, **NOT surfaced as UI controls** (P1) |

### Economic / network

| ID | Description | Feature | Status |
|:--:|-------------|---------|:------:|
| FR-025 | User sees today's Fed Funds, Prime, 30Y Mortgage, and 10Y Treasury rates, each with a sparkline + 1-day delta | feat-rates | ✅ |
| FR-026 | User taps a rate to see its 365-day chart + full observation history | feat-rates | ✅ |
| FR-027 | Offline, the user still sees the last-synced rates marked stale | feat-rates | ✅ |
| FR-028 | With no FRED key configured, each rate row shows "FRED_API_KEY is not configured" (not a crash) | feat-rates | ✅ |
| FR-029 | User sees today's FX rates for a base currency and searches the list by currency code | feat-currency-rates | ✅ |
| FR-030 | User gets a spot conversion that stays fresh online and doesn't error offline (connectivity-routed) | feat-currency-rates | ✅ |
| FR-031 | User charts a currency pair's history over a selectable period (7/14/30/90 days) | feat-currency-rates | ✅ |
| FR-032 | User sees a country's GDP, inflation, and unemployment with trend sparklines + latest year | feat-country-macro | ✅ |
| FR-033 | User switches countries via a searchable picker and drills into a 25-year indicator history | feat-country-macro | ✅ |
| FR-034 | One failed indicator does not blank the macro screen; each card retries on its own | feat-country-macro | ✅ |

### Crypto

| ID | Description | Feature | Status |
|:--:|-------------|---------|:------:|
| FR-035 | User scrolls an infinite list of top cryptocurrencies with price + up/down-coloured 24h change | feat-crypto | ✅ |
| FR-036 | Scroll position + loaded pages are restored across tab-switch, rotation, and process-death | feat-crypto | ✅ |
| FR-037 | User taps a coin to see its detail screen | feat-crypto | ⏳ data-wired, **UI-pending** (P1); tap is a no-op today |
| FR-038 | User stars/un-stars coins into a private device-local watchlist showing live price + 24h change | feat-watchlist | ⏳ **UI-pending** (P1) |
| FR-039 | Watchlist membership stays private on-device (coinIds only; values always live) with no account/sync | feat-watchlist | ⏳ data shipped, UI-pending (P1) |
| FR-040 | User configures a price-threshold alert (ABOVE/BELOW/PCT_CHANGE at a target) for a coin | feat-alerts | ⏳ **UI-pending** (P1) |
| FR-041 | User sees all configured alerts newest-first, edits a target, toggles on/off, and deletes | feat-alerts | ⏳ UI-pending + **persistence bug** (P1) |

---

## Non-Functional Requirements (NFR) — per feature

| ID | Description | Feature |
|:--:|-------------|---------|
| NFR-001 | Composite dashboard: per-card independent loading/error/retry + worst-of-2 FreshnessIndicator; VM survives bottom-nav tab switches (retainedKoinViewModel) | feat-home |
| NFR-002 | Preference change reflected app-wide within one frame (optimistic StateFlow re-emit) and survives restart | feat-settings |
| NFR-003 | Profile renders instantly, fully static, zero async/network | feat-profile |
| NFR-004 | Showcase gated to `!isReleaseBuild()`, zero presence in release builds, cleanly deletable | feat-showcase |
| NFR-005 | Loan/bill offline draft recovery: edits auto-saved and committed on reconnect (no loss) | feat-loans, feat-bills |
| NFR-006 | EMI/affordability/comparison/schedule: time-to-first-result < 1s, synchronous on-device, zero crashes on non-numeric input | feat-emi-calculator, feat-calculators |
| NFR-007 | Amortization is read-only (only Back interactive); no error state ever emitted (local read + math can't fail) | feat-amortization |
| NFR-008 | Bill notifications are best-effort + OS-permission-gated; scheduler mockable in tests via BillNotificationGateway seam | feat-bills |
| NFR-009 | FRED usage stays under 120 calls/min via 24h Store5 TTL; graceful offline stale + key-missing states | feat-rates |
| NFR-010 | FX + macro degrade gracefully offline (stale band / NoNetwork with retry); wasmJs glyph-safe icons (ArrowForward, ISO-code badge, em-dash sparkline fallback) | feat-currency-rates, feat-country-macro |
| NFR-011 | Crypto paging stays under CoinGecko demo rate limit via 2-min TTL; locale-free formatters safe on JS/wasmJs | feat-crypto |
| NFR-012 | i18n: all user-facing copy via compose-resources string keys (RULE-IMPL-NO-HARDCODED-STRING-001); localized in de/es/fr/hi/ja/zh-rCN | all UI features |
| NFR-013 | Accessibility: every Icon/Image has contentDescription (or null if decorative); numeric keyboards per field; radio rows use Role.RadioButton | all UI features |
| NFR-014 | All pure-local features work identically on 5 platforms — pure commonMain, no expect/actual | feat-emi-calculator, feat-calculators, feat-profile |

---

## Data Requirements (DR) — per feature

| ID | Description | Feature | Storage / Source |
|:--:|-------------|---------|------------------|
| DR-001 | Composite: reads `banking_loans` + `banking_bill_reminders` (local Room) + FRED rates + Frankfurter exchange (Store5) | feat-home | Room + Store5 |
| DR-002 | `UserData` blob (themeBrand, useDynamicColor, darkThemeConfig, appLanguage + secure auth fields not touched here) | feat-settings | multiplatform-settings (plain `user_data_key` + secure) |
| DR-003 | `Loan` / `banking_loans` (id, name, kind, principal, principalRemaining, annualRatePercent, tenureMonths, monthsRemaining, monthlyPayment, nextDueDate, totalPaid, timestamps) | feat-loans | Room + OFFLINE_LOCAL_ONLY Store5 |
| DR-004 | No DTOs/tables — pure-local EMI math (`EmiResult`) | feat-emi-calculator | none |
| DR-005 | No owned tables; READS `banking_loans` (amortization pre-fill) + WRITES a `Loan` (wizard); `SubmitOutbox<LoanCalcScenario>` draft persistence | feat-calculators | shared Room + framework_submit_drafts outbox |
| DR-006 | READ-ONLY projection of `Loan`/`banking_loans`; `AmortizationRow` computed, never persisted | feat-amortization | Room read (reuses LoansStore) |
| DR-007 | `BillReminder` / `banking_bill_reminders` (id, name, amount, dueDay, recurrence, category, enabled, reminderDaysBefore, timestamps) | feat-bills | Room + OFFLINE_LOCAL_ONLY Store5 |
| DR-008 | FRED series [DFF, DPRIME, MORTGAGE30US, DGS10] → `interest_rate_series` Room table (24h TTL) | feat-rates | NETWORK_WITH_CACHE Store5; **needs FRED_API_KEY** |
| DR-009 | Frankfurter `latest` (list + spot) → `exchange_rates`; `{start}..{end}` (history) → `rate_history` | feat-currency-rates | NETWORK_WITH_CACHE / NETWORK_ONLY / CACHE_ONLY; **no key** |
| DR-010 | World Bank indicators [GDP NY.GDP.MKTP.CD, INFLATION_CPI FP.CPI.TOTL.ZG, UNEMPLOYMENT SL.UEM.TOTL.ZS] — in-memory only | feat-country-macro | MEMORY_ONLY Store5 (NO Room, NO SourceOfTruth); **no key** |
| DR-011 | CoinGecko `/coins/markets` (page-keyed) → `coin_markets` (2-min TTL); `/coins/{id}` → `coin_detail` (5-min TTL, **data-wired UI-pending**) | feat-crypto | NETWORK_WITH_CACHE Store5; **no key** |
| DR-012 | `WatchlistEntity` / `personal_watchlist` (coinId PK + addedAtMs); `AppDatabase` v5→v6 migration; live values joined from `feat-crypto` CoinMarket | feat-watchlist | raw Room DAO (NO Store5) + invalidation bridge |
| DR-013 | `PriceAlert` (id, coinId, AlertDirection, targetValue, enabled, createdAtMs) → `AlertEntity` / `alerts` (schema v8→v10) | feat-alerts | OFFLINE_LOCAL_ONLY Store5 + outbox. ⚠ **entity is lossy: drops `enabled` + `PCT_CHANGE` (P1 widen)** |

---

## Integration Requirements (IR)

| ID | Description | Service | Auth |
|:--:|-------------|---------|------|
| IR-001 | US interest-rate series | FRED (St. Louis Fed) | free `FRED_API_KEY` (graceful "not configured" state) |
| IR-002 | Foreign-exchange rates + history | Frankfurter | none (open) |
| IR-003 | Country macro indicators | World Bank Open Data | none (open) |
| IR-004 | Crypto coin markets + detail | CoinGecko | none (public tier) |
| IR-005 | Analytics / Crashlytics / App-Distribution | Firebase | opt-in Koin swap |

---

## Infrastructure / Non-Functional (driven by `/release` · `/ci` · `/secrets`; tracked-not-generated by `/idea-agent`)

> These are the reverse-engineered platform-wide NFRs and DRs from the infrastructure
> analysis. `/idea-agent` **tracks** them (they gate matrix-green as applicable
> capabilities) but does **not** generate them — they are owned by `/release`, `/ci`,
> and `/secrets`.

### Infrastructure NFRs

| ID | Description | Owner |
|:--:|-------------|-------|
| NFR-INFRA-OFFLINE-FIRST | `core-base/store` DecisionEngine drives loading/error/empty/content/stale per screen with **zero per-screen state code** | /ci |
| NFR-INFRA-CROSS-PLATFORM | Shared logic + Compose UI across **5 targets** (Android, iOS, macOS, Desktop, Web) via expect/actual | /ci, /release |
| NFR-INFRA-MVI-UNIDIRECTIONAL | All ViewModels extend `BaseViewModel<S, E, A>` — unidirectional MVI | /ci |
| NFR-INFRA-CI-QUALITY-GATE | Spotless + Detekt + DependencyGuard + Kover + verify-demo-convention; prod stages behind GitHub Environment reviewers | /ci |
| NFR-INFRA-MULTI-PLATFORM-RELEASE | firebase → internal → beta → production rung ladder; 23 targets / 5 platforms; mifos-x-actionhub v2 | /release |
| NFR-INFRA-A11Y-MOTION | MD3 motion duration-symmetry; TalkBack/VoiceOver support | /ci |
| NFR-INFRA-SECRETS-DUAL-MODE | Manual secrets (`secrets/live`) vs SOPS+age vault — identical canonical paths either mode | /secrets |
| NFR-INFRA-PERF | JankStats instrumentation; image-cache size caps | /ci |
| NFR-INFRA-SECURITY | `core-base/security`: cert-pinning, field encryption, biometric, session/tamper/deep-link guards, `isReleaseBuild` gate | /secrets, /ci |
| NFR-INFRA-FORK-SYNCABILITY | sync-dirs 3-way merge via `customization-surface.yaml` so forks pull upstream template updates | /release |

### Infrastructure DRs

| ID | Description | Owner |
|:--:|-------------|-------|
| DR-INFRA-ROOM-DB | Room 3 + `RoomChangeBus` wasmJs invalidation bridge (async fan-out workaround) | /ci |
| DR-INFRA-DATASTORE | multiplatform-settings — plain + secure variants | /ci |
| DR-INFRA-STORE5 | 8 archetypes: OFFLINE_LOCAL_ONLY / NETWORK_WITH_CACHE / NETWORK_ONLY / CACHE_ONLY / PERIODIC / MEMORY_ONLY / LOAD_ONCE / MUTABLE + SubmitOutbox drafts | /ci |
| DR-INFRA-NETWORK | Ktorfit / Ktor with `Result<T, RemoteError>` typed errors | /ci |
| DR-INFRA-SECRETS | Android keystore, Firebase/Play SA JSON, Apple `.p8`/Match, macOS `.p12`, Azure/MS-Store/Cloudflare/Netlify/Vercel tokens | /secrets |
| DR-EXT-FRED | FRED external API (US interest rates) — needs free key | /secrets |
| DR-EXT-WORLDBANK | World Bank Open Data external API (macro) — no key | — |
| DR-EXT-FRANKFURTER | Frankfurter external API (FX) — no key | — |
| DR-EXT-COINGECKO | CoinGecko external API (crypto) — no key | — |
| DR-EXT-FIREBASE | Firebase Analytics / Crashlytics / App-Distribution — opt-in Koin swap | /secrets |
