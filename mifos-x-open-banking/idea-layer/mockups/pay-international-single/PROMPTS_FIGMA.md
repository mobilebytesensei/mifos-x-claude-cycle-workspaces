# PROMPTS_FIGMA — Pay Abroad (International Single Payment)

Design specs for Figma frame generation and Stitch render targets.
Design system: **Open Banking — Trust Blue** (Material 3, seed `#266489`, Roboto / Roboto Mono).
Source of truth for token values: `design-system/design-tokens.yaml`.

---

## Mood palette

| Role name | Light hex | Dark hex | Usage |
|-----------|-----------|----------|-------|
| `primary` | `#266489` | `#95CDF7` | Confirm CTA, active step, filled amount value |
| `onPrimary` | `#FFFFFF` | `#00344E` | CTA label text |
| `primaryContainer` | `#C9E6FF` | `#004B6F` | Selected account card fill |
| `onPrimaryContainer` | `#004B6F` | `#C9E6FF` | Text on selected account card |
| `secondary` | `#50606E` | `#B7C9D9` | FX disclosure banner stroke |
| `secondaryContainer` | `#D3E5F5` | `#384956` | FX disclosure banner fill |
| `onSecondaryContainer` | `#384956` | `#D3E5F5` | FX disclosure text |
| `surface` | `#F7F9FF` | `#101417` | Screen background |
| `surfaceContainer` | `#EBEEF3` | `#1C2024` | Card background (review_card, account cards) |
| `surfaceContainerHighest` | `#E0E3E8` | `#313539` | Skeleton shimmer fill |
| `onSurface` | `#181C20` | `#E0E3E8` | Body text, field input |
| `onSurfaceVariant` | `#41474D` | `#C1C7CE` | Labels, helper text, note text, disabled step labels |
| `outline` | `#72787E` | `#8B9198` | Text field border (default) |
| `outlineVariant` | `#C1C7CE` | `#41474D` | Dividers in review_card (decorative only — never bound to a control) |
| `error` | `#BA1A1A` | `#FFB4AB` | BIC length error text, debit amounts |
| `errorContainer` | `#FFDAD6` | `#93000A` | Error panel fill |
| `onErrorContainer` | `#93000A` | `#FFDAD6` | Error panel text |

Theme is **auto** — follow OS. Dynamic colour enabled on Android 12+.

---

## Typography mapping

| Stitch / Figma style | Roboto scale | Size / weight | Usage on this screen |
|----------------------|--------------|---------------|----------------------|
| `displaySmall` | displaySmall | 36sp / 400 | (not used) |
| `headlineSmall` | headlineSmall | 24sp / 400 | Amount field input text (mono) |
| `titleLarge` | titleLarge | 22sp / 400 | Top app bar title "Pay abroad" |
| `titleMedium` | titleMedium | 16sp / 500 | Review card header "Review your payment" |
| `titleSmall` | titleSmall | 14sp / 500 | Error panel title |
| `bodyLarge` | bodyLarge | 16sp / 400 | Field input text, review row values, account names |
| `bodyMedium` | bodyMedium | 14sp / 400 | FX disclosure body, empty-state body, error row messages |
| `bodySmall` | bodySmall | 12sp / 400 | Field labels (floating), helper text, notes |
| `labelLarge` | labelLarge | 14sp / 500 | Button labels ("Send £5.00", "Next →") |
| `labelMedium` | labelMedium | 12sp / 500 | Step indicator labels |
| `labelSmall` | labelSmall | 11sp / 500 | Error row path text, ineligible accounts note |

Amount field and all account-number / IBAN / BIC values: **Roboto Mono** (not Roboto).
Currency prefix in amount field (`£`, `$`, etc.) is `onSurfaceVariant` and NOT part of the editable value.

---

## Auto Layout specs

### Screen frame

```
Frame: 390 × auto (scrollable)
Auto Layout: vertical
Padding: 16dp all sides (spacing.md)
Gap: 16dp (spacing.md)
Fill: surface (#F7F9FF light)
```

### Top app bar

```
Component: M3 TopAppBar (CenterAligned)
Height: 64dp
Container fill: surface (#F7F9FF)
Title: titleLarge, onSurface (#181C20), "Pay abroad"
Navigation icon: arrow_back, icon.md (24dp), onSurface
No trailing actions
```

### Step indicator (stepper)

```
Component: custom horizontal stepper
Auto Layout: horizontal, 8dp gap
Width: fill-container
Height: 48dp (touch target)
Active step: filled circle (20dp), primary (#266489), labelMedium onPrimary
Completed step: filled circle, primaryContainer, check icon (icon.sm 20dp), onPrimaryContainer
Inactive step: outline circle (20dp), outline (#72787E), labelMedium onSurfaceVariant
Connector line: 1dp, outlineVariant; horizontal between circles
Labels below circles: labelSmall, onSurfaceVariant (all) / primary (active)
```

