# Services Index - O(1) Lookup

> **Purpose**: Instant lookup for all network services in the client-layer.

---

## Quick Reference

| # | Service | Methods | Repository | Keywords | Path |
|:-:|---------|:-------:|------------|----------|------|
| 1 | AuthenticationService | 2 | AuthRepository | login, authenticate | services/AuthenticationService.kt |
| 2 | RegistrationService | 2 | AuthRepository | register, otp | services/RegistrationService.kt |
| 3 | ClientService | 4 | ClientRepository | client, profile, image | services/ClientService.kt |
| 4 | BeneficiaryService | 5 | BeneficiaryRepository | beneficiary, tpt | services/BeneficiaryService.kt |
| 5 | ThirdPartyTransferService | 2 | TransferRepository | transfer, payment | services/ThirdPartyTransferService.kt |
| 6 | SavingAccountsListService | 6 | SavingsRepository | savings, deposit | services/SavingAccountsListService.kt |
| 7 | LoanAccountsListService | 7 | LoanRepository | loan, repayment | services/LoanAccountsListService.kt |
| 8 | ShareAccountService | 4 | ShareRepository | share, dividend | services/ShareAccountService.kt |
| 9 | GuarantorService | 5 | GuarantorRepository | guarantor | services/GuarantorService.kt |
| 10 | NotificationService | 3 | NotificationRepository | notification, device | services/NotificationService.kt |
| 11 | ClientChargeService | 3 | ChargeRepository | charges, fees | services/ClientChargeService.kt |
| 12 | RecentTransactionsService | 1 | TransactionRepository | transactions, history | services/RecentTransactionsService.kt |
| 13 | UserDetailsService | 1 | UserRepository | password, settings | services/UserDetailsService.kt |

---

## Category Index

### Authentication Services
| Service | Repository | Path |
|---------|------------|------|
| AuthenticationService | AuthRepository | services/AuthenticationService.kt |
| RegistrationService | AuthRepository | services/RegistrationService.kt |

### Account Services
| Service | Repository | Path |
|---------|------------|------|
| SavingAccountsListService | SavingsRepository | services/SavingAccountsListService.kt |
| LoanAccountsListService | LoanRepository | services/LoanAccountsListService.kt |
| ShareAccountService | ShareRepository | services/ShareAccountService.kt |

### Transaction Services
| Service | Repository | Path |
|---------|------------|------|
| BeneficiaryService | BeneficiaryRepository | services/BeneficiaryService.kt |
| ThirdPartyTransferService | TransferRepository | services/ThirdPartyTransferService.kt |
| RecentTransactionsService | TransactionRepository | services/RecentTransactionsService.kt |

### Utility Services
| Service | Repository | Path |
|---------|------------|------|
| ClientService | ClientRepository | services/ClientService.kt |
| GuarantorService | GuarantorRepository | services/GuarantorService.kt |
| NotificationService | NotificationRepository | services/NotificationService.kt |
| ClientChargeService | ChargeRepository | services/ClientChargeService.kt |
| UserDetailsService | UserRepository | services/UserDetailsService.kt |

---

## Keyword → Service Mapping (O(1) Lookup)

```yaml
# Authentication
login: AuthenticationService
authenticate: AuthenticationService
register: RegistrationService
registration: RegistrationService
otp: RegistrationService

# Client
client: ClientService
profile: ClientService
client image: ClientService
accounts list: ClientService

# Savings
savings: SavingAccountsListService
savings account: SavingAccountsListService
deposit: SavingAccountsListService
withdraw: SavingAccountsListService
savings products: SavingAccountsListService

# Loan
loan: LoanAccountsListService
loan account: LoanAccountsListService
repayment: LoanAccountsListService
loan products: LoanAccountsListService

# Share
share: ShareAccountService
share account: ShareAccountService
share products: ShareAccountService

# Beneficiary & Transfer
beneficiary: BeneficiaryService
add beneficiary: BeneficiaryService
transfer: ThirdPartyTransferService
make transfer: ThirdPartyTransferService
tpt: ThirdPartyTransferService

# Guarantor
guarantor: GuarantorService
loan guarantor: GuarantorService

# Notification
notification: NotificationService
device registration: NotificationService
push notification: NotificationService

# Charges
charges: ClientChargeService
fees: ClientChargeService
client charges: ClientChargeService

# Transaction
transactions: RecentTransactionsService
transaction history: RecentTransactionsService
recent: RecentTransactionsService

# User
password: UserDetailsService
change password: UserDetailsService
settings: UserDetailsService
```

---

## Service → Repository Mapping

| Service | Repository |
|---------|------------|
| AuthenticationService | AuthRepository |
| RegistrationService | AuthRepository |
| ClientService | ClientRepository |
| BeneficiaryService | BeneficiaryRepository |
| ThirdPartyTransferService | TransferRepository |
| SavingAccountsListService | SavingsRepository |
| LoanAccountsListService | LoanRepository |
| ShareAccountService | ShareRepository |
| GuarantorService | GuarantorRepository |
| NotificationService | NotificationRepository |
| ClientChargeService | ChargeRepository |
| RecentTransactionsService | TransactionRepository |
| UserDetailsService | UserRepository |

---

## Service Interface Pattern

```kotlin
interface {ServiceName} {
    @GET("/endpoint")
    suspend fun method1(): Response<Type>
    
    @POST("/endpoint")
    suspend fun method2(@Body body: Type): Response<Type>
}
```

---

## Base Path

```
core/network/src/commonMain/kotlin/org/mifos/mobile/core/network/services/
```

---

## Commands

```bash
/enforce-index services    # Validate this index
/client [service]          # Create service (auto-indexes)
/gap-analysis client       # Check client layer gaps
```
