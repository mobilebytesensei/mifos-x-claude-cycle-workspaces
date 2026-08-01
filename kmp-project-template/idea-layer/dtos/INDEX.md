# DTO Registry — kmp-project-template

Auto-maintained by `/idea-data-dtos`. One row per canonical DTO at `idea-layer/dtos/{Name}.yaml`.
Bootstrapped via `/idea-data-dtos --bootstrap-from-server` (Phase 2 — Capture Core Data Contracts).

> **Backend-less template — `origin: synthetic` everywhere.** `kmp-project-template` has
> NO first-party server: data is either LOCAL Room / preferences or fetched from THIRD-PARTY
> public APIs (CoinGecko, Frankfurter, World Bank, FRED). `server-layer/` holds only bridge
> docs — there are no `api_specs/` or `tables/`. Every DTO therefore uses `source.origin: synthetic`
> (client-composed / no owned backend wire shape); the true underlying source (local Room table
> or external REST endpoint) is recorded in each file's `description` + `tags`. This keeps
> RULE-DTO-REGISTRY-001 D6 (server-owned-origin match) from being falsely tripped for external
> public APIs the template does not own. Registry reverse-engineered from the screen `api.yaml` +
> `data-flow.yaml` surface (NOT from `core/model` Kotlin — no command reverse-maps Kotlin).

| Name | Version | Origin | Consumers | Tier | Underlying source |
|---|---|---|---|---|---|
| AmortizationRow | 1.0.0 | synthetic | 1 | minimal | computed in-memory (no I/O) |
| BillReminder | 1.0.0 | synthetic | 2 | medium | local Room `banking_bill_reminders` |
| BillReminderSchedule | 1.0.0 | synthetic | 1 | minimal | platform notification payload |
| CoinDetail | 1.0.0 | synthetic | 2 | medium | Room cache `coin_detail` (CoinGecko domain) |
| CoinDetailDto | 1.0.0 | synthetic | 1 | medium | CoinGecko `api/v3/coins/{id}` wire |
| CoinMarket | 1.0.0 | synthetic | 2 | medium | Room cache `coin_markets` (CoinGecko domain) |
| CoinMarketDto | 1.0.0 | synthetic | 1 | medium | CoinGecko `api/v3/coins/markets` wire |
| ExchangeRates | 1.0.0 | synthetic | 2 | medium | Room cache `exchange_rates` (Frankfurter domain) |
| ExchangeRatesDto | 1.0.0 | synthetic | 2 | minimal | Frankfurter `v1/latest` wire |
| FredObservationsDto | 1.0.0 | synthetic | 2 | minimal | FRED `fred/series/observations` wire |
| InterestRateSeries | 1.0.0 | synthetic | 2 | medium | Room cache `interest_rate_series` (FRED domain) |
| Loan | 1.0.0 | synthetic | 3 | medium | local Room `banking_loans` |
| MacroIndicator | 1.0.0 | synthetic | 1 | medium | in-memory only (World Bank domain) |
| PriceAlert | 1.0.0 | synthetic | 1 | medium | local Room `alerts` (lossy persistence) |
| RateHistory | 1.0.0 | synthetic | 1 | medium | Room cache `rate_history` (Frankfurter domain) |
| RateHistoryDto | 1.0.0 | synthetic | 1 | minimal | Frankfurter `v1/{start}..{end}` wire |
| WatchlistItem | 1.0.0 | synthetic | 1 | minimal | local Room `personal_watchlist` |
| WorldBankResponseDto | 1.0.0 | synthetic | 1 | medium | World Bank `v2/country/{c}/indicator/{i}` wire |

**Totals:** 18 DTOs · 12 domain/local + 6 external-API wire · 0 orphan (every DTO has ≥1 consumer) · 0 duplicate names · 0 shadow of `templates/shared/common-dtos.yaml`.

## Shared baselines (from `templates/shared/common-dtos.yaml` — not redeclared here)

`ErrorEnvelope`, `PaginationCursor`, `PaginatedEnvelope`, `AuthSession` — available by reference; this template references none directly (no first-party error envelope; pagination is offset-page in Room, not cursor-wire).

## Notes

- **Primitives are not DTOs:** `Double`, `Int`, `Boolean`, `Unit` appear as `response.dto` in the
  scalar/aggregate operations (counts, sums, membership) and resolve as `PrimitiveType`, not registry entries.
- **Time-series flattening:** domain series (`InterestRateSeries.observations`, `MacroIndicator.observations`,
  `RateHistory.rates`) are `List<Point>` in source; modeled here as ordered `map_of {key,value}` so the
  registry stays connected (no orphan nested point DTOs). The true List shape is noted per field.
- **Pure-UI features have no DTOs:** `emi-calculator`, `calculators`, `profile`, `showcase`, `settings`
  declare `api: []` (settings uses local `preferences:` only) — no `has_api` data contract.
