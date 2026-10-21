# Payment Status — Figma Design Prompt

> Source: `screens/payment-status/*.yaml` + `design-system/design-tokens.yaml`
> Design System: Open Banking — Trust Blue · Material Design 3 · seed `#266489`
> Generated: 2026-08-07

---

## 1. Frame Setup

- **Frame**: Android (412 × 892dp)
- **Grid**: 4-column, 16dp gutter, 16dp margin
- **Status bar**: 24dp (system overlay)
- **Top App Bar**: 64dp (M3 Medium)
- **Bottom nav**: 80dp (visible on all states)
- **Safe area**: top 24dp, bottom 24dp
- **Scrollable content zone**: 892 − 24 − 64 − 80 − 24 = 700dp available

---

## 2. Design Token Variables

### Colors (Light Mode)

| Variable Name                    | Value       | Usage                                     |
|----------------------------------|-------------|-------------------------------------------|
| `color/primary`                  | `#266489`   | Active tab, filled buttons, credit amounts |
| `color/onPrimary`                | `#FFFFFF`   | Text on primary buttons                   |
| `color/primaryContainer`         | `#C9E6FF`   | terminal_success chip container           |
| `color/onPrimaryContainer`       | `#004B6F`   | terminal_success chip text + icon         |
| `color/secondary`                | `#50606E`   | Supporting text, tonal buttons            |
| `color/secondaryContainer`       | `#D3E5F5`   | in_progress chip container                |
| `color/onSecondaryContainer`     | `#384956`   | in_progress chip text + icon              |
| `color/error`                    | `#BA1A1A`   | terminal_failure chip text + icon, error_state icon |
| `color/errorContainer`           | `#FFDAD6`   | terminal_failure chip container           |
| `color/onErrorContainer`         | `#93000A`   | terminal_failure chip text + icon         |
| `color/surface`                  | `#F7F9FF`   | Screen background                         |
| `color/onSurface`                | `#181C20`   | Primary text (amounts, payee names)       |
| `color/surfaceVariant`           | `#DDE3EA`   | instruction_established chip container    |
| `color/onSurfaceVariant`         | `#41474D`   | instruction_established text + icon; supporting labels |
| `color/surfaceContainerLow`      | `#F1F4F9`   | payment_summary card fill                 |
| `color/outline`                  | `#72787E`   | Card dividers (decorative only — W-32 fails WCAG 1.4.11; never bound a control) |

### Colors (Dark Mode)

| Variable Name                    | Value       |
|----------------------------------|-------------|
| `color/primary`                  | `#95CDF7`   |
| `color/primaryContainer`         | `#004B6F`   |
| `color/onPrimaryContainer`       | `#C9E6FF`   |
| `color/secondaryContainer`       | `#384956`   |
| `color/onSecondaryContainer`     | `#D3E5F5`   |
| `color/error`                    | `#FFB4AB`   |
| `color/errorContainer`           | `#93000A`   |
| `color/onErrorContainer`         | `#FFDAD6`   |
| `color/surface`                  | `#101417`   |
| `color/onSurface`                | `#E0E3E8`   |
| `color/surfaceVariant`           | `#41474D`   |
| `color/onSurfaceVariant`         | `#C1C7CE`   |
| `color/surfaceContainerLow`      | `#181C20`   |

### Typography

| Style         | Font          | Size | Weight | Line Height |
|---------------|---------------|:----:|:------:|:-----------:|
| titleLarge    | Roboto        | 22sp | 400    | 28sp        |
| titleMedium   | Roboto        | 16sp | 500    | 24sp        |
| titleSmall    | Roboto        | 14sp | 500    | 20sp        |
| bodyLarge     | Roboto        | 16sp | 400    | 24sp        |
| bodyMedium    | Roboto        | 14sp | 400    | 20sp        |
| bodySmall     | Roboto        | 12sp | 400    | 16sp        |
| labelLarge    | Roboto        | 14sp | 500    | 20sp        |
| mono          | Roboto Mono   | —    | —      | —           |

Amount labels: `bodyLarge` weight 400, `color/onSurface`, mono font family.

### Spacing

