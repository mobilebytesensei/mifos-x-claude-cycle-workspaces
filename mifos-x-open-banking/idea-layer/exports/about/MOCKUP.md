# MOCKUP — About

**Archetype:** settings
**Shell:** Top app bar ("About") with back arrow (`arrow_back`). No bottom navigation bar.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: content

```
┌─────────────────────────────────────┐
│ ←  About                            │  ← M3 TopAppBar, title_large, arrow_back #4C662B
├─────────────────────────────────────┤
│                                     │
│         ┌──────────────┐            │
│         │  [Mifos Logo]│            │  ← Image 80×80dp, tint #4C662B, centered
│         └──────────────┘            │  ← padding_top + padding_bottom 32dp (spacing.xl)
│       Mifos X Open Banking          │  ← headline_small (24sp/600), #4C662B, centered
│      Open Banking for Everyone      │  ← body_medium (14sp/400), #44483D, centered
│                                     │
│  ┌───────────────────────────────┐  │  ← App Info card: #FFFFFF, radius 12dp, pad 16dp
│  │  Version            1.0.0     │  │  ← body_large #1A1C16 | body_medium #44483D (data_driven)
│  │ ────────────────────────────  │  │  ← divider #E1E4D5, 4dp margins
│  │  Build          2026.05.001   │  │  ← body_large #1A1C16 | body_medium #44483D (data_driven)
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← Legal card: #FFFFFF, radius 12dp, pad 16dp
│  │  Legal                        │  │  ← title_medium (16sp/500), #4C662B, pad_bottom 8dp
│  │ ────────────────────────────  │  │
│  │  Terms of Service         ↗   │  │  ← body_large #1A1C16 | open_in_new 18dp #C5C8BA
│  │ ────────────────────────────  │  │  ← divider #E1E4D5
│  │  Privacy Policy           ↗   │  │  ← body_large #1A1C16 | open_in_new 18dp #C5C8BA
│  │ ────────────────────────────  │  │  ← divider #E1E4D5
│  │  Open Source Licenses     >   │  │  ← body_large #1A1C16 | chevron_right 20dp #C5C8BA
│  └───────────────────────────────┘  │
│                                     │  ← margin_top 24dp (spacing.lg)
│  ┌───────────────────────────────┐  │
│  │        Rate This App          │  │  ← Outlined button, border+text #4C662B, label_large (14sp/500)
│  └───────────────────────────────┘  │  ← data-action="rate_app" → ReviewManager API
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:**
- Screen background: #F9FAEF (`background` token). Root padding: 24dp (spacing.lg) on all sides.
- Logo section: centered column, 32dp top + bottom padding; logo → app name → tagline stacked with 4dp gaps.
- App Info card: full-width, 12dp radius. Row layout: label (flex 1) + value right-aligned. Hairline #E1E4D5 divider with 4dp top/bottom margin between Version and Build rows.
- Legal card: full-width, 12dp radius. "Legal" header in title_medium #4C662B with 8dp bottom padding. Each link row: body_large text (flex 1) + trailing icon (18–20dp). Hairline #E1E4D5 dividers between all three rows.
- Rate App button: full-width outlined, 32dp horizontal padding, centered. 24dp top margin.
- Scroll: SingleChildScrollView — content may overflow on small screens (390dp baseline).

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  About                            │  ← TopAppBar visible during loading
├─────────────────────────────────────┤
│                                     │
│       ░░░░░░░░░░░░░░░  (skeleton)   │  ← 80×80dp logo shimmer, centered
│       ░░░░░░░░░░░░░░░░ (skeleton)   │  ← App name placeholder
│       ░░░░░░░░░░░░░░   (skeleton)   │  ← Tagline placeholder
│                                     │
│  ┌───────────────────────────────┐  │  ← App Info card skeleton
│  │ ░░░░░░░░░   ░░░░░░░░░░░░░░░  │  │
│  │ ──────────────────────────── │  │
│  │ ░░░░░░░░░   ░░░░░░░░░░░░░░░  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← Legal card skeleton (3 rows, settings variant)
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  │
│  │ ──────────────────────────── │  │
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  │
│  │ ──────────────────────────── │  │
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Shimmer animates #E1E4D5 → #F0F1E6 (trust_horizon gradient); duration short4 (200ms). Reduced-motion: static #E1E4D5 blocks (no animation). No interactive elements visible. Top app bar always visible. Rate App button not shown during loading.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  About                            │
├─────────────────────────────────────┤
│                                     │
│                                     │
│                                     │
│               ⓘ                     │  ← info_outline icon, 48dp, #BA1A1A (error), centered
│                                     │  ← padding_bottom 16dp (spacing.md)
│   Unable to load app information.   │  ← body_medium (14sp/400), #44483D, centered
│       Please restart the app.       │  ← body_medium (14sp/400), #44483D, centered
│                                     │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** `about_error_state` centered column with 32dp padding (spacing.xl). Icon + message only — no retry button (user must restart app). Cards and Rate App button hidden. Top app bar remains visible with back arrow functional.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│ ←  About                            │
├─────────────────────────────────────┤
│                                     │
│         ┌──────────────┐            │
│         │  [Mifos Logo]│            │  ← Logo always rendered (#4C662B tint)
│         └──────────────┘            │
│       Mifos X Open Banking          │  ← headline_small, #4C662B
│      Open Banking for Everyone      │  ← body_medium, #44483D
│                                     │
│  ┌───────────────────────────────┐  │  ← Legal card always visible
│  │  Legal                        │  │
│  │ ────────────────────────────  │  │
│  │  Terms of Service         ↗   │  │
│  │ ────────────────────────────  │  │
│  │  Privacy Policy           ↗   │  │
│  │ ────────────────────────────  │  │
│  │  Open Source Licenses     >   │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** App Info card (version/build rows) and Rate App button are hidden — version data unavailable. Logo section and Legal card always rendered; legal navigation must remain accessible regardless of build data availability. No empty-state illustration shown (`show_empty_state: false` per ui.yaml).

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar: title "About", `arrow_back` navigation icon, #4C662B icon color
- [ ] App logo: 80×80dp centered, tinted #4C662B, a11y label "Mifos X Open Banking logo"
- [ ] App name: headline_small (Outfit 24sp/600) in #4C662B, centered
- [ ] Tagline: body_medium (Outfit 14sp/400) in #44483D, centered
- [ ] Logo section: 32dp top + bottom padding (spacing.xl), centered column alignment
- [ ] App Info card: #FFFFFF fill, 12dp radius, 16dp padding, 16dp bottom margin
- [ ] Version row: "Version" body_large #1A1C16 (left) + "1.0.0" body_medium #44483D (right)
- [ ] Build row: "Build" body_large #1A1C16 (left) + "2026.05.001" body_medium #44483D (right)
- [ ] Hairline #E1E4D5 divider with 4dp top/bottom margin between Version and Build rows
- [ ] Legal card: #FFFFFF fill, 12dp radius, 16dp padding, 16dp bottom margin
- [ ] "Legal" header: title_medium (Outfit 16sp/500) in #4C662B, 8dp bottom padding
- [ ] Terms of Service + Privacy Policy rows: body_large #1A1C16 + `open_in_new` 18dp #C5C8BA trailing
- [ ] Open Source Licenses row: body_large #1A1C16 + `chevron_right` 20dp #C5C8BA trailing
- [ ] Hairline #E1E4D5 dividers between all three Legal rows (4dp top/bottom margin)
- [ ] "Rate This App" outlined button: #4C662B border + text, label_large (Outfit 14sp/500), 32dp horizontal padding, 24dp top margin
- [ ] Loading: settings-variant skeleton shimmer — #E1E4D5 blocks, 200ms short4, static on reduced motion
- [ ] Error state: `info_outline` 48dp #BA1A1A centered; "Unable to load app information. Please restart the app." body_medium #44483D
- [ ] Empty state: logo section + Legal card visible; App Info card + Rate App button hidden
- [ ] All text: Outfit typeface. Screen background #F9FAEF. 24dp root padding.
- [ ] All interactive rows and button: 48dp minimum touch target (M3 standard)
