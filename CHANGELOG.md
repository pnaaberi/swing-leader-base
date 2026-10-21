# Changelog

## Unreleased

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
