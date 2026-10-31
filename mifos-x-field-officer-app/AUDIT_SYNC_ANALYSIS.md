# AUDIT_SYNC_ANALYSIS — mifos-x-field-officer-app ⋈ kmp-project-template

> Produced by `/kmp-project-template-sync` **STEP 0.ANALYZE** (read-only).
> Generated: 2026-09-19 · Analyst: Claude (inline-opus)
> `$SRC` = `workspaces/mifos-x/mifos-x-field-officer-app/source/mifos-x-field-officer-app`
> `$TPL` = `workspaces/mifos-x/kmp-project-template/source/kmp-project-template`

---

## A — what this fork is

| | value |
|---|---|
| fork default branch | `dev` — **corrected 2026-09-19**; was reporting `development` from a framework fallback because `PROJECT_CONFIG.yaml` did not exist |
| `dev` head | `44d92532f` (2026-08-13) — local `dev` == `origin/dev` == `upstream/dev`, 0 divergence |
| open sync attempt | PR **#2704**, branch `session-mifos-x-field-officer-app-20260821174327158`, head `e60c74925` (2026-09-04), **25 commits / 2212 files / +134,238 −27,002** ahead of `dev` |
| `.template-version` | present **only on the PR branch** — `template_sha=6fe88bade`, `synced_at=2026-08-21T13:21:32Z` |
| `.template-version` on `dev` | **ABSENT** — `dev` has **no per-file merge base** against the template |
| template head | `template/dev` = `708da6e2e` (2026-09-18) |

`dev` already carries `core/`, `core-base/`, `cmp-navigation/`, `cmp-shared/` from the
`sync/template-bootstrap-2026-05-21` bootstrap — but has **no `customization-surface.yaml`**, **no
`scripts/white-label/`** (root `sync-dirs.sh` only) and **no `.template-version`**. It predates the
ownership contract entirely.

---

## A.1 — BASE SELECTION (the decisive finding)

Path-collision measured across the synced dirs (`core core-base cmp-* build-logic deployment scripts
tools app-profile sync`) for both candidate bases against `template/dev`:

| base | collide (reconcile) | fork-only (survives) | template-only (arrives free) |
|---|---:|---:|---:|
| **`dev`** (2026-08-13) | **134** — of which **39 already byte-identical → 95 real** | 1,400 | 1,760 |
| PR #2704 branch | **987** | 1,330 | 907 |

**Branching fresh from `dev` is ~10× less reconciliation work than continuing PR #2704.**

The cause is mechanical, not stylistic: PR #2704 *imported* the Aug-21 template's `core/`,
`core-base/`, `scripts/`, `deployment/` trees into the fork. Those files then aged a month, so every
one is now a three-way merge. On `dev` those same paths largely do not exist yet — so they simply
**arrive** instead of **conflicting**. The Aug-21 sync attempt made the migration harder, which is
the empirical reason it stalled.

---

## B — adoption plan, from the template's own migration ledger

`$TPL/template-migrations.yaml`, each row's `detect` run against `$SRC`:

| order | migration | blocking | state |
|---:|---|:---:|---|
| 10 | `whitelabel-engine-layout` | **yes** | **NOT ADOPTED** — root `sync-dirs.sh` still present ⇒ the fork runs a **stale engine** that can never self-update |
| 20 | `module-deps-seam` | **yes** | **NOT ADOPTED** — `MS-1`=12 modules, `MS-2`=7 modules with inline fork deps |
| 30 | `ksp-registration` | no¹ | **NOT ADOPTED** — `KS-1`=1, `KS-2`=3 |
| 40 | `template-first-ownership` | no² | **NOT ADOPTED** — fork carries the old module-scoped contract |
| 50 | `platform-shells-3way` | no | **NOT ADOPTED** |

¹ `blocking: false` **only because it cannot be pre-done** — the KSP processors arrive in `tools/`
with the sync. It is still destructive; it is enforced *inside* the sync branch. Not optional.
² the sync's own bootstrap performs it.

---

## C — the five structural detectors

| detector | verdict | reading |
|---|---|---|
| `sync-coverage-reconcile` | `CL-1`=12 · `CL-2`=376 · `CL-3`=0 | **TEMPLATE-side defects**, not fork blockers → enqueue upstream |
| `sync-module-scaffold-audit` | `MS-1`=12 · **`MS-2`=7** · `MS-3`=0 | **BLOCKING.** `build.gradle.kts` full-copy **DELETES** these inline deps |
| `sync-ksp-shell-audit` | `KS-1`=1 · `KS-2`=3 | sequence **inside** the sync branch (no `tools/` in fork yet) |
| `sync-puresync-divergence` | identical=657 · BEHIND=168 · **FORK-EDITED=37** · ORPHAN=229 | 37 fork edits sit in pure-sync areas → a full-copy destroys them |
| `sync-ownership-transition` | **hardening/upstream=3** · hardening/fork-only=96 · loosening/upstream=107 · loosening/fork-only=**1,253** | 3 BLOCKING; the 1,253 is a **CORRECTION, no action** |

