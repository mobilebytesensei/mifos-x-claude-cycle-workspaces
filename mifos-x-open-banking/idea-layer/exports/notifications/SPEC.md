# SPEC — Notifications

| Field         | Value                     |
|---------------|---------------------------|
| Feature       | notifications             |
| Flavor        | consumer                  |
| Status        | approved                  |
| Quality Score | 95                        |
| ViewModel     | NotificationsViewModel    |
| Archetype     | index_list                |

---

## Overview

A time-grouped notification list — Today and Earlier — with per-category routing and a Mark All Read
action.

Tapping a notification navigates by **category**, not by a per-notification target: payment →
`transaction-detail`, security → `profile`, system → `accounts`. The card is the tap target; the
row, icon, icon background, text column and unread dot nested inside it are presentational and carry
no handlers of their own, so each notification reads as one control rather than six.

Unread state is shown by a dot rather than a background change on the whole row, so a read and an
unread notification stay equally legible.

---

## Screens

| ID            | Name          | ViewModel              | Archetype  |
|---------------|---------------|------------------------|------------|
| notifications | Notifications | NotificationsViewModel | index_list |

**Shell:** top app bar shown, title "Notifications", `arrow_back` → `navigate_back`, with a
`done_all` action mirroring Mark All Read.

---

## Components

| ID                        | Type   | Description                                              |
|---------------------------|--------|-----------------------------------------------------------|
| title_action_row          | stack  | Header row — presentational container                    |
| └ notifications_title     | text   | "Notifications"                                          |
| └ mark_all_read_button    | button | "Mark All Read" → `mark_all_read`                        |
| section_today_label       | text   | "Today"                                                  |
| notification_payment_james| box    | Payment notification card — **the tap target** → transaction-detail |
| └ payment_james_row       | stack  | Layout row (presentational)                              |
| └ payment_james_icon_bg   | box    | Icon background (presentational)                         |
| └ payment_james_icon      | icon   | `arrow_downward` — decorative                            |
| └ payment_james_text_col  | stack  | Text column (presentational)                             |
| └ payment_james_title     | text   | "Payment received"                                       |
| └ payment_james_message   | text   | "Payment of £50.00 received from James Wilson"           |
| └ payment_james_time      | text   | "10 min ago"                                             |
| └ unread_dot_payment_james| box    | Unread indicator — `role: status`                        |
| notification_kyc_approved | box    | Security notification card → **profile**                 |
| └ kyc_approved_*          | —      | Same nested structure as above                           |
| └ unread_dot_kyc          | box    | Unread indicator                                         |
| section_earlier_label     | text   | "Earlier"                                                |
| notification_netflix_mandate | box | System notification card → accounts                      |
| └ netflix_mandate_*       | —      | Same nested structure; read, so no unread dot            |
| notification_salary_credited | box | Payment notification card → transaction-detail            |
| └ salary_credited_*       | —      | Same nested structure; read                              |
| bottom_spacer             | spacer | Trailing spacing                                         |

The four cards are demo instances of one repeating pattern — a real implementation renders one card
per `NotificationItem`.

---

## States

Initial state: `loading`. Four states.

| State     | Rendering                                       |
|-----------|--------------------------------------------------|
| loading   | Fetching                                        |
| populated | Time-grouped cards (Today / Earlier)            |
| empty     | No notifications                                |
| error     | `LOAD_FAILED` — retry                           |

---

## State Model

**ViewModel:** `NotificationsViewModel`.

**State fields**

| Field           | Type                      | Default      |
|-----------------|---------------------------|--------------|
| `notifications` | `List<NotificationItem>`  | `emptyList()`|
| `unreadCount`   | `Int`                     | `0`          |
| `uiState`       | `NotificationsUiState`    | `Loading`    |
| `error`         | `UiError?`                | `null`       |

**Errors:** `global` / `LOAD_FAILED` → "Unable to load notifications. Please try again."

**Events:** `NotificationsLoaded`,
`NotificationOpened(notificationId: String, category: NotificationCategory)`,
`MarkAllReadClicked`, `MarkAllReadComplete`, `RetryLoad`, `NotificationSettingsOpened`.

`NotificationOpened` carries the **category** as well as the id — that is what selects the
destination, so routing is a property of the category rather than something stored per notification.

**Actions:** `open_notification`, `mark_all_read`, `open_notification_settings`.

**DI:** `NotificationRepository`, `SignalRepository`.

---

## Navigation

| From          | To                 | Trigger                              | Category | Type |
|---------------|--------------------|--------------------------------------|----------|------|
| notifications | transaction-detail | `open_notification` on a payment card | payment  | push |
| notifications | profile            | `open_notification` on a security card| security | push |
| notifications | accounts           | `open_notification` on a system card  | system   | push |
| notifications | settings           | `open_notification_settings`         | —        | push |
| notifications | home               | `navigate_back`                      | —        | pop  |

`flow.yaml#navigates_to` is `[]` — routing is category-driven at runtime rather than a declared
static edge set.

**Security notifications route to `profile`.** They previously deep-linked to `kyc-review`, a
field-officer screen that no longer exists in this consumer-only app; retargeted 2026-08-02.

---

## API Endpoints

| ID                  | Endpoint                          | Purpose                          |
|---------------------|-----------------------------------|----------------------------------|
| obp_signal_channels | `GET /obp/v6.0.0/signal/channels` | Signal channel configuration     |

The notification list itself is managed by `NotificationRepository`; only channel configuration is
fetched. Full detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. Category is carried by the icon
background — `primary` for security, `secondary` for system, and the `payment_disposition` pair for
money movement — rather than by card colour, so unread state stays the only thing the card's fill
communicates. Components reference semantic roles, so both theme modes resolve from
`design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/notifications/{ui,api,flow,docs}.yaml. -->
