# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/design-spec-layer/_shared/COMPONENTS.md"
# last_modified: "2026-03-20"

# Shared Components - mobile-wallet

> Common UI components used across features

---

## Component Categories

### Navigation

| Component | Usage | Source |
|-----------|-------|--------|
| BottomNavigation | Main navigation | `core/designsystem/` |
| TopAppBar | Screen headers | `core/designsystem/` |
| BackButton | Navigation back | `core/designsystem/` |

### Input

| Component | Usage | Source |
|-----------|-------|--------|
| MifosTextField | Text input | `core/designsystem/` |
| MifosPasswordField | Password input | `core/designsystem/` |
| AmountInput | Money input | `core/ui/` |
| PhoneInput | Phone number | `core/ui/` |

### Display

| Component | Usage | Source |
|-----------|-------|--------|
| AccountCard | Account display | `core/ui/` |
| TransactionItem | Transaction list | `core/ui/` |
| BalanceDisplay | Balance showing | `core/ui/` |

### Actions

| Component | Usage | Source |
|-----------|-------|--------|
| MifosButton | Primary action | `core/designsystem/` |
| MifosOutlinedButton | Secondary action | `core/designsystem/` |
| FAB | Floating action | `core/designsystem/` |

### Feedback

| Component | Usage | Source |
|-----------|-------|--------|
| LoadingScreen | Loading state | `core/ui/` |
| ErrorScreen | Error state | `core/ui/` |
| EmptyScreen | Empty state | `core/ui/` |
| SuccessScreen | Success state | `core/ui/` |

### QR

| Component | Usage | Source |
|-----------|-------|--------|
| QrCodeDisplay | Show QR | `feature/mpay-qr/` |
| QrScanner | Scan QR | `feature/mpay-qr-scan/` |

---

## Design System

The app uses a custom design system located in `core/designsystem/`:

- Colors (Light/Dark themes)
- Typography (Material3)
- Shapes
- Icons
- Spacing

---

## Component Documentation

Each component should document:
1. Purpose
2. Props/Parameters
3. Usage example
4. Variants
5. Accessibility
