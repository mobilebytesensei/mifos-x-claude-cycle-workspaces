# template_meta
# template_version: "2.84.0"
# template_path: "templates/blueprints/workspace-project/design-spec-layer/_shared/MOTION_CHOREOGRAPHY.md"
# last_modified: "2026-03-20"

# Motion Choreography - mifos-mobile

> **Purpose**: Comprehensive motion design system for coordinated animations, transitions, and micro-interactions.
> **Last Updated**: 2026-03-19
> **Principle**: Motion should be purposeful, guiding users through state changes with clarity and delight.

---

## 1. Motion Design Principles

### Core Principles

| Principle | Description | Example |
|-----------|-------------|---------|
| **Purposeful** | Every animation serves a function | Loading → indicates progress |
| **Natural** | Follows physics and real-world behavior | Easing, momentum, gravity |
| **Continuous** | Maintains spatial and temporal consistency | Shared element transitions |
| **Responsive** | Reacts immediately to user input | Touch feedback < 100ms |
| **Accessible** | Respects reduced motion preferences | Static fallbacks available |

### Motion Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MOTION HIERARCHY (Attention Priority)                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Level 1: HERO TRANSITIONS                                                   │
│  └── Shared element, container transform, full-screen changes               │
│      Duration: 300-450ms | User attention: HIGH                             │
│                                                                              │
│  Level 2: STRUCTURAL CHANGES                                                 │
│  └── Screen transitions, modal presentation, navigation                     │
│      Duration: 250-350ms | User attention: MEDIUM-HIGH                      │
│                                                                              │
│  Level 3: COMPONENT STATE                                                    │
│  └── Expand/collapse, selection, toggle                                     │
│      Duration: 150-250ms | User attention: MEDIUM                           │
│                                                                              │
│  Level 4: MICRO-INTERACTIONS                                                 │
│  └── Button press, hover, ripple, icon state                                │
│      Duration: 50-150ms | User attention: LOW                               │
│                                                                              │
│  Level 5: AMBIENT                                                            │
│  └── Shimmer, pulse, breathing indicators                                   │
│      Duration: 1000-2000ms | User attention: PERIPHERAL                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Timing & Easing Standards

### Duration Scale

| Token | Value | Use Case |
|-------|:-----:|----------|
| `instant` | 0ms | Immediate state changes |
| `quick` | 100ms | Micro-interactions, ripples |
| `fast` | 150ms | Button states, icon changes |
| `normal` | 200ms | Standard transitions |
| `moderate` | 250ms | Component animations |
| `slow` | 300ms | Screen transitions |
| `emphasis` | 400ms | Hero transitions |
| `dramatic` | 500ms | Celebration animations |

### Easing Curves

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  EASING CURVE REFERENCE                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STANDARD (default for most animations)                                      │
│  cubic-bezier(0.4, 0.0, 0.2, 1.0)                                           │
│  ────────────────●                                                          │
│               ●                                                              │
│            ●                                                                 │
│         ●                                                                    │
│       ●                                                                      │
│     ●                                                                        │
│    ●                                                                         │
│  ●                                                                           │
│  Use: Navigation, state changes                                              │
│                                                                              │
│  DECELERATE (entering elements)                                              │
│  cubic-bezier(0.0, 0.0, 0.2, 1.0)                                           │
│  ────────────────●                                                          │
│             ●                                                                │
│          ●                                                                   │
│        ●                                                                     │
│      ●                                                                       │
│    ●                                                                         │
│   ●                                                                          │
│  ●                                                                           │
│  Use: Elements appearing, dialog entry                                       │
│                                                                              │
│  ACCELERATE (exiting elements)                                               │
│  cubic-bezier(0.4, 0.0, 1.0, 1.0)                                           │
│                 ●────────────────                                           │
│                ●                                                             │
│               ●                                                              │
│              ●                                                               │
│             ●                                                                │
│            ●                                                                 │
│          ●                                                                   │
│  ●●●●●●●                                                                     │
│  Use: Elements exiting, dismissing                                           │
│                                                                              │
│  SPRING (playful/interactive)                                                │
│  spring(damping: 0.7, stiffness: 300)                                       │
│                 ●                                                            │
│                  ●                                                           │
│                 ●                                                            │
│             ●●●●                                                             │
│          ●●                                                                  │
│       ●●                                                                     │
│    ●●                                                                        │
│  ●●                                                                          │
│  Use: Bounce, overshoot, playful interactions                                │
│                                                                              │
│  SHARP (abrupt, intentional)                                                 │
│  cubic-bezier(0.4, 0.0, 0.6, 1.0)                                           │
│  Use: Selection snaps, toggle states                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Platform-Specific Curves

