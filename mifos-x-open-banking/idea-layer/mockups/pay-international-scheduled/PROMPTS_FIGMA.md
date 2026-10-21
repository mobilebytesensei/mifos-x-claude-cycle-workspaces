# Pay International Scheduled — Figma Design Prompt

> Generated from `screens/pay-international-scheduled/{ui,docs}.yaml`
> Design system: Open Banking — Trust Blue · Material Design 3
> Rail: international-scheduled-payment · Six steps · FAPI 1.0 Advanced

---

## 1. Frame Setup

- **Frame**: Android (412 × 892dp) / iPhone 14 Pro (393 × 852dp)
- **Grid**: 4-column, 16dp gutter, 16dp margin
- **Status bar**: 24dp height
- **Top app bar**: 56dp height
- **Bottom nav**: 80dp height
- **Safe area bottom**: 34dp (home indicator on iOS)
- **Total scrollable viewport**: 892 − 24 − 56 − 80 − 34 = 698dp (Android)

---

## 2. Design Token Variables

### Colors (Light Mode)

| Variable Name | Value | Usage |
|--------------|-------|-------|
| `color/primary` | #266489 | Filled buttons, step indicator active, selected account highlight |
| `color/onPrimary` | #FFFFFF | Button label text |
| `color/primaryContainer` | #C9E6FF | Selected date chip in calendar, step active background |
| `color/onPrimaryContainer` | #004B6F | Text on selected date chip |
| `color/secondary` | #50606E | Step indicator inactive labels |
| `color/secondaryContainer` | #D3E5F5 | Info banners (fx_disclosure, deferred_charge_note, no_funds_check_note, amend_notice) |
| `color/onSecondaryContainer` | #384956 | Text and icon on info banners |
| `color/surface` | #F7F9FF | Screen background |
| `color/onSurface` | #181C20 | Primary text, amount input text |
| `color/surfaceContainerLow` | #F1F4F9 | Account list item background |
| `color/surfaceContainerHigh` | #E5E8ED | Bottom nav bar background |
| `color/surfaceContainerHighest` | #E0E3E8 | Shimmer block fill (loading state) |
| `color/onSurfaceVariant` | #41474D | Helper text, field labels, secondary step labels, fee "unknown" text |
| `color/outline` | #72787E | TextField default border |
| `color/outlineVariant` | #C1C7CE | Dividers (decorative only — never on controls) |
| `color/error` | #BA1A1A | Field error text, error_panel icon |
| `color/errorContainer` | #FFDAD6 | error_panel background |
| `color/onErrorContainer` | #93000A | Text and icon on error_panel |
| `color/surfaceVariant` | #DDE3EA | instruction_established chip container |
| `color/scrim` | #000000 | Modal overlays |

### Colors (Dark Mode)

| Variable Name | Value |
|--------------|-------|
| `color/primary` | #95CDF7 |
| `color/onPrimary` | #00344E |
| `color/primaryContainer` | #004B6F |
| `color/onPrimaryContainer` | #C9E6FF |
| `color/secondaryContainer` | #384956 |
| `color/onSecondaryContainer` | #D3E5F5 |
| `color/surface` | #101417 |
| `color/onSurface` | #E0E3E8 |
| `color/onSurfaceVariant` | #C1C7CE |
| `color/outline` | #8B9198 |
| `color/error` | #FFB4AB |
| `color/errorContainer` | #93000A |
| `color/onErrorContainer` | #FFDAD6 |
| `color/surfaceVariant` | #41474D |

### Typography

| Style | Font | Size | Weight | Line Height |
|-------|------|:----:|:------:|:-----------:|
| titleLarge | Roboto | 22sp | 400 | 28sp |
| titleSmall | Roboto | 14sp | 500 | 20sp |
| headlineSmall | Roboto Mono | 24sp | 400 | 32sp |
| bodyLarge | Roboto | 16sp | 400 | 24sp |
| bodyMedium | Roboto | 14sp | 400 | 20sp |
| bodySmall | Roboto | 12sp | 400 | 16sp |
| labelLarge | Roboto | 14sp | 500 | 20sp |
| labelSmall | Roboto | 11sp | 500 | 16sp |

Note: `headlineSmall` uses **Roboto Mono** for all amount fields so digits align and do not reflow during typing.

### Spacing

