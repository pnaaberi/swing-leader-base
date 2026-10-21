# Swing Leader Base + Market Bias

TradingView Pine Script v6 overlay combining swing setups, a custom volume profile, support/resistance zones, Market Bias and Bollinger Bands.

## Use

Open `swing-leader-base.pine` in TradingView's Pine Editor, save it and select **Add to chart**. Settings are grouped by feature.

This is an indicator, not a trading strategy or order-execution system. Profile volumes are approximated from chart OHLCV. Native TradingView VRVP is a separate optional companion. Market Bias is independent of the setup conditions. Not financial advice.

## Bollinger Bands

Enabled by default under **10 · Bollinger Bands**. Uses a 20-period simple moving average of close, with outer bands at ±2 standard deviations. Length, multiplier and source are adjustable; the visibility toggle hides all three lines and their fill. Length must be at least 2 and the multiplier must be positive. Bands need sufficient source history.

| Shared style token | Default | Usage |
| --- | --- | --- |
| `BB_LINE_COLOR` | `#000000` | Upper, basis and lower lines: pure black |
| `BB_LINE_WIDTH` | `1` | All three lines: thinnest native plot width |
| `BB_FILL_COLOR` | `#EEEEEE` | Near-white light-gray fill between outer bands |

Fixed black styling is intended for a light chart background. Bollinger Bands are an independent overlay: they do not change setup signals, alerts or risk levels.

## Checks

Run `python3 -B -m unittest discover -s tests -v` for source-contract regressions. These check integration, style, input bounds and hide behavior; they do not execute Pine. Compile in TradingView, inspect the three lines/fill, then toggle the overlay off to check the chart. The original source is retained in Git for rollback.

## Status

Version 0.2.0. Existing setup logic and alerts are unchanged. Source-contract tests pass; TradingView compilation and chart rendering have not been verified.

## Attribution and licenses

- Volume order-block logic: adapted from © LuxAlgo, [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), including its noncommercial and share-alike conditions.
- Market Bias: adapted from © Professeur_X, [Mozilla Public License 2.0](https://mozilla.org/MPL/2.0/).

Retain the respective notices and comply with the original terms. No blanket license or additional relicensing permission is asserted for the combined script.
