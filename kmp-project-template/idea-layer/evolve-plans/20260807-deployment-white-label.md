# EVOLVE_PLAN — Deployment white-label (config-text · store-media · platform), sync-to-any-consumer

**Created:** 2026-08-07 · **Door:** `/idea-agent evolve` (plan-only default — this doc is the review gate) ·
**Intent:** *"Deep audit deployment/ of kmp-project-template and awaazly; make deployment project-level
config text, media/store data, and platform-wise deployment white-label + sync-able to any consumer."*
**Audited:** `kmp-project-template/deployment/` (template) + `awaazly/deployment/` (real consumer).

---

## Completability verdict: ⚠ PARTIAL — strong spine, 6 real gaps · **VEHICLE = INFRA rail, not product `/idea-agent`**

**Governance (read first).** Deployment is **INFRA** (`GOVERNANCE_LEDGER.yaml`): it has no idea-layer
screen/flow/DTO analog, so the product `/idea-agent` dispatch queue structurally cannot — and must not —
drive it. Promoting this plan **does NOT run the product pipeline**; it routes to the INFRA vehicle:
`fork.properties` (SoT) + `SyncForkConfigPlugin` (generator) + `customization-surface.yaml` (ownership) +
`DEPLOYMENT_MANIFEST.yaml`, delivered as a **draft fork→upstream PR** (RULE-TEMPLATE-MODULE-FIX-UPSTREAM-001)
and folded via `/kmp-project-template-retrain`. *(This is exactly why plan-only-is-default matters: an
auto-drive would have mis-routed deployment config into product screens.)*

**State:** the template already has ~80% of the white-label deployment spine working (fork.properties →
`syncForkConfig` → store-metadata text; `customization-surface.yaml` fork carve-outs; `fork-identity.sh`
gate). awaazly is a *mature but partially-drifted* adopter that proves the missing 20%. The gaps are
"the key exists but the generator doesn't write that target" + "the enforcement/orchestration half was
never propagated to consumers" — **extensions, not new infrastructure.**

---

## Traceability matrix — the three axes

| Axis | Template state | awaazly (consumer) reality | Gap |
|---|---|---|---|
| **Config text** | fork.properties SoT + `syncForkConfig` regenerate store `.txt` | schema-clean adopter; real drift (title, secondary-category) | G1 en-US locale unsynced · G4 no `store.description` · G5 no locale param · G6 no contact/trade-rep block |
| **Store media** | screenshots/og-images `owner: fork` (preserved, not generated), Mifos PNGs | media in fastlane `metadata/images/**` + `_over8_backup/` + per-desktop-res; template `screenshots/**` unused | G3 no single canonical media convention; duplicate fastlane metadata root fills with git-log junk |
| **Platform** | android/ios/mac/desktop/web targets; DEPLOYMENT_MANIFEST + PROMOTION_LOG | added linux/windows (19 vs 18 targets); **DROPPED** MANIFEST + PROMOTION_LOG + `product-health/` | G2 template-prefixed vault aliases · G7 manifest/health/promotion-log not propagated to consumers |

---

## Gaps (ordered by severity — the promote-ready work items)

- **G1 · HIGH · iOS primary-locale metadata never synced.** `SyncForkConfigPlugin` writes iOS/mac
  metadata to `en-GB` only, but `config.rb#primary_locale = en-US` → the 9 `ios/appstore/metadata/en-US/*.txt`
  (name="Mifos - Money Toolkit", description, promo, URLs) are template-owned AND not regenerated → a fork
  ships Mifos text in its primary locale. **Fix:** generator writes the `store.primary.locale` dir.
- **G2 · HIGH · vault aliases are template-name-prefixed + template-owned.** `android/{firebase,play-*}/
  secrets-needs.yaml` hardcode `alias: kmp-project-template-upload-keystore*` in `owner: template` files →
  a fork can't rename to `<fork>-*` without clobber-drift. **Fix:** parameterize the alias prefix from
  fork identity (projectName), or move `secrets-needs.yaml` → fork/merge ownership.
- **G3 · HIGH (config drift) · no synced-value↔on-disk drift gate on consumers.** awaazly's real title
  ("Awaazly: AI Voice to Text") + iOS secondary-category ("UTILITIES") are hand-tuned on disk but the
  matching fork.properties keys are stale/absent → next `syncForkConfig` reverts/blanks them. The gate that
  catches this (`product-health/{fork-identity,store-listing}.sh`) **exists in the template but was never
  shipped to awaazly.** **Fix:** propagate `scripts/product-health/` as part of the white-label deploy layer.
