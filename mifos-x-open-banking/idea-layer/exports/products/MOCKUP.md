# MOCKUP — Products

**Archetype:** index_list
**Shell:** Top app bar (title "Products", back arrow → navigate_back, search icon → search_products) + 5-tab Bottom nav (Products active, #DCE7C8 pill indicator).
**Accent:** #4C662B (Earth-green primary). Typography: Outfit. Design system: M3.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Products                   [🔍]  │  ← M3 TopAppBar: navigation_icon=arrow_back, #F9FAEF bg
├─────────────────────────────────────┤
│                                     │
│  Products                           │  ← headline_large (Outfit 32sp/400), #4C662B, 16dp top/h pad
│  Explore accounts, savings,         │  ← body_medium (14sp/400), #44483D, 16dp h pad
│  loans and cards tailored for you.  │
│                                     │
│  [●All][Savings][Loans][Cards]      │  ← Horizontal scroll chip row; 8dp gap; 16dp h pad
│  [Mortgages]                        │    Active chip bg #4C662B text #FFFFFF radius 20dp
│                                     │    Inactive: outlined #E1E4D5 text #44483D radius 20dp
│  ┌───────────────────────────────┐  │
│  │  ████████████████  [░░░░░░░] │  │  ← Skeleton card 1 (#E1E4D5 shimmer, radius 16, h-margin 20)
│  │  ███████████████████████████  │  │    shimmer_duration: short4 (200ms), motion.standard easing
│  │  ████████████                 │  │
│  │                 [░░░░][░░░░] │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  ████████████████  [░░░░░░░] │  │  ← Skeleton card 2
│  │  ███████████████████████████  │  │
│  │  ████████████                 │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  ████████████████  [░░░░░░░] │  │  ← Skeleton card 3
│  │  ███████████████████████████  │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  ████████████████  [░░░░░░░] │  │  ← Skeleton card 4
│  │  ███████████████████████████  │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  🏠   💳  ●Products  💸    ···      │  ← Bottom nav; Products: store icon, #DCE7C8 active pill
└─────────────────────────────────────┘
```

**Layout notes:** skeleton_count=4; shimmer on full card placeholder; filter tab row visible but non-interactive. No promotions banner during loading. Title + subtitle always visible.

---

## Screen: populated

```
┌─────────────────────────────────────┐
│ ←  Products                   [🔍]  │
├─────────────────────────────────────┤
│                                     │
│  Products                           │  ← headline_large, #4C662B
│  Explore accounts, savings, loans   │  ← body_medium, #44483D
│  and cards tailored for you.        │
│                                     │
│  [●All][Savings][Loans][Cards]      │  ← All: bg #4C662B text #FFFFFF (role=tab, selected=true)
│  [Mortgages]                        │    Others: outlined #E1E4D5 border, text #44483D
│                                     │
│  ┌───────────────────────────────┐  │  ← product_instant_access_savings card
│  │  Instant Access Savings [Savings]│    White #FFFFFF, radius 16, elevation 2, pad 16
│  │                               │  │    h-margin 20, b-margin 12; border #F9FAEF 1dp
│  │  4.5% AER                     │  │  ← display_small (32sp/600), #4C662B, bold
│  │  Earn 4.5% AER on every pound │  │  ← body_medium (14sp/400), #44483D
│  │  you save. Withdraw at any    │  │
│  │  time with no notice period.  │  │
│  │                               │  │
│  │  [4.5% AER][Instant access]   │  │  ← Chips: #CDEDA3 text #4C662B · #DCE7C8 text #386663
│  │  [No minimum deposit]         │  │    All radius 8, label_small (11sp/500)
│  │                               │  │
│  │           [Details][Apply Now]│  │  ← right-aligned; outlined (#4C662B) + filled (#4C662B)
│  └───────────────────────────────┘  │    Both radius 8, label_medium (12sp/500), pad_h 16 pad_v 8
│                                     │
│  ┌───────────────────────────────┐  │  ← product_fixed_rate_bond card
│  │  Fixed Rate Bond 1yr [Savings]│  │    Badge: bg #CDEDA3 text #4C662B, radius 6, label_small
│  │  5.1% AER                     │  │  ← display_small, #4C662B, bold
│  │  Lock in a market-leading     │  │
│  │  5.1% AER for 12 months.      │  │  ← body_medium, #44483D
│  │  Minimum deposit £1,000.      │  │
│  │  Interest paid at maturity.   │  │
│  │                               │  │
│  │  [5.1% AER][12-month term]    │  │  ← Chips: #CDEDA3/#4C662B · #CDEDA3/#44483D (A11Y fix)
│  │  [FSCS protected]             │  │    #CDEDA3/#4C662B
│  │                               │  │
│  │           [Details][Apply Now]│  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← product_personal_loan card
│  │  Personal Loan          [Loans]│  │    Badge: bg #CDEDA3, text #44483D, radius 6 (A11Y fix)
│  │  From 6.9% APR                │  │  ← display_small, #4C662B, bold
│  │  Borrow from £1,000 to        │  │
│  │  £25,000 at a representative  │  │  ← body_medium, #44483D
│  │  6.9% APR. Flexible terms     │  │
│  │  from 1 to 7 years.           │  │
│  │                               │  │
│  │  [From 6.9% APR][Up to £25k] │  │  ← #CDEDA3/#44483D · #CDEDA3/#4C662B
│  │  [1–7 year terms]             │  │    #DCE7C8 bg, text #386663
│  │                               │  │
│  │           [Details][Apply Now]│  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← product_platinum_credit_card card
│  │  Platinum Credit Card  [Cards]│  │    Badge: bg #DCE7C8, text #386663, radius 6
│  │  0% for 20 months             │  │  ← display_small, #4C662B, bold
│  │  0% interest on purchases for │  │
│  │  20 months. No annual fee.    │  │  ← body_medium, #44483D
│  │  Contactless & Apple / Google │  │
│  │  Pay enabled.                 │  │
│  │                               │  │
│  │  [0% 20 months][No annual fee]│  │  ← #DCE7C8/#386663 · #CDEDA3/#4C662B
│  │  [Contactless & Apple/Google] │  │    #CDEDA3/#4C662B
│  │                               │  │
│  │           [Details][Apply Now]│  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← promotions_banner: #4C662B fill, radius 12
│  │  Refer a friend — earn £50    │  │  ← promo_banner_text: title_small (14sp/500), #FFFFFF, semibold
│  │  When your friend opens any   │  │  ← promo_banner_detail: body_small (12sp/400), #CDEDA3
│  │  account before 30 June 2026  │  │    h-margin 20, b-margin 16; tap → navigate(home)
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  🏠   💳  ●Products  💸    ···      │
└─────────────────────────────────────┘
```

**Layout notes:**
- Screen background: #F9FAEF (background token).
- Each product card: #FFFFFF fill, radius 16dp, 2dp elevation (level2 = 3dp M3), 1dp #F9FAEF border, 16dp internal padding, 20dp horizontal margin, 12dp bottom margin.
- Card header row: product name (title_medium 16sp/500, #1A1C16) + category badge (right-aligned in row, label_small 11sp/500).
- Headline rate: display_small (32sp/600), #4C662B — dominant typographic hierarchy.
- Description: body_medium (14sp/400), #44483D, padding_bottom 8dp.
- Feature chips: horizontal scroll row, 8dp gap, each chip radius 8dp, label_small (11sp/500), 8dp h-padding, 4dp v-padding.
- Action row: justify=flex_end, 8dp gap; "Details" outlined (border+text #4C662B, radius 8); "Apply Now" filled (bg #4C662B, text #FFFFFF, radius 8); both label_medium, 16dp h-pad, 8dp v-pad.
- A11Y fixes in source: frb_feat_term text #44483D (was #E8A317 FAIL), pl_category_badge text #44483D (was #E8A317 FAIL), personal_loan_feat_apr text #44483D.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│ ←  Products                   [🔍]  │
├─────────────────────────────────────┤
│                                     │
│  Products                           │  ← headline_large, #4C662B
│  Explore accounts, savings, loans   │  ← body_medium, #44483D
│  and cards tailored for you.        │
│                                     │
│  [●All][Savings][Loans][Cards]      │  ← Category tabs remain visible and interactive
│  [Mortgages]                        │
│                                     │
│                                     │
│             🏪                      │  ← store_outlined icon, 48dp, #75796C, centred
│                                     │
│      No products available          │  ← title_medium (16sp/500), #1A1C16, centred
│                                     │
│  No products match the selected     │  ← body_medium (14sp/400), #44483D, centred
│  category. Try a different filter   │
│  or check back later.               │
│                                     │
├─────────────────────────────────────┤
│  🏠   💳  ●Products  💸    ···      │
└─────────────────────────────────────┘
```

**Layout notes:** Empty state (icon + title + message) centred below filter tab row. No product cards or promotions banner shown. Category tabs remain active so user can switch filter.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Products                   [🔍]  │
├─────────────────────────────────────┤
│                                     │
│  Products                           │  ← headline_large, #4C662B
│  Explore accounts, savings, loans   │  ← body_medium, #44483D
│  and cards tailored for you.        │
│                                     │
│  [●All][Savings][Loans][Cards]      │  ← Category tabs remain visible
│  [Mortgages]                        │
│                                     │
│              ☁                      │  ← cloud_off icon, 48dp, #BA1A1A (error token), centred
│                                     │
│     Unable to load products         │  ← title_medium (16sp/500), #1A1C16, centred
│                                     │
│  Check your connection and try      │  ← body_medium (14sp/400), #44483D, centred
│  again. Your saved favourites       │
│  are still available offline.       │
│                                     │
│         ┌─────────────┐             │
│         │    Retry    │             │  ← Outlined button, border+text #4C662B, radius pill
│         └─────────────┘             │    fires RetryLoad event
│                                     │
├─────────────────────────────────────┤
│  🏠   💳  ●Products  💸    ···      │
└─────────────────────────────────────┘
```

**Layout notes:** Error icon `cloud_off` in error color (#BA1A1A). Title in on_surface (#1A1C16). Message in on_surface_variant (#44483D). Retry button fires `RetryLoad` event → re-triggers `GET /obp/v5.0.0/banks/{bankId}/products`.

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar: #F9FAEF background, 56dp height, title "Products" (title_large Outfit 22sp/400), back arrow icon left, search icon right
- [ ] Page title: "Products" — headline_large (Outfit 32sp/400), #4C662B, bold; 16dp top + horizontal padding
- [ ] Subtitle: "Explore accounts, savings, loans and cards tailored for you." — body_medium (14sp/400), #44483D
- [ ] Filter chips row: horizontal scroll, 8dp gap, 16dp horizontal padding; 5 chips (All / Savings / Loans / Cards / Mortgages)
- [ ] Active chip "All": bg #4C662B, text #FFFFFF, radius 20dp, label_medium (12sp/500), 16dp h-pad, 8dp v-pad
- [ ] Inactive chips: outlined 1dp border #E1E4D5, text #44483D, radius 20dp, label_medium
- [ ] Product cards: #FFFFFF fill, radius 16dp, elevation 2 (3dp M3 level2), 1dp border #F9FAEF, 16dp internal padding, 20dp h-margin, 12dp b-margin
- [ ] Card header row: product name (title_medium 16sp/500, #1A1C16, semibold) + category badge (label_small 11sp/500, radius 6dp)
- [ ] Savings badges: bg #CDEDA3, text #4C662B
- [ ] Loans badge: bg #CDEDA3, text #44483D (A11Y fix — not #E8A317)
- [ ] Cards badge: bg #DCE7C8, text #386663
- [ ] Headline rates: display_small (Outfit 32sp/600), #4C662B, bold — primary visual anchor per card
- [ ] Product descriptions: body_medium (14sp/400), #44483D
- [ ] Feature chips: radius 8dp, label_small (11sp/500), 8dp h-pad, 4dp v-pad; correct per-chip bg+text pair per SPEC
- [ ] frb_feat_term chip text: #44483D on #CDEDA3 (NOT #E8A317 — A11Y-002 contrast fix)
- [ ] personal_loan_feat_apr chip text: #44483D on #CDEDA3 (A11Y fix)
- [ ] Action row: right-aligned, 8dp gap; "Details" outlined (#4C662B border+text, radius 8); "Apply Now" filled (#4C662B bg, #FFFFFF text, radius 8); label_medium (12sp/500)
- [ ] Promotions banner: bg #4C662B, radius 12dp, 16dp h-pad, 14dp v-pad, 20dp h-margin, 16dp b-margin
- [ ] Promo title "Refer a friend — earn £50": title_small (14sp/500), #FFFFFF, semibold
- [ ] Promo detail "When your friend opens any account before 30 June 2026": body_small (12sp/400), #CDEDA3
- [ ] Loading state: 4 skeleton product cards, #E1E4D5 shimmer base, 200ms shimmer (short4), radius 16dp; filter row visible
- [ ] Empty state: store_outlined icon 48dp centred, "No products available" title_medium #1A1C16, message body_medium #44483D; no product cards
- [ ] Error state: cloud_off icon 48dp #BA1A1A centred, title title_medium #1A1C16, message body_medium #44483D, Retry outlined button #4C662B
- [ ] Bottom nav: 5 tabs (Home=home, Accounts=account_balance, Products=store, Send=send, More=more_horiz); Products tab active with #DCE7C8 pill indicator; 80dp height
- [ ] Screen background: #F9FAEF (background token)
- [ ] All text: Outfit typeface only. Touch targets 48dp minimum. 16dp horizontal content padding throughout.
