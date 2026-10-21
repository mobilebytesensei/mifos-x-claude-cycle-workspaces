# Visual Specification — Notifications

| Field | Value |
|---|---|
| Feature | notifications |
| Flavor | consumer |
| Archetype | index_list |
| States | loading, populated, empty, error |

---

## Screen Layout (Populated State)

Top app bar: "Notifications" title, arrow_back navigation icon, done_all action ("Mark all as read"), tune action ("Notification settings"). No bottom navigation bar. Scrollable single-column list on `surface` background.

```
┌─────────────────────────────────────────────┐
│  ← Notifications                  ✓✓  ⚙    │  ← Top app bar
├─────────────────────────────────────────────┤
│                                             │
│  Notifications                Mark All Read │  ← Header row
│                                             │
│  TODAY                                      │  ← Section header
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ ●  [↓]  Payment received           ● ● │ │  ← Unread card
│ │         Payment of £50.00 received      │ │     (`primary_container`)
│ │         from James Wilson               │ │
│ │         10 min ago                      │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ ●  [✓]  KYC verification approved  ● ● │ │  ← Unread card
│ │         Your identity has been verified. │ │     (`primary_container`)
│ │         You now have full access.        │ │
│ │         1 hr ago                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│  EARLIER                                    │  ← Section header
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │    [↻]  Direct debit mandate created    │ │  ← Read card
│ │         Direct debit mandate created for│ │     (`surface`)
│ │         Netflix — £15.99/month from     │ │
│ │         your Current Account. 3 hr ago  │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │    [↓]  Salary credited                 │ │  ← Read card
│ │         £3,200.00 from Acme Ltd has     │ │     (`surface`)
│ │         been credited to your Current   │ │
│ │         Account. Yesterday              │ │
│ └─────────────────────────────────────────┘ │
│                                             │  ← spacing.lg bottom spacer
└─────────────────────────────────────────────┘
```

Legend: `● ●` = unread dot (10×10, `primary`) | `[↓]` = payment icon | `[✓]` = verified_user icon | `[↻]` = autorenew icon

---

## Components

### Header Row
- **Layout:** Horizontal, space-between, center-aligned
- **Padding:** horizontal `spacing.md`, top `spacing.md`, bottom `spacing.sm`
- **Title:** "Notifications" — `headlineLarge`, `primary`, bold
- **Button:** "Mark All Read" — text variant, `secondary`, `labelMedium`, no horizontal padding

### Section Headers

**Today**
- typography: `labelMedium`, `on_surface_variant`, semi-bold
- padding: horizontal `spacing.md`, top `spacing.sm`, bottom `spacing.xs`

**Earlier**
- typography: `labelMedium`, `on_surface_variant`, semi-bold
- padding: horizontal `spacing.md`, top `spacing.md`, bottom `spacing.xs`

---

### Notification Card — Payment of £50.00 from James Wilson (Unread, payment)

**Container**
- Background: `primary_container` — unread signal
- Border: `outline`, `border.thin`
- Corner radius: `radius.lg`
- Padding: horizontal `spacing.md`, vertical `spacing.md`
- Margin: horizontal `spacing.md`, bottom `spacing.sm`
- Tap action: open_notification → transaction-detail

**Internal row (horizontal, spacing `spacing.md`, align: flex_start)**

Icon circle
- Size: 44×44 dp, radius `radius.full`
- Background: `primary` — incoming money (credit)
- Icon: arrow_downward, `icon.md`, `on_primary`

Text column (flex: 1)
- Title: "Payment received" — `bodyMedium`, `on_primary_container`, semi-bold (maximum contrast = unread)
- Body: "Payment of £50.00 received from James Wilson" — `bodySmall`, `on_primary_container`, amount in Roboto Mono
- Timestamp: "10 min ago" — `labelSmall`, `on_primary_container`

Unread dot
- Size: 10×10 dp, radius `radius.full`
- Color: `primary`
- Align: flex_start, margin_top `spacing.xs`
- Accessibility role: status, content_description: "Unread notification"

---

### Notification Card — KYC Verification Approved (Unread, security)

**Container**
- Background: `primary_container`, border `outline` — same unread style
- Tap action: open_notification → kyc-review (cross-persona deep link)

**Internal row**

Icon circle
- Background: `secondary` — identity/trust, distinguished from the money-in circles
- Icon: verified_user, `icon.md`, `on_secondary`

Text column
- Title: "KYC verification approved" — `bodyMedium`, `on_primary_container`, semi-bold
- Body: "Your identity has been verified. You now have full access to all account features." — `bodySmall`, `on_primary_container`
- Timestamp: "1 hr ago" — `labelSmall`, `on_primary_container`

Unread dot: same as above

---

### Notification Card — Netflix Direct Debit Mandate (Read, system)

**Container**
- Background: `surface` — read signal
- Border: `outline`, `border.thin`
- Corner radius: `radius.lg`
- Padding: horizontal `spacing.md`, vertical `spacing.md`
- Margin: horizontal `spacing.md`, bottom `spacing.sm`
- Tap action: open_notification → accounts

**Internal row**

Icon circle
- Background: `surface_container` — scheduled/system, informational
- Icon: autorenew, `icon.md`, `on_surface_variant`

Text column
- Title: "Direct debit mandate created" — `bodyMedium`, `on_surface_variant`, semi-bold (reduced contrast = read)
- Body: "Direct debit mandate created for Netflix — £15.99/month from your Current Account." — `bodySmall`, `on_surface_variant`
- Timestamp: "3 hr ago" — `labelSmall`, `on_surface_variant`
- No unread dot

