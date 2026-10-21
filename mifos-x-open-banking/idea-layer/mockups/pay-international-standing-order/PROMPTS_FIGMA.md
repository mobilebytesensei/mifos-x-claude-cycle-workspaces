# Overseas Standing Order — Figma Design Prompt

> Source: `screens/pay-international-standing-order/ui.yaml` + `design-tokens.yaml` v2.4.0
> Design system: Open Banking — Trust Blue · Material Design 3
> Figma project: 17153754672098888646 · Design system: 2047482829824847747

---

## 1. Frame Setup

- **Frame**: iPhone 14 Pro (393 x 852dp) / Android reference (412 x 892dp)
- **Grid**: 4-column, gutter 16dp, margin 16dp (= `spacing.md`)
- **Status bar**: 54dp (system)
- **Top app bar**: 56dp — title "Overseas standing order", back arrow, no trailing actions
- **Bottom nav**: 80dp — tabs: Home / Accounts / Pay / More
- **Safe area**: top 54dp, bottom 34dp (home indicator)
- **Scroll content**: fills between top app bar and bottom nav

---

## 2. Design Token Variables

Create as Figma Local Variables — link to the design system file 2047482829824847747.

### Colors (Light Mode)

| Variable Name | Value | Usage |
|---|---|---|
| `color/primary` | `#266489` | CTA fill, stepper active dot, amount field focus ring |
| `color/onPrimary` | `#FFFFFF` | CTA label, icon on primary fill |
| `color/primaryContainer` | `#C9E6FF` | payment_disposition.terminal_success chip background |
| `color/onPrimaryContainer` | `#004B6F` | terminal_success chip text |
| `color/secondary` | `#50606E` | submitting_indicator label, secondary text emphasis |
| `color/secondaryContainer` | `#D3E5F5` | deferred_charge_note info banner container |
| `color/onSecondaryContainer` | `#384956` | deferred_charge_note info banner text |
| `color/tertiary` | `#64597B` | warning icon, fx_not_fixed_notice / amend_notice icon |
| `color/tertiaryContainer` | `#EADDFF` | fx_not_fixed_notice / amend_notice banner container |
| `color/onTertiaryContainer` | `#4C4162` | fx_not_fixed_notice / amend_notice banner text |
| `color/error` | `#BA1A1A` | error_panel text, validation error, field error ring |
| `color/errorContainer` | `#FFDAD6` | error_panel container |
| `color/onErrorContainer` | `#93000A` | error_panel text on container |
| `color/surface` | `#F7F9FF` | screen background |
| `color/onSurface` | `#181C20` | primary text, review_card row values |
| `color/surfaceContainer` | `#EBEEF3` | review_card / summary_card background |
| `color/surfaceVariant` | `#DDE3EA` | instruction_established chip background |
| `color/onSurfaceVariant` | `#41474D` | helper text, field labels, secondary content, instruction_established chip text |
| `color/outline` | `#72787E` | text_field default border |
| `color/outlineVariant` | `#C1C7CE` | dividers (non-interactive only — fails WCAG on text) |

### Colors (Dark Mode)

| Variable Name | Value |
|---|---|
| `color/primary` | `#95CDF7` |
| `color/onPrimary` | `#00344E` |
| `color/primaryContainer` | `#004B6F` |
| `color/onPrimaryContainer` | `#C9E6FF` |
| `color/tertiary` | `#CFC0E8` |
| `color/tertiaryContainer` | `#4C4162` |
| `color/onTertiaryContainer` | `#EADDFF` |
| `color/error` | `#FFB4AB` |
| `color/errorContainer` | `#93000A` |
| `color/onErrorContainer` | `#FFDAD6` |
| `color/surface` | `#101417` |
| `color/onSurface` | `#E0E3E8` |
| `color/surfaceContainer` | `#1C2024` |
| `color/onSurfaceVariant` | `#C1C7CE` |
| `color/outline` | `#8B9198` |

### Typography

| Style | Font | Size (sp) | Weight | Line height (sp) |
|---|---|---|---|---|
| headlineSmall | Roboto | 24 | 400 | 32 |
| titleLarge | Roboto | 22 | 400 | 28 |
| titleMedium | Roboto | 16 | 500 | 24 |
| bodyLarge | Roboto | 16 | 400 | 24 |
| bodyMedium | Roboto | 14 | 400 | 20 |
| bodySmall | Roboto | 12 | 400 | 16 |
| labelLarge | Roboto | 14 | 500 | 20 |
| labelMedium | Roboto | 12 | 500 | 16 |
| mono/amount | Roboto Mono | 24 | 400 | 32 |

`amount_field` uses `mono/amount` (headlineSmall scale, Roboto Mono) so digits do not reflow while typing.

