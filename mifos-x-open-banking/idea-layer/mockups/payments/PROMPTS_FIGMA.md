# Payments Hub — Figma Design Prompt

> Feature: `payments` · State: `content` (only state)
> Design System: Open Banking — Trust Blue (Material 3, seed `#266489`)
> Source: `screens/payments/ui.yaml` · `design-tokens.yaml` v2.4.0

---

## 1. Frame Setup

- **Frame:** Android 390 × 844dp (baseline) / iPhone 14 Pro 393 × 852pt
- **Grid:** 4-column, 16dp gutter, 16dp margin
- **Status bar:** 24dp (Android) / 54dp (iOS notch area)
- **Bottom nav:** 80dp — visible and active on `Pay` tab
- **Safe area:** top 24dp, bottom 34dp (home indicator / gesture bar)
- **Content area (scrollable):** frame height minus status bar minus bottom nav

---

## 2. Design Token Variables

Create as Figma Local Variables (collection: "Open Banking — Trust Blue").

### Colors — Light Mode

| Variable Name                    | Value     | Usage                                   |
|----------------------------------|-----------|-----------------------------------------|
| `color/primary`                  | `#266489` | Active tab, tile icon, pressed overlay  |
| `color/onPrimary`                | `#FFFFFF` | Text on primary containers              |
| `color/primaryContainer`         | `#C9E6FF` | (not used on hub, declared for system completeness) |
| `color/onPrimaryContainer`       | `#004B6F` | (system completeness)                   |
| `color/secondary`                | `#50606E` | (system completeness)                   |
| `color/surface`                  | `#F7F9FF` | Screen background                       |
| `color/onSurface`                | `#181C20` | Hub heading, tile labels                |
| `color/surfaceVariant`           | `#DDE3EA` | (system completeness)                   |
| `color/onSurfaceVariant`         | `#41474D` | Tile descriptions, amend notice         |
| `color/surfaceContainer`         | `#EBEEF3` | Bottom nav bar background               |
| `color/surfaceContainerLow`      | `#F1F4F9` | Tile card backgrounds                   |
| `color/outline`                  | `#72787E` | (not used on hub — decorative only)     |
| `color/outlineVariant`           | `#C1C7CE` | Tile card border at rest (decorative — never on text or glyphs; fails WCAG 1.4.11 against surface) |
| `color/error`                    | `#BA1A1A` | (system completeness — not used on hub) |

### Colors — Dark Mode

| Variable Name                    | Value     |
|----------------------------------|-----------|
| `color/primary`                  | `#95CDF7` |
| `color/onPrimary`                | `#00344E` |
| `color/surface`                  | `#101417` |
| `color/onSurface`                | `#E0E3E8` |
| `color/onSurfaceVariant`         | `#C1C7CE` |
| `color/surfaceContainer`         | `#1C2024` |
| `color/surfaceContainerLow`      | `#181C20` |
| `color/outlineVariant`           | `#41474D` |
| `color/error`                    | `#FFB4AB` |

### Typography Styles

| Style         | Font       | Size | Weight | Line Height |
|---------------|------------|:----:|:------:|:-----------:|
| `titleMedium` | Roboto     | 16sp | 500    | 24sp        |
| `bodySmall`   | Roboto     | 12sp | 400    | 16sp        |
| `labelMedium` | Roboto     | 12sp | 500    | 16sp        |
| `labelLarge`  | Roboto     | 14sp | 500    | 20sp        |

### Spacing

| Token         | Value |
|---------------|:-----:|
| `spacing/xs`  | 4dp   |
| `spacing/sm`  | 8dp   |
| `spacing/md`  | 16dp  |
| `spacing/lg`  | 24dp  |

### Corner Radius

| Token       | Value  |
|-------------|:------:|
| `radius/sm` | 8dp    |
| `radius/md` | 12dp   |
| `radius/lg` | 16dp   |
| `radius/xl` | 28dp   |

### Icon Sizes

| Token      | Value |
|------------|:-----:|
| `icon/md`  | 24dp  |

---

## 3. Auto Layout Structure — Content State (only state)

