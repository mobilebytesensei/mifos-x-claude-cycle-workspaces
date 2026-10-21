# MOCKUP — Settings

**Archetype:** settings
**Shell:** Bottom navigation bar (More tab active). No top app bar.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: content (Preferences loaded)

```
┌─────────────────────────────────────┐
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Appearance                   │  │  ← title_medium, #4C662B
│  │  ─────────────────────────── │  │
│  │  Dark Mode          [○──]    │  │  ← Switch (off) active=#4C662B
│  │  Switch to a darker color     │  │  ← body_small #44483D
│  │  scheme                       │  │
│  │  ─────────────────────────── │  │  ← divider #E1E4D5
│  │  Language     [English  ▾]   │  │  ← combobox, body_medium
│  │  Choose your preferred        │  │  ← body_small #44483D
│  │  display language             │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Notifications                │  │  ← title_medium, #4C662B
│  │  ─────────────────────────── │  │
│  │  Push Notifications [●──]    │  │  ← Switch (on) #4C662B
│  │  Receive alerts and updates   │  │
│  │  from Mifos X                 │  │
│  │  ─────────────────────────── │  │
│  │  Transaction Alerts [●──]    │  │  ← Switch (on) #386663 teal
│  │  Notify me for every debit    │  │
│  │  and credit activity          │  │
│  │  ─────────────────────────── │  │
│  │  Marketing Updates  [○──]    │  │  ← Switch (off) active=#4C662B
│  │  Product news and promotions  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Security                     │  │  ← title_medium, #4C662B
│  │  ─────────────────────────── │  │
│  │  Biometric Login    [○──]    │  │  ← Switch; disabled if no HW
│  │  Use fingerprint or face ID   │  │
│  │  to sign in faster            │  │
│  │  ─────────────────────────── │  │
│  │  Data & Consent            >  │  │  ← chevron #C5C8BA, tappable row
│  │  Manage your data sharing     │  │
│  │  consents                     │  │
│  │  ─────────────────────────── │  │  ← divider #E1E4D5
│  │  Change Password           >  │  │  ← chevron #C5C8BA, tappable row
│  │  Update your account login    │  │
│  │  password                     │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  About                        │  │  ← title_medium, #4C662B
│  │  ─────────────────────────── │  │
│  │  About Mifos X Open Banking > │  │  ← link body_large #1A1C16 + chevron
│  │  ─────────────────────────── │  │
│  │  Terms of Service          >  │  │  ← link + chevron, navigates terms-of-service
│  │  ─────────────────────────── │  │
│  │  Privacy Policy            >  │  │  ← link + chevron, navigates privacy-policy
│  │  ─────────────────────────── │  │
│  │  Open-source Licences      >  │  │  ← link + chevron, navigates licences
│  │  ─────────────────────────── │  │
│  │  App Version         v1.0.0   │  │  ← label #1A1C16 / value #44483D body_small
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│ 🏠 Home  🏦 Accts  📤 Pay  💳 Cards  ··· More │  ← BottomNav, More active #DCE7C8
└─────────────────────────────────────┘
```

**Layout notes:**
- #F9FAEF background throughout.
- 16 dp horizontal padding, 24 dp vertical padding on root column.
- Four white cards (radius 12dp, pad 16dp) with 16dp vertical gap between them.
- Section header (title_medium #4C662B) with 8dp padding-bottom.
- Each toggle row: full-width, space-between, label column left + switch right, 8dp top/bottom padding.
- Dividers: #E1E4D5, 4dp vertical margin above/below.
- Transaction alerts switch uses #386663 (secondary teal) when active; disabled (#C5C8BA) when push is off.
- Biometric toggle disabled on devices without biometric hardware (shown with #C5C8BA inactive tint).

---

## Screen: loading (DataStore hydration)

```
┌─────────────────────────────────────┐
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ████████████  (shimmer)      │  │  ← Appearance header skeleton
│  │  ██████████████████████████   │  │  ← Dark Mode row skeleton
│  │  ██████████████████████████   │  │  ← Language row skeleton
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ████████████  (shimmer)      │  │  ← Notifications header skeleton
│  │  ██████████████████████████   │  │
│  │  ██████████████████████████   │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ████████████  (shimmer)      │  │
│  │  ██████████████████████████   │  │
│  │  ██████████████████████████   │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ████████████  (shimmer)      │  │
│  │  ██████████████████████████   │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│ 🏠 Home  🏦 Accts  📤 Pay  💳 Cards  ··· More │
└─────────────────────────────────────┘
```

**Layout notes:** Shimmer animation applied to all card content. Card outlines visible with shimmer fill matching row proportions. Bottom nav remains visible and interactive.

---

## Design Checklist (Figma / Stitch)

- [ ] No top app bar — Settings is a bottom-nav destination screen
- [ ] Bottom navigation bar with More tab showing active indicator (#DCE7C8 pill)
- [ ] #F9FAEF background behind all four cards
- [ ] Four white ElevatedCard sections (radius 12dp, pad 16dp) — Appearance / Notifications / Security / About
- [ ] Section headers: Outfit title_medium (16sp/500) in #4C662B
- [ ] Each row: body_large label + body_small description left; toggle or chevron right
- [ ] Dark mode + push notifications + biometric switches: active color #4C662B
- [ ] Transaction alerts switch: active color #386663 (secondary teal), disabled when push=off
- [ ] Marketing Updates switch: active color #4C662B, default off
- [ ] Biometric switch: disabled on devices without biometric hardware (grey #C5C8BA)
- [ ] Data & Consent row: trailing chevron_right 20dp #C5C8BA, navigates to consent-manager
- [ ] Change Password row: trailing chevron_right 20dp #C5C8BA, navigates to change-password
- [ ] About link: body_large #1A1C16 + trailing chevron, navigates to about
- [ ] Terms of Service / Privacy Policy / Open-source Licences links: body_large #1A1C16 + chevron, navigate to respective legal screens
- [ ] App Version: "v1.0.0" in body_small #44483D
- [ ] Dividers: #E1E4D5 single-pixel between rows
- [ ] Loading: shimmer blocks matching row dimensions in each card
- [ ] All text Outfit typeface
