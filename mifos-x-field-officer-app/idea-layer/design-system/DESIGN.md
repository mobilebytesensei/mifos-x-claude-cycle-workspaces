# Design system — mifos-x-field-officer-app

> **EXTRACTED from the shipped theme on 2026-10-02, not authored.** Tokens and their provenance live
> in `design-tokens.yaml`. This file is the narrative a mockup generator reads; that file is the
> numbers it must obey.

## Why this was extracted rather than designed

The app already ships a working, device-verified design system in
`core/designsystem/.../theme/`. Authoring a fresh palette here would make every generated mockup
diverge from the running app on its first frame, and that divergence would then be treated as the
spec by everything downstream. This is the same extraction-over-invention rule the feature import
follows (`FEATURE_LAYER_MIGRATION_SPEC.md` §7.0), applied to the design layer.

Verify any value with `grep -n "primaryLight = " core/designsystem/.../theme/Color.kt`.

## The look, in one paragraph

A light, near-white slate app (`#FAFAFB` background, `#0F172A` text) with an **indigo** primary
(`#4338CA`), **emerald** secondary (`#059669`) and **amber** tertiary (`#D97706`). Type is
**Outfit** — geometric, noticeably wider than Roboto at the same size — on the stock Material 3
scale. Surfaces are flat by default (`elevation.resting = 0`); elevation is reserved for genuine
layering, not decoration.

## What a mockup must get right

**Money is not brand.** `moneyPositive` (`#0E7A3B`) and `moneyNegative` (`#B3261E`) are semantic
tokens provided through `LocalFinanceColors`. A credit painted in indigo because indigo is the brand
colour is wrong, even though it looks on-brand. This is a lending app: the difference between a
positive and a negative balance is the most important colour decision on most screens.

**Touch targets have a floor.** `spacing.touchTargetMin = 48dp`. A field officer uses this standing
up, often one-handed, sometimes in poor light. A mockup that draws a 32dp tap target is proposing
something the implementation must then refuse.

**The four non-content states are branded and shared.** Loading, empty, error and no-network come
from `LocalScreenStateDefaults` (`core/store/AppScreenStateDefaults.kt`), not from per-screen art. A
mockup that invents its own empty-state illustration will disagree with the generated screen — and
those states are what the user actually sees most often on a slow connection.

**Spacing is an 8-point scale with a 4 and a 12.** `xs 4 · sm 8 · md 12 · lg 16 · xl 24 · xxl 32 ·
xxxl 48`. Nothing in between.

## Modes

`KptTheme` resolves **light** by default, with dark, dynamic-colour and `androidTheme` variants.
Mockups target light unless a screen specifically concerns dark mode — that is what the app opens
in, so it is what a reviewer should be comparing against.

## Known divergence

`MifosColor.kt` also carries a full **medium/high-contrast** set (`primaryLightMediumContrast =
#183566` and siblings) that `lightScheme` does not reference — a navy-based palette from an earlier
iteration, still compiled and unused. Recorded because it is easy to grep, easy to mistake for the
live palette, and would produce an entirely different-looking mockup. The live tokens are the ones
in `Color.kt` that `lightScheme` names.
