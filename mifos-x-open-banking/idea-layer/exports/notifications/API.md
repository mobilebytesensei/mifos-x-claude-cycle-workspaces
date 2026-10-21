# API — Notifications

Client contract for `notifications`. This project owns no backend: this is a Ktorfit contract
against the OBP sandbox, not owned schema.
Consumers: `NotificationRepository`, `SignalRepository`.

---

## obp_signal_channels

| | |
|---|---|
| Endpoint | `GET /obp/v6.0.0/signal/channels` |
| Consumer | `SignalRepository` |

Returns the signal-channel configuration — which delivery channels exist and are enabled for this
user.

**This is not the notification list.** The notifications themselves are managed by
`NotificationRepository`; only channel configuration comes from this endpoint. A failure here means
the app cannot describe *how* notifications are delivered, not that there are none to show.

Failure → `LOAD_FAILED`, "Unable to load notifications. Please try again."

---

## Category routing

There is no per-notification target field. `NotificationOpened` carries a
`category: NotificationCategory`, and the destination is derived from it:

| Category   | Destination          |
|------------|----------------------|
| `payment`  | `transaction-detail` |
| `security` | `profile`            |
| `system`   | `accounts`           |

Adding a category therefore means adding a routing rule, not adding a field to the payload — and a
notification with an unrecognised category has no destination rather than a wrong one.

**Security previously routed to `kyc-review`**, a field-officer screen removed when the app became
consumer-only. Retargeted to `profile` on 2026-08-02: an identity-verification result belongs on the
customer's own profile.

---

## Read state

`mark_all_read` clears `unreadCount` and the per-card unread dots. `MarkAllReadComplete` is a
separate event from `MarkAllReadClicked` so the UI can reflect the committed result rather than
optimistically clearing — a failed mark-all leaves the dots in place rather than silently lying
about what has been seen.

Opening a notification marks that one read as it navigates, so the indicator has cleared when the
customer returns.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/notifications/api.yaml. -->
