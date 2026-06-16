# Current Work

**Last Updated**: 2026-06-15
**Active Project**: mifos-x/kmp-project-template
**Branches**: framework=`claude-session-mbs-20260606` · workspace=`claude-session-mifos-x-20260523` · source=`feat/kmp-secrets-setup-skill`

---

## Session Resumption

This session landed the **fastlane-modernization release/promote axis** end-to-end. Reframed CURRENT_WORK's prior "macOS Keychain rewrite" thread after the user clarified: the issue was macOS **desktop deployment** using a custom bash script, not secret intake. Rewrote `deployment/desktop/dmg-notarized/` to full Fastlane (Match-managed Developer ID + native `notarize` action), then designed + implemented a 3-stage promotion ladder across every platform with explicit `action × target_stage` semantics in both GHA workflows and the `/release` runtime.

None committed by Claude (per HR #1). Pick up by deciding commit boundaries.

---

## Promotion ladder design (the model now baked in)

Uniform 3-stage ladder across every platform, plus out-of-band Stage 0:

| Stage | Semantics | Apple | Google | Direct distribution |
|---|---|---|---|---|
| **0 · firebase** | Out-of-band dev/QA. | Firebase | Firebase | — |
| **1 · internal** | Instant, team-only. | TF Internal | Play Internal | GH Release `prerelease=true` |
| **2 · beta** | External pre-release. Review-gated. | TF External (~24h beta review) | Play Open Beta | GH Release `latest=false`, not prerelease |
| **3 · production** | Public. Review-gated. | App Store / Mac App Store | Play Production (staged rollout) | GH Release `latest=true` |

Two-axis input model for every workflow + `/release` invocation:

- **`action: release | promote | firebase`**
  - `release` = build + ship to specified stage
  - `promote` = move existing build to next rung (no rebuild — Play track-promote, TestFlight distribute_only, GH Release flip)
  - `firebase` = Stage 0 (Android/iOS only)
- **`target_stage: internal | beta | production`** = where the run lands

Invalid combos rejected at the workflow's `validate` job. Production-stage actions gated by `confirm: CONFIRM`.

### Lane mapping (the matrix)

| Platform | action=firebase | release+internal | release+beta | release+production | promote+beta | promote+production |
|---|---|---|---|---|---|---|
| **android** | `deployReleaseApkOnFirebase` | `deployInternal` | ❌ | ❌ (force staged) | `promoteToBeta` | `promote_to_production` |
| **ios** | `deploy_on_firebase` | `beta` (TF upload) | ❌ | `release` (full rebuild) | `promoteToExternalBeta` | `promoteToAppStore` |
| **mac (mas)** | — | `desktop_testflight` | ❌ | `desktop_release` | `promoteMacToExternalBeta` | `promoteMacToAppStore` |
| **mac (dmg)** | — | `buildNotarizedMacDmg` STAGE=prerelease | STAGE=beta | STAGE=stable | `gh-release-stage.sh` STAGE=beta | `gh-release-stage.sh` STAGE=stable |
| **desktop** | — | `script.sh` STAGE=prerelease | STAGE=beta | STAGE=stable | `gh-release-stage.sh` STAGE=beta | `gh-release-stage.sh` STAGE=stable |
| **web** | — | `gh-pages-preview` | `gh-pages-staging` | `gh-pages` | push preview→staging | push staging→gh-pages |

---

## What landed (Source: `feat/kmp-secrets-setup-skill`)

### `deployment/desktop/dmg-notarized/` — custom bash → full Fastlane
- **NEW** `lane.rb` (~250 lines) — `match(type: "developer_id", platform: "macos")` + `notarize(...)` action + Match-managed Developer ID cert
- **DELETED** `script.sh` (was 40 lines of `xcrun notarytool` + `security import` + `gh release upload`)
- `secrets-needs.yaml` collapsed 6 → 5 aliases (Match owns the .p12 — `DEVELOPER_ID_CERT_B64` + `DEVELOPER_ID_CERT_PASSWORD` + `DEVELOPER_ID_NAME` GitHub secrets disappear)
- `workflow-snippet.yml` simplified (no manual keychain-import step)
- `config.yaml` runner switches to Fastlane invocation; adds `dev_fallback.command` for `AD_HOC_SIGNING=1`
- `README.md` documents one-time Match seeding: `bundle exec fastlane match developer_id --platform macos`

### 3 lane gaps closed (Fastlane Ruby)
- `promoteToExternalBeta` (iOS) — Stage 1 → Stage 2 via `pilot(distribute_only: true)`
- `promoteMacToExternalBeta` (macOS MAS) — same pattern, `app_platform: "osx"`
- `--stage` flag on `buildNotarizedMacDmg` — controls GH Release `prerelease` + `latest` flags via shared helper

### Shared bash helper
- **NEW** `deployment/_shared/scripts/gh-release-stage.sh` — single source of truth for prerelease/latest mapping (used by Fastlane lanes + 4 desktop bash scripts)

### Direct-distribution scripts uniformly support `STAGE` env
- `windows-exe/script.sh`, `msi-signed/script.sh`, `linux-deb/script.sh` — `STAGE=prerelease|beta|stable` post-upload flag flip
- `macos-dmg-unsigned/lane.rb` — same support via the helper

### 6 NEW GitHub Actions workflows (action × target_stage axis)
- `.github/workflows/release.yml` — top-level dispatcher
- `release-android.yml` — action + target_stage; lane resolved in `validate` job
- `release-ios.yml` — same shape
- `release-mac.yml` — adds `channel: mas | dmg`; dmg promote = no-rebuild GH Release flag flip
- `release-desktop.yml` — adds `target: windows-exe | msi-signed | linux-deb`; release vs promote branches `script.sh` vs `gh-release-stage.sh`
- `release-web.yml` — release deploys gh-pages-{preview,staging,production}; promote copies one branch → next

Every child workflow has a `validate` job that maps `(action, target_stage)` → Fastlane lane name and rejects invalid combos with a clear `::error::`. Production-stage actions gated by `inputs.confirm == 'CONFIRM'`.

### 4 NEW GHA helper scripts
- `_shared/scripts/promotion-log-append.sh` — appends 12-field row to `deployment/PROMOTION_LOG.yaml` per RULE-DEPLOYMENT-MANIFEST-001 DM6
- `_shared/scripts/materialize-{android,ios,mac}-secrets.sh` — manual-mode (no vault) materialization helpers

### Legacy reconciliation
- `multi-platform-build-and-publish.yml` kept as-is (still works via `openMF/mifos-x-actionhub@v1.0.11`); added a header comment pointing at the new `release.yml` for ladder-aware promotion. Not deprecated.

---

## What landed (Framework: `claude-session-mbs-20260606`)

### `layers/project/commands/release-status.md` extended
- New input: `deployment/PROMOTION_LOG.yaml`
- New CLI flag: `--rungs`
- New STEP 1.5: parse deploy log → per-(platform, lane, stage) `rung_matrix`
- New STEP 5: renders the Per-Platform Rung Matrix below the existing release table; stage-inference rules per lane name encoded
- JSON schema gains `rung_matrix` field

---

## Validation status

- `ruby -c` on every touched `*.rb` → OK
- `bash -n` on every touched `*.sh` (and chmod +x on the 5 new ones) → OK
- `YAML.safe_load` on all 6 new workflows → OK
- No automated runtime test — first real GHA fire will exercise the validate→dispatch chain

---

## Next Session

1. **Decide source-repo churn fate**: the prior orphaned `deployment/**` + `cmp-ios/*` + screenshot deletions on this branch — keep / stash / discard. The new fastlane-modernization work piled on top is clean and worth keeping regardless.
2. **One-time Match seeding** (before any CI dispatch with `mac dmg`): `(cd deployment && bundle exec fastlane match developer_id --platform macos)` from a maintainer machine.
3. **Commit boundaries**:
   - Source: scoped to `feat/kmp-secrets-setup-skill` — `/git-session-commit --source`
   - Workspace: submodule pointer bump after source PR lands
   - Framework: the `release-status.md` runtime edit + the broader idea-agent sub-plan B–E + auto-heal recipe pivot edits — `/git-session-commit --framework`
4. **Wire `/release` slash command** to the new GHA inputs — the framework-level `release.md` runtime already documents the CLI signature; verify it dispatches `gh workflow run release.yml -f platform=... -f action=... -f target_stage=...` correctly.

---

## Project Summary

- **Imported From**: https://github.com/openMF/kmp-project-template
- **Features**: 3 (home, profile, settings)
- **Platforms**: android, ios, desktop, web
- **Core Modules**: 10
