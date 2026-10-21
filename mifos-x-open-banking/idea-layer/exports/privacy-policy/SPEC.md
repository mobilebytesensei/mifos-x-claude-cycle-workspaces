# SPEC — Privacy Policy

| Field         | Value                      |
|---------------|----------------------------|
| Feature       | privacy-policy             |
| Flavor        | shared                     |
| Status        | enriched                   |
| Quality Score | 92                         |
| ViewModel     | PrivacyPolicyViewModel     |

---

## Overview

The Privacy Policy screen is a shared, static-content legal screen accessible from both Consumer and Field Officer personas via the About screen's Legal card. It renders a GDPR-compliant policy document split into seven structured card sections: Data We Collect, Lawful Basis for Processing, How We Use Your Data, Third-Party Data Sharing, Data Retention, Your Rights Under GDPR, and Data Controller & DPO Contact.

A prominent green GDPR compliance banner at the top confirms compliance with UK GDPR, the Data Protection Act 2018, and EU GDPR Regulation 2016/679. Content is bundled as a local asset (no network call required for rendering) but the screen gracefully handles a loading skeleton (while the asset deserializes) and an error state with a Retry button in case the bundled asset is missing. The last-updated footer stamps "28 May 2026 — Version 1.0".

---

## Screens

| ID             | Name           | Route          | Layout | Scroll   |
|----------------|----------------|----------------|--------|----------|
| privacy-policy | Privacy Policy | /legal/privacy | Column | Vertical |

**Shell:** Top app bar ("Privacy Policy", back arrow). No bottom navigation bar.

---

## Components

| ID                       | Type     | Description                                                                                      |
|--------------------------|----------|--------------------------------------------------------------------------------------------------|
| pp_root                  | stack    | Column root with #F9FAEF background, 24dp padding                                               |
| pp_gdpr_banner           | banner   | Info variant — #CDEDA3 bg, radius 8, 16dp padding — GDPR compliance notice                     |
| pp_gdpr_banner_text      | text     | "This policy complies with UK GDPR, the Data Protection Act 2018, and EU GDPR…" — Outfit/body_small, #1A1C16 |
| pp_data_collection_card  | card     | White card (radius 12) — "Data We Collect" section                                              |
| pp_data_collection_header| text     | "Data We Collect" — Outfit/title_medium, #4C662B                                               |
| pp_data_collection_body  | text     | 5 categories: Identity, Contact, Financial, Technical, Authentication data — Outfit/body_medium, #44483D |
| pp_lawful_basis_card     | card     | White card — "Lawful Basis for Processing" section                                              |
| pp_lawful_basis_header   | text     | "Lawful Basis for Processing" — Outfit/title_medium, #4C662B                                   |
| pp_lawful_basis_body     | text     | 4 GDPR bases: Contract performance, Legal obligation, Legitimate interests, Consent — body_medium, #44483D |
| pp_purpose_card          | card     | White card — "How We Use Your Data" section                                                     |
| pp_purpose_header        | text     | "How We Use Your Data" — Outfit/title_medium, #4C662B                                          |
| pp_purpose_body          | text     | 7 specific purposes (account display, payments, KYC, fraud, push notifications, analytics) — body_medium, #44483D |
| pp_third_party_card      | card     | White card — "Third-Party Data Sharing" section                                                 |
| pp_third_party_header    | text     | "Third-Party Data Sharing" — Outfit/title_medium, #4C662B                                      |
| pp_third_party_body      | text     | 3 processors: OBP Limited (API), KYC providers, Firebase/Google — body_medium, #44483D        |
| pp_retention_card        | card     | White card — "Data Retention" section                                                           |
| pp_retention_header      | text     | "Data Retention" — Outfit/title_medium, #4C662B                                                |
| pp_retention_body        | text     | Schedules: 7yr transactions, 1hr tokens, 90d crash logs, 30d post-deletion — body_medium, #44483D |
| pp_user_rights_card      | card     | White card — "Your Rights Under GDPR" section                                                   |
| pp_user_rights_header    | text     | "Your Rights Under GDPR" — Outfit/title_medium, #4C662B                                        |
| pp_user_rights_body      | text     | 7 rights (Articles 15-22): Access, Rectification, Erasure, Portability, Restriction, Objection, Withdraw Consent — body_medium, #44483D |
| pp_dpo_card              | card     | White card — "Data Controller & DPO Contact" section                                            |
| pp_dpo_header            | text     | "Data Controller & DPO Contact" — Outfit/title_medium, #4C662B                                 |
| pp_dpo_controller_text   | text     | "Data Controller: Mifos Initiative, 1 World Trade Center, New York, NY 10007, USA" — body_medium, #44483D |
| pp_dpo_processor_text    | text     | "Data Processor (API services): Open Bank Project Limited, 11 Leadenhall Street, London EC3V 1LP" — body_medium, #44483D |
| pp_dpo_contact_text      | text     | "DPO: privacy@mifos.org. ICO complaint right at ico.org.uk." — body_medium, #44483D            |
| pp_last_updated_text     | text     | "Last updated: 28 May 2026 — Version 1.0" — Outfit/body_small, #C5C8BA, centred              |
| pp_loading_skeleton      | skeleton | Settings-variant shimmer — #F9FAEF bg, 24dp padding — while bundled asset deserializes         |
| pp_error_state           | stack    | Centred column — policy icon, error message, Retry button                                       |
| pp_error_icon            | icon     | "policy" icon — 48dp, #BA1A1A, centred                                                         |
| pp_error_message         | text     | "Unable to load Privacy Policy. Please check your connection and try again." — body_medium, #44483D, centred |
| pp_retry_button          | button   | "Retry" — outlined, border+text #4C662B, centred; fires retry_load → privacy-policy            |

