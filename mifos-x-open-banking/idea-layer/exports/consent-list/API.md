# API — Consent List

Client contract for `consent-list`. This project owns no backend: this is a Ktorfit contract
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `ConsentDetailRepository`, with `ConsentSession` supplying the known ConsentIds.

---

## consent-status

| | |
|---|---|
| Endpoint | `GET /account-access-consents/{ConsentId}` |
| Response DTO | `ConsentSummary` |
| Auth | `client_credentials` |

**Called once per locally-stored ConsentId** — there is no list endpoint. The bank exposes consents
individually, so the screen's list is assembled client-side from the ConsentIds this app has
recorded, each refreshed in turn.

Two consequences follow from that, and both are visible in the UI:

**The list can only ever show consents this app knows about.** A consent granted through another
channel is invisible here — not because it was filtered out, but because no ConsentId for it was
ever stored locally.

**Expired and revoked consents are fetched deliberately.** They are not errors to be swallowed:
their `Status` is what populates the History section. Dropping a non-`Authorised` response would
erase the customer's consent history, which PSD2 transparency expects them to be able to see.

### Sandbox constraint

In the HSBC sandbox a PSU can hold **only one active consent at a time**. The Active section is
therefore effectively single-card, while History accumulates. Code that assumes a multi-consent
Active list will not be exercised against this sandbox.

---

## Status → section mapping

| `Data.Status`           | Section |
|-------------------------|---------|
| `Authorised`            | Active  |
| `AwaitingAuthorisation` | Active  |
| `Rejected`              | History |
| `Revoked`               | History |
| `Consumed`              | History |
| expired                 | History |

---

## Errors

| Type                       | Cause                          | State        | Recovery         |
|----------------------------|--------------------------------|--------------|------------------|
| `NetworkError`             | Offline / transport            | `error`      | Retry            |
| `ConsentStatusServerError` | Bank-side failure              | `error`      | Retry            |
| `TokenExpiredSession`      | Client-credentials token expired | `error_auth` | **Re-authenticate** |

The auth case gets its own state and its own CTA. Retrying an expired session re-sends a request
that will be refused identically — the only path forward is a fresh authorisation, so
`auth_error_state` routes to `LoginRenewRoute` instead of offering a retry that cannot succeed.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/consent-list/api.yaml. -->
