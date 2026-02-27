# Screens Index - mobile-wallet

> 55 screens discovered from source analysis

---

## Screens by Module

### auth (4 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| LoginScreen | LoginViewModel | ⬜ |
| SignupScreen | SignupViewModel | ⬜ |
| MobileVerificationScreen | MobileVerificationViewModel | ⬜ |
| PasscodeScreen | - | ⬜ |

### accounts (5 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| AccountsScreen | AccountsViewModel | ⬜ |
| AccountDetailScreen | AccountDetailViewModel | ⬜ |
| AccountTransactionsScreen | AccountTransactionsViewModel | ⬜ |
| BankAccountDetailScreen | BankAccountDetailViewModel | ⬜ |
| LinkBankAccountScreen | LinkBankAccountViewModel | ⬜ |

### home (1 screen)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| HomeScreen | HomeViewModel | ⬜ |

### payments (3 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| SendMoneyScreen | SendMoneyViewModel | ⬜ |
| RequestMoneyScreen | - | ⬜ |
| PaymentsScreen | - | ⬜ |

### transfer-intrabank (4 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| TransferScreen | TransferViewModel | ⬜ |
| TransferConfirmScreen | TransferConfirmViewModel | ⬜ |
| TransferSuccessScreen | - | ⬜ |
| BeneficiarySelectScreen | BeneficiarySelectViewModel | ⬜ |

### transfer-interbank (5 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| InterBankTransferScreen | InterBankTransferViewModel | ⬜ |
| BankSelectionScreen | - | ⬜ |
| AccountVerificationScreen | - | ⬜ |
| TransferConfirmScreen | - | ⬜ |
| TransferReceiptScreen | - | ⬜ |

### kyc (4 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| KycLevel1Screen | KycLevel1ViewModel | ⬜ |
| KycLevel2Screen | KycLevel2ViewModel | ⬜ |
| KycLevel3Screen | KycLevel3ViewModel | ⬜ |
| DocumentUploadScreen | DocumentUploadViewModel | ⬜ |

### history (3 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| TransactionHistoryScreen | TransactionHistoryViewModel | ⬜ |
| TransactionDetailScreen | TransactionDetailViewModel | ⬜ |
| FilterScreen | FilterViewModel | ⬜ |

### invoices (2 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| InvoicesScreen | InvoicesViewModel | ⬜ |
| InvoiceDetailScreen | InvoiceDetailViewModel | ⬜ |

### savedcards (3 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| SavedCardsScreen | SavedCardsViewModel | ⬜ |
| AddCardScreen | AddCardViewModel | ⬜ |
| CardDetailScreen | CardDetailViewModel | ⬜ |

### merchants (2 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| MerchantsScreen | MerchantsViewModel | ⬜ |
| MerchantDetailScreen | MerchantDetailViewModel | ⬜ |

### standing-instruction (3 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| StandingInstructionsScreen | StandingInstructionsViewModel | ⬜ |
| CreateInstructionScreen | CreateInstructionViewModel | ⬜ |
| InstructionDetailScreen | InstructionDetailViewModel | ⬜ |

### profile (2 screens)

| Screen | ViewModel | Doc |
|--------|-----------|:---:|
| ProfileScreen | ProfileViewModel | ⬜ |
| EditProfileScreen | EditProfileViewModel | ⬜ |

### Other Screens

| Module | Screen | ViewModel |
|--------|--------|-----------|
| editpassword | EditPasswordScreen | EditPasswordViewModel |
| faq | FaqScreen | FaqViewModel |
| fast-mpay | FastMpayScreen | FastMpayViewModel |
| finance | FinanceScreen | - |
| mpay-qr | QrCodeScreen | QrCodeViewModel |
| mpay-qr-scan | QrScanScreen, QrResultScreen | QrScanViewModel |
| notification | NotificationScreen | NotificationViewModel |
| receipt | ReceiptScreen | ReceiptViewModel |
| settings | SettingsScreen | SettingsViewModel |
| upi-setup | UpiSetupScreen, UpiPinScreen, UpiVerifyScreen, UpiSuccessScreen | - |

---

## Quick Actions

```bash
# Document screen
/feature [module]/[screen]

# Check gaps
/gap-analysis feature
```
