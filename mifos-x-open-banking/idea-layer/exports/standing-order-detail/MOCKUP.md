# MOCKUP — Standing Order Detail

**Archetype:** detail_screen
**Shell:** Top app bar ("Standing Order") with back arrow and edit icon. No bottom navigation bar.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: content (Standing order loaded)

```
┌─────────────────────────────────────┐
│ ←  Standing Order            ✎      │  ← TopAppBar, #F9FAEF, edit icon top-right
├─────────────────────────────────────┤
│                                     │
│ ┌─────────────────────────────────┐ │
│ │  Rent Payment                   │ │  ← headline_medium #FFFFFF, weight 600
│ │  [Active]                       │ │  ← badge: #CDEDA3 bg, #4C662B text, radius 20
│ └─────────────────────────────────┘ │  ← sod_header_card: #4C662B full-width
│                                     │
│   ┌─────────────────────────────┐   │  ← sod_beneficiary_card: overlaps header (margin_top -24)
│   │  RECIPIENT                  │   │     white, radius 16, elevation 4
│   │  Name      Landlord         │   │
│   │            Holdings Ltd     │   │  ← body_medium #1A1C16, weight 500
│   │  IBAN      GB29 NWBK 6016   │   │  ← monospace body_small #1A1C16
│   │            1331 9268 19     │   │
│   │  Bank      NatWest Bank     │   │  ← body_medium #1A1C16, weight 500
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │  ← sod_schedule_card: white, radius 16, elevation 1
│   │  SCHEDULE                   │   │  ← label_small #44483D uppercase
│   │  Frequency    Monthly       │   │
│   │  Start Date   1 Jan 2026    │   │
│   │  Next Payment 1 Jun 2026    │   │  ← next payment: #4C662B, weight 600 (highlighted)
│   │  Final Date   31 Dec 2026   │   │
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │  ← sod_amount_card: white, radius 16, elevation 1
│   │  PAYMENT AMOUNT             │   │
│   │  £1,200.00  [GBP]           │   │  ← display_small #1A1C16 w700 + currency badge #F9FAEF
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │  ← sod_history_card
│   │  RECENT EXECUTIONS          │   │
│   │  1 May 2026  Completed  £1,200  │  ← status #4C662B, amount right-aligned w600
│   │  ─────────────────────────  │   │
│   │  1 Apr 2026  Completed  £1,200  │
│   │  ─────────────────────────  │   │
│   │  1 Mar 2026  Completed  £1,200  │
│   │  ─────────────────────────  │   │
│   │  1 Feb 2026  Failed     £1,200  │  ← status #BA1A1A, amount #BA1A1A (error color)
│   │             Insufficient Funds  │
│   │  ─────────────────────────  │   │
│   │  1 Jan 2026  Completed  £1,200  │
│   └─────────────────────────────┘   │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ ⏸  Pause Standing Order         │ │  ← outlined button, #4C662B border/text, radius 12
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 🗑  Cancel Standing Order        │ │  ← outlined button, #BA1A1A border/text, radius 12
│ └─────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:**
- #F9FAEF background.
- sod_header_card: full-width flush (0dp radius), #4C662B, 24dp horizontal padding, 32dp bottom padding.
- sod_beneficiary_card overlaps header by 24dp (negative margin_top) creating a layered card effect; elevation 4dp to float above header.
- Three detail cards (schedule, amount, history): white, radius 16dp, elevation 1dp, margin_horizontal 24dp, 16dp gap between.
- History items: two-line list items — date (body_medium #1A1C16, w500) + status text (body_small; #4C662B for Completed, #BA1A1A for Failed) + amount right-aligned (body_medium, w600; same color as status on failure).
- Pause + Cancel buttons: full-width outlined, 14dp vertical padding, leading icons.
- Bottom spacer 24dp before safe area.

---

## Screen: loading (API call in flight)

```
┌─────────────────────────────────────┐
│ ←  Standing Order            ✎      │
├─────────────────────────────────────┤
│                                     │
│ ███████████████████████████████████ │  ← header shimmer (full-width green block)
│                                     │
│   ┌─────────────────────────────┐   │
│   │  ██████████████████████████ │   │  ← beneficiary card shimmer rows
│   │  ██████████████████████████ │   │
│   │  ██████████████████████████ │   │
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │  ████████  ████████████████ │   │  ← schedule card shimmer
│   │  ████████  ████████████████ │   │
│   │  ████████  ████████████████ │   │
│   │  ████████  ████████████████ │   │
│   └─────────────────────────────┘   │
│                                     │
│   ┌─────────────────────────────┐   │
│   │  ████████████████  [████]   │   │  ← amount shimmer
│   └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Full-screen shimmer matching content block structure. Shimmer base #F0F1E6 → #E1E4D5 animation (trust_horizon gradient used as shimmer base).

---

## Screen: error (API 404 / network failure)

```
┌─────────────────────────────────────┐
│ ←  Standing Order            ✎      │
├─────────────────────────────────────┤
│                                     │
│                                     │
│              sync_problem           │  ← icon 48dp, #BA1A1A, centered
│                                     │
│      Standing Order Not Found       │  ← title_medium #1A1C16, centered
│   We could not load this standing   │  ← body_medium #44483D, centered
│   order. It may have been cancelled │
│   or there may be a connection      │
│   issue.                            │
│                                     │
│  ┌────────────────────────────────┐ │
│  │            Retry               │ │  ← outlined button, #4C662B
│  └────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

---

## Screen: empty (API 200 — null/empty body)

```
┌─────────────────────────────────────┐
│ ←  Standing Order            ✎      │
├─────────────────────────────────────┤
│                                     │
│                                     │
│              repeat_off             │  ← icon 48dp, #C5C8BA, centered
│                                     │
│   No details are available for      │  ← body_medium #44483D, centered
│   this standing order.              │
│                                     │
│  ┌────────────────────────────────┐ │
│  │    Back to Standing Orders     │ │  ← outlined button, #4C662B
│  └────────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar: back arrow + "Standing Order" title + edit icon action
- [ ] sod_header_card: full-width #4C662B, 0dp radius, 32dp bottom padding
- [ ] sod_status_badge: #CDEDA3 bg, #4C662B text, 20dp radius pill
- [ ] sod_beneficiary_card: white, radius 16dp, elevation 4dp, negative margin overlapping header by 24dp
- [ ] Section headers: Outfit label_small (11sp/500) uppercase, #44483D, letter-spacing 0.8
- [ ] next_payment_value: #4C662B green, weight 600 (visual emphasis)
- [ ] sod_amount_value: display_small (32sp/SemiBold), #1A1C16; sod_currency_badge: #F9FAEF bg
- [ ] History items: two-line — Completed status #4C662B; Failed status and amount #BA1A1A
- [ ] Pause button: outlined #4C662B, pause_circle leading icon; toggles to "Resume" when status=PAUSED
- [ ] Cancel button: outlined #BA1A1A, delete_outline leading icon
- [ ] Alert dialog: radius 28dp, "Cancel Order" button filled #BA1A1A
- [ ] Loading: shimmer blocks matching all detail card shapes
- [ ] Error: sync_problem 48dp #BA1A1A + centered text + Retry outlined button
- [ ] Empty: repeat_off 48dp #C5C8BA + centered text + Back button
- [ ] All text Outfit typeface
- [ ] 16 dp horizontal padding in cards; 24 dp screen margin
