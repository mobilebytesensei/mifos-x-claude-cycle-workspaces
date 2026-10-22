# Product Idea — Mifos X Open Banking

> **Version**: 1.0
> **Last Updated**: 2026-10-21
> **Status**: Active (source-derived from openMF/mifos-x-open-banking @ d5c6782)

---

## Vision Statement

One Kotlin Multiplatform codebase that acts as a UK Open Banking TPP — see every account and initiate single, scheduled, standing-order and VRP payments against the HSBC UK sandbox with FAPI-grade security.

## Problem

Banks and fintechs in the Mifos/Fineract ecosystem have no open-source, production-shaped reference for building a UK Open Banking (OBIE v4.0) TPP app. mTLS client certificates, `private_key_jwt` token auth, OIDC hybrid-flow consent redirects across mobile and desktop, detached-JWS payment signing and idempotent submission must otherwise be rebuilt from scratch on every platform.

## Solution

A Compose Multiplatform app with one shared networking core (`Aisp`, `Pisp`, `Vrp`, `OAuth`) and a Store5/Room data layer running the full consent lifecycle: client-credentials token → create consent → PS256-signed authorize URL → PSU authorises in the browser → an HTTPS relay page hands the fragment back (custom scheme on mobile, loopback on desktop) → validate state/nonce → exchange the code → read accounts or submit the payment.

---

## Target Users

| Persona | Role | Primary Need | Key Workflow |
|---------|------|-------------|-------------|
| Priya the PSU | HSBC UK personal account holder using a third-party money app | See all balances in one place and pay without opening the bank app | Connect bank → Home → send / schedule / standing order / VRP → receipt |
| Dev the TPP integrator | Fintech or bank developer forking the reference client | Working sandbox app with their own certs in under an hour | Supply client_id, kid, SSA, certs → host relay page → first sandbox call |
| Mifos institution product owner | Product lead at a Mifos/Fineract-powered institution | Evaluate Open Banking AIS/PIS as a member capability | Demo the end-to-end consent + payment experience |
| Sam the security/compliance reviewer | Security engineer or compliance officer auditing the TPP | Evidence that FAPI controls, consent handling and secret hygiene hold | Review FAPI controls → consent revoke at ASPSP → secrets in vault |

---

## Core Value Propositions

1. One codebase for AIS + PIS on Android, iOS and desktop, with FAPI security (mTLS, private_key_jwt, signed request objects, detached JWS) built in.
2. Complete consent lifecycle: create, authorise via the browser relay, callback, status poll, renew and revoke.
3. Every OBIE PIS product — domestic and international single, scheduled and standing-order payments — plus domestic VRP.
4. Unified account view: balances, paginated transactions, statements with PDF/CSV download, standing orders, direct debits, beneficiaries, product and party.
5. Fork-friendly: credentials and certs are per developer, git-ignored, and config is generated from `local.properties`.

**Differentiator:** open-source (MPL-2.0), client-only, no aggregator in the money path. Unlike TrueLayer, Yapily, Tink or Plaid, the integrator holds the certificates and talks to the ASPSP directly.

**Regulatory frame:** PSD2 + RTS on SCA · UK Open Banking Read/Write API v4.0 · OpenID FAPI 1.0 Advanced · FCA AISP/PISP permissions (production only).

---

## Platform & Technology

| Attribute | Value |
|-----------|-------|
| Platforms | Android, iOS (experimental, unverified), Desktop (JVM), Web (UI shell only — no bank connectivity) |
| Backend | None first-party — HSBC UK Open Banking sandbox (OBIE Read/Write v4.0, OAuth2/OIDC v1.1) |
| Project Type | kmp (fork of kmp-project-template) |
| Stack | Kotlin 2.3.20 · Compose Multiplatform 1.10.3 · Koin 4.1.1 · Ktor 3.3.3 + Ktorfit · Store5 + Room 3 · navigation-compose |
| License | MPL-2.0 (CLA required) |

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| AIS consent completion rate | ≥ 95% of started consents land on Home with accounts | consent-callback success vs. Login StartOAuth |
| Payment submission success after authorisation | ≥ 95% | payment-consent → payment-status accepted |
| Duplicate payment writes | 0 | idempotency key + single-use PendingAuth; redirect dedupe |
| Fork-to-first-call time | < 1 hour | developer onboarding walkthrough |
| Platform parity | Android + desktop + iOS verified each release | device / desktop smoke run against the sandbox |
| Crash-free sessions | ≥ 99.5% | Crashlytics |

---

## Constraints & Assumptions