### Account card (debtor_account_list item)

```
Component: M3 Card (Outlined)
Auto Layout: vertical, 12dp gap
Padding: 16dp
Corner radius: radius.md (12dp)
Container fill: surfaceContainer (#EBEEF3)
Selected state: fill primaryContainer (#C9E6FF), border 2dp primary
Min height: 72dp

Row 1: horizontal, fill
  - Account name: bodyLarge, onSurface
  - Radio button (trailing): 20dp, primary when selected
Row 2: Mono account number: bodyMedium, Roboto Mono, onSurfaceVariant
Row 3: Available balance: labelLarge, Roboto Mono, primary (#266489)
```

### Text field (default — iban_field, payee_name_field, bic_field)

```
Component: M3 OutlinedTextField
Height: 56dp (form.field.min_height_dp)
Corner radius: radius.sm (8dp) [form.field.radius]
Outline default: 1dp, outline (#72787E) [form.field.outline_default]
Outline focused: 2dp, primary (#266489) [form.field.outline_focus]
Outline error: 2dp, error (#BA1A1A) [form.field.outline_error]
Label (floating): bodySmall, onSurfaceVariant
Input text: bodyLarge, onSurface, Roboto
Helper text (below): bodySmall, onSurfaceVariant
Error text (below): bodySmall, error (#BA1A1A)
Disabled opacity: 0.38 [form.field.disabled_opacity]
```

### Amount field (amount_field)

```
Component: M3 OutlinedTextField (amount variant)
Height: 56dp
Corner radius: radius.sm (8dp)
Prefix text: currency symbol, bodyLarge, onSurfaceVariant, Roboto (not part of editable value)
Input text: headlineSmall (24sp/400), onSurface, Roboto Mono [form.amount_field]
Alignment: left [form.amount_field.alignment = left]
Decimals: per instructed currency — NOT hardcoded to 2 decimal places
No leading/trailing icons
```

### Dropdown (currency pickers)

```
Component: M3 ExposedDropdownMenuBox
Height: 56dp
Corner radius: radius.sm (8dp)
Trailing icon: arrow_drop_down, icon.md (24dp), onSurfaceVariant
Container: outlined style (same token as text_field)
Option items: bodyLarge, onSurface
```

### Radio group (charge_bearer_picker)

```
Component: vertical column of M3 RadioButton rows
Gap between rows: 12dp (spacing.sm + spacing.xs)
Each row: horizontal, 8dp gap, 48dp min height (touch target)
  - RadioButton: 20dp, primary when selected
  - Label: bodyLarge, onSurface
```

### FX disclosure banner (fx_disclosure)

```
Component: M3 Card (no elevation, info variant)
Auto Layout: horizontal, 12dp gap, 16dp padding
Corner radius: radius.md (12dp)
Container fill: secondaryContainer (#D3E5F5)
Icon: info, icon.md (24dp), onSecondaryContainer (#384956)
Text: bodyMedium, onSecondaryContainer (#384956)
Visible only when instructedCurrency ≠ currencyOfTransfer
```

### Note text (no_reference_note, no_charge_note, ineligible_accounts_note)

```
Typography: bodySmall (12sp/400)
Color: onSurfaceVariant (#41474D)
Padding-top: 4dp (spacing.xs)
Prefix: ▸ character
```

### Review card (summary_card)

```
Component: M3 Card (Elevated, elevation.level1)
Auto Layout: vertical, 0dp gap
Padding: 16dp
Corner radius: radius.md (12dp)
Container fill: surfaceContainer (#EBEEF3)
Elevation: 1dp (elevation.level1)

Header row: titleMedium, onSurface, "Review your payment", padding-bottom 12dp

Each review row:
  Auto Layout: vertical, 2dp gap (spacing.xxs)
  Padding: 12dp horizontal, 8dp vertical
  Label: bodySmall, onSurfaceVariant
  Value: bodyLarge, onSurface (monetary values in Roboto Mono, primary)
  Divider between rows: 1dp outlineVariant (decorative, never around a control)

BIC row hidden when bic is blank (conditional visibility).
No fee row. No reference row.

Footer rows:
  "No payment reference" — bodySmall, onSurfaceVariant
  "No fee quoted by HSBC" — bodySmall, onSurfaceVariant
  Both preceded by ▸ prefix
```

### Confirm button (confirm_button)

```
Component: M3 Button (Filled)
Width: fill-container
Height: 48dp (touch_targets.comfortable)
Corner radius: radius.full (9999dp)
Container fill: primary (#266489)
Label: labelLarge, onPrimary (#FFFFFF), "Send £5.00"
  (Amount in the label is mandatory per irreversible_action.cta_label_by_rail)
On tap: locks immediately (opacity 0.38 on container), shows CircularProgressIndicator (16dp, onPrimary)
Double-submission: impossible — button is disabled while uiState is Submitting
```

