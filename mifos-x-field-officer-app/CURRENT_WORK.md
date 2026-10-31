# Current Work

**Project**: mifos-x/mifos-x-field-officer-app
**Last Updated**: 2026-10-25 (audit pass, device-verified)
**Session**: session-mifos-x-field-officer-app-20260919135200752 (PR #2705, draft)
**Epic**: `plan-layer/project-plans/mifos-x/mifos-x-field-officer-app/active/template-port-fresh/`

---

## Active Focus

Porting the app onto the latest `openMF/kmp-project-template`. This is a **rewrite, not a merge** —
measured at the outset: 0 `kpt.*` imports shared with the template, dead `core-base/`, 308
`DataState` references, 0 Store5. The substrate was rebuilt bottom-up; features are then **migrated**
from the original source.

**Server:** the field-officer gateway, `https://apis.mifos.community/1.0/field/v1/`, tenant
`mifos-bank-1`. `app-profile/app.yaml#network.access_points[mifos]` is the ONE place it is written;
the server-config screen's default (`AppServerConfig`, core/network) is derived from it.

**Layer status**

| layer | state |
|---|---|
| `core/network` | done — 22 APIs, all `@ApiBinding("mifos")`, 168 operations, 0 missing vs original |
| `core/database` | done — Room, feature-first, KSP-generated `AppDatabase`; encrypted |
| `core/datastore` | done — file set matches the template exactly; fork prefs on `ProjectPreferencesRepository` |
| `core/store` | done — reads, offline-write queues, shared read cache |
| `core/data` | done — every API operation wired; writes through `MutationGateway` |
| `core/designsystem` | migrated — template theme + ported Mifos components |
| `core/ui` | migrated |
| `core/domain` | retired — deleted in Phase 9; only `kpt.core.domain.validation` remains |
| `feature/**` | **18 of 20** original modules ported or absorbed; **offline**, **path-tracking** and **passcode** not started |

Per-feature status table: `template-port-fresh/CURRENT_WORK.md`. Per-module detail (the SoT):
`source/mifos-x-field-officer-app/feature/<f>/MIGRATION.md`.

---

## Completed (2026-10-26)

- [x] Server config shows the LIVE instance (card + "Live" badge, signed-in user)
- [x] Drafts for all 12 create flows (client, group, centre, loan, group loan, savings, address, FD, RD, share, collateral, default account): offline = kept + replayed on reconnect; refused = "Save as draft" (FAILED + reason); Resume/Discard banner; Sync & Drafts titles + Open. Generic parts in core-base (FormDraft*, localized banner) — queued upstream and mirrored into the template tree (uncommitted)
- [x] Template fixes: OfflineSubmitSyncer retried nothing (first exception final) and swept only on reconnect; outbox not form-scoped; data-ksp qualifier collision; Koin raw-type syncer override
- [x] Create-flow bugs: no way to activate a pending client (+ AppScaffold dropped bottom bars); loan wizard stuck on Terms (id-less repayment strategies) and empty schedule table; group create did not open the group; RD/FD/share say when no product exists; inline status dialogs drawn transparent

## Completed (2026-10-25)

- [x] Server config: instances come from Supabase `app_server_config` (one row per instance, filtered by `supported_apps`), cached in the DB through `ServerInstancesStore` (bundled list as fallback); demo instances and roles; restart confirmation when signed in; the same screen from sign-in and Settings
- [x] Sign out at the bottom of Settings, "Sign out and clear data" by default
- [x] Audit of original vs migrated (group · center · loan · savings · client · search): dead edges wired (group accounts, clients and notes; centre meeting, summary and add-savings; loan notes and more-info; savings more-info; client → group; search create FAB and centre results). Notes are owner-generic (DB v18)
- [x] Device bugs fixed at root: group loans failed to decode · group savings had no owner name · search create/result navigation crashed (inner nav controller) · centre groups unfiltered · `CenterInfo` counts all 0 (lowercase keys) · client account money shown as "$0.0" · approved loan's status shown as "Unknown" · filter chip wrapped · FAB a11y labels

## Completed (2026-10-24)

- [x] Search record · About · Individual collection sheet · Run reports · Checker inbox & tasks
- [x] Center create · center + group offline download (device-verified, incl. airplane mode)
- [x] Create client with inline datatables · `ServerErrorParser` / `serverErrorMessage()` app-wide
- [x] Back on the gateway; server default derived from `app.yaml`
- [x] Device-verified on the gateway as `fieldofficer`: sign-in, lists, search, checker inbox,
      About, both downloads
- [x] Device bugs fixed at root: search key dead (`AppOutlinedTextField` dropped keyboard
      actions) · rejected session silent (now signs out, keeping data) · 403 showed generic copy ·
      a failed first load showed "no items"
- [x] Three core-base fixes proposed upstream: openMF/kmp-project-template#310 (draft)
- [x] G-8 four-platform build green for the first time (Android · desktop · web js+wasm · iOS simulator);
      fixed three breaks it exposed — web broken since 2026-09-19, CSV export not multiplatform, iOS
      fast path skipping compose resources
- [x] G-7 dead clickables 86 → 4 (root fixes + a tracer fix for previews/comments)

---

## Next Steps

1. **Offline dashboard** (the drawer's Offline Sync; 20 original files) — the download half already
   exists as `OfflineDownloadRepository`, so this is mostly the queue/sync screen.
2. **Path tracker** (5) — platform location + a background service.
3. **Passcode** (`libs/mifos-passcode`) — app lock around sign-in.
4. Owed inside landed modules: group create's tests + device verification · loan application
   charges/collateral + transaction row actions · document preview (multiplatform image+PDF viewer).

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
8. ViewModels derive state with `stateIn(WhileSubscribed)` — no `init {}` collectors.

---

## Session Notes

### Implementation Details
- Commands are `OnlineRequired` — they await the server and write nothing offline, returning
  `Blocked(OFFLINE)`. Offline capture is the explicit `OfflineQueueRepository`, never a silent
  fallback.
- Reads take the `CACHE_FIRST_SWR` default so an empty cache offline renders the app's own Empty,
  not a blocking `NoNetwork`. TTLs feed the freshness indicator only — never cache validity.
- A 401 on a credentialed request signs out (keeping local data) via `SignOutOnRejectedSession` +
  core-base's opt-in `UnauthorizedHandler`; a 403 is a client error that keeps the server's reason.

### Invariants not to break
- `offline-first-reads.sh` — no `validator` on a read store (an expired cache must still serve
  offline), no `createMemoryStore`, every store has a source of truth.
- `store-mutable-logout.sh` — every `MutableStore` declares `logout = false`; rows purge via the
  paired `pending*` read store. Omitting it crashes Koin **at launch**.
- Room: derived properties need `@Ignore`; a converter-stored value type must NOT also be `@DbEntity`.

### Gaps Identified
| Gap | Layer | Priority |
|-----|-------|----------|
| Offline dashboard · path tracker · passcode not ported | feature | P1 |
| Home tab is undesigned (`home-dashboard-undesigned`) — needs a product decision | feature | P1 |
| Group create has no tests and no device verification | feature | P1 |
| Gateway `fieldofficer` is 403 on reports + collection sheets; no client datatables — blocks three device checks | server | P2 |
| G-7 dead clickables 86 → 4: the 4 are the carried-over "More" options — a design decision (`client-signature-more-option-inert`) | ui | P2 |
| `app-profile/platforms/**` still claims "App Toolkit / collects no data" — false for this app, must not reach a store submission | deployment | P2 |
| iOS/desktop icons · store listing · privacy URL | deployment | P2 |

---

## Session Resumption

```bash
/context-start mifos-x-mifos-x-field-officer-app
```

**First thing to read**: "Next Steps" above — the offline dashboard is next. Then the per-feature
recipe, which applies unchanged.

Full epic detail (subordinate to this file, not a substitute):
`plan-layer/project-plans/mifos-x/mifos-x-field-officer-app/active/template-port-fresh/CURRENT_WORK.md`
