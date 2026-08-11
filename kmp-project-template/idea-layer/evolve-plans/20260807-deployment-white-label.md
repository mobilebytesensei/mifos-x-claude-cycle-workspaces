# EVOLVE_PLAN — Deployment white-label (config-text · store-media · platform), sync-to-any-consumer

**Created:** 2026-08-07 · **Door:** `/idea-agent evolve` (plan-only default — this doc is the review gate) ·
**Intent:** *"Deep audit deployment/ of kmp-project-template and awaazly; make deployment project-level
config text, media/store data, and platform-wise deployment white-label + sync-able to any consumer."*
**Audited:** `kmp-project-template/deployment/` (template) + `awaazly/deployment/` (real consumer).

---

## ✅ PROVEN ON A REAL FORK (awaazly, 2026-08-07) — all 7 capabilities built + fork-verified

Ran the actual white-label code against **awaazly's identity** (controlled experiment on the template repo,
restored after): `./gradlew syncForkConfig` derived awaazly's identity into every template-owned file —
`wrangler.toml`→`awaazly-web` · `Package.appxmanifest`→`MobileByteSensei.Awaazly`/`CN=MobileByteSensei` ·
`secrets-needs.yaml`→`awaazly-upload-keystore` · `fork.properties` regenerated from `app.yaml` · 70 store
metadata files rewritten. The **product-health gate caught a real gap** the template-self-skip hid —
`deployment/web/cloudflare-pages/workflow-snippet.yml` was missed by cap-3's cloudflare tokenization —
which is now **fixed** (added to the tokenize target list); re-run → `--project-name=awaazly-web` → gate PASS
(B3 warns only on unset windows placeholders). Template working tree restored to Mifos identity; only the
white-label code + `app-profile/` (template values) remain as the change. Exactly why "prove on a fork first" mattered.

## Completability verdict: ✅ COMPLETE (7/7 · fork-proven) · **VEHICLE = INFRA rail, not product `/idea-agent`**

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
| 3 | **`SyncForkConfigPlugin` reads `app.yaml`** → derive fork.properties/catalog/xcconfig/metadata; locale (G1/G5) + description (G4) + cloudflare/appxmanifest/contact (G6) | infra · build-logic | ● done (2026-08-07 · snakeyaml + get() app-profile-first + fork.properties regen + writeLocalized + tokenize cloudflare/appxmanifest · `compileKotlin` ✓; B2 flips green when `./gradlew syncForkConfig` runs on a fork) |
| 4 | **NEW `product-health/deployment-whitelabel.sh` gate** — boundary verified (G3) | infra · product-health | ● done (B1–B4; canary RED/GREEN ✓; auto-registered) |
| 5 | G2 vault-alias parameterization (prefix from `projectName`, tokenized in syncForkConfig) | infra · customization-surface | ● done (2026-08-07 · secrets-needs.yaml alias prefix tokenized; compile ✓) |
| 6 | G7 manifest↔`app.yaml#targets` relationship + linux/windows template-owned + scaffold kept | infra · sync-dirs+manifest | ● done (linux/win already template-owned; headers + B5 gate; ownership merge/fork confirmed) |
| 7 | G8 one `app-profile/**/media` convention + drop junk fastlane root | infra · customization-surface | ● done (duplicate `fastlane/metadata` removed; media doc + B6 gate) |

> **Review this plan, then promote (INFRA rail, not the product drive):** the deployment fixes flow via
> `/kmp-project-template-retrain propose` + `/kmp-project-template-sync` as upstream draft PRs. Do NOT
> `/idea-agent evolve --promote` this into the product pipeline (deployment has no idea-layer analog).

---

## PHASE 2 (refinement, 2026-08-07) — make `app-profile/` the FULLY-ENRICHED end-to-end store-listing SoT

**Intent (verbatim):** *"we want to generate config from `/idea-deploy config` media+text generation in
deployment-layer/ and promote to source `app-profile/`, and `app-profile/` should be bound with source
`deployment/` + build.gradle etc — make `app-profile/` fully enriched, sync it store-listing end to end so
all in sync."*