| Token        | Value |
|--------------|:-----:|
| `spacing/xs` | 4dp   |
| `spacing/sm` | 8dp   |
| `spacing/md` | 16dp  |
| `spacing/lg` | 24dp  |
| `spacing/xl` | 32dp  |

### Corner Radius

| Token        | Value  | Usage                                     |
|--------------|:------:|-------------------------------------------|
| `radius/sm`  | 8dp    | text_field, tonal buttons                 |
| `radius/md`  | 12dp   | payment_summary card                      |
| `radius/full`| 9999dp | status_chip (pill), filled/tonal buttons  |

---

## 3. Auto Layout Structure

### Loading State

```
Frame: payment_status_loading (412 × 892dp, Fill, Auto Layout Vertical)
  ├─ StatusBar (412 × 24dp, system overlay)
  ├─ TopAppBar (412 × 64dp, Auto Layout Horizontal, padding 4/16)
  │   ├─ back_button (48 × 48dp, icon arrow_back 24dp, color/onSurface)
  │   └─ Title "Payment status" (titleLarge, color/onSurface, Fill)
  ├─ Body (Fill, Auto Layout Vertical, padding=16dp, centred alignment)
  │   └─ CircularProgressIndicator (48 × 48dp, color/primary, centred)
  └─ BottomNavBar (412 × 80dp, container=color/surfaceContainerLow)
      Pay tab active (color/primary)
```

### Content State — in_progress (single rail, settling)

```
Frame: payment_status_content_inprogress (412 × 892dp, Fill, Auto Layout Vertical)
  ├─ StatusBar (412 × 24dp)
  ├─ TopAppBar (412 × 64dp, Auto Layout Horizontal, padding 4/16)
  │   ├─ back_button (48 × 48dp, icon arrow_back 24dp)
  │   └─ Title "Payment status" (titleLarge)
  ├─ ScrollContent (Fill, Auto Layout Vertical, padding=16dp, gap=16dp, overflow=scroll)
  │   ├─ status_chip (Hug × 32dp, Auto Layout Horizontal, gap=8dp, padding=8/16, radius=full)
  │   │     fill: color/secondaryContainer (#D3E5F5)
  │   │     ├─ Icon: schedule (24dp, color/onSecondaryContainer)
  │   │     └─ Label: "Processing" (labelLarge, color/onSecondaryContainer)
  │   │
  │   ├─ payment_summary (Fill × Hug, Card, radius=12dp, fill=color/surfaceContainerLow, elevation=1)
  │   │     Auto Layout Vertical, padding=16dp, gap=8dp
  │   │     ├─ RowPair: "Amount" / "£850.00" (mono)
  │   │     ├─ RowPair: "To" / "Jameson Lettings"
  │   │     ├─ RowPair: "From" / "····3349"
  │   │     ├─ RowPair: "Reference" / "RENT-FLAT12"
  │   │     └─ RowPair: "Submitted" / "30 Jul 2026, 10:44"
  │   │
  │   ├─ in_progress_note (Fill × Hug, bodyMedium, color/onSurfaceVariant, padding=0)
  │   │     "The bank has accepted this payment. Settlement is typically confirmed within a few minutes."
  │   │
  │   └─ refresh_button (Fill × 48dp, tonal, radius=full)
  │         fill: color/secondaryContainer
  │         label: "Check again" (labelLarge, color/onSecondaryContainer)
  └─ BottomNavBar (412 × 80dp)
```

### Content State — terminal_success

```
Frame: payment_status_content_success (412 × 892dp)
  ├─ TopAppBar (same)
  ├─ ScrollContent
  │   ├─ status_chip
  │   │     fill: color/primaryContainer (#C9E6FF)
  │   │     ├─ Icon: check_circle (24dp, color/onPrimaryContainer)
  │   │     └─ Label: "Payment sent" (labelLarge, color/onPrimaryContainer)
  │   └─ payment_summary (same structure, no buttons)
  └─ BottomNavBar
```

### Content State — terminal_failure

```
Frame: payment_status_content_failure (412 × 892dp)
  ├─ TopAppBar (same)
  ├─ ScrollContent
  │   ├─ status_chip
  │   │     fill: color/errorContainer (#FFDAD6)
  │   │     ├─ Icon: error (24dp, color/onErrorContainer)
  │   │     └─ Label: "Payment not made" (labelLarge, color/onErrorContainer)
  │   ├─ payment_summary (same structure)
  │   └─ new_payment_button (Fill × 48dp, filled, radius=full)
  │         fill: color/primary
  │         label: "Make a new payment" (labelLarge, color/onPrimary)
  └─ BottomNavBar
```

