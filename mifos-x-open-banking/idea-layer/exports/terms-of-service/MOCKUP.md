# MOCKUP — Terms of Service

**Archetype:** settings
**Shell:** Top app bar ("Terms of Service", back arrow). No bottom navigation bar.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: content

```
┌─────────────────────────────────────┐
│ ←  Terms of Service                 │  ← TopAppBar (M3), arrow_back
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Agreement Overview           │  │  ← title_medium, #4C662B
│  │  ─────────────────────────── │  │
│  │  These Terms of Service       │  │  ← body_medium, #44483D, 1.6 line-height
│  │  govern your use of Mifos X   │  │
│  │  Open Banking, provided by    │  │
│  │  the Mifos Initiative...      │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Acceptance of Terms          │  │
│  │  ─────────────────────────── │  │
│  │  By creating an account or    │  │
│  │  continuing to use Mifos X    │  │
│  │  Open Banking after changes…  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Account Usage                │  │
│  │  ─────────────────────────── │  │
│  │  You are responsible for      │  │
│  │  maintaining the              │  │
│  │  confidentiality of your      │  │
│  │  DirectLogin credentials…     │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Data Handling via Open Bank  │  │
│  │  Project API                  │  │
│  │  ─────────────────────────── │  │
│  │  This application connects    │  │
│  │  to banking services via the  │  │
│  │  OBP REST API…                │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Prohibited Uses              │  │
│  │  ─────────────────────────── │  │
│  │  You must not use this app    │  │
│  │  to: (a) initiate fraudulent  │  │
│  │  transactions; (b) reverse-   │  │
│  │  engineer; (c)…               │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Limitation of Liability      │  │
│  │  ─────────────────────────── │  │
│  │  To the maximum extent        │  │
│  │  permitted by law, the Mifos  │  │
│  │  Initiative shall not be      │  │
│  │  liable for indirect…         │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Dispute Resolution           │  │
│  │  ─────────────────────────── │  │
│  │  Contact legal@mifos.org      │  │
│  │  before formal dispute. LCIA  │  │
│  │  arbitration after 30 days…   │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Governing Law                │  │
│  │  ─────────────────────────── │  │
│  │  Laws of England and Wales.   │  │
│  │  FCA guidance + UK GDPR +     │  │
│  │  Data Protection Act 2018.    │  │
│  └───────────────────────────────┘  │
│                                     │
│     Last updated: 28 May 2026       │  ← body_small, #C5C8BA, centered
│     Version 1.0                     │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:**
- All 8 section cards: white `#FFFFFF`, radius 12dp, 16dp internal padding, 16dp gap between cards.
- Section headers: Outfit/title_medium (16sp/500), `#4C662B`. Thin divider line below each header.
- Section body: Outfit/body_medium (14sp/400), `#44483D`, line-height 1.6 for readability.
- Root padding: 24dp horizontal, 24dp top. Content extends to bottom with 32dp padding.
- Footer: "Last updated: 28 May 2026 — Version 1.0", Outfit/body_small (12sp), `#C5C8BA`, centered, padding-top 16dp.
- Full-scroll: `SingleChildScrollView` — content overflows on small screens.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Terms of Service                 │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ████████████████  (skeleton) │  │  ← Card header skeleton
│  │  ████████████████████████████ │  │  ← Body line 1 skeleton
│  │  ██████████████               │  │  ← Body line 2 skeleton
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  ████████████████  (skeleton) │  │
│  │  ████████████████████████████ │  │
│  │  ████████████████████████████ │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  ████████████████  (skeleton) │  │
│  │  ████████████████████████████ │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Shimmer animation on 3 representative skeleton cards. Matches radius-12dp card proportions. No interactive elements while loading.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Terms of Service                 │
├─────────────────────────────────────┤
│                                     │
│                                     │
│              [gavel]                │  ← icon 48dp, #BA1A1A, centered
│                                     │
│   Unable to load Terms of Service.  │  ← bodyMedium, #44483D, center
│   Please check your connection      │
│   and try again.                    │
│                                     │
│         ┌──────────────┐            │
│         │    Retry     │            │  ← OutlinedButton, #4C662B border+text
│         └──────────────┘            │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Centred vertically in viewport. Gavel icon 48dp in `#BA1A1A`. Message Outfit/body_medium centered in `#44483D`. Retry: M3 OutlinedButton, pill radius, `#4C662B` text and border.

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar with back navigation icon
- [ ] 8 ElevatedCard / FilledCard sections with white background, radius 12dp
- [ ] Section headers in Outfit/title_medium, `#4C662B`
- [ ] Section body in Outfit/body_medium, `#44483D`, line-height 1.6
- [ ] Thin divider below each section header
- [ ] Last-updated footer centered, Outfit/body_small, `#C5C8BA`
- [ ] Loading: 3 shimmer skeleton cards matching card proportions
- [ ] Error: gavel 48dp icon `#BA1A1A` + OutlinedButton retry
- [ ] 24dp horizontal padding throughout
- [ ] 16dp vertical gap between section cards
- [ ] All text Outfit typeface
- [ ] Scrollable content area (SingleChildScrollView)
