# SPEC — Terms of Service

| Field         | Value                      |
|---------------|----------------------------|
| Feature       | terms-of-service           |
| Flavor        | shared                     |
| Status        | enriched                   |
| Quality Score | 92                         |
| ViewModel     | TermsOfServiceViewModel    |

---

## Overview

The Terms of Service screen is a shared legal content screen accessible from both Consumer and Field Officer flavors. It renders a scrollable collection of legal section cards — Agreement Overview, Acceptance of Terms, Account Usage, Data Handling via OBP API, Prohibited Uses, Limitation of Liability, Dispute Resolution, and Governing Law — each as a white M3 card on a warm off-white background. The screen is primarily static (content bundled or fetched from a legal content repository). A "Last updated: 28 May 2026 — Version 1.0" footer anchors the document. Error and loading states handle the edge case where asset deserialization fails. No backend API is required for nominal operation.

---

## Screens

| ID               | Name             | Route         | Layout | Scroll   |
|------------------|------------------|---------------|--------|----------|
| terms-of-service | Terms of Service | /legal/terms  | Column | Vertical |

**Shell:** Top app bar with back arrow. No bottom navigation bar.

| Element         | Value              |
|-----------------|--------------------|
| Title           | "Terms of Service" |
| Navigation icon | arrow_back         |
| Navigation action | navigate_back    |

---

## Components

| ID                          | Type     | Description                                                                                          |
|-----------------------------|----------|------------------------------------------------------------------------------------------------------|
| tos_root                    | stack    | Root column, background `#F9FAEF`, padding 24dp (spacing.lg)                                        |
| tos_scroll_content          | stack    | Scrollable column containing all legal section cards                                                 |
| tos_intro_card              | card     | "Agreement Overview" section — white `#FFFFFF`, radius 12dp, padding 16dp                          |
| tos_intro_header            | text     | "Agreement Overview" — Outfit/title_medium, `#4C662B`                                              |
| tos_intro_body              | text     | "These Terms of Service govern your use of Mifos X Open Banking…" — Outfit/body_medium, `#44483D`  |
| tos_acceptance_card         | card     | "Acceptance of Terms" section card                                                                   |
| tos_acceptance_header       | text     | "Acceptance of Terms" — Outfit/title_medium, `#4C662B`                                             |
| tos_acceptance_body         | text     | "By creating an account or continuing to use Mifos X Open Banking after changes…" — Outfit/body_medium, `#44483D` |
| tos_account_usage_card      | card     | "Account Usage" section card                                                                         |
| tos_account_usage_header    | text     | "Account Usage" — Outfit/title_medium, `#4C662B`                                                   |
| tos_account_usage_body      | text     | "You are responsible for maintaining the confidentiality of your DirectLogin credentials…" — Outfit/body_medium, `#44483D` |
| tos_data_handling_card      | card     | "Data Handling via Open Bank Project API" section card                                               |
| tos_data_handling_header    | text     | "Data Handling via Open Bank Project API" — Outfit/title_medium, `#4C662B`                         |
| tos_data_handling_body      | text     | "This application connects to banking services via the Open Bank Project (OBP) REST API…" — Outfit/body_medium, `#44483D` |
| tos_prohibited_card         | card     | "Prohibited Uses" section card                                                                       |
| tos_prohibited_header       | text     | "Prohibited Uses" — Outfit/title_medium, `#4C662B`                                                 |
| tos_prohibited_body         | text     | "You must not use this application to: (a) initiate fraudulent…" — Outfit/body_medium, `#44483D`   |
| tos_liability_card          | card     | "Limitation of Liability" section card                                                               |
| tos_liability_header        | text     | "Limitation of Liability" — Outfit/title_medium, `#4C662B`                                         |
| tos_liability_body          | text     | "To the maximum extent permitted by law, the Mifos Initiative shall not be liable…" — Outfit/body_medium, `#44483D` |
| tos_dispute_card            | card     | "Dispute Resolution" section card                                                                    |
| tos_dispute_header          | text     | "Dispute Resolution" — Outfit/title_medium, `#4C662B`                                              |
| tos_dispute_body            | text     | "We encourage you to contact us at legal@mifos.org before initiating any formal dispute…" — Outfit/body_medium, `#44483D` |
| tos_governing_law_card      | card     | "Governing Law" section card                                                                         |
| tos_governing_law_header    | text     | "Governing Law" — Outfit/title_medium, `#4C662B`                                                   |
| tos_governing_law_body      | text     | "These Terms of Service are governed by… laws of England and Wales…" — Outfit/body_medium, `#44483D` |
| tos_last_updated_text       | text     | "Last updated: 28 May 2026 — Version 1.0" — Outfit/body_small, `#C5C8BA`, centered                |
| tos_loading_skeleton        | skeleton | settings-variant shimmer block; background `#F9FAEF`, padding 24dp                                  |
| tos_error_state             | stack    | Centred column: tos_error_icon + tos_error_message + tos_retry_button                               |
| tos_error_icon              | icon     | gavel 48dp, `#BA1A1A`, centered                                                                     |
| tos_error_message           | text     | "Unable to load Terms of Service. Please check your connection and try again." — Outfit/body_medium, `#44483D`, centered |
| tos_retry_button            | button   | "Retry" — outlined variant, border `#4C662B`, text `#4C662B`, Outfit/label_large                   |

