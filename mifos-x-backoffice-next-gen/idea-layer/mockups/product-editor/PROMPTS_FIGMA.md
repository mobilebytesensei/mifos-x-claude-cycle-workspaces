<!-- source: screens/product-editor/ui.yaml (+ docs.yaml, flow.yaml, demo-data.yaml, design-tokens.yaml) -->
<!-- source_hash: ui=ab4944d66c85 docs=badac140d422 flow=1f63e8b76f99 -->
<!-- generated: 2026-07-31T03:24:55Z -->

# Product Editor — Figma Design Handoff Prompts

> Generated from `screens/product-editor/ui.yaml` by `/idea-feature-mockup`. Companion to `MOCKUP.md` (ASCII wireframes).
> Format: natural-language design instructions for Figma AI / manual design handoff — same source data as the mockup, framed as prose "Create a..." / "On tap, navigate to..." instructions rather than YAML spec blocks.
> Archetype: `form_screen` · Module: `m08-products-charges` · Screens: 1 (`product-editor`) · States: `loading`, `content`, `empty`, `error`

---

## Section 1: Design System Context

Design the Product Editor as part of **Mifos-X Back Office NextGen**, a permission-gated, offline-first Fineract back-office admin console. The overall feel is calm, dense, and clinical — a financial-admin tool, not a consumer app. Use Material 3 components throughout, light theme as the primary surface (dark theme is available as a full tonal flip but is not the default). Base typeface is **Roboto** for all UI text; use **Roboto Mono** specifically for every numeric figure — principal amounts, interest rates, repayment counts, dates — so digits align column-to-column during config review.

Bind every color to a Figma variable rather than a literal hex, using this token→variable map (light theme values shown; a parallel dark-theme collection exists with the tonal-flip values noted where relevant):

- `color/primary` = **#0091EA** (deep light-blue, brand identity) with `color/on-primary` = **#FFFFFF**. Because white-on-#0091EA sits at roughly 2.6:1 contrast (below WCAG-AA 4.5:1 for body text), reserve flat `primary` fills for large/bold labels and icons only — the Save button's white label at 14sp/500-weight on a 48dp-tall filled button is an accepted large-text use, but never set small on-primary body copy.
- `color/primary-container` = **#CBE6FF** with `color/on-primary-container` = **#001E30** — this AA-safe pairing (7:1+) is what any text-on-primary-tinted surface should use instead (e.g. the Charges section's status chip).
- `color/secondary` = **#00796B** (teal) / `color/secondary-container` = **#B8F2E6** — reserved for positive/primary-action emphasis, used sparingly (≤2 accent instances per screen per the framework's density convention).
- `color/error` = **#BA1A1A**, `color/on-error` = **#FFFFFF**, `color/error-container` = **#FFDAD6**, `color/on-error-container` = **#410002** — used for the error-state icon, validation-error field borders and helper text.
- `color/warning-strong` = **#B45309** — the persistent online-only / offline-blocked connect banner fill (white text on amber).
- `color/surface` = **#FCFCFF**, `color/on-surface` = **#1A1C1E** — the app-bar and section-row background plus primary text.
- `color/surface-variant` = **#DEE3EB**, `color/on-surface-variant` = **#42474E** — field fills, shimmer-placeholder fill, and field labels/section headers.
- `color/outline` = **#72777F** and `color/outline-variant` = **#C2C7CF** — section borders and field dividers respectively (this design favors thin 1px outline borders over drop shadows, so elevation stays subtle — level0/level1 on-surface, level3 only for overlays like bottom sheets).

Typography variables (Figma text styles) to bind: `type/title-medium` (16sp/24sp line-height, weight 500) for section headers; `type/body-medium` (14sp/20sp, weight 400) for field labels and body copy; `type/label-medium` (12sp/16sp, weight 500) for helper and validation text; `type/headline-small` (24sp/32sp, weight 600) for the error-state headline; and `type/mono-body` bound to Roboto Mono for every principal/interest/repayment figure.

