# template_meta
# template_version: "2.81.0"
# template_path: "templates/blueprints/workspace-project/design-spec-layer/_shared/FEEDBACK_PATTERNS.md"
# last_modified: "2026-03-19"

# Feedback Patterns - mifos-mobile

> **Purpose**: Comprehensive guide for user feedback mechanisms including snackbars, toasts, dialogs, and micro-interactions.
> **Last Updated**: 2026-03-19
> **Principle**: Every user action deserves acknowledgment

---

## 1. Feedback Type Decision Tree

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           FEEDBACK TYPE DECISION TREE                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│                              User Action Occurs                                          │
│                                     │                                                    │
│                         ┌───────────┴───────────┐                                       │
│                         │  Requires User        │                                       │
│                         │  Decision/Input?      │                                       │
│                         └───────────┬───────────┘                                       │
│                                     │                                                    │
│                    ┌────────────────┼────────────────┐                                  │
│                   YES               │                NO                                  │
│                    │                │                │                                   │
│                    ▼                │                ▼                                   │
│             ┌──────────┐            │         ┌──────────────┐                          │
│             │  DIALOG  │            │         │ Is action    │                          │
│             └──────────┘            │         │ reversible?  │                          │
│                                     │         └──────┬───────┘                          │
│                                     │                │                                   │
│                                     │    ┌───────────┼───────────┐                      │
│                                     │   YES          │           NO                      │
│                                     │    │           │           │                       │
│                                     │    ▼           │           ▼                       │
│                                     │ ┌──────────┐   │    ┌──────────┐                  │
│                                     │ │ SNACKBAR │   │    │  TOAST   │                  │
│                                     │ │ + Undo   │   │    │ (brief)  │                  │
│                                     │ └──────────┘   │    └──────────┘                  │
│                                     │                │                                   │
│                                     │         ┌──────┴──────┐                           │
│                                     │         │ Is message  │                           │
│                                     │         │ critical?   │                           │
│                                     │         └──────┬──────┘                           │
│                                     │                │                                   │
│                                     │    ┌───────────┼───────────┐                      │
│                                     │   YES          │           NO                      │
│                                     │    │           │           │                       │
│                                     │    ▼           │           ▼                       │
│                                     │ ┌──────────┐   │    ┌────────────┐                │
│                                     │ │ SNACKBAR │   │    │  INLINE    │                │
│                                     │ │(persist) │   │    │ INDICATOR  │                │
│                                     │ └──────────┘   │    └────────────┘                │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1.1 Expanded Snackbar vs Toast Decision Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SNACKBAR vs TOAST - DETAILED DECISION MATRIX                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  QUESTION 1: Does the message have an action?                               │
│  ─────────────────────────────────────────────────────────────────────      │
│                                                                              │
│    YES (Undo, Retry, View, etc.)                                            │
│    └── ALWAYS use SNACKBAR                                                  │
│                                                                              │
│    NO (Pure information)                                                    │
│    └── Continue to Question 2                                               │
│                                                                              │
│  QUESTION 2: How important is the message?                                  │
│  ─────────────────────────────────────────────────────────────────────      │
│                                                                              │
│    CRITICAL (User must see this)                                            │
│    └── Use SNACKBAR (longer duration: 6-10s)                               │
│    Examples: Payment processed, Item deleted, Settings changed             │
│                                                                              │
│    INFORMATIONAL (Nice to know)                                             │
│    └── Use TOAST (2-3s)                                                    │
│    Examples: Copied to clipboard, Saved, Refreshed                         │
│                                                                              │
│  QUESTION 3: Is the action reversible?                                      │
│  ─────────────────────────────────────────────────────────────────────      │
│                                                                              │
│    YES (Can be undone)                                                      │
│    └── SNACKBAR with UNDO action + progress bar                            │
│    Duration: 6s with visual countdown                                       │
│                                                                              │
│    NO (Permanent)                                                           │
│    └── SNACKBAR without undo                                               │
│    Consider: Confirmation dialog BEFORE action instead                     │
│                                                                              │
│  QUESTION 4: Is this a success or error?                                    │
│  ─────────────────────────────────────────────────────────────────────      │
│                                                                              │
│    SUCCESS (Positive outcome)                                               │
│    ├── Simple success → TOAST (2s, green accent)                           │
│    └── Success with next step → SNACKBAR with action                       │
│                                                                              │
│    ERROR (Something went wrong)                                             │
│    ├── Recoverable → SNACKBAR with Retry (persist until dismissed)         │
│    └── Non-recoverable → SNACKBAR with info (6-10s) or DIALOG             │
│                                                                              │
│    WARNING (Heads up)                                                       │
│    └── SNACKBAR with optional action (6s)                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Quick Reference Table

