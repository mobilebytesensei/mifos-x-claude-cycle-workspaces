<!-- source: screens/permission-set-detail/{ui,docs,flow,demo-data}.yaml + design-system/{design-tokens,app-shell,COMPONENTS}.md -->
<!-- source_hash: ui=b99fa6b3311f docs=35f3e964db41 flow=6c78983086b8 -->
<!-- generated: 2026-07-31T03:23:52Z -->

# Permission Set Detail — Figma Design Handoff Prompts

> Generated from `screens/permission-set-detail/ui.yaml` (+ `docs.yaml`, `flow.yaml`, `demo-data.yaml`) by `/idea-feature-mockup`.
> Target: Figma AI / manual design handoff. Prose design instructions, not YAML spec blocks — read top to bottom as a build brief for a designer or a Figma-AI generation prompt.
> Screen: Permission Set Detail (resolved codes · umbrellas · fingerprint) · Archetype: detail_screen · Module: permission-capability-engine

---

## 1. Design System Context

Design this screen inside the **mifos-x-backoffice-next-gen** design system: a calm, dense, clinical Material 3 financial-admin console, light-theme default, built around an 8pt spacing grid with a soft (not sharp, not pill-heavy) corner-radius language. The brand identity color is Light Blue **#0091EA** (Figma variable `color/primary`), paired with a Teal secondary **#00796B** (`color/secondary`) reserved for positive or primary-action emphasis, used sparingly — no more than two visible accent uses per screen. A muted indigo tertiary **#5B5891** (`color/tertiary`) exists for informational chips but is not used on this screen. Body copy runs in **Roboto** (`font/family-base`); every numeric or fingerprint-like value — held/total counts, the sha256 fingerprint — runs in **Roboto Mono** (`font/family-mono`) so digits and hex characters align column-for-column, per this design system's house rule for financial/technical data.

Bind every surface, text, and border color to its semantic Figma variable rather than a literal hex, so theme-swapping (light ⇄ dark) is a single variable-collection swap:

- Screen background / app-bar fill / card fill → `color/surface` = **#FCFCFF** (dark-mode counterpart `#1A1C1E`).
- Primary body text (role name, permission code names) → `color/on-surface` = **#1A1C1E** (dark: `#E2E2E6`).
- Secondary/meta text (grouping metadata, fingerprint helper copy) → `color/on-surface-variant` = **#42474E** (dark: `#C2C7CF`).
- Input and shimmer fill → `color/surface-variant` = **#DEE3EB** (dark: `#42474E`).
- Held-code affirmative marker → `color/success` = **#2E7D32** (dark: `#7FCF82`).
- Error icon and message accent → `color/error` = **#BA1A1A** (dark: `#FFB4AB`).
- Retry button fill → `color/primary` = **#0091EA**; its label → `color/on-primary` = **#FFFFFF**.
- Expanded-grouping accent chip → `color/primary-container` = **#CBE6FF** (dark: `#004B70`).
- Card and row hairline borders → `color/outline` = **#72777F**; the app-bar's bottom hairline → the slightly lighter `color/outline-variant` = **#C2C7CF**.

Typography scale — map each usage to its M3 type-role Figma text style: the role name ("Branch Manager") uses **title/medium** (16px/24px, weight 500, tracking 0.15px); permission code names and grouping labels use **body/medium** (14px/20px, weight 400); grouping meta (entity · action) and held/total counts use **body/small** (12px/16px) or **label/small** (11px/16px, weight 500) where the count needs to read as a badge rather than prose; the sha256 fingerprint and every held/total numeral use **font/family-mono** at **body/small** size so the monospace figure column aligns cleanly under the header card's fixed-width layout.

Shape and elevation: bind the search field's rounded corners to `radius/sm` = **8px**; the header card and each grouping row to `radius/lg` = **16px**. This design system favors 1px `color/outline` hairline borders over drop shadows for fast offline rendering — keep elevation at `elevation/level-1` (a near-imperceptible `0 1px 2px rgba(0,0,0,0.05)`) on the header card and skip elevation entirely on grouping rows (flat, divider-separated instead, consistent with the `list-row` pattern in this system's component library). Auto Layout spacing throughout binds to the 8pt scale: `spacing/md` = **16px** for screen-edge padding and inter-section gaps, `spacing/sm` = **8px** between stacked grouping rows, `spacing/xs` = **4px** for tight label/value pairs within a row.

