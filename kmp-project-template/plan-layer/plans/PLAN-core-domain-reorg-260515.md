# Implementation Plan: core/ Domain-Context Re-organisation

## Metadata

| Field | Value |
|---|---|
| Plan ID | PLAN-core-domain-reorg-260515 |
| Generated | 2026-05-15 |
| Status | Draft |
| Scope | All `core/` modules + `sync-dirs.sh` |
| Type | Refactor — package re-organisation (no behaviour changes) + consumer workflow |
| Branch | `feat/core-domain-reorg-260515` from `origin/development` |
| Target PR | `openMF/kmp-project-template` base `development` |

---

## Goal

Replace the current **technical-role flat packages** (`repository/`, `repositoryImpl/`, flat
root) inside each `core/` module with **domain-context sub-packages** so every layer of a
domain is immediately discoverable.

A consumer adding **loan management** adds exactly these — nothing else:

```
core/model/loan/      Loan, LoanProduct, LoanStatus
core/network/loan/    LoanApi, LoanDto, LoanProductDto
core/database/loan/   LoanDao, LoanEntity, LoanEntityMapper
core/data/loan/       LoanRepository (interface)
core/data/loan/impl/  LoanRepositoryImpl, LoanStore
core/domain/loan/     GetLoanUseCase, ApproveLoanUseCase
```

Six consistent folders. One per module. Same name everywhere.

**Extended goal (Phase 7):** Extend `sync-dirs.sh` so that consumer apps (`mobile-wallet`,
`mifos-mobile`) can sync the **framework infrastructure** from this template automatically,
while treating `crypto/`, `currency/`, `emi/` packages as **sample patterns** they replace
with their own domains (`loan/`, `savings/`, `beneficiary/`, etc.).

---

## Consumer app audit — key findings

Audited `mobile-wallet` and `mifos-mobile` before finalising this plan.

### What mobile-wallet already does right (gold standard)

`mobile-wallet/core/model` is **already domain sub-packages** — `account/`, `bank/`,
`beneficiary/`, `client/`, `datatables/invoice/`, `instance/`, `interbank/`, `kyc/`,
`notification/`, `office/`, `savedcards/`, `savingsaccount/`, `search/`,
`standinginstruction/`, `user/`, `utils/`. This is exactly our target structure.

**What it still needs:** `core/data` is flat `repository/` + `repositoryImpl/` + `mapper/`.
Our plan is the direct upgrade.

### What mifos-mobile does right

- Rich `core/data/mapper/{domain}/` sub-packages (`accounts/`, `auth/`, `beneficiary/`,
  `charge/`, `client/`, `guarantor/`, `loan/`, `payloads/`, `savings/`, `transactions/`).
- Clean `core/network/dto/{domain}/` sub-packages.

### What mifos-mobile over-engineers (do NOT copy)

`core/model/entity/accounts/loan/calendardata/` — **4 levels deep**. This makes navigation
worse, not better. **Rule: 2 levels maximum** (`module/domain/`). Never 3+ levels.

### `user/` nesting decision — FLAT (confirmed)

Do **not** nest `user/` into `userdata/` + `userlogout/`. Mobile-wallet keeps `user/` flat
with `UserDataRepository`, `UserPreferencesRepository`, etc. all as siblings. The types
are few enough that nesting adds navigation friction without clarity gain.

```
core/data/user/                  ✅ CORRECT
├── UserDataRepository.kt
├── UserLogoutManager.kt
├── LogoutEvent.kt
├── LogoutReason.kt
└── impl/
    ├── UserDataRepositoryImpl.kt
    └── UserLogoutManagerImpl.kt

core/data/user/userdata/         ❌ WRONG — over-nesting
core/data/user/userlogout/       ❌ WRONG — over-nesting
```

### Mapper placement rule

- **Entity mappers** (DB entity → domain model): live inside the **domain sub-package** of
  `core/database/{domain}/` — co-located with the entity (e.g., `CoinMarketEntityMapper.kt`
  next to `CoinMarketEntity.kt`). This mirrors mifos-mobile's pattern.
- **DTO mappers** (network DTO → domain model): live inside `core/data/{domain}/impl/` —
  co-located with the repository impl that uses them.
- **No separate top-level `mapper/` directory.** mifos-mobile's flat `mapper/` is the
  anti-pattern we're fixing.

---

## Grouping strategy per module type

