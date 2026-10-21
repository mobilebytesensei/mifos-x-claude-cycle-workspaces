# server-layer

> Last updated: 2026-05-28 (auto-populated by /project-verify)

| Attribute | Value |
|---|---|
| **Maturity** | bootstrap |
| **Status** | API manifest present in idea-layer/server/; no server-layer endpoint docs yet |
| **Backend** | HSBC UK Open Banking — OBIE Read/Write API v4.0 (`https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/{aisp\|pisp}/…`); Open Data v2.2 unauthenticated on `https://api.hsbc.com` |
| **Auth** | mTLS + `private_key_jwt` (PS256) client authentication + OAuth 2.0 authorization-code (FAPI 1.0 Advanced) — authorize `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`, token `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/token` |
| **Next** | Run `/server scan` to generate Ktorfit interface stubs from idea-layer/server/apis/ |

## Notes

- `idea-layer/server/api_manifest.yaml` + `idea-layer/server/apis/` contain OBIE Read/Write v4.0 API contracts
- No Ktorfit interface files in `server-layer/` yet — awaiting `/server` command execution
- `LAYER_GUIDE.md` present with OBIE + Ktorfit patterns
- Firebase observability (Crashlytics + Performance) wired separately in source
