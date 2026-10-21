import argparse
import json
import math
from collections import Counter
from pathlib import Path

from PIL import Image


def checker_pair(image_path, rect):
    with Image.open(image_path) as image:
        if len(rect) != 4 or not (0 <= rect[0] < rect[2] <= image.width and
                                  0 <= rect[1] < rect[3] <= image.height):
            raise ValueError("Swatch rectangle is outside the image")
        patch = image.convert("RGBA").crop(rect)
        background = Image.new("RGBA", patch.size, "white")
        pixels = Image.alpha_composite(background, patch).convert("RGB").getdata()
        common = Counter(pixels).most_common(2)
    colors = [color for color, count in common]
    if len(colors) == 1:
        colors.append(colors[0])
    return sorted(colors, key=sum)


def calibrate(image_path, swatches):
    estimates = [[], []]
    for swatch in swatches:
        transparency = swatch["transparency"] / 100
        if not 0 < transparency < 1:
            raise ValueError("Calibration needs a known partially transparent color")
        pair = checker_pair(image_path, swatch["rect"])
        for side in range(2):
            estimates[side].append([
                (pair[side][channel] - (1 - transparency) * swatch["rgb"][channel])
                / transparency for channel in range(3)
            ])
    if not swatches:
        raise ValueError("At least one calibration swatch is required")
    backgrounds = []
    for side in estimates:
        average = [sum(row[c] for row in side) / len(side) for c in range(3)]
        if any(value < -2 or value > 257 for value in average):
            raise ValueError("Calibration is incompatible with the supplied colors")
        if any(abs(row[c] - average[c]) > 3 for row in side for c in range(3)):
            raise ValueError("Calibration swatches disagree on the checker backgrounds")
        backgrounds.append([max(0, min(255, value)) for value in average])
    return backgrounds


def composite(rgb, transparency, background):
    t = transparency / 100
    return [math.floor((1 - t) * rgb[c] + t * background[c] + 0.5)
            for c in range(3)]


def recover(pair, backgrounds):
    delta = [backgrounds[1][c] - backgrounds[0][c] for c in range(3)]
    denominator = sum(value * value for value in delta)
    if denominator < 1:
        raise ValueError("Checker backgrounds need measurable contrast")
    observed_delta = [pair[1][c] - pair[0][c] for c in range(3)]
    center = max(0, min(0.999, sum(observed_delta[c] * delta[c]
                                 for c in range(3)) / denominator))
    candidates = []
    for alpha in range(255, 0, -1):
        t = (255 - alpha) / 255
        rgb = []
        for channel in range(3):
            estimate = sum(pair[side][channel] - t * backgrounds[side][channel]
                           for side in range(2)) / (2 * (1 - t))
            middle = max(0, min(255, round(estimate)))
            options = range(max(0, middle - 1), min(255, middle + 1) + 1)
            def error(value):
                return sum((math.floor((1 - t) * value +
                                       t * backgrounds[side][channel] + 0.5)
                            - pair[side][channel]) ** 2 for side in range(2))
            rgb.append(min(options, key=lambda value: (error(value), abs(value - estimate))))
        transparency = t * 100
        predicted = [composite(rgb, transparency, bg) for bg in backgrounds]
        errors = [predicted[s][c] - pair[s][c] for s in range(2) for c in range(3)]
        candidates.append((sum(value * value for value in errors),
                           abs(t - center), rgb, transparency, predicted, max(map(abs, errors)), alpha))
    best = min(candidates, key=lambda row: (row[0], row[1]))
    if best[5] > 2:
        raise ValueError("Swatch does not fit the calibrated checkerboard within 2 RGB levels")
    return {
        "rgb": best[2], "hex": "#" + "".join(f"{value:02X}" for value in best[2]),
        "transparency": round(best[3], 4), "alpha_8bit": best[6],
        "observed_checker_colors": pair,
        "reconstructed_checker_colors": best[4], "max_channel_error": best[5],
        "equivalent_fit_count": sum(row[0] == best[0] for row in candidates),
        "status": "calibrated visual estimate; original RGBA is not uniquely identifiable",
    }


def main():
    parser = argparse.ArgumentParser(description="Recover a closest RGBA fit from screenshot swatches")
    parser.add_argument("config", type=Path, help="Private JSON: calibration_image, calibrations, image, swatches")
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    backgrounds = calibrate(config["calibration_image"], config["calibrations"])
    results = {name: recover(checker_pair(config["image"], rect), backgrounds)
               for name, rect in config["swatches"].items()}
    print(json.dumps({"checker_backgrounds": backgrounds, "swatches": results}, indent=2))


if __name__ == "__main__":
    main()
