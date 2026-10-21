# MOCKUP — Login

**Archetype:** form
**Shell:** No top app bar (first-launch screen). No bottom navigation bar.
**Accent:** #4C662B (Earth-green primary). Typography: Outfit. Design system: M3.

---

## Screen: idle (Primary)

```
┌─────────────────────────────────────┐
│                                     │  ← Screen background #F9FAEF
│                                     │
│            ┌──────────┐             │
│            │  [Logo]  │             │  ← Mifos X logo 80×80dp, tint #4C662B
│            └──────────┘             │
│                                     │
│          Welcome Back               │  ← headline_small, #4C662B, centered
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Username                      │  │  ← Outlined input, #C5C8BA border
│  │ Enter your username           │  │    placeholder body_large #44483D
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ Password                   👁 │  │  ← Password input with visibility toggle
│  │ Enter your password           │  │    Focus: #4C662B border
│  └───────────────────────────────┘  │
│                                     │
│  ☐  Keep me signed in               │  ← Checkbox #4C662B + body_medium #1A1C16
│                                     │
│  ┌───────────────────────────────┐  │
│  │           Sign In             │  │  ← Filled button, #4C662B bg, #FFFFFF text
│  └───────────────────────────────┘  │
│                                     │
│  ─────────────  OR  ─────────────   │  ← Dividers #E1E4D5 + label_medium #44483D
│                                     │
│  ┌───────────────────────────────┐  │
│  │ ↗  Sign in with OBP Account   │  │  ← Outlined, #4C662B border/text
│  └───────────────────────────────┘  │
│  Redirects to Open Bank Project for │  ← body_small #44483D centered
│  secure authentication              │
│                                     │
│  ─────────────────────────────────  │  ← Divider #E1E4D5
│                                     │
│         Forgot Password?            │  ← body_medium #386663 centered, 44dp touch
│                                     │
│         Powered by Mifos            │  ← body_medium #4C662B, BOLD (700), centered
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:**
- Screen padding: 24dp (`spacing.lg`) all sides.
- Logo + title: vertically centered in top ~30% of screen. No subtitle.
- Username and password inputs: 56dp height, 4dp radius, 16dp internal padding.
- Remember-me row: 8dp top/bottom padding.
- CTA button: full-width, 40dp height, pill radius (999dp), 24dp top margin.
- OR divider row: 24dp top/bottom padding.
- OAuth button: full-width, same height/radius as CTA.
- Bottom divider + forgot password: 16dp top margin.
- **Footer ("Powered by Mifos"): body_medium, #4C662B, font_weight 700, centered, pinned LAST. 8dp top padding, 32dp bottom padding.**
- Scroll: vertical (SingleChildScrollView) — content may overflow on short screens.

---

## Screen: loading / authenticating

```
┌─────────────────────────────────────┐
│            ┌──────────┐             │
│            │  [Logo]  │             │
│            └──────────┘             │
│          Welcome Back               │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ john.doe                      │  │  ← Fields show current values, disabled
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ ••••••••                   👁 │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │       ◯  Signing in…          │  │  ← CTA shows circular spinner + "Signing in…"
│  └───────────────────────────────┘  │  ← Button muted, inputs disabled
│                                     │
│  ─────────────  OR  ─────────────   │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ ↗  Sign in with OBP Account   │  │  ← Disabled, muted opacity
│  └───────────────────────────────┘  │
│                                     │
│         Powered by Mifos            │  ← body_medium #4C662B, BOLD (700), centered
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Identical layout to idle; CTA button in loading variant. All inputs and OAuth button disabled (muted opacity 0.5). Footer remains pinned at the bottom.

---

## Screen: error

```
┌─────────────────────────────────────┐
│            [Logo]                   │
│          Welcome Back               │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ john.doe                      │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │ ••••••••                   👁 │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ ⚠  Invalid username or        │  │  ← Error banner: #CDEDA3 bg, #BA1A1A border
│  │    password. Please check…    │  │    error_outline 20dp #BA1A1A + body_small #BA1A1A
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │           Sign In             │  │  ← Enabled again for retry
│  └───────────────────────────────┘  │
│  ─────────────  OR  ─────────────   │
│  ┌───────────────────────────────┐  │
│  │ ↗  Sign in with OBP Account   │  │
│  └───────────────────────────────┘  │
│         Forgot Password?            │
│         Powered by Mifos            │  ← body_medium #4C662B, BOLD (700), centered
└─────────────────────────────────────┘
```

**Layout notes:** Error banner appears above the Sign In CTA; inputs re-enabled for retry. Footer remains pinned at the bottom.

---

## Screen: oauth_redirecting

```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│            ┌──────────┐             │
│            │  [Logo]  │             │
│            └──────────┘             │
│                                     │
│   Redirecting to Open Bank Project  │  ← headline_small #1A1C16 centered
│                                     │
│  Opening your browser for secure    │  ← body_medium #44483D centered
│  OAuth authentication…              │
│                                     │
│               ◯                     │  ← Circular indeterminate #4C662B 32dp
│                                     │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Full-screen takeover; column layout vertically centered. Logo + title + message + spinner only — no form, no footer. Browser handles the session.

---

## Screen: oauth_exchanging

```
┌─────────────────────────────────────┐
│                                     │
│            ┌──────────┐             │
│            │  [Logo]  │             │
│            └──────────┘             │
│                                     │
│          Completing Sign In         │  ← headline_small #1A1C16 centered
│                                     │
│  Exchanging authorization code for  │  ← body_medium #44483D centered
│  your session token…                │
│                                     │
│               ◯                     │  ← Circular indeterminate #4C662B 32dp
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Full-screen takeover, vertically centered. Logo + title + message + spinner only — no footer.

---

## Screen: empty

```
┌─────────────────────────────────────┐
│            [Logo]                   │
│          Welcome Back               │
│                                     │
│          ○ (account_circle_off)     │  ← empty state icon 48dp #75796C
│                                     │
│        No accounts found.           │  ← headline_small #1A1C16 centered
│   Contact your bank to set up       │
│   online banking.                   │  ← body_medium #44483D centered
│                                     │
│         Powered by Mifos            │  ← body_medium #4C662B, BOLD (700), centered
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Logo + title + empty-state message + footer. Footer pinned at the bottom.

---

## Design Checklist (Figma / Stitch)

- [ ] No top app bar — full-bleed `#F9FAEF` background
- [ ] Logo: 80×80dp, tint `#4C662B`, center-aligned
- [ ] Headline "Welcome Back": headline_small, `#4C662B`, centered
- [ ] NO subtitle (removed 2026-06-02 design-resync)
- [ ] Username/password inputs: outlined variant, 4dp radius, `#C5C8BA` default border, `#4C662B` focus border
- [ ] Password field: trailing visibility_toggle icon
- [ ] Remember me: M3 checkbox in `#4C662B`
- [ ] Sign In CTA: full-width filled `#4C662B`, pill radius, shows spinner when loading
- [ ] OR divider row: horizontal dividers `#E1E4D5` + "OR" label_medium `#44483D`
- [ ] OAuth button: full-width outlined `#4C662B`, leading open_in_browser icon
- [ ] Error banner: `#CDEDA3` bg, `#BA1A1A` 1dp border, error_outline icon, body_small error text
- [ ] Forgot Password: body_medium `#386663`, 44dp touch target, center-aligned
- [ ] **Footer "Powered by Mifos": body_medium, `#4C662B`, font_weight 700, centered, pinned LAST in every form state**
- [ ] OAuth states: full-screen vertically centered logo + message + circular spinner (no footer)
- [ ] All text Outfit typeface; 24dp screen padding
```
