# MOCKUP — Direct Debit Detail

**Archetype:** detail_screen
**Shell:** Top app bar ("Direct Debit", back arrow, more_vert overflow). No bottom navigation — consumer detail screen.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: content (Primary)

```
┌─────────────────────────────────────┐
│ ←  Direct Debit              ⋮      │  ← Top app bar #F9FAEF, more_vert
├─────────────────────────────────────┤
│                                     │  ← #F9FAEF background, pad 24dp
│  ┌──────────────────────────────┐   │  ← Merchant hero #4C662B bg, radius-bottom 24dp
│  │                              │   │    pad H24/T32/B36
│  │    ┌───────┐                 │   │
│  │    │ NFLX  │                 │   │    56×56dp logo #FFFFFF bg, radius 12
│  │    └───────┘                 │   │
│  │    Netflix Entertainment     │   │    headline_small #FFFFFF centered
│  │      [  Active  ]            │   │    badge: #CDEDA3 bg #4C662B text, radius 20
│  │                              │   │
│  │          £15.99              │   │    display_small #FFFFFF bold centered
│  │          Monthly             │   │    body_medium #CDEDA3 centered
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │  ← Mandate Details card #FFFFFF, radius 12
│  │  Mandate Details             │   │    title_medium #4C662B
│  │  ──────────────────────────  │
│  │  Next Payment    15 Jun 2026 │   │    body_medium; label=#44483D value=#1A1C16 bold
│  │  ──────────────────────────  │
│  │  Account         Current     │   │    account name bold; number #44483D body_small
│  │                  ****4521    │
│  │  ──────────────────────────  │
│  │  Mandate Ref  MDT-2024-00947 │   │    monospace
│  │  ──────────────────────────  │
│  │  Start Date      12 Jan 2024 │   │    body_medium bold
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │  ← Recent Payments card #FFFFFF, radius 12
│  │  Recent Payments   View all  │   │    title_medium #4C662B + label_medium #386663 link
│  │  ──────────────────────────  │
│  │  15 May 2026              −£15.99│   body_medium #1A1C16 bold; right-aligned
│  │  Collected                   │   │    body_small #4C662B
│  │  ──────────────────────────  │
│  │  15 Apr 2026              −£15.99│
│  │  Collected                   │   │    #4C662B
│  │  ──────────────────────────  │
│  │  15 Mar 2026              −£15.99│   #BA1A1A (failed — error color)
│  │  Failed                      │   │    body_small #BA1A1A
│  └──────────────────────────────┘   │
│                                     │
│  [Cancel Mandate] [  Edit Mandate ] │  ← Cancel: outlined #BA1A1A, radius 12
│                                     │    Edit: filled #386663, radius 12
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:**
- Screen root: #F9FAEF, pad 24dp column.
- Merchant hero: #4C662B bg, radius only bottom-left/right 24dp, no top radius. Logo centered, name centered, badge centered, amount centered, frequency below amount.
- Status badge: #CDEDA3 bg (primary_container), #4C662B text. Paused = #FFF3CD. Cancelled = #FFDAD6.
- Cards: #FFFFFF bg, radius 12dp, pad 16dp, margin B16.
- Detail rows: horizontal space-between, pad V8; dividers #E1E4D5 between rows, margin V4.
- Payment history items: date column left (body_medium date + body_small status) + amount right (body_medium bold). Collected=green, Failed=red.
- Action row: space-between, top pad 16dp, horizontal gap 16dp.
- Cancel: outlined error #BA1A1A, half-width, radius 12. Edit: filled #386663, half-width, radius 12.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Direct Debit              ⋮      │
├─────────────────────────────────────┤
│                                     │
│  ████████████████████████████████   │  ← Hero skeleton (tall, radius-bottom 24)
│  ████████████████████████████████   │
│  ████████████████████████████████   │
│                                     │
│  ┌──────────────────────────────┐   │  ← Card skeleton
│  │  ████████████████████████   │   │    shimmer on #F0F1E6 base
│  │  ████████████  ████████████ │   │
│  │  ████████████  ████████████ │   │
│  │  ████████████  ████████████ │   │
│  │  ████████████  ████████████ │   │
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │
│  │  ████████████  ████████████ │   │
│  │  ████████████  ████████████ │   │
│  │  ████████████  ████████████ │   │
│  └──────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Hero placeholder same height as content hero. Card skeletons match Mandate Details + Payment History proportions. No action buttons during loading.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Direct Debit              ⋮      │
├─────────────────────────────────────┤
│                                     │
│                                     │
│              ⚠                      │  ← error_outline icon, 48dp, #BA1A1A, centered
│                                     │
│  Couldn't load mandate details.     │  ← body_medium #44483D, centered
│  Please try again.                  │
│                                     │
│       [      Try Again      ]       │  ← Filled #4C662B, radius 12, pad H32
│                                     │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Icon + text + button vertically centered. Button width auto (content), centered horizontally.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│ ←  Direct Debit              ⋮      │
├─────────────────────────────────────┤
│                                     │
│           📅                        │  ← event_busy icon 48dp, #44483D
│                                     │
│    Mandate details not available    │  ← title_medium #1A1C16, centered
│                                     │
│  This direct debit mandate could    │  ← body_medium #44483D centered
│  not be found. It may have already  │
│  been cancelled or expired.         │
│                                     │
│  [ Back to Direct Debits ]          │  ← Outlined #4C662B pill, centered
│                                     │
└─────────────────────────────────────┘
```

---

## Design Checklist (Figma / Stitch)

- [ ] Top app bar: back arrow left, "Direct Debit" title, more_vert overflow action
- [ ] Merchant hero: #4C662B fill, radius ONLY bottom-left + bottom-right 24dp, pad H24/T32/B36
- [ ] Merchant logo: 56×56dp, radius 12dp, #FFFFFF bg, centered; initials fallback on error
- [ ] Status badge: #CDEDA3 bg / #4C662B text; Paused=#FFF3CD; Cancelled=#FFDAD6; radius 20dp
- [ ] Mandate amount: Outfit display_small #FFFFFF bold, centered
- [ ] Frequency text: Outfit body_medium #CDEDA3, centered (using primary_container on dark bg)
- [ ] Mandate Details card: white, radius 12, pad 16; rows space-between, dividers #E1E4D5
- [ ] Mandate ref value: monospace font family
- [ ] Recent Payments: Collected status=#4C662B; Failed status+amount=#BA1A1A
- [ ] "View all" link: label_medium #386663 (secondary color)
- [ ] Cancel Mandate: outlined #BA1A1A border+text, radius 12
- [ ] Edit Mandate: filled #386663 bg #FFFFFF text, radius 12
- [ ] Loading: shimmer hero + card skeletons; shimmer base #F0F1E6
- [ ] Error: error_outline 48dp #BA1A1A + centered text + filled green Try Again btn
- [ ] All text Outfit typeface; 24dp screen padding