| Module | Strategy | Reason |
|---|---|---|
| `core/model` | Domain sub-packages | Entities belong to a domain; mobile-wallet already does this |
| `core/network` | Domain sub-packages | APIs + DTOs belong to a domain |
| `core/database` | Domain sub-packages | DAOs + Entities + EntityMappers co-located by domain |
| `core/data` | Domain sub-packages + `impl/` nested | Interface/impl boundary; features import interfaces only |
| `core/domain` | Feature sub-packages | Use cases belong to a feature context |
| `core/analytics` | **Leave flat for now** | <10 events total; split deferred until ≥20 events per domain |
| `core/ui` | Concern sub-packages | Already partially done; extend consistently |
| `core/designsystem` | **No change** | Already correct (`theme/`, `icon/`, `utils/`) |
| `core/datastore` | **No change** | 3 files, cross-cutting; sub-packages would be 1 file each |
| `core/store` | **No change** | 4 files, pure customisation seam |
| `core/common` | **No change** | 2 utility files; no grouping needed |

---

## `infra/` boundary rule (enforced across all phases)

`infra/` sub-packages contain **framework wiring only**. No domain types in `infra/` signatures.

- ✅ `StoreCacheManagerImpl` — registers stores (opaque `Store<*, *>` — no domain types)
- ✅ `RoomFetchedAtRepository` — persists timestamps (plain `String` key, `Instant` value)
- ✅ `NetworkMonitor` — emits `NetworkStatus` (framework type, not domain)
- ❌ Wrong: `infra/LoanBookkeeperHelper` — touches domain types, belongs in `loan/impl/`

---

## Phase 1 — `core/model` (11 files)

**Rule:** No `impl/` needed — models are pure data, no interface/impl split.
**Max nesting depth:** 2 levels — `module/domain/File.kt`. Never deeper.

**Current state:** `CoinMarket`, `ExchangeRates`, `EmiResult` are already in `fintech/`
sub-package; `CountryFlagUtils` is in `util/`; remaining 7 files are at root. This phase
renames `fintech/` into correct domain splits and moves root files to `user/`.

### Target structure

```
org.mifos.core.model/
├── crypto/
│   └── CoinMarket.kt                 (was fintech/)
├── currency/
│   ├── ExchangeRates.kt              (was fintech/)
│   ├── Country.kt                    (was root)
│   └── CountryFlagUtils.kt           (was util/)
├── emi/
│   └── EmiResult.kt                  (was fintech/ — was miscategorised with market-data types)
└── user/
    ├── AuthState.kt                  (was root)
    ├── UserData.kt                   (was root)
    ├── DarkThemeConfig.kt            (was root)
    ├── ThemeBrand.kt                 (was root)
    ├── LanguageConfig.kt             (was root)
    └── UnlockType.kt                 (was root)
```

### Consumer domain examples (mobile-wallet pattern)

A consumer like mobile-wallet would add alongside these sample domains:

```
org.mifos.core.model/
├── crypto/         ← sample (consumer can delete)
├── currency/       ← sample (consumer can delete)
├── emi/            ← sample (consumer can delete)
├── user/           ← keep (cross-cutting auth)
├── loan/           ← consumer adds: Loan, LoanProduct, LoanStatus
├── savings/        ← consumer adds: SavingsAccount, SavingsProduct
├── beneficiary/    ← consumer adds: Beneficiary, BeneficiaryType
├── client/         ← consumer adds: Client, ClientStatus
└── account/        ← consumer adds: Account, AccountType, AccountSummary
```

### Consumer impact
`core/data`, `core/datastore`, `core/domain`, `feature/*` — import updates only.

---

## Phase 2 — `core/network` (6 files)

**Rule:** Each domain owns its own API interface + all DTOs it produces. Shared infra
(`FintechApiClient`) moves to `di/` since it's a Ktor client factory, not a domain.

**Current state:** All non-DI files live in `fintech/` or `fintech/model/`. `fintech/model/`
is a pre-existing 3-level depth violation (`network.fintech.model`) that this phase fixes.

### Target structure

```
org.mifos.core.network/
├── crypto/
│   ├── CoinGeckoApi.kt               (was fintech/)
│   └── CoinMarketDto.kt              (was fintech/model/ — fixes 3-level depth violation)
├── currency/
│   ├── FrankfurterApi.kt             (was fintech/)
│   └── ExchangeRatesDto.kt           (was fintech/model/ — fixes 3-level depth violation)
└── di/
    ├── NetworkModule.kt              (was di/ — unchanged)
    └── FintechApiClient.kt           (was fintech/ — Ktor client factory, not domain)
```

