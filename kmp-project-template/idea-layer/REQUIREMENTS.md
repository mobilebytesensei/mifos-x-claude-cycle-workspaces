# Requirements — kmp-project-template

---

## Functional Requirements (FR)

| ID | Description | Feature | Status |
|:--:|-------------|---------|:------:|
| FR-001 | User can view task calendar with year/month/day selection | home | ✅ |
| FR-002 | User can create and edit tasks | home | ✅ |
| FR-003 | User can view task list filtered by selected date | home | ✅ |
| FR-004 | User can navigate between tasks and edit task screens | home | ✅ |
| FR-005 | User can view and edit profile information | profile | ✅ |
| FR-006 | User can access app settings | settings | ✅ |
| FR-007 | User can change app language | settings | ✅ |
| FR-008 | User can toggle notification preferences | settings | ✅ |
| FR-009 | User can switch between light/dark/system theme | settings | ✅ |
| FR-010 | User can enable/disable dynamic color theming | settings | ✅ |
| FR-011 | App shows splash screen on launch before navigation | navigation | ✅ |
| FR-012 | App provides bottom navigation bar for main screens | navigation | ✅ |
| FR-013 | App supports adaptive navigation (rail on larger screens) | navigation | ✅ |

## Server Functional Requirements (SFR)

| ID | Description | Service | Status |
|:--:|-------------|---------|:------:|
| SFR-001 | StorageService provides task CRUD operations | StorageService | ✅ |
| SFR-002 | UserPreferencesRepository provides user data persistence | DataStore | ✅ |
| SFR-003 | SampleDao provides database sample entity operations | Room DB | ✅ |

## Data Requirements (DR)

| ID | Description | Entity | Storage |
|:--:|-------------|--------|---------|
| DR-001 | System stores user preferences (theme, language, auth state) | UserData | DataStore |
| DR-002 | System stores sample entities with auto-generated IDs | SampleEntity | Room DB |
| DR-003 | System stores task entities in-memory with cache | TaskEntity | In-memory |

## Integration Requirements (IR)

| ID | Description | Service | Protocol |
|:--:|-------------|---------|----------|
| IR-001 | System integrates with Firebase Analytics for event tracking | Firebase | SDK |
| IR-002 | System integrates with Ktor for HTTP networking | Ktor | REST |
| IR-003 | System integrates with Fastlane for deployment automation | Fastlane | CLI |

## Non-Functional Requirements (NFR)

| ID | Description | Category |
|:--:|-------------|----------|
| NFR-001 | App supports 4 platforms: Android, iOS, Desktop, Web | Multi-platform |
| NFR-002 | App uses Material Design 3 with dynamic color support | Design |
| NFR-003 | App supports multiple languages via LanguageConfig | Localization |
| NFR-004 | App provides biometric/passcode authentication | Security |
| NFR-005 | App uses responsive/adaptive layouts for different screen sizes | Responsiveness |
| NFR-006 | App runs offline with local persistence (DataStore + Room) | Offline |