Touch targets: every tappable row, chip, and button must meet a minimum **44×44dp** hit target (`touch-target/minimum`), with 48dp preferred for the primary Retry action per this system's comfortable tier.

---

## 2. Screen Layouts

**Frame setup**: create one Figma frame per state — `Permission Set Detail / Content`, `/ Loading`, `/ Empty`, `/ Error` — each **393×852** (Pixel-5-class mobile portrait canvas, this system's reference device). All four frames share an identical top region (the app bar) and differ only in body content below it; build the app bar once as a component and instance it into all four frames so a title or icon change propagates everywhere.

### Frame: Permission Set Detail / Content

Root Auto Layout: **vertical**, fill-container width, `spacing/md` (16px) between top-level children, no horizontal padding at the frame level (each child manages its own inset).

1. **Top App Bar** (component `app-bar-detail`, small M3 variant) — full width, fixed height 56px, `color/surface` fill, bottom hairline `color/outline-variant`. Auto Layout horizontal, `spacing/sm` between children, vertical-center aligned: a 24px back-chevron icon (`color/on-surface`, tap target 44×44dp) at the leading edge, then the title "My Access" in **title/large** (22px/28px, weight 600) `color/on-surface`, left-aligned, filling remaining width. No trailing icons on this screen.
2. **Header Card** (component `card`) — horizontal padding `spacing/md` (16px), vertical padding `spacing/md`, `radius/lg` corners, `color/surface` fill, 1px `color/outline` border, `elevation/level-1`. Internal Auto Layout vertical, `spacing/xs` between rows: row 1 is a horizontal Auto Layout with the role label ("Branch Manager", **title/medium**, `color/on-surface`) left-aligned and the held/total ("Held 42 / 128", **body/small** `font/family-mono`, `color/on-surface-variant`) right-aligned via `space-between` justification; row 2 is a horizontal Auto Layout with the truncated fingerprint ("sha256 1c7d0f4a…40f9a3", **body/small** `font/family-mono`, `color/on-surface-variant`) left-aligned and a text-style Copy button ("Copy", **label/large**, `color/primary`, no fill/no border — ghost/text button variant) right-aligned, both vertically centered.
3. **Search Field** (component `text-field`, search variant) — full width, fixed height 48px, `radius/sm` corners, `color/surface-variant` fill, no border. Auto Layout horizontal, `spacing/sm` internal padding `spacing/sm` (8px) left/right: a 20px search-glyph icon (`color/on-surface-variant`) at the leading edge, placeholder/value text "Search permission code" in **body/medium** `color/on-surface-variant` filling the remainder.
4. **Grouping List** — vertical Auto Layout, `spacing/sm` (8px) between each grouping row, three instances of the `expandable_section` component in this order: `portfolio` (expanded state — see Component Specifications §3 for its expanded sub-layout), `transaction_loan` (collapsed), `accounting` (collapsed).

### Frame: Permission Set Detail / Loading

Identical app-bar instance at the top. Below it, a vertical Auto Layout with `spacing/md` gaps reproduces the **exact same block structure** as the Content frame but with every content-bearing region swapped for a `shimmer-skeleton` component instance at matching dimensions: one shimmer block sized to the header card's footprint, one sized to the search field's footprint, and three shimmer blocks sized to a collapsed grouping row's footprint. Shimmer fill is `color/surface-variant` with a 1.5s pulse animation (opacity 0.6 → 1.0 → 0.6, ease-in-out, looping) — do not add any text, icon, or numeral inside a shimmer block.

### Frame: Permission Set Detail / Empty

App bar instance at the top. Below it, a **centered** vertical Auto Layout (`align: center`, both axes) fills the remaining frame height: a 96×96 illustration placeholder frame (`color/surface-variant` fill, `radius/lg` corners, centered glyph), then `spacing/md` gap, then the message "No permission set has been resolved for this role yet" in **body/large** `color/on-surface-variant`, center-aligned text, max width 280px so it wraps to two lines rather than spanning the full frame width.

### Frame: Permission Set Detail / Error

App bar instance at the top. Below it, a centered vertical Auto Layout: a 48px error-triangle icon in `color/error`, `spacing/sm` gap, the message "The permission catalog failed to load — showing the last cached set" in **body/large** `color/on-surface`, center-aligned, max width 300px, then `spacing/md` gap, then the Retry button (component `button-primary`, full label "Retry", `color/primary` fill, `color/on-primary` label, `radius/xl` corners, fixed height 48px, horizontal padding `spacing/md`).

---

## 3. Component Specifications

**`app-bar-detail`** (instance of the shared small M3 top-app-bar pattern): 393×56, `color/surface` fill, bottom 1px `color/outline-variant` stroke. Variants: default (as specified above). No trailing-action variant needed for this screen — build it with an empty trailing slot so the shared component's other instances (which do carry trailing icons on list screens) remain a single source of truth.

**Header `card`**: fill-width minus 32px total horizontal margin (16px each side), auto height, `radius/lg` (16px), `color/surface` fill, 1px `color/outline` stroke, `elevation/level-1`. Two internal rows as described in §2. **Content variant** (as shown): role + held/total + fingerprint + Copy button all populated. There is no loading/error/empty variant of this card — it only appears in the Content frame; other frames omit it entirely rather than showing a disabled version.

**`psd_copy_fingerprint`** (text-button variant, id from `ui.yaml`): no fill, no border, label "Copy" in **label/large** `color/primary`, 44×44dp minimum hit area even though the visible label is smaller (pad the hit target invisibly). On press, apply the system's `pressed` state-layer overlay (`color/on-surface` at 12% opacity per `state-layer.opacity.pressed`) clipped to the button's hit-area bounds. Add a Figma prototype interaction: **On Tap → Fire Snackbar** (see §4).

**`psd_search`** (search-variant `text-field`): 393px minus 32px margin wide, 48px tall, `radius/sm`, `color/surface-variant` fill, no stroke. Variants to build: **empty** (placeholder "Search permission code" in `color/on-surface-variant`), **focused** (add a 2px `color/primary` focus ring per `border.focus`), **filled** (value text in `color/on-surface`, placeholder replaced by the typed query, e.g. "LOAN"). Leading search-glyph icon persists across all three variants.

**`psd_grouping`** (`expandable_section` component, three instances: portfolio / transaction_loan / accounting): **collapsed variant** — single row, fill width, `radius/lg`, `color/surface` fill, 1px `color/outline` stroke, height 56px, horizontal Auto Layout `space-between`: a chevron-right icon + grouping name (**body/medium**, `color/on-surface`, e.g. "transaction_loan") on the leading side, the held/total badge (e.g. "6 / 9", **label/small** `font/family-mono`, `color/on-surface-variant`) on the trailing side. **Expanded variant** — same header row but chevron rotates to point down and gains a `color/primary-container` tint on the header background; below it, a nested vertical Auto Layout lists one row per code: a leading ✓/✗ glyph (`color/success` for held, `color/on-surface-variant` for not-held), the code name in **body/medium** `font/family-mono` `color/on-surface`, and the `entityName · actionName` meta in **label/small** `color/on-surface-variant` right-aligned. Each code row is 40px tall with a 1px `color/outline-variant` divider between rows (omit the divider after the last row).

**`shimmer-skeleton`** (loading placeholder): `color/surface-variant` fill, `radius/md` (12px) corners, no text/icon content, animated opacity pulse. Build three size presets as component variants — `header-card` (footprint matching the header card), `search-field` (footprint matching the search field), `grouping-row` (footprint matching a collapsed grouping row) — so the Loading frame simply instances the matching preset per position.

**`empty-state`**: centered vertical stack, illustration placeholder (96×96, `color/surface-variant`, `radius/lg`) + message text (`body/large`, `color/on-surface-variant`, center-aligned, max-width 280px). No CTA button variant on this screen (diagnostic-only empty state, no corrective action available).

**`button-primary`** (Retry): 48px height, `radius/xl` (28px) corners, `color/primary` fill, label "Retry" **label/large** `color/on-primary`, horizontal padding `spacing/md` (16px) each side, auto width (hug contents). Variants: **default** (as specified), **pressed** (apply `state-layer.opacity.pressed` = 12% `color/on-primary` overlay), **disabled** (not used on this screen — Retry is always enabled in the Error state).

---

## 4. Interaction Patterns

### Navigation Transitions

| From | To | Trigger | Animation |
|------|-----|---------|-----------|
| permission-capability-engine (`view_permission_set`) | Permission Set Detail (`loading`) | drill-in tap | slide_right 300ms `emphasized` easing |
| Permission Set Detail (any state) | permission-capability-engine | system back | slide_left 300ms `emphasized` easing |

This is a **leaf screen** — there is no forward navigation out of Permission Set Detail; every prototype connection either stays within the frame (state changes below) or exits via system back.

### In-Frame State Prototyping (Figma "Change to" transitions within one flow)

- **Loading → Content**: automatic after-delay trigger (simulate the local PermissionSet resolve + cache-first catalog join), **smart-animate** 300ms `standard-decelerate` easing, shimmer blocks cross-fade into their populated counterparts.
- **Loading → Empty**: alternate automatic transition (branch for the "no permission set resolved" demo path) — smart-animate 300ms fade.
- **Loading → Error**: alternate automatic transition (branch for the "catalog failed, no cache" demo path) — smart-animate 200ms fade, error block fades in.
- **Content → Content (grouping tap)**: tapping the `portfolio` grouping row toggles between the collapsed and expanded component variants — set as an **interactive component** variant swap (not a frame change) with a 200ms `standard` ease height animation as the code rows expand/collapse.
- **Content → Content (search typed)**: tapping into `psd_search` swaps it to its **focused** variant (instant, no animation — 150ms border-fade only); typing swaps to the **filled** variant showing the query text; this is best represented in Figma as a component-variant interactive swap rather than a frame change, since the surrounding grouping list re-filters in the real app (out of scope for static Figma frames — annotate with a sticky note: "grouping rows filter live in the implemented app; Figma shows the search field state only").
- **Content → Content (copy tap)**: tapping `psd_copy_fingerprint` fires a **Snackbar** overlay component ("Fingerprint copied", `color/inverse-surface` fill, `color/inverse-on-surface` text, bottom-anchored, `spacing/md` inset from the bottom edge) that auto-dismisses after 2500ms — model this as an overlay trigger with an after-delay auto-close back to the base Content frame.
- **Error → Loading**: tapping the Retry button navigates back to the Loading frame — smart-animate 200ms fade, models the `call_api` reload.

### Gesture Handling

- **Scroll**: the Content frame's grouping list is vertically scrollable once more than ~4 groupings are present (this demo shows 3, fitting without scroll on a 852px canvas) — mark the grouping-list Auto Layout frame as a scrolling container in the prototype settings.
- **Pull-to-refresh**: not applicable — this screen has no explicit refresh gesture; `OnLoad` runs once per entry and `OnRetry` is the only explicit reload path.
- **Long-press / swipe**: none declared for this screen.

### Animation Specifications

| Component | Type | Duration | Easing |
|-----------|------|----------|--------|
| shimmer-skeleton | opacity pulse | 1500ms | ease-in-out (looping) |
| grouping expand/collapse | height + chevron rotation | 200ms | standard `cubic-bezier(0.2,0,0,1)` |
| search field focus ring | border opacity | 150ms | standard |
| state frame transition (Loading→Content/Empty/Error) | cross-fade / smart-animate | 200–300ms | standard-decelerate `cubic-bezier(0,0,0,1)` |
| snackbar enter/exit | slide-up + fade | 250ms in / 200ms out | emphasized-decelerate / emphasized-accelerate |

---

## 5. Content Data

All copy below is sourced from `demo-data.yaml` and `docs.yaml` — zero placeholders, zero "Lorem ipsum", zero "Item 1"-style filler. Use these exact strings when populating Figma text layers.

**Header card**
- Role name: **"Branch Manager"**
- Held / total: **"Held 42 / 128"**
- Fingerprint (full): `sha256:1c7d0f4a92e63b58ad4f10c2e7b9d035f6a81e2c4b0d9f37a5c6e8b1d240f9a3`
- Fingerprint (truncated, as displayed): **"sha256 1c7d0f4a…40f9a3"**
- Copy button label: **"Copy"**

**Groupings and codes**

| Grouping | Held / Total | Codes shown (code · entity · action · held) |
|---|---|---|
| portfolio | 8 / 10 | `READ_CLIENT` · CLIENT · READ · ✓ held  ·  `CREATE_CLIENT` · CLIENT · CREATE · ✓ held  ·  `DELETE_CLIENT` · CLIENT · DELETE · ✗ not held |
| transaction_loan | 6 / 9 | `READ_LOAN` · LOAN · READ · ✓ held  ·  `APPROVE_LOAN` · LOAN · APPROVE · ✓ held  ·  `DISBURSE_LOAN` · LOAN · DISBURSE · ✗ not held |
| accounting | 4 / 12 | `READ_JOURNALENTRY` · JOURNALENTRY · READ · ✓ held  ·  `CREATE_JOURNALENTRY` · JOURNALENTRY · CREATE · ✗ not held |

**Search field**
- Placeholder: **"Search permission code"**
- Example typed query (for the focused/filled variant mock): **"LOAN"** — filters the visible set down to `READ_LOAN`, `APPROVE_LOAN`, `DISBURSE_LOAN` under `transaction_loan`, per `tests.yaml#search_filters_codes_in_vm`.

**Empty state**
- Message: **"No permission set has been resolved for this role yet"**

**Error state**
- Message: **"The permission catalog failed to load — showing the last cached set"**
- Button label: **"Retry"**

**Top app bar**
- Title: **"My Access"**

**Snackbar (copy confirmation)**
- Message: **"Fingerprint copied"** (implementation detail per `psd_copy_fingerprint`'s `copy_clipboard` effect + this design system's snackbar host contract; exact string finalized at implementation, shown here as the working design-handoff copy).

---

## 6. Responsive Rules

**Canvas**: base mobile-portrait canvas 393×852dp (Pixel-5-class reference), status bar 24dp, gesture nav bar 48dp (or 56dp for 3-button nav), leaving a 393×770dp safe content area matching `app-shell.yaml#safe_area` (`top: respect`, `bottom: respect`, `notch_handling: extend-and-pad`).

**Touch targets**: every tappable element — search field, grouping rows, Copy button, Retry button — meets the 44×44dp WCAG 2.5.8 minimum (`touch_targets.minimum`); the Retry button is sized to the 48dp comfortable tier (`touch_targets.comfortable`) since it is this screen's sole primary action.

**Font scaling**: supports system font scaling from 85% to 200%; the type scale is anchored to **body/medium** (14sp) as the reference size. At the largest scale steps, the header card's role/held-total row should wrap to two lines (its Auto Layout is already vertical-stacking-safe) rather than truncating the role name.

**Theme variants**: Light theme uses `colors.light.*` tokens throughout (as specified in §1); a dark-theme variant exists in `design-tokens.yaml#colors.dark` and should be built as a second Figma variable mode on the same components rather than duplicated frames — every token reference above already has its dark-mode hex noted for this purpose. System-default should follow the device setting.

**Adaptive layout (tablet / desktop, 600dp+)**: at the `tablet` breakpoint (600dp) and above, widen the header card and grouping list to a max content width of 640dp, centered, with the surrounding chrome (app bar) spanning full width; this screen does not need a two-column master-detail split (it is itself the "detail" side of a drill-in, not a list). At `desktop` (840dp+) the same 640dp-max-width centered column applies — no additional columns are introduced.
