# Release Layer — mifos-x-group-banking (MifosSave)

## Platform Summary

| Platform | Package / Bundle | Track | Fastlane Lanes | Status |
|----------|-----------------|-------|----------------|--------|
| Android | org.mifos.groupbanking | internal → production | assembleReleaseApks, publishOnPlayStore | Not released |
| iOS | org.mifos.groupbanking | TestFlight → App Store | deployOnTestflight, deployOnAppStore | Not released |
| Firebase | mifos-mobile-apps group | beta | deployReleaseApkOnFirebase | Not released |

## Credentials Checklist

### Android
- [ ] `release_keystore.keystore` in source root
- [ ] `secrets/playStorePublishServiceCredentialsFile.json` (Play Console service account)
- [ ] `cmp-android/google-services.json` ✅ exists
- [ ] GitHub Secret: `ORIGINAL_KEYSTORE_FILE` (base64)
- [ ] GitHub Secret: `PLAYSTORECREDS`
- [ ] GitHub Secret: `GOOGLESERVICES`
- [ ] GitHub Secret: `FIREBASECREDS`
- [ ] ⚠️ Move keystore password out of `fastlane-config/project_config.rb` → ENV vars

### iOS
- [ ] `secrets/AuthKey.p8` (App Store Connect API key)
- [ ] Match SSH key → `secrets/match_ci_key`
- [ ] GitHub Secret: `APPSTORE_KEY_ID` = ZVQ6W6P822
- [ ] GitHub Secret: `APPSTORE_ISSUER_ID` = 7ab9e361-9603-4c3e-b147-be3b0f816099
- [ ] GitHub Secret: `MATCH_SSH_KEY_PATH`
- [ ] GitHub Secret: `TEAM_ID` = L432S2FZP5
- [ ] GitHub Secret: `NOTARIZATION_APPLE_ID` / `NOTARIZATION_PASSWORD`

### Firebase
- [ ] `secrets/firebaseAppDistributionServiceCredentialsFile.json`
- [ ] GitHub Secret: `FIREBASECREDS`

## CI/CD Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `multi-platform-build-and-publish.yml` | Manual / dispatch | Build + publish Android, iOS, Firebase |
| `promote-to-production.yml` | Manual | Promote internal → production on Play Store |
| `tag-weekly-release.yml` | Schedule | Auto-tag weekly releases |
| `monthly-version-tag.yml` | Schedule | Monthly version tagging |
| `pr-check.yml` | PR | Build validation |

## Fastlane Lanes Reference

| Lane | Platform | Purpose |
|------|----------|---------|
| `assembleDebugApks` | android | Debug APK build |
| `assembleReleaseApks` | android | Signed release APK |
| `bundleReleaseApks` | android | Signed release AAB |
| `deployReleaseApkOnFirebase` | android | Firebase App Distribution |
| `publishOnPlayStore` | android | Play Store upload (internal track) |
| `deployOnTestflight` | ios | TestFlight beta |
| `deployOnAppStore` | ios | App Store production |

## Release Commands

```bash
/release matrix          # View this dashboard
/release changelog       # Generate CHANGELOG.md for a version
/release android         # Deploy Android to Play Store internal track
/release ios             # Deploy iOS to TestFlight
/release firebase        # Deploy to Firebase App Distribution
```

## Security Notes

- `secrets/` directory is gitignored — NEVER commit credentials
- Keystore password in `fastlane-config/project_config.rb` line 31 should be
  moved to `ENV['KEYSTORE_PASSWORD']` + GitHub Secret
- Match repo: `git@github.com:openMF/ios-provisioning-profile.git`