```
Frame: payments_content (Fill × Fill, Auto Layout Vertical)
  │
  ├─ StatusBar (Fill × 24dp, system chrome)
  │
  ├─ ScrollContent (Fill, Auto Layout Vertical, padding 16/16/0/16, gap 0, overflow Scroll)
  │   │
  │   ├─ hub_heading (Fill × Hug, Auto Layout)
  │   │   Text: "How do you want to pay?"
  │   │   Style: titleMedium / color/onSurface
  │   │   Padding: top 16dp, bottom 8dp
  │   │
  │   ├─ payment_type_grid (Fill, Auto Layout Vertical, gap 12dp)
  │   │   │   padding: 0 (outer padding provided by ScrollContent)
  │   │   │
  │   │   ├─ GridRow1 (Fill, Auto Layout Horizontal, gap 12dp)
  │   │   │   ├─ tile_domestic_single        (1/3 Fill × Hug, see Tile Anatomy)
  │   │   │   ├─ tile_domestic_scheduled     (1/3 Fill × Hug)
  │   │   │   └─ tile_domestic_standing_order (1/3 Fill × Hug)
  │   │   │
  │   │   ├─ GridRow2 (Fill, Auto Layout Horizontal, gap 12dp)
  │   │   │   ├─ tile_international_single         (1/3 Fill × Hug)
  │   │   │   ├─ tile_international_scheduled      (1/3 Fill × Hug)
  │   │   │   └─ tile_international_standing_order (1/3 Fill × Hug)
  │   │   │
  │   │   └─ GridRow3 (Fill, Auto Layout Horizontal, gap 12dp)
  │   │       ├─ tile_vrp_mandate   (1/3 Fill × Hug)
  │   │       ├─ Spacer             (1/3 Fill — empty, no background)
  │   │       └─ Spacer             (1/3 Fill — empty, no background)
  │   │
  │   └─ amend_notice (Fill × Hug, Auto Layout)
  │       Text: "To change or cancel a standing order or scheduled payment, you'll need
  │              to do this in the HSBC app or by calling HSBC directly. Third-party apps
  │              cannot change existing recurring payments."
  │       Style: bodySmall / color/onSurfaceVariant
  │       Padding: top 16dp, bottom 24dp
  │
  └─ BottomNavBar (Fill × 80dp, Auto Layout Horizontal, space-between, padding 0/16)
      Fill: color/surfaceContainer
      │
      ├─ NavItem_Home     (Hug, Auto Layout Vertical, center, gap 4dp) — inactive
      │   ├─ Icon: home (24dp, color/onSurfaceVariant)
      │   └─ Label: "Home" (labelSmall, color/onSurfaceVariant)
      │
      ├─ NavItem_Accounts (Hug, Auto Layout Vertical, center, gap 4dp) — inactive
      │   ├─ Icon: account_balance (24dp, color/onSurfaceVariant)
      │   └─ Label: "Accounts" (labelSmall, color/onSurfaceVariant)
      │
      ├─ NavItem_Pay      (Hug, Auto Layout Vertical, center, gap 4dp) — ACTIVE
      │   ├─ Icon: payment (24dp, color/primary)
      │   └─ Label: "Pay" (labelSmall, color/primary, weight 500)
      │
      └─ NavItem_More     (Hug, Auto Layout Vertical, center, gap 4dp) — inactive
          ├─ Icon: more_horiz (24dp, color/onSurfaceVariant)
          └─ Label: "More" (labelSmall, color/onSurfaceVariant)
```

### Tile Anatomy (component shared by all 7 tiles)

```
rail_tile (1/3 Fill × Fixed height matching width for 1:1 aspect ratio)
  Fill: color/surfaceContainerLow
  Corner: radius/md (12dp)
  Border: 1dp color/outlineVariant (decorative — not on glyphs or text)
  Elevation: level 1 (tonal, M3 surface tint)
  Padding: 16dp all sides
  Layout: Auto Layout Vertical, gap 8dp, align start
  Min tap target: 48dp × 48dp (touch overlay)
  │
  ├─ tile_icon (24dp × 24dp, color/primary, Material Symbols Outlined)
  ├─ tile_label (Fill, labelMedium, color/onSurface)
  └─ tile_description (Fill, bodySmall, color/onSurfaceVariant, max 2 lines)
```

---

## 4. Component Variants

### Component: `rail_tile`

**Variant Properties:**

| Property | Values                       |
|----------|------------------------------|
| State    | Default, Pressed, Focused    |
| Rail     | domestic_single · domestic_scheduled · domestic_standing_order · international_single · international_scheduled · international_standing_order · vrp_mandate |

**Default state:**
- Background: `color/surfaceContainerLow`
- Border: 1dp `color/outlineVariant`
- Elevation: level 1
- Icon: `color/primary`

**Pressed state:**
- Background: `color/surfaceContainerLow`
- Ripple overlay: `color/primary` at 12% opacity (scrim layer)
- Border: 1dp `color/outlineVariant`

**Focused state:**
- Background: `color/surfaceContainerLow`
- Focus ring: 2dp `color/primary` (replaces outlineVariant border)
- Icon: `color/primary`

**Tile content by rail:**

| Rail Component                    | Icon              | Label                   | Description                              |
|-----------------------------------|-------------------|-------------------------|------------------------------------------|
| tile_domestic_single              | `payments`        | Pay someone             | One payment, sent now                    |
| tile_domestic_scheduled           | `event`           | Pay on a date           | One payment, on a future date            |
| tile_domestic_standing_order      | `repeat`          | Standing order          | Same payment, repeating                  |
| tile_international_single         | `public`          | Pay abroad              | One overseas payment, sent now           |
| tile_international_scheduled      | `public_off`      | Pay abroad on a date    | One overseas payment, on a future date   |
| tile_international_standing_order | `currency_exchange` | Overseas standing order | Same overseas payment, repeating       |
| tile_vrp_mandate                  | `all_inclusive`   | Variable payments       | Set limits once, pay any amount within them |

---

## 5. Assets Required

### Icons (Material Symbols Outlined, 24dp)