Spacing variables: `space/md` = 16dp between fields inside a section; `space/section-gap` = 24dp between stacked sections; `space/row-padding` = 12dp vertical padding inside each collapsed section row. Corner-radius variables: `radius/lg` = 16dp for the expandable-section card; `radius/sm` = 8dp for individual fields and chips; `radius/xl` = 28dp for the Save and Retry pill buttons. Elevation stays intentionally restrained — `elevation/level0` (none) for in-flow content, `elevation/level1` (1px/2px, 5% opacity) for the section cards, reserving `elevation/level3` for any modal/bottom-sheet overlay only.

WCAG compliance notes for this screen specifically: every field label (`on-surface-variant` on `surface`) clears 4.5:1; disabled read-only fields drop to 38% opacity per `opacity/disabled`, which is intentional (WCAG allows reduced contrast for disabled controls, and the read-only state is never the only way to see the data — the same values remain legible in the label row). All touch targets — section headers, field rows, the Save button, the Retry button — meet the 48dp minimum comfortable touch target; the Save/Retry pill buttons target 48dp height explicitly.

### Token → Figma variable quick reference

| Design token (`design-tokens.yaml`) | Figma variable | Hex / value | Used for on this screen |
|---|---|---|---|
| `colors.light.primary` | `color/primary` | #0091EA | Save button fill, expanded-chevron tint |
| `colors.light.on_primary` | `color/on-primary` | #FFFFFF | Save button label |
| `colors.light.primary_container` | `color/primary-container` | #CBE6FF | Charges status-chip fill |
| `colors.light.on_primary_container` | `color/on-primary-container` | #001E30 | Charges status-chip text |
| `colors.light.error` | `color/error` | #BA1A1A | Field-error border, error-state icon |
| `colors.light.error_container` | `color/error-container` | #FFDAD6 | Error-state background accent |
| `colors.light.on_error_container` | `color/on-error-container` | #410002 | Error-state icon/text tint |
| `colors.light.warning_strong` | `color/warning-strong` | #B45309 | Offline / online-only connect banner |
| `colors.light.surface` | `color/surface` | #FCFCFF | App bar, section-card fill |
| `colors.light.on_surface` | `color/on-surface` | #1A1C1E | Field values, headline text |
| `colors.light.surface_variant` | `color/surface-variant` | #DEE3EB | Field fills, shimmer, disabled fields |
| `colors.light.on_surface_variant` | `color/on-surface-variant` | #42474E | Field labels, section headers |
| `colors.light.outline` | `color/outline` | #72777F | Section-card border |
| `colors.light.outline_variant` | `color/outline-variant` | #C2C7CF | Field dividers |
| `typography.title_medium` | `type/title-medium` | 16sp/24sp, 500 | Section headers |
| `typography.body_medium` | `type/body-medium` | 14sp/20sp, 400 | Field labels, body copy |
| `typography.label_medium` | `type/label-medium` | 12sp/16sp, 500 | Helper/validation/bound-hint text |
| `typography.label_large` | `type/label-large` | 14sp/20sp, 500 | Save/Retry button labels |
| `typography.headline_small` | `type/headline-small` | 24sp/32sp, 600 | Error-state headline |
| `typography.font_family_mono` | `type/mono-body` | Roboto Mono | Principal/interest/repayment figures |
| `spacing.md` | `space/md` | 16dp | Field-to-field gap |
| `spacing.section_gap` | `space/section-gap` | 24dp | Section-to-section gap |
| `spacing.row_padding` | `space/row-padding` | 12dp | Collapsed section-row vertical padding |
| `radius.lg` | `radius/lg` | 16dp | Section card |
| `radius.sm` | `radius/sm` | 8dp | Field, chip |
| `radius.xl` | `radius/xl` | 28dp | Save / Retry buttons |
| `opacity.disabled` | `opacity/disabled` | 0.38 | Read-only field state |
| `elevation.level1` | `elevation/level1` | 1px/2px, 5% | Section-card resting elevation |

---

## Section 2: Screen Layouts

### Screen: Product Editor — State: Loading

