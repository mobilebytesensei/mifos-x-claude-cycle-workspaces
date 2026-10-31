# signin — on-device verification, 2026-10-03

Device **OnePlus CPH2423** (`Q4CIZHA6Y5GMJV89`), clean install, live `apis.mifos.community`.

APK md5 **`b7f2f78464c0962f14badc5841d2acb2`** — the device-installed `base.apk` md5 was read back and
compared to the built APK before any capture (IA3-7). `adb install -r` does NOT kill the running
process, so every capture here was taken after the `device-verify-arm.sh` force-stop + md5 match;
without that a screenshot shows the OLD composition and reads as proof of something that never ran.

## What each capture confirms

| capture | state | confirms |
|---|---|---|
| `01-empty.png` | empty | **D1** CTA pinned to the bottom bar · **D12** no top app bar · logo tile holds the real asset · two-line title · toggle present |
| `03-validation_error.png` | validation_error | **D2** username trailing error icon + red border + "Invalid username length", while the password field stays clean with its toggle |
| `03b-password_error.png` | validation_error (password) | **pre-fix — shows the defect**: `123` in clear text |
| `03b-password_error-FIXED.png` | validation_error (password) | **D3** error icon REPLACES the toggle, username clean, password masked `•••` |
| `02-submitting.png` | submitting | **D4** modal overlay scrims the whole form; button persists as "Signing in…" disabled; password masked; bottom-bar CTA still reachable |
| `06-success.png` | success | live sign-in reaches the authenticated shell |

`03-validation_error.png` is the one that proves **per-field attribution**: only the offending field
is marked. v1 set BOTH error resources whenever EITHER rule failed, so a valid password still showed
a password error.

`06-success.png` exercises the whole vertical in one action — `core/network` auth DTO →
`core/data` `OnlineRequired` command → `core/datastore` session persist → `feature/signin` →
`cmp-navigation` root-nav transition.

## Not verified here

- **transport_error** — needs an induced server failure; the live instance answered normally.
- **offline** — needs airplane-mode toggling mid-request; not driven this run.

Both still rest on unit tests alone. Neither is a render-level change, so the risk is lower than the
four above, but neither is device-proven and they should not be described as such.

## The defect device-truth caught

The first `03b` capture showed the password **rendered in clear text**. Implementing D3 by setting
`isPasswordToggleDisplayed = false` — to hand the trailing slot to the error icon — also switched
masking off, because `MifosOutlinedTextField` derived its mask from
`!isPasswordVisible && isPasswordToggleDisplayed`. The password was displayed at exactly the moment
the user is told it is wrong.

**No unit test could have caught it.** The state's `password` value is identical either way; only the
rendering differs, and every existing assertion read state rather than pixels. v1 never had the bug —
it derived masking from `passwordVisibility` alone, independent of the trailing slot.

Fixed in `core/designsystem`: the mask now derives from the field's KIND
(`keyboardType == KeyboardType.Password`), never from whether a button happens to be drawn. That
module is template-derived, so the change is also enqueued upstream per
RULE-TEMPLATE-MODULE-FIX-UPSTREAM-001 rather than living only in this fork.

Locked by `SignInScreenUiTest.anInvalidPasswordIsStillMasked`, which was **proven RED** against the
old condition before the fix was restored — a guard that passes either way would have been worthless.

## Status

`maestro-not-authored`. This was Claude-driven live navigation, not an executed Maestro flow, so
**BE-3 is unsatisfied** and this run is not a substitute for one.
