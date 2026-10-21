import tempfile
import unittest
from pathlib import Path

from PIL import Image

from tools.recover_swatch import calibrate, composite, recover


class SwatchRecoveryTests(unittest.TestCase):
    def test_recovers_quantized_synthetic_swatch(self):
        backgrounds = [[170, 170, 176], [255, 255, 255]]
        rgb = [19, 116, 103]
        transparency = 100 * 73 / 255
        pair = [composite(rgb, transparency, bg) for bg in backgrounds]
        result = recover(pair, backgrounds)
        self.assertLessEqual(result["max_channel_error"], 1)
        self.assertLess(abs(result["transparency"] - transparency), 2)
        self.assertTrue(all(abs(a - b) <= 3 for a, b in zip(rgb, result["rgb"])))
        self.assertIn("not uniquely identifiable", result["status"])

    def test_rejects_incompatible_swatch(self):
        with self.assertRaises(ValueError):
            recover([[10, 20, 230], [200, 220, 25]], [[170, 170, 176], [255, 255, 255]])

    def test_rejects_missing_checker_contrast(self):
        with self.assertRaises(ValueError):
            recover([[20, 30, 40], [20, 30, 40]], [[255, 255, 255], [255, 255, 255]])

    def test_rejects_inconsistent_calibration(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reference.png"
            image = Image.new("RGB", (2, 1))
            image.putdata([(128, 128, 130), (162, 162, 162)])
            image.save(path)
            swatches = [
                {"rect": [0, 0, 2, 1], "rgb": [100, 100, 100], "transparency": 40},
                {"rect": [0, 0, 2, 1], "rgb": [120, 120, 120], "transparency": 40},
            ]
            with self.assertRaisesRegex(ValueError, "disagree"):
                calibrate(path, swatches)


if __name__ == "__main__":
    unittest.main()