Create a full-bleed mobile frame (393×852dp, Pixel 5 reference) with the resolved app shell in place: a small M3 top app bar (`surface` fill, back-chevron leading, title area) and — because `ui.yaml` declares no per-screen shell override — the project-default bottom navigation bar remains visible beneath the content, even though this is a drill-in form. Use Auto Layout, direction vertical, no horizontal padding on the frame itself; the content column below the app bar uses 16dp horizontal padding and 16dp vertical gap between children.

Inside the content column, stack five shimmer placeholder blocks, one per form section (Details, Terms, Settings, Charges, Accounting), each 56dp tall with `radius/lg` corners and a `surface-variant` fill pulsing at a gentle 1.5s cycle — this shimmer composition must match the collapsed-section-row geometry of the Content state block-for-block, so the transition from Loading to Content reads as a content "reveal" rather than a layout jump. Do not render any text, field values, or the Save button in this state.

### Screen: Product Editor — State: Content (edit mode, Group Business Loan)

On tap from the M08 catalog row, navigate into this frame. Auto Layout vertical, top app bar pinned (title = "Group Business Loan (GBL)", back leading to M08), a scrollable content column beneath it (`content_area`), and a footer-pinned Save button that does not scroll with the list.

The content column is five stacked `expandable_section` cards, each Auto Layout vertical with 16dp internal padding, 16dp gap between the header row and its field rows when expanded, and a 24dp gap between one section card and the next. Each section header row is Auto Layout horizontal, space-between alignment: a chevron/disclosure icon on the left, the section title (Details / Terms / Settings / Charges / Accounting) in `type/title-medium`, and — when collapsed — a trailing summary (e.g. Charges collapsed shows "1: Processing Fee — KES 500"; Accounting collapsed shows "Accrual (periodic)").

When a section is expanded, stack its field rows vertically with 16dp gaps. The Details section's field rows are: a full-width Name text field, then a horizontal pair (Short name text field, Currency dropdown). The Terms section's field rows are: a full-width Principal currency field showing the bound hint "min 5,000 · max 100,000" below it in `type/label-medium`, a horizontal pair (Number of repayments field, Repayment frequency field), then a horizontal pair (Interest rate currency field, Interest type dropdown). The Settings section holds Amortization-type and Interest-calculation-period dropdowns. The Charges section, when expanded, lists each charge as a removable chip row plus a trailing "+ Add charge" affordance that opens the template's `chargeOptions` list. The Accounting section holds the accounting-rule dropdown.

Pin the Save button (a filled `button-primary`, 160dp × 48dp, `radius/xl`, centered horizontally in a 16dp-padded footer bar) beneath the scrollable content, always visible regardless of scroll position, exactly like a bottom action bar.

**Row-by-row Auto Layout spec for the Content state (top to bottom):**

| Row | Auto Layout direction | Padding | Gap to next | Alignment |
|---|---|---|---|---|
| Top app bar | horizontal | 16dp sides | 0 (pinned) | space-between (leading/title/trailing) |
| Details section card | vertical | 16dp all sides | 24dp (`space/section-gap`) | stretch |
| ├─ Name field row | horizontal | 0 | 16dp (`space/md`) | fill-width |
| └─ Short name + Currency row | horizontal | 0 | 0 (two children, 8dp gap between) | fill-width, 60/40 split |
| Terms section card | vertical | 16dp all sides | 24dp | stretch |
| ├─ Principal + bound-hint | vertical | 0 | 4dp | fill-width |
| ├─ Repayments + frequency row | horizontal | 0 | 8dp | fill-width, 50/50 split |
| └─ Interest rate + type row | horizontal | 0 | 8dp | fill-width, 50/50 split |
| Settings section card (collapsed) | vertical | 16dp | 24dp | stretch |
| Charges section card (collapsed) | vertical | 16dp | 24dp | stretch |
| Accounting section card (collapsed) | vertical | 16dp | 24dp | stretch |
| Footer Save bar | horizontal | 16dp all sides | 0 (pinned) | center |

### Screen: Product Editor — State: Empty (create mode)

