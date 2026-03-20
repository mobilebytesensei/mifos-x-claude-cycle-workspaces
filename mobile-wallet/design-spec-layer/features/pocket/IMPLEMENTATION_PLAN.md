# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mobile-wallet/design-spec-layer/features/pocket/IMPLEMENTATION_PLAN.md"
# last_modified: "2026-03-20"

# Implementation Plan: Pocket Feature

> Step-by-step implementation guide for Pocket (Favorites) integration

---

## Overview

| Attribute | Value |
|-----------|-------|
| Feature | Pocket (Favorites for Home Screen) |
| Complexity | Medium |
| Layers | Server → Client → Feature (Home enhancement) |
| Dependencies | Existing Home feature, Account models |

---

## Implementation Order

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    IMPLEMENTATION PHASES                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  PHASE 1: SERVER LAYER (Network)                    ~2 hours            │
│  ─────────────────────────────────────────────────────────────────      │
│  1.1 Add POCKETS to ApiEndPoints.kt                                     │
│  1.2 Create PocketService.kt (Ktorfit interface)                        │
│  1.3 Create entity models (PocketAccountsEntity, etc.)                  │
│  1.4 Register service in FineractApiManager                             │
│                                                                          │
│  PHASE 2: CLIENT LAYER (Repository)                 ~2 hours            │
│  ─────────────────────────────────────────────────────────────────      │
│  2.1 Create domain models (Pocket, PocketAccount)                       │
│  2.2 Create PocketRepository interface                                  │
│  2.3 Create PocketRepositoryImpl                                        │
│  2.4 Register in RepositoryModule                                       │
│                                                                          │
│  PHASE 3: FEATURE LAYER (Home Integration)          ~4 hours            │
│  ─────────────────────────────────────────────────────────────────      │
│  3.1 Extend HomeState with pocket fields                                │
│  3.2 Extend HomeAction with pocket actions                              │
│  3.3 Update HomeViewModel to fetch/manage pocket                        │
│  3.4 Add star indicator to AccountCard                                  │
│  3.5 Create ViewDropdownMenu component                                  │
│  3.6 Create AccountContextMenu component                                │
│  3.7 Update HomeScreen to integrate pocket                              │
│                                                                          │
│  PHASE 4: MANAGE POCKET SCREEN                      ~2 hours            │
│  ─────────────────────────────────────────────────────────────────      │
│  4.1 Create ManagePocketScreen                                          │
│  4.2 Create ManagePocketViewModel                                       │
│  4.3 Add navigation                                                     │
│                                                                          │
│  PHASE 5: TESTING                                   ~2 hours            │
│  ─────────────────────────────────────────────────────────────────      │
│  5.1 Unit tests for PocketRepository                                    │
│  5.2 Unit tests for HomeViewModel pocket logic                          │
│  5.3 UI tests for pocket interactions                                   │
│                                                                          │
│  TOTAL ESTIMATED TIME: ~12 hours                                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## PHASE 1: SERVER LAYER (core:network)

### 1.1 Add POCKETS to ApiEndPoints.kt

**File:** `core/network/src/commonMain/kotlin/org/mifospay/core/network/utils/ApiEndPoints.kt`

```kotlin
object ApiEndPoints {
    // Existing endpoints...
    const val STANDING_INSTRUCTION = "standinginstructions"
    const val OFFICES = "offices"

    // ADD: Pocket endpoint
    const val POCKETS = "self/pockets"
}
```

---

### 1.2 Create PocketService.kt

**File:** `core/network/src/commonMain/kotlin/org/mifospay/core/network/services/PocketService.kt`

```kotlin
package org.mifospay.core.network.services

import de.jensklingenberg.ktorfit.http.Body
import de.jensklingenberg.ktorfit.http.GET
import de.jensklingenberg.ktorfit.http.POST
import de.jensklingenberg.ktorfit.http.Query
import kotlinx.coroutines.flow.Flow
import org.mifospay.core.network.model.entity.pocket.PocketAccountsEntity
import org.mifospay.core.network.model.entity.pocket.PocketCommandResponse
import org.mifospay.core.network.model.entity.pocket.PocketLinkRequest
import org.mifospay.core.network.utils.ApiEndPoints

interface PocketService {

    @GET(ApiEndPoints.POCKETS)
    fun getPocketAccounts(): Flow<PocketAccountsEntity>

    @POST(ApiEndPoints.POCKETS)
    suspend fun linkAccounts(
        @Query("command") command: String = "linkAccounts",
        @Body request: PocketLinkRequest,
    ): PocketCommandResponse

    @POST(ApiEndPoints.POCKETS)
    suspend fun delinkAccounts(
        @Query("command") command: String = "delinkAccounts",
        @Body request: PocketLinkRequest,
    ): PocketCommandResponse
}
```

