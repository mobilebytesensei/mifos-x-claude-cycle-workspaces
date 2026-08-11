# Design System Overview — mifos-x-group-banking (MifosSave)

## Profile: Outdoor WCAG

Higher contrast ratios than standard WCAG AA. Designed for bright sunlight + low-cost screens in rural Kenya.

- Touch targets: minimum 48dp (rural UX — field workers with rough hands)
- Font: Noto Sans — multilingual, supports Swahili + local scripts
- Contrast ratio: ≥5.5:1 (exceeds WCAG AA 4.5:1)
- Offline-first: all primary flows work without connectivity

## Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | Primary actions, FAB, active nav |
| secondary | #FF8F00 | Warnings, savings highlights, share-out |
| tertiary | #1565C0 | Loans, info states |
| surface | #FAFAFA | Card backgrounds |
| on-primary | #FFFFFF | Text on primary |
| error | #B00020 | Errors, defaulted loans |
| success | #1B5E20 | Paid loans, confirmed meetings |

## Typography Scale

- Headline: Noto Sans Bold 24sp (screen titles)
- Title: Noto Sans SemiBold 18sp (section headers, card titles)
- Body: Noto Sans Regular 16sp (content — larger than standard for outdoor)
- Label: Noto Sans Medium 14sp (chips, badges)
- Caption: Noto Sans Regular 12sp (secondary info)

## Spacing Rhythm

Base unit: 4dp. Primary grid: 8dp. Section spacing: 24dp. Page padding: 16dp.

## Elevation & Shadows

- Cards: 2dp elevation (subtle — saves battery on AMOLED)
- Dialogs: 8dp elevation
- Bottom sheet: 16dp elevation
- FAB: 6dp elevation

## Component Design Principles

1. **Single-handed operation** — key actions reachable with thumb in bottom 40% of screen
2. **Large data ink** — numbers (KES amounts) in 20sp+ for at-a-glance outdoor reading
3. **Status always visible** — loan status, attendance status never hidden in overflow
4. **Confirmations before destructive actions** — share-out, loan approval, mark-defaulted always show confirmation dialog
5. **Offline badge** — persistent offline indicator in app bar when connectivity lost