Structurally identical Auto Layout to the Content state — same five-section stack, same footer Save button — but every field starts unpopulated except where the template supplies a sane default (Currency defaults to the template's first `currencyOptions` entry; Interest type defaults to the template's first `interestTypeOptions` entry). The Details and Terms sections start expanded (to invite immediate entry); Settings, Charges, and Accounting start collapsed with their template defaults already applied. The Charges section shows "0" charges initially. The app-bar title reads "New product" instead of a loaded product name, and the Save button is gated on `CREATE_LOANPRODUCT` instead of `UPDATE_LOANPRODUCT`.

### Screen: Product Editor — State: Error

Center a compact vertical stack in the middle of the frame: a 48×48dp error icon (`on-error-container` tint) at the top, then a `type/headline-small` headline ("Couldn't load this product"), then a `type/body-medium` message describing the specific failure (product load, template load, or save failure), then 24dp of gap before a single `button-primary` labeled "Retry loading" (or "Retry save" for the save-failure variant), 180dp × 48dp, `radius/xl`. No form fields, no shimmer, and no footer Save button render in this state — the app bar falls back to a generic "Product editor" title since no product name has resolved.

---

## Section 3: Component Specifications

### Component: pe_section (`expandable_section`, extends `card`)

Create a card component with two states, **collapsed** and **expanded**. Both states share a `surface` fill, `outline` 1px border, `radius/lg` (16dp) corners, and `elevation/level1` (a very subtle 1px/2px 5%-opacity shadow — this design favors borders over shadows). The header row is always visible: a leading disclosure chevron icon that rotates 180° between collapsed (pointing right) and expanded (pointing down) with a 200ms standard-easing rotation animation; the section title in `type/title-medium` / `on-surface`; and, only when collapsed, a trailing summary string in `type/body-medium` / `on-surface-variant` (e.g. "1: Processing Fee — KES 500"). Tapping anywhere on the header row toggles collapsed↔expanded — this is a pure client-side UI-state toggle with **no network request**, so design the tap target generously (full header row height, minimum 48dp) since it fires very frequently during form review. When expanded, reveal the field-row stack beneath the header with a 250ms fade+expand transition.

### Component: pe_field (`dynamic_form_field`, extends `input`)

This is a runtime-metadata-driven field renderer — its concrete control type (text field, currency field, or dropdown/select) is decided by the Fineract template field's declared type, not hardcoded per field. Design four visual variants sharing one geometry (full-width minus 16dp side margins inside its section, 48dp height, `radius/sm` 8dp corners, `surface-variant` fill):
- **Default** — `surface-variant` fill, `on-surface` value text in `type/body-medium` (or `type/mono-body` for numeric fields), `on-surface-variant` label above in `type/label-medium`.
- **Focused** — add a 2dp `primary` focus ring around the field border, per the framework's `border/focus` token.
- **Disabled (read-only mode)** — apply `opacity/disabled` (38%) uniformly to fill, label, and value; remove the input cursor/focus affordance entirely. This variant activates screen-wide whenever the signed-in user lacks both `CREATE_LOANPRODUCT` and `UPDATE_LOANPRODUCT` — the loaded values stay legible for review, they simply cannot be edited.
- **Error** — swap the fill's border to 2dp `error`, and render a `type/label-medium` helper line beneath in `on-error-container` text (e.g. "Min principal must be less than max principal — correct the Terms section"). This variant appears the instant a field-level or cross-field template validation fails, and clears the instant the value becomes valid again — every edit re-runs the check immediately (no debounce beyond normal input latency).

A **currency_field** sub-variant (used for Principal and Interest-rate) additionally right-aligns its numeric value in `type/mono-body` (Roboto Mono) and shows a persistent bound hint beneath in `type/label-medium` (e.g. "min 5,000 · max 100,000") whenever the underlying template field declares min/max bounds.

A **select / dropdown** sub-variant (used for Currency, Interest type, Amortization type, Interest-calculation period, Accounting rule) renders the current value left-aligned in `type/body-medium` with a trailing 20dp chevron-down icon in `on-surface-variant`; tapping opens a bottom-sheet or inline menu (per platform convention) listing every option from the matching `template.*Options[]` array — never a hardcoded option list, always the live template values.

**Component variant matrix (all `pe_field` sub-variants):**

