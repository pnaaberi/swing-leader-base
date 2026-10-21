# Swing Leader Base + Market Bias

TradingView Pine Script v6 overlay combining swing setups, a custom volume profile, support/resistance zones, Market Bias and Bollinger Bands.

## Use

Open `swing-leader-base.pine` in TradingView's Pine Editor, save it and select **Add to chart**. The first Inputs section, **0 · Indicators**, has the module switches; detailed settings remain grouped below.

This is an indicator, not a trading strategy or order-execution system. Profile volumes are approximated from chart OHLCV. Native TradingView VRVP is a separate optional companion. Market Bias is independent of the setup conditions. Not financial advice.

## Top module switches

Nine checkboxes cover SLB signals/levels/guide, moving averages, the custom volume profile/shelves, support/resistance, Fibonacci zones, structure breaks, candle profiles, Market Bias and Bollinger Bands. Fibonacci, structure breaks and candle profiles remain off by default; existing numeric, color and timeframe defaults are unchanged.

The SLB master also gates its bar tint and alert conditions; moving-average display is independent. The Market Bias master hides its ribbon, optional HA candles and data-window values, and gates its six alert conditions. Other module switches retain their original behavior. The custom-profile switch cannot control a separate native TradingView VRVP.

When upgrading a version that changes inputs, use a fresh instance or reset inputs to source defaults, then reapply personal overrides. Existing TradingView alerts retain their own settings snapshot; disable/recreate them separately after changing module switches.

## Market Bias defaults

| Setting | Default |
| --- | --- |
| Timeframe | Chart |
| Period / Smoothing | 7 / 20 |
| Show HA Candles / Market Bias | Off / On |
| Extra transparency / Oscillator period | 0 / 7 |
| Bullish color / base transparency | `#066756` / 13.3333% |
| Bearish color / base transparency | `#F75360` / 22.7451% |

The shorter periods change the default Market Bias overlay and its alerts, not the SLB setup formulas. Colors are calibrated visual estimates from the reference swatches, with at most one RGB level of checker-pixel reconstruction error under the calibration model. Quantized screenshot pixels cannot prove unique original RGBA values. Extra transparency 0 means no *additional* transparency, not an opaque bias fill.

Existing TradingView chart instances and saved templates can retain prior input values. Use the indicator's Defaults/reset controls or add a fresh instance to apply source defaults.

## Bollinger Bands

Enabled by default in **0 · Indicators**, with settings under **10 · Bollinger Bands**. Uses a 20-period simple moving average of close, with outer bands at ±2 standard deviations. **Upper line**, **Middle line**, **Lower line** and **Band fill** each have an independent color/opacity picker. The top switch hides all three lines and their fill. Length must be at least 2 and the multiplier must be positive. Bands need sufficient source history.

| Shared style token | Default | Usage |
| --- | --- | --- |
| `BB_LINE_COLOR` | `#000000` | Default for the independent upper, middle and lower line pickers |
| `BB_LINE_WIDTH` | `1` | All three lines: thinnest native plot width |
| `BB_FILL_COLOR` | `#EEEEEE` | Default for the band-fill color/opacity picker |

Black defaults suit a light chart background; choose different line colors for a dark chart. The four picker roles are `bbUpperColor`, `bbBasisColor`, `bbLowerColor` and `bbFillColor`. Changing one affects only that part. Bollinger Bands do not change setup signals, alerts or risk levels.

The Bollinger drawing block runs before Market Bias. Its customizable fill is below the Market Bias ribbon, while native fill/plot z-groups keep the thin Bollinger outlines crisp. No global plot-z-order override is used.

## Checks

Run `python3 -B -m unittest discover -s tests -v` for source-contract regressions. These check integration, style, input bounds and hide behavior; they do not execute Pine. Compile in TradingView, inspect the three lines/fill, then toggle the overlay off to check the chart. The original source is retained in Git for rollback.

### Optional swatch recovery

`tools/recover_swatch.py` uses Pillow to read screenshot swatches, calibrate checker backgrounds from known reference colors, and find the closest RGB/8-bit-alpha fit. Pillow is needed only for this tool and its tests, not for the Pine indicator.

Run `python3 -B tools/recover_swatch.py /path/to/private-config.json`. The JSON supplies `calibration_image`, `calibrations` (each with `rect`, `rgb`, `transparency`), `image`, and named `swatches` rectangles. Rectangles are `[left, top, right, bottom]`; transparency is 0–100. Output includes inferred colors, reconstructed checker colors, fit error and ambiguity. Incompatible calibration/swatches fail instead of claiming a match. Keep source screenshots and private configuration outside the repository.

## Status

Version 0.3.1 adds independent Bollinger line/fill color and opacity controls. Existing top module controls and Market Bias layering are retained. Source-contract checks pass; native TradingView compilation, color pickers and chart rendering remain unverified.

## Repository protection

`main` blocks force pushes and branch deletion, including for administrators. The repository remains public. Normal authorized fast-forward pushes remain allowed; pull-request reviews and required CI checks have not been added. Administrators can still manage protection settings, and public source can still be read or forked.

## Attribution and licenses

- Volume order-block logic: adapted from © LuxAlgo, [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), including its noncommercial and share-alike conditions.
- Market Bias: adapted from © Professeur_X, [Mozilla Public License 2.0](https://mozilla.org/MPL/2.0/).

Retain the respective notices and comply with the original terms. No blanket license or additional relicensing permission is asserted for the combined script.