### Cancel / secondary button

```
Component: M3 TextButton
Width: fill-container
Height: 48dp
Color: onSurface
Typography: labelLarge
"Cancel" label
Same visual weight row as confirm — neither option is visually subordinate
```

### Progress indicator (submitting_indicator)

```
Component: M3 CircularProgressIndicator (indeterminate)
Size: 48dp
Color: primary (#266489)
Centred in available space
Stage label below: bodyLarge, onSurface, centre-aligned
Label strings: StagingConsent / AwaitingAuthorisation / ConfirmingFunds / SubmittingPayment
```

### Error panel (error_panel)

```
Component: M3 Card (no elevation)
Auto Layout: vertical, 0dp gap
Padding: 16dp
Corner radius: radius.md (12dp)
Container fill: errorContainer (#FFDAD6)

Header row: horizontal, 8dp gap
  - error icon (icon.md 24dp), onErrorContainer (#93000A)
  - titleSmall, onErrorContainer (#93000A)

Each error row:
  Padding: 12dp all, 8dp bottom gap
  Divider above: 1dp outlineVariant
  Message: bodyMedium, onErrorContainer (#93000A)
  Path: labelSmall, onSurfaceVariant (#41474D), Roboto Mono
  Rows appear in WIRE ORDER — never sorted, never deduplicated
```

### Skeleton cards (loading state)

```
Component: M3 Card (Outlined)
Height: 72dp
Corner radius: radius.md (12dp)
Fill: surfaceContainerHighest (#E0E3E8)
Shimmer: horizontal gradient sweep, 150ms (motion.durations.short), looping
Reduced-motion fallback: static fill, no animation
Three cards, 16dp gap between each
```

### Bottom navigation

```
Component: M3 NavigationBar
Height: 80dp
Container fill: surfaceContainer (#EBEEF3)
Active icon + label: primary (#266489), labelMedium
Inactive: onSurfaceVariant (#41474D), labelMedium
Tabs: Home · Accounts · Pay (active on this screen) · More
```

---

## WCAG contrast checks

All pairs from `design-tokens.yaml#accessibility.validated_pairs` (32 pairs measured 2026-08-02).
Pairs relevant to this screen:

| Pair | Ratio (light) | WCAG target | Verdict |
|------|---------------|-------------|---------|
| `primary` on `surface` | 6.11:1 | AA (4.5:1) | pass |
| `onPrimary` on `primary` | 8.26:1 | AA (4.5:1) | pass |
| `onPrimaryContainer` on `primaryContainer` | 7.27:1 | AA (4.5:1) | pass |
| `onSecondaryContainer` on `secondaryContainer` | 7.22:1 | AA (4.5:1) | pass |
| `onErrorContainer` on `errorContainer` | 7.24:1 | AA (4.5:1) | pass |
| `error` on `surface` | 6.14:1 | AA (4.5:1) | pass |
| `onSurface` on `surface` | 15.1:1 | AA (4.5:1) | pass |
| `onSurfaceVariant` on `surface` | 7.28:1 | AA (4.5:1) | pass |
| `outline` on `surface` | 4.24:1 | AA (3.0:1 — non-text) | pass |
| `outlineVariant` on `surface` | 1.62:1 | decorative only | constrained — never bound to a control or glyph |
| `form.field.outline_default` on `surface` | 4.24:1 | AA non-text (3.0:1) | pass |
| `form.field.outline_focus` on `surface` | 6.11:1 | AA non-text (3.0:1) | pass |
| `form.field.error_text` on `surface` | 6.14:1 | AA (4.5:1) | pass |

Minimum touch target: 48dp (`touch_targets.comfortable`). Applies to every button, radio,
dropdown, and navigation item. Text fields are 56dp.

Colour is never the only signal: every form validation, payment disposition, and error state
carries an icon and a text label alongside the colour change (WCAG 1.4.1).

---

## Component variants summary

| Component | Variants |
|-----------|---------|
| text_field | default / focused / error / disabled |
| amount_field | default / focused / (no error variant — amount errors are contextual) |
| dropdown | closed / open (popover) |
| radio_group option | unselected / selected |
| account card | unselected / selected (primaryContainer fill) |
| step indicator item | inactive / active / completed |
| confirm_button | enabled / loading (spinner) / disabled |
| error_panel | single-entry / multi-entry (two rows, wire order) |
| fx_disclosure banner | hidden (currencies match) / visible (currencies differ) |
| bic_length_error | hidden (blank or valid length) / visible (non-blank, not 11 chars) |

---

<!-- Generated 2026-08-07 by /idea-feature-export from screens/pay-international-single/{ui,docs}.yaml + design-system/design-tokens.yaml. -->