| Field | Sub-variant | Default state | Notes |
|---|---|---|---|
| Name | text field | free text | Details section |
| Short name | text field | free text | Details section |
| Currency | select | KES / USD (template `currencyOptions`) | Details section |
| Principal | currency_field | Roboto Mono, bound hint | Terms section |
| Number of repayments | dynamic_form_field (numeric) | Roboto Mono | Terms section |
| Repayment frequency | select | Months (template-driven) | Terms section |
| Interest rate | currency_field | Roboto Mono, % suffix | Terms section |
| Interest type | select | Declining Balance / Flat | Terms section |
| Amortization type | select | Equal principal / Equal installments | Settings section |
| Interest-calc period | select | Same as repayment period | Settings section |
| Accounting rule | select | None / Cash / Accrual (periodic) | Accounting section |

### Component: pe_save (`button-primary` / `button-primary-disabled`)

A filled pill button, 160dp × 48dp, `radius/xl` (28dp), centered in the footer bar with 16dp padding on all sides.
- **Default (enabled)** — `primary` fill, `on-primary` label text "Save product" in `type/label-large` (14sp/500 weight) — this is a large/bold label use so the sub-AA contrast of white-on-#0091EA is the accepted usage per the design system's contrast note.
- **Hovered** (desktop/tablet pointer) — darken the fill slightly using the `primary-hover` derived tone.
- **Pressed** — darken further to `primary-pressed`, and apply the `state-layer/pressed` 12%-opacity overlay per Material 3 interaction-state conventions.
- **Disabled** — swap the fill to `surface-variant` (tonal, not simply a dimmed primary) with `on-surface-variant` label text — this specific disabled treatment communicates "a network-required action is currently blocked," matching the "network-required action while offline" convention documented in `COMPONENTS.md`. This state fires whenever the form has an active validation error (Save stays disabled until every field is valid) or while offline (Save is blocked with the connect banner instead).
- This entire component is **absent** (not rendered, not merely disabled) whenever the user holds neither `CREATE_LOANPRODUCT` nor `UPDATE_LOANPRODUCT` — read-only mode removes the button from the layout rather than showing a permanently-disabled affordance.

### Component: pe_error_retry (`button-primary`)

Visually identical construction to `pe_save` (filled pill, `radius/xl`, `primary` fill / `on-primary` label) but sized 180dp × 48dp to fit the longer "Retry loading" label, and centered standalone in the error-state layout rather than pinned to a footer. On tap, this button always transitions the screen back to the Loading state and re-issues both `GET /v1/loanproducts/{productId}` and `GET /v1/loanproducts/template` (or, for the save-failure variant, re-attempts the previously-failed save).

### Supporting components (chrome, referenced but not newly authored)

- **app-bar-detail** — the standard small M3 detail app bar from the shared chrome library: back-chevron leading, screen-sourced title, optional trailing overflow. Used here with the product name (or "New product" / fallback "Product editor") as the title.
- **shimmer-skeleton** — the standard loading placeholder from the shared chrome library, `surface-variant` fill, `radius/lg`, gentle pulse motion; must mirror the content-state section-row geometry exactly.
- **status-chip** — used for each Charges-section line item ("Processing Fee · KES 500 · Disbursement"), `primary-container` fill / `on-primary-container` text, `radius/sm`, with a trailing remove ("×") affordance.
- **offline-banner** — the shared persistent warning banner (`warning-strong` fill, white text), surfaced only when the user attempts to Save while offline, since product/config edits are online-only per this project's maker-checker policy.
- **snackbar** — the shared transient bottom confirmation host, used for save-success and save-failed toasts.

---

## Section 4: Interaction Patterns

### Navigation Transitions

| From | To | Trigger | Animation |
|------|-----|---------|-----------|
| M08 products & charges list | Product Editor (Content) | tap a product row (`open_product_detail`) | slide_right, 300ms `standard` easing |
| M08 products & charges list | Product Editor (Empty) | tap the "new product" affordance | slide_right, 300ms `standard` easing |
| Product Editor (any state) | M08 products & charges list | back / successful Save resolves in-place, then back | slide_left (reverse), 300ms |