---

### 1.3 Create Entity Models

**File:** `core/network/src/commonMain/kotlin/org/mifospay/core/network/model/entity/pocket/PocketAccountsEntity.kt`

```kotlin
package org.mifospay.core.network.model.entity.pocket

import kotlinx.serialization.Serializable
import org.mifospay.core.model.savingsaccount.Currency

@Serializable
data class PocketAccountsEntity(
    val savingsAccounts: List<PocketSavingsAccountEntity> = emptyList(),
    val loanAccounts: List<PocketLoanAccountEntity> = emptyList(),
    val shareAccounts: List<PocketShareAccountEntity> = emptyList(),
)

@Serializable
data class PocketSavingsAccountEntity(
    val id: Long,
    val accountNo: String,
    val productName: String,
    val accountBalance: Double,
    val currency: Currency,
)

@Serializable
data class PocketLoanAccountEntity(
    val id: Long,
    val accountNo: String,
    val productName: String,
    val outstandingBalance: Double,
    val currency: Currency,
)

@Serializable
data class PocketShareAccountEntity(
    val id: Long,
    val accountNo: String,
    val productName: String,
    val totalShares: Int,
    val currentValue: Double,
    val currency: Currency,
)
```

**File:** `core/network/src/commonMain/kotlin/org/mifospay/core/network/model/entity/pocket/PocketLinkRequest.kt`

```kotlin
package org.mifospay.core.network.model.entity.pocket

import kotlinx.serialization.Serializable

@Serializable
data class PocketLinkRequest(
    val savingsAccounts: List<Long> = emptyList(),
    val loanAccounts: List<Long> = emptyList(),
    val shareAccounts: List<Long> = emptyList(),
)
```

**File:** `core/network/src/commonMain/kotlin/org/mifospay/core/network/model/entity/pocket/PocketCommandResponse.kt`

```kotlin
package org.mifospay.core.network.model.entity.pocket

import kotlinx.serialization.Serializable

@Serializable
data class PocketCommandResponse(
    val pocketId: Long,
    val changes: PocketChanges,
)

@Serializable
data class PocketChanges(
    val savingsAccounts: List<Long> = emptyList(),
    val loanAccounts: List<Long> = emptyList(),
    val shareAccounts: List<Long> = emptyList(),
)
```

---

### 1.4 Register in FineractApiManager

**File:** `core/network/src/commonMain/kotlin/org/mifospay/core/network/FineractApiManager.kt`

```kotlin
// ADD to FineractApiManager class:
val pocketApi: PocketService by lazy { ktorfit.createPocketService() }
```

**File:** `core/network/src/commonMain/kotlin/org/mifospay/core/network/di/NetworkModule.kt`

```kotlin
// Ensure PocketService is created by Ktorfit
// (Ktorfit auto-generates implementations for interfaces)
```

---

## PHASE 2: CLIENT LAYER (core:data + core:model)

### 2.1 Create Domain Models

**File:** `core/model/src/commonMain/kotlin/org/mifospay/core/model/pocket/PocketAccount.kt`

```kotlin
package org.mifospay.core.model.pocket

import org.mifospay.core.model.savingsaccount.Currency

data class PocketAccount(
    val id: Long,
    val accountNo: String,
    val productName: String,
    val balance: Double,
    val currency: Currency,
    val accountType: PocketAccountType,
)

enum class PocketAccountType {
    SAVINGS,
    LOAN,
    SHARE,
}
```

**File:** `core/model/src/commonMain/kotlin/org/mifospay/core/model/pocket/Pocket.kt`

