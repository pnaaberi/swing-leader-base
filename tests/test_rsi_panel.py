"""Source-only checks for the appended RSI panel; these do not compile or render Pine."""
import re
import unittest
from pathlib import Path

FULL = (Path(__file__).resolve().parents[1] / "swing-leader-base.pine").read_text()
PANEL = FULL.split("// ── RSI panel", 1)[1]


class RsiPanelTests(unittest.TestCase):
    def test_panel_is_appended_last_with_four_inputs(self):
        inputs = re.findall(r"(?m)^(\w+) = input\.\w+\(", PANEL)
        self.assertEqual(inputs, ["showRsiPanel", "rsiLenInput", "rsiPanelBars", "rsiPanelPos"])
        self.assertIn("rsiPanelPos = input.string(position.bottom_right", PANEL)

    def test_timeframe_auto_length_and_closed_htf(self):
        self.assertIn("rsiAutoLen = chartSeconds <= 300 ? 9 : chartSeconds <= 3600 ? 12 : chartSeconds <= 86400 ? 14 : 10", PANEL)
        self.assertIn("ta.rsi(close, rsiPLen)[1], lookahead=barmerge.lookahead_on", PANEL)

    def test_setup_rsi_untouched_and_two_panel_alerts(self):
        self.assertIn("rsi = ta.rsi(close, 14)", FULL)
        self.assertEqual(len(re.findall(r"(?m)^alertcondition\(showRsiPanel", PANEL)), 2)
        self.assertNotIn(":=", PANEL)


if __name__ == "__main__":
    unittest.main()