| Scenario | Component | Duration | Has Action |
|----------|-----------|:--------:|:----------:|
| "Copied to clipboard" | Toast | 2s | No |
| "Message sent" | Toast | 2s | No |
| "Item deleted" | Snackbar | 6s | Yes (Undo) |
| "Archive moved" | Snackbar | 6s | Yes (Undo) |
| "Connection lost" | Snackbar | Persist | Yes (Retry) |
| "Payment failed" | Snackbar | 10s | Yes (Retry) |
| "Profile updated" | Toast | 3s | No |
| "New version available" | Snackbar | 10s | Yes (Update) |
| "Offline mode" | Snackbar | Persist | Yes (Retry) |
| "Form saved" | Toast | 2s | No |
| "Email verified" | Snackbar | 4s | Yes (Continue) |
| "Rate limit reached" | Snackbar | 6s | No |

### Edge Case Handling

| Edge Case | Solution |
|-----------|----------|
| Multiple messages queued | Show highest priority first, queue others |
| User navigates during snackbar | Dismiss snackbar on navigation |
| Message too long | Truncate with "..." or use dialog |
| Action expired | Show "Action no longer available" |
| Network timeout during undo | Restore item, show retry option |

---

## 2. Feedback Types Overview

| Type | Duration | Dismissal | Action | Use Case |
|------|:--------:|-----------|:------:|----------|
| **Toast** | 2-4s | Auto | No | Simple confirmations |
| **Snackbar** | 4-10s | Auto/Manual | Optional | Reversible actions, errors |
| **Dialog** | Persistent | User action | Required | Critical decisions |
| **Inline** | Persistent | State change | Optional | Form validation, status |
| **Haptic** | Instant | N/A | N/A | Touch feedback |

---

## 3. Toast Specifications

### Visual Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                                                                              │
│                                                                              │
│                          (Main content area)                                 │
│                                                                              │
│                                                                              │
│                                                                              │
│    ┌───────────────────────────────────────────────────────────────────┐    │
│    │  [Icon]  Message text here                                        │    │
│    └───────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│    ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐                          │
│    │  Tab   │  │  Tab   │  │  Tab   │  │  Tab   │                          │
│    └────────┘  └────────┘  └────────┘  └────────┘                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Properties

| Property | Value |
|----------|-------|
| Position | Bottom center, above navigation |
| Margin | 16dp from bottom nav, 16dp horizontal |
| Height | 48dp (single line), 68dp (two lines) |
| Max Width | Screen width - 32dp |
| Corner Radius | 8dp |
| Background | inverseSurface (dark on light, light on dark) |
| Text | Body Medium, inverseOnSurface |
| Icon | 24dp, optional, leading |
| Elevation | 6dp |

### Toast Variants

| Variant | Icon | Background | Duration |
|---------|------|------------|:--------:|
| **Info** | info_outline | inverseSurface | 3s |
| **Success** | check_circle | #2E7D32 | 2s |
| **Warning** | warning | #F57C00 | 4s |
| **Error** | error | #C62828 | 4s |

