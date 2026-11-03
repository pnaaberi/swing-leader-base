"""Source-only checks for the appended RSI panel; these do not compile or render Pine."""
import re
import unittest
from pathlib import Path

FULL = (Path(__file__).resolve().parents[1] / "swing-leader-base.pine").read_text()
PANEL = FULL.split("// ── RSI gauge", 1)[1]


class RsiPanelTests(unittest.TestCase):
    def test_gauge_is_appended_last_with_three_inputs(self):
        inputs = re.findall(r"(?m)^(\w+) = input\.\w+\(", PANEL)
        self.assertEqual(inputs, ["showRsiPanel", "rsiLenInput", "rsiPanelPos"])
        self.assertIn("position.bottom_right", PANEL)

    def test_timeframe_auto_length(self):
        self.assertIn("rsiAutoLen = chartSeconds <= 300 ? 9 : chartSeconds <= 3600 ? 12 : chartSeconds <= 86400 ? 14 : 10", PANEL)

    def test_setup_rsi_untouched_and_no_gauge_alerts(self):
        self.assertIn("rsi = ta.rsi(close, 14)", FULL)
        self.assertNotIn("alertcondition(", PANEL)
        self.assertNotIn("rsi :=", PANEL)


if __name__ == "__main__":
    unittest.main()
