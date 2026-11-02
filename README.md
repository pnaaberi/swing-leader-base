# Swing Leader Base + Market Bias

TradingView Pine Script v6 overlay combining swing setups, a custom volume profile, support/resistance zones, Market Bias and Bollinger Bands.

## Use

Open `swing-leader-base.pine` in TradingView's Pine Editor, save it and select **Add to chart**. The first Inputs section, **0 · Indicators**, has the module switches; detailed settings remain grouped below.

This is an indicator, not a trading strategy or order-execution system. The custom range profile and shelves approximate volume from chart OHLCV; optional candle profiles use the selected lower-timeframe data, with up/down direction based on candle close versus open, not actual bid/ask delta. Native TradingView VRVP is a separate optional companion. Market Bias is independent of the setup conditions. Not financial advice.

## Top module switches

Nine checkboxes cover SLB signals/levels/guide, moving averages, the custom volume profile/shelves, support/resistance, Fibonacci zones, structure breaks, candle profiles, Market Bias and Bollinger Bands. Fibonacci, structure breaks and candle profiles remain off by default. Setup, volume, risk and timeframe defaults are unchanged by the visual polish.

The SLB master gates its signals, stop/target levels, guide, bar tint and five entry/exit alerts (Buy, Breakout, Pullback, Stop and Target); moving averages are independent. Structure-break alerts follow the Structure breaks switch, and the four order-block formation/invalidation alerts follow Support / resistance in Volume order blocks mode, independently of the SLB master. The Market Bias master hides its ribbon, optional HA candles and data-window values, and gates its six alert conditions. The custom-profile switch cannot control a separate native TradingView VRVP.

When upgrading a version that changes inputs, use a fresh instance or reset inputs to source defaults, then reapply personal overrides. Existing TradingView alerts retain their own settings snapshot; disable/recreate them separately after changing module switches.

## Visual hierarchy

Version 0.3.3 enables the EMA cloud by default, raises signal font size from 1 to 7, narrows the custom profile from 18% to 13%, and adds 18 points of Market Bias transparency. Bar tint and HA candles remain off. All 104 inputs retain their order; these appearance defaults intentionally change.

In both S/R modes, the newest surviving zone on each side has a stronger border and text. Older zones add 3 fill-transparency points (capped at 98) and use fainter borders/text. This denotes recency, not confidence, strength or a changed zone-detection rule. The existing midpoint controls remain independent.

Profile tags use VAH / POC / VAL with full names in hover tooltips; outside-value-area histogram rows fade further. The compact guide shows a state badge and score, a base-high trigger (or the reference entry while managing), and the existing next-action explanation. Its score is a setup-rule count, not a probability. Missing setup history shows a dash rather than an incomplete score. Checklist rows remain available, with neutral backgrounds and an extra Next row; candle-profile warnings occupy a separate row.

## EMA cloud ribbon

**4 · Minimal display → EMA cloud ribbon** is on by default and requires **0 · Indicators → Moving averages** on. It fills the existing fast/slow EMA gap with a translucent gradient: 55% opacity at the defined slow-EMA edge, fading to 10% at the fast edge. The slow edge is 2 px. Bullish clouds use the existing mint **Breakout / support** color; bearish clouds use rose **Stop / resistance**. Those color pickers also retain their existing uses elsewhere.

This is a visual treatment of our EMA ribbon, not a recreation of another indicator's calculations. EMA periods, signals, alerts and Market Bias calculations are unchanged. Turning the ribbon off restores mint/peach EMA colors; the slow line retains its 2 px width. Native TradingView compilation and visual acceptance of the gradient remain to be checked.

## Market Bias defaults

| Setting | Default |
| --- | --- |
| Timeframe | Chart |
| Period / Smoothing | 7 / 20 |
| Show HA Candles / Market Bias | Off / On |
| Extra transparency / Oscillator period | 18 / 7 |
| Bullish color / base transparency | `#066756` / 13.3333% |
| Bearish color / base transparency | `#F75360` / 22.7451% |

