# client-layer

> Last updated: 2026-05-28 (auto-populated by /project-verify)

| Attribute | Value |
|---|---|
| **Maturity** | bootstrap |
| **Status** | scaffold only — no repository implementations yet |
| **Tech** | Ktor 3.2.0 + Ktorfit 2.5.2 + Store5 |
| **Next** | Run `/client {feature}` to wire Ktorfit service + Store5 repository per feature |

## Notes

- `LAYER_GUIDE.md` present with Ktorfit + Store5 patterns
- No feature-specific client files yet — awaiting `/kmp-implement` per feature
- Backend: HSBC UK Open Banking — OBIE Read/Write API (`secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/{aisp|pisp}`) — `api_version: v4.0`; Open Data v2.2 unauthenticated on `api.hsbc.com`. Auth is mTLS + `private_key_jwt` (PS256) + OAuth authorization-code (FAPI 1.0 Advanced)
