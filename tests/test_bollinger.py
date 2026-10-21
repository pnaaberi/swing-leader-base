import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "swing-leader-base.pine").read_text()
BANDS = SOURCE.split('\nconst string G_BB = "10 · Bollinger Bands"', 1)[1].split('\nmb_o = ', 1)[0]
PLOTS = re.findall(r"(?m)^(?:bb\w+ = )?plot\((.+)$", BANDS)


class BollingerContractTests(unittest.TestCase):
    def test_native_calculation_and_input_bounds(self):
        self.assertIn(
            "[bbBasis, bbUpper, bbLower] = ta.bb(bbSource, bbLength, bbMultiplier)",
            BANDS,
        )
        self.assertIn('showBB = input.bool(true, "Bollinger Bands", group=G_CONTROLS', SOURCE)
        self.assertIn('input.int(20, "Length", minval=2, maxval=500', BANDS)
        self.assertIn(
            'input.float(2.0, "Standard deviations", minval=0.1, maxval=10.0',
            BANDS,
        )
        self.assertIn('input.source(close, "Source", group=G_BB)', BANDS)

    def test_three_thin_black_defaults_and_independent_line_colors(self):
        self.assertIn("const color BB_LINE_COLOR = #000000", BANDS)
        self.assertIn("const int BB_LINE_WIDTH = 1", BANDS)
        self.assertEqual(len(PLOTS), 3)
        for plot, role in zip(PLOTS, ("bbUpperColor", "bbBasisColor", "bbLowerColor")):
            self.assertIn(f"color={role}", plot)
            self.assertIn("linewidth=BB_LINE_WIDTH", plot)
        self.assertEqual(
            set(re.findall(r"plot\(showBB \? (bb\w+) : na", BANDS)),
            {"bbUpper", "bbBasis", "bbLower"},
        )

    def test_near_white_outer_band_fill_and_hide(self):
        self.assertIn("const color BB_FILL_COLOR = #EEEEEE", BANDS)
        self.assertIn(
            "fill(bbUpperPlot, bbLowerPlot, color=showBB ? bbFillColor : na,",
            BANDS,
        )
        self.assertIn('title="Bollinger fill", fillgaps=false)', BANDS)
        self.assertEqual(sum("showBB ? " in plot for plot in PLOTS), 3)

    def test_four_native_color_pickers_have_separate_defaults(self):
        roles = {
            "bbUpperColor": ("BB_LINE_COLOR", "Upper line"),
            "bbBasisColor": ("BB_LINE_COLOR", "Middle line"),
            "bbLowerColor": ("BB_LINE_COLOR", "Lower line"),
            "bbFillColor": ("BB_FILL_COLOR", "Band fill"),
        }
        for name, (default, label) in roles.items():
            self.assertIn(f'{name} = input.color({default}, "{label}", group=G_BB', BANDS)
        self.assertEqual(BANDS.count("input.color("), 4)

    def test_no_new_alerts_or_signal_mutation(self):
        self.assertEqual(len(re.findall(r"(?m)^alertcondition\(", SOURCE)), 17)
        self.assertNotIn("alertcondition(", BANDS)
        self.assertNotIn(":=", BANDS)
        self.assertNotIn("request.", BANDS)


if __name__ == "__main__":
    unittest.main()
