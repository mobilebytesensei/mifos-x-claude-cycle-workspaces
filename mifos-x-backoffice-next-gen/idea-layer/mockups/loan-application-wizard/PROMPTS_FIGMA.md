# Loan Application Wizard — Figma Design Hand-off Prompts

> Generated from `screens/loan-application-wizard/ui.yaml` by `/idea-feature-mockup`
> Source hash: ui=126f8d53340f · Generated: 2026-07-31 · Design system: `design-tokens.yaml`
> Canvas: 393×852dp (Pixel 5), Material 3, **light theme default**, Roboto (Roboto Mono for money/term figures).

---

## §DS — Design System Variables (map once in Figma)

- **primary** `#0091EA` (active stepper node, Next/Submit fill) · **on-primary** `#FFFFFF` · **secondary** `#00796B` (Preview-schedule secondary accent) · **on-secondary** `#FFFFFF`
- **surface** `#FCFCFF` · **on-surface** `#1A1C1E` (values/figures) · **on-surface-variant** `#42474E` (labels) · **surface-variant** `#DEE3EB` (field fills + shimmer) · **outline** `#72777F` · **error** `#BA1A1A`
- **Type**: title-large 22/28 · title-medium 16/24 · label-large 14/20 · body-medium 14/20 · body-small 12/16 · mono = Roboto Mono for money, rate, term figures
- **Radius**: field sm 8 · button 28 · stepper nodes circular · **Spacing**: 16dp field gap

---

## Screen: Content (active wizard step)

Design the **content** state of the Loan Application Wizard for **mifos-x-backoffice-next-gen**, a clinical Material-3 financial-admin console. Light theme, 393×852dp.

Top app bar (56dp, `surface`): back arrow, title **"New Loan"** with a client subtitle **"Amina Hassan Ali"** in `body-small` `on-surface-variant`.

Below, a **horizontal stepper** (`lw_stepper`): four circular nodes with labels **① Product · ② Charges · ③ Schedule · ④ Review**. The active node is filled `primary #0091EA` with `on-primary` numeral; completed nodes show a check; upcoming nodes are outlined `outline`.

Body = the active step's **template-driven form** (`lw_field` × N, `dynamic_form_field`): each field is an outlined input (`surface-variant #DEE3EB` fill, radius 8, label above in `label-large` `on-surface-variant`, value in `body-medium` `on-surface`). Seed the Product step with real template-driven data: **Product** dropdown "Group Business Loan" (options: Group Business Loan · Emergency Loan · Asset Finance Loan); **Principal** "KES 50,000" (Roboto Mono, min/max from template); **Term** "12 Months" (12 repayments); **Interest** "2.0% · Declining balance"; **Officer** "Peter Kariuki"; processing fee "KES 500"; disbursement date "2026-08-01".

Footer controls: a **secondary/outlined button "Preview schedule"** (`lw_preview_schedule`, `secondary #00796B` accent) on the terms/charges steps, and a **filled primary button "Next"** (`lw_next`, bg `primary #0091EA`, `on-primary`) — enabled only when the current step passes template validation. On the Review step, replace Next with **"Submit"** (`lw_submit`, primary, CREATE_LOAN-gated). The Schedule step renders the previewed installment table (dueDate · principal · interest · fees · total, Roboto Mono, totals principal KES 50,000 / interest KES 6,500).

---

## Screen: Loading

Design the **loading** state. Keep the app bar and stepper. Render the step-form fields as **shimmer skeletons** (bg `surface-variant #DEE3EB`, 1.2s pulse) while the loan product template loads cache-first. No footer buttons.

---

## Screen: Empty

Design the **empty** ("client ineligible") state. Keep the app bar. Center a guidance block: a 48dp muted info icon (`on-surface-variant`), headline **"No eligible loan products"** in `title-medium`, sub-line "This client isn't eligible for any loan product yet." in `body-medium` `on-surface-variant`. No stepper/form.

---

## Screen: Error

Design the **error** state (template/calc/submit failed hard, no fallback). Keep the app bar. Center: 48dp `[!]` icon in `error #BA1A1A`, body copy in `body-medium` `on-surface-variant`, and a **filled primary button "Retry"** (`lw_error_retry`, bg `primary #0091EA`, `on-primary`, "Retry loading the loan application template"). Retry → Loading → Content (preserving captured form values where possible).

---

## Prototype Interactions

- Field edit → re-run template validators, toggle Next enablement (no network).
- Preview schedule tap → `POST /v1/loans?command=calculateLoanSchedule`, render installments on the Schedule step.
- Next / Back → advance/retreat the stepper in place.
- Submit tap (Review) → enqueue `POST /v1/loans` to the outbox; on success navigate to the new loan-detail; show a queued badge until sync.
- Retry → Error → Loading → Content.
- System back → return to the M04 loan list.
