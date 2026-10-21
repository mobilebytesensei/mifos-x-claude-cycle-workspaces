---
name: Open Banking — Trust Blue
version: 1.4.0
previous_version: 1.3.0
description: >-
  Material 3 design system for a UK Open Banking AISP + PISP reference app. Calm,
  trustworthy, data-legible retail banking that moves money across seven distinct payment
  rails and also publishes three unauthenticated Open Data surfaces. Accessibility-first,
  regulated-industry restraint. Seeded from the Material Theme Builder export (primary #266489).
aesthetic_family: minimalist-ui
theme: auto
colors:
  primary: "#266489"
  on_primary: "#FFFFFF"
  primary_container: "#C9E6FF"
  secondary: "#50606E"
  tertiary: "#64597B"
  background: "#F7F9FF"
  surface: "#F7F9FF"
  surface_container: "#EBEEF3"
  on_surface: "#181C20"
  on_surface_variant: "#41474D"
  outline: "#72787E"
  error: "#BA1A1A"
  positive: "#266489"
  negative: "#BA1A1A"
typography:
  brand: Roboto
  body: Roboto
  mono: Roboto Mono
  scale: default
rounded:
  none: 0
  small: 8
  medium: 12
  large: 16
  extra_large: 28
  full: 9999
spacing:
  base: 4
  screen_padding: 16
  density: comfortable
components:
  - card: { radius: "{rounded.medium}", container: "{colors.surface_container}", elevation: 1 }
  - button_filled: { container: "{colors.primary}", label: "{colors.on_primary}", radius: "{rounded.full}" }
  - list_item: { container: "{colors.surface}", supporting: "{colors.on_surface_variant}" }
  - amount: { font: "{typography.mono}", positive: "{colors.positive}", negative: "{colors.negative}" }
  - top_app_bar: { container: "{colors.surface}", title: "{colors.on_surface}" }
  - bottom_nav: { container: "{colors.surface_container}", active: "{colors.primary}" }
  - text_field: { radius: "{rounded.small}", outline: "{colors.outline}", focus: "{colors.primary}", error: "{colors.error}" }
  - amount_field: { font: "{typography.mono}", scale: headlineSmall, radius: "{rounded.small}" }
  - status_chip: { in_progress: "{colors.secondary}", success: "{colors.primary}", failure: "{colors.error}", established: "{colors.on_surface_variant}" }
  - review_card: { radius: "{rounded.medium}", container: "{colors.surface_container}", elevation: 1 }
  - mandate_health_chip: { active: "{colors.primary}", failing: "{colors.tertiary}", unpayable: "{colors.error}", revoked: "{colors.on_surface_variant}" }
---

## Overview

Open Banking — Trust Blue is the design language for a UK Open Banking **AISP + PISP**
reference app. The product reads a customer's bank data — accounts, balances, transactions,
statements — strictly with their consent, and **initiates domestic payments on their
instruction**. The design's job is therefore **trust and legibility**: the customer must
always feel their data is handled carefully, understand exactly what they are sharing, read
their finances at a glance, and — before any money moves — see precisely what they are about
to commit to.

> **Changed in 1.1.0.** Through 1.0.0 this app never moved money, and the system was written
> for a read-only product: no forms beyond search, no field validation, no irreversible
> actions, and a two-way money palette (credit / debit). Payment initiation breaks all four
> assumptions. The additions are confined to three areas — **form input and validation**,
> **payment disposition**, and the **irreversible-action contract** — plus a correction to
> the documented bottom-nav rail, which had been wrong since the 2026-07-28 reverse sync.
> No colour role, type scale, radius or spacing value changed.

> **Changed in 1.4.0.** Two capability areas landed after 1.3.0 was written, and the system
> described neither. Payment initiation went from one domestic form to **seven rails**
> (domestic and international × single / scheduled / standing-order, plus domestic VRP), and
> three **Open Data** surfaces appeared that are reachable with no session at all. The
> additions are again confined: a fourth payment disposition for the deferred rails, a
> **mandate-health** vocabulary that is not derived from consent status, the Open Data state
> vocabulary, and the irreversible-action contract widened from one screen to seven. No
> colour role, seed, font, type scale, radius, spacing value or dial changed — every new
> semantic maps onto a role the palette already ships, and every contrast figure quoted is a
> pair measured in an earlier release, not a new claim.

The aesthetic is **minimalist Material 3** — restrained, grid-aligned, low-motion. It is a
regulated-industry, accessibility-first system: high contrast, generous touch targets, and no
decorative noise that could obscure financial data. The mood is a calm trust-blue: a
desaturated steel-blue primary (#266489) on near-white surfaces, with a quiet slate secondary
and a soft violet tertiary for occasional accent.

## Colors

The palette is the verbatim Material 3 role set from the theme export (29 light + 29 dark
roles in `design-tokens.yaml`). Key roles:

- **Primary `#266489`** (dark mode `#95CDF7`) — the brand trust-blue. Used for primary
  actions, the active bottom-nav tab, links, and selected states. Sparingly — it should mark
  intent, not fill the screen.
- **Secondary `#50606E`** — neutral slate for supporting controls and secondary emphasis.
- **Tertiary `#64597B`** — soft violet. Carries the **warning / attention-needed** semantic as
  of 1.3.0 (consent nearing expiry, awaiting authorisation). It was previously reserved for PFM
  category accents and idle after the PFM screens were removed in the 2026-07-28 reverse sync.
  As of 1.4.0 it also carries **mandate "payments failing"** and the Open Data **`rate_limited`**
  state — both the same semantic: *attention needed, nothing has failed terminally*. Do **not**
  reach for it to differentiate the **disposition of a single payment** — those use the
  secondary/primary/error/neutral set below. Tertiary answers "act soon", never "what happened
  to this payment".
- **Surface / Background `#F7F9FF`** with the tonal surface-container ladder
  (`#FFFFFF → #E0E3E8`) for cards, sheets, and elevation without shadows.
- **Error `#BA1A1A`** — also doubles as the **negative/debit** money colour; positive/credit
  uses the primary blue (never green-on-red, to stay calm and colour-blind-safe).

### Payment disposition — a submitted payment is not a boolean

A successful submit returns `AcceptedSettlementInProcess`: accepted, **not settled**. Showing
that as success is a false statement about someone's money, so the system gives it its own
identity rather than folding it into a success/failure pair.

| Disposition | Role | Container / on-container | Icon | Contrast |
|---|---|---|---|---|
| **In progress** | `secondary` | `#D3E5F5` / `#384956` | `schedule` | 7.22:1 |
| **Settled** | `primary` | `#C9E6FF` / `#004B6F` | `check_circle` | 7.27:1 |
| **Rejected** | `error` | `#FFDAD6` / `#93000A` | `error` | 7.24:1 |
| **Instruction set up** | `onSurfaceVariant` | `#DDE3EA` / `#41474D` | `event_repeat` | 7.28:1 |

In progress is deliberately **not** primary. Primary is already the credit colour here, so a
primary chip would read as *money arrived*. Neutral slate reads as *working*.

**Instruction set up is new in 1.4.0, and it is a fourth state rather than a shade of the
other three.** Four of the seven rails — domestic and international scheduled, domestic and
international standing orders — are **deferred**: OBIE gives them no per-execution status at
all. Their terminal status is `InitiationCompleted` (INCO), which means *the instruction now
exists at the bank*, not *a payment happened*. None of the first three dispositions can say
that honestly. Settled would claim money moved. Rejected would claim failure. In progress
would claim something is currently happening, when nothing is — the instruction is simply
recorded and waiting for a date that may be months away.

So the fourth disposition is deliberately **neutral, not tonal**: `surfaceVariant` behind
`onSurfaceVariant`, the same pair the system already uses for unsigned running balances. A
neutral chip makes no claim about money, which is exactly the claim that can be made here.
Its icon is `event_repeat`, not a tick and not a clock, and its label names the **instruction**
— "Standing order set up", "Scheduled for 14 March" — never the money.

> The three tonal figures still sit within 0.041 of each other; the neutral fourth is measured
> at 7.28:1 (pair W-30) and lands inside that band by construction rather than by tuning. It is
> distinguished from the other three by having **no hue**, which is the point.

**This corrects a live gap, not just an omission.** The prior rule was "an OBIE status outside
the mapped vocabulary renders as *in progress*" — a safe default when the only unmapped codes
were rare failure modes. But `INCO` was unmapped and is the **terminal** status of four of the
seven rails, so that rule rendered every scheduled payment and every standing order as
perpetually *in progress*: a payment screen implying activity on an instruction that will not
execute until its due date. Fail-open-to-in-progress remains correct for genuinely unknown
codes, but `INCO` proves that rule is a safety net, not a substitute for mapping a status you
know exists. `BLCK` (Blocked) is **not** a second instance of that gap: `dtos/ObPaymentStatus.yaml`
— the source of truth for status mapping — lists it under `dispositions.terminal_failure.members`
alongside `RJCT`, by decision rather than by fall-through, so it takes the *Rejected* treatment.
(Corrected 2026-08-07; this paragraph previously described `BLCK` as still unmapped.)

**The three tonal contrast figures are a calibration, not a coincidence.** They sit within 0.041
of each other so no disposition shouts louder than the others — a rejected payment must not look
more urgent than one still settling, and one still settling must not look weaker than one that
landed. Any change to an `on*Container` value has to preserve that spread.

This also fixes the tone: on-container colours are **tone 30**, not tone 10. Pushing them to
near-black would raise contrast to ~13.3:1 and still pass AA, but at tone 10 the three
on-container values are indistinguishable from one another at a glance — the blue/slate/red
signal collapses to black, and this system's rule is *colour never alone*, which presumes the
colour is still legible. Higher contrast is not automatically better when it costs the hue.

> Hex literals are deliberately omitted from this paragraph. `preflight-mockup-theme-consistency`
> harvests the palette by scanning this file, so quoting a non-token hex here — even as a
> counter-example — silently widens the set it accepts. Role names only outside the tables above.

Renderers must take these values from `design-tokens.yaml`. A preview or component that derives
its own M3 tonal ramp will land near these numbers but not on them, and the drift is invisible
because it still passes every contrast gate. That is exactly what happened to the 95 rendered
preview cells on 2026-08-04 (finding W-1); see `state/DESIGN_SYSTEM_STATE.yaml#token_drift_2026_08_04`
for the nine roles and the correction table.

**Colour is never the only signal.** Every disposition carries its icon **and** its text
label. That is WCAG 1.4.1, and it is also what makes the rule auditable — a reviewer can read
the label and see whether a screen is claiming a settlement it does not have.

### Mandate health is not consent status

A VRP mandate has a second, independent axis, and 1.4.0 is the first release to say so. A
mandate can be **simultaneously authorised and incapable of paying**: consent reaches `AUTH`,
funds confirmation answers *Available*, and every payment then fails `U021` because the bank
wrote a debtor account the scheme will not accept. Reading health off the consent ladder would
render that mandate green and healthy while it silently pays nothing.

| Health | Role | Icon | Meaning | Contrast |
|---|---|---|---|---|
| **Active** | `primary` | `autorenew` | Set up, and payments are succeeding | 7.27:1 |
| **Payments failing** | `tertiary` | `schedule` | Authorised; recent payments rejected | 7.27:1 |
| **Cannot pay** | `error` | `error` | Authorised, but structurally unable to pay | 7.24:1 |
| **Cancelled** | `onSurfaceVariant` | `block` | Revoked — terminated, muted | 7.28:1 |

**Three of these four coexist with `Data.Status == AUTH`.** Health is derived from *payment
outcomes*, never from the status ladder — the ladder goes `AWAU → AUTH` and then stays `AUTH`
regardless of whether a single payment ever succeeds. Any renderer that colours this chip from
consent status is wrong by construction, no matter which colours it picks.

Two of these reuse pairs from other blocks, and one of those reuses needs a guard.
**Cannot pay** is `error` even though nothing the customer did failed — the same reading the
rejected disposition gets, and for the same reason: red marks *the bank did not make the
payment*, not *you made a mistake*. And **Active** reuses the `primary` pair that
`terminal_success` also uses, which is the one place this vocabulary can lie: primary here must
not be read as *paid*. It is held apart by its icon (`autorenew`, never `check_circle`) and by
its label, which names the mandate's state and never an amount. That reuse is recorded as an
open divergence in `state/DESIGN_SYSTEM_STATE.yaml` rather than silently blessed.

### Open Data surfaces have a different state vocabulary

Three screens — **atm-locator**, **branch-locator** and **products** — read public Open Data
APIs that declare no security scheme and return no 401 and no 403 on any path. They are
reachable with **no session, no token and no consent**, and they are the only screens a
prospective customer sees before connecting anything.

That is a design constraint, not a footnote: **a sign-in prompt or a session-expired state on
these three screens is unreachable code and a misleading message.** The authenticated screens'
vocabulary does not transfer. `consent-list` correctly ships an `error_auth` state with a
`lock_open` glyph and a *Sign in again* CTA; on an Open Data screen that state cannot occur, so
rendering it would tell a customer to fix a credential problem that does not exist.

Their state vocabulary is therefore `loading · content · empty · error · no_network`, plus
`rate_limited` and — where the screen asks for device location — `location_denied`:

- **`rate_limited`** is the state to actually design for. These are unauthenticated public APIs
  rate-limited by origin, so a map that refetches on every pan will hit 429. It is a *wait*,
  not a failure: `tertiary`, the warning role, with a "try again in a moment" message — never
  `error`, which would frame a working public API as broken.
- **`location_denied`** is a **supported path, not an error**. Refusing location leaves the
  screen fully useful via postcode, town or sort-code search, so it renders as an informational
  state with the search affordance in focus — not the error layout with a retry button.
- **`empty`** means the bank published nothing (no ATMs, no branches in radius, no catalogue) —
  never "you have nothing", which is what empty means on an authenticated screen.

`branch-locator` is the conforming model here and states the rule in its own YAML.
`atm-locator` and `products` each still declare an `unauthenticated` state their own `api.yaml`
says is unreachable; that is a screen-layer defect recorded in the state file, not something
this file can fix.

### Warning and success have no hue of their own

This palette ships M3's five families and no more. There is no amber and no green, so
**warning maps to tertiary and success maps to primary** — the same move the disposition table
above makes, for the same reason: a new tonal family is four more pairs to keep accessible
across two themes and two contrast variants, to say something the existing palette already
distinguishes.

| Semantic | Role | Container / on-container | Icon | Contrast |
|---|---|---|---|---|
| **Warning** (attention needed) | `tertiary` | `#EADDFF` / `#4C4162` | `schedule` | 7.27:1 |
| **Success** (terminal) | `primary` | `#C9E6FF` / `#004B6F` | `check_circle` | 7.27:1 |

Warning is **tertiary, not error**. A consent expiring in seven days has not failed — the
customer still has full access and a working reconfirm path. Error-red would frame a live,
healthy connection as broken. Error stays reserved for **Revoked, Rejected and Expired**, where
access is actually gone. "Act soon" and "too late" must not share a colour.

All foreground/background pairs meet **WCAG AA** — 32 pairs measured (15 at 1.1.0, 4 more for
the status semantics at 1.3.0, and 13 more in the 2026-08-02 corpus-wide pass over the pairs
the screens actually compose), ratios recorded in `state/DESIGN_SYSTEM_STATE.yaml`. **1.4.0 adds
no new pair**: the fourth disposition and all four mandate-health states reuse pairs already
measured (W-30, W-02/W-05, W-16/W-17, W-03/W-06), which is a consequence of minting no new hues
rather than a shortcut. One measured pair **fails** and is constrained rather than used —
`outlineVariant` on `surface` at 1.62:1 (W-32) is decorative-only and must never bound a control
or carry a glyph. Theme is **auto** (follows the OS), with dynamic colour enabled on Android 12+.

## Typography

**Roboto** throughout (Material 3 default), with **Roboto Mono** for monetary amounts and
account/sort-code numbers so figures align and scan cleanly. The full M3 type scale is in
`design-tokens.yaml`. Conventions:

- Screen titles: `headlineSmall` (24).
- Account balance / hero figures: `displaySmall`–`headlineMedium`, mono.
- List primary text: `bodyLarge` (16); supporting: `bodyMedium` (14) on `on_surface_variant`.
- Buttons / tabs: `labelLarge` (14, medium).

Avoid more than two type sizes per card. Let whitespace, not weight, create hierarchy.

## Layout

A single-column, **8dp grid**. Screen padding 16dp; comfortable density (`design_read`
density 5). Content is organised into M3 cards on the surface-container ladder. Lists are the
dominant pattern (accounts, transactions, beneficiaries) — full-width rows with a leading
glyph, primary + supporting text, and a trailing value or chevron. Detail screens use a
top-app-bar + scrollable content with grouped, labelled sections.

The app shell is a bottom-navigation scaffold: **Home · Accounts · Pay · More**. (Corrected in
1.1.0 — this section previously documented "Accounts · Transactions · Consents · Settings",
which stopped being true at the 2026-07-28 reverse sync. Transactions is reached from account
detail and from Home's "View all", never from a tab; consents live under More → Settings.)

**Multi-step forms** — introduced in 1.1.0 for the single send-money screen, and as of 1.4.0 the
shape of **all seven payment rails** — advance one step per screenful rather than scrolling one
long form: choose the funding account and payee, then the amount, then review. Each step ends in
a single primary action; the step indicator is textual, not a decorative progress bar, in keeping
with the low-motion dial. (The 1.1.0 text called this pattern provisional because one screen used
it. Seven rails is no longer a sample — it is the dominant input pattern in the app.)

**The seven rails are one family, and the family is the hub — not the form.** The rails share
chrome, type, spacing and disposition vocabulary, but they must **not** share a single generic
form, because their real differences are not cosmetic:

- The **amount field is mutually exclusive across rails**. A domestic standing order sends
  `FirstPaymentAmount` and is refused (`U005`) if given `InstructedAmount`; an international
  standing order is the exact inverse. One field that "adapts" would be one field that is wrong
  half the time.
- **The three international rails refuse a reference field entirely** — `RemittanceInformation`
  returns `U005` — and instead *require* a charge-bearer choice that no domestic rail has.
- **Only the two single-payment rails have funds confirmation.** The four deferred rails have no
  such endpoint, so a "checking funds" step must not appear on them.

The design consequence is the **payments hub**: seven tiles presenting seven distinct choices,
each landing on a form shaped for its own rail. A generic form flattens differences the bank
will reject, and it does so *after* the customer has filled it in. Choosing the rail first is
what makes each form able to be honest.

## Elevation & Depth

Depth comes from **tonal surface containers**, not heavy shadows (M3 tonal elevation). Cards
sit on `surface_container` at elevation 1; sheets/dialogs at level 3. Keep elevation shallow —
a calm, flat banking surface reads as trustworthy. Reserve the highest containers for sticky
headers and the bottom-nav bar.

## Shapes

Soft, consistent rounding: small 8 / medium 12 / large 16 / extra-large 28dp. Cards use
`medium`; buttons are `full` (pill); bottom sheets use `extra_large` top corners. No sharp
0dp corners (that reads brutalist/cold for a consumer banking app).

## Components

- **Account / transaction list item** — leading category or bank glyph, primary label,
  supporting line (date / account type), trailing **mono amount** coloured positive (primary)
  or negative (error). 48dp min height.
- **Balance card** — hero mono figure, account label, available-vs-current sub-line.
- **Consent card** — clear "what you're sharing" permission list, expiry, and a revoke action;
  this is the trust-critical surface — always explicit, never truncated.
- **Filled button** (primary action), **outlined / text button** (secondary).
- **Top app bar** + **bottom navigation** per the app shell.
- **State surfaces** — every data screen renders loading (skeleton), content, empty, and error
  (with retry) states. Forms add **submitting**. Payment screens add a **terminal** state, which
  is the disposition the rail actually reached — settled, rejected or instruction-set-up — never
  a generic "success". Open Data screens use the variant vocabulary in §Colors and carry **no**
  authentication state.

Added in 1.1.0 for payments:

- **Text field** — 8dp radius (tighter than a card's 12dp), 56dp min height, label above,
  helper or error text below. Validation runs **on change after the first blur**: flagging a
  half-typed amount as wrong reads as hostile, but waiting until submit makes correction slow.
- **Amount field** — mono `headlineSmall`, currency symbol as a non-editable prefix. Mono so
  digits don't reflow while typing. Held and validated as minor units; displayed formatted.
- **Status chip** — the four dispositions above (the three tonal ones plus the neutral
  *instruction set up*); icon + label always, colour never alone. This line read "the disposition
  triad" from 1.1.0 through 1.3.0; `instruction_established` made it four in 1.4.0. Anything
  quoting the older wording is quoting a superseded revision, not a fourth-less contract.
- **Review card** — the last surface before money moves. Lists every value that will be
  committed: funding account, payee, amount, reference. Nothing summarised, nothing truncated.
  It is to payments what the consent card is to data sharing, and it is trust-critical in the
  same way.

Added in 1.4.0 for the seven rails and Open Data:

- **Mandate health chip** — the four-state VRP vocabulary above. Structurally a status chip, but
  a **separate component on purpose**: it must never be fed from consent status, and giving it
  its own identity is what stops a generator wiring it to the status ladder because the two look
  alike.
- **Rail tile** — one of the seven entries on the payments hub. Carries the rail's name and the
  one sentence that distinguishes it (immediate / on a date / repeating / mandate). Tiles are
  uniform in weight: no rail is promoted as the default, because "the usual one" is a domestic
  assumption that the international rails do not share.
- **Open Data state surfaces** — `rate_limited` (tertiary, a wait) and `location_denied`
  (informational, with the search affordance in focus, **not** the error layout). Neither is an
  error state, and neither has a sign-in path.

**Extended in 1.4.0** — the **review card** was specified for one screen and its row order
(`funding_account · payee · amount · reference`) was that screen's row order. It now precedes
every one of the seven rails, so the rows are the rail's committed values rather than a fixed
list: the three international rails have **no reference row** and gain a charge-bearer row, and
the deferred rails commit a *schedule* whose first row is the date or frequency. The rule that
does not flex is RC-1 — every value that will be committed appears in full, nothing summarised,
nothing truncated. The CTA label pattern flexes too, and must: **"Send £850.00" is only true on
the two single-payment rails.** A standing order commits an instruction, not a transfer, so its
CTA says what is actually being created — "Set up standing order" — because a customer who taps
"Send £850.00" and sees no money leave has been told something false.

**Removed in 1.1.0** — `category_chip`, `chart_donut` and `progress_budget` were declared for
PFM screens that were never built and were deleted on 2026-07-28. They are struck from the
catalog rather than left as aspirational entries a generator might try to satisfy.

## Do's and Don'ts

**Do**
- Keep primary blue for intent and the active tab only; let surfaces stay near-white/dark-grey.
- Show money in mono, credit in primary, debit in error.
- Make consent explicit: full permission list, expiry, easy revoke.
- Maintain WCAG AA contrast and 48dp touch targets everywhere.
- Show a review surface listing every committed value before money moves, with a same-weight
  escape beside the confirm.
- Label the confirm CTA with the action **and the amount** — "Send £850.00", not "Confirm" — on
  the rails where money moves now. On a deferred rail, name what is being created instead.
- Lock the CTA and show progress on tap, so double-submission is impossible from the UI.
- Show running balances **unsigned**, in neutral.
- Treat all seven rails as irreversible. Money movement cannot be undone the way account reading
  can, and a standing order is *more* consequential than a single payment, not less — it commits
  future money the customer will not be asked about again.
- Say what a rail cannot do, on the rail. An international payment has no reference field; a
  scheduled payment has no funds check. Absent affordances are explained, not silently missing.

**Don't**
- Don't use green/red money semantics or celebratory colour — this is calm, regulated finance.
  This applies with full force to a completed payment: a settled payment gets the trust-blue
  chip, not a green tick and not a celebration.
- Don't render an in-progress payment as sent, complete, or successful — see Payment disposition.
  `ACSP` persists for **minutes** on a payment that will succeed, because settlement is batched on
  five-minute boundaries. That wait is normal and must not be styled as a problem or hurried with
  a faster poll.
- Don't colour a payment confirm CTA `error` on any of the seven rails. Red frames a payment the
  customer intends as a danger; red is reserved for genuine failure. Weight comes from the review
  surface and the amount in the label.
- Don't imply a deferred rail has paid. Scheduled payments and standing orders have **no
  per-execution status** — `InitiationCompleted` means the instruction exists, not that money
  moved. No tick, no "sent", no "complete", no amount-in-the-past-tense.
- Don't colour a mandate-health chip from consent status. Three of the four health states coexist
  with `AUTH`, so a mandate that pays nothing would render as healthy.
- Don't render a sign-in prompt, a session-expired state, or a "Sign in again" CTA on
  atm-locator, branch-locator or products. Those APIs return no 401 and no 403 — the state is
  unreachable, and the message would be false.
- Don't style `rate_limited` as an error. An unauthenticated public API that is rate-limiting is
  working correctly; it is a wait, not a fault.
- Don't sign a running balance off a per-transaction credit/debit indicator — that indicator
  describes the transaction, not the balance, and signing on it renders a healthy account
  negative.
- Don't add gradients/shadows for decoration (low-motion, low-variance system).
- Don't truncate or hide what data is being shared, or what a payment will commit.
- Don't pin a `data-theme` — honour the OS (auto theme).
