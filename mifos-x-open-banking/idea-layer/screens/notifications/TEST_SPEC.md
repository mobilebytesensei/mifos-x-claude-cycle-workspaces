# TEST SPEC — Notifications

| Field      | Value                                        |
|------------|----------------------------------------------|
| Feature    | notifications                                |
| Source     | `screens/notifications/tests.yaml`           |
| Scenarios  | 13                                           |
| Priorities | high 8 · medium 4 · low 1                    |
| States     | populated 9 · error 2 · loading 1 · empty 1  |
| Module     | _none yet — spec-only feature_               |

> No source module exists. These are **forward specs** derived from the feature's idea-layer
> siblings, not reverse-synced from a shipped suite.

---

## Coverage

| State     | Scenarios | Covered |
|-----------|-----------|---------|
| loading   | 1 | TC-NOTIF-001 |
| populated | 9 | TC-NOTIF-002 … -009, -013 |
| empty     | 1 | TC-NOTIF-010 |
| error     | 2 | TC-NOTIF-011, -012 |

All four states covered.

---

## Read state is local, and only local

TC-NOTIF-007 is the structural fact: marking a notification read writes to
`androidx.datastore` and issues **no server call**, because the app has no server-side notification
read state. Two consequences the spec does not yet address:

- Read state does not survive a reinstall, and does not follow the customer to another device.
- `unreadCount` is a device-local number, so two devices disagree about the same inbox.

Neither is wrong for a demo client against a sandbox. Both are worth stating before someone treats
the count as authoritative.

TC-NOTIF-013 now says the same thing from the other side: the screen makes **no** network call at
all, so push configuration is local too. There is no server-side half of this screen to disagree
with the local read state.

---

## TC-NOTIF-001 — Loading state shows the header above a four-row skeleton

**Priority:** medium · **State:** loading

- **Given** The notification list is loading (`initial_state: loading`)
- **When** Screen mounts
- **Then**
  - `title_action_row` and `notifications_title` visible
  - A four-row skeleton list is shown
  - Reduced-motion preference substitutes `static_placeholder` for the shimmer

---

## TC-NOTIF-002 — Populated state groups notifications under Today and Earlier

**Priority:** high · **State:** populated

- **Given** Two unread notifications from today and two read notifications from earlier
- **When** Screen renders
- **Then**
  - `section_today_label` precedes the two recent rows
  - `section_earlier_label` precedes the older rows
  - `mark_all_read_button` visible in the header row
  - `bottom_spacer` closes the list

The fixture correlates unread with today and read with earlier, which is realistic but means these
two dimensions are never tested independently. An old-but-unread notification — the one most worth
surfacing — is not covered by any scenario here.

---

## TC-NOTIF-003 — Unread rows carry a dot that read rows do not

**Priority:** high · **State:** populated

- **Given** Two unread and two read notifications
- **When** The rows render
- **Then**
  - `unread_dot_payment_james` and `unread_dot_kyc` render on the two unread rows
  - The read Netflix and salary rows render no unread dot
  - Unread status is conveyed by the dot, not by colour alone

Both the positive and the negative case are asserted against the same render. A dot that appears
on every row communicates nothing, and that failure only shows up when read rows are checked too.

---

## TC-NOTIF-004 — Each row states its title, message and relative time

**Priority:** high · **State:** populated

- **Given** A payment notification
- **When** The row renders
- **Then**
  - `payment_james_title` reads "Payment received"
  - `payment_james_message` reads "Payment of £50.00 received from James Wilson"
  - `payment_james_time` reads a relative label such as "10 min ago"
  - The row a11y label combines all three plus the unread status

Folding unread status into the row's a11y label is what carries TC-NOTIF-003's dot to a screen
reader — the dot itself is a shape, and shapes do not announce.

---

## TC-NOTIF-005 — Row icons are decorative and not separately announced

**Priority:** low · **State:** populated

- **Given** Populated state
- **When** The icon backgrounds and glyphs render
- **Then**
  - `payment_james_icon_bg` and `payment_james_icon` carry empty a11y labels
  - The parent row supplies the announced description

---

## TC-NOTIF-006 — Opening a notification carries its id and category

**Priority:** high · **State:** populated

