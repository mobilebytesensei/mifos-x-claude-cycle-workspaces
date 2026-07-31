# Idea Layer Changelog — CommonPurse

## v1.0.0 (2026-05-08)
- 30 screens enriched to `designed` status across 15 features
- Fineract API coverage: 55+ endpoints + 10 custom datatables
- Two client types: Admin (group management) + End User (self-service)
- Offline-first architecture with sync queue design
- Corpus tracking with loan disbursement blocking
- Export tracking added to all 30 screen YAMLs
- journeys/ directory: 10 user journeys (7 critical + 3 medium)
- dtos/ directory: 12 DTOs covering all Fineract entities + custom datatables
- components.yaml: 10 project-specific components (CommonPurse banking domain)
- DESIGN_CONTEXT.md: full design brief (offline-first, rural UX, color system)
- PROJECT_CONFIG.yaml: schema v2 with branding, client_types, backend environments

## v0.9.0 (2026-05-07)
- Completeness pass: added missing screens from /idea completeness
- Added: loan-mark-defaulted-dialog, loan-repayment-dialog, settings-logout-dialog
- Added: member-savings-detail screen
- Total screen count: 28 → 30
- FEATURES.md Screen Inventory updated: 28 → 30 screens

## v0.8.0 (2026-05-06)
- Initial enrichment pass on 25 core screens
- TRAINING_MASTER.yaml generated from enriched screen YAMLs
- design-tokens.yaml established (CommonPurse green/amber/blue palette)
- Component registry seeded with banking domain types
- State models defined for all ViewModels

## v0.1.0 (2026-05-05)
- Initial idea-plan.yaml scaffolded
- 15 features identified from VSLA community research
- FEATURES.md + REQUIREMENTS.md created
- idea-plan.yaml with two client types (admin + end_user)
- Fineract MCP bridge run: 65 MCP tools resolved
- 10 custom datatables designed for missing Fineract capabilities
- [design-system-stitch] 2026-07-31 — DESIGN.md uploaded to Stitch (asset_id=18068522450062802666, design_md_sha=c3a638b3a935)