| Animation Type | Android | iOS |
|----------------|---------|-----|
| Standard | FastOutSlowInInterpolator | .easeInOut |
| Decelerate | DecelerateInterpolator | .easeOut |
| Accelerate | AccelerateInterpolator | .easeIn |
| Spring | SpringAnimation | .spring() |
| Linear | LinearInterpolator | .linear |

---

## 3. Shared Element Transitions

### Hero Transition Pattern

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SHARED ELEMENT TRANSITION                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SOURCE SCREEN                        TARGET SCREEN                          │
│  ┌─────────────────────┐              ┌─────────────────────────────┐       │
│  │  [Card]             │              │  ┌───────────────────────┐  │       │
│  │  ┌───────────┐      │              │  │                       │  │       │
│  │  │  [Image]  │      │    ───►      │  │     [Image Hero]      │  │       │
│  │  ├───────────┤      │              │  │                       │  │       │
│  │  │  Title    │      │              │  └───────────────────────┘  │       │
│  │  │  Desc     │      │              │                             │       │
│  │  └───────────┘      │              │  Title (expanded)           │       │
│  │                     │              │  Full description text...   │       │
│  │  [Other cards...]   │              │                             │       │
│  └─────────────────────┘              └─────────────────────────────┘       │
│                                                                              │
│  TIMELINE (350ms total):                                                     │
│  ─────────────────────────────────────────────────────────────────────      │
│  0ms                    175ms                               350ms           │
│  │                        │                                    │            │
│  ├── Image starts morph ──┼────── Image completes morph ──────┤            │
│  ├── Card fades (0-150ms)─┤                                    │            │
│  │                        ├── Title fades in (175-300ms) ──────┤            │
│  │                        ├── Content fades in (200-350ms) ────┤            │
│  │                        │                                    │            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Shared Element Properties

| Property | Behavior |
|----------|----------|
| Position | Interpolates from source to target coordinates |
| Size | Morphs from source to target dimensions |
| Corner Radius | Animates radius change (e.g., 12dp → 0dp) |
| Elevation | Increases during transition, settles at target |
| Clip Bounds | Expands/contracts with morph |

### Container Transform

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONTAINER TRANSFORM (Material Design)                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  FAB → Full Screen:                                                          │
│                                                                              │
│  ┌─────────┐     ┌───────────┐     ┌─────────────────┐     ┌──────────────┐│
│  │   [+]   │ ──► │  [    ]   │ ──► │                 │ ──► │              ││
│  └─────────┘     │  [ ++ ]   │     │    [Content]    │     │   [Screen]   ││
│   56x56dp        └───────────┘     │                 │     │              ││
│                    expanding       └─────────────────┘     └──────────────┘│
│                                        morphing              full screen   │
│                                                                              │
│  Properties:                                                                 │
│  ├── Duration: 300ms                                                        │
│  ├── Easing: Standard (fast out, slow in)                                   │
│  ├── Surface color: FAB color → Screen surface                              │
│  ├── Elevation: FAB elevation → Screen elevation                            │
│  └── Content: Cross-fade at 50% of animation                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Implementation Guide

```kotlin
// Android - Shared Element
val extras = FragmentNavigatorExtras(
    imageView to "hero_image",
    titleView to "hero_title"
)

findNavController().navigate(
    R.id.detailFragment,
    args,
    null,
    extras
)

// In destination fragment
sharedElementEnterTransition = MaterialContainerTransform().apply {
    duration = 350
    scrimColor = Color.TRANSPARENT
    setAllContainerColors(requireContext().getColor(R.color.surface))
}
```

```swift
// iOS - Hero Animation
let transition = HeroTransition()
transition.modalPresentationStyle = .fullScreen

// Source view
heroID = "card_image"

// Destination view
heroID = "card_image"
heroModifiers = [.arc, .duration(0.35)]
```

---

## 4. Staggered Entry Animations

