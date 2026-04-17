# Services Index — kmp-project-template

| Service | Type | Feature | Module | Status |
|---------|------|---------|--------|:------:|
| StorageService | Local | home | feature:home | ✅ |
| UserPreferencesRepository | Local | settings | core:datastore | ✅ |
| UserDataRepository | Local | navigation | core:data | ✅ |
| NetworkMonitor | Local | navigation | core:data | ✅ |
| UserLogoutManager | Local | navigation | core:data | ✅ |
| KtorHttpClient | Remote | - | core-base:network | ✅ |
| SampleDao | Local (DB) | - | core:database | ✅ |

---

## Service → Repository Mapping

| Repository | Service | Data Source |
|-----------|---------|-------------|
| UserDataRepositoryImpl | UserPreferencesRepository | DataStore |
| NetworkMonitorImpl | - | System API |
| UserLogoutManagerImpl | UserDataRepository | DataStore |
| StorageServiceImpl | CacheManager | In-memory LRU cache |