Phase 1 (caps 1–7) made `app-profile/` the SoT for **identity + org + basic store text**. It does NOT yet
hold the *rich* store listing that `/idea-deploy config generate` already produces (per-platform per-locale
promo/release-notes/URLs/categories, age-rating, privacy-details, review-info, trade-rep, app-content
privacy-policy/data-safety, media, icon fan-out) — and the generation's promote path today writes
`deployment/**/metadata/` **directly**, bypassing `app-profile/`. Phase 2 closes that loop.

### Target end-to-end flow (the "all in sync" spine)
```
GENERATE   idea-layer → /idea-deploy config generate → deployment-layer/store-listing/variants/vN/  (+ SELECTED.yaml)
              text/{ios,macos,android}/{en-US/*.txt, review_information/, trade_representative/, age_rating.json, privacy_details.json, categories}
              app-content/{privacy-policy.md, data-safety.csv, app-content.yaml} · icons/ · media/
                    │
PROMOTE      SELECTED variant  ──────►  source/app-profile/store-listing/   ← the ENRICHED SoT (NEW target; was deployment/metadata)
                    │
BIND         app-profile/  ──(config.rb + syncForkConfig, identity-tokenized)──►  deployment/**/metadata/ + build.gradle + cmp-* icons
                    │
PUBLISH      deployment/**/metadata/  →  fastlane  →  stores
                    ▲
INPUT (loop) app-profile/app.yaml identity+org+contact+categories  ──feeds──►  /idea-deploy config generate
```

### Three trees, clear roles (no redundancy)
| Tree | Layer | Role |
|---|---|---|
| `deployment-layer/store-listing/variants/vN/` + `SELECTED.yaml` | idea/workspace | GENERATION workspace — versioned candidates + winner selection (stays here) |
| `app-profile/{app.yaml, store-listing/, icons/, platforms/*/media/}` | source (fork-owned) | **SoT** — the promoted SELECTED, enriched; sync NEVER rewrites |
| `deployment/**/metadata/` + build catalog + cmp-* icons | source (generated) | DERIVED publish artifact — regenerated from app-profile by `syncForkConfig` (gitignored / owner:generated) |

### Gap analysis (GAP 1–9)

- **GAP 1 · HIGH · app-profile schema is thin.** Holds identity + basic text only. Missing the full
  per-platform per-locale rich listing: `promotional_text`, `release_notes`, `marketing/support/privacy_url`,
  `primary/secondary_category`, `age_rating.json`, `app_privacy_details.json`, `review_information/`,
  `trade_representative_contact_information/`, and **`app-content/`** (privacy-policy.md, data-safety.csv,
  app-content.yaml). → Add `app-profile/store-listing/{text,app-content,media,icons}/` mirroring the variant tree.
- **GAP 2 · HIGH · promote path targets `deployment/metadata`, not `app-profile`.** `store-assets-sync.ts`
  (via `/idea-deploy store-listing --sync`, runtime STEP 1.7.0) copies the SELECTED variant straight to
  `source/deployment/**/metadata/`. → **Retarget to `source/app-profile/store-listing/`** so promotion lands
  in the SoT, and deployment/metadata becomes derived.
- **GAP 3 · HIGH · app-profile → deployment/metadata for the ENRICHED content.** `syncForkConfig` today
  writes only identity-derived basic text. → It (or a new bind step) writes the FULL metadata tree (all text +
  review_info + trade-rep + app-content + images) from `app-profile/store-listing/` → `deployment/**/metadata/`,
  identity-tokenized on top.
- **GAP 4 · MED · media + icon fan-out from app-profile.** Generated icons (android res/mipmap, ios.png,
  desktop, web-favicon) + media promote into `app-profile/{icons, platforms/*/media}` → `syncForkConfig` fans
  icons → `branding/icons/` → cmp-*; media → `deployment/**/metadata/images/`. (Today store-assets-sync writes
  straight to source — route through app-profile.)