### Animation

```
ENTER (300ms):
  ├─ Fade: 0 → 1
  └─ Translate Y: 100% → 0 (from bottom)

EXIT (250ms):
  ├─ Fade: 1 → 0
  └─ Translate Y: 0 → 100%
```

---

## 4. Snackbar Specifications

### Visual Design

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│                                                                              │
│                          (Main content area)                                 │
│                                                                              │
│                                                                              │
│    ┌───────────────────────────────────────────────────────────────────┐    │
│    │  Message text can span multiple lines if needed       [ACTION]    │    │
│    └───────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│    ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐                          │
│    │  Tab   │  │  Tab   │  │  Tab   │  │  Tab   │                          │
│    └────────┘  └────────┘  └────────┘  └────────┘                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Properties

| Property | Value |
|----------|-------|
| Position | Bottom center, above navigation |
| Margin | 16dp from bottom nav |
| Min Height | 48dp |
| Max Height | 68dp (2 lines) |
| Corner Radius | 4dp |
| Background | #323232 (dark) / #FFFFFF (light) |
| Text | Body Medium |
| Action | Label Large, Primary color |
| Elevation | 6dp |

### Snackbar with Undo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│    ┌───────────────────────────────────────────────────────────────────┐    │
│    │  Item deleted                                            [UNDO]   │    │
│    │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░░░░░░░░░░░░░░░            │    │
│    └───────────────────────────────────────────────────────────────────┘    │
│         ↑ Progress bar showing time remaining to undo                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Snackbar Types

| Type | Has Action | Duration | Progress |
|------|:----------:|:--------:|:--------:|
| **Information** | No | 4s | No |
| **Confirmation** | No | 3s | No |
| **Reversible** | Yes (Undo) | 6s | Yes |
| **Error** | Yes (Retry) | 10s | No |
| **Persistent** | Yes (Dismiss) | Until dismissed | No |

### Snackbar Queue Behavior

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SNACKBAR QUEUE RULES                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. Only ONE snackbar visible at a time                                      │
│  2. New snackbar dismisses current (unless current has undo action)          │
│  3. Priority order: Error > Warning > Info > Success                         │
│  4. If current has undo, queue new snackbar (show after current)             │
│                                                                              │
│  Queue Example:                                                              │
│  ┌─────────┐                                                                 │
│  │ Error   │ ← Shows immediately (highest priority)                         │
│  ├─────────┤                                                                 │
│  │ Info    │ ← Queued, shows after error dismisses                          │
│  ├─────────┤                                                                 │
│  │ Success │ ← Queued, shows after info                                     │
│  └─────────┘                                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Dialog Specifications

### Alert Dialog

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          (Scrim overlay 50% black)                           │
│                                                                              │
│          ┌─────────────────────────────────────────────────────┐            │
│          │                                                     │            │
│          │                      [Icon]                         │            │
│          │                                                     │            │
│          │                   Dialog Title                      │            │
│          │                                                     │            │
│          │    Dialog body text explaining the situation        │            │
│          │    or asking for user confirmation.                 │            │
│          │                                                     │            │
│          │                                                     │            │
│          │                    [Cancel]  [Confirm]              │            │
│          │                                                     │            │
│          └─────────────────────────────────────────────────────┘            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Dialog Properties

| Property | Value |
|----------|-------|
| Min Width | 280dp |
| Max Width | 560dp (or screen width - 48dp) |
| Corner Radius | 28dp |
| Background | surfaceContainerHigh |
| Scrim | #000000 @ 50% |
| Elevation | 24dp |
| Padding | 24dp |

### Dialog Types

| Type | Icon | Buttons | Use Case |
|------|------|---------|----------|
| **Confirmation** | Optional | Cancel + Confirm | Destructive actions |
| **Alert** | warning | OK | Important notices |
| **Error** | error | Retry + Cancel | Error recovery |
| **Success** | check_circle | OK + Secondary | Completion with next step |
| **Input** | None | Cancel + Submit | Single input collection |