### Stagger Pattern

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STAGGERED ENTRY PATTERN                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LIST ITEMS APPEARING:                                                       │
│                                                                              │
│  0ms      50ms     100ms    150ms    200ms    250ms    300ms                │
│  │         │        │        │        │        │        │                   │
│  ├─────────────────────────────────────────────────────────────            │
│  │  [Item 1] ●──────────────────────────────────────────────►  visible     │
│  │         │                                                                │
│  │         [Item 2] ●──────────────────────────────────────►  visible      │
│  │                  │                                                       │
│  │                  [Item 3] ●────────────────────────────►  visible       │
│  │                           │                                              │
│  │                           [Item 4] ●──────────────────►  visible        │
│  │                                    │                                     │
│  │                                    [Item 5] ●────────►  visible         │
│                                                                              │
│  RULES:                                                                      │
│  ├── Stagger delay: 50ms between items                                      │
│  ├── Max visible stagger: 5 items (then instant)                            │
│  ├── Per-item duration: 200ms                                               │
│  ├── Animation: Fade (0→1) + Translate Y (24dp→0)                           │
│  └── Easing: Decelerate                                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Stagger Specifications

| Parameter | Value | Notes |
|-----------|:-----:|-------|
| Stagger Delay | 50ms | Between consecutive items |
| Max Staggered Items | 5 | Items 6+ appear instantly |
| Item Animation Duration | 200ms | Each item's animation |
| Total Max Duration | 450ms | First to last item |
| Entry Distance | 24dp | Vertical slide distance |
| Initial Opacity | 0 | Fade from invisible |

### Grid Stagger Pattern

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  GRID STAGGER (diagonal wave)                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Order of appearance:                                                        │
│                                                                              │
│  ┌─────┐  ┌─────┐  ┌─────┐                                                 │
│  │  1  │  │  2  │  │  4  │                                                 │
│  └─────┘  └─────┘  └─────┘                                                 │
│  ┌─────┐  ┌─────┐  ┌─────┐                                                 │
│  │  3  │  │  5  │  │  7  │                                                 │
│  └─────┘  └─────┘  └─────┘                                                 │
│  ┌─────┐  ┌─────┐  ┌─────┐                                                 │
│  │  6  │  │  8  │  │  9  │                                                 │
│  └─────┘  └─────┘  └─────┘                                                 │
│                                                                              │
│  Pattern: Diagonal from top-left                                             │
│  Formula: delay = (row + column) * staggerDelay                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Choreographed Transitions

### Screen Transition Choreography

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  FORWARD NAVIGATION CHOREOGRAPHY                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  EXIT (Current Screen)          ENTER (New Screen)                          │
│  ─────────────────────          ─────────────────                           │
│                                                                              │
│  0ms────100ms────200ms          0ms────100ms────200ms────300ms              │
│                                                                              │
│  Content fades ●──────►         ●───────────────────────────► Toolbar       │
│  (0ms-150ms, ease-in)                                           (instant)   │
│                                                                              │
│  Screen slides ●──────►              ●──────────────────► Content           │
│  left 30%                            (50ms delay, stagger)                  │
│  (0ms-200ms)                                                                │
│                                                                              │
│                                           ●────────────► FAB                │
│                                           (100ms delay, scale)              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BACK NAVIGATION CHOREOGRAPHY                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  EXIT (Current Screen)          ENTER (Previous Screen)                     │
│  ─────────────────────          ───────────────────────                     │
│                                                                              │
│  0ms────100ms────200ms          0ms────100ms────200ms────300ms              │
│                                                                              │
│  FAB scales ●──────►            ●───────────────────────────► Screen        │
│  down first                      slides in from left                        │
│  (0ms-100ms)                    (0ms-250ms, decelerate)                     │
│                                                                              │
│  Content fades ●──────►              ●──────────────────► Content           │
│  (50ms delay)                        fades in                               │
│  (50ms-200ms)                        (100ms-300ms)                          │
│                                                                              │
│  Screen slides ●──────►                                                     │
│  right (exit)                                                               │
│  (0ms-200ms)                                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Modal Presentation Choreography

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BOTTOM SHEET CHOREOGRAPHY                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ENTER:                                                                      │
│  0ms        100ms       200ms       300ms       400ms                       │
│  │           │           │           │           │                          │
│  ├─ Scrim fades in (0-150ms) ────────┤                                     │
│  │           │           │           │                                      │
│  │           ├─ Sheet slides up (100-350ms, decelerate) ─────────┤         │
│  │           │           │           │           │                          │
│  │           │           ├─ Handle appears (200-300ms) ──────────┤         │
│  │           │           │           │           │                          │
│  │           │           │           ├─ Content staggers (300-450ms) ─────┤│
│  │           │           │           │           │                          │
│                                                                              │
│  EXIT:                                                                       │
│  0ms        100ms       200ms       250ms                                   │
│  │           │           │           │                                      │
│  ├─ Content fades (0-100ms) ─────────┤                                     │
│  │           │           │           │                                      │
│  ├─ Sheet slides down (0-200ms, accelerate) ─────────────────────┤         │
│  │           │           │           │                                      │
│  │           ├─ Scrim fades out (100-250ms) ─────────────────────┤         │
│  │           │           │           │                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. State Transition Animations

