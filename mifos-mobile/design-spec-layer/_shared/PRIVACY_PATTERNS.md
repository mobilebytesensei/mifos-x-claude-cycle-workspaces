# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/design-spec-layer/_shared/PRIVACY_PATTERNS.md"
# last_modified: "2026-03-19"

# Privacy Patterns - mifos-mobile

> **Purpose**: Comprehensive guide for handling sensitive data in UI, including masking, blur effects, and peek interactions.
> **Last Updated**: 2026-03-19
> **Principle**: Protect user data by default, reveal on explicit intent

---

## 1. Privacy States Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              PRIVACY STATE MACHINE                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│                              ┌─────────────┐                                            │
│                              │   MASKED    │ ◄─── Default state                        │
│                              │   (Hidden)  │      Data protected                        │
│                              └──────┬──────┘                                            │
│                                     │                                                    │
│               ┌─────────────────────┼─────────────────────┐                            │
│               │                     │                     │                            │
│          Tap toggle            Long press            Biometric                         │
│               │                     │                     │                            │
│               ▼                     ▼                     ▼                            │
│        ┌───────────┐         ┌───────────┐         ┌───────────┐                       │
│        │  REVEALED │         │   PEEK    │         │  TRUSTED  │                       │
│        │ (Toggle)  │         │ (Temp)    │         │ (Session) │                       │
│        └─────┬─────┘         └─────┬─────┘         └─────┬─────┘                       │
│              │                     │                     │                            │
│         Tap again              Release              Timeout/Lock                       │
│              │                     │                     │                            │
│              └─────────────────────┴─────────────────────┘                            │
│                                    │                                                    │
│                                    ▼                                                    │
│                              ┌─────────────┐                                            │
│                              │   MASKED    │                                            │
│                              └─────────────┘                                            │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Sensitive Data Categories

| Category | Examples | Default State | Reveal Method |
|----------|----------|---------------|---------------|
| **Financial** | Balance, amounts, transactions | Fully masked | Peek or toggle |
| **Identity** | SSN, passport, ID numbers | Partially masked | Biometric |
| **Payment** | Card numbers, CVV, expiry | Partially masked | Peek |
| **Contact** | Phone, email, address | Partially masked | Toggle |
| **Health** | Medical records, conditions | Fully masked | Biometric |
| **Authentication** | Passwords, PINs, tokens | Always masked | Never reveal in UI |

---

## 3. Masking Techniques

### 3.1 Character Masking

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CHARACTER MASKING PATTERNS                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  FULL MASK (High sensitivity)                                                │
│  ────────────────────────────────────────────────────────────────────────   │
│  Actual:    $12,345.67                                                       │
│  Masked:    $••,•••.••                                                       │
│  Use for:   Balances, full amounts                                           │
│                                                                              │
│  PARTIAL MASK - LAST 4 (Medium sensitivity)                                  │
│  ────────────────────────────────────────────────────────────────────────   │
│  Actual:    4532 1234 5678 9012                                              │
│  Masked:    •••• •••• •••• 9012                                              │
│  Use for:   Card numbers, account numbers                                    │
│                                                                              │
│  PARTIAL MASK - FIRST/LAST (Medium sensitivity)                              │
│  ────────────────────────────────────────────────────────────────────────   │
│  Actual:    john.doe@example.com                                             │
│  Masked:    j•••••e@example.com                                              │
│  Use for:   Email addresses                                                  │
│                                                                              │
│  PARTIAL MASK - MIDDLE (Low sensitivity)                                     │
│  ────────────────────────────────────────────────────────────────────────   │
│  Actual:    +1 (555) 123-4567                                                │
│  Masked:    +1 (•••) •••-4567                                                │
│  Use for:   Phone numbers                                                    │
│                                                                              │
│  FORMAT PRESERVED (All categories)                                           │
│  ────────────────────────────────────────────────────────────────────────   │
│  Actual:    123-45-6789 (SSN)                                                │
│  Masked:    •••-••-6789                                                      │
│  Rule:      Keep separators, spacing, and last meaningful digits             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Mask Character Guidelines

