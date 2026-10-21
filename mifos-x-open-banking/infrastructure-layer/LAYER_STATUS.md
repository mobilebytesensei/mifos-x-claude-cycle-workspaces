# infrastructure-layer

> Last updated: 2026-05-28 (auto-populated by /project-verify)

| Attribute | Value |
|---|---|
| **Maturity** | bootstrap |
| **Status** | Gradle + KMP + Koin + cmp-navigation in place (from kmp-project-template) |
| **Tech** | Koin 4.1.0 + koin-annotations 2.1.0, Jetpack Navigation Compose (type-safe @Serializable routes) |
| **Flavor** | none — single variant since 2026-08-02 (the consumer / fieldOfficer split was dropped with the field-officer persona) |
| **Next** | Run `/kmp-implement` for each feature to wire Koin modules + navigation routes |

## Notes

- `LAYER_GUIDE.md` present with Koin DI + navigation patterns
- `cmp-navigation` module is the navigation entry point; no flavor gating
- CI workflows present in source repo (GitHub Actions)
- No framework-side infrastructure files yet — awaiting feature implementation