```kotlin
package org.mifospay.core.model.pocket

import org.mifospay.core.model.savingsaccount.Currency

data class Pocket(
    val accounts: List<PocketAccount>,
    val totalBalance: Double,
    val currency: Currency?,
) {
    companion object {
        val EMPTY = Pocket(
            accounts = emptyList(),
            totalBalance = 0.0,
            currency = null,
        )
    }

    val isEmpty: Boolean get() = accounts.isEmpty()
}
```

---

### 2.2 Create PocketRepository Interface

**File:** `core/data/src/commonMain/kotlin/org/mifospay/core/data/repository/PocketRepository.kt`

```kotlin
package org.mifospay.core.data.repository

import kotlinx.coroutines.flow.Flow
import org.mifospay.core.common.DataState
import org.mifospay.core.model.pocket.Pocket
import org.mifospay.core.model.pocket.PocketAccountType

interface PocketRepository {

    /**
     * Get all accounts linked to user's pocket.
     * Returns Pocket.EMPTY if no pocket exists (404 from API).
     */
    fun getPocket(): Flow<DataState<Pocket>>

    /**
     * Link an account to pocket.
     */
    suspend fun linkAccount(
        accountId: Long,
        accountType: PocketAccountType,
    ): DataState<Unit>

    /**
     * Remove an account from pocket.
     */
    suspend fun delinkAccount(
        accountId: Long,
        accountType: PocketAccountType,
    ): DataState<Unit>

    /**
     * Link multiple accounts to pocket.
     */
    suspend fun linkAccounts(
        savingsIds: List<Long> = emptyList(),
        loanIds: List<Long> = emptyList(),
        shareIds: List<Long> = emptyList(),
    ): DataState<Unit>

    /**
     * Check if an account is in the pocket.
     */
    fun isAccountInPocket(accountId: Long): Boolean
}
```

---

### 2.3 Create PocketRepositoryImpl

**File:** `core/data/src/commonMain/kotlin/org/mifospay/core/data/repositoryImpl/PocketRepositoryImpl.kt`

