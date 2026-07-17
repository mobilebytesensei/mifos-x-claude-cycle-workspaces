# Authentication — API Contract

> **Backend note (global self-signup pivot, 2026-07-17):** The auth operations for the unified
> login/signup flow (self-register, login, me) are now implemented as **Companion API tools in mcp-mifosx**,
> not direct Fineract calls. The endpoints below (`/authentication`, `/self/authentication`) remain valid
> for Fineract back-office credential flows but the primary client path uses COMP-AUTH-001/002/003 at
> `/companion/auth/*`. See `exports/login-signup/API.md` for the full companion auth contract and
> `server-layer/COMPANION_API_BUILD_DEPLOY.md` for the backend build spec (TIER-1: auth-model change + COMP-AUTH tools).

## Companion Auth Endpoints (primary path — mcp-mifosx)

| Contract | Method | Path | Description |
|----------|--------|------|-------------|
| COMP-AUTH-001 | POST | `/companion/auth/self-register` | Self-register → Fineract `POST /self/registration` |
| COMP-AUTH-002 | POST | `/companion/auth/login` | Login → Fineract session + group memberships |
| COMP-AUTH-003 | GET | `/companion/auth/me` | Session identity + memberships (Bearer) |

Full request/response contract: `exports/login-signup/API.md`

## Fineract Direct Endpoints (back-office / legacy path)

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /authentication | Authenticate admin/staff via Fineract username+password | None (pre-auth) |
| POST | /self/authentication | Authenticate end user via Fineract self-service credentials | None (pre-auth) |

## Request / Response Details

### authenticate_admin

**Request**:

| Field | Type | Required | Source |
|-------|------|----------|--------|
| username | String | Yes | user_input |
| password | String | Yes | user_input |

Request body (form or JSON):
```
POST /authentication
{
  "username": "mwangaza_treasurer",
  "password": "••••••••"
}
```

**Response**:

| Field | Type | Description |
|-------|------|-------------|
| userId | Long | Fineract internal user ID |
| base64EncodedAuthenticationKey | String | Base64 Basic auth token for subsequent requests |
| authenticated | Boolean | True on success |
| username | String | Confirmed username |
| roles | List\<String\> | e.g. ["ROLE_TELLER", "ROLE_LOAN_OFFICER"] |
| officeId | Long | Fineract office/branch ID |
| officeName | String | Office display name |

**Errors**:

| HTTP Code | Meaning | UX Action |
|-----------|---------|-----------|
| 401 | Invalid credentials | Show `error_invalid_credentials` banner; re-enable fields |
| 503 | Server unavailable | Show `error_server` banner; offer PIN mode |

**Cache**: no-cache. Offline fallback: use_local_pin (PIN auth handled fully on-device via PinManager).

---

### authenticate_end_user

**Request**:

| Field | Type | Required | Source |
|-------|------|----------|--------|
| username | String | Yes | user_input |
| password | String | Yes | user_input |

Request body:
```
POST /self/authentication
{
  "username": "grace.mwangi",
  "password": "••••••••"
}
```

**Response**:

| Field | Type | Description |
|-------|------|-------------|
| userId | Long | Fineract internal user ID |
| base64EncodedAuthenticationKey | String | Self-service auth token |
| authenticated | Boolean | True on success |
| username | String | Confirmed username |
| clientId | Long | Linked Fineract client (member) ID — passed to dashboard |
| clientName | String | Member display name |

**Errors**:

| HTTP Code | Meaning | UX Action |
|-----------|---------|-----------|
| 401 | Invalid credentials | Show `error_invalid_credentials` banner |
| 503 | Server unavailable | Show `error_server` banner; offer PIN mode |

**Cache**: no-cache. Offline fallback: use_local_pin.

---

## DTOs

### AdminAuthResponse

| Field | Type |
|-------|------|
| userId | Long |
| base64EncodedAuthenticationKey | String |
| authenticated | Boolean |
| username | String |
| roles | List\<String\> |
| officeId | Long |
| officeName | String |

### SelfAuthResponse

| Field | Type |
|-------|------|
| userId | Long |
| base64EncodedAuthenticationKey | String |
| authenticated | Boolean |
| username | String |
| clientId | Long |
| clientName | String |

## Offline / PIN Authentication

PIN and biometric authentication are handled entirely on-device by `PinManager` and `BiometricManager`. No network call is made for PIN/biometric login. The PIN is derived from and verified against a locally stored encrypted hash created during the first successful password login.

| Mode | Network Required | Repository | On Success |
|------|-----------------|-----------|------------|
| Password | Yes | AuthRepository | Store token + prime PIN hash |
| PIN | No | PinManager (local) | Restore cached session |
| Biometric | No | BiometricManager (local) | Restore cached session |

## Error Type Map

| LoginError Type | Retry | i18n Key | Trigger |
|----------------|-------|---------|---------|
| InvalidCredentials | true | error_invalid_credentials | HTTP 401 |
| Network | true | error_network | No connectivity |
| Server | true | error_server | HTTP 5xx / timeout |
| PinNotSet | false | error_pin_not_set | PIN attempted but not configured |
| BiometricFailed | true | error_biometric_failed | OS biometric returns FAILED |
