# MOCKUP — User Profile

**Archetype:** profile
**Shell:** Top app bar ("Profile", back arrow). No bottom navigation bar.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Profile                          │  ← M3 TopAppBar, back arrow
├─────────────────────────────────────┤
│                                     │
│             ████████                │  ← Avatar skeleton circle, 96dp
│           ████████████              │  ← Display name skeleton
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Personal Information         │  │  ← Form section header (not skeletonised)
│  │                               │  │
│  │  ████████████████████████████ │  │  ← Full name input skeleton
│  │  ████████████████████████████ │  │  ← Email input skeleton
│  │  ████████████████████████████ │  │  ← Phone input skeleton
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Avatar, display name, and all 3 input fields show shimmer skeleton. Section header is visible to orient the user.

---

## Screen: viewing

```
┌─────────────────────────────────────┐
│ ←  Profile                          │
├─────────────────────────────────────┤
│                                     │
│         ┌──────────────┐            │
│         │   [Avatar]   │  ✏        │  ← 96dp circle, #CDEDA3 bg, #4C662B border 2dp
│         └──────────────┘            │  ← ✏ edit_photo icon 28dp, bg #4C662B
│           Maria Santos              │  ← headline_small, #4C662B, centred
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Personal Information         │  │  ← White card, radius 12
│  │                               │  │
│  │  Full Name                    │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  Maria Santos           │  │  │  ← body_large, pre-filled, border #C5C8BA
│  │  └─────────────────────────┘  │  │
│  │                               │  │
│  │  Email Address                │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │ maria.santos@example.com│  │  │  ← pre-filled from OBP
│  │  └─────────────────────────┘  │  │
│  │                               │  │
│  │  Phone Number                 │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  +63 917 123 4567       │  │  │  ← pre-filled
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Save Changes                 │  │  ← Filled button #4C662B, DISABLED (grey)
│  │  Change Password              │  │  ← Outlined button #4C662B
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │           Log Out             │  │  ← Text button, #BA1A1A, full width
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Save Changes button disabled (opacity 38%) — no unsaved changes. All inputs in read-only visual state (border #C5C8BA, bg #F9FAEF).

---

## Screen: editing

```
┌─────────────────────────────────────┐
│ ←  Profile                          │
├─────────────────────────────────────┤
│         [Avatar circle + ✏]         │
│           Maria Santos              │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Personal Information         │  │
│  │                               │  │
│  │  Full Name                    │  │
│  │  ┌─────────────────────────┐  │  │  ← Focused input — border #4C662B
│  │  │  Maria Santos           │  │  │
│  │  └─────────────────────────┘  │  │
│  │                               │  │
│  │  Email Address                │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │ maria.santos@example.com│  │  │
│  │  └─────────────────────────┘  │  │
│  │                               │  │
│  │  Phone Number                 │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  +63 917 123 4567       │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌─────────────────────────────┐    │
│  │        Save Changes         │    │  ← Filled #4C662B, ENABLED
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │       Change Password       │    │  ← Outlined #4C662B
│  └─────────────────────────────┘    │
│                                     │
│  ┌───────────────────────────────┐  │
│  │           Log Out             │  │
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Focused input field shows #4C662B border. Save Changes button fully opaque and tappable.

---

## Screen: saving

```
┌─────────────────────────────────────┐
│ ←  Profile                          │
├─────────────────────────────────────┤
│         [Avatar + ✏]                │
│           Maria Santos              │
│  [form fields — disabled]           │
│                                     │
│  ┌─────────────────────────────┐    │
│  │   ⟳  Saving…               │    │  ← Save button with spinner, disabled
│  └─────────────────────────────┘    │
│  [Change Password — disabled]       │
│  [Log Out — disabled]               │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Save button shows circular progress indicator. All inputs and other buttons disabled during save.

---

## Screen: saved

```
┌─────────────────────────────────────┐
│ ←  Profile                          │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ✓ Your profile has been      │  │  ← #CDEDA3 bg, #4C662B border, check icon
│  │    updated successfully.      │  │  ← body_small, #4C662B
│  └───────────────────────────────┘  │
│                                     │
│         [Avatar + ✏]                │
│           Maria Santos              │
│  [form section]                     │
│  [Save (disabled) + Change Password]│
│  [Log Out]                          │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Success banner appears at top of content area. Auto-transitions to viewing state after 2 seconds. Banner uses role=alert for a11y announcement.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Profile                          │
├─────────────────────────────────────┤
│         [Avatar — error state]      │  ← Avatar shows error banner component
│           [Name skeleton failed]    │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Personal Information         │  │
│  │                               │  │
│  │  [Full Name — empty + error]  │  │  ← Error text below field
│  │  [Email — empty + error]      │  │
│  │  [Phone — empty + error]      │  │
│  └───────────────────────────────┘  │
│                                     │
│  [Save — disabled] [Change Password]│
│  [Log Out]                          │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Per-component error banners show below each failed field. Form remains visible; user may attempt to type manually and retry save.

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar with back navigation only (no actions)
- [ ] 96dp circle avatar with 2dp #4C662B border, #CDEDA3 bg fallback
- [ ] edit_photo icon overlaid — 28dp, bg #4C662B, white icon, offset (+32dp, -16dp)
- [ ] Display name below avatar: headline_small, #4C662B, centred
- [ ] Form card: white (#FFFFFF), radius 12, 24dp padding
- [ ] 3 input fields: bg #F9FAEF, default border #C5C8BA, focused border #4C662B
- [ ] Save Changes: filled #4C662B, full width, radius 8; disabled when no unsaved changes
- [ ] Change Password: outlined #4C662B, full width, radius 8
- [ ] Log Out: text button, #BA1A1A, full width — in separate white card (danger zone)
- [ ] Success banner: #CDEDA3 bg, #4C662B border+icon+text, role=alert
- [ ] Skeleton shimmer on loading for avatar + name + 3 inputs
- [ ] Error state: per-component banners on failed fields
- [ ] All text Outfit typeface; 24dp outer padding
