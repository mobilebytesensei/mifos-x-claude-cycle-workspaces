# Current Work

**Project**: mifos-x/mifos-x-field-officer-app
**Last Updated**: 2026-10-23
**Session**: session-mifos-x-field-officer-app-20260919135200752 (PR #2705)
**Epic**: `plan-layer/project-plans/mifos-x/mifos-x-field-officer-app/active/template-port-fresh/`

---

## Active Focus

Porting the app onto the latest `openMF/kmp-project-template`. This is a **rewrite, not a merge** —
measured at the outset: 0 `kpt.*` imports shared with the template, dead `core-base/`, 308
`DataState` references, 0 Store5. The substrate is rebuilt bottom-up; features are then **migrated**
from the original source.

**Layer status**

| layer | state |
|---|---|
| `core/network` | done — 22 APIs, all `@ApiBinding("mifos")`, 168 operations, 0 missing vs original |
| `core/database` | done — 69 Room tables, feature-first, KSP-generated `AppDatabase` |
| `core/datastore` | done — file set matches the template exactly; fork prefs on `ProjectPreferencesRepository` |
| `core/store` | done — 96 stores (reads, offline-write queues, shared read cache) |
| `core/data` | done — 42 repositories, **168/168 API operations wired** (96 reads, 72 writes) |
| `core/designsystem` | migrated — 89 files (template theme + ported Mifos components) |
| `core/ui` | migrated — 75 files |
| `core/domain` | retired — deleted in Phase 9; only `kpt.core.domain.validation` remains |
| `feature/**` | **12 of 21** original modules started, 9 not started (2026-10-23, measured from disk) |

Per-feature status table: `template-port-fresh/CURRENT_WORK.md`. Per-module detail:
`source/mifos-x-field-officer-app/feature/<f>/MIGRATION.md`.

Not started: collectionSheet · offline · report · checker-inbox-task · path-tracking · passcode ·
about · search-record (89 original `.kt`).

---

## Completed This Session

- [x] `core/data` rebuilt on `core/store`; every API operation reachable (was 16/168)
- [x] All 72 writes wired via 14 command repositories (`MutationGateway`, `OnlineRequired`)
- [x] Shared offline read cache (`api_response_cache`) + `cachedRead` store helper
- [x] `core/designsystem` + `core/ui` migrated from the original app
- [x] Two product-health gates added, each proven RED then GREEN
- [x] Unblocked every JVM target — see "Method too large" below

---

## Next Steps

1. **Redo `feature/auth` as a PORT, not a rewrite** — THE correction from this session
   - [ ] It was authored fresh, discarding the original 258-line `LoginScreen` (logo, strings,
         Scaffold/Snackbar, server-config entry, design-system components)
   - [ ] Port `6b66e8a43:feature/auth/src/commonMain/kotlin/com/mifos/feature/auth/login/**`
   - [ ] **Rule for all 19 remaining features: port the ORIGINAL file and rewrite its
         package/imports. Never author a replacement screen.** 196 original feature files import
         the Mifos components by name.

2. **Migrate the remaining 19 features, in this order**
   - [ ] client (163 files) · center (17) · groups (13) · loan (62) · savings (33)
   - [ ] recurringDeposit (10) · note (8) · document (8) · data-table (20)
   - [ ] checker-inbox-task (10) · collectionSheet (17) · report (16) · offline/sync (20)
   - [ ] search (9) · search-record (4) · path-tracking (10) · activate (5) · settings (12) · about (4)

### Per-feature recipe (proven on the UI-substrate migration)

1. `git show 6b66e8a43:<original file>` — the ORIGINAL is the input.
2. Rewrite namespaces, **each substitution applied once** (chaining produced a `kpt.kpt.` prefix):
   `com.mifos.core.`→`kpt.core.` · `com.mifos.room.`→`kpt.core.database.` ·
   `template.core.base.`→`kpt.core.base.` · `org.mifos.core.`→`kpt.core.` ·
   `androidclient.<mod>.generated.resources`→`kpt.<mod>.generated.resources`
3. Adapt to the new data layer: `DataState`→`ScreenDataStream`/`MutationResult`;
   `UserPreferencesRepository`→`ProjectPreferencesRepository`; dropped `core/domain` use-cases
   become inline logic or a `core/data` call.
4. Scaffold: `build.gradle.kts` (`cmp.feature.convention`, `packageOfResClass =
   "kpt.feature.<f>.generated.resources"`), `AndroidManifest.xml`, `composeResources/`,
   `di/<F>Module.kt` with `viewModelOf`.
5. **Fork seams**: include in `settings.local.gradle.kts` (NEVER `settings.gradle.kts` —
   RULE-KMP-FORK-MODULE-SEAM-001) + a row in `feature/module-packages.yaml`.
6. `@FeatureDestination` on top-level nav entries. **Login is deliberately excluded** — that
   annotation registers on the AUTHENTICATED graph, which is where the sign-in gate must not be.
7. A ViewModel test per screen; prefer real impls over `MapSettings` to hand-written fakes.

---

## Session Notes

### Implementation Details
- Commands are `OnlineRequired` — they await the server and write nothing offline, returning
  `Blocked(OFFLINE)`. An optimistic approval is a lie an officer would act on. Offline capture is
  the explicit `OfflineQueueRepository`, never a silent fallback.
- Reads take the `CACHE_FIRST_SWR` default so an empty cache offline renders the app's own Empty,
  not a blocking `NoNetwork`. TTLs feed the freshness indicator only — never cache validity.
- Three latent bugs fixed at root, all invisible until generated code was first compiled:
  16 types declared as Room tables **and** stored as converted columns (plus 13 foreign keys that
  could never be satisfied) — that dead schema pushed `onValidateSchema` past the JVM 64KB method
  cap and blocked **every** JVM target; computed properties Room tried to assign (`@Ignore`);
  the template's own `PasswordChecker` importing a type from the wrong package.

### Invariants not to break
- `offline-first-reads.sh` — no `validator` on a read store (an expired cache must still serve
  offline), no `createMemoryStore`, every store has a source of truth.
- `store-mutable-logout.sh` — every `MutableStore` declares `logout = false`; rows purge via the
  paired `pending*` read store. Omitting it crashes Koin **at launch**.
- Room: derived properties need `@Ignore`; a converter-stored value type must NOT also be `@DbEntity`.

### Gaps Identified
| Gap | Layer | Priority |
|-----|-------|----------|
| `feature/auth` written fresh — must be redone as a port | feature | P1 |
| 19 feature modules not migrated | feature | P1 |
| `core/domain` — 82 files on retired `com.mifos.core.data.*` | domain | P2 |
| `MifosImageCropperDialog` / `MifosSignatureDrawDialog` withheld — `com.attafitamim.krop` and `com.niyajali.compose.sign` are in neither the catalog nor the template; block client image-upload + signature | ui | P2 |
| 4 `retrieveAll*` filtered queries + 5 raw downloads are live-only by design (reason stated on each `{Ctx}LiveReadRepository` method) | data | P3 |
| `app-profile/platforms/**` still claims "App Toolkit / 100% offline, no login" — false for this app, must not reach a store submission | deployment | P2 |

---

## Session Resumption

```bash
/context-start mifos-x-mifos-x-field-officer-app
```

**First thing to read**: "Next Steps" above — item 1 is redoing `feature/auth` as a PORT of the
original screen, not the fresh rewrite currently committed. Then the per-feature recipe, which
applies unchanged to the remaining 19 features.

Full epic detail (subordinate to this file, not a substitute):
`plan-layer/project-plans/mifos-x/mifos-x-field-officer-app/active/template-port-fresh/CURRENT_WORK.md`
