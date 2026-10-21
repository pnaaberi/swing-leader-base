import re
import unittest
from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "swing-leader-base.pine").read_text()
MASTERS = {
    "showSLB": "true", "showMAs": "true", "showVPVR": "true",
    "showSR": "true", "showFibZones": "false", "showBOS": "false",
    "showSessionVP": "false", "mb_enabled": "true", "showBB": "true",
}


class ModuleControlTests(unittest.TestCase):
    def test_all_nine_switches_are_first_and_unique(self):
        inputs = re.findall(r"(?m)^(\w+) = (?:mb_forceCtf\()?input\.\w+\(", SOURCE)
        self.assertEqual(inputs[:9], list(MASTERS))
        self.assertEqual(len(inputs), 100)
        for name, default in MASTERS.items():
            declarations = re.findall(
                rf"(?ms)^{name} = input\.bool\((.*?)\)\s*$", SOURCE,
            )
            self.assertEqual(len(declarations), 1, name)
            self.assertEqual(declarations[0].split(",", 1)[0], default)
            self.assertIn("group=G_CONTROLS", declarations[0])
        self.assertLess(SOURCE.index('"0 · Indicators"'), SOURCE.index("fastLen = input."))

    def test_bias_ribbon_is_after_bollinger_fill(self):
        self.assertLess(SOURCE.index("fill(bbUpperPlot, bbLowerPlot"),
                        SOURCE.index("fill(mb_p_l, mb_p_h"))
        self.assertLess(SOURCE.index("bbLowerPlot = plot("),
                        SOURCE.index("mb_p_h = plot("))
        self.assertNotIn("explicit_plot_zorder=true", SOURCE)

    def test_slb_off_hides_guide_levels_tint_and_conditions(self):
        for name in ("buySignal", "stopExit", "targetExit"):
            self.assertIn(f"{name} = showSLB and ", SOURCE)
        for price in ("stopPrice", "targetPrice"):
            self.assertIn(f"plot(showSLB and showLevels and inTrade ? {price} : na", SOURCE)
        self.assertIn('if showSLB and guideMode != "Off"', SOURCE)
        self.assertIn("barcolor(showSLB and showBarTint ?", SOURCE)
        self.assertIn("fastPlot = plot(showMAs ?", SOURCE)

    def test_bias_off_hides_all_output_and_gates_all_six_alerts(self):
        for value in ("mb_h2", "mb_l2", "mb_ha_avg"):
            self.assertIn(f"plot(mb_enabled ? {value} : na", SOURCE)
        self.assertIn("fill(mb_p_l, mb_p_h, mb_enabled and mb_show_mb ? mb_sigcolor : na)", SOURCE)
        self.assertIn("display=not mb_enabled ? display.none : mb_show_ha ?", SOURCE)
        alerts = re.findall(r"(?m)^alertcondition\(([^,\n]+),", SOURCE)
        self.assertEqual(len(alerts), 17)
        self.assertEqual(sum(value.startswith("mb_enabled and ") for value in alerts), 6)
        self.assertIn("mb_bullTrendSwitch = ta.change(mb_biasSignChange > 0)", SOURCE)
        self.assertIn("mb_bearTrendSwitch = ta.change(mb_biasSignChange < 0)", SOURCE)

    def test_existing_zone_and_structure_off_gates_remain(self):
        self.assertIn('obModeActive = showSR and srMode == "Volume order blocks"', SOURCE)
        self.assertIn("bullBOS = showBOS and barstate.isconfirmed", SOURCE)
        self.assertIn("bearBOS = showBOS and barstate.isconfirmed", SOURCE)
        self.assertIn("if showSR and srMode ==", SOURCE)
        self.assertIn("if showFibZones and fibUp", SOURCE)
        self.assertIn("if showSessionVP and lowerTfValid", SOURCE)
        self.assertIn("if showVPVR and includeProfileBar", SOURCE)


if __name__ == "__main__":
    unittest.main()
