# Product Roadmap — Mifos X Open Banking

> **Last Updated**: 2026-10-21
> Managed by `/idea roadmap`. Read by `/gap-planning-project`. Mirrors `idea-plan.yaml#deployment_plan` (CalVer).

---

## Shipped (from source history)

| Version | Delivered |
|---------|-----------|
| 2026.5.x | Template sync, project customisation |
| 2026.6.x | App shell de-templating, OIDC sign-in |
| 2026.7.x | login, consent-callback, home, accounts |
| 2026.8.x | send-money, payments-schedule-payment, payments-standing-order, vrp |
| 2026.9.x | settings (theme picker, licences) |

---

## 2026.11.0 — Release readiness

**Status**: ⏳ Planned | **Target**: — | **Order** (each step gates the next):

1. BLK-001 — rotate the Android upload keystore, move signing secrets to the vault (human step)
2. High-severity defects DEF-001…004 + **consent-relay on Cloudflare Pages** (HSBC redirect URI re-registered)
3. FR-046…049 — sign-out, manage-consents link, Accounts / Payments Hub reachable, AIS 401/403 routing
4. BLK-002 branding + BLK-003 store listing + about/legal screens
5. iOS build + sandbox verification
6. First store release — **gated by BLK-004**

### Features

| Feature | FR Coverage | Designed | Impl | Tests |
|---------|:----------:|:--------:|:----:|:-----:|
| consent-relay | FR-050–052 | — | — | tests.yaml (Playwright) |
| accounts, payments-hub (reachability) | FR-048 | — | ✅ (unreachable) | — |
| settings (sign-out) | FR-046 | — | ⚠️ | — |
| payment forms (manage consents) | FR-047 | — | ⚠️ | — |

### Known Issues

- **BLK-004 (critical):** TPP private keys ship inside the app. A *public* store release needs the Cloudflare Worker bank gateway first. **Decision pending:** pull the bank gateway into 2026.11.0, or keep 2026.11.0 a sandbox / internal-testing release.

---

## 2027.1 — Platform reach

**Status**: ❌ Proposed

- **Cloudflare Worker bank gateway** (task `cloudflare-bank-gateway`, TD-008, NFR-010/012/013, FR-053…055) — keys off device, unblocks web. **🚧 In progress since 2026-10-22** as goal `hsbc-identity-bank-gateway` (8 phases: idea-layer → deploy + spike → Worker core → AIS + auth → PIS + VRP → attestation → app cutover → docs + end-to-end). Once it lands, BLK-004 is resolved and the 2026.11.0 release-order question goes away.
- Config-driven ASPSP + multi-ASPSP (TD-004), user-selectable AIS scope
- Shared payment form module (TD-003)
- Medium/low defects DEF-005…014
- atm-locator (deferred route)