- **Given** Populated state
- **When** User taps `notification_payment_james` (`open_notification`)
- **Then**
  - `NotificationOpened` fires with the `notificationId` and `NotificationCategory`
  - The row's unread dot clears once it is opened

The event carries a category but the spec never says where any category routes to. Opening a
payment notification presumably reaches `transaction-detail` and a KYC one somewhere else; neither
destination is asserted. A follow-up scenario per category is owed.

---

## TC-NOTIF-007 — Mark all read writes local state only

**Priority:** high · **State:** populated

- **Given** Two unread notifications
- **When** User taps `mark_all_read_button` (`mark_all_read`)
- **Then**
  - The read flag for every listed notification is written to `androidx.datastore`
  - `notifications.readState` and `notifications.unreadCount` are the write targets
  - No server call is issued — this app has no server-side notification read state

---

## TC-NOTIF-008 — Mark all read clears every unread dot and the count

**Priority:** high · **State:** populated

- **Given** `unreadCount` is 2
- **When** `MarkAllReadComplete` is handled
- **Then**
  - `unreadCount` becomes 0
  - All unread dots disappear
  - The rows themselves remain listed

"The rows remain listed" is the assertion that separates *read* from *dismissed*. A mark-all-read
that empties the screen destroys the customer's ability to go back and look at what they cleared.

---

## TC-NOTIF-009 — Notification settings opens from the header action

**Priority:** medium · **State:** populated

- **Given** Populated state
- **When** The `open_notification_settings` action is invoked
- **Then**
  - `NotificationSettingsOpened` fires
  - The action is exposed as "Notification settings" in the header

No destination screen is named, and no `notification-settings` feature exists in the idea-layer.
The event fires into nothing until that surface is declared.

---

## TC-NOTIF-010 — Empty state reassures rather than reporting a fault

**Priority:** high · **State:** empty

- **Given** The load succeeds and returns no notifications
- **When** Screen renders
- **Then**
  - `notifications_none_outlined` icon visible
  - Title "You're all caught up" and the payments/alerts/updates message visible
  - `mark_all_read_button` is not offered
  - This is distinct from the error state

Withholding mark-all-read on an empty list is a small thing done right — a button that would do
nothing invites a tap that appears to fail.

---

## TC-NOTIF-011 — Error state offers retry

**Priority:** high · **State:** error

- **Given** The load fails (`LOAD_FAILED`)
- **When** Screen renders
- **Then**
  - `cloud_off` icon with "Unable to load notifications" and "Check your connection and try again" visible
  - A retry button is shown and wired to `RetryLoad`
  - The header row and title remain visible

---

## TC-NOTIF-012 — Retry re-runs the load

**Priority:** medium · **State:** error

- **Given** Error state is displayed
- **When** `RetryLoad` is dispatched
- **Then**
  - The notification load re-runs
  - State transitions error → loading → populated or empty

The only retry scenario in the corpus that names **both** possible successful outcomes. Worth
copying: a retry that lands on empty is a success, and a test asserting only `populated` would
call it a failure.

---

## TC-NOTIF-013 — The screen makes no network call

**Priority:** medium · **State:** populated

- **Given** a network interceptor recording all outbound requests
- **When** The screen loads and is left idle
- **Then**
  - Zero HTTP requests are made
  - The list renders entirely from local notification records

> Rewritten 2026-08-06. This previously read: "`SignalRepository` is injected alongside
> `NotificationRepository` … `GET /obp/v6.0.0/signal/channels` resolves the available FCM
> channels". OBIE has no notification resource — no channel list, no per-transaction alert.
> Notifications come from Firebase, driven by records this app derives from its own AIS polling.
> A fetch here would give the screen a loading state and a failure mode it does not have.

The operational point survives the rewrite, strengthened: a push-configuration lookup can never
block the list a customer opened the screen to read, because there is no lookup.

---

## Traceability

| Action | Scenario | Destination |
|--------|----------|-------------|
| `open_notification` | TC-NOTIF-006 | not declared |
| `mark_all_read` | TC-NOTIF-007, -008 | local datastore |
| `open_notification_settings` | TC-NOTIF-009 | not declared |
| `RetryLoad` | TC-NOTIF-012 | — |

Two of four actions fire events with no declared destination.

---

_Generated by /idea-feature-test-export | 2026-08-04_