```kotlin
package org.mifospay.core.data.repositoryImpl

import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.flowOn
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.withContext
import org.mifospay.core.common.DataState
import org.mifospay.core.common.asDataStateFlow
import org.mifospay.core.data.repository.PocketRepository
import org.mifospay.core.model.pocket.Pocket
import org.mifospay.core.model.pocket.PocketAccount
import org.mifospay.core.model.pocket.PocketAccountType
import org.mifospay.core.model.savingsaccount.Currency
import org.mifospay.core.network.FineractApiManager
import org.mifospay.core.network.model.entity.pocket.PocketAccountsEntity
import org.mifospay.core.network.model.entity.pocket.PocketLinkRequest

class PocketRepositoryImpl(
    private val apiManager: FineractApiManager,
    private val ioDispatcher: CoroutineDispatcher,
) : PocketRepository {

    // Cache pocket account IDs for quick lookup
    private val pocketAccountIds = MutableStateFlow<Set<Long>>(emptySet())

    override fun getPocket(): Flow<DataState<Pocket>> {
        return apiManager.pocketApi
            .getPocketAccounts()
            .map { entity -> entity.toPocket() }
            .onEach { pocket ->
                // Update cache
                pocketAccountIds.value = pocket.accounts.map { it.id }.toSet()
            }
            .catch { e ->
                // 404 means no pocket - return empty
                if (e.message?.contains("404") == true) {
                    emit(Pocket.EMPTY)
                } else {
                    throw e
                }
            }
            .asDataStateFlow()
            .flowOn(ioDispatcher)
    }

    override suspend fun linkAccount(
        accountId: Long,
        accountType: PocketAccountType,
    ): DataState<Unit> {
        return linkAccounts(
            savingsIds = if (accountType == PocketAccountType.SAVINGS) listOf(accountId) else emptyList(),
            loanIds = if (accountType == PocketAccountType.LOAN) listOf(accountId) else emptyList(),
            shareIds = if (accountType == PocketAccountType.SHARE) listOf(accountId) else emptyList(),
        )
    }

    override suspend fun delinkAccount(
        accountId: Long,
        accountType: PocketAccountType,
    ): DataState<Unit> {
        return try {
            withContext(ioDispatcher) {
                val request = PocketLinkRequest(
                    savingsAccounts = if (accountType == PocketAccountType.SAVINGS) listOf(accountId) else emptyList(),
                    loanAccounts = if (accountType == PocketAccountType.LOAN) listOf(accountId) else emptyList(),
                    shareAccounts = if (accountType == PocketAccountType.SHARE) listOf(accountId) else emptyList(),
                )
                apiManager.pocketApi.delinkAccounts(request = request)

                // Update cache
                pocketAccountIds.value = pocketAccountIds.value - accountId
            }
            DataState.Success(Unit)
        } catch (e: Exception) {
            DataState.Error(e)
        }
    }

    override suspend fun linkAccounts(
        savingsIds: List<Long>,
        loanIds: List<Long>,
        shareIds: List<Long>,
    ): DataState<Unit> {
        return try {
            withContext(ioDispatcher) {
                val request = PocketLinkRequest(
                    savingsAccounts = savingsIds,
                    loanAccounts = loanIds,
                    shareAccounts = shareIds,
                )
                apiManager.pocketApi.linkAccounts(request = request)

                // Update cache
                pocketAccountIds.value = pocketAccountIds.value + savingsIds + loanIds + shareIds
            }
            DataState.Success(Unit)
        } catch (e: Exception) {
            DataState.Error(e)
        }
    }

    override fun isAccountInPocket(accountId: Long): Boolean {
        return accountId in pocketAccountIds.value
    }

    // Extension function to convert entity to domain model
    private fun PocketAccountsEntity.toPocket(): Pocket {
        val accounts = mutableListOf<PocketAccount>()
        var defaultCurrency: Currency? = null

        savingsAccounts.forEach { entity ->
            accounts.add(
                PocketAccount(
                    id = entity.id,
                    accountNo = entity.accountNo,
                    productName = entity.productName,
                    balance = entity.accountBalance,
                    currency = entity.currency,
                    accountType = PocketAccountType.SAVINGS,
                )
            )
            if (defaultCurrency == null) defaultCurrency = entity.currency
        }

        loanAccounts.forEach { entity ->
            accounts.add(
                PocketAccount(
                    id = entity.id,
                    accountNo = entity.accountNo,
                    productName = entity.productName,
                    balance = -entity.outstandingBalance, // Loans are negative
                    currency = entity.currency,
                    accountType = PocketAccountType.LOAN,
                )
            )
            if (defaultCurrency == null) defaultCurrency = entity.currency
        }

        shareAccounts.forEach { entity ->
            accounts.add(
                PocketAccount(
                    id = entity.id,
                    accountNo = entity.accountNo,
                    productName = entity.productName,
                    balance = entity.currentValue,
                    currency = entity.currency,
                    accountType = PocketAccountType.SHARE,
                )
            )
            if (defaultCurrency == null) defaultCurrency = entity.currency
        }

        return Pocket(
            accounts = accounts,
            totalBalance = accounts.sumOf { it.balance },
            currency = defaultCurrency,
        )
    }
}
```

---

### 2.4 Register in RepositoryModule

**File:** `core/data/src/commonMain/kotlin/org/mifospay/core/data/di/RepositoryModule.kt`

```kotlin
// ADD to RepositoryModule:
single<PocketRepository> { PocketRepositoryImpl(get(), get(ioDispatcher)) }
```

---

## PHASE 3: FEATURE LAYER (feature:home)

### 3.1 Extend HomeState

**File:** `feature/home/src/commonMain/kotlin/org/mifospay/feature/home/HomeViewModel.kt`

Add to `HomeState`:

```kotlin
@Serializable
data class HomeState(
    // Existing fields...
    val client: Client,
    val defaultAccountId: Long?,
    val accounts: List<Account> = emptyList(),
    val selectedAccount: Account? = null,
    val transactions: List<Transaction>? = null,
    val isRefreshing: Boolean = false,
    val viewState: ViewState = ViewState.Loading,

    // NEW: Pocket fields
    val pocket: Pocket = Pocket.EMPTY,
    val showPocketView: Boolean = true,  // Default to pocket if not empty
    val showViewDropdown: Boolean = false,
    val showContextMenu: Boolean = false,
    val contextMenuAccount: Account? = null,
) {
    // Computed property: accounts to display
    val displayedAccounts: List<Account>
        get() = when {
            pocket.isEmpty -> accounts  // Empty pocket = show all
            showPocketView -> pocket.accounts.map { it.toAccount() }  // Pocket view
            else -> accounts  // All accounts view
        }

    // Computed property: total balance to display
    val displayedTotalBalance: Double
        get() = if (showPocketView && !pocket.isEmpty) {
            pocket.totalBalance
        } else {
            accounts.sumOf { it.balance }
        }

    // Check if account is in pocket
    fun isInPocket(accountId: Long): Boolean {
        return pocket.accounts.any { it.id == accountId }
    }
}
```