---

### Notification Card — Acme Ltd Salary Credited (Read, payment)

**Container**
- Same read card style as Netflix card
- Tap action: open_notification → transaction-detail

**Internal row**

Icon circle
- Background: `surface_container` — receded because the item is read
- Icon: arrow_downward, `icon.md`, `on_surface_variant`

Text column
- Title: "Salary credited" — `bodyMedium`, `on_surface_variant`, semi-bold
- Body: "£3,200.00 from Acme Ltd has been credited to your Current Account." — `bodySmall`, `on_surface_variant`, amount in Roboto Mono
- Timestamp: "Yesterday" — `labelSmall`, `on_surface_variant`
- No unread dot

---

## State Variants

### Loading State

Top app bar visible. Header row (title only, no "Mark All Read" button). Four shimmer skeleton cards stacked vertically, each with:
- `surface_container` rectangle (44×44 dp) for icon circle
- Two `surface_container` rounded rectangles for title + body lines
- One short `surface_container` line for timestamp

### Empty State

Top app bar visible. Header row (title only). Centered column:
- Icon: notifications_none_outlined, 64 dp, `outline`
- Title: "You're all caught up" — `headlineSmall`, `on_surface`
- Message: "No new notifications. We'll let you know about payments, alerts and updates." — `bodyMedium`, `on_surface_variant`, centered, max_width 280 dp

### Error State

Top app bar visible. Header row (title only). Centered column:
- Icon: cloud_off, 64 dp, `outline`
- Title: "Unable to load notifications" — `headlineSmall`, `on_surface`
- Message: "Check your connection and try again" — `bodyMedium`, `on_surface_variant`
- Retry button: "Try again" — outlined, `primary`, margin_top `spacing.md`, tap → RetryLoad

---

## Interaction Patterns

| Target | Gesture | Action | Navigation |
|---|---|---|---|
| notification_payment_james | Tap | open_notification | → transaction-detail |
| notification_kyc_approved | Tap | open_notification | → kyc-review (cross-persona) |
| notification_netflix_mandate | Tap | open_notification | → accounts |
| notification_salary_credited | Tap | open_notification | → transaction-detail |
| mark_all_read_button | Tap | mark_all_read | All unread dots removed; card backgrounds → `surface` |
| Top app bar done_all | Tap | mark_all_read | Same as button |
| Top app bar tune | Tap | open_notification_settings | → settings |
| Top app bar back arrow | Tap | navigate_back | → home |

---

## Content Data

| # | Category | Icon | Icon Role | Title | Body | Time | State |
|---|---|---|---|---|---|---|---|
| 1 | payment | arrow_downward | `primary` | "Payment received" | "Payment of £50.00 received from James Wilson" | 10 min ago | Unread |
| 2 | security | verified_user | `secondary` | "KYC verification approved" | "Your identity has been verified. You now have full access to all account features." | 1 hr ago | Unread |
| 3 | system | autorenew | `surface_container` | "Direct debit mandate created" | "Direct debit mandate created for Netflix — £15.99/month from your Current Account." | 3 hr ago | Read |
| 4 | payment | arrow_downward | `surface_container` | "Salary credited" | "£3,200.00 from Acme Ltd has been credited to your Current Account." | Yesterday | Read |

---

## Design Notes

**Unread vs read visual system — triple signal for accessibility:**
- Unread: `primary_container` background + `outline` border + `primary` unread dot + `on_primary_container` text.
- Read: `surface` background + `outline` border + no dot + `on_surface_variant` text.
- Three simultaneous signals ensure the read/unread distinction is perceived even when colour alone is unavailable.

**Section grouping rationale:**
- "Today" = notifications received since midnight — drives urgency; the user expects to act on these.
- "Earlier" = older read notifications — reference only; lower visual weight confirms no action needed.

**Category icon semantics stay inside the palette:**
- `primary` — money in (payment received, salary credited). This palette maps credit to the trust-blue and ships no green; the `arrow_downward` glyph carries the direction.
- `secondary` — trust/identity events (KYC, security). Neutral slate reads as procedural rather than financial.
- `surface_container` — scheduled/system actions (direct debit mandates). Informational, so it takes no coloured role at all.
- Read cards mute their icon circle to `surface_container` regardless of category: once consumed, the item's category matters less than its state, and this keeps the read row visually quiet.

**Typography hierarchy:**
- Unread title: `bodyMedium` semi-bold in `on_primary_container` — maximum contrast, priority reading.
- Read title: `bodyMedium` semi-bold in `on_surface_variant` — same weight, lower contrast = consumed state.
- All body text: `bodySmall` — compact enough to show the full notification message without truncation.
- All timestamps: `labelSmall` — minimal visual weight. Monetary figures in body text use Roboto Mono per the `amount` component contract.

**"Mark All Read" placement:**
- Inline text button in `secondary` (not `primary`) to signal utility rather than a primary CTA.
- Mirrored in the top app bar `done_all` icon for thumb-reach accessibility on large screens.

**Accessibility:**
- Each card has a comprehensive a11y content_description including read state, title, message, and relative age.
- Unread dot: role="status" with "Unread notification" description.
- All card tap targets span the full card width for thumb reach.
- Minimum touch target `touch_targets.comfortable` (48×48 dp), which the card padding guarantees.

---

*Generated by /idea export | 2026-08-03*
