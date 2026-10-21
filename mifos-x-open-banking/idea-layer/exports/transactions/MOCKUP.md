# MOCKUP — Transaction History

**Archetype:** index_list
**Shell:** Top app bar ("Transactions", back arrow, filter action). Bottom navigation bar (Accounts tab active).
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Transactions           [filter]  │  ← TopAppBar, arrow_back + filter_list
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │  ← Search bar, #F9FAEF, radius 12
│  │ [search] Search by merchant…  │  │
│  └───────────────────────────────┘  │
│                                     │
│  [All] [Debit] [Credit] [Pending]   │  ← Filter chips row
│                                     │
│  ████████████████████████████████   │  ← Summary card skeleton (80dp, #E1E4D5)
│                                     │
│  ████████████████████████████████   │  ← Row skeleton 1 (68dp, r=12)
│  ████████████████████████████████   │  ← Row skeleton 2 (68dp, r=12)
│  ████████████████████████████████   │  ← Row skeleton 3 (68dp, r=12)
│                                     │
├─────────────────────────────────────┤
│  [home] [Accounts] [Pay][Cards][More]│ ← Bottom nav, Accounts active
└─────────────────────────────────────┘
```

**Layout notes:** Search bar + filter chips visible in loading state. Summary card and 3 row skeletons at `#E1E4D5`, shimmer animation. Filter "All" chip shows selected state (`#4C662B` fill).

---

## Screen: content

```
┌─────────────────────────────────────┐
│ ←  Transactions           [filter]  │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │  ← Search bar, #F9FAEF, r=12
│  │ [search] Search by merchant…  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← Date range picker, #F9FAEF
│  │ [date_range] Last 30 Days  ▾  │  │
│  └───────────────────────────────┘  │
│                                     │
│  [●All] [Debit] [Credit] [Pending]  │  ← Chips; All=filled #4C662B/white
│                                     │
│  ┌───────────────────────────────┐  │  ← Monthly summary, #CDEDA3, r=16
│  │  Spent this month  │  Received│  │
│  │  £1,240.30         │ £3,200.00│  │  ← #BA1A1A debit | #4C662B credit
│  └───────────────────────────────┘  │    title_large 700w
│                                     │
│  25 May 2026                        │  ← Date group header, label_medium #44483D
│                                     │
│  ┌───────────────────────────────┐  │  ← Txn row 1, white, r=12, elev=1
│  │ [T] Tesco Supermarket -£42.50 │  │  ← logo 40dp circle #CDEDA3
│  │     25 May 2026 · [Groceries] │  │  ← date #44483D · chip #CDEDA3/#4C662B
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │  ← Txn row 2
│  │ [B] Salary Payment +£3,200.00 │  │  ← credit amount #4C662B
│  │     24 May 2026 · [Income]    │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │  ← Txn row 3
│  │ [E] EDF Energy       -£94.20  │  │
│  │     23 May 2026 · [Utilities] │  │  ← Utilities badge: #CDEDA3 / #44483D (a11y)
│  └───────────────────────────────┘  │
│                                     │
│       Load More Transactions        │  ← Text button, #4C662B, label_medium, centered
│                                     │
├─────────────────────────────────────┤
│ [Home] [●Accounts] [Pay][Cards][More]│  ← Accounts active: #DCE7C8 indicator pill
└─────────────────────────────────────┘
```

**Layout notes:**
- Search bar: `#F9FAEF` fill, radius 12dp, search icon `#44483D` leading, mic trailing.
- Date range picker: `#F9FAEF` fill, radius 12dp, date_range icon `#4C662B`, expand_more chevron.
- Filter chips: "All" filled `#4C662B`/white. Others outlined `#E1E4D5` border / `#44483D` text. Radius pill (20dp). Horizontally scrollable.
- Monthly summary: `#CDEDA3` background, radius 16dp, padding 16dp. Spent in `#BA1A1A` title_large/700. Received in `#4C662B` title_large/700. 1×40dp `#E1E4D5` vertical divider.
- Date group header: label_medium `#44483D`, tracking 0.5, padding H 20dp.
- Transaction rows: white `#FFFFFF`, radius 12dp, elevation 1, padding 14dp, margin H 20dp, gap 8dp. Merchant logo 40×40dp circle `#CDEDA3` bg. Name body_medium 500w `#1A1C16`. Debit amount body_large 600w `#BA1A1A`; credit `#4C662B`. Category badge `#CDEDA3` bg, radius 4dp.
- Load More: text button, `#4C662B`, centred, padding_vertical 16dp.
- Bottom nav: `#F9FAEF` bg, `#C5C8BA` border-top. Accounts tab: `#DCE7C8` active indicator pill.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│ ←  Transactions           [filter]  │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │ [search] Search by merchant…  │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ [date_range] Last 30 Days  ▾  │  │
│  └───────────────────────────────┘  │
│  [●All] [Debit] [Credit] [Pending]  │
│                                     │
│         [no_transactions]           │  ← illustration 64dp, #44483D
│       No transactions found         │  ← titleMedium, #1A1C16, center
│   No transactions match your        │  ← bodyMedium, #44483D, center
│   current filters. Try adjusting    │
│   your search or date range.        │
│                                     │
│      ┌─────────────────────┐        │
│      │    Clear Filters    │        │  ← OutlinedButton, #4C662B
│      └─────────────────────┘        │
├─────────────────────────────────────┤
│ [Home] [●Accounts] [Pay][Cards][More]│
└─────────────────────────────────────┘
```

**Layout notes:** Illustration/icon 64dp `#44483D` centred. "Clear Filters" OutlinedButton triggers `clear_filters` action.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Transactions           [filter]  │
├─────────────────────────────────────┤
│  ┌───────────────────────────────┐  │
│  │ [search] Search by merchant…  │  │
│  └───────────────────────────────┘  │
│                                     │
│          [error_outline]            │  ← 48dp, #BA1A1A, centered
│   Could not load transactions       │  ← titleMedium, #1A1C16, center
│   We were unable to load your       │  ← bodyMedium, #44483D, center
│   transactions. Check your          │
│   connection and try again.         │
│                                     │
│         ┌──────────────┐            │
│         │    Retry     │            │  ← FilledButton, #4C662B
│         └──────────────┘            │
├─────────────────────────────────────┤
│ [Home] [●Accounts] [Pay][Cards][More]│
└─────────────────────────────────────┘
```

**Layout notes:** Search bar persists. Error icon + message centred. Retry FilledButton.

---

## Screen: searching

```
┌─────────────────────────────────────┐
│ ←  Transactions           [filter]  │
├─────────────────────────────────────┤
│  ┌─────────────────────────────────┐│  ← Search bar focused, active border
│  │ [search] "Tesco"              X ││
│  └─────────────────────────────────┘│
│  [●All] [Debit] [Credit] [Pending]  │
│                                     │
│  ████████████████████████████████   │  ← Search result skeleton 1 (68dp)
│  ████████████████████████████████   │  ← Search result skeleton 2 (68dp)
│                                     │
├─────────────────────────────────────┤
│ [Home] [●Accounts] [Pay][Cards][More]│
└─────────────────────────────────────┘
```

**Layout notes:** Search bar shows active state with clear (X) trailing button. 2 skeleton rows while results load.

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar with back arrow + filter_list action
- [ ] Search bar: `#F9FAEF` fill, radius 12dp, search leading + mic trailing icons
- [ ] Date range picker: `#F9FAEF` fill, radius 12dp, tappable row with expand chevron
- [ ] 4 filter chips: "All" filled `#4C662B`/white; others outlined `#E1E4D5`/`#44483D`; pill radius 20dp
- [ ] Monthly summary card: `#CDEDA3` bg, radius 16dp; spent `#BA1A1A`, received `#4C662B`, both title_large/700
- [ ] Date group header: label_medium `#44483D`, tracking 0.5
- [ ] Transaction rows: white, radius 12dp, elevation 1; merchant logo 40dp circle `#CDEDA3`
- [ ] Debit amounts `#BA1A1A` body_large/600; credit amounts `#4C662B`
- [ ] Category chips: `#CDEDA3` bg, radius 4dp; text `#4C662B` (or `#44483D` for Utilities a11y fix)
- [ ] "Load More Transactions" text button centred `#4C662B`
- [ ] Bottom nav: Accounts active with `#DCE7C8` indicator pill
- [ ] Empty state: illustration + "Clear Filters" OutlinedButton
- [ ] Error state: error_outline icon `#BA1A1A` + Retry FilledButton
- [ ] Searching state: 2 skeleton rows, focused search bar
- [ ] All text Outfit typeface
- [ ] 20dp horizontal margin on cards
