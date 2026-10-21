# API — Connect with HSBC

Client contract for `login`. This project owns no backend: this is a Ktorfit contract against the
HSBC UK/CE sandbox (OBIE Read/Write Standard, FAPI 1.0 Advanced), not owned schema.
Consumer: `LoginRepository`.

This screen makes **one** call. The rest of the authorisation journey — the FAPI redirect and the
token exchange — happens in the browser and on `consent-callback`.

---

## consent-create

| | |
|---|---|
| Endpoint | `POST /account-access-consents` |
| Auth | **client_credentials** grant — *not* a PSU token |
| Requires auth | yes |
| Response DTO | `HSBCCreateConsentResponse` |

Stages the consent the PSU is about to authorise.

The auth model is the point to get right: there is no PSU token yet — that is what the whole journey
exists to obtain. The consent resource is created at TPP level with the client-credentials grant,
and only then does the PSU authorise it at the bank.

**Request body:** an `OBReadConsent1` carrying the full `Permissions[]` array (ten OBIE read scopes,
including `ReadAccountsDetail`, `ReadBalances`, `ReadTransactionsDetail`) and a 90-day
`ExpirationDateTime`.

The permission list matters downstream: several screens degrade or refuse based on scopes granted
here. `ReadParty` gates `account-holder`; `ReadBeneficiariesDetail` gates `beneficiaries`;
`ReadDirectDebits` must be present at creation because it cannot be added to a live consent;
`ReadStatementsDetail` (not the narrower `ReadStatements`) is what makes statement balances readable.
A scope omitted here cannot be recovered without a new consent.

**Response key fields**

| Field                       | Purpose                                       |
|-----------------------------|-----------------------------------------------|
| `Data.ConsentId`            | Used to construct the FAPI authorisation URL  |
| `Data.Status`               | Initial consent status                        |
| `Data.ExpirationDateTime`   | Drives `consent_expiry_display`               |
| `Data.Permissions`          | Renders `permissions_list`                    |

`permissions_list` is populated from the **response**, not from the request — the customer is shown
what the bank recorded, not what the app asked for.

---

## Errors

| Code | Cause | Handling |
|------|-------|----------|
| 400 | Malformed `OBReadConsent1` — invalid `Permissions[]` enum values or datetime format; HSBC returns an `OBErrorResponse1` body | `error` state, retry |
| 401 | Client-credentials bearer invalid or expired | App must re-request a token before retrying |
| 500 | HSBC upstream error — transient | Eligible for **one** automatic retry with 2-second exponential back-off |
| `NetworkException` | Device offline or DNS failure | "Check your connection and try again" |
| `FapiRedirectException` | HSBC app not installed, or the TPP `redirect_uri` scheme is not registered on this device | Prompt the PSU to install the HSBC app |

`FapiRedirectException` is the one worth designing for: it is not a network problem and not a bank
problem — the app-to-app redirect has nowhere to land. Telling the customer to check their
connection would send them chasing the wrong fault.

---

## After this call

`StartOAuth` continues past the response without another API call from this screen:

1. build a FAPI 1.0 Advanced `/authorize` URL (`response_type=code id_token`, `scope=openid accounts`)
   with a PS256-signed request object (jose4j, `private_key_jwt`) carrying the `ConsentId`, a nonce and state
2. persist the in-flight authorisation in `PendingAuthStore` so it survives the redirect
3. launch the app-to-app redirect via `BrowserLauncher` (expect/actual per platform)
4. move to `authorising` until the PSU returns through the `consent-callback` deep link

The token exchange itself is `consent-callback`'s `fapi-token-exchange` — see that feature's `API.md`.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/login/api.yaml. -->
