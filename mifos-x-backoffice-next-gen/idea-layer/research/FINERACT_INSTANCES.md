# Fineract Live Instances — Connection Guide

> **Rule of use:** call the **PRIMARY** instance (`mifos-bank-2`) first for every API call.
> Fall back to the **sandbox** only if the primary is unreachable. Both accept the same demo
> credentials (`mifos` / `password` = **Super user**). Updated 2026-08-01.

## Instances

| | PRIMARY | FALLBACK |
|---|---|---|
| Host | `https://mifos-bank-2.mifos.community` | `https://sandbox.mifos.community` |
| API base | `https://mifos-bank-2.mifos.community/fineract-provider/api/v1` | `https://sandbox.mifos.community/fineract-provider/api/v1` |
| **Tenant id** (`Fineract-Platform-TenantId`) | **`mifos-bank-2`** ⚠️ (NOT `default`) | `default` |
| Credentials | `mifos` / `password` (Super user) | `mifos` / `password` (Super user) |
| Roles configured | **15** (real multi-role MFI config) | 2 (Super user, Self Service User) |
| Use for | primary — realistic role/permission data | fallback only |

> ⚠️ The single most common mistake: `mifos-bank-2` uses tenant **`mifos-bank-2`**, not `default`
> — a `default` tenant there returns **401 Unauthenticated**. The sandbox uses `default`.

## Mandatory request headers (every call)

- `Fineract-Platform-TenantId: <tenant>` — required on **every** request (auth included).
- `Authorization: Basic <base64(username:password)>` — for authenticated reads/writes.
  `mifos:password` → `bWlmb3M6cGFzc3dvcmQ=`.
- `Content-Type: application/json` — for POST/PUT bodies.
- TLS: both are HTTPS with valid certs. `curl -k` only needed if a proxy re-signs.

## Auth — two ways

**A. `POST /authentication` (what the app does at login)** — returns the user + `roles[]` +
`permissions[]` + `officeId`/`staffId` + a `base64EncodedAuthenticationKey` (the Basic token to
replay on later calls):
```bash
curl -s -X POST \
  -H "Fineract-Platform-TenantId: mifos-bank-2" \
  -H "Content-Type: application/json" \
  -d '{"username":"mifos","password":"password"}' \
  "https://mifos-bank-2.mifos.community/fineract-provider/api/v1/authentication"
```

**B. HTTP Basic header directly** (for one-off reads):
```bash
curl -s \
  -H "Fineract-Platform-TenantId: mifos-bank-2" \
  -H "Authorization: Basic bWlmb3M6cGFzc3dvcmQ=" \
  "https://mifos-bank-2.mifos.community/fineract-provider/api/v1/roles"
```

## Handy endpoints

| Endpoint | Returns |
|---|---|
| `POST /authentication` | user + roles[] + permissions[] + office/staff (login payload) |
| `GET /roles` | all roles (15 on primary, 2 on fallback) |
| `GET /roles/{id}` | one role |
| `GET /roles/{id}/permissions` | the role's grant matrix (`permissionUsageData[]`, `selected` flag per code) |
| `GET /permissions` | full permission catalog (693 across 29 groupings) |
| `GET /users`, `GET /users/template` | users; a user = office + roles (+ optional staff) — **no "user type"** |

## Roles on the PRIMARY instance (`mifos-bank-2`) — real data 2026-08-01

| id | Role | Granted perms | Maps to |
|---|---|---|---|
| 1 | Super user | 13 (ALL_FUNCTIONS + exchange-rate/transfer-fee extras) | super-user |
| 2 | Self Service User | 29 | self-service |
| 3 | SUPERVISOR | 99 | supervisor/checker |
| 4 | REVISOR DE PRESTAMOS | 459 | loan reviewer/checker |
| 5 | CAPTURISTA Y REVISOR | 459 | maker + checker |
| 6 | Oficial KYC | 43 | CSR / onboarding |
| 7 | OFICIAL DE CONTROL | 105 | compliance |
| 8 | TESORERO | 89 | treasurer |
| 9 | CAJERO | 75 | teller / cashier |
| 10 | CAPTURISTA | 150 | maker (data entry) |
| 11 | PROMOTOR | 139 | field agent |
| 12 | **OFICIAL DE CAMPO** | 149 (145 portfolio; **no APPROVE/DISBURSE** — maker only) | **loan / field officer** |
| 13 | EJECUTIVO | 195 | branch officer |
| 14 | OFICIAL PLD | 40 | AML officer |
| 15 | ANALISTA DE PRESTAMOS | 0 (empty role) | loan analyst |

> `OFICIAL DE CAMPO` is the real-world proof of the plan's maker-only field-officer surface:
> it can CREATE clients/loans/savings/guarantors/collateral and READ everything, but holds
> **no `APPROVE_LOAN` / `DISBURSE_LOAN`** — those escalate to a checker (REVISOR/SUPERVISOR).

## Permission model (recap)

Codes are `{ACTION}_{ENTITY}` (`READ_CLIENT`, `CREATE_LOAN`), maker-checker twin `{...}_CHECKER`,
umbrellas in the `special` grouping (`ALL_FUNCTIONS`, `ALL_FUNCTIONS_READ`, `CHECKER_SUPER_USER`,
`REPORTING_SUPER_USER`, `BYPASS_TWOFACTOR`). Fineract has **no role type and no user type** — a
role is a named permission bundle; a user is office + roles (+ optional staff). The app assembles
its UI purely from the login `permissions[]` + `officeId`/`staffId`.