### Gesture Handling

- **Tap-to-expand/collapse** on every `pe_section` header — the primary interaction pattern on this screen, fires with zero network latency.
- **Scroll** — the content column scrolls vertically beneath the pinned app bar and above the pinned footer Save button; the footer never scrolls with the list.
- **Pull-to-refresh** is not applicable here (this is a form, not a list) — refreshing happens implicitly via the Retry action in the error state.
- **Long-press** is not used anywhere on this screen.

### Animation Specifications

| Component | Type | Duration | Easing | Delay |
|-----------|------|----------|--------|-------|
| pe_section chevron | rotate 0°→180° | 200ms | standard | 0ms |
| pe_section field-row reveal | fade + expand | 250ms | standard_decelerate | 0ms |
| shimmer pulse | opacity pulse | 1500ms loop | linear | 0ms |
| Loading → Content | fade_in | 300ms | standard_decelerate | 0ms |
| Loading → Error | fade_in | 200ms | standard_decelerate | 0ms |
| Empty → Content (as fields populate) | none (instant, values fill in place) | — | — | — |
| pe_field validation-error appear/clear | fade | 150ms | standard | 0ms |

### State Transitions (mirrors `flow.yaml#transitions`)

- Loading → Content: the product + template resolve cache-first.
- Loading → Empty: create mode — only the template loaded, no product.
- Loading → Error: the product or template failed to load and no cache is available.
- Content → Content: a section expands/collapses, a field changes, or a charge is added (self-transition, no navigation).
- Content → Error: save failed hard with no fallback.
- Empty → Content: the create form is populated from the template defaults.
- Error → Loading: "Retry" tapped — reloads the product + template, or re-attempts the failed save.

---

## Section 5: Content Data

> Zero placeholders. All data sourced from `demo-data.yaml` (real Fineract `LoanProductDto` / `LoanProductTemplateDto` shapes).

### Loaded product (Content state) — Group Business Loan

```yaml
product:
  id: 4
  name: "Group Business Loan"
  shortName: "GBL"
  description: "Working-capital loan for group-guaranteed members, 12-month term."
  currency: { code: "KES", decimalPlaces: 2 }
  principal: 60000.00
  minPrincipal: 5000.00
  maxPrincipal: 100000.00
  numberOfRepayments: 12
  repaymentEvery: 1
  repaymentFrequencyType: "Months"
  interestRatePerPeriod: 2.0
  interestRateFrequencyType: "Per month"
  amortizationType: "Equal installments"
  interestType: "Declining Balance"
  interestCalculationPeriodType: "Same as repayment period"
  charges:
    - { id: 12, name: "Processing Fee", chargeTimeType: "Disbursement", amount: 500.00 }
  accountingRule: "Accrual (periodic)"
```

### Template option lists (drives every dropdown, both Content and Empty states)

```yaml
template:
  currencyOptions: ["KES (Kenyan Shilling)", "USD (US Dollar)"]
  interestTypeOptions: ["Declining Balance", "Flat"]
  amortizationTypeOptions: ["Equal principal payments", "Equal installments"]
  accountingRuleOptions: ["None", "Cash", "Accrual (periodic)"]
  chargeOptions: ["Processing Fee (id=12)", "Late Payment Penalty (id=15)"]
```

### Validation-error content (Content state, out-of-bounds principal)

```yaml
validation_error_state:
  field: principal
  attempted_value: 120000.00
  message: "Min principal must be less than max principal — correct the Terms section"
```

### Per-field content (Content state, Group Business Loan)

| Section | Field | Value | Type |
|---|---|---|---|
| Details | name | "Group Business Loan" | text |
| Details | shortName | "GBL" | text |
| Details | currency | "KES" | select |
| Terms | principal | 60,000.00 (min 5,000 / max 100,000) | mono currency |
| Terms | numberOfRepayments | 12 | mono numeric |
| Terms | repaymentEvery / frequency | 1 / Months | select |
| Terms | interestRatePerPeriod | 2.0 (Per month) | mono currency |
| Terms | interestType | "Declining Balance" | select |
| Settings | amortizationType | "Equal installments" | select |
| Settings | interestCalculationPeriodType | "Same as repayment period" | select |
| Charges | charges[0] | Processing Fee, id=12, KES 500, Disbursement | chip |
| Accounting | accountingRule | "Accrual (periodic)" | select |

