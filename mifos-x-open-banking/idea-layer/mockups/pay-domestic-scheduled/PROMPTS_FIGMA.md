# pay-domestic-scheduled — Figma Design Prompt

> Generated from `screens/pay-domestic-scheduled/ui.yaml` by `/idea export --mockup`
> Design System: Open Banking — Trust Blue (Material Design 3)
> Tokens: design-tokens.yaml v2.4.0 · DESIGN.md v1.4.0
> Feature: Pay on a date (domestic scheduled payment)

---

## 1. Frame Setup

- **Frame**: Android (412 × 892dp) · iPhone 14 Pro (393 × 852dp)
- **Grid**: 4-column, 16dp gutter, 16dp margin
- **Status bar**: 54dp height (system)
- **Top app bar**: 56dp height
- **Bottom nav**: 80dp height (`bottom_nav: true`)
- **Safe area**: Top 54dp, Bottom 34dp (home indicator)
- **Usable content height**: 892 − 54 − 56 − 80 − 34 = 668dp (Android)
- **Scroll**: Content region scrolls; TopAppBar + BottomNav are sticky

---

## 2. Design Token Variables

Create as Figma Local Variables (separate Light and Dark mode collections).

### Colors — Light Mode

| Variable Name | Value | Usage |
|---|---|---|
| `color/primary` | `#266489` | Confirm button, active step dot, active nav tab, calendar selected date |
| `color/onPrimary` | `#FFFFFF` | Text on confirm button, selected calendar date number |
| `color/primaryContainer` | `#C9E6FF` | Selected step indicator chip background |
| `color/onPrimaryContainer` | `#004B6F` | Text on selected step chip |
| `color/secondary` | `#50606E` | Beneficiary list icon tint |
| `color/secondaryContainer` | `#D3E5F5` | `no_funds_check_note` banner background |
| `color/onSecondaryContainer` | `#384956` | `no_funds_check_note` banner text and icon |
| `color/surface` | `#F7F9FF` | Screen background, list item background |
| `color/surfaceContainerLow` | `#F1F4F9` | review_card background |
| `color/surfaceContainerHigh` | `#E5E8ED` | Bottom nav background |
| `color/surfaceVariant` | `#DDE3EA` | `amend_notice` banner background, `instruction_established` chip bg |
| `color/onSurface` | `#181C20` | Primary text: titles, row values, amount |
| `color/onSurfaceVariant` | `#41474D` | Supporting text, helper text, `amend_notice` text, `date_normalisation_note`, `instruction_established` chip text |
| `color/outline` | `#72787E` | TextField default border, inactive stepper step border |
| `color/outlineVariant` | `#C1C7CE` | Calendar disabled date numbers (decorative only — never on controls) |
| `color/error` | `#BA1A1A` | Error state icon, error text, field error outline |
| `color/errorContainer` | `#FFDAD6` | Error banner background |
| `color/onErrorContainer` | `#93000A` | Error banner text |

### Colors — Dark Mode

| Variable Name | Value | Usage |
|---|---|---|
| `color/primary` | `#95CDF7` | As above |
| `color/onPrimary` | `#00344E` | As above |
| `color/primaryContainer` | `#004B6F` | As above |
| `color/onPrimaryContainer` | `#C9E6FF` | As above |
| `color/secondaryContainer` | `#384956` | As above |
| `color/onSecondaryContainer` | `#D3E5F5` | As above |
| `color/surface` | `#101417` | As above |
| `color/surfaceContainerLow` | `#181C20` | As above |
| `color/surfaceContainerHigh` | `#262A2E` | As above |
| `color/surfaceVariant` | `#41474D` | As above |
| `color/onSurface` | `#E0E3E8` | As above |
| `color/onSurfaceVariant` | `#C1C7CE` | As above |
| `color/outline` | `#8B9198` | As above |
| `color/error` | `#FFB4AB` | As above |

### Typography

