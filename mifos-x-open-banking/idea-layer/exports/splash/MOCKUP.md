# MOCKUP — Splash Screen

**Archetype:** loading
**Shell:** No top app bar. No bottom navigation bar. Full-screen surface.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: loading (Cold start — session check in progress)

```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│                                     │
│                                     │
│         ┌──────────────┐            │
│         │   [Logo]     │            │  ← splash_logo: mifos_logo asset 120×120 dp
│         │              │            │     tint #4C662B; centered
│         └──────────────┘            │
│                                     │
│     Mifos X Open Banking            │  ← display_small (32sp/SemiBold), #4C662B
│                                     │     padding_top 24dp; centered
│       Banking for Everyone          │  ← body_large (16sp/Regular), #386663
│                                     │     padding_top 8dp; centered
│                                     │
│                                     │
│                                     │
│              (○)                    │  ← circular_indeterminate 40dp, #4C662B
│                                     │     padding_top 32dp; centered
│                                     │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:**
- Full-screen white (#FFFFFF) surface — no top bar, no bottom nav.
- All content vertically + horizontally centred in the viewport (Column with Arrangement.Center + Alignment.CenterHorizontally).
- Logo 120×120 dp with #4C662B tint — earth green brand signal at startup.
- App name: Outfit display_small (32sp SemiBold 600); tagline: Outfit body_large (16sp Regular) in secondary teal #386663.
- Loading indicator: M3 CircularProgressIndicator (indeterminate), 40dp, color #4C662B.
- Reduced-motion fallback: static logo only (no spinner) per WCAG 2.3.3 preference.
- No user-interactive elements on this screen.

---

## Screen: navigating (Session check resolved — transition firing)

```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│                                     │
│         ┌──────────────┐            │
│         │   [Logo]     │            │  ← same as loading state
│         └──────────────┘            │
│                                     │
│     Mifos X Open Banking            │
│                                     │
│       Banking for Everyone          │
│                                     │
│                                     │
│              (○)                    │  ← spinner continues until nav stack replaced
│                                     │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Visual layout identical to loading state. Navigation replaces the back stack — Splash is removed from history. No visible transition from the user's perspective beyond the screen swap.

---

## Design Checklist (Figma / Stitch)

- [ ] Full-screen white surface (#FFFFFF) — no system chrome visible behind content
- [ ] No TopAppBar, no BottomNavigation, no FAB
- [ ] splash_logo: 120×120 dp, tint #4C662B (vector asset, not raster)
- [ ] App name: Outfit display_small (32sp/SemiBold), color #4C662B, horizontally centered
- [ ] Tagline: Outfit body_large (16sp/Regular), color #386663 (secondary teal), centered
- [ ] CircularProgressIndicator: indeterminate, 40dp, color #4C662B
- [ ] Vertical centring: logo + name + tagline + spinner form a tight column centred in the full viewport
- [ ] 24dp gap between logo and app name; 8dp gap between app name and tagline; 32dp gap before spinner
- [ ] Reduced-motion variant: hide spinner, static logo only
- [ ] No state-specific visual changes — loading and navigating states are visually identical
- [ ] All text Outfit typeface
