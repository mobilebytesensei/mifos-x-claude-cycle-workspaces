# API — HSBC Connection Detail

Client contracts for `consent-detail`. This project owns no backend: these are Ktorfit contracts
against the HSBC UK/CE sandbox (OBIE Read/Write Standard), not owned schema.
Consumer: `ConsentDetailRepository`.

Both calls authenticate with the **client_credentials** token — the consent resource is a TPP-level
object, not a PSU-level one, so the PSU bearer is not what reads or deletes it.

---

## consent-status

| | |
|---|---|
| Endpoint | `GET /account-access-consents/{ConsentId}` |
| Response DTO | `ConsentSummary` |
| Requires auth | yes — `client_credentials` |
| Path param | `ConsentId: string` |

Fetches the full consent resource: `Status`, `Permissions[]`, and the date fields.

The date set is what the screen's Dates section renders, and the four are not interchangeable:
creation and expiry bound the consent's *life*, while `TransactionFromDateTime` /
`TransactionToDateTime` bound the *history window* it can read. OBIE requires both be disclosed;
showing only expiry would understate what was agreed.

`Permissions[]` populates `permissions_list` one row per granted permission — this is the
authoritative answer to "what did I agree to", and it is why the list is rendered from the response
rather than from a local assumption about what the app requested.

---

## consent-revoke

| | |
|---|---|
| Endpoint | `DELETE /account-access-consents/{ConsentId}` |
| Success | **204 No Content** |
| Requires auth | yes — `client_credentials` |
| Path param | `ConsentId: string` |
| Triggered by | `ExecuteRevoke`, only from the `RevokeConfirm` dialog |

Revokes the consent resource.

**Local cleanup is mandatory on success.** The app must clear the stored PSU access token and the
`ConsentId`. Leaving them behind means holding credentials for access that no longer exists — every
subsequent call would fail with a confusing 401 rather than a clean logged-out state. Where the
revoked consent is the active one, `AppLogout` ends the session and the root navigator returns the
customer to onboarding.

### 404 is success, not failure

A 404 means the consent no longer exists server-side. It **must be treated idempotently as
already-revoked**: perform the identical local cleanup and navigate to `consent-list` **without
surfacing an error**.

The customer asked for access to end. If it has already ended — a duplicate tap, a parallel
revocation, an expiry that landed first — then their intent is satisfied. Showing an error would
tell them revocation failed when access is in fact gone, which is the more dangerous of the two
wrong messages.

### Error surface

`RevokeServerError` is modelled separately from `NetworkError` precisely because a failed revoke is
not an ordinary read failure: the customer believes they have withdrawn access, and the UI must not
imply success. Anything other than 204 or 404 leaves the consent live and must say so.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/consent-detail/api.yaml. -->
