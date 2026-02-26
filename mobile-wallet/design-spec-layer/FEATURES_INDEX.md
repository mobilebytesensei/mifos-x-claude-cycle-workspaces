# Features Index - mobile-wallet

> 31 features (23 implemented + 8 planned)

---

## Feature Summary

| Total | Implemented | Planned | In Progress |
|:-----:|:-----------:|:-------:|:-----------:|
| 31 | 23 | 8 | 0 |

---

## Features by Category

### Authentication & Security

| Feature | Screens | VMs | SPEC | API | STATUS | MOCKUP |
|---------|:-------:|:---:|:----:|:---:|:------:|:------:|
| [auth](features/auth/) | 4 | 3 | ⬜ | ⬜ | ⬜ | ⬜ |
| [editpassword](features/editpassword/) | 1 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [kyc](features/kyc/) | 4 | 4 | ⬜ | ⬜ | ⬜ | ⬜ |
| [upi-setup](features/upi-setup/) | 4 | 0 | ⬜ | ⬜ | ⬜ | ⬜ |

### Core Wallet Features

| Feature | Screens | VMs | SPEC | API | STATUS | MOCKUP |
|---------|:-------:|:---:|:----:|:---:|:------:|:------:|
| [home](features/home/) | 1 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [accounts](features/accounts/) | 5 | 5 | ⬜ | ⬜ | ⬜ | ⬜ |
| [profile](features/profile/) | 2 | 2 | ⬜ | ⬜ | ⬜ | ⬜ |
| [settings](features/settings/) | 1 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |

### Transfers & Payments

| Feature | Screens | VMs | SPEC | API | STATUS | MOCKUP |
|---------|:-------:|:---:|:----:|:---:|:------:|:------:|
| [payments](features/payments/) | 3 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [transfer-intrabank](features/transfer-intrabank/) | 4 | 3 | ⬜ | ⬜ | ⬜ | ⬜ |
| [transfer-interbank](features/transfer-interbank/) | 5 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [fast-mpay](features/fast-mpay/) | 1 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [standing-instruction](features/standing-instruction/) | 3 | 3 | ⬜ | ⬜ | ⬜ | ⬜ |

### QR & Merchants

| Feature | Screens | VMs | SPEC | API | STATUS | MOCKUP |
|---------|:-------:|:---:|:----:|:---:|:------:|:------:|
| [mpay-qr](features/mpay-qr/) | 1 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [mpay-qr-scan](features/mpay-qr-scan/) | 2 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [merchants](features/merchants/) | 2 | 2 | ⬜ | ⬜ | ⬜ | ⬜ |

### Financial Services

| Feature | Screens | VMs | SPEC | API | STATUS | MOCKUP |
|---------|:-------:|:---:|:----:|:---:|:------:|:------:|
| [finance](features/finance/) | 1 | 0 | ⬜ | ⬜ | ⬜ | ⬜ |
| [invoices](features/invoices/) | 2 | 2 | ⬜ | ⬜ | ⬜ | ⬜ |
| [savedcards](features/savedcards/) | 3 | 3 | ⬜ | ⬜ | ⬜ | ⬜ |

### History & Receipts

| Feature | Screens | VMs | SPEC | API | STATUS | MOCKUP |
|---------|:-------:|:---:|:----:|:---:|:------:|:------:|
| [history](features/history/) | 3 | 3 | ⬜ | ⬜ | ⬜ | ⬜ |
| [receipt](features/receipt/) | 1 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |

### Support & Info

| Feature | Screens | VMs | SPEC | API | STATUS | MOCKUP |
|---------|:-------:|:---:|:----:|:---:|:------:|:------:|
| [faq](features/faq/) | 1 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [notification](features/notification/) | 1 | 1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [chat-support](features/chat-support/) | 📝 | 📝 | ⬜ | ⬜ | ⬜ | ⬜ |

---

## Planned Features (New)

### Rewards & Engagement

| Feature | Description | Priority | SPEC | API | STATUS | MOCKUP |
|---------|-------------|:--------:|:----:|:---:|:------:|:------:|
| [rewards](features/rewards/) | Cashback & loyalty points program | P1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [referral](features/referral/) | Refer friends & earn rewards | P2 | ⬜ | ⬜ | ⬜ | ⬜ |

### Financial Management

| Feature | Description | Priority | SPEC | API | STATUS | MOCKUP |
|---------|-------------|:--------:|:----:|:---:|:------:|:------:|
| [budget](features/budget/) | Budget tracking & spending limits | P1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [loans](features/loans/) | Micro-loans & credit features | P2 | ⬜ | ⬜ | ⬜ | ⬜ |
| [insurance](features/insurance/) | Micro-insurance offerings | P2 | ⬜ | ⬜ | ⬜ | ⬜ |

### Additional Payments

| Feature | Description | Priority | SPEC | API | STATUS | MOCKUP |
|---------|-------------|:--------:|:----:|:---:|:------:|:------:|
| [bill-pay](features/bill-pay/) | Utility & bill payment integration | P1 | ⬜ | ⬜ | ⬜ | ⬜ |
| [split-bill](features/split-bill/) | Split expenses with friends | P2 | ⬜ | ⬜ | ⬜ | ⬜ |

---

## Legend

| Symbol | Meaning |
|:------:|---------|
| ⬜ | Not created |
| 🟡 | In progress |
| ✅ | Complete |

---

## Quick Actions

```bash
# Generate spec for a feature
/design [feature-name]

# Generate mockup prompts
/mockup [feature-name]

# Check gaps
/gap-analysis design
```