### Section summary strings (collapsed-row trailing text)

| Component | Field | Value |
|-----------|-------|-------|
| pe_section (Charges, collapsed) | summary | "1: Processing Fee — KES 500" |
| pe_section (Accounting, collapsed) | summary | "Accrual (periodic)" |
| app-bar-detail (Content) | title | "Group Business Loan (GBL)" |
| app-bar-detail (Empty) | title | "New product" |
| app-bar-detail (Error) | title (fallback) | "Product editor" |

### Error-state text

| State variant | Headline | Body |
|---|---|---|
| product_load_failed | "Couldn't load this product" | "The product failed to load. Check your connection and try again." |
| template_load_failed | "Couldn't load the product template" | "The template failed to load, so field options and validation can't render. Try again." |
| save_failed | "Couldn't save this product" | "The save didn't go through. Your changes are preserved — try again." |

---

## Section 6: Responsive Rules

### Canvas Specification

- Base canvas: 393×852dp (mobile portrait, Pixel 5 reference frame).
- Status bar: 24dp, light-icon transparent overlay over the app bar.
- Bottom navigation bar: 48dp (gesture) / 56dp (3-button), visible per the resolved app-shell defaults.
- Safe content area beneath chrome: 393×770dp.

### Touch Targets

- Minimum touch target: 48×48dp (WCAG 2.5.8) for every `pe_field`, section header row, and both buttons.
- The Save / Retry pill buttons target the "comfortable" 48dp tier rather than the bare 44dp minimum, since they are the primary/only action in their respective states.

### Font Scaling

- Supports system font scaling from 85% to 200%.
- Typography scale is anchored to `type/body-medium` (14sp); at 200% scale, field labels and section headers must not truncate — allow field rows to grow in height rather than clipping text.
- Minimum readable text size after scaling: 12sp (`type/label-medium` floor).

### Theme Variants

- Light theme (default): `colors.light.*` tokens as specified in Section 1.
- Dark theme (available, tonal flip): `primary` becomes **#6FD3FF** / `on-primary` **#00344F**, `surface` becomes **#1A1C1E** / `on-surface` **#E2E2E6**, `error` becomes **#FFB4AB**; every other token relationship (container/on-container pairing, disabled opacity, focus ring) carries over unchanged.
- System default: follow the device theme setting.

### Adaptive Layout

- Portrait phone (this spec's primary target): single column, full-width section cards as designed above.
- Tablet / desktop (≥600dp, per `breakpoints.tablet`): the bottom navigation bar is replaced by a permanent navigation rail per the app shell's adaptive-scaffold behavior; the form content column gains a max-width constraint (~600dp) and centers within the remaining space rather than stretching edge-to-edge.
- Foldable: dual-pane is not applicable to this single-screen form; it renders single-pane on either half of an unfolded device.

### Breakpoint reference (`design-tokens.yaml#breakpoints`)

| Breakpoint | Width | Layout behavior for this screen |
|---|---|---|
| mobile | 0dp+ | Single-column section stack, bottom nav bar, footer-pinned Save (primary target) |
| tablet | 600dp+ | Navigation rail replaces bottom nav; form column max-width ~600dp, centered |
| desktop | 840dp+ | Permanent drawer available; form column stays ~600dp centered with generous side margins |
| large | 1240dp+ | Same as desktop; no additional multi-pane behavior for this single-screen form |

### Icon and touch-target reference (`design-tokens.yaml#icon`, `#touch_targets`)

- Disclosure chevron (`pe_section`): `icon.sm` 20dp.
- Error-state icon: `icon.xl` 48dp.
- Dropdown trailing chevron: `icon.sm` 20dp.
- Minimum touch target: 44dp (`touch_targets.minimum`); this screen's interactive rows all target the "comfortable" 48dp tier (`touch_targets.comfortable`).
