"""Source-only contracts for the 0.4.0 modules; these do not compile or render Pine."""
import unittest
from pathlib import Path


SOURCE = (Path(__file__).resolve().parents[1] / "swing-leader-base.pine").read_text()


class NewModuleTests(unittest.TestCase):
    def test_whale_dots_credit_and_label_budget(self):
        self.assertIn('// Detector adapted from the HK whale detector in "Fabio + Whale + VRVP" by saivivek0192.', SOURCE)
        self.assertIn("whaleBudgetRaw = math.min(whaleKeep, 500 - LABEL_RESERVE - markerKeep)", SOURCE)
        self.assertIn("whaleBudget = math.max(6, whaleBudgetRaw - whaleBudgetRaw % 6)", SOURCE)
        self.assertIn("if barstate.isconfirmed and wBuy > 0", SOURCE)
        self.assertIn("if barstate.isconfirmed and wSell > 0", SOURCE)

    def test_fib_zones_follow_master_switch(self):
        for gate in ("showFibZones and fibLavShow and fibUp", "showFibZones and fibSellShow and fibDn",
                     "showFibZones and fibTgtShow and fibUp", "showFibZones and fibTgtShow and fibDn",
                     "showFibZones and fibLabelShow"):
            self.assertIn(gate, SOURCE)

    def test_fundamentals_limited_to_stocks(self):
        self.assertIn('fundEligible = fundShow and (syminfo.type == "stock" or syminfo.type == "dr")', SOURCE)
        self.assertEqual(SOURCE.count("request.financial("), 9)

    def test_trendlines_use_closed_bars_and_are_redrawn_once(self):
        self.assertIn("if barstate.isconfirmed and not na(tlPH)", SOURCE)
        self.assertIn("if barstate.isconfirmed and not na(tlPL)", SOURCE)
        self.assertIn("lastK = barstate.isconfirmed ? bar_index : bar_index - 1", SOURCE)
        self.assertIn("    tlLines.clear()\n    if tlShow", SOURCE)

    def test_overlapping_order_blocks_replaced(self):
        self.assertIn("dropOverlappingZones(obSupports, hl2[obLength], low[obLength])", SOURCE)
        self.assertIn("dropOverlappingZones(obResistances, high[obLength], hl2[obLength])", SOURCE)


if __name__ == "__main__":
    unittest.main()