- **G4 · HIGH · no multi-line `store.description` surface.** The long store body — the single most important
  field — has no fork.properties key, forcing hand-authoring + drift (both template and awaazly).
  **Fix:** add `store.description` (+ per-platform overrides) to the fork.properties schema + generator.
- **G5 · MED · store locale hardcoded, not parameterized.** Generator ignores `store.primary.locale`
  (hardcodes en-GB iOS / en-US android). **Fix:** locale-driven metadata dirs.
- **G6 · MED · uncovered config-text: contact/trade-rep block, cloudflare project, MS-Store appxmanifest.**
  App-Store trade-representative fields + `web.cloudflare.project` (`mifos-x-web`) + `microsoft-store/
  Package.appxmanifest` (`MifosInitiative.MoneyToolkit`) are read-but-not-written / uncovered. **Fix:**
  extend `syncForkConfig writeIfPresent(...)` to these targets (keys already exist in fork.properties).
- **G7 · MED · manifest/promotion/health not scaffolded per-consumer + linux/windows not template-owned.**
  awaazly dropped `DEPLOYMENT_MANIFEST.yaml` + `PROMOTION_LOG.yaml` + `product-health/` while keeping the
  scripts that need them; and added linux/windows targets by hand. **Fix:** the white-label layer scaffolds
  + keeps the manifest/promotion/health trio for every consumer, and the template owns linux/windows targets.
- **G8 · LOW · media hygiene.** Kill the duplicate `deployment/fastlane/metadata/android/` root (git-log junk);
  reconcile ONE canonical screenshot convention (fastlane `metadata/images/**` vs template `screenshots/**`)
  incl. Play `>8` overflow + per-desktop-resolution buckets; media stays fork-owned + `/idea-store-assets-generate`.

---

## Architecture decision (LOCKED 2026-08-07): `app-profile/` — one per-platform fork-owned SoT

Supersedes the earlier "text in fork.properties + media in a separate dir" split. The whole-project
white-label data lives in ONE fork-owned module the deployment logic binds to:

```
app-profile/                     ← owner: fork · project-level SoT · sync NEVER rewrites
  app.yaml                       ← COMMON: identity, org, shared store text, media root
  platforms/
    android/  { android.yaml,  media/screenshots/{phone,sevenInch,tenInch}/ · feature-graphic/ }
    apple/    { apple.yaml (team_id·match·ASC contact·keywords·categories),
                ios/{ios.yaml, media/screenshots/{iPhone_6.9,iPad_13}/},
                macos/{macos.yaml, media/screenshots/} }
    web/      { web.yaml (cloudflare project·base url·og),  media/og-images/ }
    desktop/  { desktop.yaml (win msix·linux deb·categories), media/screenshots/{hd,qhd,fhd}/ }
  icons/                         ← shared icon source (platform icons derived by syncForkConfig)
```

- **Shared-once / override-per-platform:** `app.yaml` = identity/org + base title/description; each
  `platforms/<p>/<p>.yaml` holds only that store's differences (Android short-desc+changelog · Apple
  keywords+categories · web cloudflare · desktop msix/deb). No duplication. Media lives with its platform
  (collapses the G8 two-tree collision into one location).
- **`fork.properties` is KEPT but DEMOTED to a GENERATED build-bridge** (owner: generated). Gradle keeps
  its native `.properties` fast path at config time; a human NEVER edits it — `./gradlew syncForkConfig`
  DERIVES `fork.properties` + `libs.versions.toml#appId` + `Config.xcconfig` + metadata `.txt` FROM
  `app-profile/app.yaml`. One human SoT (yaml), zero build-path change.
- **Binding:** the fastlane lanes already go through `deployment/_shared/config.rb` (`ForkIdentity`,
  `TESTFLIGHT_CONFIG`, `APPSTORE_CONFIG`, `get_firebase_config`, `TESTERS`) → add ONE resolver
  `AppProfile.load` reading `app-profile/**` so every lane sources from it with no per-lane change.