### Consumer domain examples (mifos-mobile pattern)

```
org.mifos.core.network/
├── crypto/           ← sample
├── currency/         ← sample
├── loan/             ← consumer adds: LoanApi, LoanDto, LoanProductDto, LoanRepaymentDto
├── savings/          ← consumer adds: SavingsApi, SavingsAccountDto, SavingsProductDto
├── beneficiary/      ← consumer adds: BeneficiaryApi, BeneficiaryDto
└── di/               ← framework infra (synced)
```

### Consumer impact
`core/data` store factory files — import updates only.

---

## Phase 3 — `core/database` (24 files)

**Rule:** `AppDatabase.kt` stays at root — Room requires a stable aggregator class location.
Its internal DAO property imports and `@TypeConverters` annotation imports both require updating.

**Mapper placement:** `*EntityMapper.kt` files live **inside the domain sub-package**,
co-located with the entity they transform. No separate `mapper/` root directory.

**Current state:** Files are in technical-role sub-packages — `dao/`, `entity/`, `mapper/`,
`utils/`. This phase reorganises from technical-role → domain packages. The `di/` sub-package
(`DatabaseModule.kt` + platform variants) stays unchanged.

### Target structure

```
org.mifos.core.database/
├── crypto/
│   ├── CoinDetailDao.kt              (was dao/)
│   ├── CoinDetailEntity.kt           (was entity/)
│   ├── CoinDetailEntityMapper.kt     (was mapper/ — co-locating with entity)
│   ├── CoinMarketDao.kt              (was dao/)
│   ├── CoinMarketEntity.kt           (was entity/)
│   ├── CoinMarketEntityMapper.kt     (was mapper/ — co-locating with entity)
│   └── FintechTypeConverters.kt      (was utils/ — crypto-specific converters)
├── currency/
│   ├── ExchangeRatesDao.kt           (was dao/)
│   ├── ExchangeRatesEntity.kt        (was entity/)
│   ├── ExchangeRatesEntityMapper.kt  (was mapper/)
│   ├── RateHistoryDao.kt             (was dao/)
│   ├── RateHistoryEntity.kt          (was entity/)
│   ├── RateHistoryEntityMapper.kt    (was mapper/)
│   └── ChargeTypeConverters.kt       (was utils/ — currency-specific converters)
├── infra/
│   ├── BookkeeperDao.kt              (was dao/)
│   ├── BookkeeperEntity.kt           (was entity/)
│   ├── DraftDao.kt                   (was dao/)
│   ├── DraftEntity.kt                (was entity/)
│   ├── FetchedAtDao.kt               (was dao/)
│   └── FetchedAtEntity.kt            (was entity/)
├── sample/
│   ├── SampleDao.kt                  (was dao/ — template placeholder)
│   └── SampleEntity.kt               (was entity/)
├── di/                               (unchanged — DatabaseModule.kt + platform variants)
└── AppDatabase.kt                    (stays root — update entity + @TypeConverters imports)
```

### Consumer domain examples

```
org.mifos.core.database/
├── infra/            ← framework infra (synced)
├── crypto/           ← sample
├── currency/         ← sample
├── loan/             ← consumer adds: LoanDao, LoanEntity, LoanEntityMapper
├── savings/          ← consumer adds: SavingsDao, SavingsEntity, SavingsEntityMapper
└── AppDatabase.kt    ← consumer updates @Database(entities=[...]) annotation
```

### Consumer impact
`core/data` store factories + `AppDatabase.kt` DAO property imports + `@TypeConverters` annotation imports (converters move to domain packages) — import updates only.

---

## Phase 4 — `core/data` (26 files)

**Rule:** `impl/` nested inside each domain package. Features import from `crypto/`
(the interface), never from `crypto/impl/` (the implementation). This is the one module
where the interface/impl boundary matters most at compile time.

**`infra/` boundary:** All types in `infra/` signatures must be framework types only
(`String`, `Instant`, `Store<*, *>`, `NetworkStatus`). No domain model types.

**`user/` is flat** — `UserDataRepository` and `UserLogoutManager` are siblings in
`user/`, not nested into sub-sub-packages. Confirmed by mobile-wallet audit.