| Style Name | Font | Size (sp) | Weight | Line Height (sp) |
|---|---|---|---|---|
| `type/displaySmall` | Roboto | 36 | 400 | 44 |
| `type/headlineSmall` | Roboto Mono | 24 | 400 | 32 | ← amount field input |
| `type/titleLarge` | Roboto | 22 | 400 | 28 | ← screen title |
| `type/titleMedium` | Roboto | 16 | 500 | 24 | ← section headings (Pay from, Pay to) |
| `type/titleSmall` | Roboto | 14 | 500 | 20 | ← review card row labels |
| `type/bodyLarge` | Roboto | 16 | 400 | 24 | ← list primary text, review values |
| `type/bodyMedium` | Roboto | 14 | 400 | 20 | ← supporting text, banner body |
| `type/bodySmall` | Roboto | 12 | 400 | 16 | ← helper text, date_normalisation_note |
| `type/labelLarge` | Roboto | 14 | 500 | 20 | ← button labels |
| `type/labelSmall` | Roboto | 11 | 500 | 16 | ← stepper step labels |
| `type/mono/amount` | Roboto Mono | 24 | 400 | 32 | ← amount field — digits must not reflow |

### Spacing

| Token | Value (dp) | Usage |
|---|---|---|
| `spacing/xs` | 4 | Intra-stepper gap |
| `spacing/sm` | 8 | Field error text offset, inner row gap |
| `spacing/md` | 16 | Screen padding, component gap, section gap |
| `spacing/lg` | 24 | Error state gap between icon / title / body |
| `spacing/xl` | 32 | Empty state vertical padding |

### Corner Radius

| Token | Value (dp) | Usage |
|---|---|---|
| `radius/sm` | 8 | TextField, DatePicker frame, AmountField |
| `radius/md` | 12 | Cards (review_card, account list item), banners |
| `radius/full` | 9999 | confirm_button (pill), "Enter sort code…" outlined button |

---

## 3. Auto Layout Structure

### content state — Step 4: Date (the new step, most distinctive frame to spec)

```
Frame: pay_domestic_scheduled_date_step (412 × 892, Auto Layout Vertical, clip)
  ├─ StatusBar (Fill × 54dp, surfaceContainerHigh) — system component
  │
  ├─ TopAppBar (Fill × 56dp, surfaceContainerHigh, Auto Layout Horizontal, pad 4/4)
  │   ├─ BackIconButton (48 × 48, ripple on tap)
  │   │   └─ Icon: arrow_back (24dp, onSurface)
  │   └─ Title "Pay on a date" (type/titleLarge, onSurface, Fill, padding-left 4dp)
  │
  ├─ Stepper (Fill × 40dp, Auto Layout Horizontal, padding 16/16, gap 4dp)
  │   ├─ StepChip_account   (Hug × 28dp, Auto Layout Horizontal, radius/full)
  │   │   Fill: primaryContainer (completed step)  Text: "Account" (labelSmall, onPrimaryContainer)
  │   ├─ StepConnector (8dp × 1dp, outlineVariant)
  │   ├─ StepChip_payee     (Hug × 28dp, radius/full, primaryContainer) "Payee"
  │   ├─ StepConnector (8dp × 1dp, outlineVariant)
  │   ├─ StepChip_amount    (Hug × 28dp, radius/full, primaryContainer) "Amount"
  │   ├─ StepConnector (8dp × 1dp, outlineVariant)
  │   ├─ StepChip_date      (Hug × 28dp, radius/full, primary) "Date" ← ACTIVE
  │   │   Fill: primary  Text: "Date" (labelSmall, onPrimary)
  │   ├─ StepConnector (8dp × 1dp, outlineVariant)
  │   └─ StepChip_review    (Hug × 28dp, radius/full, outline border, transparent fill) "Review"
  │       Border: 1dp outline  Text: "Review" (labelSmall, onSurfaceVariant)
  │
  ├─ ScrollContent (Fill, Auto Layout Vertical, padding 16dp, gap 16dp)
  │   ├─ SectionLabel "Payment date" (type/titleMedium, onSurface)
  │   │
  │   ├─ DatePicker_execution_date_picker (Fill, radius/sm, outline 1dp, surfaceContainerLow)
  │   │   ─ Month header row: "< August 2026 >" (titleMedium, onSurface, auto layout horizontal)
  │   │   ─ Weekday header row: "Mo Tu We Th Fr Sa Su" (labelSmall, onSurfaceVariant)
  │   │   ─ Date grid (7 columns × ~6 rows, 44dp cell min)
  │   │     ├─ Disabled cell (today, past dates): outlineVariant text, no tap affordance
  │   │     ├─ Disabled cell (T+366+): outlineVariant text, no tap affordance
  │   │     ├─ Available cell (T+1..T+365, incl Sat/Sun): onSurface text, ripple on tap
  │   │     └─ Selected cell (chosen date): primary fill circle, onPrimary text
  │   │
  │   └─ Text_date_normalisation_note (Fill, type/bodySmall, onSurfaceVariant)
  │       Content: "Your payment will be made on the date you choose. The bank does not
  │                 guarantee a time of day."
  │
  ├─ NextButton (Fill × 56dp, primary fill, radius/full, padding 16/24, margin 16dp)
  │   Disabled state (no date chosen): opacity 0.38
  │   Label: "Next" (labelLarge, onPrimary)
  │
  └─ BottomNav (Fill × 80dp, surfaceContainerHigh, Auto Layout Horizontal)
      ├─ NavItem "Home"     (icon.md home_outlined, labelSmall, onSurfaceVariant)
      ├─ NavItem "Accounts" (icon.md account_balance_wallet_outlined, onSurfaceVariant)
      ├─ NavItem "Pay"      (icon.md payments_filled, labelSmall, primary) ← ACTIVE
      └─ NavItem "More"     (icon.md more_horiz, onSurfaceVariant)
```