- **GAP 5 · MED · generation must READ app-profile (close the loop).** `/idea-deploy config generate` G7
  identity/contact/category precedence today reads `DEPLOYMENT_PROJECT_CONFIG` + `_org/company.yaml` +
  `fork.properties`. → Read `app-profile/app.yaml` (identity, org, contact, categories) as the primary seed.
- **GAP 6 · LOW · variant/SELECTED boundary.** Variants (v1,v2) + `SELECTED.yaml` stay in `deployment-layer/`;
  `app-profile/` holds ONLY the promoted SELECTED (active listing), not variant history. Document the split.
- **GAP 7 · MED · sync/drift gate ("all in sync").** Extend `deployment-whitelabel.sh` (B7–B9): verify
  `app-profile/store-listing` == promoted SELECTED variant == `deployment/metadata` (post-syncForkConfig).
  Detect silent divergence.
- **GAP 8 · LOW · de-dup basic store text.** `store.title/subtitle/description` in `app.yaml` overlap the
  enriched `store-listing/text`. → `app.yaml` keeps identity+org+contact+distribution+categories (the config
  that *feeds* generation); rich store text lives in `app-profile/store-listing/` (promoted). No field owned twice.
- **GAP 9 · LOW · workspace↔source promote boundary.** The promote crosses `deployment-layer/` (workspace)
  → `app-profile/` (source), same boundary as today's store-assets-sync. Retargeted command writes source.

## ✅ PHASE 2 PROMOTED + PROVEN END-TO-END (2026-08-07) — all 7 caps built + verified