**Current state packages:** `repository/` (interfaces + TimeZoneMonitor), `repositoryImpl/`
(impls), `store/` (Store factories + RoomBookkeeper + RoomSubmitOutbox), `model/` (LogoutEvent,
LogoutReason — dissolved into `user/` by this phase), `di/` (unchanged), `util/` (unchanged).

### Target structure

```
org.mifos.core.data/
├── crypto/
│   ├── CryptoRepository.kt           (interface — was repository/)
│   └── impl/
│       ├── CryptoRepositoryImpl.kt   (was repositoryImpl/)
│       ├── CoinDetailStore.kt        (was store/)
│       └── CoinMarketsStore.kt       (was store/)
├── currency/
│   ├── CurrencyRepository.kt         (interface — was repository/)
│   └── impl/
│       ├── CurrencyRepositoryImpl.kt (was repositoryImpl/)
│       ├── ExchangeRatesStore.kt     (was store/)
│       └── RateHistoryStore.kt       (was store/)
├── user/
│   ├── UserDataRepository.kt         (interface — was repository/)
│   ├── UserLogoutManager.kt          (interface — was repository/)
│   ├── LogoutEvent.kt                (was model/ — model/ sub-package dissolved)
│   ├── LogoutReason.kt               (was model/ — model/ sub-package dissolved)
│   └── impl/
│       ├── UserDataRepositoryImpl.kt (was repositoryImpl/)
│       └── UserLogoutManagerImpl.kt  (was repositoryImpl/)
├── infra/
│   ├── NetworkMonitor.kt             (interface — was repository/)
│   ├── StoreCacheManager.kt          (interface — was repository/)
│   ├── TimeZoneMonitor.kt            (interface — was repository/)
│   └── impl/
│       ├── NetworkMonitorImpl.kt     (was repositoryImpl/ — commonMain)
│       ├── StoreCacheManagerImpl.kt  (was repositoryImpl/)
│       ├── RoomFetchedAtRepository.kt(was repositoryImpl/)
│       ├── RoomBookkeeper.kt         (was store/)
│       ├── RoomSubmitOutbox.kt       (was store/)
│       └── TimeZoneMonitorImpl.kt    (was repository/, androidMain source set)
├── util/                             (unchanged — was util/)
│   ├── ResultExtensions.kt
│   └── SharedFlowExtensions.kt
└── di/
    ├── RepositoryModule.kt           (unchanged)
    └── ApplicationStoreRegistry.kt   (unchanged)
```

> **Note on androidMain source sets:**
> - `TimeZoneMonitorImpl` lives in `androidMain` — move to `infra/impl/` in the androidMain source tree, update package only.
> - `NetworkMonitorImpl` is in `commonMain` (uses `NetworkMonitorProvider.install()` delegation) — no androidMain work needed for this file.

### Consumer domain examples (mobile-wallet upgrade path)

A consumer migrating from flat `repository/` to domain sub-packages:

```
org.mifos.core.data/
├── user/             ← keep (synced from template)
├── infra/            ← keep (synced from template)
├── di/               ← keep (synced from template)
├── crypto/           ← sample (consumer deletes)
├── currency/         ← sample (consumer deletes)
├── loan/             ← consumer adds
│   ├── LoanRepository.kt
│   └── impl/
│       ├── LoanRepositoryImpl.kt
│       └── LoanStore.kt
├── savings/          ← consumer adds
│   ├── SavingsRepository.kt
│   └── impl/
│       ├── SavingsRepositoryImpl.kt
│       └── SavingsAccountStore.kt
└── beneficiary/      ← consumer adds
    ├── BeneficiaryRepository.kt
    └── impl/
        └── BeneficiaryRepositoryImpl.kt
```

### Consumer impact
`feature/crypto`, `feature/currency-rates`, `feature/emi-calculator`, `cmp-navigation` —
import updates only. Feature modules must only import from `crypto/`, `currency/`, `user/`
(interfaces), never from `*/impl/`.

---

## Phase 5 — `core/domain` (1 file, establish pattern)

**Rule:** Sub-package name = **feature context**, not technical category.
`emi/` not `calculator/` — matches the feature module name `feature/emi-calculator`.

### Target structure

```
org.mifos.core.domain/
└── emi/
    └── CalculateEmiUseCase.kt        (was usecase/ flat — renamed sub-package)
```

