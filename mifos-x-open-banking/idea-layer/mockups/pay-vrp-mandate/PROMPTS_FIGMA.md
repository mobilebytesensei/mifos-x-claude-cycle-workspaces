# Figma Prompt Guide — pay-vrp-mandate

Design system: Open Banking — Trust Blue v1.4.0  
Seed: #266489 (Material Theme Builder export)  
Theme: auto (light shown; dark roles in `design-tokens.yaml`)

---

## Auto Layout Conventions

All screens use Auto Layout with direction=vertical, alignment=top-start.

| Surface | Direction | Spacing | Padding |
|---|---|---|---|
| Screen content area | Vertical | 12dp between sections | 16dp all sides |
| Card interior | Vertical | 8dp between rows | 16dp all sides |
| Row inside card | Horizontal | auto (space-between) | 0dp |
| Chip | Horizontal | 6dp (icon + label) | 8dp H · 4dp V |
| Banner | Horizontal | 12dp (icon + text) | 16dp all sides |
| Button | Horizontal | 8dp (icon + label) | 24dp H · 12dp V |
| Dialog | Vertical | 16dp between sections | 24dp all sides |

Minimum touch target: 48dp × 48dp on all interactive elements.

---

## Component Variants

### MandateHealthChip

Variant property: `state` ∈ {active, failing, unpayable, revoked}

| State | Icon | Fill | Icon + label colour | Label text |
|---|---|---|---|---|
| active | autorenew | primaryContainer | onPrimaryContainer | Active |
| failing | schedule | tertiaryContainer | onTertiaryContainer | Payments failing |
| unpayable | error_outline | errorContainer | onErrorContainer | Cannot pay |
| revoked | block | surfaceVariant | onSurfaceVariant | Cancelled |

Corner radius: full (pill). Icon size: 16dp. Typography: labelSmall (Roboto 11sp medium). Width: hug-contents.

**Do not create a StatusChip variant for mandate health.** It is a separate component family. The `active` state reuses `primaryContainer / onPrimaryContainer` but its icon (`autorenew`) disambiguates it from the settled-payment chip (`check_circle` on `primaryContainer`).

### MandateRow card

ElevatedCard: corner radius 12dp (medium) · fill=surfaceContainer · shadow elevation 1dp.

Interior layout (horizontal):
- Leading: Icon(autorenew · 40×40dp · primary) inside a 48×48dp Box
- Body (vertical, flex-grow): titleMedium / bodySmall
- Trailing: MandateHealthChip

### HeadroomBar

LinearProgressIndicator: height=4dp · corner-radius=full · progress-fill=primary · track-fill=primaryContainer. Label row above: bodyMedium (period name) and bodySmall (spent/limit) in onSurface / onSurfaceVariant respectively.

### ReviewCard

ElevatedCard: radius=medium · fill=surfaceContainer · elevation=1. Each row: horizontal, label=bodyMedium/onSurfaceVariant (min-width=120dp) · value=bodyLarge/onSurface (flex-grow). 8dp between rows.

### PaymentAmountField

AmountField variant: prefix "£" (non-editable, Roboto Mono headlineSmall · onSurface) · input Roboto Mono headlineSmall · onSurface · stroke outline · radius 8dp (small) · fill surfaceContainerLow. Height: 64dp. Error state: stroke=error, helper text=error/bodySmall below.

---

## Token Mappings (light mode)

All token names resolve from `design-tokens.yaml`. Do not use literal hex in Figma styles — use the token names below mapped to Figma Variables.

| Token | Hex (light) | Usage |
|---|---|---|
| `colors.primary` | #266489 | Active chip icon/label, Pay now button fill, progress bar, active bottom-nav tab |
| `colors.onPrimary` | #FFFFFF | Button label, icon on primary fills |
| `colors.primaryContainer` | #C9E6FF | Active health chip fill, settling indicator track |
| `colors.onPrimaryContainer` | #004B6F | Active health chip icon + label |
| `colors.secondary` | #50606E | In-progress/settling indicators, step indicator text |
| `colors.secondaryContainer` | #D3E5F5 | (not used on this screen) |
| `colors.tertiary` | #64597B | Failing health chip, warning banner icon |
| `colors.tertiaryContainer` | #EADDFF | Failing chip fill, info/warning banner fill |
| `colors.onTertiaryContainer` | #4C4162 | Failing chip icon + label, banner text |
| `colors.error` | #BA1A1A | Unpayable chip, revoke button, error field outlines |
| `colors.errorContainer` | #FFDAD6 | Unpayable chip fill, error banner fill |
| `colors.onErrorContainer` | #93000A | Unpayable chip icon + label, error banner text |
| `colors.surface` | #F7F9FF | Screen background |
| `colors.surfaceContainer` | #EBEEF3 | Card fills |
| `colors.surfaceContainerHigh` | #E5E8ED | Dialog fill |
| `colors.surfaceVariant` | #DDE3EA | Revoked chip fill |
| `colors.onSurface` | #181C20 | Primary text, screen titles |
| `colors.onSurfaceVariant` | #41474D | Supporting text, revoked chip icon + label, limit labels |
| `colors.outline` | #72787E | Text field outlines (unfocused), dividers |

---

## Mood Palette

**Character:** calm, regulated trust-blue. Steel-blue primary on near-white surfaces. No green, no amber, no celebration. Low-motion.

