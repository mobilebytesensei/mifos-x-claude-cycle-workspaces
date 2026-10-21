# MOCKUP — Connected Apps (Consent Manager)

**Archetype:** index_list
**Shell:** Top App Bar — "Connected Apps", back arrow (← → settings), info_outlined action. No bottom nav.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Connected Apps              [ℹ] │  ← TopAppBar: #F9FAEF bg, back + info icons
├─────────────────────────────────────┤
│                                     │
│  Connected Apps                     │  ← headline_large, #4C662B, bold
│  Manage third-party apps that       │  ← body_medium, #44483D
│  have access to your account data   │
│                                     │
│  ████████████████████████████████   │  ← skeleton card 1, 130dp, #E1E4D5, 16dp radius
│  ████████████████████████████████   │     trust_horizon shimmer: #F0F1E6 → #E1E4D5
│  ████████████████████████████████   │     animated at short4 (200ms)
│  ████████████████████████████████   │
│                                     │
│  ████████████████████████████████   │  ← skeleton card 2
│  ████████████████████████████████   │
│  ████████████████████████████████   │
│  ████████████████████████████████   │
│                                     │
│  ████████████████████████████████   │  ← skeleton card 3
│  ████████████████████████████████   │
│  ████████████████████████████████   │
│  ████████████████████████████████   │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Title + subtitle always visible during load. Three skeleton cards 130dp height, 20dp horizontal margin, matching real card position. Shimmer gradient `#F0F1E6 → #E1E4D5` (mood_gradients.trust_horizon). No visible content, no bottom nav.

---

## Screen: populated (3 apps — MoneyManager Pro, TaxHelper, BudgetWise)

