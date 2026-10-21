# MOCKUP — Transaction Detail

**Archetype:** detail_screen
**Shell:** Top app bar ("Transaction Details", back arrow, share action). No bottom navigation bar.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Transaction Details     [share]  │  ← TopAppBar
├─────────────────────────────────────┤
│                                     │
│  ████████████████████████████████   │  ← Hero skeleton (160dp, #4C662B base)
│  ████████████████████████████████   │
│  ████████████████████████████████   │
│                                     │
│   ┌─────────────────────────────┐   │  ← Merchant card skeleton (100dp)
│   │ ████████████████████████   │   │    margin_top -20dp overlap
│   └─────────────────────────────┘   │
│                                     │
│  ┌───────────────────────────────┐  │  ← Details card skeleton (300dp)
│  │ ████████████  ██████████████  │  │
│  │ ████████████  ██████████████  │  │
│  │ ████████████  ██████████████  │  │
│  │ ████████████  ██████████████  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ████████████████████████████████   │  ← Actions skeleton (52dp)
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** 4 skeleton blocks per state definition. Hero `#4C662B` height 160dp (no shimmer — uses brand color). Merchant card white/`#E1E4D5` 100dp, radius 20dp, margin_top -20dp. Details card 300dp, radius 16dp. Actions 52dp, radius 12dp. All shimmer on `#E1E4D5`.

---

## Screen: content

```
┌─────────────────────────────────────┐
│ ←  Transaction Details     [share]  │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │                               │  │  ← Hero section, bg #4C662B
│  │           -£42.50             │  │  ← display_large 700w, #BA1A1A
│  │                               │  │
│  │     ╔══════════════╗          │  │
│  │     ║ ✓ Completed  ║          │  │  ← Semi-transparent pill badge
│  │     ╚══════════════╝          │  │
│  └───────────────────────────────┘  │
│                                     │
│      ┌──────────────────────────┐   │  ← Merchant card, white, r=20, elev=4
│      │ [logo] Tesco Supermarket │   │    overlaps hero by 20dp
│      │        [Groceries]       │   │  ← badge #CDEDA3/#4C662B
│      └──────────────────────────┘   │
│                                     │
│  ┌───────────────────────────────┐  │  ← Details card, white, r=16, elev=1
│  │  Date & Time    25 May, 14:32 │  │
│  │  ─────────────────────────── │  │
│  │  Reference   SEPA-202605...23 │  │  ← monospace + [copy] icon #4C662B
│  │  ─────────────────────────── │  │
│  │  Type   SEPA Credit Transfer  │  │
│  │  ─────────────────────────── │  │
│  │  From    Primary Checking     │  │
│  │          ...0130              │  │  ← body_small monospace #44483D
│  │  ─────────────────────────── │  │
│  │  To      Tesco PLC            │  │
│  │          DE89 3704...0044     │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ ↓  Download Receipt           │  │  ← OutlinedButton, #4C662B border+text
│  └───────────────────────────────┘  │
│                                     │
│       [flag] Report an Issue        │  ← label_medium, #BA1A1A, centered
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:**
- Hero: full-width, background `#4C662B`, padding H 24dp, top 28dp, bottom 36dp. Amount `-£42.50` centred, Outfit/display_large (57sp) 700-weight in `#BA1A1A`.
- Status badge: semi-transparent pill (`#4C662B33`), radius 20dp, check_circle icon 14dp + "Completed" label_medium `#4C662B`.
- Merchant card: white `#FFFFFF`, radius 20dp, elevation 4, padding 20dp. Overlaps hero by `margin_top: -20dp`. Logo 56×56dp circle background `#CDEDA3`. Merchant name title_large (22sp/600) `#1A1C16`. Category chip `#CDEDA3`, radius 6dp.
- Details card: white, radius 16dp, elevation 1, padding 20dp, margin H 20dp. 4 label/value rows separated by `#F9FAEF` dividers. Labels label_small `#44483D`, values body_medium 500w `#1A1C16`. Reference value and IBANs in monospace body_small.
- Download Receipt: OutlinedButton, `#4C662B` text + border, radius 12dp, download icon, full-width-ish margin H 20dp.
- Report an Issue: horizontal centred row, flag 16dp `#BA1A1A` + label_medium text `#BA1A1A`.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Transaction Details     [share]  │
├─────────────────────────────────────┤
│                                     │
│                                     │
│           [error_outline]           │  ← icon 48dp, #BA1A1A, centered
│                                     │
│      Transaction not found          │  ← titleMedium, #1A1C16, center
│  We could not load this transaction.│  ← bodyMedium, #44483D, center
│  It may have been removed or there  │
│  may be a connection issue.         │
│                                     │
│         ┌──────────────┐            │
│         │   Go Back    │            │  ← FilledButton, #4C662B → navigate_back
│         └──────────────┘            │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Centred vertically. error_outline icon 48dp `#BA1A1A`. Title titleMedium `#1A1C16`. Body bodyMedium `#44483D`. "Go Back" FilledButton triggers navigate_back.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│ ←  Transaction Details     [share]  │
├─────────────────────────────────────┤
│                                     │
│           [receipt_long]            │  ← icon 48dp, #44483D, centered
│                                     │
│  Transaction details not available  │  ← titleMedium, #1A1C16, center
│  No details are available for this  │  ← bodyMedium, #44483D, center
│  transaction. It may have been      │
│  archived.                          │
│                                     │
│         ┌──────────────┐            │
│         │   Go Back    │            │  ← FilledButton → navigate_back
│         └──────────────┘            │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** receipt_long icon 48dp `#44483D`. Same centred layout as error. "Go Back" FilledButton.

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar back arrow + share icon action
- [ ] Full-bleed hero section `#4C662B`, 160dp height
- [ ] Amount in Outfit/display_large (57sp) 700-weight, `#BA1A1A` (debit)
- [ ] Status badge: semi-transparent pill `#4C662B33`, radius 20dp, check_circle icon
- [ ] Merchant card: white, radius 20dp, elevation 4, overlaps hero -20dp
- [ ] Merchant logo: 56×56dp circle, `#CDEDA3` background
- [ ] Category chip: `#CDEDA3` background, `#4C662B` text, radius 6dp
- [ ] Details card: white, radius 16dp, elevation 1; 4 label/value rows with `#F9FAEF` dividers
- [ ] Reference row: monospace value + content_copy 16dp icon `#4C662B`
- [ ] From/To IBAN values in monospace body_small `#44483D`
- [ ] Download Receipt: OutlinedButton `#4C662B`, download icon, radius 12dp
- [ ] Report an Issue: flag icon 16dp + label_medium, both `#BA1A1A`, centred
- [ ] 4 skeleton blocks matching state layout (loading state)
- [ ] Error/empty states: centred icon + title + body + FilledButton
- [ ] All text Outfit typeface
