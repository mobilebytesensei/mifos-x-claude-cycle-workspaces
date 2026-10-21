# MOCKUP — Home Dashboard

**Archetype:** dashboard
**Shell:** Bottom navigation bar with 5 tabs (Home/Accounts/Pay/Cards/More). Home active.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│                                     │
│  Good morning, Alex                 │  ← headline_medium, #4C662B (visible)
│  Monday, 25 May 2026                │  ← body_medium, #44483D (visible)
│                                     │
│  ┌───────────────────────────────┐  │
│  │                               │  │  ← Skeleton account card (200dp, #E1E4D5, 20dp radius)
│  │ ████████████████████████████  │  │
│  │ ████████████████████████████  │  │
│  │ ████████████████████████████  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ████████████████████████████████   │  ← Skeleton balance chip
│                                     │
│  ┌───────────────────────────────┐  │
│  │ ███  ████████████████  ██████ │  │  ← Skeleton txn row 1 (72dp, #E1E4D5, 12dp radius)
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ ███  ████████████████  ██████ │  │  ← Skeleton txn row 2
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  [home*] [accounts] [pay] [cards] [more] │  ← Bottom nav, Home active
└─────────────────────────────────────┘
```

**Layout notes:** Greeting and date always visible during loading. Account card and transactions shimmer with skeleton blocks. No services grid during loading.

---

## Screen: content

```
┌─────────────────────────────────────┐
│                                     │
│  Good morning, Alex                 │  ← headline_medium, #4C662B
│  Monday, 25 May 2026                │  ← body_medium, #44483D
│                                     │
│  ┌───────────────────────────────┐  │  ← Account card: #4C662B fill, 20dp radius, 4dp elev
│  │  Primary Checking             │  │  ← label_large, #FFFFFF
│  │                               │  │
│  │  £4,250.00                    │  │  ← display_small, #FFFFFF
│  │                               │  │
│  │  •••• •••• •••• 0130          │  │  ← body_medium, #FFFFFF
│  │                               │  │
│  │  [Send Money] [Beneficiaries] [View Cards] │  ← Quick action buttons
│  └───────────────────────────────┘  │
│                                     │
│  ┌─────────────────────────────┐    │  ← Total balance chip: #CDEDA3, 12dp radius
│  │ 💼 Total across 3 accounts:  │    │
│  │    £12,480.50                │    │  ← label_medium, #4C662B
│  └─────────────────────────────┘    │
│                                     │
│  Recent Transactions      View All  │  ← title_large + label_medium link
│                                     │
│  ┌───────────────────────────────┐  │  ← Txn 1: white card, 12dp radius, 1dp elev
│  │ [🛒] Tesco Supermarket       │  │  ← shopping_cart, #4C662B on #CDEDA3 circle
│  │      23 May · Groceries      │  │  ← body_small, #44483D
│  │                   −£42.50    │  │  ← body_large, #BA1A1A, bold
│  │                   [DEBIT]    │  │  ← label_small badge, #BA1A1A on #CDEDA3
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ [💳] Salary Payment          │  │  ← payments icon, #4C662B on #CDEDA3 circle
│  │      22 May · Income         │  │
│  │                  +£3,200.00  │  │  ← body_large, #4C662B, bold
│  │                   [CREDIT]   │  │  ← label_small, #4C662B on #CDEDA3
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ [⚡] EDF Energy              │  │  ← bolt icon, #44483D on #CDEDA3 (a11y fix)
│  │      20 May · Utilities      │  │
│  │                   −£94.20    │  │  ← #BA1A1A, bold
│  │                   [DEBIT]    │  │
│  └───────────────────────────────┘  │
│                                     │
│  Services                           │  ← title_large, #1A1C16
│                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────┐ │  ← 3 service tiles, horizontal flex-wrap
│  │ 🔁       │ │ 📍       │ │ 💱   │ │
│  │ Standing │ │ ATM &    │ │ FX   │ │
│  │ Orders   │ │ Branches │ │ Rates│ │
│  └──────────┘ └──────────┘ └──────┘ │
│                                     │
├─────────────────────────────────────┤
│  [home*] [accounts] [pay] [cards] [more] │
└─────────────────────────────────────┘
```

**Layout notes:**
- Account card: #4C662B fill (earth-green hero), 20dp radius, 4dp elevation, md horizontal margin.
- Quick action buttons: inside card — "Send Money" (filled white), "Beneficiaries" + "View Cards" (outlined white), sm padding, 12dp radius, equal flex.
- Total balance chip: full content width, #CDEDA3, 12dp radius, row with wallet icon 16dp.
- Transaction icon containers: 44×44dp circles, #CDEDA3 fill. bolt icon uses #44483D (contrast fix from #E8A317 — a11y compliance).
- Service tiles: #CDEDA3 (Standing Orders + FX) and #DCE7C8 (ATM), 16dp radius, equal flex.

---

## Screen: error

```
┌─────────────────────────────────────┐
│                                     │
│  Good morning, Alex                 │
│  Monday, 25 May 2026                │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ⚠ Could not load your       │  │  ← Error card: white, error_outline icon
│  │    account                   │  │
│  │  Check your connection and   │  │
│  │  try again.                  │  │
│  │                              │  │
│  │         [  Retry  ]          │  │  ← outlined button, #4C662B
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  [home*] [accounts] [pay] [cards] [more] │
└─────────────────────────────────────┘
```

---

## Screen: empty

```
┌─────────────────────────────────────┐
│                                     │
│  Good morning, Alex                 │
│  Monday, 25 May 2026                │
│                                     │
│  ┌───────────────────────────────┐  │
│  │     [account_empty icon]      │  │  ← Empty state illustration
│  │                               │  │
│  │       No accounts yet         │  │  ← title_medium, center
│  │  Your accounts will appear    │  │  ← body_medium, #44483D, center
│  │  here once your profile       │  │
│  │  is set up.                   │  │
│  │                               │  │
│  │     [ Set Up Account ]        │  │  ← filled, #4C662B
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  [home*] [accounts] [pay] [cards] [more] │
└─────────────────────────────────────┘
```

---

## Design Checklist (Figma / Stitch)

- [ ] Greeting "Good morning, Alex" — headline_medium (Outfit 28sp), #4C662B; 24dp top padding
- [ ] Date line — body_medium (Outfit 14sp/400), #44483D
- [ ] Hero account card: #4C662B fill, 20dp radius, 4dp elevation, 16dp horizontal margin
- [ ] Account balance: display_small (Outfit 32sp/600), white text
- [ ] Quick actions: "Send Money" filled white; "Beneficiaries" + "View Cards" outlined white; 12dp radius; equal flex
- [ ] Total balance chip: #CDEDA3 fill, 12dp radius, account_balance_wallet icon 16dp #4C662B + label_medium #4C662B text
- [ ] "Recent Transactions" header: title_large (22sp), #1A1C16; "View All" label_medium #4C662B link
- [ ] Transaction rows: #FFFFFF fill, 12dp radius, 1dp elevation; 44×44dp icon circle (#CDEDA3 fill)
- [ ] Debit amounts: body_large #BA1A1A bold. Credit amounts: #4C662B bold.
- [ ] DEBIT badge: #CDEDA3 fill, #BA1A1A text, label_small. CREDIT badge: #CDEDA3 fill, #4C662B text.
- [ ] bolt icon on EDF Energy row: #44483D (NOT #E8A317 — a11y contrast fix)
- [ ] "Services" header: title_large (22sp), #1A1C16
- [ ] Standing Orders + FX tiles: #CDEDA3 fill, icons #4C662B + #386663. ATM tile: #DCE7C8 fill, icon #386663.
- [ ] Bottom nav: 5 tabs, Home active indicator (#DCE7C8 pill), 80dp height
- [ ] Skeleton cards during loading: #E1E4D5, 20dp radius (account), 12dp radius (txn rows)
- [ ] All text: Outfit typeface. Touch targets 48dp minimum. 16dp horizontal content padding.