### content state — Step 5: Review

```
Frame: pay_domestic_scheduled_review_step (412 × 892, Auto Layout Vertical, clip)
  ├─ StatusBar + TopAppBar (same as above, title "Pay on a date")
  ├─ Stepper (all 5 steps completed — Date chip = primaryContainer like Account/Payee/Amount; Review = active/primary)
  ├─ ScrollContent (Fill, Auto Layout Vertical, padding 16dp, gap 16dp)
  │   │
  │   ├─ ReviewCard_review_card (Fill, surfaceContainerLow, radius/md, elevation 1)
  │   │   Auto Layout Vertical, padding 16dp, gap 0
  │   │   ├─ ReviewRow "From" / "Current Account · 40-20-01" (titleSmall / bodyLarge, gap 8dp between label+value)
  │   │   ├─ Divider (outlineVariant, 1dp, decorative)
  │   │   ├─ ReviewRow "To"   / "Ramu · ••••3351"
  │   │   ├─ Divider
  │   │   ├─ ReviewRow "Amount" / "£1.01" (bodyLarge, mono)
  │   │   ├─ Divider
  │   │   ├─ ReviewRow "Date"   / "13 August 2026"  ← date only, NO time of day
  │   │   ├─ Divider
  │   │   ├─ ReviewRow "Reference" / "Rent"         ← hidden if blank
  │   │   ├─ Divider
  │   │   └─ ReviewRow "Fee"  / "£0.05"             (bodyLarge, mono)
  │   │
  │   ├─ Banner_no_funds_check_note (Fill, secondaryContainer, radius/md, Auto Layout Horizontal, padding 12/16, gap 12dp)
  │   │   ├─ Icon: info (icon.md, onSecondaryContainer)
  │   │   └─ Text "We cannot check whether funds will be available on the payment date.
  │   │           The bank will attempt the payment on the chosen date." (bodyMedium, onSecondaryContainer)
  │   │
  │   └─ Banner_amend_notice (Fill, surfaceVariant, radius/md, Auto Layout Horizontal, padding 12/16, gap 12dp)
  │       ├─ Icon: info (icon.md, onSurfaceVariant)
  │       └─ Text "Once scheduled, this payment cannot be changed or cancelled through this app.
  │               To amend or cancel, use your bank's own app or online banking."
  │               (bodyMedium, onSurfaceVariant)
  │
  ├─ ConfirmButton_confirm_button (Fill × 56dp, primary fill, radius/full, padding 16/24, margin 16dp)
  │   Label: "Schedule payment" (labelLarge, onPrimary)
  │   — NEVER "Send £1.01" — this is a deferred instruction, not an immediate transfer
  │
  └─ BottomNav (same as above)
```