---

### 3.2 Extend HomeAction

Add to `HomeAction`:

```kotlin
sealed interface HomeAction {
    // Existing actions...
    data object RequestClicked : HomeAction
    data object SendClicked : HomeAction

    // NEW: Pocket actions
    data object TogglePocketView : HomeAction
    data object ShowViewDropdown : HomeAction
    data object DismissViewDropdown : HomeAction
    data class ShowContextMenu(val account: Account) : HomeAction
    data object DismissContextMenu : HomeAction
    data class AddToPocket(val accountId: Long) : HomeAction
    data class RemoveFromPocket(val accountId: Long) : HomeAction
    data object NavigateToManagePocket : HomeAction
}
```

Add to `HomeEvent`:

```kotlin
sealed interface HomeEvent {
    // Existing events...

    // NEW: Pocket events
    data object NavigateToManagePocket : HomeEvent
    data class ShowPocketToast(val message: String) : HomeEvent
}
```

---

### 3.3 Update HomeViewModel

Add to `HomeViewModel`:

```kotlin
class HomeViewModel(
    private val preferencesRepository: UserPreferencesRepository,
    private val repository: SelfServiceRepository,
    private val pocketRepository: PocketRepository,  // NEW: Inject
) : BaseViewModel<HomeState, HomeEvent, HomeAction>(...) {

    init {
        getAccounts()
        getPocket()  // NEW: Fetch pocket on init
    }

    // NEW: Fetch pocket
    private fun getPocket() {
        launchIO {
            pocketRepository.getPocket().collect { result ->
                when (result) {
                    is DataState.Success -> {
                        mutableStateFlow.update {
                            it.copy(
                                pocket = result.data,
                                // If pocket was empty but now has accounts, switch to pocket view
                                showPocketView = result.data.accounts.isNotEmpty(),
                            )
                        }
                    }
                    is DataState.Error -> {
                        // Silent fail - pocket is optional
                        mutableStateFlow.update {
                            it.copy(pocket = Pocket.EMPTY, showPocketView = false)
                        }
                    }
                    is DataState.Loading -> { /* No-op */ }
                }
            }
        }
    }

    override fun handleAction(action: HomeAction) {
        when (action) {
            // Existing handlers...

            // NEW: Pocket handlers
            is HomeAction.TogglePocketView -> {
                mutableStateFlow.update {
                    it.copy(showPocketView = !it.showPocketView)
                }
            }

            is HomeAction.ShowViewDropdown -> {
                mutableStateFlow.update { it.copy(showViewDropdown = true) }
            }

            is HomeAction.DismissViewDropdown -> {
                mutableStateFlow.update { it.copy(showViewDropdown = false) }
            }

            is HomeAction.ShowContextMenu -> {
                mutableStateFlow.update {
                    it.copy(showContextMenu = true, contextMenuAccount = action.account)
                }
            }

            is HomeAction.DismissContextMenu -> {
                mutableStateFlow.update {
                    it.copy(showContextMenu = false, contextMenuAccount = null)
                }
            }

            is HomeAction.AddToPocket -> {
                addToPocket(action.accountId)
            }

            is HomeAction.RemoveFromPocket -> {
                removeFromPocket(action.accountId)
            }

            is HomeAction.NavigateToManagePocket -> {
                mutableStateFlow.update { it.copy(showViewDropdown = false) }
                sendEvent(HomeEvent.NavigateToManagePocket)
            }
        }
    }

    private fun addToPocket(accountId: Long) {
        launchIO {
            // Determine account type from accounts list
            val account = state.accounts.find { it.id == accountId }
            val accountType = account?.accountType?.toPocketAccountType()
                ?: PocketAccountType.SAVINGS

            when (val result = pocketRepository.linkAccount(accountId, accountType)) {
                is DataState.Success -> {
                    getPocket()  // Refresh pocket
                    sendEvent(HomeEvent.ShowPocketToast("Added to Pocket"))
                }
                is DataState.Error -> {
                    sendEvent(HomeEvent.ShowPocketToast("Failed to add to Pocket"))
                }
                else -> {}
            }
        }
        mutableStateFlow.update { it.copy(showContextMenu = false) }
    }

    private fun removeFromPocket(accountId: Long) {
        launchIO {
            val pocketAccount = state.pocket.accounts.find { it.id == accountId }
            val accountType = pocketAccount?.accountType ?: PocketAccountType.SAVINGS

            when (val result = pocketRepository.delinkAccount(accountId, accountType)) {
                is DataState.Success -> {
                    getPocket()  // Refresh pocket
                    sendEvent(HomeEvent.ShowPocketToast("Removed from Pocket"))

                    // If last account removed, switch to all view
                    if (state.pocket.accounts.size == 1) {
                        mutableStateFlow.update { it.copy(showPocketView = false) }
                    }
                }
                is DataState.Error -> {
                    sendEvent(HomeEvent.ShowPocketToast("Failed to remove from Pocket"))
                }
                else -> {}
            }
        }
        mutableStateFlow.update { it.copy(showContextMenu = false) }
    }
}
```