### Spacing

| Token | dp |
|---|---|
| `spacing/xxs` | 2 |
| `spacing/xs` | 4 |
| `spacing/sm` | 8 |
| `spacing/md` | 16 |
| `spacing/lg` | 24 |
| `spacing/xl` | 32 |
| `spacing/xxl` | 48 |

### Corner Radius

| Token | dp |
|---|---|
| `radius/sm` | 8 — text_field inputs |
| `radius/md` | 12 — cards (review_card, summary_card) |
| `radius/lg` | 16 — sheets |
| `radius/xl` | 28 — large containers |
| `radius/full` | 9999 — confirm_button (filled_pill) |

---

## 3. Auto Layout Structure

### Content State — Recipient step (initial)

```
Frame: pay_iso_content_recipient (Fill × 852, Auto Layout Vertical)
  ├─ TopAppBar (Fill × 56, Auto Layout Horizontal, padding 4/16)
  │     ├─ IconButton: arrow_back (48dp touch target, icon 24dp, onSurface)
  │     └─ Title: "Overseas standing order" (titleLarge, onSurface, Fill)
  │
  ├─ ScrollContent (Fill, Auto Layout Vertical, padding: spacing.md, gap: spacing.lg)
  │     ├─ stepper#step_indicator (Fill, Auto Layout Horizontal, gap: spacing.sm)
  │     │     Dots: 5 steps · Active=1 (primary) · Inactive=outline
  │     │     Labels: "Recipient · Schedule · Amount · Charges · Review" (labelSmall)
  │     │
  │     ├─ text#no_debtor_note
  │     │     "The payment is taken from the account you pick at your bank when you authorise."
  │     │     bodySmall · onSurfaceVariant · Fill
  │     │
  │     ├─ text_field#iban_field (Fill × 56, radius.sm)
  │     │     Label: "Recipient IBAN" (bodySmall, onSurfaceVariant, floating)
  │     │     Helper: "e.g. FR29NWBK60161331926819" (bodySmall, onSurfaceVariant)
  │     │     Border: outline (default 1dp) → primary (focus 2dp)
  │     │
  │     ├─ text_field#payee_name_field (Fill × 56, radius.sm)
  │     │     Label: "Payee name" (bodySmall, onSurfaceVariant)
  │     │     Border: outline (1dp)
  │     │
  │     └─ text_field#bic_field (Fill × 56, radius.sm)
  │           Label: "Bank identifier code (BIC) — optional" (bodySmall, onSurfaceVariant)
  │           Helper: "11 characters if provided" (bodySmall, onSurfaceVariant)
  │           Border: outline (1dp)
  │
  └─ BottomNav (Fill × 80) — Home / Accounts / Pay (active, primary) / More
```

### Content State — Amount step

```
Frame: pay_iso_content_amount
  ├─ TopAppBar (same)
  ├─ ScrollContent (padding: spacing.md, gap: spacing.lg)
  │     ├─ stepper (step 3 active)
  │     │
  │     ├─ text_field#amount_field (Fill × 72, radius.sm)
  │     │     Prefix: currency symbol (bodyLarge, onSurfaceVariant — not editable)
  │     │     Input: headlineSmall scale · Font: Roboto Mono · onSurface
  │     │     Label: "Amount per payment" (bodySmall, onSurfaceVariant)
  │     │     Border: outline → primary (focus 2dp) → error (error 2dp)
  │     │
  │     ├─ [instructed_currency_picker] "You send: GBP" — dropdown / chip row
  │     ├─ [transfer_currency_picker]   "Recipient receives in: USD" — dropdown / chip row
  │     │
  │     ├─ banner#fx_not_fixed_notice (Fill, Auto Layout Vertical, radius.md)
  │     │     Background: tertiaryContainer
  │     │     Icon: schedule (24dp, tertiary) — left aligned
  │     │     Text: "The exchange rate is not fixed. Each payment converts at the
  │     │           rate applying on its own date — we cannot show you a rate,
  │     │           projected total, or estimated amount in advance."
  │     │           bodyMedium · onTertiaryContainer
  │     │     Padding: spacing.md all sides
  │     │
  │     └─ text#no_varying_amounts_note
  │           "Every payment is the same amount."
  │           bodySmall · onSurfaceVariant
  │
  └─ BottomNav
```

### Content State — Review step

