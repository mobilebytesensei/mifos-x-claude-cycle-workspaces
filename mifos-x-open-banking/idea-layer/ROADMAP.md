# mifos-x-open-banking — Roadmap

> **Empty-slate state** — feature roadmap is pending product-scope definition.
> Only architectural / infrastructure milestones are listed.

## v0.1 — Empty-slate Scaffold

**Status**: complete · completed: 2026-05-22

Goal: post-template-sync infrastructure is clean and consistent; product scope is ready to be defined on top.

- [x] Replace source tree with latest `kmp-project-template` (Stream-First architecture)
- [x] Update PROJECT.md + PROJECT_CONFIG.yaml to reflect actual source state
- [x] Scaffold idea-layer foundation docs (IDEA, FEATURES, REQUIREMENTS, ROADMAP, CHANGELOG, LAYER_STATUS)
- [x] Bootstrap design-system (`design-tokens.yaml`, `DESIGN.md`, `COMPONENTS.md`, `app-shell.yaml`)
- [x] Run `/idea verify` to surface remaining gaps
- [x] Remove template residue from source: `feature/{crypto,currency-rates,emi-calculator}` modules
- [x] Remove corresponding `idea-layer/screens/{crypto,currency-rates,emi-calculator}/` directories
- [x] Remove template residue from `core/data` (CryptoRepository, CurrencyRatesRepository) and `core/database` entities
- [x] Update settings.gradle.kts and root build.gradle.kts to drop excluded modules
- [x] Re-run `/idea sync` → 0 verify failures

## v0.2 — Product Scope Definition

**Status**: complete · completed: 2026-05-27

Goal: define the actual open-banking product roster.

- [x] Run `/idea-plan` to draft product vision (problem, target users, key flows)
- [x] Run `/idea add` for each declared feature
- [x] Run `/idea-enrich` per feature to produce SPEC/MOCKUP/PROMPTS
- [x] Review with stakeholders → `/idea approve`

39 features defined · 3 personas · 6-phase 16-week release plan · all sections approved at quality ≥85%.

> **Superseded 2026-08-02.** The roster is now 26 features and a single consumer persona.
> See the scope change below.

## v0.3.0 — Consumer-only scope reset

**Status**: complete · completed: 2026-08-02

Milestone: the product is a consumer-only Open Banking app.

The field-officer persona was removed in full — 12 screens (`fo-dashboard`,
`customer-search`, `customer-detail`, `customer-profile`, `customer-onboarding`,
`corporate-onboarding`, `kyc-review`, `account-applications`, `application-detail`,
`customer-messages`, `meetings`, `agent-registration`), `flows/field-officer.yaml`,
3 `fo-*` journeys, 7 API groups and 10 DTOs. PFM went with it: `pfm-dashboard`,
`pfm-settings` and `business-insights`.

There is no `fieldOfficer` product flavor and no flavor-aware navigation.

## v0.4.0 — Feature Complete

**Status**: pending · target: W15

Milestone: the consumer roster ships; iOS + Web (Wasm) builds passing.

Features: `standing-orders`, `standing-order-detail`, `direct-debits`, `direct-debit-detail`,
`atm-locator`, `branch-locator`, `consent-manager`, `notifications`, `products`

> **Corrected 2026-08-07.** This list named three screens deleted in the 2026-08-06 OBIE
> migration:
> `standing-order-edit` (a PISP may not amend or cancel a standing order — OBL Customer
> Experience Guidelines), `transaction-tags` (an OBP v1.2.1 metadata API with no OBIE
> counterpart) and `fx-rates` (OBIE exposes no FX rate endpoint, so the screen had no data
> source at all). None can be built, so none can be a Feature-Complete exit criterion.
>
> **Updated 2026-08-07.** `branch-locator` added — HSBC UK Branch Locator, Open Data on
> `api.hsbc.com`, unauthenticated. `products` here means the HSBC UK **Product Finder**
> catalogue (four families: personal-current-accounts, business-current-accounts,
> unsecured-sme-loans, commercial-credit-cards), not the per-account `product` terms screen,
> which already ships.
>
> **Also 2026-08-07.** `cards` and `card-detail` were deleted outright (roster 44 → 42), decided
> by the repository owner. Neither appeared in this milestone's Features list, so nothing is
> removed from it here — the note is recorded so the roster count reconciles. OBIE has no card
> resource: a card is an `Account` with `SchemeName == UK.OBIE.PAN`. The
> **commercial-credit-cards** family named above is the Open Data Product Finder catalogue, a
> different resource on a different host, and is unaffected.

`atm-locator` is specified but not yet built — `AtmLocatorRoute` currently resolves to a
placeholder screen. Its idea-layer spec, exports, mockups, `atm` API group and 7 DTOs are
retained as the input to `/implement`.

`branch-locator` is newer (2026-08-07) and is spec-only: `screens/branch-locator/` exists, but it
has no `exports/` or `mockups/` entry yet. It needs `/idea-feature-export` before `/implement`.

PISP payment initiation — the payments hub and the seven per-type rails — is phased separately
as P3–P5 in `IDEA.md#feature-roadmap` and `idea-plan.yaml#release_phases`, and is not folded into
this milestone.

Platforms: Android · iOS · Desktop · Web

## v1.0.0 — Production Release

**Status**: pending · target: W16

Milestone: all platforms pass smoke tests; release artifacts signed and ready.

- [ ] End-to-end testing on all platforms
- [ ] Performance profiling (startup, scrolling, API latency)
- [ ] Security audit (token storage, certificate pinning)
- [ ] Release builds (signed APK/AAB, IPA, Desktop installers, Wasm)
- [ ] Store metadata + screenshots

Platforms: Android · iOS · Desktop · Web
Artifacts: apk, aab, ipa, exe, msi, dmg, deb, wasm

---

## Constraints (architecture-level, apply across all future work)

- Stream-First architecture (BaseViewModel + ScreenDataStream + Store5) — NO regression to MVI
- 4-platform parity (Android · iOS · Desktop · Web) — every feature ships on all 4
- Material 3 design system (light + dark) — brand-primary `#4C662B`
- WCAG AA accessibility — non-negotiable for production release

## Deferred / Future

To be populated post-v1.0 (biometric auth, real-time push notifications, production bank OAuth setup).
