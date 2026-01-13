# Mockup Validation Checklist

> Use this checklist to validate mockup completeness before marking design layer as done.

**Version**: 1.0.0
**Last Updated**: 2025-01-13

---

## Quick Validation

Run these checks before finalizing any MOCKUP.md:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MOCKUP VALIDATION CHECKLIST                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SCREEN COVERAGE                                    Status                   │
│  ────────────────────────────────────────────────────────────────────────   │
│  [ ] All screens from SPEC.md have wireframes      ___/___                  │
│  [ ] Each screen has Success state                 ___/___                  │
│  [ ] Each screen has Loading state (shimmer)       ___/___                  │
│  [ ] Each screen has Empty state                   ___/___                  │
│  [ ] Each screen has Error state                   ___/___                  │
│                                                                              │
│  COMPONENT COVERAGE                                Status                    │
│  ────────────────────────────────────────────────────────────────────────   │
│  [ ] All unique components documented              ___/___                  │
│  [ ] Each component has wireframe                  ___/___                  │
│  [ ] Each component has specifications             ___/___                  │
│  [ ] Each component has states defined             ___/___                  │
│  [ ] Each component has data binding               ___/___                  │
│                                                                              │
│  INTERACTION COVERAGE                              Status                    │
│  ────────────────────────────────────────────────────────────────────────   │
│  [ ] All buttons have tap actions                  ___/___                  │
│  [ ] All cards have navigation targets             ___/___                  │
│  [ ] Gestures defined (pull, swipe, etc.)          ___/___                  │
│  [ ] Navigation flow documented                    Yes / No                 │
│                                                                              │
│  DATA COVERAGE                                     Status                    │
│  ────────────────────────────────────────────────────────────────────────   │
│  [ ] All API endpoints mapped to screens           ___/___                  │
│  [ ] All response fields mapped to UI              ___/___                  │
│  [ ] Error codes mapped to error states            ___/___                  │
│  [ ] Offline strategy defined                      Yes / No                 │
│                                                                              │
│  ACCESSIBILITY                                     Status                    │
│  ────────────────────────────────────────────────────────────────────────   │
│  [ ] Touch targets ≥ 48dp                          Yes / No                 │
│  [ ] Screen reader labels documented               Yes / No                 │
│  [ ] Focus order defined                           Yes / No                 │
│  [ ] Color contrast verified                       Yes / No                 │
│                                                                              │
│  QUALITY                                           Status                    │
│  ────────────────────────────────────────────────────────────────────────   │
│  [ ] Wireframes detailed (not placeholders)        Yes / No                 │
│  [ ] Consistent ASCII width (~60 chars)            Yes / No                 │
│  [ ] Annotations present and aligned               Yes / No                 │
│  [ ] Measurements in dp                            Yes / No                 │
│                                                                              │
│  ════════════════════════════════════════════════════════════════════════   │
│                                                                              │
│  OVERALL SCORE: ____%                                                        │
│                                                                              │
│  [ ] READY FOR IMPLEMENTATION                                                │
│  [ ] NEEDS WORK (see gaps below)                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Validation

### 1. Screen Coverage

| Screen | Success | Loading | Empty | Error | Notes |
|--------|:-------:|:-------:|:-----:|:-----:|-------|
| ${SCREEN_1} | ☐ | ☐ | ☐ | ☐ | |
| ${SCREEN_2} | ☐ | ☐ | ☐ | ☐ | |
| ${SCREEN_3} | ☐ | ☐ | ☐ | ☐ | |

**Validation Rules:**
- Success: Full wireframe with real content placeholders
- Loading: Shimmer elements matching success layout exactly
- Empty: Centered illustration (200x200dp) + title + message + CTA
- Error: Error icon (48dp) + title + message + Retry + Go Back

---

### 2. Component Coverage

| Component | Wireframe | Specs | States | Data Binding |
|-----------|:---------:|:-----:|:------:|:------------:|
| ${COMPONENT_1} | ☐ | ☐ | ☐ | ☐ |
| ${COMPONENT_2} | ☐ | ☐ | ☐ | ☐ |
| ${COMPONENT_3} | ☐ | ☐ | ☐ | ☐ |

**Validation Rules:**
- Wireframe: ASCII art showing structure
- Specs: Size, background, radius, elevation, padding
- States: Default, pressed, selected, disabled
- Data Binding: Which API field populates each UI element

---

### 3. Interaction Coverage

| Element | Action | Result | Haptic | Documented |
|---------|--------|--------|:------:|:----------:|
| Back Button | Tap | Navigate back | - | ☐ |
| Menu Button | Tap | Show bottom sheet | - | ☐ |
| Primary CTA | Tap | ${ACTION} | ✓ | ☐ |
| Card | Tap | Navigate to detail | - | ☐ |
| Pull down | Gesture | Refresh data | - | ☐ |