---

### 3.4 Add Star Indicator to AccountCard

Update `AccountCard` composable:

```kotlin
@Composable
private fun AccountCard(
    account: Account,
    defaultAccountId: Long?,
    isInPocket: Boolean,  // NEW: Pocket indicator
    onMarkAsDefault: (Long, String) -> Unit,
    onLongPress: () -> Unit,  // NEW: Long press handler
    modifier: Modifier = Modifier,
    onClick: (Long) -> Unit,
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(200.dp)
            .background(...)
            .clip(RoundedCornerShape(16.dp))
            .combinedClickable(  // NEW: Support long press
                onClick = { onClick(account.id) },
                onLongClick = { onLongPress() },
            ),
    ) {
        Column(...) {
            Row(...) {
                Column {
                    // Existing account type text

                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(text = account.name, ...)

                        // NEW: Star indicator
                        if (isInPocket) {
                            Spacer(modifier = Modifier.width(4.dp))
                            Icon(
                                imageVector = Icons.Filled.Star,
                                contentDescription = "In Pocket",
                                modifier = Modifier.size(16.dp),
                                tint = Color(0xFFFFD700), // Gold color
                            )
                        }
                    }
                }
                // ... rest of header
            }
            // ... rest of card
        }
    }
}
```

---

### 3.5 Create ViewDropdownMenu Component

**File:** `feature/home/src/commonMain/kotlin/org/mifospay/feature/home/components/ViewDropdownMenu.kt`

```kotlin
@Composable
fun ViewDropdownMenu(
    isExpanded: Boolean,
    showPocketView: Boolean,
    pocketCount: Int,
    allAccountsCount: Int,
    onDismiss: () -> Unit,
    onSelectPocket: () -> Unit,
    onSelectAll: () -> Unit,
    onManagePocket: () -> Unit,
) {
    DropdownMenu(
        expanded = isExpanded,
        onDismissRequest = onDismiss,
    ) {
        DropdownMenuItem(
            text = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (showPocketView) {
                        Icon(Icons.Filled.Check, null, Modifier.size(20.dp))
                    } else {
                        Spacer(Modifier.width(20.dp))
                    }
                    Spacer(Modifier.width(8.dp))
                    Text("Pocket ($pocketCount)")
                }
            },
            onClick = {
                onSelectPocket()
                onDismiss()
            },
        )

        DropdownMenuItem(
            text = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (!showPocketView) {
                        Icon(Icons.Filled.Check, null, Modifier.size(20.dp))
                    } else {
                        Spacer(Modifier.width(20.dp))
                    }
                    Spacer(Modifier.width(8.dp))
                    Text("All Accounts ($allAccountsCount)")
                }
            },
            onClick = {
                onSelectAll()
                onDismiss()
            },
        )

        HorizontalDivider()

        DropdownMenuItem(
            leadingIcon = { Icon(Icons.Filled.Settings, null) },
            text = { Text("Manage Pocket") },
            onClick = onManagePocket,
        )
    }
}
```

---

### 3.6 Create AccountContextMenu Component

