"""Source-only display regressions; these do not compile or render Pine."""
import hashlib
import re
import unittest
from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "swing-leader-base.pine").read_text()
# Exact protected regions from v0.3.2 (fc843b1), independent of local Git history.
BASELINE_HASHES = {
    "core": "c1ed1f6cc5fbc451c3c9684d07c21dfeddcf484cc15222938cbc4015a10164a3",
    "order_blocks": "55c42d1d19cca032fb1cc9934eb250297911d0c6fdbc2e39a2637689695ce268",
    "market_bias": "13a6d035aa6f4369655a9bdbdcbc2d13a1e3c9998ea39931eda325fce24169a4",
    "candle_profiles": "0dca60dd905e21871a3d86d23b0118f5fdb5ea192ce8b930a16cb57b1d6837a7",
    "fibonacci": "13ada7e93f73d31d253c836f7f45e965e8a4e6be360e4f910befef145868f811",
    "alerts": "9d2d06a7bd92a6c1df3769453fe72258da3e6787050603461117cabef9e1eca1",
    "input_order": "f7cf2ee2cda7e46ed72bfa1af5c52d3e77f6a7c614d765e51e6012d1f6655002",
}


def protected_hashes(source):
    blocks = {
        "core": source.split("emaFast = ta.ema", 1)[1].split("labelGap = ", 1)[0],
        "order_blocks": source.split("obUpper = ", 1)[1].split(
            "\nif barstate.islast\n    clearBoxes(obDrawBoxes)", 1)[0],
        "market_bias": source.split("mb_o = ta.ema", 1)[1],
        "candle_profiles": source.split("requestedProfiles = ", 1)[1].split(
            "\nsetupDataReady = ", 1)[0],
        "fibonacci": source.split("fibHigh = ", 1)[1].split("plot(showFibZones", 1)[0],
        "alerts": "\n".join(re.findall(r"(?m)^alertcondition\([\s\S]*?\)\s*$", source)),
        "input_order": "\n".join(re.findall(
            r"(?m)^(\w+) = (?:mb_forceCtf\()?input\.\w+\(", source)),
    }
    return {key: hashlib.sha256(value.encode()).hexdigest() for key, value in blocks.items()}


def zone_style_contract(source):
    return all(part in source for part in (
        "newest = i == array.size(zones) - 1",
        "zone = array.get(zones, array.size(zones) - 1 - i)",
        "bgcolor=color.new(tint, zoneFill(i == 0))",
        "border_color=color.new(tint, zoneBorder(i == 0))",
        "text_color=color.new(chart.fg_color, zoneText(i == 0))",
        "stylePivotZones(supportBoxes, true)",
        "stylePivotZones(resistanceBoxes, false)",
        "math.min(98, srTransparency + (newest ? 0 : ZONE_OLDER_FILL_FADE))",
    ))


class VisualPolishTests(unittest.TestCase):
    def test_calculations_alerts_and_input_order_unchanged(self):
        self.assertEqual(protected_hashes(SOURCE), BASELINE_HASHES)

    def test_preservation_check_rejects_logic_and_alert_mutations(self):
        for before, after, region in (
            ("score >= minScore and pivotBreak", "score > minScore and pivotBreak", "core"),
            ("close - atr * atrStopMult", "close + atr * atrStopMult", "core"),
            ('"SLB Buy"', '"Changed Buy"', "alerts"),
        ):
            with self.subTest(region=region, mutation=after):
                self.assertIn(before, SOURCE)
                changed = protected_hashes(SOURCE.replace(before, after, 1))
                self.assertNotEqual(changed[region], BASELINE_HASHES[region])

    def test_readable_markers_and_narrower_profile(self):
        self.assertIn('markerFontSize = input.int(7, "Signal font size", minval=1, maxval=12', SOURCE)
        self.assertIn('showRibbon = input.bool(true, "EMA cloud ribbon"', SOURCE)
        self.assertIn('vpWidthPct = input.float(13.0, "Histogram width % of range", minval=5, maxval=40', SOURCE)
        self.assertIn("vpTransparency + PROFILE_OUTSIDE_FADE", SOURCE)
        for short, full in (("VAH", "Value area high"), ("VAL", "Value area low")):
            self.assertRegex(SOURCE, rf'profileLevel\([^\n]+"{short}"')
            self.assertIn(f'words == "{short}" ? "{full}"', SOURCE)

    def test_zone_recency_in_both_modes(self):
        self.assertTrue(zone_style_contract(SOURCE))
        for name, value in (
            ("ZONE_RECENT_BORDER_T", 55), ("ZONE_OLDER_BORDER_T", 85),
            ("ZONE_RECENT_TEXT_T", 20), ("ZONE_OLDER_TEXT_T", 50),
            ("ZONE_OLDER_FILL_FADE", 3),
        ):
            self.assertIn(f"const int {name} = {value}", SOURCE)

    def test_zone_recency_rejects_reversed_or_missing_styles(self):
        for before, after in (
            ("zoneFill(i == 0)", "zoneFill(i != 0)"),
            ("stylePivotZones(supportBoxes, true)", ""),
        ):
            self.assertFalse(zone_style_contract(SOURCE.replace(before, after, 1)))

    def test_neutral_guide_and_noncolliding_rows(self):
        rows = SOURCE.split("guideRow(int row,", 1)[1].split("\nif barstate.islast", 1)[0]
        self.assertNotIn("mintColor", rows)
        self.assertNotIn("roseColor", rows)
        self.assertIn('setupDataReady ? "Score " + str.tostring(score) + "/7" : "Score —"', SOURCE)
        self.assertIn('guideRow(1, inTrade ? "Entry" : "Trigger"', SOURCE)
        self.assertIn('guideRow(2, "Next", actionText, true)', SOURCE)
        self.assertIn('guideRow(9, "Next", actionText, true)', SOURCE)
        self.assertIn('guideMode == "Checklist" ? 10 : 3, "Candle profiles"', SOURCE)
        self.assertIn("table.clear(guide, 0, 0, 1, 11)", SOURCE)
        self.assertIn("not setupDataReady ? \"Loading required history\"", SOURCE)

    def test_drawing_budgets_and_master_gates_retained(self):
        self.assertIn("max_boxes_count=500, max_lines_count=100, max_labels_count=500", SOURCE)
        self.assertIn('if showSLB and guideMode != "Off"', SOURCE)
        self.assertIn('if showSR and srMode == "Price pivots (original)"', SOURCE)
        self.assertIn('obModeActive = showSR and srMode == "Volume order blocks"', SOURCE)
        self.assertIn("math.min(95, vpTransparency + PROFILE_OUTSIDE_FADE)", SOURCE)


if __name__ == "__main__":
    unittest.main()
