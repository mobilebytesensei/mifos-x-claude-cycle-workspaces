# User Flows Index - mobile-wallet

> User journey documentation and flow diagrams

---

## Flow Summary

| Total | Documented | Pending |
|:-----:|:----------:|:-------:|
| 8 | 8 | 0 |

---

## Documented Flows

### Full App (Consolidated)

| Flow | File | Features | Screens | Priority | Status |
|------|------|----------|:-------:|:--------:|:------:|
| [Full App](flows/full-app/flow.mmd) | `full-app/flow.mmd` | ALL (25 features) | 540+ | P0 | ✅ |

### Authentication

| Flow | File | Features | Screens | Priority | Status |
|------|------|----------|:-------:|:--------:|:------:|
| [Authentication](flows/authentication/flow.mmd) | `authentication/flow.mmd` | auth, editpassword, profile, kyc | 15+ | P0 | ✅ |

### Navigation & Home

| Flow | File | Features | Screens | Priority | Status |
|------|------|----------|:-------:|:--------:|:------:|
| [Main Navigation](flows/main-navigation/flow.mmd) | `main-navigation/flow.mmd` | home, accounts, finance, notification | 7 | P0 | ✅ |

### Transfers

| Flow | File | Features | Screens | Priority | Status |
|------|------|----------|:-------:|:--------:|:------:|
| [Transfers](flows/transfers/flow.mmd) | `transfers/flow.mmd` | transfer-interbank, transfer-intrabank, beneficiary, standing-instruction | 12+ | P0 | ✅ |

### Payments

| Flow | File | Features | Screens | Priority | Status |
|------|------|----------|:-------:|:--------:|:------:|
| [Payments](flows/payments/flow.mmd) | `payments/flow.mmd` | payments, mpay-qr, mpay-qr-scan, fast-mpay, merchants, upi-setup | 14+ | P0 | ✅ |

### Financial Services

| Flow | File | Features | Screens | Priority | Status |
|------|------|----------|:-------:|:--------:|:------:|
| [Financial Services](flows/financial-services/flow.mmd) | `financial-services/flow.mmd` | invoices, savedcards, history, receipt | 10+ | P1 | ✅ |

### Settings & Support

| Flow | File | Features | Screens | Priority | Status |
|------|------|----------|:-------:|:--------:|:------:|
| [Settings](flows/settings/flow.mmd) | `settings/flow.mmd` | settings, faq | 16 | P1 | ✅ |

### Wallet Management

| Flow | File | Features | Screens | Priority | Status |
|------|------|----------|:-------:|:--------:|:------:|
| [Pocket](flows/FLOW-pocket.md) | `FLOW-pocket.md` | pocket | 5 | P1 | ✅ |

---

## Feature Coverage

| Feature | Flow | Sync Mode |
|---------|------|-----------|
| auth | authentication | bidirectional |
| editpassword | authentication | bidirectional |
| profile | authentication | bidirectional |
| kyc | authentication | bidirectional |
| home | main-navigation | bidirectional |
| accounts | main-navigation | bidirectional |
| finance | main-navigation | bidirectional |
| notification | main-navigation | bidirectional |
| transfer-interbank | transfers | bidirectional |
| transfer-intrabank | transfers | bidirectional |
| beneficiary | transfers | bidirectional |
| standing-instruction | transfers | bidirectional |
| payments | payments | bidirectional |
| mpay-qr | payments | bidirectional |
| mpay-qr-scan | payments | bidirectional |
| fast-mpay | payments | bidirectional |
| merchants | payments | bidirectional |
| upi-setup | payments | bidirectional |
| invoices | financial-services | bidirectional |
| savedcards | financial-services | bidirectional |
| history | financial-services | bidirectional |
| receipt | financial-services | bidirectional |
| settings | settings | bidirectional |
| faq | settings | bidirectional |
| pocket | pocket | bidirectional |

---

## Quick Actions

```bash
# View a flow
/flow [flow-name]

# Validate all flows
/flow-validate

# Generate feature from flow
/flow-to-design [flow-name]
```

---

## Flow Patterns Available

See `patterns/` directory for common flow patterns:
- auth-basic.mmd
- payment-confirm.mmd
- form-wizard.mmd
