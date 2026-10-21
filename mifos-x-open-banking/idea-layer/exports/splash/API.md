# API — Splash Screen

**No backend API dependencies.** `api.yaml` declares no operations, and no HTTP request is issued
from this screen.

---

## Session resolution is local

The splash screen renders while `RootNavViewModel` resolves the session from the persisted token in
local storage. It does not perform that resolution itself — it has no DI, no actions and no events.

| Scenario                       | Resolution                                | Navigate to    | Delay    |
|--------------------------------|-------------------------------------------|----------------|----------|
| No stored token                | `hasValidToken = false`                   | login          | 2 000 ms |
| Valid token                    | `hasValidToken = true`                    | home           | 0 ms     |
| Expired token (refresh needed) | `ObpAuthRepository.refreshToken()` called | login on fail  | —        |

The 2-second delay on the no-token path is deliberate: it is the only case where the splash is shown
for its own sake rather than covering work, and it gives the brand moment somewhere to land before
the customer is asked to connect a bank.

**Role does not participate in session resolution.** A `FIELD_OFFICER` branch routing to
`fo-dashboard` existed in an earlier revision; no such screen exists and the project has been
consumer-only single-flavor since 2026-08-02.

For the authentication endpoints themselves, see `idea-layer/exports/login/API.md` — the consent
creation and FAPI redirect happen there, not here.

---

<!--
Regenerated 2026-08-04 by /idea-feature-export --all --force from screens/splash/api.yaml.

The previous revision carried a FIELD_OFFICER session-resolution row routing to fo-dashboard (removed
earlier the same day) and described resolution via a local `SessionManager` reading a DirectLogin
token from `CredentialStore`. Session state is owned by RootNavViewModel; splash declares no DI at
all. The base-URL header was also misleading on a screen that issues no requests.
-->