Market Bias period/smoothing settings affect its own calculations and alerts, not the SLB setup formulas; extra transparency changes display only. Colors are calibrated visual estimates from the reference swatches, with at most one RGB level of checker-pixel reconstruction error under the calibration model. Quantized screenshot pixels cannot prove unique original RGBA values. Extra transparency 18 adds 18 percentage points: strong/weak bias fills are 53%/93% transparent. Setting it to 0 restores the previous ribbon opacity.

Existing TradingView chart instances and saved templates can retain prior input values. Use the indicator's Defaults/reset controls or add a fresh instance to apply source defaults.

## Bollinger Bands

Enabled by default in **0 · Indicators**, with settings under **10 · Bollinger Bands**. Defaults to a 20-period simple moving average of close, with outer bands at ±2 standard deviations; Length, Standard deviations and Source are configurable. **Upper line**, **Middle line**, **Lower line** and **Band fill** each have an independent color/opacity picker. The top switch hides all three lines and their fill. Length must be at least 2 and the multiplier must be positive. Bands need sufficient source history.

All 100 pre-existing input declarations retain their order; the four color pickers are appended to that input schema.

| Shared style token | Default | Usage |
| --- | --- | --- |
| `BB_LINE_COLOR` | `#7C8798`, 20% transparent | Default for the independent upper and lower line pickers |
| `BB_BASIS_COLOR` | `#7C8798`, 55% transparent | Quieter middle-line default |
| `BB_LINE_WIDTH` | `1` | All three lines: thinnest native plot width |
| `BB_FILL_COLOR` | `#EEEEEE`, 92% transparent | Subtle band-fill default |

Muted slate defaults replace the previous black outlines, with a quieter middle line and 8%-opaque fill. The four picker roles remain `bbUpperColor`, `bbBasisColor`, `bbLowerColor` and `bbFillColor`; each picker changes only its own part. Confirm contrast on both light and dark charts and adjust the independent pickers if needed. Bollinger Bands do not change setup signals, alerts or risk levels.

The Bollinger drawing block runs before Market Bias. Its customizable fill is below the Market Bias ribbon, while native fill/plot z-groups keep the thin Bollinger outlines crisp. No global plot-z-order override is used.

## Checks

Run `python3 -B -m unittest discover -s tests -v` for source-contract regressions. These check integration, style, input bounds and hide behavior; they do not execute Pine. Compile in TradingView, inspect the three lines/fill, then toggle the overlay off to check the chart. The original source is retained in Git for rollback.

For visual acceptance, use a fresh/reset instance on the same symbol, timeframe and zoom as the previous revision. Check light and dark backgrounds; all nine switches and all-off; Compact/Checklist/Off guides with candle-profile warnings; both S/R modes as new zones form or invalidate; profile/VA/POC labels; and active stop/target visibility. Test insufficient history and a candle-profile timeframe equal to or above the chart timeframe: retain the loading/invalid-timeframe explanation, without overlapping guide rows. These are manual TradingView checks, not results supplied by the source tests. Roll back to the previous Git revision and restore prior saved settings if needed.

### Optional swatch recovery

`tools/recover_swatch.py` uses Pillow to read screenshot swatches, calibrate checker backgrounds from known reference colors, and find the closest RGB/8-bit-alpha fit. Pillow is needed only for this tool and its tests, not for the Pine indicator.

Run `python3 -B tools/recover_swatch.py /path/to/private-config.json`. The JSON supplies `calibration_image`, `calibrations` (each with `rect`, `rgb`, `transparency`), `image`, and named `swatches` rectangles. Rectangles are `[left, top, right, bottom]`; transparency is 0–100. Output includes inferred colors, reconstructed checker colors, fit error and ambiguity. Incompatible calibration/swatches fail instead of claiming a match. Keep source screenshots and private configuration outside the repository.