| Character | Usage | Accessibility |
|-----------|-------|---------------|
| `•` (bullet) | Primary mask character | "Masked content" for screen readers |
| `*` (asterisk) | Legacy/ASCII fallback | Same as bullet |
| `X` | Document redaction style | Avoid for digital |

---

## 4. Blur Overlay

### Visual Specification

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BLUR OVERLAY SPECIFICATION                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LIGHT MODE:                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  ╔═══════════════════════════════════════════════════════════════╗  │    │
│  │  ║  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ║  │    │
│  │  ║  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ║  │    │
│  │  ║  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  ║  │    │
│  │  ╚═══════════════════════════════════════════════════════════════╝  │    │
│  │                                                                     │    │
│  │                    [👁 Tap to reveal]                               │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Blur Parameters:                                                            │
│  ├─ Radius: 16px (Gaussian)                                                 │
│  ├─ Saturation: 0.8 (slightly desaturated)                                  │
│  └─ Background: surfaceVariant @ 90% over blur                              │
│                                                                              │
│  DARK MODE:                                                                  │
│  ├─ Radius: 20px (slightly more for dark backgrounds)                       │
│  ├─ Saturation: 0.7                                                         │
│  └─ Background: surfaceVariant @ 85% over blur                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Blur Animation

```
REVEAL ANIMATION (300ms):
├─ Blur radius: 16px → 0px
├─ Opacity: 0.9 → 0
└─ Scale: 1.0 → 1.0 (no scale change)

HIDE ANIMATION (250ms):
├─ Blur radius: 0px → 16px
├─ Opacity: 0 → 0.9
└─ Scale: 1.0 → 1.0
```

---

## 5. Eye Toggle Component

### Visual States

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  EYE TOGGLE COMPONENT                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  HIDDEN STATE (Default):                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  $••,•••.••                                          [👁]           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Icon: visibility_off (eye with line through)                               │
│  Color: onSurfaceVariant                                                    │
│  Size: 24x24dp                                                              │
│  Touch target: 48x48dp                                                      │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  REVEALED STATE:                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  $12,345.67                                          [👁]           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Icon: visibility (eye open)                                                │
│  Color: primary                                                             │
│  Size: 24x24dp                                                              │
│  Touch target: 48x48dp                                                      │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  PEEK STATE (While long pressing):                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  $12,345.67                                          [👁 ━━━━░░]   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Icon: visibility (eye open) with timeout indicator                         │
│  Progress ring around icon shows time remaining                             │
│  Auto-hides after 10 seconds                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Interaction Patterns

| Gesture | Action | Use Case |
|---------|--------|----------|
| **Tap** | Toggle visibility | When user wants persistent view |
| **Long press** | Peek (temporary) | Quick glance without committing |
| **Double tap** | Copy to clipboard | Quick copy masked value (shows toast) |

---

## 6. Peek Micro-Interaction

