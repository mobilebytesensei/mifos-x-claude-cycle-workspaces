# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/server-layer/API_INDEX.md"
# last_modified: "2026-03-20"

# API Index - mobile-wallet

> 19 API services discovered (Fineract REST via Ktorfit)

---

## Backend Configuration

| Field | Value |
|-------|-------|
| Provider | Fineract Self-Service |
| Protocol | REST |
| Client | Ktorfit (Ktor-based) |
| Secondary | Supabase (config) |

---

## API Services

### Authentication & User

| Service | Endpoints | Status |
|---------|:---------:|:------:|
| AuthenticationService | auth, login, logout | ⬜ |
| RegistrationService | register, verify | ⬜ |
| TwoFactorAuthService | 2fa setup, verify | ⬜ |
| UserService | user CRUD | ⬜ |

### Client & Account

| Service | Endpoints | Status |
|---------|:---------:|:------:|
| ClientService | client profile | ⬜ |
| SavingsAccountsService | accounts CRUD | ⬜ |
| AccountTransfersService | transfers | ⬜ |

### Transfers & Payments

| Service | Endpoints | Status |
|---------|:---------:|:------:|
| ThirdPartyTransferService | P2P transfers | ⬜ |
| InterBankService | interbank transfers | ⬜ |
| BeneficiaryService | beneficiary management | ⬜ |
| StandingInstructionService | recurring payments | ⬜ |

### Financial Services

| Service | Endpoints | Status |
|---------|:---------:|:------:|
| InvoiceService | invoices CRUD | ⬜ |
| SavedCardService | cards management | ⬜ |

### KYC & Documents

| Service | Endpoints | Status |
|---------|:---------:|:------:|
| KYCLevel1Service | KYC verification | ⬜ |
| DocumentService | document upload | ⬜ |

### Search & Reports

| Service | Endpoints | Status |
|---------|:---------:|:------:|
| SearchService | search clients, accounts | ⬜ |
| RunReportService | reports generation | ⬜ |

### Notifications & Config

| Service | Endpoints | Status |
|---------|:---------:|:------:|
| NotificationService | notifications | ⬜ |
| AppConfigService | app configuration | ⬜ |

---

## Service Details

### AuthenticationService

```kotlin
// Location: core/network/services/AuthenticationService.kt
interface AuthenticationService {
    suspend fun authenticate(credentials: Credentials): AuthResponse
    suspend fun logout(): GenericResponse
    suspend fun refreshToken(token: String): AuthResponse
}
```

### SavingsAccountsService

```kotlin
// Location: core/network/services/SavingsAccountsService.kt
interface SavingsAccountsService {
    suspend fun getSavingsAccounts(clientId: Long): List<SavingsAccount>
    suspend fun getSavingsAccountDetails(accountId: Long): SavingsAccountDetails
    suspend fun getTransactionHistory(accountId: Long): List<Transaction>
}
```

---

## API Patterns

### Base URL Configuration
- Production: Configured via Supabase instance config
- Self-Service: `/fineract-provider/api/v1/self/`

### Authentication
- Basic Auth for initial login
- Bearer token for subsequent requests
- 2FA optional support

### Error Handling
- Standard HTTP status codes
- GenericResponse for errors
- Error codes documented per service

---

## Quick Actions

```bash
# Document API endpoint
/server [service-name]

# Check API gaps
/gap-analysis server
```