## Status

Version 0.3.3 is a display-only polish of signal labels, EMA/Bias/Bollinger hierarchy, zone recency, profile tags and the guide. Setup/risk calculations, zone detection, all 17 alerts, input ordering and drawing budgets are preserved. Source-contract checks do not prove native execution; TradingView compilation, color pickers, light/dark chart rendering and saved-instance migration remain unverified.

## Repository protection

`main` blocks force pushes and branch deletion, including for administrators. The repository remains public. Normal authorized fast-forward pushes remain allowed; pull-request reviews and required CI checks have not been added. Administrators can still manage protection settings, and public source can still be read or forked.

## Attribution and licenses

- Volume order-block logic: adapted from © LuxAlgo, [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), including its noncommercial and share-alike conditions.
- Market Bias: adapted from © Professeur_X, [Mozilla Public License 2.0](https://mozilla.org/MPL/2.0/).

Retain the respective notices and comply with the original terms. No blanket license or additional relicensing permission is asserted for the combined script.

## RSI panel

**11 · RSI panel** draws a classic RSI chart in the empty space right of the last bar, at the top of the recent 120-bar price range: purple RSI line, dashed 70/30 and dotted 50 levels, a faint 30–70 band, mint fill above 70 and rose fill below 30. A label shows length, chart timeframe, current RSI and the next-higher timeframe's RSI from closed bars only (no repaint). History bars and panel height are adjustable; widen the chart's right margin if the panel is cut off.

| Chart |
| Period / Smoothing | 7 / 20 |
| Show HA Candles / Market Bias | Off / On |
| Extra transparency / Oscillator period | 18 / 7 |
| Bullish color / base transparency | `#066756` / 13.3333% |
| Bearish color / base transparency | `#F75360` / 22.7451% |

Market Bias period/smoothing settings affect its own calculations and alerts, not the SLB setup formulas; extra transparency changes display only. Colors are calibrated visual estimates from the reference swatches, with at most one RGB level of checker-pixel reconstruction error under the calibration model. Quantized screenshot pixels cannot prove unique original RGBA values. Extra transparency 18 adds 18 percentage points: strong/weak bias fills are 53%/93% transparent. Setting it to 0 restores the previous ribbon opacity.

Existing TradingView chart instances and saved templates can retain prior input values. Use the indicator's Defaults/reset controls or add a fresh instance to apply source defaults.

## Bollinger Bands

Enabled by default in **0 · Indicators**, with settings under **10 · Bollinger Bands**. Defaults to a 20-period simple moving average of close, with outer bands at ±2 standard deviations; Length, Standard deviations and Source are configurable. **Upper line**, **Middle line**, **Lower line** and **Band fill** each have an independent color/opacity picker. The top switch hides all three lines and their fill. Length must be at least 2 and the multiplier must be positive. Bands need sufficient source history.

All 100 pre-existing input declarations retain their order; the four color pickers are appended to that input schema.

| Shared style token | Default | Usage |
| --- | --- | --- |
| `BB_LINE_COLOR` | `#7C8798`, 20% transparent | Default for the independent upper and lower line pickers |
| `BB_BASIS_COLOR` | `#7C8798`, 55% transparent | Quieter middle-line default |
| `BB_LINE_WIDTH` | `1` | All three lines: thinnest native plot width |
| `BB_FILL_COLOR` | `#EEEEEE`, 92% transparent | Subtle band-fill default |

Muted slate defaults replace the previous black outlines, with a quieter middle line and 8%-opaque fill. The four picker roles remain `bbUpperColor`, `bbBasisColor`, `bbLowerColor` and `bbFillColor`; each picker changes only its own part. Confirm contrast on both light and dark charts and adjust the independent pickers if needed. Bollinger Bands do not change setup signals, alerts or risk levels.

The Bollinger drawing block runs before Market Bias. Its customizable fill is below the Market Bias ribbon, while native fill/plot z-groups keep the thin Bollinger outlines crisp. No global plot-z-order override is used.

## Checks

Run `python3 -B -m unittest discover -s tests -v` for source-contract regressions. These check integration, style, input bounds and hide behavior; they do not execute Pine. Compile in TradingView, inspect the three lines/fill, then toggle the overlay off to check the chart. The original source is retained in Git for rollback.

For visual acceptance, use a fresh/reset instance on the same symbol, timeframe and zoom as the previous revision. Check light and dark backgrounds; all nine switches and all-off; Compact/Checklist/Off guides with candle-profile warnings; both S/R modes as new zones form or invalidate; profile/VA/POC labels; and active stop/target visibility. Test insufficient history and a candle-profile timeframe equal to or above the chart timeframe: retain the loading/invalid-timeframe explanation, without overlapping guide rows. These are manual TradingView checks, not results supplied by the source tests. Roll back to the previous Git revision and restore prior saved settings if needed.

### Optional swatch recovery

`tools/recover_swatch.py` uses Pillow to read screenshot swatches, calibrate checker backgrounds from known reference colors, and find the closest RGB/8-bit-alpha fit. Pillow is needed only for this tool and its tests, not for the Pine indicator.

Run `python3 -B tools/recover_swatch.py /path/to/private-config.json`. The JSON supplies `calibration_image`, `calibrations` (each with `rect`, `rgb`, `transparency`), `image`, and named `swatches` rectangles. Rectangles are `[left, top, right, bottom]`; transparency is 0–100. Output includes inferred colors, reconstructed checker colors, fit error and ambiguity. Incompatible calibration/swatches fail instead of claiming a match. Keep source screenshots and private configuration outside the repository.

## Status

Version 0.3.3 is a display-only polish of signal labels, EMA/Bias/Bollinger hierarchy, zone recency, profile tags and the guide. Setup/risk calculations, zone detection, all 17 alerts, input ordering and drawing budgets are preserved. Source-contract checks do not prove native execution; TradingView compilation, color pickers, light/dark chart rendering and saved-instance migration remain unverified.

## Repository protection

`main` blocks force pushes and branch deletion, including for administrators. The repository remains public. Normal authorized fast-forward pushes remain allowed; pull-request reviews and required CI checks have not been added. Administrators can still manage protection settings, and public source can still be read or forked.

## Attribution and licenses

- Volume order-block logic: adapted from © LuxAlgo, [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), including its noncommercial and share-alike conditions.
- Market Bias: adapted from © Professeur_X, [Mozilla Public License 2.0](https://mozilla.org/MPL/2.0/).

Retain the respective notices and comply with the original terms. No blanket license or additional relicensing permission is asserted for the combined script.

## RSI panel

**11 · RSI panel** draws a blocky RSI meter in the bottom-right corner (position selectable) with a small edge gap. Each column is one bar, oldest left; each block is 10 RSI points. Rose ≥ 70, peach 50–70, blue 30–50, mint ≤ 30; faint rows mark 70 and 30. The header shows length, chart timeframe, current RSI with a 3-bar slope arrow, and the next-higher timeframe's RSI from closed bars only (no repaint).

| Chart | Auto length | Higher TF |
|---|---|---|
| ≤ 5m | 9 | 15m |
| ≤ 15m | 12 | 1h |
| ≤ 1h | 12 | 4h |
| ≤ 4h | 14 | 1D |
| 1D | 14 | 1W |
| > 1D | 10 | 1M |

Set **RSI length** above 0 to override. The setup score keeps its own fixed RSI 14. Two alerts fire when panel RSI crosses above 70 or below 30.

### RSI in its own pane (recommended)

`rsi-pane.pine` is a separate indicator that shows the same timeframe-aware RSI in a normal pane under the chart: purple line, 70/50/30 levels, gradient fills above 70 / below 30 and a stepped higher-timeframe RSI line. Add it as a second script. The in-chart panel above is now off by default.