### Destructive Dialog (Special Case)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│          ┌─────────────────────────────────────────────────────┐            │
│          │                                                     │            │
│          │                 [🗑️ Delete Icon]                   │            │
│          │                   (Error color)                     │            │
│          │                                                     │            │
│          │                Delete "Project X"?                  │            │
│          │                                                     │            │
│          │    This action cannot be undone. All data           │            │
│          │    associated with this project will be             │            │
│          │    permanently removed.                             │            │
│          │                                                     │            │
│          │                                                     │            │
│          │    [Cancel]              [Delete] ← Error color     │            │
│          │                                                     │            │
│          └─────────────────────────────────────────────────────┘            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Button Colors for Destructive:**
- Cancel: Text button, neutral
- Delete/Confirm: Text button, Error color (#B3261E)

---

## 6. Inline Feedback

### Form Validation States

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  DEFAULT STATE                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Email                                                               │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │                                                             │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  │  Enter your email address                                           │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ERROR STATE                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Email                                                    [Error]   │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │  invalid-email                                    [X Clear] │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  │  ⚠️ Please enter a valid email address                              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│      ↑ Error color border                    ↑ Error helper text           │
│                                                                              │
│  SUCCESS STATE                                                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Email                                                    [✓]       │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │  user@example.com                                           │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  │  ✓ Email verified                                                   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│      ↑ Success color border                  ↑ Success helper text         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Inline Status Indicators

| State | Border | Icon | Helper Text Color |
|-------|--------|------|-------------------|
| Default | outline | None | onSurfaceVariant |
| Focused | primary (2dp) | None | onSurfaceVariant |
| Error | error | error_outline | error |
| Success | success | check_circle | success |
| Loading | primary | CircularProgress | onSurfaceVariant |

---

## 7. Haptic Feedback Matrix

### When to Use Haptics

| Action | Haptic Type | Platform |
|--------|-------------|----------|
| Button tap | Light | Both |
| Toggle switch | Light | Both |
| Pull to refresh | Medium | Both |
| Swipe action | Light | Both |
| Success | `notificationSuccess` | iOS |
| Success | `CONFIRM` (pattern) | Android |
| Error | `notificationError` | iOS |
| Error | `REJECT` (pattern) | Android |
| Warning | `notificationWarning` | iOS |
| Warning | `CLOCK_TICK` | Android |
| Selection | `selectionClick` | iOS |
| Selection | `TICK` | Android |
| Long press trigger | Heavy | Both |

### Haptic Implementation Guide

```kotlin
// Android
object HapticFeedback {
    fun success(view: View) {
        view.performHapticFeedback(HapticFeedbackConstants.CONFIRM)
    }

    fun error(view: View) {
        view.performHapticFeedback(HapticFeedbackConstants.REJECT)
    }

    fun light(view: View) {
        view.performHapticFeedback(HapticFeedbackConstants.CLOCK_TICK)
    }
}
```

```swift
// iOS
import UIKit

func successHaptic() {
    let generator = UINotificationFeedbackGenerator()
    generator.notificationOccurred(.success)
}

func errorHaptic() {
    let generator = UINotificationFeedbackGenerator()
    generator.notificationOccurred(.error)
}
```

---

## 8. Micro-Interactions Catalog

### Button Press

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BUTTON PRESS MICRO-INTERACTION                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Timeline: 0ms ─────────────────────────────────────────────────── 300ms    │
│                                                                              │
│  Press Down (0-100ms):                                                       │
│  ├─ Scale: 1.0 → 0.95                                                       │
│  ├─ Elevation: default → default - 2dp                                      │
│  └─ Ripple starts from touch point                                          │
│                                                                              │
│  Release (100-300ms):                                                        │
│  ├─ Scale: 0.95 → 1.0                                                       │
│  ├─ Elevation: returns to default                                           │
│  └─ Ripple expands and fades                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Toggle Switch

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TOGGLE MICRO-INTERACTION                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  OFF State:                                                                  │
│  ┌────────────────┐                                                         │
│  │ ○──────────    │  Track: surfaceVariant                                  │
│  └────────────────┘  Thumb: outline                                         │
│                                                                              │
│  Transition (200ms, EaseInOut):                                              │
│  ┌────────────────┐                                                         │
│  │    ──●──────   │  Thumb slides, color morphs                             │
│  └────────────────┘  + Haptic at midpoint                                   │
│                                                                              │
│  ON State:                                                                   │
│  ┌────────────────┐                                                         │
│  │    ──────────● │  Track: primaryContainer                                │
│  └────────────────┘  Thumb: primary, with check icon                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pull to Refresh

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PULL TO REFRESH MICRO-INTERACTION                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Phase 1: Pulling (0-64dp)                                                   │
│  ├─ Indicator appears, rotates based on pull distance                       │
│  ├─ Content follows finger with resistance (0.5 factor)                     │
│  └─ Opacity: 0 → 1 as approaching threshold                                 │
│                                                                              │
│  Phase 2: Threshold Reached (64dp+)                                          │
│  ├─ Haptic: Medium impact                                                   │
│  ├─ Indicator snaps to full opacity                                         │
│  └─ Visual cue: "Release to refresh"                                        │
│                                                                              │
│  Phase 3: Refreshing                                                         │
│  ├─ Content snaps back with indicator visible                               │
│  ├─ Indicator: Circular progress (indeterminate)                            │
│  └─ Duration: Until data loaded                                             │
│                                                                              │
│  Phase 4: Complete                                                           │
│  ├─ Indicator: Checkmark (200ms)                                            │
│  ├─ Haptic: Success                                                         │
│  └─ Indicator dismisses (300ms fade + slide up)                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Like/Favorite Animation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  LIKE ANIMATION                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Inactive → Active:                                                          │
│  0ms      100ms     200ms     300ms     400ms                               │
│  │         │         │         │         │                                   │
│  ♡ ────────────────────────────────────────                                 │
│       scale(1 → 1.3)                                                        │
│           color(outline → error)                                            │
│               fill(♡ → ♥)                                                  │
│                   scale(1.3 → 0.9 → 1.0) bounce                             │
│                       + particles burst                                      │
│                                                                              │
│  + Haptic: Medium at 100ms                                                  │
│                                                                              │
│  Active → Inactive:                                                          │
│  ♥ → ♡ (200ms, scale 1 → 0.9 → 1, color error → outline)                  │
│  + Haptic: Light                                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Solution-Oriented Error Messages

### Error Message Formula

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ERROR MESSAGE FORMULA                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  BAD:  "Error 403: Forbidden"                                               │
│  GOOD: "You don't have permission to access this. Contact your admin."      │
│                                                                              │
│  FORMULA:                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  [What happened] + [Why it matters] + [What to do next]             │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  Examples:                                                                   │
│                                                                              │
│  Network Error:                                                              │
│  "We couldn't connect to the server. Check your internet connection         │
│   and try again."                                                            │
│                                                                              │
│  Validation Error:                                                           │
│  "This email is already registered. Sign in instead or use a                │
│   different email."                                                          │
│                                                                              │
│  Permission Error:                                                           │
│  "We need camera access to scan QR codes. Enable it in Settings."           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Error Message Templates

| Error Type | Title | Message | Actions |
|------------|-------|---------|---------|
| **Network** | "No Connection" | "Check your internet and try again." | Retry, Settings |
| **Server** | "Something Went Wrong" | "We're working on it. Try again shortly." | Retry |
| **Auth** | "Session Expired" | "Please sign in again to continue." | Sign In |
| **Permission** | "Permission Required" | "Enable {permission} in Settings." | Settings, Cancel |
| **Validation** | "Invalid {field}" | "{specific guidance}" | Fix input |
| **Not Found** | "{Item} Not Found" | "It may have been moved or deleted." | Go Back, Search |
| **Limit** | "Limit Reached" | "You've reached your {limit}. Upgrade?" | Upgrade, Cancel |

### 9.1 Tone Guidelines for Error Copy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ERROR COPY TONE GUIDE                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  DO:                                                                         │
│  ├── Be empathetic: "We understand this is frustrating..."                  │
│  ├── Take responsibility: "We couldn't" not "You failed"                    │
│  ├── Be specific: "Password must be 8+ characters" not "Invalid password"  │
│  ├── Offer solutions: Always include next steps                             │
│  └── Use plain language: "Something went wrong" not "Error 500"             │
│                                                                              │
│  DON'T:                                                                      │
│  ├── Blame the user: "You entered wrong password" ❌                        │
│  ├── Use technical jargon: "Socket timeout exception" ❌                    │
│  ├── Be vague: "An error occurred" ❌                                       │
│  ├── Use negative phrases: "Don't forget to..." ❌                          │
│  └── Over-apologize: Multiple "sorry" in one message ❌                     │
│                                                                              │
│  TONE SPECTRUM:                                                              │
│  ─────────────────────────────────────────────────────────────────────      │
│  Casual ◄────────●────────► Professional                                    │
│                  ▲                                                           │
│              (Sweet spot for most apps)                                      │
│                                                                              │
│  Fintech apps: Lean professional, build trust                               │
│  Social apps: Lean casual, feel friendly                                    │
│  Enterprise: More professional, less personality                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Contextual Error Templates by Category

#### Network & Connectivity Errors

| HTTP Code | User-Friendly Title | Message | Primary Action |
|:---------:|---------------------|---------|----------------|
| Offline | "You're Offline" | "Connect to the internet to continue." | Settings |
| Timeout | "Taking Too Long" | "The server is slow. Try again?" | Retry |
| 400 | "Something's Not Right" | "We couldn't process that request. Try again." | Retry |
| 401 | "Sign In Required" | "Your session expired. Sign in to continue." | Sign In |
| 403 | "Access Denied" | "You don't have permission. Contact support." | Contact |
| 404 | "Not Found" | "This {item} doesn't exist or was removed." | Go Back |
| 429 | "Slow Down" | "Too many requests. Wait a moment and retry." | Retry (delayed) |
| 500 | "Our Mistake" | "Something went wrong on our end. Try again." | Retry |
| 502/503 | "Temporarily Unavailable" | "We're doing maintenance. Back shortly." | Retry Later |

#### Form Validation Errors

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  FORM VALIDATION ERROR PATTERNS                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  EMAIL FIELD:                                                                │
│  ├── Empty:     "Enter your email address"                                  │
│  ├── Invalid:   "Enter a valid email (e.g., name@example.com)"             │
│  ├── Taken:     "This email is registered. Sign in instead?"               │
│  └── Not found: "No account with this email. Sign up instead?"             │
│                                                                              │
│  PASSWORD FIELD:                                                             │
│  ├── Empty:     "Enter your password"                                       │
│  ├── Too short: "Password must be at least 8 characters"                   │
│  ├── Too weak:  "Add a number or symbol for a stronger password"           │
│  ├── Mismatch:  "Passwords don't match"                                    │
│  └── Incorrect: "Wrong password. Forgot password?"                         │
│                                                                              │
│  PHONE NUMBER:                                                               │
│  ├── Empty:     "Enter your phone number"                                   │
│  ├── Invalid:   "Enter a valid 10-digit phone number"                      │
│  └── Taken:     "This number is already registered"                        │
│                                                                              │
│  AMOUNT/CURRENCY:                                                            │
│  ├── Empty:     "Enter an amount"                                           │
│  ├── Too low:   "Minimum amount is {currency}{minimum}"                    │
│  ├── Too high:  "Maximum amount is {currency}{maximum}"                    │
│  └── Insufficient: "Insufficient balance. You have {currency}{balance}"    │
│                                                                              │
│  DATE FIELD:                                                                 │
│  ├── Empty:     "Select a date"                                             │
│  ├── Past:      "Select a future date"                                     │
│  ├── Too far:   "Select a date within the next {period}"                   │
│  └── Invalid:   "Enter a valid date (MM/DD/YYYY)"                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Payment & Transaction Errors

| Error | Title | Message | Actions |
|-------|-------|---------|---------|
| Card Declined | "Card Declined" | "Your card was declined. Try another payment method." | Try Another, Contact Bank |
| Insufficient Funds | "Not Enough Funds" | "Add funds or try a different payment method." | Add Funds, Try Another |
| Expired Card | "Card Expired" | "Update your card details to continue." | Update Card |
| Invalid CVV | "Invalid CVV" | "Check the 3-digit code on the back of your card." | Re-enter |
| Fraud Suspected | "Verification Needed" | "For your security, verify this transaction." | Verify |
| Daily Limit | "Daily Limit Reached" | "You've hit today's limit. Try again tomorrow." | View Limits |
| Account Frozen | "Account Restricted" | "Contact support to unlock your account." | Contact Support |

### 9.3 Error Recovery Flows

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ERROR RECOVERY FLOW PATTERNS                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PATTERN 1: INLINE RECOVERY                                                  │
│  ─────────────────────────────────────────────────────────────────────      │
│  Error appears inline, user fixes without leaving context                   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────┐                │
│  │  Email                                         [Error]  │                │
│  │  ┌─────────────────────────────────────────────────┐    │                │
│  │  │  john@                                          │    │                │
│  │  └─────────────────────────────────────────────────┘    │                │
│  │  ⚠️ Enter a complete email address (e.g., name@site.com)│                │
│  └─────────────────────────────────────────────────────────┘                │
│  Use: Form validation, minor input errors                                   │
│                                                                              │
│  PATTERN 2: SNACKBAR RECOVERY                                               │
│  ─────────────────────────────────────────────────────────────────────      │
│  Error shown briefly, user can retry from snackbar                          │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │  Couldn't save changes                                    [RETRY] │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│  Use: Network errors, save failures, sync issues                            │
│                                                                              │
│  PATTERN 3: DIALOG RECOVERY                                                  │
│  ─────────────────────────────────────────────────────────────────────      │
│  Error requires user decision before continuing                             │
│                                                                              │
│         ┌─────────────────────────────────────────────┐                    │
│         │                                             │                    │
│         │           [!] Card Declined                 │                    │
│         │                                             │                    │
│         │  Your payment couldn't be processed.       │                    │
│         │  Try another card or contact your bank.    │                    │
│         │                                             │                    │
│         │        [Cancel]  [Try Another Card]         │                    │
│         │                                             │                    │
│         └─────────────────────────────────────────────┘                    │
│  Use: Payment errors, critical failures, requires decision                  │
│                                                                              │
│  PATTERN 4: FULL-SCREEN RECOVERY                                            │
│  ─────────────────────────────────────────────────────────────────────      │
│  Error replaces content, dedicated recovery screen                          │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │                        [Cloud Offline Icon]                         │   │
│  │                                                                     │   │
│  │                      You're Offline                                 │   │
│  │                                                                     │   │
│  │         Connect to the internet to view your account                │   │
│  │                                                                     │   │
│  │                        [Try Again]                                  │   │
│  │                                                                     │   │
│  │         ─────────────────────────────────────                      │   │
│  │         While offline, you can still view cached data              │   │
│  │                   [View Offline Mode]                               │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│  Use: No network, critical data missing, app-level errors                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.4 Error Copy Transformation Examples

| Bad Copy ❌ | Good Copy ✓ | Why Better |
|-------------|-------------|------------|
| "Error 404" | "Page not found. Go back or search?" | Actionable |
| "Invalid input" | "Enter a number between 1-100" | Specific guidance |
| "Request failed" | "We couldn't load your data. Try again?" | Clear + action |
| "Authentication error" | "Wrong password. Reset it?" | Direct + helpful |
| "Network error" | "No internet connection. Check settings?" | Cause + solution |
| "Operation not permitted" | "You need admin access for this" | Plain language |
| "Null pointer exception" | "Something went wrong. Try again?" | No jargon |
| "Maximum retries exceeded" | "Still not working. Contact support?" | Escalation path |
| "Invalid date format" | "Use format: MM/DD/YYYY" | Shows correct format |
| "Field required" | "Enter your name to continue" | Contextual |

### 9.5 Error Severity Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ERROR SEVERITY & PRESENTATION                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LEVEL 1: BLOCKING (Critical)                                               │
│  ─────────────────────────────────────────────────────────────────────      │
│  Presentation: Full-screen or modal dialog                                  │
│  Examples: Authentication failure, payment error, data corruption           │
│  User CANNOT proceed without resolution                                     │
│                                                                              │
│  LEVEL 2: SERIOUS (Major)                                                   │
│  ─────────────────────────────────────────────────────────────────────      │
│  Presentation: Persistent snackbar or inline banner                         │
│  Examples: Sync failure, feature unavailable, partial data loss            │
│  User CAN proceed with degraded experience                                  │
│                                                                              │
│  LEVEL 3: MODERATE (Minor)                                                  │
│  ─────────────────────────────────────────────────────────────────────      │
│  Presentation: Auto-dismiss snackbar (6-10s)                               │
│  Examples: Optional feature error, non-critical API failure                │
│  User experience mostly unaffected                                          │
│                                                                              │
│  LEVEL 4: INFORMATIONAL (Warning)                                           │
│  ─────────────────────────────────────────────────────────────────────      │
│  Presentation: Toast or subtle indicator                                    │
│  Examples: Slow connection warning, approaching limit                      │
│  Heads-up, no action required                                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Feedback Timing Guidelines

| Action | Feedback Type | Timing |
|--------|---------------|--------|
| Button tap | Haptic + ripple | Immediate (0ms) |
| Form submit | Loading indicator | Immediate |
| Form success | Success toast | After 500ms (perceived smoothness) |
| Form error | Inline error | Immediate |
| Network request start | Skeleton/shimmer | After 200ms delay |
| Network request complete | Content swap | Immediate |
| Delete action | Snackbar with undo | Immediate |
| Save action | Auto-save indicator | Debounced (500ms) |
| Navigation | Screen transition | 300ms |

---

## 11. Implementation Checklist

### Per-Action Feedback

- [ ] Every button has haptic feedback
- [ ] Every form has validation states
- [ ] Every async action has loading indicator
- [ ] Every error has recovery action
- [ ] Every success has next step suggestion

### Visual Consistency

- [ ] All toasts use same position/style
- [ ] All snackbars queue properly
- [ ] All dialogs have consistent padding
- [ ] All error states use error color

### Accessibility

- [ ] Snackbars announced to screen readers
- [ ] Dialog focus trapped properly
- [ ] Error messages linked to inputs
- [ ] Haptics have visual alternatives

---

## 12. Related Files

| File | Purpose |
|------|---------|
| `COMPONENTS.md` | Component specifications |
| `MOCKUP.md` | Screen state templates |
| `MOTION_CHOREOGRAPHY.md` | Animation specifications |
| `PRIVACY_PATTERNS.md` | Sensitive data feedback |

---

## Version History

| Date | Change |
|------|--------|
| 2026-03-19 | Initial feedback patterns document |
