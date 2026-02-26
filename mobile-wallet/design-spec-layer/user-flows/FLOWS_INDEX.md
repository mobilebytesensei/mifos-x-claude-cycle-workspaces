# User Flows Index - mobile-wallet

> User journey documentation and flow diagrams

---

## Flow Summary

| Total | Documented | Pending |
|:-----:|:----------:|:-------:|
| 0 | 0 | TBD |

---

## Core Flows (To Be Created)

### Authentication Flows

| Flow | Screens | Priority |
|------|:-------:|:--------:|
| Login | 2-3 | P0 |
| Registration | 3-4 | P0 |
| Password Reset | 2-3 | P1 |
| 2FA Setup | 2-3 | P1 |

### Wallet Flows

| Flow | Screens | Priority |
|------|:-------:|:--------:|
| View Balance | 1-2 | P0 |
| Account Details | 2-3 | P0 |
| Transaction History | 2-3 | P0 |

### Transfer Flows

| Flow | Screens | Priority |
|------|:-------:|:--------:|
| P2P Transfer | 4-5 | P0 |
| Bank Transfer | 5-6 | P0 |
| Standing Instruction | 3-4 | P1 |

### Payment Flows

| Flow | Screens | Priority |
|------|:-------:|:--------:|
| QR Payment | 3-4 | P0 |
| Merchant Payment | 3-4 | P1 |
| Bill Payment | 3-4 | P1 |

### KYC Flows

| Flow | Screens | Priority |
|------|:-------:|:--------:|
| KYC Level 1 | 2-3 | P0 |
| KYC Level 2 | 3-4 | P1 |
| Document Upload | 2-3 | P1 |

---

## Quick Actions

```bash
# Create new flow
/flow-create [flow-name]

# View flow
/flow [flow-name]

# Validate flows
/flow-validate
```

---

## Flow Patterns Available

See `patterns/` directory for common flow patterns:
- auth-basic.mmd
- payment-confirm.mmd
- form-wizard.mmd