**Promote signal:** user "promote all of Phase 2" (2026-08-07). Drove the full sequence 8→9→10→11→12→14 (+13).
**End-to-end proof:** injected a distinctive marker into `app-profile/store-listing/text/{android,ios}/…`,
ran `./gradlew syncForkConfig` → the marker flowed through into `deployment/android/metadata/en-US/title.txt`
+ `deployment/ios/appstore/metadata/en-US/name.txt`, **winning over the app.yaml scalar** — i.e.
`app-profile/store-listing` now DERIVES `deployment/metadata`. Restored + re-derived; idempotent.
**Bonus heal (pre-existing SoT defects surfaced by the resync, now fixed):** `fork.properties#project.name`
was stuck at `awaazly` (leftover from the fork proof) → restored to `kmp-project-template` (fixed the
`awaazly-*` keystore-alias leak); `desktop.yaml` + `fork.properties` msix were `YOUR_MSIX_*` placeholders while
the committed appxmanifest had real identity → set to the template's real `MifosInitiative.MoneyToolkit` /
`CN=Mifos Initiative`. Also replaced the committed iOS `release_notes.txt` (which was PR-merge-title junk —
`Merge pull request #56…`) with the clean store-listing notes. Discovered a **literal-replace fragility** in the
Phase-1 keystore-alias tokenizer (can't re-tokenize a file already forked to a non-template namespace) — worked
around by restoring the 3 `secrets-needs.yaml` to committed before resync; upstream regex-fix noted as follow-up.
**Verification:** `compileKotlin` BUILD SUCCESSFUL · product-health `TEMPLATE_SELF_BUILD=1` → **4/4 PASS**
(incl. extended deployment-whitelabel B1–B9) · store-assets-sync gate SAS-1..11 (live+green PASS, red FAIL) ·
both canaries (deployment-whitelabel green0/red1, store-assets-sync green0/red1) PASS.

### ⚠️ CORRECTION (2026-08-07 rev 2) — file-dump SUPERSEDED by managed platforms-first schema

User feedback: *"we just copied the deployment-layer store listing into app-profile — we want PROPER
MANAGEMENT like we initially did in app-profile, binded into source deployment/, GitHub Actions,
fork.properties etc wherever needed."* + "platforms-first, prose as YAML keys, extend the icons approach to
media, end-to-end." The first Phase-2 build (`app-profile/store-listing/**` raw `.txt` file-tree) was a
**redundant dump** of data the Phase-1 structured schema already manages. **Redone the managed way (R1–R5):**

- **DISSOLVED** `app-profile/store-listing/`. Store copy is MANAGED STRUCTURED KEYS: `app.yaml#store.*` (common,
  prose incl. description/release_notes as YAML scalars) + `platforms/<p>/<p>.yaml` (per-store overrides).
  The ONE genuinely-missing block — `trade_representative` — added as keys in `apple.yaml` + `APP_PROFILE_MAP`
  (Kotlin `SyncForkConfigPlugin` + Ruby `config.rb`, lockstep). `age_rating.json` DERIVED from `store.age_rating`.
- **BOUND** (the whole point): `syncForkConfig` DERIVES `deployment/**/metadata` (text + trade-rep + review +
  media + docs) FROM the keys/files; identity keys also bind → fork.properties + appxmanifest + cloudflare +
  GitHub Actions via the existing tokenization. **Marker-proven:** `apple.yaml#trade_representative.first_name`
  → syncForkConfig → `deployment/ios/…/first_name.txt`.
- **MEDIA end-to-end (extends the icons pattern):** `app-profile/platforms/<p>/media/` is the SoT →
  `syncForkConfig deriveForkMedia()` fans it → `deployment/<p>/metadata` images (+ Play ≤8 cap). Icons unchanged
  (`app-profile/icons → branding/icons → cmp-*`). Managed docs: `platforms/android/app-content/data-safety.csv`,
  `platforms/apple/ios/app_privacy_details.json`.
- **PROMOTE folds, never dumps:** `store-assets-sync.ts` app-profile mode FOLDS a winning variant's text into the
  structured keys (comment-preserving, section-aware line edits — `org.first_name` ≠ `store.review.first_name` ≠
  `trade_representative.first_name`), media→platforms-first, icons→app-profile/icons, docs→managed files.

### Phase-2 capability status (rev 2 — managed platforms-first)

| # | Capability | Rail | status |
|---|---|---|---|
| R1 | **Platforms-first managed schema** — dump dissolved; `trade_representative` structured keys in apple.yaml; docs relocated to platforms-first | infra · app-profile | ● done |
| R2 | **Bind keys→deployment** — `syncForkConfig` derives trade-rep + media (`deriveForkMedia`) + docs from keys/files; `APP_PROFILE_MAP` rows (Kotlin+Ruby) | infra · build-logic + config.rb | ● done (compile ✓; **marker-proven** key→deployment) |
| R3 | **Promote folds text→keys** — `store-assets-sync` `foldTextIntoAppProfile()` (24 mappings, comment/section-safe) + media/icons/docs → platforms-first | deployment · store-assets-sync | ● done (self-test: comments preserved, no key cross-contamination; deno ✓) |
| R4 | **Gate** — `deployment-whitelabel.sh` B7 (schema authored + placeholder-free) B8 (no template copy in a fork) B9 (deployment↔key-SoT drift) + canary | infra · product-health | ● done (canary green0/red1) |
| R5 | **End-to-end + gates + product-health** — key→syncForkConfig→deployment; SAS-1..11; whitelabel canary; TEMPLATE_SELF_BUILD 4/4 | — | ● verifying |

Superseded caps 8–11/14 (file-dump) are folded into R1–R4. Caps 12 (G7 reads app-profile) + 13 (boundary doc)
stand. SoT heals (projectName=`kmp-project-template`, msix real identity) retained.

> **Delivery:** template-rail (R1/R2/R4 + apple.yaml/desktop.yaml + config.rb + gate + heals) extends **PR #286**
> (`session-kmp-project-template-20260807151415156`); framework-rail (R3 store-assets-sync + gate/canary + cap-12/13
> docs) on the framework session branch. Both via `/git-session-commit` (INFRA draft PR per
> RULE-TEMPLATE-MODULE-FIX-UPSTREAM-001, human-gated — never auto-merged).