### Technical Constraints
- mTLS on every bank call; PS256 `private_key_jwt` client authentication.
- OIDC hybrid flow (`code id_token`) returns in the URL fragment, so an HTTPS relay page (`docs/consent-callback-page`) is required.
- Redirect scheme `org.mifosx.openbanking` and desktop loopback port 8765 are duplicated across bridge.js, AndroidManifest, Info.plist, cmp-shared and cmp-desktop.
- PIS/VRP writes need a detached JWS (`x-jws-signature`) and an `x-idempotency-key` of at most 40 characters.
- Secrets flow via `local.properties` → `:core:network:generateHsbcConfig`; blank secrets fail at client construction.

### Business Constraints
- Sandbox only — production requires FCA authorisation and OB/eIDAS certificates.
- MPL-2.0; contributions need a signed CLA.
- PSD2 / UK Open Banking: AIS consent capped at 90-day expiry and 90-day history.

### Assumptions
- Each developer registers their own HSBC sandbox TPP and hosts their own relay page.
- The sandbox accepts PISP calls without `x-fapi-financial-id`.

---

## Known Limitations

- iOS mTLS is implemented but has never been built or verified on a Mac (planned for v2026.11.0).
- Web targets cannot reach the bank (a browser cannot present an mTLS client certificate); statement download on web is a no-op.
- Single ASPSP: hosts and paths are hardcoded to `/obie/open-banking`, and the authorize path appears in five repositories.
- AIS consent always requests every permission (`OBPermission.ALL`) — no user choice of scope.
- `x-fapi-financial-id` is hardcoded blank and will fail on production ASPSPs.
- **Release blocker:** Android upload-keystore passwords are committed in `fastlane-config/project_config.rb` — rotate and move to the vault before any store release.
- **Release blocker (BLK-004):** the TPP's private keys ship inside every app build — a public release needs the Cloudflare Worker BFF first (NFR-010).

---

## Scope Boundaries

### In Scope
- AIS: account-access-consents CRUD; accounts, balances, transactions (Links.Next paging), statements (+detail, +transactions, +file), standing orders, scheduled payments, direct debits, beneficiaries, product, party.
- PIS: domestic and international single, scheduled and standing-order consents, funds confirmation, submit and receipt.
- VRP: domestic-vrp-consents create/get/delete, funds confirmation, domestic-vrps submit/get.
- Consent management: list, detail, renew via LoginRenew, revoke (logs out).
- Local payment history per product; settings (theme, licences, consents).

### Out of Scope
- Web bank connectivity.
- In-app Dynamic Client Registration (done out-of-band on HSBC DevHub).
- Multi-ASPSP selection.
- Cards, PFM insights, FX, ATM locator, change/forgot password, ToS/privacy (placeholder routes today).
- CBPII confirmation-of-funds API, file payments, event notifications.

---

## Ideas Backlog

> Add ideas with `/idea add "description"`. Claude structures them into requirements.

| # | Idea | From | Priority | Status | Added |
|:-:|------|------|:--------:|:------:|:-----:|
| 1 | Sign out from Settings (FR-046) | source analysis | should | planned | 2026-10-21 |
| 2 | Wire "Manage consents" in payment flows to ConsentList (FR-047) | source analysis | should | planned | 2026-10-21 |
| 3 | Make Accounts and Payments Hub reachable (bottom-nav tabs or Home entry points) | source analysis | should | planned | 2026-10-21 |
| 4 | User-selectable AIS permission scope instead of OBPermission.ALL | source analysis | could | idea | 2026-10-21 |
| 5 | Multi-ASPSP support (configurable bank hosts/paths) | source analysis | could | idea | 2026-10-21 |
| 6 | **consent-relay** — open-source OAuth consent relay on Cloudflare Pages (`relay/` in the app repo, `*.pages.dev`), hardened headers, history scrub, App Links / Universal Links; replaces the personal GitHub Pages copy | user | must | planned (2026.11.0) | 2026-10-21 |
| 7 | **Cloudflare Worker BFF** — TPP keys off the device (mTLS binding + Workers secrets); unblocks a public store release (BLK-004) and web | user | must for public release | planned (2027.1, release-order decision pending) | 2026-10-21 |

### Hosting decision (2026-10-21)

Cloudflare, permanently: Pages for the relay, a Worker for the BFF, one domain. Not Supabase, because Edge Functions rewrite HTML to plain text and can't serve the relay page. Both are open source under openMF; secrets live only in Cloudflare secrets, mTLS bindings and the vault.