### Detailed Timeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PEEK INTERACTION TIMELINE                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Time: 0ms ──────────────────────────────────────────────────────── 10s     │
│        │                                                              │      │
│  0ms   │ Long press detected                                          │      │
│        │ ├─ Haptic: Light impact                                      │      │
│        │ └─ Start timeout countdown                                   │      │
│        │                                                              │      │
│  150ms │ Reveal animation starts                                      │      │
│        │ ├─ Mask fades out (150ms)                                   │      │
│        │ ├─ Value fades in (150ms)                                   │      │
│        │ └─ Eye icon shows progress ring                             │      │
│        │                                                              │      │
│  300ms │ Reveal complete                                              │      │
│        │ └─ Data fully visible                                       │      │
│        │                                                              │      │
│  5s    │ Warning (if still peeking)                                  │      │
│        │ ├─ Haptic: Light pulse                                      │      │
│        │ └─ Progress ring turns warning color                        │      │
│        │                                                              │      │
│  8s    │ Final warning                                                │      │
│        │ ├─ Progress ring turns error color                          │      │
│        │ └─ Haptic: Double pulse                                     │      │
│        │                                                              │      │
│  10s   │ Auto-hide (even if still pressing)                          │      │
│        │ ├─ Security timeout                                         │      │
│        │ └─ Require new gesture to peek again                        │      │
│        │                                                              │      │
│  RELEASE (any time):                                                         │
│        │ ├─ Haptic: Light impact                                     │      │
│        │ ├─ Hide animation (150ms)                                   │      │
│        │ └─ Return to masked state                                   │      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Peek Progress Indicator

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PROGRESS RING AROUND EYE ICON                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  0-5 seconds: Primary color                                                  │
│  ┌─────┐                                                                    │
│  │ ╭─╮ │  Progress: 100% → 50%                                              │
│  │ │👁│ │  Ring depletes clockwise                                          │
│  │ ╰─╯ │                                                                    │
│  └─────┘                                                                    │
│                                                                              │
│  5-8 seconds: Warning color (#F57C00)                                        │
│  ┌─────┐                                                                    │
│  │ ╭─╮ │  Progress: 50% → 20%                                               │
│  │ │👁│ │  Visual urgency increases                                         │
│  │ ╰─╯ │                                                                    │
│  └─────┘                                                                    │
│                                                                              │
│  8-10 seconds: Error color (#F44336)                                         │
│  ┌─────┐                                                                    │
│  │ ╭─╮ │  Progress: 20% → 0%                                                │
│  │ │👁│ │  Final warning before auto-hide                                   │
│  │ ╰─╯ │                                                                    │
│  └─────┘                                                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Privacy-Aware Input Fields

### Password Field

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PASSWORD INPUT FIELD                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  MASKED (Default):                                                           │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Password                                                           │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │  ••••••••••••                                       [👁]    │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  │  8-16 characters, mix of letters and numbers                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  REVEALED (While holding eye):                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Password                                                           │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │  MyP@ssw0rd123                                      [👁━━]  │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  │  ✓ Strength: Strong                                                 │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Security Rules:                                                             │
│  ├─ Never show password on focus loss                                       │
│  ├─ Auto-hide after 3 seconds (shorter than general peek)                   │
│  ├─ No clipboard copy allowed                                               │
│  └─ Clear on background (configurable)                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Sensitive Number Input (PIN, OTP)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PIN/OTP INPUT                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ENTERING (Each digit briefly visible):                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │      ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐                     │    │
│  │      │ • │  │ • │  │ • │  │ 7 │  │   │  │   │                     │    │
│  │      └───┘  └───┘  └───┘  └───┘  └───┘  └───┘                     │    │
│  │                          ↑                                         │    │
│  │                   Current digit (500ms visible)                    │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  COMPLETE (All masked):                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │      ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐                     │    │
│  │      │ • │  │ • │  │ • │  │ • │  │ • │  │ • │                     │    │
│  │      └───┘  └───┘  └───┘  └───┘  └───┘  └───┘                     │    │
│  │                                                                     │    │
│  │                    Auto-submit on completion                       │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Behavior:                                                                   │
│  ├─ Show digit for 500ms, then mask                                         │
│  ├─ Haptic on each digit entry                                              │
│  ├─ Shake animation on error                                                │
│  └─ Auto-submit when all digits entered                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Privacy Screen (App Backgrounded)

### Implementation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PRIVACY SCREEN ON BACKGROUND                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  When app enters background (multitasking view):                             │
│                                                                              │
│  BEFORE (Visible in task switcher - BAD):                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │   Balance: $12,345.67                                               │    │
│  │   Card: 4532 •••• •••• 9012                                        │    │
│  │   Recent: $500 to John...                                          │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  AFTER (Privacy screen shown - GOOD):                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                                                                     │    │
│  │                                                                     │    │
│  │                         [App Logo]                                  │    │
│  │                                                                     │    │
│  │                       {{APP_NAME}}                                  │    │
│  │                                                                     │    │
│  │                                                                     │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Implementation:                                                             │
│  ├─ iOS: applicationWillResignActive → show privacy view                    │
│  ├─ Android: FLAG_SECURE on sensitive activities                            │
│  └─ Flutter/KMP: Platform-specific implementation                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Biometric Protection

### When to Require Biometric

| Data Type | View | Copy | Edit |
|-----------|:----:|:----:|:----:|
| Balance/Amounts | Optional | No copy | N/A |
| Full card number | Required | Blocked | N/A |
| CVV | Required | Blocked | N/A |
| SSN | Required | Required | Required |
| Medical data | Required | Required | Required |
| Passwords | N/A | Blocked | Required |

### Biometric Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BIOMETRIC REVEAL FLOW                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. User taps reveal on protected data                                       │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │  SSN: •••-••-6789                              [🔒 Reveal]      │     │
│     └─────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│  2. System shows biometric prompt                                            │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │                                                                 │     │
│     │                      [Fingerprint Icon]                         │     │
│     │                                                                 │     │
│     │              Verify your identity to view                       │     │
│     │                    sensitive data                               │     │
│     │                                                                 │     │
│     │                     [Use PIN instead]                           │     │
│     │                        [Cancel]                                 │     │
│     │                                                                 │     │
│     └─────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│  3. On success, reveal with time limit                                       │
│     ┌─────────────────────────────────────────────────────────────────┐     │
│     │  SSN: 123-45-6789                              [🔓 30s]         │     │
│     └─────────────────────────────────────────────────────────────────┘     │
│                                                                              │
│  4. Auto-hide after timeout                                                  │
│     └─ Return to masked state                                               │
│     └─ Require new biometric for subsequent views                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Copy Protection

### Secure Copy Behavior

| Data Type | Copy Allowed | Clipboard Duration | Notification |
|-----------|:------------:|:------------------:|:------------:|
| Masked data | Blocked | N/A | Toast: "Copy not available" |
| Revealed balance | Yes | 60s | Toast: "Copied, clears in 60s" |
| Card number | Blocked | N/A | Toast: "Cannot copy card number" |
| CVV | Blocked | N/A | N/A |
| Account number | Yes | 30s | Toast: "Copied, clears in 30s" |
| Email/Phone | Yes | 120s | Toast: "Copied" |

### Implementation

```kotlin
// Android - Secure clipboard with auto-clear
fun copyWithAutoClear(context: Context, text: String, label: String, clearAfterMs: Long) {
    val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
    val clip = ClipData.newPlainText(label, text)
    clipboard.setPrimaryClip(clip)

    // Schedule clipboard clear
    Handler(Looper.getMainLooper()).postDelayed({
        if (clipboard.hasPrimaryClip() &&
            clipboard.primaryClip?.getItemAt(0)?.text == text) {
            clipboard.setPrimaryClip(ClipData.newPlainText("", ""))
        }
    }, clearAfterMs)
}
```

---

## 11. Screen Recording Protection

### Sensitive Screens

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SCREEN RECORDING PROTECTION                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Protected Screens (show blank in recordings):                               │
│  ├─ Account balance screen                                                  │
│  ├─ Transaction details                                                     │
│  ├─ Card details screen                                                     │
│  ├─ Profile with sensitive data                                             │
│  └─ Any screen with revealed sensitive data                                 │
│                                                                              │
│  Implementation:                                                             │
│  ├─ Android: FLAG_SECURE on Activity/Window                                 │
│  ├─ iOS: Detect screen recording, show privacy overlay                      │
│  └─ Show user notification when recording detected                          │
│                                                                              │
│  User Notification:                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  ⚠️ Screen recording detected. Sensitive data hidden for security.  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 12. Implementation Checklist

### Per-Field Privacy

- [ ] All sensitive fields have default masked state
- [ ] Eye toggle icon has 48dp touch target
- [ ] Peek gesture has timeout (max 10s)
- [ ] Haptic feedback on reveal/hide
- [ ] Screen reader announces masked state

### App-Level Privacy

- [ ] Privacy screen on app background
- [ ] FLAG_SECURE on sensitive activities (Android)
- [ ] Screen recording detection (iOS)
- [ ] Clipboard auto-clear for sensitive data
- [ ] Session timeout re-masks all data

### Accessibility

- [ ] "Hidden" / "Revealed" announced to screen readers
- [ ] Eye icon has content description
- [ ] Timeout announced before auto-hide
- [ ] Non-visual indicator for peek state

---

## 13. Related Files

| File | Purpose |
|------|---------|
| `COMPONENTS.md` | Component specifications |
| `MOCKUP.md` | Screen state templates |
| `FEEDBACK_PATTERNS.md` | Toast/snackbar for copy confirmation |
| `USER_FLOWS.md` | Authentication flows |

---

## Version History

| Date | Change |
|------|--------|
| 2026-03-19 | Initial privacy patterns document |