---

## States

| ID      | Trigger                                   | Description                                                                 |
|---------|-------------------------------------------|-----------------------------------------------------------------------------|
| loading | Screen entry while bundle deserializes    | Full-screen skeleton shimmer; no interactive elements                       |
| content | Bundle successfully deserialized          | GDPR banner + 7 content cards + last-updated footer; full scroll            |
| empty   | Not applicable — policy always has content| Gracefully falls back to content state; empty_state: false                  |
| error   | Bundled asset load fails                  | policy icon + error message + Retry button; centred in viewport             |

---

## State Model

**ViewModel:** `PrivacyPolicyViewModel`
**Screen State Type:** `PrivacyPolicyUiState`

| Name          | Type    | Default |
|---------------|---------|---------|
| policyContent | String  | ""      |
| scrollPosition| Int     | 0       |
| isLoading     | Boolean | true    |

**Events:** `OnBack`, `OnRetry`, `OnScrollPositionChanged`

**Actions:** `onRetry()`, `onScrollPositionChanged(position: Int)`

**DI Dependencies:** `LegalContentRepository`

**Errors:**
- `load_failed`: "Failed to load Privacy Policy."

---

## Navigation

| From           | To    | Trigger         | Type |
|----------------|-------|-----------------|------|
| privacy-policy | about | back arrow tap  | pop  |

---

## API Endpoints

_No backend API dependencies — static/local screen._

The Privacy Policy renders from a bundled local asset. No OBP API calls are made. The `LegalContentRepository` reads from local app resources, not network.

---

## Design Tokens

| Token                           | Value   | Usage                                            |
|---------------------------------|---------|--------------------------------------------------|
| colors.light.primary            | #4C662B | All 7 section card headers                       |
| colors.light.primary_container  | #CDEDA3 | GDPR compliance banner background                |
| colors.light.on_surface         | #1A1C16 | GDPR banner text                                 |
| colors.light.on_surface_variant | #44483D | All body text in policy sections                 |
| colors.light.surface            | #FFFFFF | All 7 section cards                              |
| colors.light.background         | #F9FAEF | Screen and root stack background                 |
| colors.light.outline_variant    | #C5C8BA | Last-updated footer text                         |
| colors.light.error              | #BA1A1A | Error state policy icon color                    |
| typography.title_medium         | —       | All 7 section card headers                       |
| typography.body_medium          | —       | All policy body text; line_height 1.6            |
| typography.body_small           | —       | GDPR banner text, last-updated footer            |
| typography.label_large          | —       | Retry button text                                |
| radius.md                       | 12dp    | All content cards                                |
| radius.sm                       | 8dp     | GDPR compliance banner                           |
| spacing.lg                      | 24dp    | Root column padding                              |
| spacing.md                      | 16dp    | Card internal padding, margin_bottom between cards|

---

_Generated by /idea export | 2026-05-29_
