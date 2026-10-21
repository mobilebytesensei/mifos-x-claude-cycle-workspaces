# API — Connected Apps

Client contracts for `consent-manager`. This project owns no backend: these are Ktorfit contracts
against the OBP sandbox, not owned schema. Consumer: `ConsentRepository`.

**These are OBP consumer-scoped endpoints, not the OBIE `account-access-consents` resource.**
`consent-list` and `consent-detail` manage consents *this app holds at banks*; this screen manages
consents *third-party apps hold at this bank*. Different objects, different API surface — the two
must not be conflated when wiring repositories.

---

## obp_my_consents

| | |
|---|---|
| Endpoint | `GET /obp/v4.0.0/consumers/{consumerId}/consents` |
| Trigger | Screen entry, and after any successful revoke |

Returns the consents granted to third-party consumers, mapped to `List<ConsentItem>`.

Each item supplies what a card renders: app name, granted date, expiry date, status, and the scope
list. Scopes come from the response rather than a local catalogue — the customer must see what was
actually granted, not what the app assumes is typical.

Failure → `LOAD_FAILED`, "Unable to load connected apps. Please try again."

---

## obp_revoke_consent

| | |
|---|---|
| Endpoint | `DELETE /obp/v4.0.0/consumers/{consumerId}/consents/{consentId}` |
| Trigger | `confirm_revoke_consent`, only from the confirmation dialog |
| On success | Dismiss dialog, refresh the list |

Revokes a third party's access.

The call is reachable only through `revoke_confirm` — `revoke_consent` opens the dialog and sends
nothing. That separation exists because revocation is immediate and irreversible from the app's
side: the third party loses access the moment this returns, and re-granting means the customer
going back through that app's own authorisation journey.

`revokingConsentId` scopes the in-flight state to the one card, so the rest of the list stays
interactive while a revoke is running.

Failure → `REVOKE_FAILED`, "Could not revoke access. Please try again." — surfaced against the
revoke action rather than replacing the screen, so the customer can retry the specific card.

---

## Revoke vs Remove

The two buttons look similar and mean different things:

| Consent status | Button          | What it does                                       | Calls the API |
|----------------|-----------------|-----------------------------------------------------|---------------|
| ACTIVE         | "Revoke Access" | Ends live access — third party loses data now       | yes           |
| EXPIRED        | "Remove"        | Clears the row; access already lapsed               | no live access to end |

`RemoveExpiredConsentClicked` is a separate event from `RevokeConsentClicked` for exactly this
reason. Labelling an expired consent "Revoke Access" would suggest access is still live and that
the customer is stopping something; labelling an active one "Remove" would understate that the
third party is about to be cut off.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/consent-manager/api.yaml. -->