### Content State — instruction_established (deferred rails)

```
Frame: payment_status_content_established (412 × 892dp)
  ├─ TopAppBar (same)
  ├─ ScrollContent
  │   ├─ status_chip
  │   │     fill: color/surfaceVariant (#DDE3EA)  ← hue-less, deliberate
  │   │     ├─ Icon: event_repeat (24dp, color/onSurfaceVariant)
  │   │     └─ Label: "Standing order set up" (labelLarge, color/onSurfaceVariant)
  │   ├─ payment_summary
  │   │     RowPair: "First payment" / "£0.01" (mono)
  │   │     RowPair: "To" / "Mr Mark"
  │   │     RowPair: "From" / "····3349"
  │   │     RowPair: "Frequency" / "Weekly"
  │   │     RowPair: "First date" / "13 Aug 2026"
  │   │     RowPair: "Final date" / "4 Dec 2026"
  │   │     [NO reference row — RemittanceInformation absent on international rails]
  │   │     RowPair: "Set up" / "6 Aug 2026, 10:35"
  │   └─ instruction_established_note (Fill × Hug, bodyMedium, color/onSurfaceVariant)
  │         "Your standing order has been set up. Individual payments cannot be tracked here."
  └─ BottomNavBar
```

### Error State

```
Frame: payment_status_error (412 × 892dp, Fill, Auto Layout Vertical)
  ├─ TopAppBar (same)
  ├─ ErrorContent (Fill, Auto Layout Vertical, padding=16dp, gap=16dp, centred)
  │   ├─ Icon: error_outline (48dp, color/error)
  │   ├─ Title: "Something went wrong" (headlineSmall, color/onSurface, centre)
  │   ├─ Message: {error.message} (bodyMedium, color/onSurfaceVariant, centre)
  │   └─ retry_button (Hug × 48dp, filled, radius=full) — visible only when retryable
  │         fill: color/primary
  │         label: "Try again" (labelLarge, color/onPrimary)
  └─ BottomNavBar
```

---

## 4. Component Variants

### status_chip

**Variant Properties**:
| Property    | Values                                                                    |
|-------------|---------------------------------------------------------------------------|
| Disposition | in_progress, terminal_success, terminal_failure, instruction_established  |
| Theme       | light, dark                                                               |

**Specifications** (per disposition):

| Disposition             | Container           | On-container        | Icon          | Radius |
|-------------------------|---------------------|---------------------|---------------|--------|
| in_progress             | `#D3E5F5` / `#384956`| `#384956` / `#D3E5F5`| schedule     | full   |
| terminal_success        | `#C9E6FF` / `#004B6F`| `#004B6F` / `#C9E6FF`| check_circle | full   |
| terminal_failure        | `#FFDAD6` / `#93000A`| `#93000A` / `#FFDAD6`| error        | full   |
| instruction_established | `#DDE3EA` / `#41474D`| `#41474D` / `#C1C7CE`| event_repeat | full   |

Padding: 8dp vertical, 16dp horizontal. Icon 24dp leading. Label labelLarge. Height: 32dp.
ALL four dispositions must show icon + text label. Colour alone is never the signal (WCAG 1.4.1).

### payment_summary (Card)

| Property   | Value                       |
|------------|-----------------------------|
| Width      | Fill                        |
| Radius     | 12dp (`radius/md`)          |
| Container  | `color/surfaceContainerLow` |
| Elevation  | 1                           |
| Padding    | 16dp (`spacing/md`)         |
| Row gap    | 8dp (`spacing/sm`)          |

RowPair layout: Auto Layout Horizontal, gap=8dp, Fill.
- Label column: bodySmall, color/onSurfaceVariant, fixed width 96dp
- Value column: bodyMedium (titleMedium for amounts), color/onSurface, Fill
- Amount value: Roboto Mono font family

### refresh_button (Tonal)

