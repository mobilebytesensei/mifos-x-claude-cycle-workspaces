# MOCKUP — Direct Debits

**Archetype:** index_list
**Shell:** Top app bar ("Direct Debits") + back arrow + overflow (more_vert). No bottom navigation bar.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Direct Debits              ⋮     │  ← Top app bar; #1A1C16 title, arrow_back, more_vert
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────┐                   │  ← title_count_row (visible, data-free row)
│  │ Direct Debits│                   │  ← headline_large, #4C662B, bold
│  └──────────────┘                   │
│                                     │
│  ┌──────────────────────────────┐   │  ← Skeleton card 1 (110dp, #E1E4D5, 16dp radius)
│  │ ████████████       ████████  │   │     shimmer, 200ms (short4)
│  │ ██████████████████████████   │   │
│  │ ████████████████████         │   │
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │  ← Skeleton card 2
│  │ ████████████       ████████  │   │
│  │ ██████████████████████████   │   │
│  │ ████████████████████         │   │
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │  ← Skeleton card 3
│  │ ████████████       ████████  │   │
│  │ ██████████████████████████   │   │
│  │ ████████████████████         │   │
│  └──────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Top app bar and "Direct Debits" title always visible during loading. Active count chip suppressed. Three 110dp skeleton cards shimmer with #E1E4D5 fill, 16dp radius. No FAB during loading (initial_state).

---

## Screen: populated

```
┌─────────────────────────────────────┐
│ ←  Direct Debits              ⋮     │  ← Top app bar; more_vert opens options sheet
├─────────────────────────────────────┤
│                                     │
│  Direct Debits   [ 3 active ]       │  ← headline_large #4C662B + chip #CDEDA3/#4C662B label_medium
│                                     │
│  ┌──────────────────────────────┐   │  ← Netflix card: #FFFFFF, 16dp radius, 2dp elev, 20dp h-margin
│  │ Netflix            [Active]  │   │  ← title_medium #1A1C16 + badge #CDEDA3/#4C662B label_small
│  │                              │   │
│  │ £15.99 / month               │   │  ← body_large #4C662B semibold
│  │ Next: 3 Jun 2026             │   │  ← body_small #44483D
│  │ Ref: DD-NF-20240301          │   │  ← label_small #44483D
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │  ← Spotify card: #FFFFFF, same style
│  │ Spotify            [Active]  │   │
│  │                              │   │
│  │ £10.99 / month               │   │
│  │ Next: 12 Jun 2026            │   │
│  │ Ref: DD-SP-20231115          │   │
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │  ← PureGym card: #F9FAEF fill (muted), 0dp elev, #E1E4D5 border
│  │ PureGym         [Cancelled]  │   │  ← title_medium #44483D + badge #F9FAEF/#44483D
│  │                              │   │
│  │ £29.99 / month               │   │  ← body_large #44483D normal weight
│  │ Ref: DD-GYM-20220601         │   │  ← label_small #E1E4D5 (very muted)
│  └──────────────────────────────┘   │
│                                     │
│                      [+ Set Up DD]  │  ← FAB: #4C662B, 16dp radius, add icon, elevation 6dp
└─────────────────────────────────────┘
```

**Layout notes:**
- Title row: "Direct Debits" headline_large #4C662B + "3 active" chip (#CDEDA3 fill, 12dp radius, 10dp h-pad, label_medium semibold).
- Active mandate cards (Netflix, Spotify): #FFFFFF fill, 16dp radius, 2dp elevation, 16dp internal padding, 20dp horizontal screen margin, 12dp bottom margin. Merchant name in title_medium #1A1C16 semibold + green "Active" badge (#CDEDA3/#4C662B). Amount in body_large #4C662B semibold. Next date in body_small #44483D. Mandate ref in label_small #44483D.
- Cancelled mandate card (PureGym): #F9FAEF fill, 16dp radius, 0dp elevation, 1dp #E1E4D5 border. Merchant text #44483D (greyed). "Cancelled" badge has #F9FAEF fill, #44483D text. Amount in body_large #44483D normal. Mandate ref label_small #E1E4D5 (barely visible — historical audit only).
- FAB: "Set Up Direct Debit" floating bottom-right, #4C662B fill, add icon, 16dp radius, 6dp elevation.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│ ←  Direct Debits              ⋮     │
├─────────────────────────────────────┤
│                                     │
│  Direct Debits                      │  ← No chip (no mandates)
│                                     │
│                                     │
│         [account_balance_wallet]    │  ← icon-2xl (48dp), #44483D; empty state illustration
│                                     │
│      No direct debits set up        │  ← title_medium, #1A1C16, center
│                                     │
│  Authorise merchants like Netflix   │
│  or your utility providers to       │  ← body_medium, #44483D, center
│  collect payments automatically     │
│  on agreed dates                    │
│                                     │
│                      [+ Set Up DD]  │  ← FAB always visible
└─────────────────────────────────────┘
```

**Layout notes:** Empty state centred in available space. account_balance_wallet icon 48dp (#44483D). No mandate cards. FAB remains visible as primary entry point for new setup.

---

## Screen: cancel_confirm

```
┌─────────────────────────────────────┐
│ ←  Direct Debits              ⋮     │
├─────────────────────────────────────┤
│                                     │
│  Direct Debits   [ 3 active ]       │
│                                     │
│  ┌──────────────────────────────┐   │  ← Mandate list (blurred/dimmed under overlay)
│  │ Netflix            [Active]  │   │
│  │ £15.99 / month               │   │
│  │ Next: 3 Jun 2026             │   │
│  │ Ref: DD-NF-20240301          │   │
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │ Spotify            [Active]  │   │
│  └──────────────────────────────┘   │
│                                     │
│  ████████████████████████████████   │  ← 50% black overlay scrim
│  ████████████████████████████████   │
│  ┌──────────────────────────────┐   │  ← Dialog: #FFFFFF, 20dp radius, 8dp elevation, 24dp pad
│  │                              │   │
│  │  Cancel Direct Debit?        │   │  ← headline_small #1A1C16 bold
│  │                              │   │
│  │  Netflix (DD-NF-20240301)    │   │  ← body_medium #44483D
│  │  will stop collecting        │   │
│  │  payments. This cannot       │   │
│  │  be undone.                  │   │
│  │                              │   │
│  │  ┌────────────────────────┐  │   │  ← "Yes, Cancel Mandate" filled #BA1A1A/#FFFFFF 12dp radius
│  │  │  Yes, Cancel Mandate   │  │   │
│  │  └────────────────────────┘  │   │
│  │                              │   │
│  │  ┌────────────────────────┐  │   │  ← "Keep Mandate" outlined #4C662B 12dp radius
│  │  │     Keep Mandate       │  │   │
│  │  └────────────────────────┘  │   │
│  └──────────────────────────────┘   │
│                                     │
│                      [+ Set Up DD]  │
└─────────────────────────────────────┘
```

**Layout notes:**
- Overlay scrim: 50% black (`colors.light.scrim` at 0.5 alpha) covers the full screen behind the dialog.
- Dialog: #FFFFFF fill, 20dp radius, 8dp elevation (level4), 24dp padding all sides.
- Dialog title: headline_small (Outfit 24sp/600), #1A1C16 bold.
- Dialog body: body_medium (Outfit 14sp/400), #44483D; merchant name and mandate reference injected from `selectedMandate`.
- "Yes, Cancel Mandate": filled button, #BA1A1A background, #FFFFFF text, 12dp radius, full-width.
- "Keep Mandate": outlined button, #4C662B border + text, 12dp radius, full-width.
- Keyboard shortcut: Escape key dismisses dialog (same as "Keep Mandate").

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Direct Debits              ⋮     │
├─────────────────────────────────────┤
│                                     │
│  Direct Debits                      │  ← Title (no chip during error)
│                                     │
│                                     │
│            [cloud_off]              │  ← icon-2xl (48dp), #44483D
│                                     │
│    Unable to load direct debits     │  ← title_medium #1A1C16 center
│                                     │
│    Check your connection and        │  ← body_medium #44483D center
│    try again                        │
│                                     │
│         [  Retry  ]                 │  ← outlined button #4C662B, 12dp radius
│                                     │
│                      [+ Set Up DD]  │  ← FAB still visible
└─────────────────────────────────────┘
```

**Layout notes:** cloud_off icon 48dp (#44483D) centred. Error title in title_medium #1A1C16. Error body in body_medium #44483D. "Retry" outlined button (#4C662B border + text, 12dp radius) triggers `RetryLoad` event. FAB remains accessible so users can set up mandates without waiting for load — defensive UX.

---

## Design Checklist (Figma / Stitch)

- [ ] Top app bar: "Direct Debits" title_large #1A1C16; `arrow_back` navigation icon; `more_vert` action; no bottom nav
- [ ] Title row: headline_large (Outfit 32sp/400) "Direct Debits" in #4C662B + "3 active" chip (#CDEDA3 fill, 12dp radius, 10dp h-pad, label_medium semibold #4C662B)
- [ ] Active mandate cards: #FFFFFF fill, 16dp radius, 2dp elevation, 16dp pad, 20dp h-margin, 12dp bottom gap
- [ ] Payee names on active cards: title_medium (Outfit 16sp/500) #1A1C16 semibold (Netflix, Spotify)
- [ ] "Active" badge: #CDEDA3 fill, 10dp radius, 8dp h-pad; label_small (11sp/500) #4C662B
- [ ] Mandate amounts on active cards: body_large (16sp/400) #4C662B semibold — e.g. "£15.99 / month"
- [ ] Next collection date: body_small (12sp/400) #44483D — e.g. "Next: 3 Jun 2026"
- [ ] Mandate reference: label_small (11sp/500) #44483D — e.g. "Ref: DD-NF-20240301"
- [ ] Cancelled mandate card (PureGym): #F9FAEF fill, 0dp elevation, 1dp #E1E4D5 border
- [ ] Cancelled payee name: title_medium #44483D (greyed, NOT #1A1C16)
- [ ] "Cancelled" badge: #F9FAEF fill, 10dp radius; label_small #44483D
- [ ] Cancelled amount: body_large #44483D normal weight (NOT semibold, NOT #4C662B)
- [ ] Cancelled mandate ref: label_small #E1E4D5 (barely visible — intentional)
- [ ] FAB: "Set Up Direct Debit" #4C662B fill, 16dp radius, add icon, 6dp elevation — always floating bottom-right
- [ ] Cancel dialog: #FFFFFF fill, 20dp (xl) radius, 8dp elevation, 24dp all-sides padding
- [ ] Dialog title: headline_small (24sp/600) #1A1C16 bold — "Cancel Direct Debit?"
- [ ] Dialog body: body_medium (14sp/400) #44483D — merchant + mandate ref injected dynamically
- [ ] "Yes, Cancel Mandate": filled #BA1A1A bg / #FFFFFF text, 12dp radius, full-width; destructive red
- [ ] "Keep Mandate": outlined #4C662B border + text, 12dp radius, full-width; safe secondary
- [ ] Overlay scrim: 50% black behind dialog in cancel_confirm state
- [ ] Loading skeletons: 3 cards × 110dp, #E1E4D5 fill, 16dp radius; shimmer 200ms (short4); reduced-motion fallback → static placeholder
- [ ] Empty state: account_balance_wallet icon 48dp #44483D; title_medium centre; body_medium #44483D help copy
- [ ] Error state: cloud_off icon 48dp #44483D; title_medium centre; "Retry" outlined #4C662B button
- [ ] All typography: Outfit typeface. Touch targets ≥ 48dp. Content padding 20dp horizontal.

---

_Generated by /idea export | 2026-05-30_