### Consumer domain pattern

```
org.mifos.core.domain/
├── emi/              ← sample
│   └── CalculateEmiUseCase.kt
├── loan/             ← consumer adds
│   ├── GetLoanUseCase.kt
│   ├── ApproveLoanUseCase.kt
│   └── MakeLoanRepaymentUseCase.kt
└── savings/          ← consumer adds
    ├── GetSavingsAccountUseCase.kt
    └── MakeDepositUseCase.kt
```

### Consumer impact
`feature/emi-calculator` — 1 import update.

---

## Phase 6 — `core/ui` (13 files)

**Rule:** Concern-based grouping (not domain). `core/ui` is a shared component library —
it has no domain knowledge. Sub-package names describe component concern, not app domain.

**Correction from draft:** `security/` is wrong — `PasswordStrengthIndicator` and
`RevealSwipe` are input widgets, not a security layer. Use `input/`.

### Target structure

```
org.mifos.core.ui/
├── bottombar/                        (already exists ✓ — no change)
│   ├── KptBottomBar.kt
│   ├── KptNavigationBarItem.kt
│   ├── KptNavigationRail.kt
│   └── KptNavigationRailItem.kt
├── scaffold/                         (already exists ✓ — no change)
│   ├── KptScaffold.kt
│   └── KptPullToRefreshState.kt
├── input/                            (new — moves from root)
│   ├── PasswordStrengthIndicator.kt  (was root)
│   └── RevealSwipe.kt                (was root)
├── utils/                            (already exists ✓ — no change)
│   ├── PasswordChecker.kt
│   ├── PasswordStrength.kt
│   ├── PasswordStrengthExtensions.kt
│   └── JankStatsExtensions.kt        (was androidMain root)
└── NavigationItem.kt                 (stays root — global nav contract, no sub-package)
```

### Consumer impact
`feature/*` screens using `PasswordStrengthIndicator` or `RevealSwipe` — import updates only.

---

## Phase 7 — `sync-dirs.sh` extension (consumer workflow)

**Goal:** Consumer apps sync **framework infrastructure** from the template automatically.
Sample domains (`crypto/`, `currency/`, `emi/`) are **not synced** — they are patterns
the consumer studies, then replaces with their own domains.

### Template/sample boundary

| Path | Category | Sync to consumer |
|---|---|---|
| `core/model/user/` | Framework (auth) | ✅ Yes |
| `core/model/crypto/` | Sample domain | ❌ No — consumer replaces |
| `core/model/currency/` | Sample domain | ❌ No — consumer replaces |
| `core/model/emi/` | Sample domain | ❌ No — consumer replaces |
| `core/data/user/` | Framework (auth) | ✅ Yes |
| `core/data/infra/` | Framework (network/cache) | ✅ Yes |
| `core/data/di/` | Framework (DI) | ✅ Yes |
| `core/data/crypto/` | Sample domain | ❌ No |
| `core/data/currency/` | Sample domain | ❌ No |
| `core/database/infra/` | Framework (bookkeeper/outbox) | ✅ Yes |
| `core/database/crypto/` | Sample domain | ❌ No |
| `core/database/currency/` | Sample domain | ❌ No |
| `core/database/sample/` | Sample domain | ❌ No |
| `core/network/di/` | Framework (Ktor client) | ✅ Yes |
| `core/network/crypto/` | Sample domain | ❌ No |
| `core/network/currency/` | Sample domain | ❌ No |
| `core/ui/` | Framework (shared components) | ✅ Yes |
| `core/designsystem/` | Framework (design tokens) | ✅ Yes |
| `core/datastore/` | Framework (preferences) | ✅ Yes |
| `core/store/` | Customisation seam | ✅ Yes (consumer overrides, not replaces) |
| `core/common/` | Framework utilities | ✅ Yes |
| `core/analytics/` | Framework (event tracking) | ✅ Yes |
| `core/domain/emi/` | Sample domain | ❌ No |
| `feature/crypto/` | Sample feature | ❌ No |
| `feature/currency-rates/` | Sample feature | ❌ No |
| `feature/emi-calculator/` | Sample feature | ❌ No |

### `sync-dirs.sh` changes