---

## States

| ID      | Trigger                           | Description                                                                     |
|---------|-----------------------------------|---------------------------------------------------------------------------------|
| loading | Screen entry                      | Settings-variant shimmer skeleton while bundled content deserializes            |
| content | Content loaded successfully       | All 8 legal section cards + last-updated footer visible; scrollable             |
| error   | Bundled asset load failure        | Centred gavel icon + error message + Retry button                               |
| empty   | (not applicable)                  | TOS always has static content — falls back to content state with bundled copy   |

---

## State Model

**ViewModel:** `TermsOfServiceViewModel`
**Screen State Type:** `TermsOfServiceUiState`

| Name           | Type    | Default |
|----------------|---------|---------|
| termsContent   | String  | ""      |
| scrollPosition | Int     | 0       |
| isLoading      | Boolean | true    |

**Events:** `OnBack`, `OnRetry`, `OnScrollPositionChanged`

**Actions:** `onRetry()`, `onScrollPositionChanged(position: Int)`

**DI Dependencies:** `LegalContentRepository`

**Errors:**
- `load_failed`: "Failed to load Terms of Service."

---

## Navigation

| From             | To    | Trigger                   | Type |
|------------------|-------|---------------------------|------|
| terms-of-service | about | Back arrow / OnBack event | pop  |

---

## API Endpoints

_No backend API dependencies — static/local screen._

Terms of Service content is bundled with the application or loaded from `LegalContentRepository` (local asset, not a network call). No OBP API endpoints are invoked.

---

## Design Tokens

| Token                          | Value   | Usage                                              |
|--------------------------------|---------|----------------------------------------------------|
| color.light.primary            | #4C662B | Section header text in all cards                   |
| color.light.on_surface_variant | #44483D | Body text paragraphs in all section cards          |
| color.light.outline_variant    | #C5C8BA | Last-updated footer text                           |
| color.light.error              | #BA1A1A | Error state gavel icon                             |
| color.light.surface            | #FFFFFF | Section card backgrounds                           |
| color.light.background         | #F9FAEF | Screen background, skeleton shimmer base           |
| typography.title_medium        | —       | Section header labels (16sp/500)                   |
| typography.body_medium         | —       | Section body paragraphs (14sp/400, line-height 1.6)|
| typography.body_small          | —       | Last-updated footer text (12sp/400)                |
| typography.label_large         | —       | Retry button text (14sp/500)                       |
| radius.md                      | 12dp    | Section card border radius                         |
| spacing.lg                     | 24dp    | Screen horizontal/vertical root padding            |
| spacing.md                     | 16dp    | Card internal padding, gap between cards           |
| spacing.sm                     | 8dp     | Section header padding-bottom                      |
| spacing.xl                     | 32dp    | Scroll content bottom padding, footer bottom pad   |

---

_Generated by /idea export | 2026-05-29_
