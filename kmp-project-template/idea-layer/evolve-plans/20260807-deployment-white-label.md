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

## Fix direction (bottom-up — extend the existing spine, never a parallel one)

1. **fork.properties schema** (SoT) — add: `store.description` (+ `store.{ios,android,macos}.description`),
   `store.ios.secondary.category`, `store.primary.locale` honored, contact/trade-rep keys, confirm windows/
   cloudflare keys. (Keys mostly already exist per the template audit §4.)
2. **`SyncForkConfigPlugin`** (generator) — add `writeIfPresent(...)` for: primary-locale metadata dir (G1/G5),
   `store.description` targets (G4), cloudflare `wrangler.toml`/`config.yaml` (G6), MS-Store appxmanifest (G6).
3. **vault-alias parameterization** (G2) — prefix from projectName; or `secrets-needs.yaml` → fork/merge in
   `customization-surface.yaml`.
4. **propagate enforcement** (G3/G7) — `scripts/product-health/` + `DEPLOYMENT_MANIFEST.yaml` + `PROMOTION_LOG.yaml`
   become part of the synced white-label deploy layer (extend `fork-identity.sh` TEMPLATE_DEFAULTS to catch
   `mifos-x-web`, `MifosInitiative.MoneyToolkit`, stale en-US store name, placeholder firebase/windows ids).
5. **media convention** (G8) — one canonical location, reconcile the two trees, drop the junk fastlane root.
6. **template owns linux/windows targets** (G7) so forks don't hand-add.

## Vehicle + how to promote

**INFRA rail** — driven by `/kmp-project-template-sync` + `/kmp-project-template-retrain` + a draft
fork→upstream PR (RULE-TEMPLATE-MODULE-FIX-UPSTREAM-001), NOT the product `/idea-agent` drive. Each fix is a
`build-logic`/`deployment`/`scripts` change on the template + a `customization-surface.yaml`/fork.properties
schema update. awaazly is the natural test-fixture consumer (`/kmp-project-template-sync` proves the sync).

---

## Capability Status  *(dashboard `--promote` targets; all `not-run` until promoted via the INFRA rail)*

| # | Capability | Rail | status |
|---|---|---|---|
| 1 | G1 iOS primary-locale metadata sync | infra · syncForkConfig | ○ not-run |
| 2 | G2 vault-alias parameterization | infra · customization-surface | ○ not-run |
| 3 | G3 propagate product-health drift gate to consumers | infra · retrain | ○ not-run |
| 4 | G4 `store.description` schema + generator | infra · fork.properties+plugin | ○ not-run |
| 5 | G5 locale parameterization | infra · syncForkConfig | ○ not-run |
| 6 | G6 contact/cloudflare/appxmanifest coverage | infra · syncForkConfig | ○ not-run |
| 7 | G7 manifest/promotion/health scaffold + linux/windows ownership | infra · sync-dirs+manifest | ○ not-run |
| 8 | G8 media convention + junk-root cleanup | infra · customization-surface | ○ not-run |

> **Review this plan, then promote (INFRA rail, not the product drive):** the deployment fixes flow via
> `/kmp-project-template-retrain propose` + `/kmp-project-template-sync` as upstream draft PRs. Do NOT
> `/idea-agent evolve --promote` this into the product pipeline (deployment has no idea-layer analog).
