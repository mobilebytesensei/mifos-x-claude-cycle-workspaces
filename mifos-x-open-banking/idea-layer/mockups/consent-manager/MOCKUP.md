# Mockup — Connected Apps (Consent Manager)

| Field | Value |
|---|---|
| Feature | consent-manager |
| Flavor | consumer |
| Archetype | index_list |
| States | populated, revoke_confirm, empty, error |

---

## State: populated — Three Connected Apps

```
┌──────────────────────────────────────────────┐
│ ←  Connected Apps                        ⓘ  │  ← Top App Bar, `primary` nav+action icons
├──────────────────────────────────────────────┤
│                                              │
│  Connected Apps                              │  ← headlineLarge, `primary`, px spacing.md
│  Manage third-party apps that have           │  ← bodyMedium, `on_surface_variant`
│  access to your account data                 │
│                                              │
│ ┌──────────────────────────────────────────┐ │  ← consent_moneymanager card
│ │ [MM]  MoneyManager Pro          [ACTIVE] │ │    `surface` bg, radius.lg, elevation 2
│ │       Granted 1 Mar 2026 ·               │ │    [MM]: 40×40, `surface_container` bg
│ │       Expires 1 Mar 2027                 │ │    [ACTIVE]: `primary_container` bg
│ │                                          │ │
│ │  [Read Accounts][View Transactions]      │ │  ← scope chips: `secondary` family
│ │  [Check Balances]                        │ │    radius.sm, labelSmall
│ │                                          │ │
│ │                       [Revoke Access ↗]  │ │  ← outlined, `error`, align_end
│ └──────────────────────────────────────────┘ │
│                                              │
│ ┌──────────────────────────────────────────┐ │  ← consent_taxhelper card
│ │ [TH]  TaxHelper           [EXPIRES SOON] │ │    `surface` bg, radius.lg, elevation 2
│ │       Granted 15 Jan 2026 ·              │ │    [TH]: 40×40, `surface_container` bg
│ │       Expires 15 Jan 2027                │ │    badge: `tertiary` family + schedule
│ │                                          │ │
│ │  [View Transactions][Read Accounts]      │ │  ← scope chips: `secondary` family
│ │                                          │ │
│ │              [Reconfirm] [Revoke Access] │ │  ← reconfirm: `primary`; revoke: `error`
│ └──────────────────────────────────────────┘ │
│                                              │
│ ┌──────────────────────────────────────────┐ │  ← consent_budgetwise card (receded)
│ │ [BW]  BudgetWise               [EXPIRED] │ │    `surface_container` bg, elevation 1
│ │       Granted 10 Oct 2025 ·              │ │    [BW]: 40×40, `surface_container` bg
│ │       Expired 10 Apr 2026                │ │    [EXPIRED]: `error` family + error icon
│ │                                          │ │    name text: `on_surface_variant`
│ │  [Check Balances]                        │ │  ← scope chip: neutral, muted
│ │                                          │ │
│ │                              [Remove]    │ │  ← text variant, `on_surface_variant`
│ └──────────────────────────────────────────┘ │
│                                              │
└──────────────────────────────────────────────┘
```

**Layout notes:**
- Cards: margin-x `spacing.md`, margin-bottom `spacing.md` between cards.
- Active cards: `surface` bg, elevation 2, `border.thin` `outline` border.
- Expired card: `surface_container` bg, elevation 1, `border.thin` `outline` border.
- Scope chip row overflows horizontally with scroll on narrow viewports.

---

## State: revoke_confirm — Revoke Confirmation Dialog Overlay

```
┌──────────────────────────────────────────────┐
│ ←  Connected Apps                        ⓘ  │
├──────────────────────────────────────────────┤
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │
│ ▒  Connected Apps                         ▒ │  ← background list still visible,
│ ▒  Manage third-party apps...             ▒ │    dimmed under `scrim`
│ ▒                                         ▒ │
│ ▒ ┌── MoneyManager Pro card (dimmed) ───┐ ▒ │
│ ▒ │  [MM]  MoneyManager Pro  [ACTIVE]  │ ▒ │
│ ▒ │        Granted 1 Mar 2026...       │ ▒ │
│ ▒ └────────────────────────────────────┘ ▒ │
│ ▒                                         ▒ │
│ ▒     ┌──────────────────────────────┐    ▒ │
│ ▒     │                              │    ▒ │  ← revoke_confirm_dialog
│ ▒     │  Revoke access?              │    ▒ │    `surface` bg, radius.xl, elevation 8
│ ▒     │                              │    ▒ │    padding spacing.lg, margin-x spacing.xl
│ ▒     │  This will immediately       │    ▒ │
│ ▒     │  remove this app's access    │    ▒ │
│ ▒     │  to your account data. You   │    ▒ │
│ ▒     │  can reconnect it at any     │    ▒ │
│ ▒     │  time.                       │    ▒ │
│ ▒     │                              │    ▒ │
│ ▒     │          [Cancel]  [Revoke]  │    ▒ │  ← Cancel: text, `primary`
│ ▒     │                              │    ▒ │    Revoke: filled `error` / `on_error`
│ ▒     └──────────────────────────────┘    ▒ │
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │
└──────────────────────────────────────────────┘
```

**Interaction notes:**
- Scrim: `scrim` at 50% over full screen behind dialog.
- "Cancel" fires `dismiss_revoke_dialog` → list returns to `populated`.
- "Revoke" fires `confirm_revoke_consent` → DELETE API call → removes card from list.
- Back gesture = Cancel behaviour.

---

## State: empty — No Connected Apps

