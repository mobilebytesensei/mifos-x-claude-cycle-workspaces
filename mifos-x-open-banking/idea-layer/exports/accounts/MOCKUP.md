# MOCKUP — My Accounts

**Archetype:** index_list
**Shell:** Consumer bottom navigation bar (Accounts tab active). No top app bar — screen-level headline replaces it.
**Accent:** #4C662B (Earth-green). Secondary: #386663 (Teal). Typography: Outfit. Design system: M3.

---

## Screen: content

```
┌─────────────────────────────────────┐
│  My Accounts                   [?]  │  ← headline_large (32sp, #1A1C16) + help_outline icon (#44483D)
│                                     │    20dp H pad · 24dp top · 8dp bottom
├─────────────────────────────────────┤
│ ◀ [ALL] [CHECKING] [SAVINGS]       ▶│  ← Horizontal-scroll tab row, 20dp H pad, 16dp V pad
│       [BUSINESS]                    │    ALL: filled #4C662B / white / 20dp radius (selected)
│                                     │    Others: outlined #E1E4D5 / #44483D / 20dp radius
├─────────────────────────────────────┤
│  ┌▌───────────────────────────────┐ │  ← account_card_1 · white #FFFFFF · 16dp radius
│  ▌  Primary Checking  [CHECKING]  │ │    4dp left border #4C662B · elevation 2
│  ▌                                │ │    24dp pad · 20dp H margin · 16dp bottom gap
│  ▌  £4,250.00                     │ │  ← display_small (32sp/600) · color #4C662B
│  ▌                                │ │
│  ▌  🏦 DE89 3704 0044 0532 0130 00│ │  ← account_box icon 16dp #44483D + body_small mono #44483D
│  └────────────────────────────────┘ │
│  ┌▌───────────────────────────────┐ │  ← account_card_2 · 4dp left border #386663
│  ▌  Holiday Savings   [SAVINGS]   │ │    badge text #386663
│  ▌                                │ │
│  ▌  £6,180.50                     │ │  ← display_small (32sp/600) · color #386663
│  ▌                                │ │
│  ▌  🏦 DE89 3704 0044 0532 0131 00│ │
│  └────────────────────────────────┘ │
│  ┌▌───────────────────────────────┐ │  ← account_card_3 · 4dp left border #E8A317 (decorative)
│  ▌  Business Current  [BUSINESS]  │ │    badge: #CDEDA3 bg / text #44483D (A11Y-002 fix)
│  ▌                                │ │
│  ▌  £2,050.00                     │ │  ← display_small (32sp/600) · color #44483D (A11Y-002 fix)
│  ▌                                │ │    (was #E8A317 · 2.17:1 FAIL → #44483D · 8.91:1 PASS)
│  ▌  🏦 DE89 3704 0044 0532 0132 00│ │
│  └────────────────────────────────┘ │
│  ─────────────────────────────────  │  ← footer_divider · #E1E4D5 · 20dp H margin
│  ┌─────────────────────────────┐    │  ← total_balance_footer · #F9FAEF · 12dp radius · 16dp pad
│  │ Total across 3 accounts     │    │    body_medium (14sp) #44483D
│  │                  £12,480.50 │    │    title_large (22sp/700) #4C662B
│  └─────────────────────────────┘    │
│                               [+]   │  ← FAB · add icon · #4C662B fill · 56×56dp
│                                     │    fixed: bottom 80dp, right 20dp · elevation 6
├─────────────────────────────────────┤
│  🏠  [🏦]  ➤  💳  ···              │  ← Consumer BottomNav · Accounts active
│ Home Accts Pay Cards More           │    Active indicator: #DCE7C8 pill · 80dp nav height
└─────────────────────────────────────┘
```