### loading state

```
Frame: pay_domestic_scheduled_loading (412 × 892, Auto Layout Vertical, clip)
  ├─ StatusBar + TopAppBar (same chrome)
  ├─ Stepper_shimmer (Fill × 40dp, surfaceContainerLow, shimmer animation, radius/full)
  ├─ ScrollContent (Fill, Auto Layout Vertical, padding 16dp, gap 16dp)
  │   ├─ Shimmer_label (Fill × 20dp, surfaceContainerLow, radius/sm)
  │   ├─ Shimmer_list_item_1 (Fill × 72dp, surfaceContainerLow, radius/md)
  │   ├─ Shimmer_list_item_2 (Fill × 72dp, surfaceContainerLow, radius/md)
  │   └─ Shimmer_note (Fill × 16dp, 60% width, surfaceContainerLow, radius/sm)
  └─ BottomNav (same)
```

Shimmer: animation 1.5s loop, left-to-right gradient from `surfaceContainerLow` to `surfaceContainer`.

### submitting state

```
Frame: pay_domestic_scheduled_submitting (412 × 892, Auto Layout Vertical, clip)
  ├─ StatusBar + TopAppBar (same chrome)
  ├─ Stepper (same 5-step, Review step as active/primary)
  ├─ ProgressContent (Fill, Auto Layout Vertical, center, gap 16dp, padding 48dp top)
  │   ├─ CircularProgressIndicator (48 × 48dp, primary stroke 4dp)
  │   └─ ProgressLabel "Setting up your scheduled payment…" (bodyMedium, onSurfaceVariant, center)
  │       Variant B: "Waiting for authorisation…"
  │       Variant C: "Scheduling your payment…"
  └─ BottomNav (same)
```

### error state

```
Frame: pay_domestic_scheduled_error (412 × 892, Auto Layout Vertical, clip)
  ├─ StatusBar + TopAppBar (same chrome)
  ├─ Stepper (persists; step depends on where error occurred)
  ├─ ErrorContent (Fill, Auto Layout Vertical, center, gap 16dp, padding 32dp top)
  │   ├─ Icon: error_outline (48 × 48dp, error color)
  │   ├─ ErrorTitle (type/headlineSmall, onSurface, center)  e.g. "No connection"
  │   ├─ ErrorBody (type/bodyMedium, onSurfaceVariant, center, max-width 300dp)
  │   │   e.g. "Check your internet connection and try again."
  │   └─ (if retryable) RetryButton (Hug × 48dp, primary fill, radius/full, padding 16/24)
  │       Label: "Try again" (labelLarge, onPrimary)
  └─ BottomNav (same)
```

---

## 4. Component Variants

### DatePicker (execution_date_picker)

**Variant Properties**:
| Property | Values |
|---|---|
| Day state | Available, Selected, Today-disabled, Past-disabled, Future-disabled |
| Week grid | 7 columns |

**Specifications**:
- Width: Fill (container inset 16dp each side → ~380dp inner on 412dp frame)
- Cell size: min 44dp × 44dp (touch target compliance)
- Corner: selected day → `radius/full` circle
- Month nav: `<` / `>` icon buttons (48dp touch target each)