- **Boundary (customization-surface.yaml):** `app-profile/** → owner: fork` (sync can't overwrite) ·
  `fork.properties`+catalog+metadata `.txt` → `owner: generated` (ignored) · `deployment/**` logic +
  `SyncForkConfigPlugin` + `scripts/product-health/**` → `owner: template` (COPIED EXACTLY by sync).

## Fix direction (bottom-up — build the `app-profile/` island, bind it, gate it)

1. **Scaffold `app-profile/`** — `app.yaml` + `platforms/*/` skeleton, migrated from the current
   `fork.properties` values; mark `owner: fork` in `customization-surface.yaml`.
2. **Bind the lanes** — add `AppProfile.load` to `deployment/_shared/config.rb`; every `config.rb` accessor
   sources from `app-profile/**` (identity, org, per-platform store text, distribution ids, media paths).
3. **`SyncForkConfigPlugin` reads `app.yaml`** — derive `fork.properties` (bridge) + catalog + xcconfig +
   metadata `.txt` (build artifacts, gitignored). Honor `store.primary.locale` (G1/G5); write long
   `description` (G4); cover cloudflare + MS-Store appxmanifest + contact/trade-rep (G6).
4. **NEW product-health gate `deployment-whitelabel.sh`** — verifies the boundary: `app-profile/` present +
   filled (no `YOUR_*`/placeholder), NO store-bound literal in any `owner: template` deployment file, no
   template-default identity (`mifos-x-web`, `MifosInitiative.MoneyToolkit`, stale en-US store name,
   `org.mifos.kmp.template`, placeholder firebase/windows ids) survives. Extends `fork-identity.sh`.
5. **vault-alias parameterization** (G2) — alias prefix from `app.yaml#identity.namespace`; or
   `secrets-needs.yaml` → fork/merge ownership.
6. **manifest/promotion/health scaffold + linux/windows ownership** (G7) — `DEPLOYMENT_MANIFEST` folds into
   `app.yaml#targets`; template owns linux/windows targets; scaffold kept per-consumer.
7. **media convention** (G8) — one `app-profile/platforms/<p>/media/**` location; drop the junk fastlane root.

## Vehicle + how to promote

**INFRA rail** — driven by `/kmp-project-template-sync` + `/kmp-project-template-retrain` + a draft
fork→upstream PR (RULE-TEMPLATE-MODULE-FIX-UPSTREAM-001), NOT the product `/idea-agent` drive. Each fix is a
`build-logic`/`deployment`/`scripts` change on the template + a `customization-surface.yaml`/fork.properties
schema update. awaazly is the natural test-fixture consumer (`/kmp-project-template-sync` proves the sync).

---

## Capability Status  *(dashboard `--promote` targets; all `not-run` until promoted via the INFRA rail)*

| # | Capability | Rail | status |
|---|---|---|---|
| 1 | **`app-profile/` scaffold** (`app.yaml` + `platforms/*`, migrated from fork.properties; owner:fork) | infra · customization-surface | ● done (promote 1, 2026-08-07 — 55/55 keys migrated, verified) |
| 2 | **Bind lanes** — `AppProfile.get` in `deployment/_shared/config.rb` (all lanes source from app-profile) | infra · config.rb | ● done (`_fork_prop`→AppProfile first; `ruby -c` + get() smoke ✓) |
| 3 | **`SyncForkConfigPlugin` reads `app.yaml`** → derive fork.properties/catalog/xcconfig/metadata; locale (G1/G5) + description (G4) + cloudflare/appxmanifest/contact (G6) | infra · build-logic | ◔ queued (CLOSES B2: cloudflare/appxmanifest still hardcoded until this) |
| 4 | **NEW `product-health/deployment-whitelabel.sh` gate** — boundary verified (G3) | infra · product-health | ● done (B1–B4; canary RED/GREEN ✓; auto-registered) |
| 5 | G2 vault-alias parameterization (prefix from `app.yaml#namespace`) | infra · customization-surface | ◔ queued |
| 6 | G7 manifest folds into `app.yaml#targets` + linux/windows template-owned + scaffold kept | infra · sync-dirs+manifest | ◔ queued |
| 7 | G8 one `app-profile/**/media` convention + drop junk fastlane root | infra · customization-surface | ◔ queued |

> **Review this plan, then promote (INFRA rail, not the product drive):** the deployment fixes flow via
> `/kmp-project-template-retrain propose` + `/kmp-project-template-sync` as upstream draft PRs. Do NOT
> `/idea-agent evolve --promote` this into the product pipeline (deployment has no idea-layer analog).
