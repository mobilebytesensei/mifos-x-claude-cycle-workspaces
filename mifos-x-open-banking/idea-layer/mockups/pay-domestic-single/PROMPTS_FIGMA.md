# pay-domestic-single — Figma Design Prompt

> Generated from `screens/pay-domestic-single/ui.yaml` + `idea-layer/design-system/design-tokens.yaml`
> Design system: Open Banking — Trust Blue (Material 3, seed primary #266489)
> Contract version: 2.1.0
> Schema version: 4.0
> States covered: loading · content · content_no_eligible_accounts · submitting · error

---

## 1. Frame Setup

- **Frame name prefix**: `pay_domestic_single/`
- **Mobile frame**: 390 × 844dp (iPhone 14 / Android 390w baseline)
- **Grid**: 4-column, 16dp gutter, 16dp margin
- **Status bar**: 44dp (iOS) / 24dp (Android) — system layer, do not add interactive elements
- **Top app bar**: 64dp (title + back icon, no action icons on this screen)
- **Step indicator**: 48dp fixed height, full width
- **Bottom nav**: 80dp height, always visible
- **Safe area bottom**: 34dp (home indicator) inside the 80dp nav
- **Content scroll area**: frame height − status bar − top app bar − bottom nav = scrollable

---

## 2. Design Token Variables

Create these as Figma Local Variables. All hex values are light-mode. The design system
ships a verbatim Material 3 role set; reference these role names, not hex literals, in
Figma's variable bindings.

### Colors (Light Mode)

| Variable Name | Hex (light) | Role | Usage |
|---|---|---|---|
| `color/primary` | #266489 | primary | confirm_button bg, stepper active step, active bottom nav tab, link taps |
| `color/onPrimary` | #FFFFFF | onPrimary | Text on confirm_button |
| `color/primaryContainer` | #C9E6FF | primaryContainer | Terminal-success disposition chip |
| `color/onPrimaryContainer` | #004B6F | onPrimaryContainer | Text on primaryContainer |
| `color/secondary` | #50606E | secondary | Supporting controls |
| `color/secondaryContainer` | #D3E5F5 | secondaryContainer | in_progress disposition chip bg |
| `color/onSecondaryContainer` | #384956 | onSecondaryContainer | in_progress chip text |
| `color/tertiary` | #64597B | tertiary | Warning / attention needed |
| `color/tertiaryContainer` | #EADDFF | tertiaryContainer | Warning banner bg |
| `color/onTertiaryContainer` | #4C4162 | onTertiaryContainer | Warning banner text |
| `color/error` | #BA1A1A | error | amount_error text, field error outline, error panel icon |
| `color/errorContainer` | #FFDAD6 | errorContainer | error_panel background |
| `color/onErrorContainer` | #93000A | onErrorContainer | error_panel text and icon |
| `color/surface` | #F7F9FF | surface | Screen background, list item bg |
| `color/onSurface` | #181C20 | onSurface | Primary text (account names, amounts) |
| `color/surfaceContainer` | #EBEEF3 | surfaceContainer | review_card bg, bottom nav bg |
| `color/surfaceContainerLow` | #F1F4F9 | surfaceContainerLow | Shimmer skeleton fill |
| `color/onSurfaceVariant` | #41474D | onSurfaceVariant | Labels, helper text, supporting text, step indicator inactive |
| `color/outline` | #72787E | outline | text_field default border |

### Colors (Dark Mode)

| Variable Name | Hex (dark) |
|---|---|
| `color/primary` (dark) | #95CDF7 |
| `color/onPrimary` (dark) | #00344E |
| `color/primaryContainer` (dark) | #004B6F |
| `color/surface` (dark) | #101417 |
| `color/onSurface` (dark) | #E0E3E8 |
| `color/onSurfaceVariant` (dark) | #C1C7CE |
| `color/error` (dark) | #FFB4AB |
| `color/errorContainer` (dark) | #93000A |
| `color/onErrorContainer` (dark) | #FFDAD6 |
| `color/surfaceContainer` (dark) | #1C2024 |
| `color/surfaceContainerLow` (dark) | #181C20 |
| `color/outline` (dark) | #8B9198 |
| `color/secondaryContainer` (dark) | #384956 |

### Typography

| Style Name | Font | Size | Weight | Line Height |
|---|---|---|---|---|
| `type/headlineSmall` | Roboto | 24sp | 400 | 32sp |
| `type/titleLarge` | Roboto | 22sp | 400 | 28sp |
| `type/titleMedium` | Roboto | 16sp | 500 | 24sp |
| `type/bodyLarge` | Roboto | 16sp | 400 | 24sp |
| `type/bodyMedium` | Roboto | 14sp | 400 | 20sp |
| `type/bodySmall` | Roboto | 12sp | 400 | 16sp |
| `type/labelLarge` | Roboto | 14sp | 500 | 20sp |
| `type/labelMedium` | Roboto | 12sp | 500 | 16sp |
| `type/labelSmall` | Roboto | 11sp | 500 | 16sp |
| `type/amount/headlineSmall` | Roboto Mono | 24sp | 400 | 32sp |
| `type/amount/bodyLarge` | Roboto Mono | 16sp | 400 | 24sp |

### Spacing

| Token | Value (dp) |
|---|---|
| `spacing/xs` | 4 |
| `spacing/sm` | 8 |
| `spacing/md` | 16 |
| `spacing/lg` | 24 |
| `spacing/xl` | 32 |

### Corner Radius

| Token | Value (dp) |
|---|---|
| `radius/sm` | 8 |
| `radius/md` | 12 |
| `radius/lg` | 16 |
| `radius/xl` | 28 |
| `radius/full` | 9999 |

---

## 3. Auto Layout Structure

### Frame: `pay_domestic_single/loading`

```
Frame: pay_domestic_single/loading  (390 × 844, Fill)
├─ TopAppBar [Fill × 64dp, Auto Layout H, padding H:4dp/V:0, gap 0]
│   ├─ NavigationIconBtn [48 × 48dp] (icon: arrow_back, 24dp, color/onSurface)
│   └─ Title: "Pay someone" [Fill, titleLarge, color/onSurface]
│
├─ StepIndicatorSkeleton [Fill × 48dp, Auto Layout H, padding H:16dp, gap 8dp]
│   ├─ Shimmer_step1 [72dp × 16dp, Rect, color/surfaceContainerLow, radius/sm]
│   ├─ Divider [1dp × 16dp, color/outline]
│   ├─ Shimmer_step2 [72dp × 16dp, Rect, color/surfaceContainerLow, radius/sm]
│   ├─ Divider
│   ├─ Shimmer_step3 [72dp × 16dp, Rect, color/surfaceContainerLow, radius/sm]
│   ├─ Divider
│   └─ Shimmer_step4 [72dp × 16dp, Rect, color/surfaceContainerLow, radius/sm]
│
├─ SkeletonContent [Fill × Fill, Auto Layout V, padding 16dp, gap 12dp]
│   ├─ Shimmer_row1 [Fill × 56dp, Rect, color/surfaceContainerLow, radius/sm]
│   ├─ Shimmer_row2 [Fill × 56dp, Rect, color/surfaceContainerLow, radius/sm]
│   └─ Shimmer_row3 [Fill × 56dp, Rect, color/surfaceContainerLow, radius/sm]
│
└─ BottomNav [Fill × 80dp, Auto Layout H, color/surfaceContainer]
    ├─ Tab: Home    (home icon, color/onSurfaceVariant, labelSmall "Home")
    ├─ Tab: Accounts (account_balance, color/onSurfaceVariant)
    ├─ Tab: Pay     (payments icon, color/primary — ACTIVE, labelSmall bold "Pay")
    └─ Tab: More    (more_horiz, color/onSurfaceVariant)
```

### Frame: `pay_domestic_single/content_step1_account`

```
Frame: pay_domestic_single/content_step1_account  (390 × 844)
├─ TopAppBar [Fill × 64dp]  (same as loading)
├─ StepIndicator [Fill × 48dp, H, padding H:16dp, gap 8dp]
│   ├─ StepLabel "Account" [labelMedium, color/primary, weight 500]
│   ├─ Divider [1dp, color/outlineVariant]
│   ├─ StepLabel "Payee"   [labelMedium, color/onSurfaceVariant]
│   ├─ Divider
│   ├─ StepLabel "Amount"  [labelMedium, color/onSurfaceVariant]
│   ├─ Divider
│   └─ StepLabel "Review"  [labelMedium, color/onSurfaceVariant]
│
├─ ScrollContent [Fill × Fill, Auto Layout V, padding 16dp, gap 0]
│   ├─ SectionLabel "Pay from" [Fill, bodyMedium, color/onSurfaceVariant, padding B:8dp]
│   │
│   ├─ AccountListItem [Fill × 56dp, H, padding H:16dp V:8dp, gap 16dp]
│   │   ├─ LeadingIcon: account_balance [24dp, color/primary]
│   │   ├─ Content [Fill, V, gap 4dp]
│   │   │   ├─ PrimaryText: "Current account" [bodyLarge, color/onSurface]
│   │   │   └─ SupportText: "80200110203349" [bodyMedium, color/onSurfaceVariant, Roboto Mono]
│   │   └─ Trailing [H, gap 8dp]
│   │       ├─ Amount: "£1,250.00" [bodyLarge, color/primary, Roboto Mono]
│   │       └─ Icon: chevron_right [24dp, color/onSurfaceVariant]
│   │
│   ├─ Divider [Fill × 1dp, color/outlineVariant]
│   │
│   ├─ AccountListItem [Fill × 56dp] (same structure)
│   │   · "Current account 2" · "80200110203348" · "£480.00"
│   │
│   ├─ Divider
│   │
│   ├─ AccountListItem [Fill × 56dp]
│   │   · "BMM ACCOUNT" · "80122590953695" · "£8,000.00"
│   │
│   └─ IneligibleNote [Fill × Hug, padding T:12dp H:16dp]
│       └─ Text: "2 accounts can't be used for this payment type. Only UK sort-code accounts are
│                  supported." [bodySmall, color/onSurfaceVariant]
│
└─ BottomNav [same as loading]
```

### Frame: `pay_domestic_single/content_step2_payee`

```
Frame: pay_domestic_single/content_step2_payee  (390 × 844)
├─ TopAppBar  (same)
├─ StepIndicator — step 2 "Payee" active (color/primary); others onSurfaceVariant
│
├─ ScrollContent [Fill, V, padding 16dp, gap 12dp]
│   ├─ SectionLabel "Pay to" [bodyMedium, color/onSurfaceVariant]
│   │
│   ├─ BeneficiaryListItem [Fill × 56dp, H, padding H:16dp V:8dp, gap 16dp]
│   │   ├─ LeadingIcon: person [24dp, color/primary]
│   │   ├─ Content [Fill, V, gap 4dp]
│   │   │   ├─ "Mr Mark" [bodyLarge, color/onSurface]
│   │   │   └─ "80200110203349" [bodyMedium, color/onSurfaceVariant, Roboto Mono]
│   │   └─ chevron_right [24dp, color/onSurfaceVariant]
│   │
│   ├─ Divider
│   ├─ BeneficiaryListItem (same) · "Ramu" · "40200110203351"
│   │
│   ├─ Divider
│   ├─ TextButton "Enter details manually" [Fill, H, center, padding V:12dp]
│   │   └─ Label [labelLarge, color/primary]
│   │
│   ├─ SortCodeField [Fill × 56dp, outlined text_field, radius/sm=8dp]
│   │   ├─ Label: "Sort code" [bodySmall, color/onSurfaceVariant]
│   │   ├─ Placeholder: "00-00-00" [bodyLarge, color/outline]
│   │   └─ Outline: 1dp color/outline (default), 2dp color/primary (focus)
│   │
│   ├─ AccountNumberField [Fill × 56dp] (same spec, label "Account number")
│   │
│   └─ PayeeNameField [Fill × 56dp] (same spec, label "Payee name")
│       (no placeholder — required field, no hint that it is optional)
│
└─ BottomNav
```

### Frame: `pay_domestic_single/content_step3_amount`

```
Frame: pay_domestic_single/content_step3_amount  (390 × 844)
├─ TopAppBar  (same)
├─ StepIndicator — step 3 "Amount" active
│
├─ ScrollContent [Fill, V, padding 16dp, gap 12dp]
│   ├─ AmountField [Fill × 72dp, H, radius/sm=8dp, padding H:16dp]
│   │   ├─ Prefix "£" [headlineSmall, color/onSurfaceVariant, non-editable]
│   │   └─ AmountInput [Fill, headlineSmall, Roboto Mono, color/onSurface]
│   │       (outline: 1dp color/outline default; 2dp color/primary focus; 2dp color/error on error)
│   │
│   ├─ [ErrorText "Amount must be greater than zero" bodySmall color/error — shown when amountProblem != null]
│   │
│   ├─ ReferenceField [Fill × 56dp, outlined text_field, radius/sm]
│   │   ├─ Label "Reference" [bodySmall, color/onSurfaceVariant]
│   │   ├─ HelperText "Up to 35 characters. Visible to the payee." [bodySmall, color/onSurfaceVariant]
│   │   └─ Outline default color/outline
│   │       (Input shows "Rent August" in demo)
│   │
│   └─ ContinueButton [Fill − 32dp × 56dp, filled, radius/full, color/primary bg]
│       └─ Label "Continue" [labelLarge, color/onPrimary]
│
└─ BottomNav
```

### Frame: `pay_domestic_single/content_step4_review`

```
Frame: pay_domestic_single/content_step4_review  (390 × 844)
├─ TopAppBar
├─ StepIndicator — step 4 "Review" active
│
├─ ScrollContent [Fill, V, padding 16dp, gap 16dp]
│   ├─ ReviewCard [Fill, V, padding 16dp, gap 12dp, radius/md=12dp,
│   │              fill=color/surfaceContainer, elevation=1]
│   │   ├─ ReviewRow [Fill, H, gap spacing/xs=4dp]
│   │   │   ├─ RowLabel "Pay from" [bodyMedium, color/onSurfaceVariant, Fill]
│   │   │   └─ RowValue "Current account · 802001 10203349" [bodyLarge, color/onSurface]
│   │   ├─ Divider [Fill × 1dp, color/outlineVariant]
│   │   ├─ ReviewRow "Pay to" / "Mr Mark · 802001 10203348"
│   │   ├─ Divider
│   │   ├─ ReviewRow "Amount" / "£15.55" (Roboto Mono, color/onSurface)
│   │   ├─ Divider
│   │   ├─ ReviewRow "Reference" / "Rent August"
│   │   ├─ Divider
│   │   └─ ReviewRow "Fee" / "£0.05" (Roboto Mono, color/onSurfaceVariant)
│   │
│   └─ ConfirmButton [Fill − 32dp × 56dp, filled pill, radius/full, color/primary]
│       Label "Send £15.55" [labelLarge, color/onPrimary]
│       NOTE: amount in label is REQUIRED on this rail (irreversible_action.cta_label_by_rail)
│
└─ BottomNav
```

### Frame: `pay_domestic_single/content_no_eligible_accounts`

```
Frame: pay_domestic_single/content_no_eligible_accounts  (390 × 844)
├─ TopAppBar
├─ StepIndicator (step 1 "Account" active)
│
├─ EmptyStateContent [Fill × Fill, V, center, gap 16dp, padding 32dp]
│   ├─ Icon: account_balance_off or no_accounts [48dp, color/onSurfaceVariant]
│   ├─ Title: "No eligible accounts" [headlineSmall, color/onSurface, center]
│   └─ Body: "This payment type requires a UK sort-code account. Your other accounts can't be
│             used here." [bodyMedium, color/onSurfaceVariant, center]
│   (No CTA — this is a terminal informational state, not an error)
│
└─ BottomNav
```

### Frame: `pay_domestic_single/submitting`

```
Frame: pay_domestic_single/submitting  (390 × 844)
├─ TopAppBar (back icon present but navigation disabled during submission)
├─ StepIndicator — all steps at opacity.disabled = 0.38 (not interactive)
│
├─ SubmittingContent [Fill × Fill, V, center, gap 16dp, padding 32dp]
│   ├─ CircularProgressIndicator [48dp, color/primary, indeterminate]
│   └─ StatusLabel [bodyLarge, color/onSurface, center]
│       · "Creating payment…"         (StagingConsent)
│       · "Waiting for your bank…"    (AwaitingAuthorisation)
│       · "Checking available funds…" (ConfirmingFunds)
│       · "Sending payment…"          (SubmittingPayment)
│   (confirm_button is ABSENT — unmounted, not disabled)
│
└─ BottomNav (visible, tabs non-interactive during submission)
```

### Frame: `pay_domestic_single/error`

```
Frame: pay_domestic_single/error  (390 × 844)
├─ TopAppBar
├─ StepIndicator (step matching last attempted step, dimmed)
│
├─ ScrollContent [Fill, V, padding 16dp, gap 16dp]
│   └─ ErrorPanel [Fill, V, padding 16dp, gap 12dp,
│                  fill=color/errorContainer, radius/md=12dp]
│       ├─ Icon: error_outline [32dp, color/onErrorContainer]
│       ├─ Title "Something went wrong" [titleMedium, color/onErrorContainer]
│       ├─ [FOR EACH entry in Errors[] — iterate ALL, not just [0]]
│       │   └─ ErrorMessage "<copy from ErrorCode+Path>" [bodyMedium, color/onErrorContainer]
│       │
│       └─ ActionRow [H, gap 8dp]
│           · NetworkError / TokenExpired → FilledButton "Try again" (color/primary)
│           · ConsentNotAuthorised        → FilledButton "Re-authorise" (color/primary)
│           · ConsentRevoked              → FilledButton "View Consents" (color/primary)
│           · SignatureMissing / InitiationMismatch → TextButton "Contact support" + ref code
│
└─ BottomNav
```

---

## 4. Component Variants

### text_field (Sort code / Account number / Payee name / Reference)

| Property | Values |
|---|---|
| State | Default · Focused · Error · Disabled |
| HasHelperText | true (Reference only) · false |

| State | Outline | Outline Width | Label Color | Opacity |
|---|---|---|---|---|
| Default | color/outline (#72787E) | 1dp | color/onSurfaceVariant | 100% |
| Focused | color/primary (#266489) | 2dp | color/primary | 100% |
| Error | color/error (#BA1A1A) | 2dp | color/error | 100% |
| Disabled | color/outline | 1dp | color/onSurfaceVariant | 38% |

Specs: radius/sm = 8dp, min_height = 56dp, padding H:16dp, label above input (bodySmall),
input (bodyLarge, onSurface), helper/error below (bodySmall).

### amount_field

| State | Prefix color | Input scale | Font |
|---|---|---|---|
| Default | color/onSurfaceVariant | headlineSmall | Roboto Mono |
| Focused | color/primary | headlineSmall | Roboto Mono |
| Error | color/error | headlineSmall | Roboto Mono |

### confirm_button (FilledPill)

| State | Background | Label | Shadow |
|---|---|---|---|
| Default | color/primary (#266489) | color/onPrimary (#FFFFFF) | elevation 0 |
| Pressed | color/primary + ripple (onPrimary at opacity.pressed=0.12) | same | elevation 0 |
| Submitting | ABSENT (unmounted — the state-transition-unmount pattern) | — | — |
| Disabled | N/A — the button never enters a disabled state; it unmounts instead | — | — |

### account_list_item

| State | Background | Ripple |
|---|---|---|
| Default | color/surface | none |
| Pressed | color/surface + onSurface ripple (opacity.pressed = 0.12) | radial from touch point |

Touch target: 48dp minimum. chevron_right trailing icon: 24dp, color/onSurfaceVariant.

### review_card

| Property | Value |
|---|---|
| Container | color/surfaceContainer (#EBEEF3) |
| Radius | radius/md = 12dp |
| Elevation | 1dp tonal (no shadow, M3 tonal) |
| Row label | bodyMedium, color/onSurfaceVariant |
| Row value | bodyLarge, color/onSurface (amounts in Roboto Mono) |
| Dividers between rows | 1dp, color/outlineVariant |

---

## 5. Assets Required

### Icons (Material Symbols, Outlined style)

| Icon name | Size | Usage | Filled? |
|---|---|---|---|
| `arrow_back` | icon/md = 24dp | TopAppBar navigation | Outlined |
| `account_balance` | icon/md = 24dp | Debtor account list item leading | Outlined |
| `person` | icon/md = 24dp | Beneficiary list item leading | Outlined |
| `chevron_right` | icon/md = 24dp | List item trailing disclosure | Outlined |
| `error_outline` | icon/lg = 32dp | error_panel icon | Outlined |
| `check_circle` | icon/md = 24dp | payment_disposition.terminal_success (payment-status screen) | Filled |
| `schedule` | icon/md = 24dp | payment_disposition.in_progress chip | Outlined |
| `home` | icon/md = 24dp | Bottom nav Home tab | Outlined (inactive) / Filled (active) |
| `account_balance` | icon/md = 24dp | Bottom nav Accounts tab | same |
| `payments` | icon/md = 24dp | Bottom nav Pay tab — ACTIVE on this screen | Filled |
| `more_horiz` | icon/md = 24dp | Bottom nav More tab | Outlined |

### Illustrations / Images

(none — this screen uses Material icons only)

---

## 6. Mood Palette Usage

| Mood Color | Token path | Hex (light) | Component(s) on this screen | If unused — reason |
|---|---|---|---|---|
| Hero gradient start | `mood_gradients.hero.light[0]` | #C9E6FF | Not used on pay-domestic-single | Payment initiation uses flat surface, not hero wash |
| Hero gradient end | `mood_gradients.hero.light[1]` | #F7F9FF | Screen background (surface) matches this value | Coincidental, not intentional gradient |
| Accent gradient start | `mood_gradients.accent.light[0]` | #266489 | confirm_button fill | Same as primary |
| Accent gradient end | `mood_gradients.accent.light[1]` | #50606E | Not used directly | No dual-tone surface on this form |

This screen is intentionally minimal in use of gradients — the design system's
`aesthetic_family: minimalist-ui` and `motion.intensity: low` mean form screens carry no
decorative surfaces. The hero gradient is appropriate for the payments hub tile background,
not for the form itself.

---

## 7. WCAG Contrast Audit

All pairs resolved against `design-tokens.yaml` light-mode values. Ratios sourced from
the design system's own validated set (W-01..W-32, 2026-08-02).

| Text Token | Background Token | Hex text | Hex bg | Ratio | Required | Pass? |
|---|---|---|---|---|---|---|
| onSurface | surface | #181C20 | #F7F9FF | 19.9:1 | 4.5:1 | Yes |
| onSurfaceVariant | surface | #41474D | #F7F9FF | 8.6:1 | 4.5:1 | Yes |
| onPrimary | primary | #FFFFFF | #266489 | 6.1:1 | 4.5:1 | Yes |
| error (bodySmall) | surface | #BA1A1A | #F7F9FF | 6.1:1 | 4.5:1 | Yes |
| onErrorContainer | errorContainer | #93000A | #FFDAD6 | 7.24:1 | 4.5:1 | Yes (W-03/W-06) |
| onSurface | surfaceContainer | #181C20 | #EBEEF3 | 17.9:1 | 4.5:1 | Yes |
| onSurfaceVariant | surfaceContainer | #41474D | #EBEEF3 | 7.5:1 | 4.5:1 | Yes |
| primary | surface (step label) | #266489 | #F7F9FF | 6.1:1 | 4.5:1 | Yes |
| outline (field border) | surface | #72787E | #F7F9FF | 4.24:1 | 3.0:1 (non-text) | Yes |
| outlineVariant (dividers) | surface | #C1C7CE | #F7F9FF | 1.62:1 | 1.0:1 (decorative) | Yes — decorative only, no control or glyph may use this pair (W-32 known failure) |

All text pairs meet WCAG AA (4.5:1). The outlineVariant/surface pair is below WCAG 1.4.11 but is
used only for decorative dividers per the design system's known constraint (W-32).

---

## 8. Responsive Variants

| Breakpoint | Layout changes |
|---|---|
| Compact (< 600dp) | Single column, full-width; this is the primary target (390dp baseline) |
| Medium (600–840dp) | Review card max-width 560dp, centred; amount field centred; list items remain full-width |
| Expanded (> 840dp) | Not declared in ui.yaml (`mobile_only: false`, `baseline_width: 390`) — apply Material 3 canonical layout for expanded displays if needed |

Note from `ui.yaml`: `responsive.mobile_only = false` and `baseline_width = 390`. The form is
designed for narrow single-column display. On wider viewports keep the scroll content at a
maximum content width of 560dp and centre it.
