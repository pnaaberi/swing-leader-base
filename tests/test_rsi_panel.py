"""Source contracts for RSI gauge removal; these do not execute Pine."""
import re
import unittest
from pathlib import Path

FULL = (Path(__file__).resolve().parents[1] / "swing-leader-base.pine").read_text()


class RsiRemovalTests(unittest.TestCase):
    def test_gauge_and_its_inputs_are_removed(self):
        self.assertNotRegex(FULL, r"\b(?:G_RSI|showRsiPanel|rsiLenInput|rsiPanelPos|rsiTbl|rsiP|RSI_CELLS)\b")

    def test_setup_rsi_and_existing_alerts_remain(self):
        self.assertIn("rsi = ta.rsi(close, 14)", FULL)
        self.assertEqual(len(re.findall(r"(?m)^alertcondition\(", FULL)), 17)


if __name__ == "__main__":
    unittest.main()
