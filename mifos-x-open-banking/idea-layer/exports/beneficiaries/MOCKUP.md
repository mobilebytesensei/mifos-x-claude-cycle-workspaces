# MOCKUP — Beneficiaries

**Archetype:** index_list
**Shell:** Top app bar ("Beneficiaries") with back arrow and filter_list action. No bottom navigation bar.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Beneficiaries              [≡]   │  ← M3 TopAppBar: arrow_back + filter_list icon
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 🔍  Search beneficiaries...    ││  ← search input, radius 28, #F9FAEF bg
│  └─────────────────────────────────┘│
│                                     │
│  ████████████████                   │  ← "Recently Used" header skeleton (#E1E4D5, 12dp radius)
│                                     │
│  ┌─────────────────────────────────┐│
│  │  (●)  ████████████████████████  ││  ← avatar circle skeleton (44dp) + name skeleton
│  │       ████████████  ██████████  ││  ← bank name + last payment skeletons
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  (●)  ████████████████████████  ││
│  │       ████████████  ██████████  ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  (●)  ████████████████████████  ││
│  │       ████████████              ││
│  └─────────────────────────────────┘│
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │  ← divider skeleton
│  ████████████████████               │  ← "All Beneficiaries" header skeleton
│  ┌─────────────────────────────────┐│
│  │  [□]  ████████████████████████  ││  ← bank logo skeleton (32×32dp) + name
│  │       ████████████  ██████████  ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  [□]  ████████████████████████  ││
│  │       ████████████  ██████████  ││
│  └─────────────────────────────────┘│
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** 6-item skeleton list, short4 shimmer (200ms). Avatar circles 44dp; bank logo placeholders 32×32dp. FAB hidden during loading. Skeleton color: surface_variant (#E1E4D5), 12dp radius.

---

## Screen: content

```
┌─────────────────────────────────────┐
│ ←  Beneficiaries              [≡]   │  ← filter_list icon → sort_beneficiaries
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 🔍  Search beneficiaries...    ││  ← search, radius 28, leading search icon
│  └─────────────────────────────────┘│
│                                     │
│  Recently Used                      │  ← title_medium (16sp/500), #1A1C16, semibold
│                                     │
│  ┌─────────────────────────────────┐│  ← white card, radius 12, elevation 1, 14dp vert pad
│  │  (JS)  John Smith               ││  ← 44dp circle, #4C662B bg, #FFFFFF "JS", title_medium/bold
│  │        Barclays UK              ││  ← body_small (12sp/400), #44483D
│  │        £500 · 2 days ago        ││  ← body_small, #386663
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │  (SW)  Sarah Williams           ││  ← 44dp circle, #386663 bg, #FFFFFF "SW"
│  │        HSBC UK                  ││  ← body_small, #44483D
│  │        £1,200 · 5 days ago      ││  ← body_small, #386663
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │  (MC)  Michael Chen             ││  ← 44dp circle, #4C662B bg, #FFFFFF "MC"
│  │        Lloyds Bank              ││  ← body_small, #44483D
│  └─────────────────────────────────┘│
│                                     │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │  ← divider #E1E4D5, 1px, 8dp vert padding
│                                     │
│  All Beneficiaries          [sort↕] │  ← title_medium + sort icon 24dp #4C662B, space-between
│                                     │
│  ┌─────────────────────────────────┐│
│  │  [NW]  James Anderson           ││  ← NatWest logo 32×32dp, radius 4, content_scale fit
│  │        GB29 NWBK ··· 8819       ││  ← body_small, #44483D, monospace
│  │        Last: 12 May 2026        ││  ← body_small, #44483D
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │  [S]   Priya Patel              ││  ← Santander logo 32×32dp
│  │        GB72 ABBY ··· 4421       ││  ← body_small, #44483D, monospace
│  └─────────────────────────────────┘│
│                                     │
│                   [+ Add Beneficiary]│  ← FAB: #4C662B fill, radius 16, elevation 6
│                                     │     person_add icon, bottom-right, 16dp margin
└─────────────────────────────────────┘
```

**Layout notes:**
- Search bar: 28dp radius (pill), 16dp horizontal margin, #F9FAEF background, leading search icon + trailing clear icon.
- Avatar circles: 44dp diameter, initials in title_medium/bold/#FFFFFF. JS + MC: #4C662B bg. SW: #386663 bg.
- Beneficiary cards: #FFFFFF fill, 12dp radius, 1dp elevation, 14dp vertical padding, 16dp horizontal padding.
- Last-payment text tinted with secondary (#386663); bank names + dates use on_surface_variant (#44483D).
- Section divider: #E1E4D5, 1px, 8dp vertical padding.
- "All Beneficiaries" header row: space-between alignment with sort icon 24dp in #4C662B.
- Bank logos: 32×32dp, 4dp radius, content_scale fit.
- IBAN/account text: body_small, #44483D, monospace font-family.
- FAB: 56dp, #4C662B fill, 16dp radius, elevation 6, person_add icon, "Add Beneficiary" label, floating bottom-right with 16dp margin.

---

## Screen: searching

```
┌─────────────────────────────────────┐
│ ←  Beneficiaries              [≡]   │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 🔍  john                 [✕]   ││  ← search active: typed query, trailing clear (X)
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│  ← filtered result card
│  │  (JS)  John Smith               ││
│  │        Barclays UK              ││
│  │        £500 · 2 days ago        ││
│  └─────────────────────────────────┘│
│                                     │
│                   [+ Add Beneficiary]│
└─────────────────────────────────────┘
```

**Layout notes:** Filtered results shown without section headers ("Recently Used" / "All Beneficiaries"). Trailing clear icon (✕) appears while text is entered. Results span both recent and all-beneficiaries sources.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│ ←  Beneficiaries              [≡]   │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 🔍  Search beneficiaries...    ││
│  └─────────────────────────────────┘│
│                                     │
│                                     │
│       person_off (48dp, #44483D)    │  ← empty icon, centered
│                                     │
│       No beneficiaries yet          │  ← body_large (16sp/400), #1A1C16, centered
│                                     │
│  Add a beneficiary to start         │
│     sending money quickly           │  ← body_medium (14sp/400), #44483D, centered
│                                     │
│                                     │
│                   [+ Add Beneficiary]│
└─────────────────────────────────────┘
```

**Layout notes:** Empty state icon + title + message centred vertically in the content area. FAB remains always visible as primary action anchor.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Beneficiaries              [≡]   │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 🔍  Search beneficiaries...    ││
│  └─────────────────────────────────┘│
│                                     │
│         cloud_off (48dp, #44483D)   │  ← error icon, centered
│                                     │
│    Unable to load beneficiaries     │  ← body_large (16sp/400), #1A1C16, centered
│    Check your connection            │
│         and try again               │  ← body_medium (14sp/400), #44483D, centered
│                                     │
│          [   Try Again   ]          │  ← filled button, #4C662B bg, centered
│                                     │
│                   [+ Add Beneficiary]│
└─────────────────────────────────────┘
```

**Layout notes:** Error icon + message + retry button centred. Error icon uses on_surface_variant (#44483D) for WCAG AA contrast. FAB remains visible.

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar with back arrow (navigation_icon: arrow_back) and filter_list action icon
- [ ] Search input: 28dp radius (pill), leading search icon, trailing clear icon (appears on input), #F9FAEF background
- [ ] "Recently Used" section: title_medium (16sp/500) / #1A1C16 / semibold / 16dp top padding
- [ ] Avatar circles 44dp: JS + MC use #4C662B bg; SW uses #386663 bg; all initials #FFFFFF title_medium/bold
- [ ] Beneficiary cards: #FFFFFF fill, 12dp radius, 1dp elevation, 14dp vertical padding, 16dp horizontal padding
- [ ] Last payment line tinted #386663 (secondary); bank name uses #44483D (on_surface_variant)
- [ ] Section divider: #E1E4D5 (surface_variant), 1px, 8dp vertical padding
- [ ] "All Beneficiaries" row: space-between with sort icon 24dp / #4C662B
- [ ] Bank logos: 32×32dp, 4dp radius, content_scale fit
- [ ] IBAN / account routing text: body_small (12sp), #44483D, monospace font-family
- [ ] FAB: #4C662B fill, 16dp radius (radius.lg), elevation 6, person_add icon, "Add Beneficiary" label, floating bottom-right, 16dp margin
- [ ] Loading skeleton: 6 items, short4 shimmer (200ms), #E1E4D5 skeleton blocks, 12dp radius
- [ ] Empty state: person_off 48dp / #44483D icon centred; body_large title; body_medium description
- [ ] Error state: cloud_off 48dp / #44483D icon centred; body_large message; filled retry button #4C662B
- [ ] Searching state: trailing clear (✕) active; section headers suppressed; results from both sources
- [ ] All text: Outfit typeface. Minimum touch target 48dp. 16dp horizontal content padding throughout.
- [ ] No bottom navigation bar (bottom_nav: false)

---

_Generated by /idea export | 2026-05-30_