| Token | Value |
|-------|:-----:|
| `spacing/xxs` | 2dp |
| `spacing/xs` | 4dp |
| `spacing/sm` | 8dp |
| `spacing/md` | 16dp |
| `spacing/lg` | 24dp |
| `spacing/xl` | 32dp |
| `spacing/xxl` | 48dp |

### Corner Radius

| Token | Value | Used By |
|-------|:-----:|---------|
| `radius/sm` | 8dp | TextField, DatePicker, amount_field |
| `radius/md` | 12dp | review_card, account list item cards |
| `radius/full` | 9999dp | Filled buttons (filled_pill shape) |

---

## 3. Auto Layout Structure

### Step Indicator (Persistent)

```
StepIndicator (Fill × Hug, Auto Layout Horizontal, padding 16/16, gap 4dp)
  REPEAT × 6:
    StepDot (24 × 24dp)
      Fill: color/primary (active) or color/outlineVariant (inactive)
      Corner: radius/full
    StepLabel (Hug × Hug) — labelSmall, onSurfaceVariant
      Text: "Account" / "Recipient" / "Amount" / "Date" / "Charges" / "Review"
    Connector (Fill × 2dp, outlineVariant) — between items
```

### Content State — Step 1: Account Selection

```
Frame: PayInternationalScheduled_content_step1 (Fill, Auto Layout Vertical)
  TopAppBar (Fill × 56dp, Auto Layout Horizontal, padding 4/16)
    BackIcon (48 × 48dp, icon/md 24dp, onSurface)
    Title: "Pay abroad on a date" (titleLarge, onSurface, Fill)

  ScrollContent (Fill, Auto Layout Vertical, padding 16dp, gap 16dp)
    StepIndicator (see above, step 1 active)

    [optional] IneligibleAccountsBanner (Fill × Hug, radius/md)
      Fill: secondaryContainer
      Auto Layout Horizontal, padding 12dp, gap 8dp
        Icon: info_outline (icon/md, onSecondaryContainer)
        Text: "1 account is not available for international payments and is not shown."
              (bodySmall, onSecondaryContainer)

    SectionHeader: "Choose funding account" (titleSmall, onSurface, Fill)

    AccountCard × N (Fill × 64dp, Auto Layout Horizontal, padding 16dp, gap 12dp)
      Fill: surfaceContainerLow · Corner: radius/md · Elevation: level1
      Leading: BankIcon (icon/md, primary)
      LabelColumn (Fill, Auto Layout Vertical, gap 2dp)
        Primary: "Barclays Current Account" (bodyLarge, onSurface)
        Secondary: "•••• 4231" (bodyMedium, onSurfaceVariant)
      Trailing: "£2,450.00" (bodyLarge, Roboto Mono, onSurface)

    FilledButton "Next" (Fill × 56dp)
      Fill: primary · Corner: radius/full · Label: "Next" (labelLarge, onPrimary)

  BottomNav (Fill × 80dp, surfaceContainerHigh)
    Tabs: Home · Accounts · Pay (active/primary) · More
```

### Content State — Step 6: Review

```
Frame: PayInternationalScheduled_content_step6 (Fill, Auto Layout Vertical)
  TopAppBar (same as step 1)
  ScrollContent (Fill, Auto Layout Vertical, padding 16dp, gap 16dp)
    StepIndicator (step 6 active)

    ReviewCard (Fill × Hug, Auto Layout Vertical, padding 16dp, gap 8dp)
      Fill: surfaceContainerLow · Corner: radius/md · Elevation: level1
      ReviewRow × 7 (Fill × 44dp, Auto Layout Horizontal)
        Label col (120dp, bodyMedium, onSurfaceVariant): "From" / "To" / "Payee" / "You send" / "They receive in" / "Date" / "Charge bearer"
        Value col (Fill, bodyMedium, onSurface, Roboto Mono for amounts)
      Divider (Fill × 1dp, outlineVariant — DECORATIVE ONLY, never on a control)
      FeeRow (Fill × 44dp)
        Label: "Fee" (bodyMedium, onSurfaceVariant)
        Value: "Not yet known" (bodyMedium, onSurfaceVariant, italic)

    InfoBanner — deferred_charge_note (Fill × Hug, secondaryContainer, radius/md)
      Icon: info_outline (icon/md, onSecondaryContainer)
      "A fee applies and will be confirmed once the payment is set up. It is charged in
       the currency you send in."

    InfoBanner — no_funds_check_note (Fill × Hug, secondaryContainer, radius/md)
      "We cannot check your available balance for future-dated payments."

    InfoBanner — amend_notice (Fill × Hug, secondaryContainer, radius/md)
      "Once set up, this payment cannot be changed or cancelled through this app.
       To amend or cancel, contact your bank directly."

    FilledButton "Schedule payment" (Fill × 56dp)
      Fill: primary · Corner: radius/full · "Schedule payment" (labelLarge, onPrimary)
      Note: CTA label is "Schedule payment" — NOT "Send £X.XX" (this is a deferred rail)
      Locks with LinearProgressIndicator on tap (prevents double-submission)
```