### Loading State Transitions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONTENT → LOADING → SUCCESS/ERROR                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CONTENT → LOADING:                                                          │
│  ┌─────────────────┐      ┌─────────────────┐                               │
│  │  [Content]      │  ──► │  [Skeleton]     │                               │
│  │  visible        │      │  shimmer        │                               │
│  └─────────────────┘      └─────────────────┘                               │
│  Animation: Cross-fade (200ms)                                              │
│  Note: Add 200ms delay before showing skeleton (perceived performance)      │
│                                                                              │
│  LOADING → SUCCESS:                                                          │
│  ┌─────────────────┐      ┌─────────────────┐                               │
│  │  [Skeleton]     │  ──► │  [Content]      │                               │
│  │  shimmer        │      │  visible        │                               │
│  └─────────────────┘      └─────────────────┘                               │
│  Animation: Fade skeleton (150ms) + Stagger content (250ms)                 │
│  Haptic: Success notification                                               │
│                                                                              │
│  LOADING → ERROR:                                                            │
│  ┌─────────────────┐      ┌─────────────────┐                               │
│  │  [Skeleton]     │  ──► │  [Error State]  │                               │
│  │  shimmer        │      │  + action       │                               │
│  └─────────────────┘      └─────────────────┘                               │
│  Animation: Skeleton fades (150ms) + Error scales in (200ms, spring)        │
│  Haptic: Error notification                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Button State Machine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  BUTTON STATE MACHINE                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                    ┌──────────────────────┐                                 │
│                    │       ENABLED        │                                 │
│                    │  [  Submit  ]        │                                 │
│                    └──────────┬───────────┘                                 │
│                               │                                              │
│                    onPress    │                                              │
│                    (100ms scale 0.95)                                        │
│                               │                                              │
│                    ┌──────────▼───────────┐                                 │
│                    │      LOADING         │                                 │
│                    │  [  ●●●  ]          │                                 │
│                    └──────────┬───────────┘                                 │
│                               │                                              │
│           ┌───────────────────┼───────────────────┐                         │
│           │                   │                   │                          │
│    ┌──────▼──────┐    ┌──────▼──────┐    ┌──────▼──────┐                   │
│    │   SUCCESS   │    │    ERROR    │    │  DISABLED   │                   │
│    │  [  ✓  ]    │    │  [  !  ]    │    │  [  ---  ]  │                   │
│    └─────────────┘    └─────────────┘    └─────────────┘                   │
│                                                                              │
│  Transitions:                                                                │
│  ├── Enabled → Loading: Icon cross-fade (150ms)                             │
│  ├── Loading → Success: Icon morph + color (200ms) + haptic                 │
│  ├── Loading → Error: Shake (300ms, 3 cycles) + haptic                      │
│  ├── Success → Enabled: Delay 1s, then fade (200ms)                         │
│  └── Error → Enabled: On tap, fade (150ms)                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Gesture-Driven Animations

