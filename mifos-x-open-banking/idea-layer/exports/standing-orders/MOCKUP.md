# MOCKUP — Standing Orders

**Archetype:** index_list
**Shell:** Top app bar ("Standing Orders", `arrow_back`, `filter_list` action). No bottom navigation bar.
**Accent:** #4C662B (Earth-green primary). Typography: Outfit. Design system: Material Design 3.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Standing Orders        [filter]  │  ← TopAppBar · title_large #1A1C16 · bg #F9FAEF
├─────────────────────────────────────┤
│                                     │
│  Standing Orders                    │  ← headline_large (32sp/400), #4C662B
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ████████████████████████████ │  │  ← Skeleton card 1 · #E1E4D5 · radius 16dp
│  │  ██████████████  ████████████ │  │    shimmer short4 (200ms)
│  │  █████████████████████  █████ │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  ████████████████████████████ │  │  ← Skeleton card 2
│  │  ██████████████  ████████████ │  │
│  │  █████████████████████  █████ │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  ████████████████████████████ │  │  ← Skeleton card 3
│  │  ██████████████  ████████████ │  │
│  │  █████████████████████  █████ │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Skeleton cards (#E1E4D5, radius 16dp, ~100dp tall each) shimmer at `motion.duration.short4` (200ms). Screen title "Standing Orders" remains visible. No active count chip and no FAB shown during loading. `show_skeleton_list: true`, `skeleton_count: 3` per ui.yaml states.loading.

---

## Screen: content

```
┌─────────────────────────────────────┐
│ ←  Standing Orders        [filter]  │  ← TopAppBar
├─────────────────────────────────────┤
│                                     │
│  Standing Orders  ┌──────────┐      │  ← headline_large, #4C662B
│                   │ 3 active │      │  ← chip: bg #CDEDA3 · text #4C662B
│                   └──────────┘      │    radius 12dp · 10dp H-pad · label_medium SemiBold
│  ┌───────────────────────────────┐  │
│  │  Rent Payment        [Active] │  │  ← title_medium SemiBold #1A1C16 │ badge #CDEDA3/#4C662B
│  │  To: Landlord Holdings Ltd    │  │  ← body_medium #44483D · padding_bottom 4dp
│  │  £1,200 / month  Next: 1 Jun  │  │  ← body_large SemiBold #4C662B │ body_small #44483D
│  │                    [✎]  [🗑]  │  │  ← edit_outlined 22dp #4C662B │ delete_outlined 22dp #BA1A1A
│  └───────────────────────────────┘  │    card: #FFFFFF · radius 16dp · elevation 2 · border #F9FAEF
│  ┌───────────────────────────────┐  │
│  │  Netflix Subscription [Active]│  │  ← same elevated white variant
│  │  £15.99 / month  Next: 7 Jun  │  │
│  │                    [✎]  [🗑]  │  │
│  └───────────────────────────────┘  │
│  ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┐  │
│  │  Gym Membership    [Paused]   │  │  ← outlined muted variant
│  │  £45.00 / month               │  │    bg #F9FAEF · border #E1E4D5 1dp · radius 16dp
│  │  Next: 15 Jun 2026 (Paused)   │  │    all text #44483D (muted)
│  │                    [✎]  [🗑]  │  │    badge: #F9FAEF/#44483D
│  └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─┘  │
│                                     │
│                       ┌──────────────────────────┐
│                       │ + Create Standing Order  │  ← Extended FAB
│                       └──────────────────────────┘    bg #4C662B · text #FFFFFF · radius 16dp · elevation 6
└─────────────────────────────────────┘
```

**Layout notes:**
- Title row (`title_count_row`): "Standing Orders" headline_large (#4C662B) + "3 active" chip (#CDEDA3 bg, #4C662B text, radius 12, 10dp H-pad, 4dp V-pad); horizontally arranged, aligned center, padding_bottom 16dp.
- Active cards (#FFFFFF, radius 16dp, elevation 2, border #F9FAEF 1dp, 16dp internal padding, 16dp margin_bottom): order name title_medium SemiBold #1A1C16 + "Active" badge (#CDEDA3/#4C662B, radius 10dp, 8dp H-pad, 3dp V-pad, label_small).
- Beneficiary text body_medium #44483D. Amount body_large SemiBold #4C662B. Next date body_small #44483D.
- Action icons at flex_end row (spacing 8dp, padding_top 16dp): `edit_outlined` 22dp #4C662B, `delete_outlined` 22dp #BA1A1A, each 8dp padding, 48dp minimum touch target.
- Paused card (#F9FAEF fill, #E1E4D5 1dp border, radius 16dp, elevation 1): all text muted #44483D; "Paused" badge (#F9FAEF/#44483D).
- Extended FAB: #4C662B fill, #FFFFFF text "Create Standing Order", `add` icon, radius 16dp, elevation 6; floating bottom-right.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│ ←  Standing Orders        [filter]  │  ← TopAppBar
├─────────────────────────────────────┤
│                                     │
│  Standing Orders                    │  ← headline_large, #4C662B (no count chip)
│                                     │
│                                     │
│          ┌──────────────────┐       │
│          │   [repeat_off]   │       │  ← Material icon, 48dp, #44483D
│          └──────────────────┘       │
│                                     │
│        No standing orders           │  ← title_medium, #1A1C16, center-aligned
│                                     │
│   Set up recurring payments to      │  ← body_medium, #44483D, center-aligned
│   automate your regular bills       │
│                                     │
│                       ┌──────────────────────────┐
│                       │ + Create Standing Order  │  ← Extended FAB
│                       └──────────────────────────┘
└─────────────────────────────────────┘
```

**Layout notes:** Empty state centered below title. `repeat_off` icon 48dp #44483D. Empty title in title_medium #1A1C16; body in body_medium #44483D; both center-aligned. No count chip visible (`active_count_chip_visible: false`). FAB persists to drive first order creation.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Standing Orders        [filter]  │  ← TopAppBar
├─────────────────────────────────────┤
│                                     │
│  Standing Orders                    │  ← headline_large, #4C662B (no count chip)
│                                     │
│                                     │
│          ┌──────────────────┐       │
│          │   [cloud_off]    │       │  ← Material icon, 48dp, #BA1A1A (error color)
│          └──────────────────┘       │
│                                     │
│   Unable to load standing orders    │  ← title_medium, #1A1C16, center-aligned
│                                     │
│   Check your connection and try     │  ← body_medium, #44483D, center-aligned
│   again                             │
│                                     │
│          ┌─────────────┐            │
│          │    Retry    │            │  ← OutlinedButton · #4C662B border + text · pill radius
│          └─────────────┘            │
│                                     │
│                       ┌──────────────────────────┐
│                       │ + Create Standing Order  │  ← Extended FAB persists
│                       └──────────────────────────┘
└─────────────────────────────────────┘
```

**Layout notes:** `cloud_off` icon 48dp #BA1A1A. Error title in title_medium #1A1C16; body in body_medium #44483D. Retry is OutlinedButton (#4C662B text + border, pill radius 999dp, 40dp height). No count chip (`active_count_chip_visible: false`). FAB persists — user can attempt order creation while error is displayed.

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar — `arrow_back` navigation icon + `filter_list` icon action; title "Standing Orders" title_large #1A1C16; bg `#F9FAEF`
- [ ] Screen-level title "Standing Orders" — Outfit headline_large (32sp/400), `#4C662B`
- [ ] Active count chip "3 active" — `#CDEDA3` fill, radius 12dp, 10dp H-pad, 4dp V-pad, `#4C662B` text, Outfit label_medium SemiBold
- [ ] Active order cards — `#FFFFFF` fill, radius 16dp, elevation 2 (3dp shadow), `#F9FAEF` border 1dp, 16dp internal padding
- [ ] Active badge "Active" — `#CDEDA3` fill, `#4C662B` text, radius 10dp, 8dp H-pad, 3dp V-pad, Outfit label_small
- [ ] Order name — Outfit title_medium (16sp/500) SemiBold, `#1A1C16` (active) / `#44483D` (paused)
- [ ] Beneficiary "To: [name]" — Outfit body_medium (14sp/400), `#44483D`
- [ ] Amount + frequency — Outfit body_large (16sp/400) SemiBold, `#4C662B` (active) / `#44483D` (paused)
- [ ] Next payment date — Outfit body_small (12sp/400), `#44483D`
- [ ] Edit icon `edit_outlined` 22dp `#4C662B` per card; minimum 48dp touch target
- [ ] Delete icon `delete_outlined` 22dp `#BA1A1A` per card; minimum 48dp touch target; triggers confirmation dialog
- [ ] Paused card — `#F9FAEF` fill, `#E1E4D5` border 1dp, radius 16dp, elevation 1; all text `#44483D`
- [ ] Paused badge "Paused" — `#F9FAEF` fill, `#44483D` text, radius 10dp
- [ ] Extended FAB — `#4C662B` fill, `#FFFFFF` text "Create Standing Order", `add` icon, radius 16dp, elevation 6; floating bottom-right
- [ ] Loading: 3 skeleton shimmer cards `#E1E4D5`, radius 16dp, shimmer 200ms (short4)
- [ ] Empty state: `repeat_off` icon 48dp `#44483D`, centered copy, FAB visible
- [ ] Error state: `cloud_off` icon 48dp `#BA1A1A`, centered copy, OutlinedButton retry, FAB visible
- [ ] 16dp horizontal content padding throughout; 16dp vertical gap between cards
- [ ] All typeface: Outfit. Touch targets ≥ 48dp. 8dp spacing between adjacent interactive elements.

---

_Generated by /idea export | 2026-05-30_