**Layout notes:**
- Header row: `accounts_header` — horizontal stack, space_between. "My Accounts" headline_large left; `help_outline` icon button right (24dp, #44483D, min touch 48dp).
- Filter tabs: `account_type_tabs` — scrollable horizontal row, 8dp spacing, `scroll_indicator: true`. ALL chip: filled `#4C662B` bg / white text / label_medium / 20dp pill radius. Unselected: outlined `#E1E4D5` border / `#44483D` text.
- Account cards: white `#FFFFFF`, 16dp radius, 24dp padding, 20dp horizontal margin, 16dp bottom margin, `elevation: 2`. Left border: 4dp thick, color per account type. Cards are keyboard-focusable and tappable (48dp min).
- Card content: header row (account name title_medium/600 flex-1 + type badge right-aligned); balance display_small; IBAN row (account_box icon 16dp + body_small monospace, 8dp gap).
- Total footer: `#F9FAEF` bg, 12dp radius, 16dp padding, 20dp H margin, 4dp top margin, 80dp bottom margin (clears FAB + nav).
- FAB `add_account_fab`: fixed bottom-right, 56×56dp, `#4C662B` fill, 16dp radius, elevation 6.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│  My Accounts                   [?]  │  ← Header visible (always)
├─────────────────────────────────────┤
│ ◀ [ALL] [CHECKING] [SAVINGS] [BIZ]▶│  ← Filter tabs visible (always)
├─────────────────────────────────────┤
│  ┌────────────────────────────────┐ │  ← skeleton_card_1 · 120dp · #E1E4D5 · 16dp radius
│  │ ░░░░░░░░░░░░░  ░░░░░░░░░░░░░  │ │    shimmer: short4 (200ms) · reduced_motion: static
│  │ ░░░░░░░░░░░░░░░░░░░░          │ │
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │  ← skeleton_card_2 · same spec
│  │ ░░░░░░░░░░░░░  ░░░░░░░░░░░░░  │ │
│  │ ░░░░░░░░░░░░░░░░░░░░          │ │
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │  ← skeleton_card_3 · same spec
│  │ ░░░░░░░░░░░░░  ░░░░░░░░░░░░░  │ │
│  │ ░░░░░░░░░░░░░░░░░░░░          │ │
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │  ← skeleton_total_footer · 48dp · #E1E4D5 · 12dp radius
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │
│  └────────────────────────────────┘ │
├─────────────────────────────────────┤
│  🏠  [🏦]  ➤  💳  ···              │
└─────────────────────────────────────┘
```

**Layout notes:** Header (`accounts_header`) and filter tabs (`account_type_tabs`) always visible. Three skeleton cards replace account cards; skeleton total footer replaces real footer. FAB hidden during load. Shimmer: `motion.duration.short4` (200ms) with `reduced_motion_fallback: static_placeholder`.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│  My Accounts                   [?]  │
├─────────────────────────────────────┤
│ ◀ [ALL] [CHECKING] [SAVINGS] [BIZ]▶│  ← Tabs visible — user can switch filter
├─────────────────────────────────────┤
│                                     │
│         [no_accounts illus]         │  ← empty_state_card illustration
│                                     │
│      No accounts found              │  ← title_medium (16sp/500), #1A1C16, centred
│                                     │
│  You don't have any accounts        │  ← body_medium (14sp), #44483D, centred
│  matching this filter. Try a        │
│  different category or request      │
│  a new account.                     │
│                                     │
│  ┌──────────────────────────────┐   │
│  │      Request Account         │   │  ← filled button #4C662B · on_click: request_new_account
│  └──────────────────────────────┘   │
│                               [+]   │  ← FAB visible
├─────────────────────────────────────┤
│  🏠  [🏦]  ➤  💳  ···              │
└─────────────────────────────────────┘
```

**Layout notes:** Empty card centred in scrollable content area. Filter tabs remain operative so the user can switch category. FAB visible to allow a new account request.

---

## Screen: error

```
┌─────────────────────────────────────┐
│  My Accounts                   [?]  │
├─────────────────────────────────────┤
│ ◀ [ALL] [CHECKING] [SAVINGS] [BIZ]▶│
├─────────────────────────────────────┤
│                                     │
│              ⚠                      │  ← error_outline icon · 48dp · #BA1A1A · centred
│                                     │
│    Could not load accounts          │  ← title_medium (16sp/500), #1A1C16, centred
│                                     │
│  We were unable to fetch your       │  ← body_medium (14sp), #44483D, centred
│  account list. Please check your    │
│  connection and try again.          │
│                                     │
│  ┌──────────────────────────────┐   │
│  │           Retry              │   │  ← filled button #4C662B · on_click: retry_load
│  └──────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│  🏠  [🏦]  ➤  💳  ···              │
└─────────────────────────────────────┘
```

**Layout notes:** Error icon, title, message, and Retry CTA centred vertically in content area. Bottom nav visible. FAB hidden (no account to target).

---

## Design Checklist (Figma / Stitch)

- [ ] "My Accounts" — headline_large (Outfit 32sp/Regular), `#1A1C16`, left-aligned; 20dp H padding, 24dp top padding
- [ ] `help_outline` icon button — 24dp, `#44483D`, right-aligned, min touch 48dp
- [ ] Scrollable filter tab row — 8dp spacing, ALL filled `#4C662B`/white/20dp radius; others outlined `#E1E4D5`/`#44483D`
- [ ] Tab row: `scroll_indicator: true` for overflow
- [ ] Three account cards — `#FFFFFF`, 16dp radius, elevation 2, 24dp padding, 20dp H margin, 16dp bottom gap
- [ ] Card left borders: Checking `#4C662B` · Savings `#386663` · Business `#E8A317` (all 4dp)
- [ ] Type badges: `#CDEDA3` bg, 6dp radius; Checking badge text `#4C662B`, Savings `#386663`, Business `#44483D`
- [ ] **A11Y-002 verified:** Business balance `#44483D` (8.91:1 WCAG AA PASS). Do NOT use `#E8A317` for text.
- [ ] Balance — display_small (32sp/600): Checking `#4C662B`, Savings `#386663`, Business `#44483D`
- [ ] IBAN row — `account_box` icon 16dp `#44483D` + body_small (12sp) monospace `#44483D`, 8dp gap
- [ ] Footer divider — `#E1E4D5`, 20dp H margin
- [ ] Total balance footer — `#F9FAEF` bg, 12dp radius, 16dp pad; label body_medium `#44483D`; amount title_large/700 `#4C662B`
- [ ] FAB — `#4C662B` fill, `add` icon white, 56×56dp, 16dp radius, elevation 6; fixed bottom 80dp right 20dp
- [ ] Loading: 3 skeleton cards 120dp × 16dp radius, 1 skeleton footer 48dp × 12dp radius, all `#E1E4D5`; shimmer short4 (200ms)
- [ ] Empty state: `no_accounts` illustration + "No accounts found" title_medium + body message + "Request Account" CTA
- [ ] Error state: `error_outline` icon 48dp `#BA1A1A` + title + message + "Retry" CTA
- [ ] Consumer bottom nav — 5 tabs, Accounts active with `#DCE7C8` pill indicator, 80dp nav height
- [ ] All text — Outfit typeface. All touch targets ≥ 48dp. 20dp horizontal content padding.