### Swipe to Delete

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SWIPE TO DELETE CHOREOGRAPHY                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Phase 1: SWIPING (gesture-driven)                                           │
│  ┌───────────────────────────────────────────────────────────────────┐      │
│  │ [Delete]◄────────────────────────────[ Item Content    ]          │      │
│  └───────────────────────────────────────────────────────────────────┘      │
│  ├── Background reveals delete action (red)                                  │
│  ├── Content follows finger with 1:1 tracking                               │
│  └── Delete icon scales: min(1.0, swipeProgress * 1.5)                      │
│                                                                              │
│  Phase 2: THRESHOLD (at 40% width)                                           │
│  ├── Haptic: Warning                                                        │
│  ├── Delete icon: Scale 1.0 → 1.2 (bounce)                                  │
│  └── Background: Intensify red                                              │
│                                                                              │
│  Phase 3: RELEASE PAST THRESHOLD                                             │
│  ├── Item slides off-screen (200ms, accelerate)                             │
│  ├── Below items animate up (200ms, decelerate, staggered)                  │
│  ├── Snackbar appears with undo                                             │
│  └── Haptic: Success (item deleted)                                         │
│                                                                              │
│  Phase 4: RELEASE BEFORE THRESHOLD                                           │
│  └── Item snaps back (200ms, spring)                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Pull to Refresh Choreography

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  PULL TO REFRESH CHOREOGRAPHY                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PULL DISTANCE:  0dp ────── 40dp ────── 80dp ────── 120dp+                  │
│                   │          │           │            │                      │
│  Indicator:      Hidden    Appearing   Full Size   Overscroll               │
│  Rotation:        0°        90°         180°        360°+                   │
│  Opacity:         0         0.5          1           1                      │
│  Content offset:  0         20dp        40dp        40dp (max)              │
│                                                                              │
│  RELEASE SEQUENCE:                                                           │
│  ─────────────────────────────────────────────────────────────────────      │
│  0ms              100ms             200ms    (data loaded)    +300ms        │
│  │                 │                 │              │            │          │
│  ├── Content snaps to 64dp offset ──┤              │            │          │
│  │                 │                 │              │            │          │
│  │                 ├── Indicator: Indeterminate spin ──────────┤│          │
│  │                 │                 │              │            │          │
│  │                 │                 │              ├── Checkmark morph     │
│  │                 │                 │              │            │          │
│  │                 │                 │              │            ├── Dismiss│
│  │                 │                 │              │    (fade + slide up)  │
│  │                 │                 │              │            │          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Celebration Animations

### Success Celebration

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SUCCESS CELEBRATION CHOREOGRAPHY                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  TIMELINE:                                                                   │
│  0ms      100ms     200ms     400ms     600ms     1000ms    2000ms          │
│  │         │         │         │         │          │         │             │
│  ├─────────────────────────────────────────────────────────────────────────│
│  │                                                                          │
│  ├── Screen transition (0-300ms) ──────────┤                               │
│  │         │         │         │           │                                │
│  │         ├── Icon scale in (100-400ms, spring) ─────────┤                │
│  │         │         │         │           │              │                 │
│  │         │         ├── Confetti burst (200-800ms) ──────┤                │
│  │         │         │         │           │              │                 │
│  │         │         │         ├── Title fade (400-600ms)─┤                │
│  │         │         │         │           │              │                 │
│  │         │         │         │           ├── Subtitle (600-800ms)        │
│  │         │         │         │           │              │                 │
│  │         │         │         │           │              ├── CTA (1000ms) │
│  │                                                                          │
│  HAPTIC:                                                                    │
│  ├── Success notification at 200ms                                         │
│  └── Light tap at 400ms (icon settle)                                      │
│                                                                              │
│  AUTO-DISMISS: After 3-5 seconds (if no CTA required)                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Confetti Specifications

| Property | Value |
|----------|-------|
| Particle Count | 50-100 |
| Particle Size | 8-16dp |
| Colors | Primary, Secondary, Tertiary, Gold |
| Shapes | Rectangle, Circle |
| Duration | 800ms |
| Spread | 60° arc from center-top |
| Gravity | 800dp/s² |
| Initial Velocity | 400-600dp/s upward |
| Rotation | Random 0-360° |
| Fade | Start at 600ms, complete by 800ms |

---

## 9. Reduced Motion Support

### Accessibility Requirements

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  REDUCED MOTION ALTERNATIVES                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CHECK USER PREFERENCE:                                                      │
│  ├── Android: Settings.Global.ANIMATOR_DURATION_SCALE                       │
│  ├── iOS: UIAccessibility.isReduceMotionEnabled                             │
│  └── Web: prefers-reduced-motion media query                                │
│                                                                              │
│  STANDARD MOTION          →         REDUCED MOTION                          │
│  ────────────────────────────────────────────────────────────────────       │
│  Shared element (350ms)   →         Cross-fade (150ms)                      │
│  Slide transition (300ms) →         Instant or fade (100ms)                 │
│  Staggered entry (450ms)  →         Simultaneous fade (150ms)               │
│  Spring bounce            →         Linear ease                              │
│  Parallax scrolling       →         Static                                   │
│  Confetti celebration     →         Static checkmark + color flash          │
│  Skeleton shimmer         →         Static placeholder                       │
│  Infinite animations      →         Static state                             │
│                                                                              │
│  NEVER REMOVE:                                                               │
│  ├── Focus indicators                                                        │
│  ├── Loading spinners (can reduce speed)                                    │
│  └── State change feedback (use instant instead)                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Implementation