| Icon                | Style    | Usage                        |
|---------------------|----------|------------------------------|
| `payments`          | Outlined | Tile 1 — Pay someone         |
| `event`             | Outlined | Tile 2 — Pay on a date       |
| `repeat`            | Outlined | Tile 3 — Standing order      |
| `public`            | Outlined | Tile 4 — Pay abroad          |
| `public_off`        | Outlined | Tile 5 — Pay abroad on a date |
| `currency_exchange` | Outlined | Tile 6 — Overseas standing order |
| `all_inclusive`     | Outlined | Tile 7 — Variable payments   |
| `home`              | Outlined | Bottom nav — Home            |
| `account_balance`   | Outlined | Bottom nav — Accounts        |
| `payment`           | Filled   | Bottom nav — Pay (active)    |
| `more_horiz`        | Outlined | Bottom nav — More            |

All icons: 24dp (`icon/md`), Material Symbols. The active nav icon (`payment`) uses the Filled
weight to signal the active state without requiring a colour change on the frame itself.

---

## 6. Mood Palette Usage

The "Open Banking — Trust Blue" system defines a hero mood gradient for use on splash, hero cards,
and onboarding. On this screen it is unused because:

| Mood Token                    | Used on Payments Hub? | Reason if unused                                     |
|-------------------------------|-----------------------|------------------------------------------------------|
| `mood_gradients.hero.light`   | No                    | Hub is a navigation grid — no hero imagery region    |
| `mood_gradients.hero.dark`    | No                    | Same                                                 |
| `mood_gradients.accent.light` | No                    | Hub has no accent decoration; tiles are flat cards   |
| `mood_gradients.accent.dark`  | No                    | Same                                                 |

The hub's minimalism is intentional: the pay tab must not promote any single rail above the others,
and a hero gradient behind the grid would do exactly that.

---

## 7. WCAG Contrast Audit

All pairs on this screen, with measured ratios from `design-tokens.yaml#accessibility`:

| Text Token             | Background Token          | Ratio  | Required | Pass? | Note |
|------------------------|---------------------------|:------:|:--------:|:-----:|------|
| `onSurface` (#181C20)  | `surface` (#F7F9FF)       | 15.84:1 | 4.5:1   | PASS  | hub_heading |
| `onSurface` (#181C20)  | `surfaceContainerLow` (#F1F4F9) | 14.21:1 | 4.5:1 | PASS | tile labels |
| `onSurfaceVariant` (#41474D) | `surface` (#F7F9FF) | 7.28:1  | 4.5:1   | PASS  | amend_notice |
| `onSurfaceVariant` (#41474D) | `surfaceContainerLow` (#F1F4F9) | 6.50:1 | 4.5:1 | PASS | tile descriptions |
| `primary` (#266489)    | `surfaceContainerLow` (#F1F4F9) | 6.11:1 | 3.0:1   | PASS  | tile icons (graphic, large) |
| `primary` (#266489)    | `surfaceContainer` (#EBEEF3)   | 5.96:1 | 4.5:1   | PASS  | active nav label |
| `onSurfaceVariant` (#41474D) | `surfaceContainer` (#EBEEF3) | 6.39:1 | 4.5:1 | PASS | inactive nav labels |
| `outlineVariant` (#C1C7CE) | `surface` (#F7F9FF)    | 1.62:1  | N/A      | DECORATIVE ONLY | tile border — must not carry text or glyphs (W-32 known failure, documented in design-tokens.yaml) |

All foreground/background pairs that carry text or icons pass WCAG AA (4.5:1 normal, 3:1 large /
graphic). The `outlineVariant` tile border fails WCAG 1.4.11 (non-text contrast 3:1) but is a
purely decorative hairline and is explicitly constrained to this use by the design token file.

---

## 8. Responsive Variants

| Breakpoint   | Grid Columns | Tile gap | Screen margin |
|:------------:|:-----------:|:--------:|:-------------:|
| < 600dp      | 3            | 12dp     | 16dp          |
| ≥ 600dp      | 4            | 12dp     | 24dp          |

Row 3 at 3-column layout: tile 7 (VRP) left-aligned; two empty cells on the right. The left
alignment is intentional — VRP is the last-in-reading-order item, and centring it would make it
look like a feature highlight, which contradicts the equal-weight tile contract.

---

## 9. Motion / Animation

The app's motion dial is **low intensity** (`motion.intensity: low`, `motion.durations.medium: 300ms`).

| Interaction       | Animation                                    | Easing                                                   |
|-------------------|----------------------------------------------|----------------------------------------------------------|
| Tile tap ripple   | Radial ripple, 300ms, fade to 0 opacity      | Android: `AccelerateDecelerateInterpolator` · iOS: `CABasicAnimation` ease-in-out |
| Tab switch to Pay | Standard M3 navigation bar indicator slide  | `cubic-bezier(0.2, 0.0, 0, 1.0)` (M3 emphasis easing)   |
| Screen entrance   | None — direct render (no enter animation for the Pay tab landing) | — |

`prefers-reduced-motion` / Android `animatorDurationScale == 0`: ripple fires and immediately
settles; no cross-frame animation plays.