### Loading State

```
Frame: PayInternationalScheduled_loading (Fill, Auto Layout Vertical)
  TopAppBar (same)
  ScrollContent (Fill, Auto Layout Vertical, padding 16dp, gap 16dp)
    ShimmerRect (Fill × 40dp, surfaceContainerHighest, radius/sm) — step indicator
    ShimmerRect (Fill × 64dp, surfaceContainerHighest, radius/md) — account card
    ShimmerRect (240 × 16dp, surfaceContainerHighest, radius/sm) — label
    ShimmerRect (Fill × 64dp, surfaceContainerHighest, radius/md) — account card
    ShimmerRect (240 × 16dp, surfaceContainerHighest, radius/sm)
    ShimmerRect (Fill × 56dp, surfaceContainerHighest, radius/full) — next button
  Shimmer animation: 1.5s loop, left-to-right gradient sweep
  BottomNav (same)
```

### Submitting State

```
Frame: PayInternationalScheduled_submitting (Fill, Auto Layout Vertical)
  TopAppBar (same)
  CenteredContent (Fill, Auto Layout Vertical, center-aligned, gap 24dp)
    CircularProgressIndicator (48dp, primary)
    StageLabel (bodyLarge, onSurface, center)
      "Setting up your payment…"         — StagingConsent
      "Waiting for your bank to authorise…" — AwaitingAuthorisation
      "Submitting payment…"              — SubmittingPayment
  BottomNav (same)
```

### Error State

```
Frame: PayInternationalScheduled_error (Fill, Auto Layout Vertical)
  TopAppBar (same)
  ScrollContent (Fill, Auto Layout Vertical, padding 16dp, gap 16dp)
    StepIndicator
    ErrorCard (Fill × Hug, errorContainer, radius/md, Auto Layout Vertical, padding 16dp, gap 12dp)
      HeaderRow (Auto Layout Horizontal, gap 12dp)
        Icon: error (icon/md, error)
        Title: "Payment could not be processed" (titleMedium, onErrorContainer)
      FOR EACH error entry (wire order):
        Divider (outlineVariant, decorative)
        ErrorEntryRow (Auto Layout Horizontal, gap 8dp)
          CodeBadge (labelSmall, onErrorContainer, outline 1dp)
          MessageText (bodyMedium, onErrorContainer, Fill)
    RetryButton "Try again" (outlined, primary, radius/full) — if retryable
    TextButton "Start a new payment" (primary) — always
  BottomNav (same)
```

### No Eligible Accounts State

```
Frame: PayInternationalScheduled_no_accounts (Fill, Auto Layout Vertical)
  TopAppBar (same)
  EmptyContent (Fill, Auto Layout Vertical, center, gap 24dp)
    StepIndicator (all steps inactive)
    Icon: account_balance_wallet (icon/xl 48dp, onSurfaceVariant)
    Title: "No accounts available" (headlineSmall, onSurface, center)
    Body: "None of your accounts can be used for international payments at this time."
          (bodyMedium, onSurfaceVariant, center, padding H 32dp)
  BottomNav (same)
```

---

## 4. Component Variants

### amount_field

| Property | Values |
|----------|--------|
| State | Default, Focused, Error, Disabled |

