import ast
import re
import unittest
from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "swing-leader-base.pine").read_text()
SHOWN_DEFAULTS = {
    "Minimal display": {
        "showTradeMarkers": True, "markerFontSize": 1, "markerKeep": 250,
        "markerGap": 0.22, "showMAs": True, "showRibbon": False,
        "showLevels": True, "showBarTint": False, "guideMode": "Compact",
        "guidePosition": "position.top_left",
    },
    "Support and resistance": {
        "showSR": True, "srMode": "Volume order blocks", "obLength": 5,
        "obMitigation": "Close", "obShowMid": True, "obMidStyle": "Dotted",
        "obMidWidth": 1, "srLeft": 5, "srRight": 5, "srHalfWidth": 0.3,
        "srKeep": 3, "srExtend": 30, "srMaxAge": 500,
        "srTransparency": 92, "srLabels": True,
    },
    "Optional overlays": {
        "showFibZones": False, "fibLookback": 80, "fibForward": 20,
        "showBOS": False, "bosLeft": 5, "bosRight": 5, "bosKeep": 8,
    },
    "Optional candle profiles": {
        "showSessionVP": False, "sessionVpScope": "Last candle",
        "sessionVpCount": 10, "sessionVpRows": 24, "sessionVpWidth": 88.0,
        "sessionVpAlignment": "Left", "sessionVpDisplay": "Up/Down split",
        "sessionVpShowPoc": True, "sessionVpTransparency": 45,
        "sessionVpTf": "5", "sessionVpSource": "HLC3",
    },
    "Market Bias": {
        "mb_ha_htf": "", "mb_ha_len": 7, "mb_ha_len2": 20,
        "mb_show_ha": False, "mb_show_mb": True,
        "mb_transparencyBoost": 0, "mb_osc_len": 7,
    },
}


def input_defaults(source):
    defaults = {}
    pattern = r"(?m)^(\w+)\s*=\s*(?:mb_forceCtf\()?input\.\w+\(([^,\n]*)"
    for name, raw in re.findall(pattern, source):
        raw = raw.strip()
        if raw in ("true", "false"):
            value = raw == "true"
        else:
            try:
                value = ast.literal_eval(raw)
            except (SyntaxError, ValueError):
                value = raw
        defaults[name] = value
    return defaults


class ScreenshotDefaultTests(unittest.TestCase):
    def test_shown_noncolor_defaults(self):
        defaults = input_defaults(SOURCE)
        for group, expected in SHOWN_DEFAULTS.items():
            for name, value in expected.items():
                with self.subTest(group=group, setting=name):
                    self.assertEqual(defaults.get(name), value)

    def test_market_bias_calibrated_color_defaults(self):
        expected = {"bull": (6, 103, 86, 13.3333), "bear": (247, 83, 96, 22.7451)}
        for side, rgba in expected.items():
            match = re.search(rf"mb_col_{side} = input.color\(color.rgb\(([^)]+)\)", SOURCE)
            self.assertIsNotNone(match)
            self.assertEqual(tuple(float(value) for value in match.group(1).split(",")), rgba)

    def test_transparency_help_matches_zero_default(self):
        setting = SOURCE.split("mb_transparencyBoost = input.int(", 1)[1].split("\n\n", 1)[0]
        self.assertIn("Default 0 adds no extra transparency", setting)
        self.assertNotIn("Default +30", setting)


if __name__ == "__main__":
    unittest.main()
