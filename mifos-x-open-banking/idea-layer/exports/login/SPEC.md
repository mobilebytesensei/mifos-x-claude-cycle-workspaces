# SPEC — Connect with HSBC

| Field         | Value          |
|---------------|----------------|
| Feature       | login          |
| Flavor        | consumer       |
| Status        | approved    |
| Quality Score | 95             |
| ViewModel     | LoginViewModel |

---

## Overview

The screen is the PSU's entry into the HSBC Open Banking consent journey — it is a consent-creation
and redirect surface, not a credential form. The app never sees HSBC credentials: it stages an
`OBReadConsent1` containing ten OBIE read scopes (including `ReadAccountsDetail`, `ReadBalances`,
`ReadTransactionsDetail`) to `account-access-consents` via ktorfit using a `client_credentials`
token, stores the returned `ConsentId`, then builds a FAPI 1.0 Advanced `/authorize` URL
(`response_type=code id_token`, `scope=openid accounts`) carrying a PS256-signed request object
(jose4j, `private_key_jwt`) with the `ConsentId`, a nonce and state. It then launches an app-to-app
redirect to HSBC, where the PSU completes SCA and selects accounts, and moves to `authorising`
until the consumer returns through the `consent-callback` deep link.

Before that redirect the screen discloses what is being asked for: an explainer card naming HSBC as
the destination, an FCA-regulated-connection badge, a dynamic list of the ten permissions with
human-readable descriptions, and the OBIE-mandated consent validity window with a computed expiry
label. A PSU who declines simply returns to `user-onboarding` with nothing staged.

---

## Screens

| ID    | Name               | Route                          | Layout | Scroll   |
|-------|--------------------|--------------------------------|--------|----------|
| login | Connect with HSBC  | LoginRoute / LoginRenewRoute   | Column | Vertical |

**Shell:** Top app bar visible with back leading icon, title `{strings.screen.login.title}`. No bottom navigation. No FAB.

**Two entry points.** `LoginRoute` is the onboarding-entry consent screen. `LoginRenewRoute` is the
same screen reached *without* the onboarding intro, used for re-consent — reached from consent-list
(`onConnectBank`, `onReauthenticate`) and consent-detail (`onReconfirm`).

---

## Components

| ID                     | Type              | State       | Description                                                                                                   |
|------------------------|-------------------|-------------|---------------------------------------------------------------------------------------------------------------|
| loading_indicator      | progress_linear   | loading     | Linear progress shown while the consent-create POST is in flight                                              |
| loading_label          | text              | loading     | bodyMedium / onSurfaceVariant status label beside the progress indicator                                       |
| authorising_spinner    | progress_circular | authorising | Circular spinner shown after the FAPI redirect launches, while the PSU authenticates in HSBC                   |
| authorising_label      | text              | authorising | bodyMedium / onSurfaceVariant status message during HSBC authentication                                        |
| authorising_hint       | text              | authorising | bodySmall hint telling the PSU to finish in HSBC and return; sits below the spinner                            |
| hsbc_explainer_card    | card              | content     | Elevation 1 card contextualising the app-to-app redirect — HSBC will ask the PSU to approve permissions and select accounts |
| └ hsbc_logo            | image             | content     | `ic_hsbc_logo` — brand identity confirming which bank the PSU is redirected to                                 |
| └ ob_regulated_badge   | text              | content     | labelSmall / primary with leading `verified_user` — confirms an FCA-authorised TPP connection                  |
| └ explainer_headline   | text              | content     | titleMedium / onSurface — names the redirect destination for informed consent                                  |
| └ explainer_body       | text              | content     | bodySmall / onSurfaceVariant — clarifies FAPI redirect behaviour and the credential-protection guarantee       |
| └ card_divider         | divider           | content     | Separates PSU-facing explainer copy from the technical security notice                                         |
| └ security_notice      | text              | content     | labelSmall with leading `lock_outline` — FAPI/mTLS/PS256 notice for technically-aware readers                   |
| permissions_header     | section_header    | content     | Heading introducing the OBIE read permissions staged in `OBReadConsent1`                                       |
| permissions_list       | list              | content     | Vertical, `items_source: {requested_permissions}` — renders each permission (10 rows expected)                 |
| └ permission_row       | list_item         | content     | `check_circle_outline` + `{item.label}` headline + `{item.description}` supporting text                         |
| consent_validity_note  | text              | content     | bodySmall — OBIE-mandated disclosure of the validity period and TransactionFromDateTime window                 |
| consent_expiry_display | text              | content     | labelMedium / primary — VM-computed expiry label from `ExpirationDateTime` (e.g. "Expires 26 Sep 2026")        |
| continue_hsbc_button   | button (filled)   | content     | `{strings.screen.login.cta.continue}` with `open_in_new` icon — primary CTA; triggers `start_oauth`             |
| cancel_button          | button (text)     | content     | `{strings.screen.login.cta.cancel}` — abandons the flow, returns to user-onboarding                            |
| error_state            | error_state       | error       | `error_outline` icon; body renders the VM-mapped `{error.user_message}`. Uses the registry's dedicated `error_state` (a11y `role: alert`), not an `empty_state` styled red |
| └ retry_button         | button (filled)   | error       | Re-triggers `start_oauth` after a consent-create failure                                                        |
| login_empty_state      | empty_state       | empty       | `manage_search` icon — zero OBIE permissions resolved. Correctly an `empty_state` (`role: status`): nothing failed, there is simply nothing to consent to |
| └ login_empty_back_button | button (filled)| empty       | Returns to user-onboarding rather than letting the PSU stage a zero-scope consent                              |

