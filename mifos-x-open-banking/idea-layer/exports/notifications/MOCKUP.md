# MOCKUP — Notifications

**Archetype:** index_list
**Shell:** Top app bar ("Notifications", back arrow, done_all + tune actions). No bottom navigation bar.
**Accent:** #4C662B (Earth-green primary). Typography: Outfit. Design system: M3.

---

## Screen: loading

```
┌─────────────────────────────────────────┐
│ ←  Notifications               ✓  ⚙    │  ← Top app bar: arrow_back / done_all / tune
├─────────────────────────────────────────┤
│                                         │
│  Notifications                          │  ← headline_large, #4C662B, bold (visible during load)
│                                         │
│  ████████████████████████████████████   │  ← Skeleton card 1 (#E1E4D5, 16dp radius, 72dp)
│  ████████████████████████████████████   │
│                                         │
│  ████████████████████████████████████   │  ← Skeleton card 2
│  ████████████████████████████████████   │
│                                         │
│  ████████████████████████████████████   │  ← Skeleton card 3
│  ████████████████████████████████████   │
│                                         │
│  ████████████████████████████████████   │  ← Skeleton card 4
│  ████████████████████████████████████   │
│                                         │
└─────────────────────────────────────────┘
```

**Layout notes:** Screen title "Notifications" remains visible (headline_large, #4C662B). Four skeleton cards shimmer at short4 duration (200ms) with #E1E4D5 fill, 16dp radius. "Mark All Read" button and section labels are hidden during loading. Reduced-motion fallback: static_placeholder (no shimmer animation).

---

## Screen: populated

```
┌─────────────────────────────────────────┐
│ ←  Notifications               ✓  ⚙    │  ← done_all = mark_all_read; tune = settings
├─────────────────────────────────────────┤
│                                         │
│  Notifications          Mark All Read   │  ← headline_large #4C662B + label_medium #386663 btn
│                                         │
│  Today                                  │  ← label_medium, #44483D, semibold; 16dp h-pad
│                                         │
│  ┌──────────────────────────────────┐   │  ← Unread card: #CDEDA3 fill, 16dp radius
│  │  ●──────────────────────────  ·  │   │  ← unread_dot (#4C662B 10dp circle, top-right)
│  │  ╔════╗  Payment received         │   │
│  │  ║ ↓  ║  Payment of £50.00       │   │  ← icon: arrow_downward, 22dp, #FFFFFF on #4C662B 44dp circle
│  │  ╚════╝  received from           │   │  ← body_medium #1A1C16 semibold + body_small #44483D
│  │           James Wilson           │   │
│  │           10 min ago             │   │  ← label_small, #44483D
│  └──────────────────────────────────┘   │
│                                         │
│  ┌──────────────────────────────────┐   │  ← Unread card: #CDEDA3 fill, 16dp radius
│  │  ●──────────────────────────  ·  │   │
│  │  ╔════╗  KYC verification         │   │
│  │  ║ ✓  ║  approved                 │   │  ← icon: verified_user, 22dp, #FFFFFF on #4C662B circle
│  │  ╚════╝  Your identity has been   │   │  ← body_medium #1A1C16 semibold
│  │           verified. Full access   │   │  ← body_small #44483D (truncates if >2 lines)
│  │           to all features.        │   │
│  │           1 hr ago                │   │  ← label_small, #44483D
│  └──────────────────────────────────┘   │
│                                         │
│  Earlier                                │  ← label_medium, #44483D, semibold; 16dp h-pad
│                                         │
│  ┌──────────────────────────────────┐   │  ← Read card: #FFFFFF fill, 16dp radius, #F9FAEF border
│  │  ╔════╗  Direct debit mandate     │   │
│  │  ║ ↻  ║  created                  │   │  ← icon: autorenew, 22dp, #FFFFFF on #386663 circle
│  │  ╚════╝  Direct debit for Netflix │   │  ← body_medium #44483D semibold (read → on_surface_variant)
│  │           — £15.99/month from     │   │  ← body_small #44483D
│  │           Current Account.        │   │
│  │           3 hr ago                │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ┌──────────────────────────────────┐   │  ← Read card: #FFFFFF fill, 16dp radius, #F9FAEF border
│  │  ╔════╗  Salary credited          │   │
│  │  ║ ↓  ║                           │   │  ← icon: arrow_downward, 22dp, #FFFFFF on #4C662B circle
│  │  ╚════╝  £3,200.00 from Acme Ltd  │   │  ← body_medium #44483D semibold
│  │           has been credited to    │   │  ← body_small #44483D
│  │           your Current Account.   │   │
│  │           Yesterday               │   │  ← label_small, #44483D
│  └──────────────────────────────────┘   │
│                                         │  ← bottom_spacer 24dp
└─────────────────────────────────────────┘
```

**Layout notes:**
- Unread cards (#CDEDA3 fill): notification_payment_james + notification_kyc_approved. Unread dot is a 10×10dp #4C662B circle, align_self: flex_start, 4dp top margin — appears at right edge of the card row.
- Read cards (#FFFFFF fill): notification_netflix_mandate + notification_salary_credited. Border: 1dp #F9FAEF. No unread dot.
- Icon containers: 44×44dp circles. Payment / KYC / Salary = #4C662B fill. Netflix mandate = #386663 fill (secondary colour, visually distinguishes system category).
- All icon glyphs: 22dp, #FFFFFF.
- Each card: 16dp corner radius, 16dp horizontal + 14dp vertical inner padding, 20dp horizontal margin, 8dp bottom margin.
- "Mark All Read" text button: label_medium, #386663, right-aligned, no horizontal padding.
- Cards are tappable (focusable: true, keyboard navigable): payment → transaction-detail, KYC → profile, Netflix → accounts, Salary → transaction-detail.
- The tap target is the card itself. The row, icon background, icon, text column and unread dot nested inside it are presentational — they carry no click handler and are not separately focusable, so the whole card reads as one control.

---

## Screen: empty

```
┌─────────────────────────────────────────┐
│ ←  Notifications               ✓  ⚙    │
├─────────────────────────────────────────┤
│                                         │
│  Notifications                          │  ← headline_large, #4C662B
│                                         │
│                                         │
│              🔔                         │  ← notifications_none_outlined icon, 48dp, #44483D
│                                         │
│         You're all caught up            │  ← title_medium, #1A1C16, center-aligned
│                                         │
│   No new notifications. We'll let       │  ← body_medium, #44483D, center, max 2 lines
│   you know about payments, alerts       │
│   and updates.                          │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

**Layout notes:** Title remains visible. Empty state centred vertically in remaining screen space. No "Mark All Read" button (nothing to mark). No section labels.

---

## Screen: error

```
┌─────────────────────────────────────────┐
│ ←  Notifications               ✓  ⚙    │
├─────────────────────────────────────────┤
│                                         │
│  Notifications                          │  ← headline_large, #4C662B
│                                         │
│                                         │
│              ☁                          │  ← cloud_off icon, 48dp, #44483D
│                                         │
│     Unable to load notifications        │  ← title_medium, #1A1C16, center-aligned
│                                         │
│   Check your connection and try again   │  ← body_medium, #44483D, center
│                                         │
│         ┌──────────────────┐            │
│         │      Retry       │            │  ← outlined button, #4C662B; triggers RetryLoad event
│         └──────────────────┘            │
│                                         │
└─────────────────────────────────────────┘
```

**Layout notes:** Retry button triggers `RetryLoad` event → `NotificationsViewModel` re-fetches notification list and re-calls `SignalRepository`. Error state persists until a successful load completes.

---

## Design Checklist (Figma / Stitch)

- [ ] Top app bar: #F9FAEF background, 56dp height, "Notifications" Title Large (22sp/Regular) — NOT the in-screen headline_large title (both coexist)
- [ ] Top app bar navigation icon: arrow_back, 24dp, #1A1C16; action 1: done_all; action 2: tune
- [ ] In-screen title "Notifications": headline_large (Outfit 32sp/400, bold override), #4C662B
- [ ] "Mark All Read" text button: label_medium (Outfit 12sp/500), #386663; right-aligned; no extra horizontal padding
- [ ] Section labels "Today" / "Earlier": label_medium (Outfit 12sp/500), #44483D, semibold; 16dp h-pad
- [ ] Unread notification cards: #CDEDA3 fill, 16dp radius, 16×14dp padding, 20dp h-margin, 8dp bottom gap
- [ ] Read notification cards: #FFFFFF fill, 16dp radius, 1dp #F9FAEF border; same padding/margin as unread
- [ ] Icon containers: 44×44dp circle; payment/security/salary = #4C662B; system (mandate) = #386663
- [ ] All icon glyphs inside containers: 22dp, #FFFFFF
- [ ] Unread indicator dot: 10×10dp circle, #4C662B, align_self: flex_start, 4dp top margin
- [ ] Notification item title (unread): body_medium (Outfit 14sp/400), #1A1C16, semibold weight
- [ ] Notification item title (read): body_medium (Outfit 14sp/400), #44483D, semibold weight
- [ ] Notification body message: body_small (Outfit 12sp/400), #44483D, xs top+bottom padding
- [ ] Relative timestamp: label_small (Outfit 11sp/500), #44483D
- [ ] Loading skeleton: 4 cards, #E1E4D5 fill, 16dp radius; shimmer short4 (200ms); static fallback for reduced-motion
- [ ] Empty state: notifications_none_outlined icon 48dp #44483D; "You're all caught up" (title_medium, #1A1C16); message body_medium #44483D; centred
- [ ] Error state: cloud_off icon 48dp #44483D; "Unable to load notifications" (title_medium, #1A1C16); "Retry" outlined button #4C662B
- [ ] All interactive cards: focusable, keyboard navigable (Enter/Space triggers on_click)
- [ ] Bottom spacer: 24dp — prevents last card clipping at scroll end
- [ ] All text: Outfit typeface. Touch targets 48dp minimum. 16dp horizontal content padding.

---

_Generated by /idea export | 2026-05-30_
