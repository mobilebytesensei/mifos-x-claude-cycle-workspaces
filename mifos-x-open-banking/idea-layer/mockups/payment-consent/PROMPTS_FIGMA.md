# payment-consent — Figma Design Prompt

> Generated from `screens/payment-consent/*.yaml` + `design-tokens.yaml` by `/idea-feature-export`
> Design System: Open Banking — Trust Blue (Material 3, seed #266489)
> Feature: payment-consent (headless transitional — 5 states)

---

## 1. Frame Setup

- **Frame sizes**: Android 412 × 892dp / iOS 393 × 852dp (iPhone 14 Pro)
- **Grid**: 4-column, 16dp gutter, 16dp margin (single-column layout in practice — centred content)
- **Status bar**: 54dp (system)
- **Top app bar**: 56dp, no bottom navigation bar
- **Safe area**: Top 54dp, Bottom 34dp (home indicator)
- **States to frame**: `validating` · `exchanging` · `checking` · `authorised` · `error_code_expired` · `error_rejected` · `error_state_mismatch` (7 frames minimum)

---

## 2. Design Token Variables

Create as Figma Local Variables (Mode: Light / Dark).

### Colors — Light Mode

| Variable Name | Hex | Usage |
|---|---|---|
| `color/primary` | `#266489` | Progress indicator, filled button, check-again label |
| `color/onPrimary` | `#FFFFFF` | Filled button label |
| `color/primaryContainer` | `#C9E6FF` | Authorised state icon container |
| `color/onPrimaryContainer` | `#004B6F` | Authorised state icon glyph + text |
| `color/surface` | `#F7F9FF` | Screen background, top app bar |
| `color/onSurface` | `#181C20` | Titles, progress text |
| `color/onSurfaceVariant` | `#41474D` | Body text, abandon-button label |
| `color/error` | `#BA1A1A` | Error state icon |
| `color/errorContainer` | `#FFDAD6` | (reserved for error banner if added later) |
| `color/onErrorContainer` | `#93000A` | (reserved) |
| `color/outline` | `#72787E` | Dividers, unfocused borders |

### Colors — Dark Mode

| Variable Name | Hex |
|---|---|
| `color/primary` | `#95CDF7` |
| `color/onPrimary` | `#00344E` |
| `color/primaryContainer` | `#004B6F` |
| `color/onPrimaryContainer` | `#C9E6FF` |
| `color/surface` | `#101417` |
| `color/onSurface` | `#E0E3E8` |
| `color/onSurfaceVariant` | `#C1C7CE` |
| `color/error` | `#FFB4AB` |
| `color/errorContainer` | `#93000A` |
| `color/onErrorContainer` | `#FFDAD6` |

### Typography

| Style | Font | Size (sp) | Weight | Line Height (sp) |
|---|---|---:|:---:|---:|
| `titleLarge` | Roboto | 22 | 400 | 28 |
| `headlineSmall` | Roboto | 24 | 400 | 32 |
| `bodyLarge` | Roboto | 16 | 400 | 24 |
| `bodyMedium` | Roboto | 14 | 400 | 20 |
| `labelLarge` | Roboto | 14 | 500 | 20 |

### Spacing

| Token | dp |
|---|---:|
| `spacing/sm` | 8 |
| `spacing/md` | 16 |
| `spacing/lg` | 24 |
| `spacing/xl` | 32 |

### Corner Radius

| Token | dp |
|---|---:|
| `radius/sm` | 8 |
| `radius/md` | 12 |
| `radius/full` | 9999 |

### Icon Sizes

| Token | dp |
|---|---:|
| `icon/md` | 24 |
| `icon/xl` | 48 |

---

## 3. Auto Layout Structure

### Frame: `payment_consent_validating`

```
Frame: payment_consent_validating (412 × 892, Auto Layout Vertical)
  ├─ TopAppBar (Fill × 56dp, Auto Layout Horizontal, padding H:16dp)
  │   └─ Title: "Authorising payment" (titleLarge, color/onSurface, Fill)
  │
  └─ CenteredContent (Fill, Auto Layout Vertical, alignment center, padding 16dp, gap 24dp)
      ├─ Spacer (Hug × auto, fills space above to center content)
      ├─ CircularProgressIndicator
      │   size: 48 × 48dp, color/primary stroke
      ├─ Text: "Confirming your approval…"
      │   bodyLarge, color/onSurface, center, maxWidth 280dp
      └─ Spacer (same as top)
```

### Frame: `payment_consent_exchanging`

```
Frame: payment_consent_exchanging (412 × 892, Auto Layout Vertical)
  ├─ TopAppBar  [same as validating]
  └─ CenteredContent  [same structure]
      ├─ CircularProgressIndicator  [same]
      └─ Text: "Connecting to your bank…"
          bodyLarge, color/onSurface, center
```

### Frame: `payment_consent_checking`

```
Frame: payment_consent_checking (412 × 892, Auto Layout Vertical)
  ├─ TopAppBar  [same]
  └─ CenteredContent (Auto Layout Vertical, center, padding 16dp, gap 24dp)
      ├─ CircularProgressIndicator  [same]
      ├─ Text: "Waiting for your bank to confirm…"
      │   bodyLarge, color/onSurface, center
      └─ TextButton: "Check again"
          labelLarge, color/primary
          minHeight: 48dp, paddingH: 24dp, paddingV: 8dp
          [state: Default / Pressed / Focused / Disabled]
```

### Frame: `payment_consent_authorised`

```
Frame: payment_consent_authorised (412 × 892, Auto Layout Vertical)
  ├─ TopAppBar  [same]
  └─ CenteredContent (Auto Layout Vertical, center, padding 16dp, gap 16dp)
      ├─ IconContainer (64 × 64dp, radius/md, fill color/primaryContainer)
      │   └─ Icon: verified_user (48dp, color/onPrimaryContainer)
      ├─ Title: "Authorisation confirmed"
      │   headlineSmall, color/onSurface, center
      └─ Body: "Your bank has approved the payment. Returning to your payment…"
          bodyMedium, color/onSurfaceVariant, center, maxWidth 280dp
```

### Frame: `payment_consent_error_code_expired`

```
Frame: payment_consent_error_code_expired (412 × 892, Auto Layout Vertical)
  ├─ TopAppBar  [same]
  └─ CenteredContent (Auto Layout Vertical, center, padding 16dp, gap 16dp)
      ├─ Icon: error_outline (48dp, color/error)
      ├─ Title: "Something went wrong"
      │   headlineSmall, color/onSurface, center
      ├─ Body: {strings.error.payment_consent.code_expired}
      │   bodyMedium, color/onSurfaceVariant, center, maxWidth 280dp
      ├─ FilledButton: "Restart authorisation"
      │   labelLarge, color/onPrimary, container color/primary
      │   radius/full, minHeight 48dp, paddingH 32dp
      │   [variants: Default / Pressed / Focused / Disabled]
      └─ TextButton: "Abandon payment"
          labelLarge, color/onSurfaceVariant, minHeight 48dp
```

### Frame: `payment_consent_error_rejected` (no restart CTA)

```
Frame: payment_consent_error_rejected (412 × 892, Auto Layout Vertical)
  ├─ TopAppBar  [same]
  └─ CenteredContent (Auto Layout Vertical, center, padding 16dp, gap 16dp)
      ├─ Icon: error_outline (48dp, color/error)
      ├─ Title: "Something went wrong"
      │   headlineSmall, color/onSurface, center
      ├─ Body: {strings.error.payment_consent.rejected}
      │   bodyMedium, color/onSurfaceVariant, center, maxWidth 280dp
      └─ TextButton: "Abandon payment"
          labelLarge, color/onSurfaceVariant, minHeight 48dp
```

### Frame: `payment_consent_error_state_mismatch` (no restart CTA — same shape as rejected)

Same structure as `error_rejected` with body text from `strings.error.payment_consent.state_mismatch`.

---

## 4. Component Variants

### `CircularProgressIndicator` / `authorising_indicator`

| Property | Value |
|---|---|
| Size | 48 × 48dp |
| Stroke width | 4dp |
| Color | `color/primary` |
| Indeterminate | true (spinning, not filled) |
| Accessibility label | `strings.payment_consent.progress_label` |

No interactive states — display only.

### `TextButton` / `check_again_button`

| State | Label color | Background | Shadow |
|---|---|---|---|
| Default | `color/primary` | transparent | none |
| Pressed | `color/primary` + ripple overlay (opacity 0.12) | transparent | none |
| Focused | `color/primary` | transparent + 2dp outline `color/primary` | none |
| Disabled | `color/onSurface` at 38% opacity | transparent | none |

- Typography: `labelLarge` (14sp, weight 500)
- Min height: 48dp (`touch_targets.comfortable`)
- Padding horizontal: 24dp (`spacing/lg`)
- Padding vertical: 8dp (`spacing/sm`)
- Corner radius: `radius/full` (9999dp) per M3 text button

### `FilledButton` / `restart_authorisation_button`

| State | Container | Label | Shadow |
|---|---|---|---|
| Default | `color/primary` | `color/onPrimary` | elevation level1 |
| Pressed | `color/primary` + ripple 12% | `color/onPrimary` | level1 |
| Focused | `color/primary` | `color/onPrimary` | level1, 2dp focus ring |
| Disabled | `color/onSurface` 12% | `color/onSurface` 38% | none |

- Typography: `labelLarge` (14sp, weight 500)
- Min height: 48dp
- Padding horizontal: 32dp (`spacing/xl`)
- Corner radius: `radius/full` (9999dp)

### `TextButton` / `abandon_button`

Same specs as `check_again_button` but label colour `color/onSurfaceVariant` in default and pressed states.

---

## 5. Assets Required

### Icons (Material Symbols — Outlined style)

| Icon | dp | State(s) | Filled / Outlined |
|---|---:|---|---|
| `verified_user` | 48 | authorised | Outlined |
| `error_outline` | 48 | error | Outlined |

No images. No illustrations. The design system's `minimal-ui` aesthetic applies here without exception — this screen is a machine in progress, not a celebration surface.

---

## 6. Mood Palette Usage Table

| Mood Color | Hex (light) | Components | Note |
|---|---|---|---|
| `mood_gradients.hero.light` | `#C9E6FF → #F7F9FF` | Unused | This screen is too brief and process-oriented for a hero gradient; the plain surface is intentional |
| `mood_gradients.accent.light` | `#266489 → #50606E` | Unused | Same reasoning — accent gradients are for contextual hub tiles, not a spinner screen |

Both mood gradients are documented as unused. The screen renders on the plain `color/surface` background. The trust-blue shows only through the progress indicator stroke and the filled button — both single-colour, not gradients.

---

## 7. WCAG Contrast Audit

| Text token | Background token | Ratio | Threshold | Pass? |
|---|---|---:|---:|:---:|
| `color/onSurface` (#181C20) on `color/surface` (#F7F9FF) | Progress detail, titles | 15.4:1 | 4.5:1 | Yes |
| `color/onSurfaceVariant` (#41474D) on `color/surface` (#F7F9FF) | Body text, abandon label | 7.3:1 | 4.5:1 | Yes |
| `color/primary` (#266489) on `color/surface` (#F7F9FF) | Indicator stroke, check-again label | 6.1:1 | 4.5:1 | Yes |
| `color/onPrimary` (#FFFFFF) on `color/primary` (#266489) | Filled button label | 6.1:1 | 4.5:1 | Yes |
| `color/onPrimaryContainer` (#004B6F) on `color/primaryContainer` (#C9E6FF) | Authorised icon + text | 7.3:1 | 4.5:1 | Yes |
| `color/error` (#BA1A1A) on `color/surface` (#F7F9FF) | Error icon (large) | 6.1:1 | 3:1 (large text / icon) | Yes |

All pairs WCAG AA. No pair uses `outlineVariant` on `surface` (that pair fails at 1.62:1 and is decorative-only per the design system contract — W-32).

---

## 8. Platform Animation Specs

**Motion intensity**: low (the project's `motion.intensity` dial — accessibility-first).

| Animation | Duration | Easing (iOS / Android) |
|---|---|---|
| State transition (validating → exchanging → checking) | 300ms cross-fade | iOS: `CABasicAnimation` with `kCAMediaTimingFunctionEaseInEaseOut` / Android: `FastOutSlowInInterpolator` |
| Circular progress indicator (continuous) | 1 333ms one revolution | iOS: `CABasicAnimation` `linear` / Android: `LinearInterpolator` |
| Button press ripple | 150ms | iOS: `UIView.animate(duration: 0.15)` / Android: M3 ripple default `RippleDrawable` |
| Error / authorised state entrance | 300ms fade-in | iOS: `CABasicAnimation` `kCAMediaTimingFunctionEaseInEaseOut` / Android: `FastOutSlowInInterpolator` |

**Reduce motion**: when the OS `preferReducedMotion` / `WindowManager.REDUCE_MOTION` flag is set, all transitions collapse to instant cuts; the circular indicator uses a determinate fill animation at low speed rather than a spinning indeterminate one.

---

## 9. Responsive Variants

This screen uses a centred single-column layout. It requires no layout changes across breakpoints — the `maxWidth: 280dp` on body text and the full-width buttons self-adapt.

| Breakpoint | Layout change |
|---|---|
| Compact (< 600dp) | Default layout — single column, centred |
| Medium (600–840dp) | Same layout, maxWidth 400dp on content column |
| Expanded (> 840dp) | Same layout, maxWidth 480dp on content column |