### The 1,253 number explains the whole stall

`loosening / fork-only = 1253` is the new **package-scoped** contract correctly *releasing* Mifos code
that the old **module-scoped** contract wrongly claimed as template-owned. Under the fork's current
`core/** → owner: template` rule the engine cannot tell `com/mifos/core/model/Client.kt` from
`kpt/core/model/user/UserData.kt` — same module, so every sync looked like total war. The current
template replaced that with ~90 package-level rules (`core/model/**/kpt/core/model/economic/**`, …)
plus a template-first default. **Adopting migration 40 is the unlock.**

### MS-2 — the 7 modules whose deps a full-copy deletes

`core/ui` (11) · `core/common` (8) · `core/data` (6) · `core/domain` (6) · `core/designsystem` (5) ·
`core/database` (1) · `core/network` (1)

### OT — the 3 BLOCKING hardening/upstream files

- `core-base/common/src/androidMain/AndroidManifest.xml`
- `core-base/observability/src/androidMain/AndroidManifest.xml`
- `core/store/src/commonMain/kotlin/kpt/core/store/di/StoreModule.kt`

### PS-2 — 37 fork-edited files in pure-sync areas

8 are `core/*/build.gradle.kts` — **the same root cause as MS-2**; fixing the seam removes them.
17 are genuine framework edits needing a decision (seam · upstream PR · accept loss):
`core-base/designsystem` (10: `KptTheme`, `KptMaterialTheme`, `KptThemeExtensions`, `AppCard`,
`HeroCard`, `KptTopAppBar`, `KptShimmerLoadingBox`, `KptGrid`, `KptMasonryGrid`, `KptSidebarLayout`,
`KptSplitPane`) · `core-base/ui` (5: `DashboardProgressBar`, `IndependentCardLayout`, `DraftPicker`,
`DraftResolutionPrompt`, `ScreenContent`) · `core-base/store` (`StorePagingSource`) ·
`sync` (`DataSyncWorker`).
Remainder: `cmp-navigation/ComposeApp.kt`, `cmp-shared/build.gradle.kts`, `core/ui` bottombar ×2,
`core/store/di/StoreModule.kt`, `deployment/` ×4, `secrets/LAYOUT.yaml`, `CODE_OF_CONDUCT.md`.

---

## D — what the mechanical steps cannot see

1. **`feature/**` was never at risk.** 23 modules, 509 `.kt`, 88,368 lines, `owner: fork`. The sync
   never touches it. Any plan whose unit of work is "port features one by one" is doing work the
   contract already does for free.
2. **The domain layer was never at risk either.** 1,098 files in `com.mifos.*` / `com.mifos.room`
   under `core/`. The engine is **additive** — `sync-dirs.sh:781`: *"`git checkout $temp_branch --
   $dir` only ever OVERWRITES files present in $temp_branch"*. Fork-only files are not deleted.
3. **`dev` is 5 weeks stale relative to the PR.** The offline-first / Store5 work on the PR branch is
   real work that must be re-landed on top of the resync, not discarded. Sequence it *after*.
4. **Missing fork seams** — `settings.local.gradle.kts` (24 `include(":feature:*")` currently sit in
   the template-owned `settings.gradle.kts`, one sync from silent deletion), `feature-deps.gradle.kts`,
   `app-profile/`, `template-migrations.yaml`.
5. **Unmeasured:** compile health. Path collision ≠ build green. `core/database` vs
   `core-base/database` (189 `com.mifos.room` files vs the template's Room 3.1) is the most likely
   place for genuine surprise.

---

## E — upstream queue (RULE-TEMPLATE-MODULE-FIX-UPSTREAM-001)

Enqueue to `TEMPLATE_UPSTREAM_QUEUE.yaml`, never auto-open:
- `CL-1` ×12 — contract promises paths `SYNC_DIRS`/`SYNC_FILES` cannot reach (engine-defect)
- `CL-2` ×376 — engine reaches paths the contract calls fork-owned (missing `is_excluded` carve-out)
- any of the 17 `core-base` fork edits that are genuine improvements

---

## Verdict

Not a rewrite. **95 genuinely-differing files**, 5 declared migrations (2 blocking before the sync,
1 enforced inside it), 3 ownership-hardening files and 17 framework edits needing a decision —
starting from `dev`, not from PR #2704.
