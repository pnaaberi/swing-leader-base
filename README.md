# Swing Leader Base + Market Bias

TradingView Pine Script v6 overlay combining swing setups, a custom volume profile, support/resistance zones and Market Bias.

## Use

Open `swing-leader-base.pine` in TradingView's Pine Editor, save it and select **Add to chart**. Settings are grouped by feature.

This is an indicator, not a trading strategy or order-execution system. Profile volumes are approximated from chart OHLCV. Native TradingView VRVP is a separate optional companion. Market Bias is independent of the setup conditions. Not financial advice.

## Status

Version 0.1.0: nonessential comments, disabled custom-alert code and excess blank lines removed. All 772 executable lines, 94 inputs and 17 alert conditions are unchanged. Source-equivalence and mutation-detection checks passed; TradingView compilation and chart behavior remain unverified.

## Attribution and licenses

- Volume order-block logic: adapted from © LuxAlgo, [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), including its noncommercial and share-alike conditions.
- Market Bias: adapted from © Professeur_X, [Mozilla Public License 2.0](https://mozilla.org/MPL/2.0/).

Retain the respective notices and comply with the original terms. No blanket license or additional relicensing permission is asserted for the combined script.
