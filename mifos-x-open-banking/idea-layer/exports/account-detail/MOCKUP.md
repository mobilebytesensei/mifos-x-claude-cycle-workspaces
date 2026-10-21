# MOCKUP — Account Detail

**Archetype:** detail_screen
**Shell:** Top app bar ("Account Details") with back arrow. Consumer bottom navigation bar (Accounts active).
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: content (Primary)

```
┌─────────────────────────────────────┐
│ ←  Account Details                  │  ← TopAppBar, title_large, back arrow
├─────────────────────────────────────┤
│                                     │
│  Primary Checking                   │  ← label_large, #FFFFFFB3 on #4C662B hero
│  £4,250.00                          │  ← display_large/Bold, #FFFFFF
│  [GBP]  [CHECKING]                  │  ← label_small badges, #FFFFFF, #FFFFFF1A bg
│                                     │
│       ┌───────────────────────┐     │
│       │ IBAN                  │     │  ← White elevated card, 16dp radius
│       │ DE89 3704 0044 0532   │     │     overlaps hero by 16dp
│       │ 0130 00          [⧉]  │     │  ← content_copy icon #4C662B
│       │ ─────────────────── │     │
│       │ BIC / SWIFT           │     │
│       │ COBADEFFXXX      [⧉]  │     │
│       └───────────────────────┘     │
│                                     │
│  [▶ Send Money] [⟲ Request] [↓ Stmt]│  ← Tonal/outlined action buttons, label_medium
│                                     │
│  ─────────────────────────────────  │  ← section_divider #E1E4D5
│  Recent Transactions       View All  │  ← title_large #1A1C16 + label_medium #4C662B
│                                     │
│  ┌───────────────────────────────┐  │
│  │ [🛒]  Tesco Supermarket       │  ← shopping_basket #BA1A1A on #CDEDA3 pill
│  │       23 May 2026    -£42.50  │  ← body_small #44483D | body_large #BA1A1A
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ [💳]  Salary Payment          │  ← payments icon #4C662B on #CDEDA3 pill
│  │       22 May 2026  +£3,200.00 │  ← body_large #4C662B
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ [⚡]  EDF Energy              │  ← bolt icon #44483D on #CDEDA3 pill
│  │       20 May 2026    -£94.20  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ [🔄]  Amazon Prime            │  ← subscriptions #4C662B
│  │       18 May 2026     -£8.99  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ [☕]  Costa Coffee            │  ← local_cafe #44483D
│  │       17 May 2026     -£3.75  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│   Home | [Accounts] | Pay | Cards   │  ← Consumer BottomNav; Accounts active (#DCE7C8)
│   | More                            │
└─────────────────────────────────────┘
```

**Layout notes:**
- Hero (`account_header_card`): full-width, `#4C662B` bg, no border radius, 24dp H padding + 20dp top + 32dp bottom.
- Info card: white `#FFFFFF`, 16dp radius, 20dp padding, 20dp H margin, -16dp top margin to overlap hero. Elevation 3. IBAN/BIC rows: label_small caption above monospace value, copy icon right-aligned. `#F9FAEF` hairline divider between rows.
- Action row: 3 equal-flex buttons with 10dp spacing, 20dp H padding. Send Money = tonal `#CDEDA3`/`#4C662B`. Request + Statement = outlined `#4C662B`.
- Transaction rows: white `#FFFFFF`, 12dp radius, 16dp padding, 20dp H margin, 8dp bottom gap, elevation 1. Icon in 44×44dp `#CDEDA3` circle (22dp radius). Amount: body_large/SemiBold; debit = `#BA1A1A`, credit = `#4C662B`.
- Bottom nav: 80dp height, `#F9FAEF` bg, `#C5C8BA` border-top. Accounts tab active with `#DCE7C8` pill.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Account Details                  │
├─────────────────────────────────────┤
│                                     │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │  ← Green hero skeleton (full-width, 160dp)
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│                                     │
│       ┌───────────────────────┐     │
│       │ ░░░░░░  ░░░░░░░░░░░░  │     │  ← Info card skeleton (#E1E4D5, radius 16dp)
│       │ ░░░░░░░░░░░░░░░░░░░░  │     │
│       └───────────────────────┘     │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │  ← Action row skeleton (52dp height)
│                                     │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │  ← Transaction skeleton (64dp height)
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│                                     │
├─────────────────────────────────────┤
│   Home | [Accounts] | Pay | Cards   │
└─────────────────────────────────────┘
```

**Layout notes:** Hero skeleton maintains same `#4C662B` background but content replaced by shimmer. Info card skeleton is `#E1E4D5` with same 16dp radius and -16dp offset. Action row and transaction rows show `#E1E4D5` rounded blocks.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Account Details                  │
├─────────────────────────────────────┤
│                                     │
│              ⚠                      │  ← error_outline, 48dp, #BA1A1A, centred
│                                     │
│        Could not load account       │  ← title_medium, #1A1C16, centred
│   We were unable to retrieve        │  ← body_medium, #44483D, centred
│   account details. Please check     │
│   your connection and try again.    │
│                                     │
│  ┌──────────────────────────────┐   │
│  │           Retry              │   │  ← Filled button #4C662B
│  └──────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│   Home | [Accounts] | Pay | Cards   │
└─────────────────────────────────────┘
```

**Layout notes:** Error content centred. Icon (48dp), title, message, and Retry button in vertical column with 24dp spacing. Bottom nav remains visible.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│ ←  Account Details                  │
├─────────────────────────────────────┤
│                                     │
│           account_balance           │  ← account_balance icon, 48dp, #44483D, centred
│                                     │
│    No account details available     │  ← title_medium, #1A1C16, centred
│   Account information could not be  │  ← body_medium, #44483D, centred
│   found. This account may have been │
│   closed or is no longer accessible.│
│                                     │
│  ┌──────────────────────────────┐   │
│  │       Go to Accounts         │   │  ← Filled button #4C662B
│  └──────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│   Home | [Accounts] | Pay | Cards   │
└─────────────────────────────────────┘
```

**Layout notes:** Empty state centred. "Go to Accounts" button navigates back to accounts list.

---

## Design Checklist (Figma / Stitch)

- [ ] Full-width `#4C662B` hero card, no border radius, 24dp H padding
- [ ] Balance in display_large (57sp/Bold) white on green hero
- [ ] Translucent currency and type badges (`#FFFFFF1A` bg, white label_small text)
- [ ] White elevated info card overlapping hero by 16dp, elevation 3 shadow
- [ ] IBAN and BIC with label_small captions above monospace body_medium values
- [ ] `content_copy` icon (22dp, `#4C662B`) right-aligned on both rows; 48dp tap zone
- [ ] Hairline `#F9FAEF` divider between IBAN and BIC rows
- [ ] Three-button action row: Send Money tonal (`#CDEDA3`/`#4C662B`), Request + Statement outlined
- [ ] Section divider `#E1E4D5` with 20dp H margin
- [ ] "Recent Transactions" title_large (22sp) left + "View All" label_medium (`#4C662B`) right
- [ ] 5 transaction rows: white card, 44×44dp `#CDEDA3` icon circle, merchant name + date, signed amount
- [ ] Debit amounts `#BA1A1A`, credit amounts `#4C662B`
- [ ] A11y-corrected icon colors: bolt + local_cafe use `#44483D` not `#E8A317` on `#CDEDA3`
- [ ] Shimmer loading skeleton for hero, info card, action row, and 1+ transaction rows
- [ ] Consumer bottom nav (5 items), Accounts active with `#DCE7C8` pill