---

## States

| State       | Meaning                                                                          |
|-------------|----------------------------------------------------------------------------------|
| content     | Requested permissions and consent expiry rendered; the PSU can continue or cancel |
| loading     | consent-create POST in flight                                                     |
| authorising | FAPI redirect launched; the PSU is authenticating in HSBC                         |
| error       | consent-create failed (network, 400, 500); retry offered                          |
| empty       | Zero OBIE permissions staged — prevents a zero-scope consent HSBC would reject     |

Initial state: `content`.

---

## State Model

**ViewModel:** `LoginViewModel` — state `LoginState { uiState: LoginUiState }`.

**Screen state:** sealed `LoginUiState` — `Loading`, `Content`, `Authorising`, `Empty`, `Error`.

**Actions:** `LoadPermissionsConfig` (reads the permission set, computes the expiry label) ·
`StartOAuth` (POST consent-create, build the FAPI URL, launch the app-to-app redirect) ·
`Cancel` (abort an in-flight authorisation and return to Content) · `Retry` (re-attempt after an error).

**DI:** `LoginRepository` (Koin single — consent creation + FAPI URL construction) ·
`BrowserLauncher` (expect/actual per platform — launches the app-to-app redirect) ·
`PendingAuthStore` (persists the in-flight authorisation — state, nonce, ConsentId — across the redirect).

**Platform expect/actual:** `BrowserLauncher` → `AndroidBrowserLauncher`, `DesktopBrowserLauncher`,
`IosBrowserLauncher`, `JsBrowserLauncher`.

---

## Navigation

| From  | To               | Trigger                                                        | Type |
|-------|------------------|----------------------------------------------------------------|------|
| login | consent-callback | HSBC authorisation redirect returns (OAuth callback) with auth code | push |
| login | user-onboarding  | `navigate_back` — Cancel tap, or Go Back from the empty state   | pop  |

**Entry point:** the PSU taps "Connect with HSBC" on user-onboarding.

Back is a nav-host `onBack` callback — `LoginAction` has no `navigateBack` member.

---

## API Endpoints

| ID             | Endpoint                          | Method | Auth                  | Purpose                                                     |
|----------------|-----------------------------------|--------|-----------------------|-------------------------------------------------------------|
| consent-create | `/account-access-consents`        | POST   | client_credentials    | Stages `OBReadConsent1` (10 read scopes, 90-day expiry); returns the `ConsentId` used to build the FAPI authorisation URL |

**Response DTO:** `HSBCCreateConsentResponse` — key fields `Data.ConsentId`, `Data.Status`,
`Data.ExpirationDateTime`, `Data.Permissions`.

**Errors:** `400` malformed OBReadConsent1 (invalid Permissions[] enum or datetime) ·
`401` client-credentials bearer invalid or expired, re-request before retry ·
`500` HSBC upstream, transient — one automatic retry with 2s exponential back-off ·
`NetworkException` offline or DNS failure → "Check your connection and try again" ·
`FapiRedirectException` HSBC app not installed or TPP redirect_uri scheme unregistered → prompt to install the HSBC app.

Note: the consent-create call is authenticated with the `client_credentials` grant, **not** a PSU token.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. Components reference semantic
roles (`primary`, `onSurface`, `onSurfaceVariant`) rather than literal hex values, so both theme
modes resolve from `design-system/design-tokens.yaml`.

---

<!--
Regenerated 2026-08-04 by /idea-sync from screens/login/{ui,api,flow,docs}.yaml.

The previous revision of this file documented a different screen entirely: dual Consumer /
Field-Officer authentication, a DirectLogin username+password form with "Keep me signed in" and a
"Forgot Password?" link, six OAuth OIDC calls covering token refresh and logout revocation, and a
role-branching navigation table sending FIELD_OFFICER users to an `fo-dashboard` screen. None of
that survives in the source of truth — the screen is OAuth-only "Connect with HSBC", carries one
endpoint, and the project has been consumer-only single-flavor since 2026-08-02 with no
field-officer persona. `fo-dashboard` resolves to no screen directory.

Provenance: first regenerated 2026-08-04 during the export-drift repair, then reconciled by
/idea-feature-export --all --force in the same session — the component table's error_state row was
corrected from `empty_state` to `error_state` after the enrich-loop retyped that component.
-->