```
Frame: pay_iso_content_review
  ├─ TopAppBar (same)
  ├─ ScrollContent (padding: spacing.md, gap: spacing.lg)
  │     ├─ stepper (step 5 active)
  │     │
  │     ├─ summary_card#review_card (Fill, Auto Layout Vertical, radius.md, elevation 1)
  │     │     Background: surfaceContainer
  │     │     Rows (Auto Layout Vertical, gap: spacing.sm, padding: spacing.md):
  │     │       Row: "To"           / IBAN value       (bodyMedium, onSurface)
  │     │       Row: "Frequency"    / "Monthly"         (bodyMedium, onSurface)
  │     │       Row: "First payment"/ date value        (bodyMedium, onSurface)
  │     │       Row: "Amount"       / "1.02 USD"        (bodyMedium, onSurface)
  │     │       Row: "Arrives in"   / "USD"             (bodyMedium, onSurface)
  │     │       Row: "Who pays fee" / "Payee"           (bodyMedium, onSurface)
  │     │       Row: "Fee"          / "Not yet known"   (bodyMedium, onSurfaceVariant)
  │     │     Row label typography: bodySmall · onSurfaceVariant
  │     │     Row value typography: bodyMedium · onSurface
  │     │     No "Reference" row — RemittanceInformation refused on this rail
  │     │
  │     ├─ banner#fx_not_fixed_notice (same as Amount step)
  │     │
  │     ├─ banner#deferred_charge_note (Fill, Auto Layout Vertical, radius.md)
  │     │     Background: secondaryContainer (#D3E5F5 light)
  │     │     Icon: info (24dp, secondary)
  │     │     Text: "A fee of 0.50 in your send currency applies when the standing
  │     │           order is set up. We cannot tell you the exact fee before you authorise."
  │     │           bodyMedium · onSecondaryContainer
  │     │
  │     ├─ banner#amend_notice (Fill, Auto Layout Vertical, radius.md)
  │     │     Background: tertiaryContainer
  │     │     Icon: info (24dp, tertiary)
  │     │     Text: "Once set up, you cannot amend or cancel this standing order
  │     │           through this app. To make changes, contact your bank directly."
  │     │           bodyMedium · onTertiaryContainer
  │     │
  │     └─ button#confirm_button (Fill × 56, radius.full)
  │           Background: primary (#266489)
  │           Label: "Set up standing order" (labelLarge, onPrimary)
  │           Min touch target: 48dp
  │
  └─ BottomNav
```

### Submitting State

```
Frame: pay_iso_submitting (Fill × 852, Auto Layout Vertical)
  ├─ TopAppBar (same as content)
  ├─ ScrollContent (centering, gap: spacing.lg)
  │     ├─ stepper (current step, partially greyed)
  │     └─ progress#submitting_indicator (Hug, Auto Layout Vertical, center, gap: spacing.md)
  │           CircularProgressIndicator: primary, indeterminate
  │           Stage label (bodyMedium, onSurface, center):
  │             StagingConsent:        "Setting up your instruction…"
  │             AwaitingAuthorisation: "Waiting for your bank to authorise…"
  │             SubmittingPayment:     "Creating your standing order…"
  │
  └─ BottomNav
```

### Error State

```
Frame: pay_iso_error (Fill × 852, Auto Layout Vertical)
  ├─ TopAppBar (same)
  ├─ ScrollContent (padding: spacing.md, gap: spacing.lg)
  │     ├─ stepper
  │     └─ error_panel (Fill, Auto Layout Vertical, radius.md)
  │           Background: errorContainer (#FFDAD6 light)
  │           One row per Errors[] entry, in wire order:
  │             Row: errorCode (labelMedium, error) + message (bodyMedium, onErrorContainer)
  │           Note: can be TWO rows simultaneously (SO-I04 batching)
  │           Retry button shown when NetworkError type only
  │
  └─ BottomNav
```

---

## 4. Component Variants

### text_field (amount_field)

| Property | Values |
|---|---|
| State | Default, Focused, Error, Disabled |
| Font | Roboto Mono (mono family) |
| Scale | headlineSmall |

| State | Border color | Border width | Background |
|---|---|---|---|
| Default | outline | 1dp | surface |
| Focused | primary | 2dp | surface |
| Error | error | 2dp | surface |
| Disabled | onSurface @ 38% opacity | 1dp | surface @ 38% opacity |

### button#confirm_button (filled_pill)

| State | Background | Label color | Opacity |
|---|---|---|---|
| Default | primary | onPrimary | 100% |
| Pressed | primary + ripple | onPrimary | 100% |
| Focused | primary | onPrimary | 100% + outline 2dp |
| Disabled | onSurface @ 12% | onSurface @ 38% | — |
| Locked (submitting) | primary | onPrimary | 100% + CircularProgress overlay |

Width: Fill · Height: 56dp · Radius: radius.full · Min touch target: 56dp

### banner (warning severity — fx_not_fixed_notice, amend_notice)

