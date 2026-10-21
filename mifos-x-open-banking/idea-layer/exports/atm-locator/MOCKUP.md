# MOCKUP — ATM & Branch Locator

**Archetype:** index_list
**Shell:** Bottom navigation bar (Home/Accounts/Pay/Cards/More — 80dp height, #F9FAEF background, #DCE7C8 active indicator). No top app bar — screen-level headline used instead.
**Accent:** #4C662B (Earth-green primary). Typography: Outfit. Design system: Material Design 3.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│                                     │
│  ATM & Branches                     │  ← headline_large (32sp/400), #4C662B
│                                     │     24dp top padding, 16dp h-padding
│  ┌─────────────────────────────────┐│
│  │ 🔍  Enter city, postcode...     ││  ← search input, pill radius 28dp
│  └─────────────────────────────────┘│     #F9FAEF bg, 16dp h-pad, 12dp v-pad
│                                     │     12dp top margin
│  ← [All▮] [ATMs] [Branches] [24/7] │  ← chips: 16dp h-pad, 8dp v-pad, 8dp spacing
│     #4C662B fill / #FFFFFF label    │     "All" chip selected by default
│                                     │
│  ┌─────────────────────────────────┐│
│  │  ████████████████████████████   ││  ← Map skeleton: 240dp, 12dp radius
│  │  ████████████████████████████   ││     #E1E4D5 shimmer (short4 = 200ms)
│  │  ████████████████████████████   ││     reduced-motion: static placeholder
│  └─────────────────────────────────┘│
│                                     │
│  ██████████████████████████         │  ← results header skeleton (#E1E4D5)
│                                     │
│  ┌─────────────────────────────────┐│
│  │  ████████████████████████████   ││  ← card skeleton 1 (72dp, 12dp radius)
│  │  ██████████████  ████████        ││     #E1E4D5 shimmer
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  ████████████████████████████   ││  ← card skeleton 2
│  │  ██████████████  ████████        ││
│  └─────────────────────────────────┘│
│  ┌─────────────────────────────────┐│
│  │  ████████████████████████████   ││  ← card skeleton 3
│  └─────────────────────────────────┘│
├─────────────────────────────────────┤
│  🏠    🏦    ↗    💳    ···         │  ← bottom nav 80dp, active indicator hidden
└─────────────────────────────────────┘
```

**Token annotations:**
- Shimmer base: `colors.light.surface_variant` #E1E4D5, `motion.duration.short4` 200ms
- Search bg: `colors.light.background` #F9FAEF
- Filter chips: no skeleton — remain interactive during loading

---

## Screen: location_denied

```
┌─────────────────────────────────────┐
│                                     │
│  ATM & Branches                     │  ← headline_large, #4C662B
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 🔍  Enter city, postcode...     ││  ← search input (#F9FAEF, 28dp radius)
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 📍 Use my location for          ││  ← banner: #DCE7C8 bg, 1dp #4C662B border
│  │    nearby ATMs          [Enable]││     8dp radius, 12dp pad, 16dp h-margin
│  └─────────────────────────────────┘│     "Enable": text-variant, #4C662B, label_medium
│                                     │     triggers request_location_permission
│  ← [All▮] [ATMs] [Branches] [24/7] │  ← filter chips still active
│                                     │
│         (map area hidden)           │
│                                     │
├─────────────────────────────────────┤
│  🏠    🏦    ↗    💳    ···         │
└─────────────────────────────────────┘
```

**Token annotations:**
- Banner bg: `colors.light.nav_active_indicator` #DCE7C8
- Banner border: `colors.light.primary` #4C662B, 1dp
- Banner radius: `radius.sm` 8dp
- "Enable" button: text variant, `colors.light.primary` #4C662B, `typography.label_medium` 12sp/500

---

## Screen: content

```
┌─────────────────────────────────────┐
│                                     │
│  ATM & Branches                     │  ← headline_large (32sp/400), #4C662B
│                                     │     24dp top, 16dp h-pad
│  ┌─────────────────────────────────┐│
│  │ 🔍  Enter city, postcode...     ││  ← #F9FAEF bg, pill radius 28dp, search icon
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │  ┌──────────────────────────┐   ││  ← Map tile: 240dp h, 12dp radius
│  │  │  MAP — 3 pins rendered   │   ││     16dp h-margin, #E1E4D5 placeholder
│  │  │  • KCB Westlands         │   ││     real geo: Nairobi lat -1.2674/lng 36.8069
│  │  │     • Equity CBD         │   ││     pins in #4C662B (ATMs) / #386663 (branches)
│  │  │           • Co-op Karen  │   ││
│  │  └──────────────────────────┘   ││
│  └─────────────────────────────────┘│
│                                     │
│  ← [All▮] [ATMs] [Branches] [24/7]→ │  ← horizontal scroll, 8dp gap, 16dp h-pad
│     ████ (#4C662B / #FFFFFF text)   │
│                                     │
│  3 ATMs found within 500m           │  ← title_medium (16sp/500), #1A1C16
│                                     │     8dp top, 4dp bottom, 16dp h-pad
│  ┌─────────────────────────────────┐│
│  │ Mifos ATM — Oxford Street        ││  ← title_small (14sp/500), #1A1C16, wt 600
│  │ 0.2km away                       ││  ← body_small (12sp/400), #44483D
│  │ Open 24/7         [Get Directions→]│ ← "Open 24/7": body_small #4C662B wt 500
│  │ £300 max withdrawal               ││  ← body_small, #44483D
│  └──────────────────────────────── ─┘│     card: #FFFFFF, 12dp radius, 2dp elev
│                                     │     16dp pad, 16dp h-margin, 8dp b-margin
│  ┌─────────────────────────────────┐│
│  │ Mifos ATM — Bond Street Station   ││ ← title_small, #1A1C16, wt 600
│  │ 0.5km away                       ││  ← body_small, #44483D
│  │ Open 24/7         [Get Directions→]│ ← "Open 24/7": #4C662B, wt 500
│  └─────────────────────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │ Mifos Branch — Mayfair            ││ ← title_small, #1A1C16, wt 600
│  │ 0.8km away                       ││  ← body_small, #44483D
│  │ Mon–Fri 9am–5pm   [Get Directions→]│ ← hours: body_small #44483D wt 500
│  │ Services: Cashier · FX · Safe Deposit│ ← body_small, #44483D
│  └─────────────────────────────────┘│
│  ─────────────────────────────────── │  ← divider: #E1E4D5, 16dp h-margin
│                                     │
├─────────────────────────────────────┤
│  🏠    🏦    ↗    💳    ···         │  ← 5 tabs, #80dp height, active indicator #DCE7C8
└─────────────────────────────────────┘
```

**Token annotations:**
- Map tile placeholder: `colors.light.surface_variant` #E1E4D5, `radius.md` 12dp
- Filter chip row selected: `colors.light.primary` #4C662B fill + `colors.light.on_primary` #FFFFFF text
- Filter chip row unselected: transparent fill + 1dp `colors.light.outline_variant` #C5C8BA border + `colors.light.on_surface` #1A1C16 text
- Results header: `typography.title_medium` (Outfit 16sp/500), `colors.light.on_surface` #1A1C16
- Result card surface: `colors.light.surface` #FFFFFF, `radius.md` 12dp, `elevation.level2` 3dp
- ATM name: `typography.title_small` (Outfit 14sp/500, weight 600), `colors.light.on_surface` #1A1C16
- Distance/limit/services: `typography.body_small` (Outfit 12sp/400), `colors.light.on_surface_variant` #44483D
- "Open 24/7": `typography.body_small`, `colors.light.primary` #4C662B, weight 500
- "Mon–Fri 9am–5pm": `typography.body_small`, `colors.light.on_surface_variant` **#44483D** — **a11y fix A11Y-002** (was #E8A317 at 2.17:1 contrast ratio, WCAG AA fail; corrected to #44483D at 8.91:1, WCAG AA pass)
- "Get Directions" link: `typography.label_medium` (Outfit 12sp/500), `colors.light.primary` #4C662B, trailing directions icon 20dp (`iconography.scale.icon-sm`)
- Divider: `colors.light.surface_variant` #E1E4D5
- Bottom nav: `component_tokens.bottom_nav.height` 80dp, active indicator `colors.light.nav_active_indicator` #DCE7C8

---

## Screen: empty

```
┌─────────────────────────────────────┐
│                                     │
│  ATM & Branches                     │  ← headline_large, #4C662B
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 🔍  Enter city, postcode...     ││  ← search active for new query
│  └─────────────────────────────────┘│
│                                     │
│  ← [All▮] [ATMs] [Branches] [24/7] │  ← chips visible (let user switch filter)
│                                     │
│                                     │
│           location_off              │  ← icon 48dp (`iconography.scale.icon-2xl`)
│                                     │     `colors.light.on_surface_variant` #44483D
│                                     │     vertically centred in remaining space
│   No ATMs or branches found         │
│          in this area               │  ← body_large (16sp/400), #1A1C16, centered
│                                     │
│                                     │
├─────────────────────────────────────┤
│  🏠    🏦    ↗    💳    ···         │
└─────────────────────────────────────┘
```

**Token annotations:**
- Empty icon: `iconography.scale.icon-2xl` 48dp, `colors.light.on_surface_variant` #44483D
- Empty message: `typography.body_lg` (Outfit 16sp/400), `colors.light.on_surface` #1A1C16, text-align center
- Map area and result cards: hidden

---

## Screen: error

```
┌─────────────────────────────────────┐
│                                     │
│  ATM & Branches                     │  ← headline_large, #4C662B
│                                     │
│  ┌─────────────────────────────────┐│
│  │ 🔍  Enter city, postcode...     ││  ← search still accessible
│  └─────────────────────────────────┘│
│                                     │
│                                     │
│          error_outline              │  ← icon 48dp, `colors.light.error` #BA1A1A
│                                     │
│   Unable to load ATMs.              │  ← title_medium, #1A1C16, centered
│   Check your connection             │  ← body_medium (14sp/400), #44483D, centered
│       and try again.                │
│                                     │
│         [ Try Again ]               │  ← filled button, #4C662B fill/#FFFFFF text
│                                     │     triggers RetryLoad event
│                                     │
├─────────────────────────────────────┤
│  🏠    🏦    ↗    💳    ···         │
└─────────────────────────────────────┘
```

**Token annotations:**
- Error icon: `iconography.scale.icon-2xl` 48dp, `colors.light.error` #BA1A1A
- Error heading: `typography.title_medium`, `colors.light.on_surface` #1A1C16
- Error body: `typography.body_md` (Outfit 14sp/400), `colors.light.on_surface_variant` #44483D
- Retry button: filled, `colors.light.primary` #4C662B fill, `colors.light.on_primary` #FFFFFF text, `component_tokens.button.height_default` 40dp
- Map area, filter chips, result cards: all hidden

---

## Design Checklist (Figma / Stitch)

- [ ] Screen title "ATM & Branches" — headline_large (Outfit 32sp/400), #4C662B, 24dp top padding, 16dp h-padding
- [ ] Search input — pill radius 28dp, leading search icon (icon-md 24dp), placeholder "Enter city, postcode or address…", #F9FAEF background, 16dp h-padding, 12dp v-padding, 12dp top margin
- [ ] Location permission banner — #DCE7C8 fill, 1dp #4C662B border, 8dp radius, 12dp padding, 16dp h-margin, row layout with "Enable" text button right-aligned; visible only in location_denied state
- [ ] "Enable" button — text variant, #4C662B, label_medium (12sp/500), 8dp h-padding; triggers permission request
- [ ] Map tile — 240dp height, 12dp radius, 16dp h-margin; #E1E4D5 placeholder; ATM pins #4C662B, branch pins #386663; hidden in location_denied + error states
- [ ] Filter chips row — horizontal scroll, 8dp item gap, 16dp left padding, 12dp vertical padding; selected chip #4C662B fill/#FFFFFF text; unselected: #F9FAEF fill, 1dp #C5C8BA border, #1A1C16 text
- [ ] Results count header — title_medium (Outfit 16sp/500), #1A1C16, 16dp h-pad, 8dp top, 4dp bottom; updates on filter change
- [ ] Result cards — #FFFFFF fill, 12dp radius, 2dp elevation, 16dp padding, 16dp h-margin, 8dp bottom margin between cards
- [ ] ATM/branch name — title_small (Outfit 14sp/500), #1A1C16, font-weight 600
- [ ] Distance text — body_small (Outfit 12sp/400), #44483D
- [ ] "Open 24/7" — body_small, #4C662B, weight 500
- [ ] Branch hours (Mon–Fri 9am–5pm) — body_small, #44483D weight 500 (NOT #E8A317 — a11y A11Y-002 fix; #E8A317 fails WCAG AA at 2.17:1)
- [ ] Services line — body_small, #44483D
- [ ] Withdrawal limit — body_small, #44483D
- [ ] "Get Directions" links — label_medium (Outfit 12sp/500), #4C662B, trailing directions icon 20dp (icon-sm), right-aligned within card
- [ ] Divider — #E1E4D5, 16dp h-margin, below last card
- [ ] Loading: skeleton shimmer on map area + results header + all 3 result cards (#E1E4D5, short4 200ms). Filter chips + search remain visible and interactive.
- [ ] Empty: location_off icon 48dp (#44483D) centred + body_lg message "No ATMs or branches found in this area" (#1A1C16) centred. Map + cards hidden.
- [ ] Error: error_outline icon 48dp (#BA1A1A) centred + message + filled retry button (#4C662B). Map + filter chips + cards hidden.
- [ ] Bottom nav: 5 tabs (Home/Accounts/Pay/Cards/More), 80dp height, #F9FAEF bg, active indicator #DCE7C8 pill, all Outfit labels 12sp
- [ ] All text: Outfit typeface throughout. Minimum 14sp for interactive/body content. Touch targets 48dp minimum (chips, links, buttons).
- [ ] Horizontal content padding: 16dp throughout

---

_Generated by /idea export | 2026-05-30_
