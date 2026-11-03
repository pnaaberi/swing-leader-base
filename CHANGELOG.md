# Changelog

## Unreleased

- Replace the RSI line panel and `rsi-pane.pine` with a compact bottom-right RSI gauge: current value, zone word and a 30/70 position bar. Removes the RSI panel alerts.
- Add `rsi-pane.pine`, a separate RSI pane indicator; turn the in-chart RSI panel off by default.
- RSI panel: move to the top of the recent range and rename its input group to 11 (9 is Market Bias).
- RSI panel: replace the block table with a classic RSI line chart (70/50/30 levels, overbought/oversold fills, value label) drawn right of the last bar; the position input becomes panel height.
- Add an RSI panel (input group 9, default bottom-right): 16 blocky RSI history columns (10 points per block, zone colors at 70/50/30), current value with 3-bar slope and closed higher-timeframe RSI. Auto length by chart timeframe: ≤5m 9, ≤1h 12, ≤1D 14, above 10. Adds four inputs (appended last) and two overbought/oversold alerts; existing calculations, inputs and alerts are unchanged. TradingView compilation and rendering require manual verification.
- Docs: clarify range versus candle-profile data sources, per-module alert gates, configurable Bollinger defaults and display-only Market Bias transparency. No Pine changes.

## 0.3.3

- Enable the EMA cloud by default, raise signal font size to 7, narrow the custom profile to 13%, and add 18 points of Market Bias transparency.
- Use muted slate Bollinger outlines, a quieter middle line and 92%-transparent near-white fill; retain independent native color/opacity pickers.
- Emphasize the newest surviving S/R zone per side in both modes; fade older fills/borders/text without changing zone detection or suggesting confidence.
- Shorten profile tags to VAH / POC / VAL with explanatory tooltips and fade outside-value-area rows further.
- Give the guide one state badge, a score header, neutral detail rows and nonoverlapping action/candle-warning rows; preserve missing-history and error explanations.
- Preserve setup/risk calculations, alerts, input order and drawing budgets. Reset inputs or add a fresh instance for the new appearance defaults; native TradingView compilation and light/dark rendering still require manual verification.

## 0.3.2

- Restyle the optional EMA ribbon with a mint/rose vertical gradient and a 2 px slow-EMA edge.
- Rename its existing default-off control to EMA cloud ribbon; keep input order and defaults.
- Preserve EMA calculations, signals, alerts and Market Bias. TradingView compilation and rendering require manual verification.

## 0.3.1

- Add independent upper, middle and lower line colors plus band-fill color under Bollinger settings; each native picker includes opacity.
- Retain thin pure-black line/near-white fill defaults, top on/off control, Market Bias layering and all calculations/alerts.
- Add focused picker/default/wiring regressions and update the shared role inventory.
- Preserve the order of all 100 pre-existing input declarations by appending the four new picker inputs.

## 0.3.0

- Add a first Inputs section with nine module checkboxes; relocate existing switches without changing their defaults.
- Add SLB and Market Bias master gates for output and this configuration's alert conditions; preserve independent moving averages and existing module behavior.
- Draw Bollinger before Market Bias so the ribbon stays above the gray band fill, retaining native plot/fill z-groups and the original three black lines.
- Document input reset/fresh-instance migration and TradingView alert snapshots; add focused control/off/layer-order regressions.
- Security: protect `main` from force pushes and deletion, including administrators, while retaining public visibility and normal fast-forward pushes.

## 0.2.1

- Set Market Bias defaults to Period 7, Smoothing 20, HA candles off and extra transparency 0.
- Preserve calculations, other shown defaults and Bollinger settings; update the transparency tooltip.
- Add regressions for 50 readable non-color reference settings and apply calibrated teal/pink-red Market Bias color estimates.
- Document saved-chart/template overrides and the effect of shorter Market Bias periods on its default output and alerts.
- Add a Pillow swatch-recovery tool with quantized alpha, calibration, reconstruction error and ambiguity reporting; keep source screenshots/private configuration outside Git.

## 0.2.0

- Add independent Bollinger Bands using the native `ta.bb` calculation, defaulting to SMA 20 and ±2 standard deviations of close.
- Draw three thin pure-black lines with a near-white light-gray fill; add visibility, length, multiplier and source settings.
- Preserve existing setups, alerts, profile, zones and Market Bias code.
- Add focused source-contract regressions; TradingView compilation and actual chart rendering remain unverified.
## 0.1.0

- Prepare the supplied Pine v6 indicator for source distribution.
- Remove explanatory comments, commented-out custom-alert code and excessive blank lines.
- Preserve executable source, inputs, alerts, drawing behavior and required third-party notices.
- TradingView compilation and chart execution remain unverified.
