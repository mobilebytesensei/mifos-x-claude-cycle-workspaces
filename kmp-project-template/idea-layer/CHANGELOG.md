# Changelog — kmp-project-template idea-layer

## 2026-03-27

### Initial Sync
- Generated screens.json with 14 screens, 121 components, 50 interactions
- Screens: splash, tasks, editTask, profile, settings, notifications,
  privacyPolicy, termsOfService, openSourceLicenses, themeSettings, languageSelect + 3 state screens
- Scaffolded: APP_FLOW.mmd, APP_FLOW_CONNECTIONS.md, TAG_REGISTRY.yaml
- Generated: GENERATION_STATE.yaml, dashboard files, legal documents
- Source code synced: feature/home, feature/settings, feature/profile, cmp-navigation
- All 4 features covered: home, profile, settings, navigation

### Flow Fixes
- Fixed splash dead-end: added auto_navigate + "Get Started" button → tasks
- Fixed Settings flow: created navigable themeSettings, languageSelect screens (was non-renderable nested components)
- Added About screens: privacyPolicy, termsOfService, openSourceLicenses with full content
- Fixed editTask input types: was rendering as text instead of input fields
- Verified: 0 dead-ends, 0 broken targets, all main screens reachable via BFS