| Property  | Value                        |
|-----------|------------------------------|
| Width     | Fill                         |
| Height    | 48dp                         |
| Radius    | full (9999dp)                |
| Container | `color/secondaryContainer`   |
| Label     | labelLarge, onSecondaryContainer |

Interactive states:
| State    | Opacity overlay |
|----------|:---------------:|
| Default  | 0%              |
| Pressed  | 12% onSecondaryContainer ripple |
| Focused  | 12% + 2dp border |
| Disabled | 38%             |

### new_payment_button (Filled)

| Property  | Value                  |
|-----------|------------------------|
| Width     | Fill                   |
| Height    | 48dp                   |
| Radius    | full                   |
| Container | `color/primary`        |
| Label     | labelLarge, onPrimary  |

---

## 5. Assets Required

### Icons (Material Symbols)

| Icon          | Size  | Usage                                    | Style    |
|---------------|:-----:|------------------------------------------|----------|
| arrow_back    | 24dp  | back_button in top app bar               | Outlined |
| schedule      | 24dp  | in_progress status_chip                  | Outlined |
| check_circle  | 24dp  | terminal_success status_chip             | Outlined |
| error         | 24dp  | terminal_failure status_chip             | Outlined |
| event_repeat  | 24dp  | instruction_established status_chip      | Outlined |
| error_outline | 48dp  | error_state illustration                 | Outlined |
| block         | 24dp  | VRP revoked mandate chip (MOCKUP.md ref) | Outlined |

---

## 6. WCAG Contrast Audit

All pairs from `design-tokens.yaml` validated at AA (4.5:1 text, 3:1 large/UI).

| Text token               | Background token          | Ratio (light) | Required | Pass? |
|--------------------------|---------------------------|:-------------:|:--------:|:-----:|
| onSecondaryContainer     | secondaryContainer        | 7.22:1        | 4.5:1    | Yes   |
| onPrimaryContainer       | primaryContainer          | 7.27:1        | 4.5:1    | Yes   |
| onErrorContainer         | errorContainer            | 7.24:1        | 4.5:1    | Yes   |
| onSurfaceVariant         | surfaceVariant            | 7.28:1        | 4.5:1    | Yes   |
| onSurface                | surface                   | 11.5:1        | 4.5:1    | Yes   |
| onSurfaceVariant         | surface                   | 5.68:1        | 4.5:1    | Yes   |
| error                    | surface                   | 6.14:1        | 4.5:1    | Yes   |
| outlineVariant           | surface                   | 1.62:1        | —        | Decor only — W-32 known fail; never bound a control |

No new pairs in this feature — all reuse measured pairs (W-02/W-05, W-03/W-06, W-16/W-17, W-30).

---

## 7. Mood Palette Usage

| Mood token                      | Hex (light)   | Component(s)                        | If Unused — Reason                                        |
|---------------------------------|---------------|-------------------------------------|-----------------------------------------------------------|
| `mood_gradients.hero.light[0]`  | `#C9E6FF`     | (none in this screen)               | Hero gradient — detail screens use flat surface, not hero wash |
| `mood_gradients.hero.light[1]`  | `#F7F9FF`     | screen background (surface)         | Indirect — surface resolves to this value                  |
| `mood_gradients.accent.light[0]`| `#266489`     | primary action buttons, filled CTA  | Via color/primary                                          |
| `mood_gradients.accent.light[1]`| `#50606E`     | tonal button (refresh_button)       | Via color/secondary → secondaryContainer                  |

---

## 8. Animation Specs

| Interaction       | Duration | iOS (CABasicAnimation)                      | Android (Interpolator)                  |
|-------------------|:--------:|---------------------------------------------|-----------------------------------------|
| Chip state change | 150ms    | `timingFunction: .easeInEaseOut`, duration: 0.15 | `FastOutSlowInInterpolator` (150ms) |
| Screen enter      | 300ms    | `timingFunction: .easeOut`, duration: 0.30  | `DecelerateInterpolator` (300ms)        |
| Button press      | 100ms    | `timingFunction: .linear`, duration: 0.10   | Ripple (instant visual, 100ms settle)  |

Motion intensity: low (`design-tokens.yaml motion.intensity`). No decorative transitions —
each animation serves a state change that communicates information. Reduce-motion supported:
all animations disable when the system accessibility flag is set.