```kotlin
// Android
val reduceMotion = Settings.Global.getFloat(
    contentResolver,
    Settings.Global.ANIMATOR_DURATION_SCALE,
    1f
) == 0f

val duration = if (reduceMotion) 0L else 300L
```

```swift
// iOS
let reduceMotion = UIAccessibility.isReduceMotionEnabled

let duration = reduceMotion ? 0.0 : 0.3
```

---

## 10. Performance Guidelines

### Frame Budget

| Target | Budget | Notes |
|--------|:------:|-------|
| 60fps | 16.67ms | Standard target |
| 90fps | 11.11ms | High refresh displays |
| 120fps | 8.33ms | ProMotion/high-end |

### Optimization Rules

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ANIMATION PERFORMANCE RULES                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  DO:                                                                         │
│  ├── Animate transform and opacity only (GPU-accelerated)                   │
│  ├── Use hardware layers during animation                                    │
│  ├── Pre-calculate animation values                                          │
│  ├── Batch layout changes before animation                                   │
│  └── Cancel running animations before starting new ones                      │
│                                                                              │
│  DON'T:                                                                      │
│  ├── Animate layout properties (width, height, margin)                      │
│  ├── Trigger layout during animation frames                                  │
│  ├── Animate more than 3-4 elements simultaneously                          │
│  ├── Use complex clip paths during motion                                    │
│  └── Run animations when app is backgrounded                                │
│                                                                              │
│  GPU-FRIENDLY PROPERTIES:                                                    │
│  ├── transform: translate, scale, rotate                                    │
│  ├── opacity                                                                 │
│  └── filter (with caution)                                                  │
│                                                                              │
│  CPU-HEAVY PROPERTIES (avoid animating):                                     │
│  ├── width, height                                                          │
│  ├── margin, padding                                                         │
│  ├── border-radius (on complex shapes)                                      │
│  └── box-shadow, text-shadow                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Motion Tokens Reference

### Quick Reference

```kotlin
// Motion Tokens (Kotlin)
object MotionTokens {
    // Durations
    const val DURATION_INSTANT = 0L
    const val DURATION_QUICK = 100L
    const val DURATION_FAST = 150L
    const val DURATION_NORMAL = 200L
    const val DURATION_MODERATE = 250L
    const val DURATION_SLOW = 300L
    const val DURATION_EMPHASIS = 400L

    // Easing
    val EASE_STANDARD = FastOutSlowInInterpolator()
    val EASE_DECELERATE = DecelerateInterpolator()
    val EASE_ACCELERATE = AccelerateInterpolator()

    // Stagger
    const val STAGGER_DELAY = 50L
    const val STAGGER_MAX_ITEMS = 5
}
```

```swift
// Motion Tokens (Swift)
enum MotionTokens {
    // Durations
    static let durationInstant: TimeInterval = 0
    static let durationQuick: TimeInterval = 0.1
    static let durationFast: TimeInterval = 0.15
    static let durationNormal: TimeInterval = 0.2
    static let durationModerate: TimeInterval = 0.25
    static let durationSlow: TimeInterval = 0.3
    static let durationEmphasis: TimeInterval = 0.4

    // Easing
    static let easeStandard = Animation.easeInOut
    static let easeDecelerate = Animation.easeOut
    static let easeAccelerate = Animation.easeIn
}
```

---

## 12. Related Files

| File | Purpose |
|------|---------|
| `COMPONENTS.md` | Component specifications |
| `MOCKUP.md` | Screen state templates |
| `FEEDBACK_PATTERNS.md` | Feedback animations |
| `PRIVACY_PATTERNS.md` | Privacy reveal animations |

---

## Version History

| Date | Change |
|------|--------|
| 2026-03-19 | Initial motion choreography document |