**Validation Rules:**
- Every interactive element must have action defined
- Haptic feedback noted for important actions
- Navigation targets must be specific screens

---

### 4. Data Coverage

| Endpoint | Screen | Fields Mapped | Loading | Empty | Error |
|----------|--------|:-------------:|:-------:|:-----:|:-----:|
| GET ${ENDPOINT_1} | ${SCREEN} | ☐ | ☐ | ☐ | ☐ |
| GET ${ENDPOINT_2} | ${SCREEN} | ☐ | ☐ | ☐ | ☐ |
| POST ${ENDPOINT_3} | ${SCREEN} | ☐ | ☐ | ☐ | ☐ |

**Validation Rules:**
- Every API endpoint must map to a screen
- All response fields must show in UI or be documented as hidden
- Each endpoint needs loading, empty, error handling

---

### 5. Accessibility Checklist

| Element | Min Size | Actual Size | Pass |
|---------|:--------:|:-----------:|:----:|
| Back Button | 48x48dp | ${SIZE} | ☐ |
| Menu Button | 48x48dp | ${SIZE} | ☐ |
| Action Buttons | 48x48dp | ${SIZE} | ☐ |
| List Items | 48x48dp | ${SIZE} | ☐ |
| Cards | 48x48dp | ${SIZE} | ☐ |

| Text Type | Background | Ratio | WCAG | Pass |
|-----------|------------|:-----:|:----:|:----:|
| Primary text | Background | ${RATIO} | AA | ☐ |
| Secondary text | Background | ${RATIO} | AA | ☐ |
| Primary on Surface | Surface | ${RATIO} | AA | ☐ |

**Focus Order Defined:** ☐ Yes / ☐ No

---

### 6. Quality Checklist

#### Wireframe Quality

- [ ] Uses box-drawing characters (┌ ─ ┐ │ └ ┘)
- [ ] Consistent width (~60 characters)
- [ ] Proper nesting for inner elements
- [ ] Annotations on right side with measurements
- [ ] Real content examples (not Lorem Ipsum)

#### Specification Quality

- [ ] All sizes in dp (not px)
- [ ] All text sizes in sp
- [ ] Colors as hex codes
- [ ] Corner radius specified
- [ ] Elevation/shadow specified
- [ ] Padding/margin specified

#### Interaction Quality

- [ ] All buttons have actions
- [ ] Navigation destinations are specific
- [ ] Gestures are standard (pull, swipe)
- [ ] Feedback specified (ripple, haptic)

---

## Gap Detection Report

### Missing Items

| Gap Type | Item | Action Required |
|----------|------|-----------------|
| Missing Screen | ${SCREEN} | Add wireframe + states |
| Missing State | ${SCREEN} - Loading | Add shimmer wireframe |
| Unmapped Data | ${API_FIELD} | Map to UI element |
| Missing Interaction | ${ELEMENT} | Define tap action |
| Accessibility Gap | ${ELEMENT} | Add screen reader label |

### Priority

| Priority | Description | Count |
|:--------:|-------------|:-----:|
| P0 | Blocks implementation | ${COUNT} |
| P1 | Should fix before impl | ${COUNT} |
| P2 | Nice to have | ${COUNT} |

---

## Scoring

Calculate completion percentage:

```yaml
scoring:
  screen_coverage:
    weight: 30%
    score: (screens_complete / total_screens) * 100

  component_coverage:
    weight: 20%
    score: (components_complete / total_components) * 100

  interaction_coverage:
    weight: 20%
    score: (interactions_mapped / total_interactions) * 100

  data_coverage:
    weight: 15%
    score: (endpoints_mapped / total_endpoints) * 100

  accessibility:
    weight: 10%
    score: (accessibility_checks_passed / total_checks) * 100

  quality:
    weight: 5%
    score: (quality_checks_passed / total_quality_checks) * 100

  total: sum(weight * score)
```

### Score Thresholds

| Score | Status | Action |
|:-----:|--------|--------|
| 95-100% | ✅ Excellent | Ready for implementation |
| 85-94% | ⚠️ Good | Minor gaps, can proceed |
| 70-84% | ⚠️ Acceptable | Fix P0/P1 gaps first |
| < 70% | ❌ Incomplete | Major rework needed |

---

## Auto-Validation Commands

Claude should run these validations automatically:

```yaml
auto_validation:
  on_mockup_create:
    - validate_screen_coverage()
    - validate_state_coverage()
    - validate_component_coverage()
    - calculate_score()
    - report_gaps()

  on_design_complete:
    - full_validation()
    - generate_score_report()
    - list_action_items()
```

---

## Related Files

| File | Purpose |
|------|---------|
| `MOCKUP_GENERATION_GUIDE.md` | How to generate mockups |
| `GENERATION_ORDER.md` | File generation pipeline |
| `features/mockups/MOCKUP.md` | Template to validate against |