```bash
# Current SYNC_DIRS (does not include core/)
SYNC_DIRS=(
    "cmp-desktop"
    "cmp-web"
    "cmp-shared"
    "core-base"
    "build-logic"
    "fastlane"
    "fastlane-config"
    "scripts"
    "config"
    ".github"
    ".run"
)

# After Phase 7 — add framework-only core/ sub-paths
SYNC_DIRS=(
    # ... existing entries unchanged ...
    "core/ui"
    "core/designsystem"
    "core/datastore"
    "core/store"
    "core/common"
    "core/analytics"
)

# These paths use selective rsync (framework sub-dirs only, not the whole module):
# NOTE: core/domain is intentionally EXCLUDED — it contains only the sample emi/ use case.
# Consumers build their own domain from scratch (no framework infrastructure in core/domain).
CORE_FRAMEWORK_PATHS=(
    "core/model/user"
    "core/data/user"
    "core/data/infra"
    "core/data/di"
    "core/database/infra"
    "core/network/di"
)
```

> **Implementation note:** The existing `sync_directory()` uses `git checkout <branch> -- <path>`
> which works correctly for sub-paths (git supports path-level checkout). For
> `CORE_FRAMEWORK_PATHS` entries, add a new `sync_subpath()` helper that calls
> `git checkout "$temp_branch" -- "$subpath"` without the exclusion-preservation logic
> (sample domains are simply never listed, so nothing is overwritten). Consumer domain
> packages (`loan/`, `savings/`, etc.) adjacent to the synced paths are never touched.
>
> ```bash
> sync_subpath() {
>     local subpath=$1
>     local temp_branch=$2
>     print_step "Syncing framework sub-path ${BOLD}$subpath${NC}..."
>     if [ "$DRY_RUN" = false ]; then
>         git checkout "$temp_branch" -- "$subpath" || {
>             print_error "Failed to sync $subpath"
>             return 1
>         }
>     fi
> }
> ```

### Consumer workflow after Phase 7

```bash
# Consumer runs template sync
./sync-dirs.sh

# Template syncs automatically:
#   core-base/        ← Store5 infrastructure
#   core/ui/          ← shared UI components
#   core/designsystem/ ← design tokens
#   core/data/infra/  ← NetworkMonitor, StoreCacheManager
#   core/data/user/   ← UserDataRepository interface + impl
#   core/store/       ← AppScreenStateDefaults, AppErrorMapper seam

# Consumer manually adds (following sample patterns):
#   core/model/loan/
#   core/data/loan/
#   core/database/loan/
#   feature/loan-list/
```

---

## Modules with no changes

| Module | Reason |
|---|---|
| `core/designsystem` | Already correct (`theme/`, `icon/`, `utils/`) |
| `core/analytics` | Deferred — split only when ≥20 events per domain; currently 1 flat file is fine |
| `core/datastore` | 3 files, zero domain knowledge; sub-packages would be 1 file each |
| `core/store` | 4 files, pure customisation seam (`AppErrorMapper`, `AppStoreRegistry`) |
| `core/common` | 2 utility files (`FormatDate`, `FormatNumber`); no grouping needed |

---

## Full consumer impact summary

| Module | Files requiring import updates |
|---|---|
| `core/data` (internal) | `RepositoryModule.kt` — store factory + DAO references |
| `core/database` (internal) | `AppDatabase.kt` — DAO property types |
| `core/datastore` | `UserPreferencesRepositoryImpl.kt` — UserData model import |
| `core/domain` | `CalculateEmiUseCase.kt` — EmiResult model import |
| `core/store` | `AppErrorMapper.kt`, `AppStoreRegistry.kt` |
| `feature/crypto` | ViewModel + Screen files (~4 files) |
| `feature/currency-rates` | ViewModel + Screen files (~5 files) |
| `feature/emi-calculator` | ViewModel file (~1 file) |
| `cmp-navigation` | `AppViewModel.kt` |

---

## Implementation checklist

### Phase 1 — `core/model`
- [ ] Rename `fintech/` → split into `crypto/`, `currency/`, `emi/`; create `user/`; rename `util/` content → `currency/`
- [ ] Move + update `package` declarations (11 files): 4 from `fintech/`, 1 from `util/`, 6 from root
- [ ] Update imports in all consumers
- [ ] Migrate test files under `commonTest`/`desktopTest` to match new package names
- [ ] Commit: `refactor(core/model): domain sub-packages`