**Specifications**:
- Width: Fill
- Height: 56dp minimum
- Padding: 16dp horizontal, 12dp vertical
- Corner Radius: `radius/sm` (8dp)
- Background: surface
- Border default: `outline` (#72787E, 1dp)
- Border focused: `color/primary` (#266489, 2dp)
- Border error: `color/error` (#BA1A1A, 2dp)
- Font: `headlineSmall` (24sp) **Roboto Mono** — digits must not reflow while typing
- Prefix "£": onSurfaceVariant, not part of the editable value
- Label above: bodySmall, onSurfaceVariant

### execution_date_picker

| Property | Values |
|----------|--------|
| Range | T+1 minimum, T+365 maximum |
| Weekend | Allowed |
| Disabled | Today, past, T+366+ |

**Specifications**:
- Type: Material 3 modal calendar (DatePicker dialog)
- Selected day: `primaryContainer` fill, `onPrimaryContainer` text
- Disabled days: `onSurface` at `opacity/disabled` (38%)
- Today indicator: outline 2dp `primary` (unselected)

### confirm_button / FilledButton

| State | Background | Label | Opacity |
|-------|-----------|-------|:-------:|
| Default | primary | onPrimary | 100% |
| Pressed | primary + ripple | onPrimary | 100% |
| Disabled | onSurface | onSurface | 38% |
| Loading (post-tap) | primary + LinearProgressIndicator | onPrimary | 100% |

Width: Fill · Height: 56dp · Corner: `radius/full` · Label: `labelLarge` (14sp, 500)

**CTA label**: "Schedule payment" — NOT "Send £X.XX". This is a deferred rail; money moves on the execution date, not now.

---

## 5. Assets Required

### Icons (Material Symbols)

| Icon | Size | Usage | Style |
|------|:----:|-------|:-----:|
| arrow_back | icon/md (24dp) | TopAppBar back navigation | Outlined |
| info_outline | icon/md | Banner leading icon | Outlined |
| error | icon/md | error_panel, field error | Filled |
| account_balance_wallet | icon/xl (48dp) | no_eligible_accounts empty state | Outlined |
| event_repeat | icon/md | instruction_established chip | Outlined |
| check_circle | icon/md | success disposition (payment-status) | Filled |
| schedule | icon/md | in_progress disposition | Outlined |
| bank (or custom) | icon/md | Account list leading icon | Outlined |

---

## 6. Mood Palette Usage

| Mood Color | Hex (light) | Component(s) | Notes |
|-----------|-------------|--------------|-------|
| hero gradient start | #C9E6FF | (unused on this feature) | This feature has no hero section |
| hero gradient end | #F7F9FF | Screen surface background | Implicit surface |
| accent gradient | — | (unused) | Payment forms use flat surfaces, not accent gradients |

The mood palette is intentionally minimal on payment forms. Trust comes from legibility and calm layout, not from decorative gradient application.

---

## 7. WCAG Contrast Audit

| Text Token | Bg Token | Ratio | Required | Pass? |
|-----------|----------|:-----:|:--------:|:-----:|
| onPrimary (#FFFFFF) | primary (#266489) | 6.11:1 | 4.5:1 | Yes |
| onSurface (#181C20) | surface (#F7F9FF) | 16.34:1 | 4.5:1 | Yes |
| onSurfaceVariant (#41474D) | surface (#F7F9FF) | 7.28:1 | 4.5:1 | Yes |
| onSurfaceVariant (#41474D) | surfaceContainerLow (#F1F4F9) | 7.27:1 | 4.5:1 | Yes |
| onSecondaryContainer (#384956) | secondaryContainer (#D3E5F5) | 7.22:1 | 4.5:1 | Yes |
| onErrorContainer (#93000A) | errorContainer (#FFDAD6) | 7.24:1 | 4.5:1 | Yes |
| error (#BA1A1A) | surface (#F7F9FF) | 6.14:1 | 4.5:1 | Yes |
| outline (#72787E) | surface (#F7F9FF) | 4.24:1 | 3.0:1 (non-text UI) | Yes |
| outlineVariant (#C1C7CE) | surface (#F7F9FF) | 1.62:1 | — | Decorative only — NEVER on controls or text |

**Known failure**: `outlineVariant` on `surface` = 1.62:1. Permitted for dividers only; must never bound a control or carry a glyph.

---

## 8. Responsive Variants

| Breakpoint | Layout |
|:----------:|--------|
| Compact (< 600dp) | Single column, full-width cards, screen padding 16dp |
| Medium (600–840dp) | Single column centred, max-width 480dp, increased side margins |
| Expanded (> 840dp) | Form centred at max-width 480dp; no multi-column split (payment forms are single-column by design) |

The form must never become a multi-column layout — amount entry and date selection require focused attention, not horizontal scanning.
