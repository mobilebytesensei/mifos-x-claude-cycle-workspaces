# Services Index - mobile-wallet

> 23 repositories discovered from source analysis

---

## Repository Summary

| Total | Documented | Pending |
|:-----:|:----------:|:-------:|
| 23 | 0 | 23 |

---

## Repositories by Domain

### Authentication

| Repository | Interface | Impl | Status |
|------------|:---------:|:----:|:------:|
| AuthenticationRepository | ✅ | ✅ | ⬜ |
| RegistrationRepository | ✅ | ✅ | ⬜ |
| TwoFactorAuthRepository | ✅ | ✅ | ⬜ |

### User & Client

| Repository | Interface | Impl | Status |
|------------|:---------:|:----:|:------:|
| UserRepository | ✅ | ✅ | ⬜ |
| ClientRepository | ✅ | ✅ | ⬜ |
| UserPreferencesRepository | ✅ | ✅ | ⬜ |

### Accounts & Finance

| Repository | Interface | Impl | Status |
|------------|:---------:|:----:|:------:|
| AccountRepository | ✅ | ✅ | ⬜ |
| SavingsAccountRepository | ✅ | ✅ | ⬜ |
| SavedCardRepository | ✅ | ✅ | ⬜ |

### Transfers

| Repository | Interface | Impl | Status |
|------------|:---------:|:----:|:------:|
| ThirdPartyTransferRepository | ✅ | ✅ | ⬜ |
| InterBankRepository | ✅ | ✅ | ⬜ |
| BeneficiaryRepository | ✅ | ✅ | ⬜ |
| StandingInstructionRepository | ✅ | ✅ | ⬜ |
| RecentPayeeRepository | ✅ | ✅ | ⬜ |

### Financial Services

| Repository | Interface | Impl | Status |
|------------|:---------:|:----:|:------:|
| InvoiceRepository | ✅ | ✅ | ⬜ |
| RunReportRepository | ✅ | ✅ | ⬜ |

### KYC & Documents

| Repository | Interface | Impl | Status |
|------------|:---------:|:----:|:------:|
| KycLevelRepository | ✅ | ✅ | ⬜ |
| DocumentRepository | ✅ | ✅ | ⬜ |
| SelfServiceRepository | ✅ | ✅ | ⬜ |

### Search & Notifications

| Repository | Interface | Impl | Status |
|------------|:---------:|:----:|:------:|
| SearchRepository | ✅ | ✅ | ⬜ |
| NotificationRepository | ✅ | ✅ | ⬜ |

### Assets & Local

| Repository | Interface | Impl | Status |
|------------|:---------:|:----:|:------:|
| AssetRepository | ✅ | ✅ | ⬜ |
| LocalAssetRepository | ✅ | ✅ | ⬜ |

---

## Repository Pattern

```kotlin
// Interface (core/domain/repository)
interface AccountRepository {
    suspend fun getAccounts(): Flow<List<Account>>
    suspend fun getAccountDetails(id: Long): Account
}

// Implementation (core/data/repository)
class AccountRepositoryImpl(
    private val accountService: AccountService,
    private val accountDao: AccountDao
) : AccountRepository {
    // Implementation with caching
}
```

---

## Quick Actions

```bash
# Document repository
/client [repository-name]

# Check gaps
/gap-analysis client
```