```
┌──────────────────────────────────────────────┐
│ ←  Connected Apps                        ⓘ  │
├──────────────────────────────────────────────┤
│                                              │
│  Connected Apps                              │  ← headlineLarge, `primary`
│  Manage third-party apps that have           │  ← bodyMedium, `on_surface_variant`
│  access to your account data                 │
│                                              │
│                                              │
│                                              │
│                  [🔗✕]                       │  ← ic_link_off, 80×80, `outline` tint
│                                              │    (centered)
│            No apps connected                 │  ← titleMedium, `on_surface`, semibold
│                                              │
│   Third-party apps you authorise will        │  ← bodyMedium, `on_surface_variant`,
│   appear here. Visit your bank's app         │    center, px spacing.xl
│   marketplace to connect apps.               │
│                                              │
│                                              │
└──────────────────────────────────────────────┘
```

**Notes:**
- Triggers when `GET /obp/v5.1.0/my/consents` returns an empty `consents` array.
- No action buttons — connecting new apps is handled externally via the bank's marketplace.
- Top app bar info action remains available (PSD2 info sheet).

---

## State: error — Load Failure

```
┌──────────────────────────────────────────────┐
│ ←  Connected Apps                        ⓘ  │
├──────────────────────────────────────────────┤
│                                              │
│  Connected Apps                              │  ← headlineLarge, `primary`
│  Manage third-party apps that have           │  ← bodyMedium, `on_surface_variant`
│  access to your account data                 │
│                                              │
│                                              │
│                                              │
│                  [☁✕]                        │  ← cloud_off icon, centred, `outline`
│                                              │
│       Unable to load connected apps          │  ← error_title, titleMedium, `on_surface`
│                                              │
│     Check your connection and try again      │  ← error_message, bodyMedium,
│                                              │    `on_surface_variant`
│                  [ Try Again ]               │  ← filled, `primary` / `on_primary`
│                                              │
└──────────────────────────────────────────────┘
```

**Notes:**
- Triggers on network timeout or API error (401/403/5xx) from the GET consents call.
- "Try Again" fires `RetryLoad` event in `ConsentManagerViewModel`.
- Generic message is used — no API error codes surfaced to avoid leaking internals.

---

## Permission Badge Reference

Every badge pairs its role with an icon and its text label, so status is never carried by colour alone (WCAG 1.4.1).

| Badge Label | Role | Container / on-container | Icon | Trigger |
|---|---|---|---|---|
| ACTIVE | `primary` | `primary_container` / `on_primary_container` | `check_circle` | consent status = ACCEPTED |
| EXPIRES SOON | `tertiary` | `tertiary_container` / `on_tertiary_container` | `schedule` | ACCEPTED and expiry within 30 days |
| PENDING | `secondary` | `secondary_container` / `on_secondary_container` | `schedule` | consent status = INITIATED |
| EXPIRED | `error` | `error_container` / `on_error_container` | `error` | consent status = EXPIRED |
| REVOKED | `error` | `error_container` / `on_error_container` | `error` | consent status = REVOKED |

## Scope Chip Reference

| Scope Label | Active (ACCEPTED) | Expired/Revoked |
|---|---|---|
| Read Accounts | `secondary_container` bg / `on_secondary_container` text | `surface_container` bg / `on_surface_variant` text |
| View Transactions | `secondary_container` bg / `on_secondary_container` text | `surface_container` bg / `on_surface_variant` text |
| Check Balances | `secondary_container` bg / `on_secondary_container` text | `surface_container` bg / `on_surface_variant` text |

---

## Design Notes

**Status colour follows DESIGN.md's live-vs-gone rule, and this screen is the reason the rule exists.**
- **ACTIVE is `primary`** — the terminal-success role. This palette ships no green, and success maps to the trust-blue.
- **EXPIRES SOON is `tertiary`** — the warning / attention-needed role added in DESIGN.md 1.3.0. A consent expiring in seven days has not failed: the customer still has full access and a working reconfirm path, so the card offers **Reconfirm** alongside Revoke. Dressing that state in error-red would frame a live, healthy connection as broken.
- **EXPIRED and REVOKED are `error`** — access is actually gone. This corrects the previous spec, which rendered EXPIRED in the same amber it used for warnings; "act soon" and "too late" must not share a colour.
- The previous purple scope chips belonged to a palette this system no longer uses. Scopes are neutral facts about what an app can read, not a status, so they take the `secondary` container family and mute to `surface_container` once the consent is dead.

**Visual differentiation — active vs. expired:**
- Active card: `surface` bg, elevation 2, `secondary` scope chips, `primary` ACTIVE badge — visually prominent.
- Expired card: `surface_container` bg, elevation 1, muted scope chips, `error` EXPIRED badge, name text in `on_surface_variant` — visually receded.
- The differential treatment lets users scan instantly to identify live data-access risks. Tone recession carries the "inactive" reading even before the badge is read.

**Revoke vs. Remove actions:**
- "Revoke Access" uses `error` on an outlined button — a deliberate danger signal to prevent accidental taps on a live consent.
- "Remove" for expired consents uses the text variant in `on_surface_variant` — no danger signal, because access is already gone; the action is housekeeping.

**Dialog UX:**
- The confirmation dialog requires an explicit "Revoke" tap. The destructive action is right-aligned per Material 3 convention. Cancel is always the safer default path.

**Accessibility:**
- Each consent card carries a full composite a11y label: app name + grant date + expiry + scopes + status.
- Revoke/Remove buttons describe their target: "Revoke MoneyManager Pro access to your account data."
- Status badges use `role: status` so screen readers announce state changes live.

---

*Generated by /idea export | 2026-08-03*