**Day state styles**:
| State | Fill | Text color | Touch |
|---|---|---|---|
| Available | transparent | `onSurface` | Ripple on tap |
| Selected | `primary` circle | `onPrimary` | None (already selected) |
| Today / past | transparent | `outlineVariant` | None — disabled |
| T+366+ | transparent | `outlineVariant` | None — disabled |
| Saturday/Sunday | transparent | `onSurface` | Ripple on tap (weekends selectable) |

### ReviewCard Row

**Specifications**:
- Width: Fill
- Height: 48dp min (each row)
- Padding: 12dp vertical, 16dp horizontal
- Auto Layout: Horizontal, Space-between
- Left: `type/titleSmall` (`onSurfaceVariant`)
- Right: `type/bodyLarge` (`onSurface`); amount and fee use `Roboto Mono`
- Divider between rows: `outlineVariant`, 1dp, decorative (W-32 — not on control)

### Banner (no_funds_check_note + amend_notice)

**Specifications**:
- Width: Fill
- Padding: 12dp top/bottom, 16dp left/right
- Gap (icon to text): 12dp
- Corner: `radius/md` (12dp)
- Icon size: `icon/md` (24dp)
- Min height: 56dp

| Banner | Fill | Text/icon | Contrast |
|---|---|---|---|
| `no_funds_check_note` | `secondaryContainer` (#D3E5F5) | `onSecondaryContainer` (#384956) | 7.22:1 |
| `amend_notice` | `surfaceVariant` (#DDE3EA) | `onSurfaceVariant` (#41474D) | 7.28:1 |

### Confirm Button (confirm_button)

**Specifications**:
- Width: Fill (inset 16dp each side)
- Height: 56dp min (M3 comfortable)
- Corner: `radius/full` (pill)
- Fill: `primary` (#266489 light / #95CDF7 dark)
- Label: "Schedule payment" (`labelLarge`, `onPrimary`)
- Disabled: opacity 0.38 (not shown on Review — button is always enabled once date is chosen)
- Pressed: ripple + slight elevation raise
- Focus: 2dp `outline` border

**Interactive states**:
| State | Background | Border | Opacity |
|---|---|---|---|
| Default | `primary` | none | 100% |
| Pressed | `primary` + ripple | none | 100% |
| Focused | `primary` | 2dp `outline` | 100% |
| Disabled | `onSurface` | none | 38% |

### instruction_established Status Chip (success state, payment-status screen)

Though rendered by payment-status, specified here as it maps to scheduled-payment outcomes:

**Specifications**:
- Width: Hug
- Height: 32dp
- Corner: `radius/full`
- Fill: `surfaceVariant` (#DDE3EA light / #41474D dark)
- Text: `onSurfaceVariant` (#41474D light / #C1C7CE dark) · `labelMedium`
- Leading icon: `event_repeat` (20dp, `onSurfaceVariant`)
- Text content: "Scheduled for 13 August 2026" (names the instruction, not the money)
- Contrast: 7.28:1 (W-30) — WCAG AA pass

---

## 5. Assets Required

### Icons (Material Symbols — Outlined unless noted)

| Icon | Size | Usage | Style |
|---|---|---|---|
| `arrow_back` | 24dp | Top app bar back navigation | Outlined |
| `account_balance` | 24dp | Account list item leading icon | Outlined |
| `person` | 24dp | Beneficiary list item leading icon | Outlined |
| `navigate_next` | 24dp | Account / beneficiary row trailing (optional) | Outlined |
| `info` | 24dp | Banner icon (no_funds_check_note, amend_notice) | Outlined |
| `event_repeat` | 20dp | instruction_established status chip | Outlined |
| `error_outline` | 48dp | Error state hero icon | Outlined |
| `home_outlined` | 24dp | Bottom nav Home tab | Outlined |
| `account_balance_wallet_outlined` | 24dp | Bottom nav Accounts tab | Outlined |
| `payments` | 24dp | Bottom nav Pay tab (active) | Filled |
| `more_horiz` | 24dp | Bottom nav More tab | Outlined |

---

## 6. Mood Palette Usage

| Mood Color | Value | Component(s) | Notes |
|---|---|---|---|
| `mood_gradients.hero.light` | `["#C9E6FF", "#F7F9FF"]` | Not used in this screen | Mood gradient unused in form flows; form uses flat surface |
| `mood_gradients.accent.light` | `["#266489", "#50606E"]` | Not used | Same — reserved for marketing / splash surfaces |

Both mood gradients are intentionally unused on this form screen. The minimalist-ui aesthetic and
form archetype use flat surfaceContainer hierarchy, not gradient washes. Mark as
`unused: true, reason: form-archetype-flat-surface` to satisfy RULE-MOODPALETTE-USAGE-001.

---

## 7. WCAG Contrast Audit

| Text Token | Background Token | Light Ratio | Dark Ratio | Required | Pass? |
|---|---|---|---|---|---|
| `onPrimary` on `primary` | confirm button | 5.04:1 | 8.42:1 | 4.5:1 | Pass |
| `onSurface` on `surface` | body text | 15.0:1 | 13.0:1 | 4.5:1 | Pass |
| `onSurfaceVariant` on `surface` | supporting text | 7.28:1 | 5.52:1 | 4.5:1 | Pass |
| `onSurfaceVariant` on `surfaceVariant` | amend_notice | 7.28:1 | 5.52:1 | 4.5:1 | Pass (W-30) |
| `onSecondaryContainer` on `secondaryContainer` | no_funds_check_note | 7.22:1 | 7.22:1 | 4.5:1 | Pass |
| `onPrimaryContainer` on `primaryContainer` | active step chip | 7.27:1 | 7.27:1 | 4.5:1 | Pass |
| `error` on `surface` | error state text | 6.14:1 | 10.90:1 | 4.5:1 | Pass |
| `outline` on `surface` | TextField default border | 4.24:1 | 5.82:1 | 3.0:1 (UI component) | Pass |
| `outlineVariant` on `surface` | calendar disabled dates | 1.62:1 | 1.97:1 | decorative | Permitted (W-32) |

Note: `outlineVariant` on `surface` (1.62:1) FAILS WCAG 1.4.11. Permitted for the calendar's
disabled date numbers only, which are purely decorative (the disabled state is also communicated by
the lack of a touch affordance and the month-boundary context). Never use `outlineVariant` text
for a control glyph or actionable label.

---

## 8. Animation Specs

| Motion | Duration | Easing | Android | iOS |
|---|---|---|---|---|
| Step advance (slide left) | 300ms | `cubic-bezier(0.2, 0, 0, 1.0)` | `FastOutSlowInInterpolator` | `CAMediaTimingFunction(.2, 0, 0, 1)` |
| Step back (slide right) | 300ms | `cubic-bezier(0.2, 0, 0, 1.0)` | `FastOutSlowInInterpolator` | Same |
| Shimmer loop | 1500ms | linear | `LinearInterpolator` | `CABasicAnimation` linear |
| Calendar day select | 150ms | `cubic-bezier(0.2, 0, 0, 1.0)` | `FastOutSlowInInterpolator` | Same |
| Banner appear | 150ms | `cubic-bezier(0.2, 0, 0, 1.0)` | `FastOutSlowInInterpolator` | Same |

Low-motion override: all durations reduce to 0ms when `prefers-reduced-motion` / `Animator.DURATION_SCALE == 0`.
This design system declares `motion.intensity: low` — no decorative animations, no bouncing.

---

## 9. Responsive Variants

| Breakpoint | Layout |
|---|---|
| Compact (< 600dp) | Single column, full-width cards, 16dp margin — primary target |
| Medium (600–840dp) | Same single column, max-width 560dp, centred |
| Expanded (> 840dp) | Max-width 640dp, centred; DatePicker may use grid layout if space allows |

Date picker is always full-width within its container. Do not switch to a 3-column calendar grid
on compact — the touch targets must stay ≥ 44dp regardless of screen width.
