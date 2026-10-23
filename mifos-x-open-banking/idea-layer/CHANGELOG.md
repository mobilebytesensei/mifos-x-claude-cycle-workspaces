# Idea Evolution Log — Mifos X Open Banking

> Tracks how the product idea evolves over time.
> Auto-updated by `/idea add`, `/idea enhance`, `/idea evolve`.

---

## 2026-10-22 — Cloudflare Worker BFF design locked (`/idea-plan-add`, goal hsbc-identity-cloudflare-bff)

- **What**:
  - Task **cloudflare-worker-bff** moved to in-progress and linked to the 8-phase plan.
  - New decision **TD-008**: a separate `workers.dev` Worker with a closed route table holds the whole TPP identity. It covers mTLS through a certificate binding, one non-extractable PS256 key, full id_token checks and PSU tokens in Durable Objects. The app gets an opaque session, plus Play Integrity or App Attest on mobile.
  - New requirements **FR-053** (identity server-side only), **FR-054** (id_token fully verified before the code exchange), **FR-055** (mobile attestation), **NFR-012** (under 10 ms p99 CPU on Workers Free), **NFR-013** (no key material in any build).
  - **consent-callback** now completes sign-in through `POST /v1/auth/complete`. The app no longer exchanges the code, inspects the id_token or stores HSBC tokens. New entity **BffSession**; **PsuTokens** move to the Worker.
  - Task **hsbc-sandbox-credentials** updated: all 7 HSBC secrets are in the vault and the local key copies are deleted.
- **Why**:
  - Every build shipped the full TPP identity (BLK-004), so anyone who unpacked a build could act as the TPP.
  - HSBC tokens are bound to the certificate, so once the certificate moves server-side the tokens have to move with it.
  - The id_token was only nonce-checked, which falls short of FAPI.
- **Impact**:
  - The requirements and technical_decisions sections need re-approval.
  - Phases 02 to 08 build the Worker and cut the app over.

---

## 2026-10-21 — consent-relay + Cloudflare hosting decision (`/idea-plan-add`)

- **What**:
  - New feature **consent-relay**: an open-source OAuth consent relay on Cloudflare Pages, in `relay/` of the app repo, on `*.pages.dev`. It replaces the personal GitHub Pages copy (obp-callback) and `docs/consent-callback-page/`.
  - New task **cloudflare-worker-bff**: moves the TPP keys off the device.
  - New requirements FR-050…052 and NFR-010/011.
  - New decision TD-007 (Cloudflare over Supabase, permanently) and blocker BLK-004 (keys ship in the app).
- **Why**:
  - Supabase Edge Functions can't serve the relay page, because they rewrite HTML to plain text.
  - Cloudflare covers the page, the App Links files and the future mTLS BFF on one domain.
  - A personal account must not control the registered redirect URI.
- **Impact**:
  - Sections requirements, features, screens, flows, api_surface, technical_decisions and deployment_plan need re-approval.
  - The public store release is gated on the BFF (BLK-004).

## 2026-10-21 — Plan approved

- **What**: All 15 sections approved (quality 92%). The prototype was healed to 0 gaps in 3 rounds (44/44 assertions).
- **Impact**: The plan is ready to promote (`/idea-plan --promote`).

## 2026-10-21 — Project created from source

- **What**: `/idea-plan --from-source https://github.com/openMF/mifos-x-open-banking`. The plan covers 25 features, 37 screens, 55 endpoints, 14 source defects and 3 release blockers.
- **Impact**: The idea-layer was created, with screen specs derived from the source.
