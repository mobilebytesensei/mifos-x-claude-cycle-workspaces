<!--
generated_by: /idea-feature-export-spec
generated_at: 2026-10-03
feature_id: signin
source: screens/signin/api.yaml
-->

# API — Sign in

Access point `mifos` → `https://apis.mifos.community/` + base path `1.0/field/v1/`.

> That base path is the **field-officer gateway**, not plain Fineract's
> `fineract-provider/api/v1/`. Probed 2026-10-01: the gateway path answers 401 (exists, credential
> rejected); the Fineract path answers 404. The wrong value cost a packet-level diagnosis because
> the UI reported "Login failed. Check your credentials and try again."
> `ServerConfigAccessPointParityTest` now fails the build if the screen's default and the access
> point diverge.

## Endpoints (1)

| Path | Method | Auth | Request | Response |
|---|---|---|---|---|
| `authentication` | POST | **anonymous** — this is the call that MINTS the credential | `username(String)`, `password(String)` | `PostAuthenticationResponse` |

### Request headers

| Header | Value | Note |
|---|---|---|
| `Fineract-Platform-TenantId` | `mifos-bank-1` | from the access-point declaration |
| `Content-Type` | `application/json` | **required** — ContentNegotiation only serializes a body whose request declares a type it has a converter for, and a Ktorfit `@Body` sets none. Without it Ktor throws before opening a socket, and the screen renders "Login failed" with no HTTP log at all. |
| `Authorization` | *(absent)* | |

### Response — `PostAuthenticationResponse`

| Field | Type |
|---|---|
| `username` | `String?` |
| `userId` | `Long?` |
| `base64EncodedAuthenticationKey` | `String?` |
| `authenticated` | `Boolean?` |
| `officeId` | `Int?` |
| `officeName` | `String?` |
| `roles` | `List<Role>?` |
| `permissions` | `List<String>?` |

Every field is nullable **on purpose**. v1 force-unwrapped `userId!!`, `officeId!!` and
`permissions!!`, so any instance answering 200 without one of them crashed the app at the moment of
a *successful* login.

### Success condition

```
status == 200  AND  body.authenticated == true
```

Not status alone. Fineract answers **200 with `authenticated: false`** for a bad credential, so a
successful CALL is not a successful LOGIN. Dropping the flag check admits a failed login.

## Write policy

`MutationPolicy.OnlineRequired` via `MutationGateway.command`.

An authentication cannot be queued for later replay: a credential check that "succeeds" locally and
syncs afterwards would admit a user the server never agreed to. Offline returns
`MutationResult.Blocked(BlockReason.OFFLINE)` **without calling the endpoint** — pinned by
`AuthCommandRepositoryTest.offlineIsBlockedAndTheEndpointIsNeverCalled`, which asserts zero calls.

## Credential handoff

The **raw** `base64EncodedAuthenticationKey` is stored; the wire prefix is added by the access
point's `AuthScheme.BASIC.format` → `Basic <token>`.

Storing a pre-formatted `"Basic <token>"` produced `Authorization: Basic Basic <token>` and 401'd
every authenticated call **while sign-in itself kept working** — measured on device 2026-10-01.

The raw password is **not** persisted. Nothing reads it: every consumer uses `username` or the
encoded key. Locked by `theRawPasswordIsNeverPersisted`.

## Error mapping

| Condition | `SignInError` | Surface |
|---|---|---|
| `authenticated != true` | `Rejected` | snackbar |
| non-2xx / transport failure | `Rejected` (cause logged) | snackbar |
| `Blocked(OFFLINE)` | `Offline` | snackbar, distinct copy |
| local rule failure | `UsernameTooShort` / `PasswordTooShort` | on the offending field |
| `FailedAttemptTracker.isLockedOut` | `LockedOut` | inline banner, submit disabled |

## Known gap

`expectSuccess` is unset on the shared client, so a non-2xx body deserializes onto DTO defaults and
reaches the caller as a successful empty result. For **this** endpoint the explicit `authenticated`
check masks it; on list reads it surfaced as "Nothing here yet" for a 401/502. Pinned by
`AuthDtoContractTest.anErrorBodyDoesNotMasqueradeAsASuccessfulLogin`. Raised for upstream
(`core-base/network`) — not fixable from this feature.
