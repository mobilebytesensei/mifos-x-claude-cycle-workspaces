# feature-layer

> Last updated: 2026-05-28 (auto-populated by /project-verify)

| Attribute | Value |
|---|---|
| **Maturity** | partial |
| **Status** | idea-layer complete (39 screens approved); implementation not started |
| **Tech** | Compose Multiplatform 1.8.2 + BaseViewModel + ScreenDataStream |
| **Next** | Run `/kmp-implement {feature}` per approved screen |

## Declared Features (from PROJECT_CONFIG.yaml)

**App shell:** splash, login, profile, settings  
**Consumer:** home, accounts, transactions, send-money, beneficiaries, cards, standing-orders, atm-locator, fx-rates

> The Field Officer feature set was removed on 2026-08-02 — this is a consumer-only app.

## Notes

- `LAYER_GUIDE.md` present with BaseViewModel + ScreenDataStream patterns
- No Kotlin feature implementations yet (source is kmp-project-template scaffold)
- Template residue pending removal: `feature/crypto`, `feature/currency-rates`, `feature/emi-calculator`