```
┌─────────────────────────────────────┐
│ ←  Connected Apps              [ℹ] │  ← TopAppBar, info_outlined → PSD2 info sheet
├─────────────────────────────────────┤
│                                     │
│  Connected Apps                     │  ← headline_large, #4C662B, bold
│  Manage third-party apps that       │  ← body_medium, #44483D
│  have access to your account data   │
│                                     │
│  ┌───────────────────────────────┐  │  ← MoneyManager Pro card: #FFFFFF, 16dp radius
│  │  [MM] MoneyManager Pro [ACTIVE]│ │  ← logo 40dp #DCE7C8 bg · badge #CDEDA3/#4C662B
│  │        Granted 1 Mar 2026      │ │  ← body_small, #44483D
│  │        Expires 1 Mar 2027      │ │
│  │  ─────────────────────────────│ │
│  │  [Read Accounts][View Txns]    │ │  ← scope chips: #CDEDA3 fill, #4C662B text, 8dp radius
│  │  [Check Balances]              │ │     horizontally scrollable row
│  │                  [Revoke ×]   │ │  ← outlined button, border #BA1A1A, text #BA1A1A
│  └───────────────────────────────┘  │     align_self: flex_end, 10dp radius
│                                     │
│  ┌───────────────────────────────┐  │  ← TaxHelper card: #FFFFFF, 16dp radius, 2dp elev
│  │  [TH] TaxHelper        [ACTIVE]│ │  ← logo 40dp #CDEDA3 bg · badge #CDEDA3/#4C662B
│  │        Granted 15 Jan 2026     │ │
│  │        Expires 15 Jan 2027     │ │
│  │  ─────────────────────────────│ │
│  │  [View Transactions]           │ │  ← scope chips
│  │  [Read Accounts]               │ │
│  │                  [Revoke ×]   │ │
│  └───────────────────────────────┘  │
│                                     │
│  ┌ · · · · · · · · · · · · · · ·┐  │  ← BudgetWise card: #F9FAEF fill, 1dp #E1E4D5 border
│  │  [BW] BudgetWise    [EXPIRED] │ │  ← logo 40dp #CDEDA3 bg · badge #CDEDA3/#44483D (muted)
│  │        Granted 10 Oct 2025    │ │     name text: #44483D (muted to signal expiry)
│  │        Expired 10 Apr 2026    │ │
│  │  ─────────────────────────────│ │
│  │  [Check Balances]              │ │  ← scope chip: #F9FAEF fill, #44483D text (expired style)
│  │                    [Remove]   │ │  ← text button, #44483D, align_self: flex_end
│  └ · · · · · · · · · · · · · · ·┘  │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:**
- Screen background `#F9FAEF`. 20dp horizontal margin for all consent cards. 12dp bottom margin between cards.
- Active cards (#FFFFFF fill, 16dp radius, 2dp elevation, 1dp `#F9FAEF` border).
- Expired BudgetWise card: `#F9FAEF` fill, 16dp radius, 1dp elevation, 1dp `#E1E4D5` border — visually demoted. Name colour `#44483D` (not `#1A1C16`) to reinforce expired state.
- ACTIVE badge: `#CDEDA3` fill, `#4C662B` text, 10dp radius, Outfit/label_small, semibold.
- EXPIRED badge: `#CDEDA3` fill, `#44483D` text (A11Y-002 fix — 7.25:1 contrast vs prior #E8A317 at 1.68:1 FAIL), 10dp radius.
- Scope chip row scrolls horizontally when chips exceed screen width. Each chip: `#CDEDA3` fill (active) / `#F9FAEF` fill (expired), 8dp radius, 8dp/4dp padding, Outfit/label_small.
- "Revoke Access" button: outlined, `#BA1A1A` border + text, `align_self: flex_end`, 10dp radius, Outfit/label_medium.
- "Remove" button: text variant, `#44483D` text, `align_self: flex_end`.
- All app logos: 40×40dp, 10dp radius — MoneyManager (`#DCE7C8` bg), TaxHelper + BudgetWise (`#CDEDA3` bg).

---

## Screen: revoke_confirm (Overlay dialog on populated list)

```
┌─────────────────────────────────────┐
│ ←  Connected Apps              [ℹ] │
├─────────────────────────────────────┤
│                                     │
│  [dimmed consent list behind scrim] │  ← populated list, scrim applied (overlay: true)
│                                     │
│    ┌─────────────────────────────┐  │  ← dialog: #FFFFFF, 24dp radius, elevation 8
│    │  Revoke access?             │  │  ← title_large, #1A1C16, bold
│    │                             │  │     24dp/28dp internal padding
│    │  This will immediately      │  │  ← body_medium, #44483D
│    │  remove this app's access   │  │
│    │  to your account data. You  │  │
│    │  can reconnect it at any    │  │
│    │  time.                      │  │
│    │                             │  │
│    │          [Cancel] [Revoke]  │  │  ← Cancel: text button, #4C662B, label_large
│    └─────────────────────────────┘  │     Revoke: filled #BA1A1A, #FFFFFF text, 10dp radius
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:**
- Dialog centred with 32dp horizontal margin. `#FFFFFF` fill, 24dp radius, 8dp elevation.
- Buttons in `Row` with `Arrangement.End` — Cancel (text, `#4C662B`) left of Revoke (filled `#BA1A1A`).
- Escape key shortcut → `dismiss_revoke_dialog` action.
- Background list is visible but muted behind the overlay scrim.

---

## Screen: empty (No connected apps)

```
┌─────────────────────────────────────┐
│ ←  Connected Apps              [ℹ] │
├─────────────────────────────────────┤
│                                     │
│  Connected Apps                     │  ← headline_large, #4C662B, bold
│  Manage third-party apps that       │  ← body_medium, #44483D
│  have access to your account data   │
│                                     │
│                                     │
│              [🔗̸]                    │  ← ic_link_off, 80×80dp, tint #E1E4D5, centered
│                                     │
│         No apps connected           │  ← title_medium, #44483D, semibold, center
│                                     │
│  Third-party apps you authorise     │  ← body_medium, #44483D, center
│  will appear here. Visit your       │     32dp horizontal padding
│  bank's app marketplace to          │
│  connect apps.                      │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Empty state centred in content area below subtitle. Icon 80dp with 16dp bottom padding, title 8dp below icon, body 8dp below title. 32dp horizontal padding on body text. No buttons or CTAs — user navigates to marketplace externally.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Connected Apps              [ℹ] │
├─────────────────────────────────────┤
│                                     │
│  Connected Apps                     │  ← headline_large, #4C662B, bold
│  Manage third-party apps that       │  ← body_medium, #44483D
│  have access to your account data   │
│                                     │
│                                     │
│               ☁✕                    │  ← cloud_off icon, 48dp, #44483D, centered
│                                     │
│   Unable to load connected apps     │  ← body_large, #1A1C16, centered
│   Check your connection and         │  ← body_medium, #44483D, centered
│   try again                         │
│                                     │
│  ┌─────────────────────────────┐    │
│  │           Retry             │    │  ← FilledButton, #4C662B fill, #FFFFFF text
│  └─────────────────────────────┘    │     fires RetryLoad event
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Error icon + messages centred vertically in content area. Retry button: `#4C662B` filled, white text (Outfit/label_large), 20dp horizontal margin, fires `RetryLoad` event.

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar: `#F9FAEF` bg, Title Large (22sp) "Connected Apps", `arrow_back` leading + `info_outlined` trailing
- [ ] Page title: headline_large (Outfit 32sp), `#4C662B`, bold, 16dp horizontal padding
- [ ] Page subtitle: body_medium (Outfit 14sp), `#44483D`, 16dp horizontal + bottom padding
- [ ] Active consent cards: `#FFFFFF` fill, 16dp radius, 2dp elevation, 1dp `#F9FAEF` border, 16dp padding, 20dp horizontal margin
- [ ] Expired BudgetWise card: `#F9FAEF` fill, 16dp radius, 1dp `#E1E4D5` border — visually demoted
- [ ] App logos: 40×40dp, 10dp radius; MoneyManager `#DCE7C8` bg; TaxHelper + BudgetWise `#CDEDA3` bg
- [ ] ACTIVE badge: `#CDEDA3` fill, `#4C662B` text, 10dp radius, Outfit/label_small, semibold
- [ ] EXPIRED badge: `#CDEDA3` fill, `#44483D` text (NOT `#E8A317` — A11Y-002 contrast fix; 7.25:1 WCAG AA pass), 10dp radius
- [ ] Scope chips: `#CDEDA3` fill (active) / `#F9FAEF` (expired), 8dp radius, horizontally scrollable row
- [ ] "Revoke Access" button: outlined, `#BA1A1A` border + text, `align_self: flex_end`, Outfit/label_medium
- [ ] "Remove" button: text variant, `#44483D`, `align_self: flex_end`
- [ ] Revoke confirm dialog: `#FFFFFF`, 24dp radius, 8dp elevation, 32dp horizontal margin; Escape key = dismiss
- [ ] Dialog "Revoke" confirm button: `#BA1A1A` filled, `#FFFFFF` text, 10dp radius
- [ ] Dialog "Cancel" button: text variant, `#4C662B`, Outfit/label_large
- [ ] Loading state: 3× skeleton cards 130dp height, `trust_horizon` shimmer (`#F0F1E6 → #E1E4D5`), 20dp horizontal margin
- [ ] Empty state: `ic_link_off` 80dp tinted `#E1E4D5`, title_medium centered, body_medium centered
- [ ] Error state: `cloud_off` icon 48dp `#44483D` + body_large title + body_medium message + FilledButton Retry
- [ ] All text: Outfit typeface. Min text size 14sp. Touch targets 48dp minimum.
- [ ] 16dp horizontal content padding, 20dp card horizontal margins, 12dp between cards.

---

_Generated by /idea export | 2026-05-30_