**File:** `feature/home/src/commonMain/kotlin/org/mifospay/feature/home/components/AccountContextMenu.kt`

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AccountContextMenu(
    account: Account,
    isInPocket: Boolean,
    onDismiss: () -> Unit,
    onAddToPocket: () -> Unit,
    onRemoveFromPocket: () -> Unit,
    onSetAsDefault: () -> Unit,
    onViewDetails: () -> Unit,
) {
    ModalBottomSheet(
        onDismissRequest = onDismiss,
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
        ) {
            // Header
            Text(
                text = account.name,
                style = MaterialTheme.typography.titleMedium,
            )
            Text(
                text = "${account.number} • ${CurrencyFormatter.format(account.balance, account.currency.code)}",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Spacer(modifier = Modifier.height(16.dp))
            HorizontalDivider()
            Spacer(modifier = Modifier.height(8.dp))

            // Pocket action
            if (isInPocket) {
                ListItem(
                    headlineContent = { Text("Remove from Pocket") },
                    supportingContent = { Text("Still accessible in All Accounts") },
                    leadingContent = {
                        Icon(Icons.Outlined.StarOutline, null)
                    },
                    modifier = Modifier.clickable { onRemoveFromPocket() },
                )
            } else {
                ListItem(
                    headlineContent = { Text("Add to Pocket") },
                    supportingContent = { Text("Quick access on home screen") },
                    leadingContent = {
                        Icon(Icons.Filled.Star, null, tint = Color(0xFFFFD700))
                    },
                    modifier = Modifier.clickable { onAddToPocket() },
                )
            }

            // Set as default
            ListItem(
                headlineContent = { Text("Set as Default Account") },
                supportingContent = { Text("Use for payments & transfers") },
                leadingContent = {
                    Icon(Icons.Default.SwapHoriz, null)
                },
                modifier = Modifier.clickable { onSetAsDefault() },
            )

            // View details
            ListItem(
                headlineContent = { Text("View Account Details") },
                supportingContent = { Text("Transactions, statements & more") },
                leadingContent = {
                    Icon(Icons.Default.Info, null)
                },
                modifier = Modifier.clickable { onViewDetails() },
            )

            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}
```

---

### 3.7 Update HomeScreen

Update `HomeScreen` composable to integrate pocket:

```kotlin
@Composable
fun HomeScreenContent(
    state: HomeState,
    onAction: (HomeAction) -> Unit,
    // ... existing params
) {
    LazyColumn {
        // NEW: View toggle header
        item {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                // View dropdown button
                Box {
                    Row(
                        modifier = Modifier.clickable {
                            onAction(HomeAction.ShowViewDropdown)
                        },
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Text(
                            text = if (state.showPocketView && !state.pocket.isEmpty) {
                                "Pocket (${state.pocket.accounts.size})"
                            } else {
                                "All Accounts (${state.accounts.size})"
                            },
                            style = MaterialTheme.typography.titleMedium,
                        )
                        Icon(Icons.Default.ArrowDropDown, null)
                    }

                    ViewDropdownMenu(
                        isExpanded = state.showViewDropdown,
                        showPocketView = state.showPocketView,
                        pocketCount = state.pocket.accounts.size,
                        allAccountsCount = state.accounts.size,
                        onDismiss = { onAction(HomeAction.DismissViewDropdown) },
                        onSelectPocket = { onAction(HomeAction.TogglePocketView) },
                        onSelectAll = { onAction(HomeAction.TogglePocketView) },
                        onManagePocket = { onAction(HomeAction.NavigateToManagePocket) },
                    )
                }

                // Total balance
                Text(
                    text = CurrencyFormatter.format(
                        state.displayedTotalBalance,
                        state.displayedAccounts.firstOrNull()?.currency?.code ?: "USD",
                    ),
                    style = MaterialTheme.typography.titleLarge,
                )
            }
        }

        // Account pager - use displayedAccounts
        item {
            AccountList(
                accounts = state.displayedAccounts,
                defaultAccountId = state.defaultAccountId,
                onMarkAsDefault = { id, no -> onAction(HomeAction.MarkAsDefault(id, no)) },
                onAccountClick = { onAction(HomeAction.AccountDetailsClicked(it)) },
                onAccountLongPress = { account ->
                    onAction(HomeAction.ShowContextMenu(account))
                },
                isInPocket = { state.isInPocket(it) },
            )
        }

        // ... rest of existing content
    }

    // Context menu bottom sheet
    if (state.showContextMenu && state.contextMenuAccount != null) {
        AccountContextMenu(
            account = state.contextMenuAccount,
            isInPocket = state.isInPocket(state.contextMenuAccount.id),
            onDismiss = { onAction(HomeAction.DismissContextMenu) },
            onAddToPocket = {
                onAction(HomeAction.AddToPocket(state.contextMenuAccount.id))
            },
            onRemoveFromPocket = {
                onAction(HomeAction.RemoveFromPocket(state.contextMenuAccount.id))
            },
            onSetAsDefault = {
                onAction(HomeAction.MarkAsDefault(
                    state.contextMenuAccount.id,
                    state.contextMenuAccount.number,
                ))
                onAction(HomeAction.DismissContextMenu)
            },
            onViewDetails = {
                onAction(HomeAction.AccountDetailsClicked(state.contextMenuAccount.id))
                onAction(HomeAction.DismissContextMenu)
            },
        )
    }
}
```

---

## PHASE 4: MANAGE POCKET SCREEN

### 4.1 Create ManagePocketScreen

**File:** `feature/pocket/src/commonMain/kotlin/org/mifospay/feature/pocket/ManagePocketScreen.kt`

```kotlin
@Composable
fun ManagePocketScreen(
    onNavigateBack: () -> Unit,
    viewModel: ManagePocketViewModel = koinViewModel(),
) {
    val state by viewModel.stateFlow.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Manage Pocket") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, "Back")
                    }
                },
            )
        },
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
        ) {
            // In Pocket section
            item {
                Text(
                    text = "In Pocket (${state.pocketAccounts.size})",
                    style = MaterialTheme.typography.titleSmall,
                    modifier = Modifier.padding(16.dp),
                )
            }

            items(state.pocketAccounts) { account ->
                PocketAccountItem(
                    account = account,
                    isInPocket = true,
                    onToggle = { viewModel.handleAction(ManagePocketAction.RemoveFromPocket(account.id)) },
                )
            }

            // Not in Pocket section
            item {
                Text(
                    text = "Not in Pocket (${state.availableAccounts.size})",
                    style = MaterialTheme.typography.titleSmall,
                    modifier = Modifier.padding(16.dp),
                )
            }

            items(state.availableAccounts) { account ->
                PocketAccountItem(
                    account = account,
                    isInPocket = false,
                    onToggle = { viewModel.handleAction(ManagePocketAction.AddToPocket(account.id)) },
                )
            }
        }
    }
}