- **Background:** surfaceContainer cards on surface background — minimal tonal lift, no hard shadows
- **Accent:** primary blue marks intent only (active action, active tab, active mandate). Not used for fills or decoration
- **Warning:** tertiary violet-grey signals "attention needed but not broken" — failing mandate, first-period caution
- **Error:** error red marks "unable to proceed" — unpayable mandate, field faults, Revoke button text. Not used for the Revoke confirm CTA fill (which stays primary, per DESIGN.md Do's and Don'ts)
- **Neutral muting:** surfaceVariant + onSurfaceVariant for revoked mandates, supporting text, step indicators — the "nothing happening here" palette

Avoid gradients, decorative shadows, and celebratory motifs. A settled VRP payment receives the trust-blue `status_chip` with `check_circle`, not a green tick or animation.

---

## Typography

| Role | Style | Font | Weight | Colour token |
|---|---|---|---|---|
| Screen title | headlineSmall | Roboto 24sp | 400 | onSurface |
| Card section label | titleMedium | Roboto 16sp | 500 | onSurface |
| Body / list primary | bodyLarge | Roboto 16sp | 400 | onSurface |
| Supporting / metadata | bodyMedium | Roboto 14sp | 400 | onSurfaceVariant |
| Chip / small label | labelSmall | Roboto 11sp | 500 | (per chip token above) |
| Button label | labelLarge | Roboto 14sp | 500 | onPrimary |
| Monetary amounts | headlineSmall | Roboto Mono 24sp | 400 | onSurface |
| Limit figures | bodyLarge | Roboto Mono 16sp | 400 | onSurface |

Maximum two type sizes per card (DESIGN.md). Use whitespace, not weight, for hierarchy.

---

## WCAG Contrast

All pairs are measured pairs from `state/DESIGN_SYSTEM_STATE.yaml`. No new pairs are introduced in this feature — every colour combination reuses a previously measured pair.

| Pair | Foreground | Background | Ratio | Reference |
|---|---|---|---|---|
| onPrimaryContainer / primaryContainer | #004B6F | #C9E6FF | 7.27:1 | W-02/W-05 |
| onTertiaryContainer / tertiaryContainer | #4C4162 | #EADDFF | 7.27:1 | W-16/W-17 |
| onErrorContainer / errorContainer | #93000A | #FFDAD6 | 7.24:1 | W-03/W-06 |
| onSurfaceVariant / surfaceVariant | #41474D | #DDE3EA | 7.28:1 | W-30 |
| onSurface / surface | #181C20 | #F7F9FF | 16.7:1 | — |
| primary / surface | #266489 | #F7F9FF | 5.4:1 (AA large) | — |

All chip pairs meet WCAG AA (4.5:1 minimum for normal text). The three tonal chip pairs sit within 0.041 of each other so no health state shouts louder than another (DESIGN.md calibration note).

**`outlineVariant` on `surface` (1.62:1, W-32):** decorative only. Never use it to bound a control or carry a glyph.

---

## Elevation & Depth

- Cards: tonal elevation 1 (surfaceContainer fill, 1dp shadow) — never hard drop shadows
- Dialogs: tonal elevation 3 (surfaceContainerHigh fill)
- Bottom sheet (pay sheet): elevation 3, top corners extra_large (28dp)
- Bottom nav bar: surfaceContainerHighest (highest tonal step)

No elevation above level 3 on content surfaces.

---

## Shape Radii

| Component | Radius token | dp value |
|---|---|---|
| Cards (mandate row, detail card, review card, headroom card) | rounded.medium | 12dp |
| Buttons (filled, text) | rounded.full | pill |
| Bottom sheet (pay sheet) | rounded.extra_large top corners only | 28dp |
| Text fields | rounded.small | 8dp |
| Chips (health chip, status chip) | rounded.full | pill |
| Dialogs (revoke confirm) | rounded.extra_large | 28dp |

No 0dp corners. No decorative shape variation.

---

## Interaction States

All interactive surfaces implement Material 3 state layer overlays (hover 8%, pressed 12%, focused 12%, dragged 16%) on the component's content colour.

- **Pay now / Authorise mandate buttons:** on tap, disable and show CircularProgressIndicator (size=18dp, strokeWidth=2dp, color=onPrimary) inside the button. Prevents double-submission.
- **Revoke button:** text button, error colour text. Tap opens the confirmation dialog — no inline loading state.
- **Mandate rows:** ripple on tap (primary at 8% opacity). Navigate to detail.
- **Account selection (Step 1):** selected row shows filled RadioButton (primary). Row taps update the selection immediately.

---

## Figma File Structure (recommended)

```
Page: pay-vrp-mandate
├── Frame: Screen / Mandate List — loading
├── Frame: Screen / Mandate List — content (2 mandates: active + revoked)
├── Frame: Screen / Mandate List — empty
├── Frame: Screen / Create — Step 1 Account
├── Frame: Screen / Create — Step 2 Payee
├── Frame: Screen / Create — Step 3 Limits
├── Frame: Screen / Create — Step 4 Review
├── Frame: Screen / Detail — active (Pay now visible)
├── Frame: Screen / Detail — paying (amount sheet open)
├── Frame: Screen / Detail — settling
├── Frame: Screen / Detail — failing (banner + no Pay now)
├── Frame: Screen / Detail — unpayable (error banner + no Pay now)
├── Frame: Screen / Detail — revoked (info banner)
├── Frame: Screen / Detail — revoking (dialog open)
└── Components
     ├── MandateHealthChip / active
     ├── MandateHealthChip / failing
     ├── MandateHealthChip / unpayable
     ├── MandateHealthChip / revoked
     ├── MandateRow / active
     ├── MandateRow / failing
     ├── MandateRow / unpayable
     ├── MandateRow / revoked
     └── HeadroomBar
```