| Slot | Token |
|---|---|
| Container | tertiaryContainer |
| Text | onTertiaryContainer |
| Icon | tertiary, `schedule` / `info` (24dp) |
| Radius | radius.md |
| Padding | spacing.md all sides |
| Gap (icon to text) | spacing.sm |

### banner (info severity — deferred_charge_note)

| Slot | Token |
|---|---|
| Container | secondaryContainer |
| Text | onSecondaryContainer |
| Icon | secondary, `info` (24dp) |

### summary_card (review_card)

| Property | Value |
|---|---|
| Background | surfaceContainer |
| Radius | radius.md (12dp) |
| Elevation | level1 |
| Row label | bodySmall · onSurfaceVariant |
| Row value | bodyMedium · onSurface |
| Row gap | spacing.sm (8dp) |
| Inner padding | spacing.md (16dp) all sides |

---

## 5. Assets Required

### Icons (Material Symbols)

| Icon | Size (dp) | Component | Variant |
|---|---|---|---|
| `arrow_back` | 24 | TopAppBar back | Outlined |
| `schedule` | 24 | fx_not_fixed_notice, amend_notice (warning) | Outlined |
| `info` | 24 | deferred_charge_note, amend_notice (info) | Outlined |
| `event_repeat` | 24 | payment-status instruction_established chip | Outlined |
| `error` | 24 | error_panel | Filled |
| `check_circle` | 24 | payment-status terminal_success chip | Filled |

---

## 6. Mood Palette Usage

| Mood gradient | Role | Component | Note |
|---|---|---|---|
| `mood_gradients.hero.light` `["#C9E6FF", "#F7F9FF"]` | primaryContainer → surface | Not used on this screen | Not applicable to payment form; reserved for account-type hero headers |
| `mood_gradients.accent.light` `["#266489", "#50606E"]` | primary → secondary | Not used | Not applicable to transactional form |

Neither hero nor accent gradients are used on this screen. The payment form uses the direct role tokens (primary, surface, surfaceContainer). Gradients are suppressed on regulated-action screens to avoid aesthetics distracting from committed values.

---

## 7. WCAG Contrast Audit

All pairs measured against WCAG AA (4.5:1 normal text, 3:1 large/UI).

| Text token | Background token | Light ratio | Dark ratio | Required | Pass? |
|---|---|---|---|---|---|
| onPrimary (#FFFFFF) | primary (#266489) | 4.62:1 | — | 4.5:1 | Pass |
| onPrimaryContainer (#004B6F) | primaryContainer (#C9E6FF) | 7.27:1 | 7.27:1 | 4.5:1 | Pass (W-02/W-05) |
| onTertiaryContainer (#4C4162) | tertiaryContainer (#EADDFF) | 7.27:1 | 7.27:1 | 4.5:1 | Pass (W-16/W-17) |
| onSecondaryContainer (#384956) | secondaryContainer (#D3E5F5) | 7.22:1 | 7.22:1 | 4.5:1 | Pass |
| onErrorContainer (#93000A) | errorContainer (#FFDAD6) | 7.24:1 | 7.24:1 | 4.5:1 | Pass (W-03/W-06) |
| onSurface (#181C20) | surface (#F7F9FF) | 16.2:1 | 16.2:1 | 4.5:1 | Pass |
| onSurfaceVariant (#41474D) | surface (#F7F9FF) | 7.28:1 | 5.52:1 | 4.5:1 | Pass (W-30) |
| outline (#72787E) | surface (#F7F9FF) | 4.24:1 | — | 3.0:1 (UI) | Pass |
| error (#BA1A1A) | surface (#F7F9FF) | 6.14:1 | — | 4.5:1 | Pass |
| outlineVariant (#C1C7CE) | surface (#F7F9FF) | 1.62:1 | — | n/a | Dividers ONLY — never on text or controls |

Known failure: `outlineVariant` on surface measures 1.62:1 (light) — FAILS WCAG 1.4.11. Permitted only for visual dividers; must never bound a control or carry text.

---

## 8. Animation Specs

| Interaction | Duration | Easing | iOS | Android |
|---|---|---|---|---|
| Step transition (content change) | 300ms (medium) | Emphasis — cubic-bezier(0.2, 0.0, 0, 1.0) | CABasicAnimation (timingFunction: kCAMediaTimingFunctionEaseInEaseOut) | FastOutSlowInInterpolator |
| confirm_button lock on tap | 150ms (short) | Standard | CABasicAnimation (timingFunction: kCAMediaTimingFunctionDefault) | AccelerateDecelerateInterpolator |
| Banner appear (fx_not_fixed_notice) | 300ms | Emphasis | CABasicAnimation | FastOutSlowInInterpolator |

All animations respect `reduce_motion_supported: true`. When system reduce-motion is on, substitute cross-fade (150ms) for slide/expand animations.