@Composable
private fun PocketAccountItem(
    account: Account,
    isInPocket: Boolean,
    onToggle: () -> Unit,
) {
    ListItem(
        headlineContent = { Text(account.name) },
        supportingContent = {
            Text("${account.number} • ${CurrencyFormatter.format(account.balance, account.currency.code)}")
        },
        leadingContent = {
            // Account type icon
        },
        trailingContent = {
            IconButton(onClick = onToggle) {
                Icon(
                    imageVector = if (isInPocket) Icons.Filled.Star else Icons.Outlined.StarOutline,
                    contentDescription = if (isInPocket) "Remove from Pocket" else "Add to Pocket",
                    tint = if (isInPocket) Color(0xFFFFD700) else MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        },
    )
}
```

---

## Jira Ticket Mapping

| Jira | Phase | Description |
|------|-------|-------------|
| MW-383 | Phase 1 | [API] Implement Pocket Service |
| MW-384 | Phase 2 | [REPO] Implement Pocket Repository |
| MW-379 | Phase 3 | [SCREEN] Pocket Dashboard (Home integration) |
| MW-385 | Phase 3 | [VM] Implement Pocket ViewModels |
| MW-380 | Phase 4 | [SCREEN] Manage Pocket |
| MW-386 | Phase 3-4 | [NAV] Add Pocket Navigation |
| MW-387 | Phase 5 | [TEST] Pocket Feature Tests |

---

## Commands to Execute

```bash
# Phase 1: Server layer
/server pocket

# Phase 2: Client layer
/client pocket

# Phase 3-4: Feature layer (Home integration + Manage screen)
/feature pocket

# Phase 5: Tests
/test pocket
```
