# MOCKUP — Privacy Policy

**Archetype:** settings
**Shell:** Top app bar ("Privacy Policy", back arrow). No bottom navigation bar.
**Accent:** #4C662B (Earth-green). Typography: Outfit. Design system: M3.

---

## Screen: content

```
┌─────────────────────────────────────┐
│ ←  Privacy Policy                   │  ← M3 TopAppBar, back arrow
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ℹ This policy complies with  │  │  ← #CDEDA3 banner, radius 8
│  │  UK GDPR, DPA 2018, and EU    │  │  ← body_small, #1A1C16
│  │  GDPR (Regulation 2016/679).  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Data We Collect              │  │  ← White card, radius 12; header #4C662B title_medium
│  │  ─────────────────────────── │  │
│  │  We collect the following:    │  │  ← body_medium, #44483D, line_height 1.6
│  │  (a) Identity data — name,    │  │
│  │  date of birth, national ID;  │  │
│  │  (b) Contact data — email,    │  │
│  │  phone; (c) Financial data —  │  │
│  │  accounts, IBAN, transactions;│  │
│  │  (d) Technical data — device, │  │
│  │  crash logs, analytics;       │  │
│  │  (e) Auth data — DirectLogin  │  │
│  │  token (SHA-256, 1hr TTL).    │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Lawful Basis for Processing  │  │  ← White card, radius 12
│  │  ─────────────────────────── │  │
│  │  (a) Contract performance;    │  │
│  │  (b) Legal obligation (AML);  │  │
│  │  (c) Legitimate interests;    │  │
│  │  (d) Consent (marketing).     │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  How We Use Your Data         │  │
│  │  ─────────────────────────── │  │
│  │  Account display, payments,   │  │
│  │  KYC onboarding, fraud        │  │
│  │  detection, push notifications│  │
│  │  (FCM, Android), analytics.   │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Third-Party Data Sharing     │  │
│  │  ─────────────────────────── │  │
│  │  (a) OBP Limited (DPA);       │  │
│  │  (b) KYC providers;           │  │
│  │  (c) Firebase/Google (Android)│  │
│  │  We do NOT sell your data.    │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Data Retention               │  │
│  │  ─────────────────────────── │  │
│  │  Transactions: 7 years (MLR). │  │
│  │  Tokens: 1 hour (not stored). │  │
│  │  Crash logs: 90 days.         │  │
│  │  Profile: 30 days post-delete │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Your Rights Under GDPR       │  │
│  │  ─────────────────────────── │  │
│  │  (a) Access; (b) Rectification│  │
│  │  (c) Erasure; (d) Portability │  │
│  │  (e) Restriction; (f) Object  │  │
│  │  (g) Withdraw consent.        │  │
│  │  Email: privacy@mifos.org.    │  │
│  │  Response within 30 days.     │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Data Controller & DPO        │  │
│  │  ─────────────────────────── │  │
│  │  Controller: Mifos Initiative │  │
│  │  1 World Trade Center, NY.    │  │
│  │  Processor: OBP Limited,      │  │
│  │  11 Leadenhall St, London.    │  │
│  │  DPO: privacy@mifos.org.      │  │
│  │  ICO complaints: ico.org.uk.  │  │
│  └───────────────────────────────┘  │
│                                     │
│  Last updated: 28 May 2026 — v1.0   │  ← body_small, #C5C8BA, centred
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:**
- 24dp horizontal padding throughout.
- GDPR banner: #CDEDA3 bg, radius 8, 16dp padding, 16dp margin-bottom.
- Each section card: white (#FFFFFF), radius 12, 16dp internal padding, 16dp margin-bottom.
- Section headers: Outfit/title_medium, #4C662B, 8dp padding-bottom.
- Section body: Outfit/body_medium, #44483D, line_height 1.6 — multi-line legal prose.
- Last-updated footer: centred, Outfit/body_small, #C5C8BA, 16dp margin-top, 32dp padding-bottom.
- SingleChildScrollView — content overflows on small screens.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Privacy Policy                   │
├─────────────────────────────────────┤
│                                     │
│  ████████████████████████████████   │  ← Banner skeleton
│                                     │
│  ┌───────────────────────────────┐  │
│  │  ████████████████             │  │  ← Card header skeleton
│  │  ██████████████████████████   │  │  ← Body line skeleton ×5
│  │  ████████████████████████     │  │
│  │  ██████████████████████████   │  │
│  │  ████████████████████         │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  ████████████████             │  │
│  │  ████████████████████████     │  │  ← Repeat for 3 more cards
│  └───────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Shimmer animation on all blocks. Cards proportionally match content height. No interactive elements.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Privacy Policy                   │
├─────────────────────────────────────┤
│                                     │
│                                     │
│              📋                     │  ← policy icon, 48dp, #BA1A1A, centred
│                                     │
│   Unable to load Privacy Policy.    │  ← body_medium, centre, #44483D
│  Please check your connection and   │
│         try again.                  │
│                                     │
│         ┌──────────┐                │
│         │  Retry   │                │  ← Outlined button, #4C662B
│         └──────────┘                │
│                                     │
└─────────────────────────────────────┘
```

**Layout notes:** Icon + message + button vertically centred. No cards rendered.

---

## Design Checklist (Figma / Stitch)

- [ ] M3 TopAppBar with back navigation only (no actions)
- [ ] GDPR compliance banner: #CDEDA3 bg, 8dp radius, body_small text
- [ ] 7 section cards: white (#FFFFFF), 12dp radius, 16dp padding
- [ ] All section headers: Outfit/title_medium, #4C662B, 8dp bottom padding
- [ ] All body text: Outfit/body_medium, #44483D, line_height 1.6
- [ ] Last-updated footer: Outfit/body_small, #C5C8BA, centred
- [ ] Loading: full shimmer skeleton matching card proportions
- [ ] Error: policy icon (#BA1A1A) + message + outlined Retry button
- [ ] No bottom navigation bar — back arrow only
- [ ] 24dp horizontal content padding throughout