### Phase 2 — `core/network`
- [ ] Rename `fintech/` → split into `crypto/`, `currency/`; move `FintechApiClient` to `di/`; flatten `fintech/model/` DTOs into domain packages (fixes 3-level depth)
- [ ] Move + update `package` declarations (6 files): 3 from `fintech/`, 2 from `fintech/model/`, 1 unchanged in `di/`
- [ ] Update imports in `core/data` store factories
- [ ] Commit: `refactor(core/network): domain sub-packages`

### Phase 3 — `core/database`
- [ ] Create sub-directories: `crypto/`, `currency/`, `infra/`, `sample/`; `di/` stays unchanged
- [ ] Move + update `package` declarations (~23 production files): from `dao/`, `entity/`, `mapper/`, `utils/` → domain sub-packages
- [ ] Update `AppDatabase.kt` DAO property import statements
- [ ] Update `AppDatabase.kt` `@TypeConverters(ChargeTypeConverters::class, FintechTypeConverters::class)` imports (converters move to `currency/` and `crypto/`)
- [ ] Verify entity mappers are in domain sub-packages (not a root `mapper/` dir)
- [ ] Migrate test files (`dao/`, `entity/`, `utils/` test packages → domain test packages)
- [ ] Commit: `refactor(core/database): domain sub-packages`

### Phase 4 — `core/data`
- [ ] Create domain directories with nested `impl/`: `crypto/impl/`, `currency/impl/`, `user/impl/`, `infra/impl/`; `util/` and `di/` unchanged
- [ ] Move + update `package` declarations (~24 production files): from `repository/`, `repositoryImpl/`, `store/`, `model/` → domain sub-packages; `util/` and `di/` stay
- [ ] Delete dissolved `model/` directory after moving `LogoutEvent` + `LogoutReason` to `user/`
- [ ] Update `androidMain` source set: `TimeZoneMonitorImpl` only (moves to `infra/impl/`); `NetworkMonitorImpl` is in `commonMain` — no androidMain work needed
- [ ] Update imports in all consumer modules
- [ ] Verify `user/` is flat (not nested into `userdata/`, `userlogout/`)
- [ ] Verify `UserLogoutManagerImpl` is only in `user/impl/` (not in `infra/impl/`)
- [ ] Commit: `refactor(core/data): domain sub-packages`

### Phase 5 — `core/domain`
- [ ] Rename `usecase/` → `emi/`, update `package` declaration
- [ ] Update import in `feature/emi-calculator`
- [ ] Commit: `refactor(core/domain): emi sub-package`

### Phase 6 — `core/ui`
- [ ] Create `input/` sub-directory
- [ ] Move `PasswordStrengthIndicator.kt` + `RevealSwipe.kt` to `input/`
- [ ] Update imports in consumers
- [ ] Commit: `refactor(core/ui): input sub-package`

### Phase 7 — `sync-dirs.sh`
- [ ] Add whole-module entries to `SYNC_DIRS`: `core/ui`, `core/designsystem`, `core/datastore`, `core/store`, `core/common`, `core/analytics`
- [ ] Add `CORE_FRAMEWORK_PATHS` array for sub-directory-level syncs (see implementation sketch above)
- [ ] Implement `sync_subpath()` helper function (see implementation sketch above)
- [ ] Add loop over `CORE_FRAMEWORK_PATHS` calling `sync_subpath()` in main sync flow
- [ ] Add `SAMPLE_DOMAINS` array + README note documenting what consumers replace vs. keep
- [ ] Test: `--dry-run` against a consumer app; verify consumer `loan/` packages untouched
- [ ] Commit: `feat(sync-dirs): add core framework sub-path sync`

### Verification
- [ ] `./gradlew :core:model:test` — pass (after Phase 1)
- [ ] `./gradlew :core:network:test` — pass (after Phase 2)
- [ ] `./gradlew :core:database:test` — pass (after Phase 3)
- [ ] `./gradlew :core:data:test` — pass (after Phase 4)
- [ ] `./gradlew :core:domain:test` — pass (after Phase 5)
- [ ] `./gradlew :core:ui:test` — pass (after Phase 6)
- [ ] `./gradlew :core-base:store:jsTest` — 211 tests pass (no regressions, any phase)
- [ ] `./gradlew :cmp-android:assembleDebug` — BUILD SUCCESSFUL (after Phase 4)
- [ ] `./gradlew detekt` on all changed modules — clean (after each phase)
