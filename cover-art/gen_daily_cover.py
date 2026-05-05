#!/usr/bin/env python3
"""Daily procedural cover art for 0704.

Each episode gets a unique wave field derived from its date, while the
typographic structure (grid density, glyph size, character sets) stays
identical to 0704_podcast_art_v2.png.

Usage:
    python3 gen_daily_cover.py                  # today
    python3 gen_daily_cover.py 2026-05-05       # specific date
    python3 gen_daily_cover.py 2026-05-05 /path/to/output.png
"""

import sys
import math
import os
import random
from datetime import date
from PIL import Image, ImageDraw, ImageFont


def date_seed(d: date) -> int:
    return int(d.strftime("%Y%m%d"))


def generate(target_date: date, out_path: str) -> str:
    seed = date_seed(target_date)
    random.seed(seed)

    W, H = 3000, 3000
    FONT_SIZE = 16

    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", FONT_SIZE)

    tmp = Image.new("RGB", (100, 50))
    td = ImageDraw.Draw(tmp)
    b = td.textbbox((0, 0), "M", font=font)
    CW = b[2] - b[0]
    CH = b[3] - b[1]
    COLS = W // CW
    ROWS = H // CH

    HEAVY = list("╬╪╫╦╩╠╣╔╗╚╝║═▓")
    MED   = list("╱╲┼┤├┬┴│─+×÷±≠")
    LIGHT = list("·∙∘○◦∞≈≡∂∇∑∏∆")

    GLYPH = {
        "0": [
            " █████  ",
            "██   ██ ",
            "██   ██ ",
            "██   ██ ",
            "██   ██ ",
            "██   ██ ",
            " █████  ",
        ],
        "7": [
            "███████ ",
            "     ██ ",
            "    ██  ",
            "   ██   ",
            "  ██    ",
            " ██     ",
            "██      ",
        ],
        "4": [
            "██   ██ ",
            "██   ██ ",
            "██   ██ ",
            "████████",
            "     ██ ",
            "     ██ ",
            "     ██ ",
        ],
    }
    TITLE = ["0", "7", "0", "4"]

    grid   = [[" "] * COLS for _ in range(ROWS)]
    bright = [[0.0]  * COLS for _ in range(ROWS)]

    # Per-episode wave parameters. Wide ranges so each day looks structurally
    # different, not just subtly shifted.
    def rf(lo, hi):
        return random.uniform(lo, hi)

    # Global field orientation: rotate the x/y axes slightly each episode
    angle = rf(-0.4, 0.4)
    cos_a, sin_a = math.cos(angle), math.sin(angle)

    # Planar wave frequencies and amplitudes: wide range
    pw = [
        (rf(6,  22), rf(4,  18), rf(0.10, 0.22)),
        (rf(3,  12), rf(12, 26), rf(0.09, 0.20)),
        (rf(8,  20), rf(8,  20), rf(0.08, 0.18)),
        (rf(2,   8), rf(18, 30), rf(0.07, 0.16)),
        (rf(14, 28), rf(2,   8), rf(0.07, 0.15)),
        (rf(5,  16), rf(5,  16), rf(0.06, 0.13)),
    ]

    # Radial sources: positions and frequencies vary widely
    sources = [
        (rf(0.05, 0.45), rf(0.05, 0.55), rf(12, 34)),
        (rf(0.55, 0.95), rf(0.45, 0.95), rf(10, 30)),
        (rf(0.30, 0.70), rf(0.30, 0.70), rf(18, 42)),
        (rf(0.05, 0.40), rf(0.55, 0.95), rf(8,  26)),
        (rf(0.55, 0.95), rf(0.05, 0.40), rf(14, 36)),
        (rf(0.20, 0.80), rf(0.10, 0.90), rf(10, 28)),
    ]
    radial_amp = rf(0.06, 0.14)

    noise_sigma = rf(0.04, 0.12)

    # Density thresholds: shift which proportion of cells are heavy/med/light
    t_heavy = rf(0.58, 0.78)
    t_med   = rf(0.35, 0.55)
    t_light = rf(0.10, 0.28)

    # Brightness levels: vary contrast and peak brightness per episode
    b_heavy = rf(0.60, 0.90)
    b_med   = rf(0.30, 0.55)
    b_light = rf(0.12, 0.30)

    def wave_pattern(c, r):
        x0, y0 = c / COLS, r / ROWS
        # Rotate field
        x = cos_a * x0 - sin_a * y0
        y = sin_a * x0 + cos_a * y0
        v = 0.0
        for (fx, fy, amp) in pw:
            v += math.sin(x * fx + y * fy) * amp
        for (cx, cy, f) in sources:
            d = math.sqrt((x0 - cx) ** 2 + (y0 - cy) ** 2)
            v += math.sin(d * f) * radial_amp
        v += random.gauss(0, noise_sigma)
        return (v + 1) / 2

    for r in range(ROWS):
        for c in range(COLS):
            d = max(0.0, min(1.0, wave_pattern(c, r)))
            if d > t_heavy:
                grid[r][c]   = random.choice(HEAVY)
                bright[r][c] = b_heavy
            elif d > t_med:
                grid[r][c]   = random.choice(MED)
                bright[r][c] = b_med
            elif d > t_light:
                grid[r][c]   = random.choice(LIGHT)
                bright[r][c] = b_light

    SCALE   = 4
    GAP     = 3
    START_R = 2
    START_C = 3

    # First pass: collect which cells are lit glyph pixels.
    glyph_cells = set()
    glyph_rows  = set()
    cc = START_C
    for ch in TITLE:
        glyph = GLYPH[ch]
        gw    = len(glyph[0])
        for lr, line in enumerate(glyph):
            for lc, px in enumerate(line):
                if px != " ":
                    for dr in range(SCALE):
                        for dc in range(SCALE):
                            gr = START_R + lr * SCALE + dr
                            gc = cc       + lc * SCALE + dc
                            if 0 <= gr < ROWS and 0 <= gc < COLS:
                                glyph_cells.add((gr, gc))
                                glyph_rows.add(gr)
        cc += gw * SCALE + GAP * SCALE

    # Dim background cells that fall within the glyph row band.
    # The dimming is gradual (falls off toward the edges of the band)
    # so there is no visible rectangle.
    if glyph_rows:
        r_min, r_max = min(glyph_rows), max(glyph_rows)
        band_h = max(r_max - r_min, 1)
        DIM = 0.28  # non-glyph cells inside the band are reduced to this fraction
        for r in range(r_min, r_max + 1):
            # Soft falloff: full dim at centre, eases toward edges
            t = 1.0 - abs((r - (r_min + r_max) / 2) / (band_h / 2))
            factor = 1.0 - t * (1.0 - DIM)
            for c in range(COLS):
                if (r, c) not in glyph_cells:
                    bright[r][c] *= factor

    # Second pass: write glyph pixels at full brightness.
    cc = START_C
    for ch in TITLE:
        glyph = GLYPH[ch]
        gw    = len(glyph[0])
        for lr, line in enumerate(glyph):
            for lc, px in enumerate(line):
                if px != " ":
                    for dr in range(SCALE):
                        for dc in range(SCALE):
                            gr = START_R + lr * SCALE + dr
                            gc = cc       + lc * SCALE + dc
                            if 0 <= gr < ROWS and 0 <= gc < COLS:
                                if grid[gr][gc] == " ":
                                    grid[gr][gc] = random.choice(HEAVY)
                                bright[gr][gc] = 1.0
        cc += gw * SCALE + GAP * SCALE

    img  = Image.new("RGB", (W, H), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    for r in range(ROWS):
        for c in range(COLS):
            ch = grid[r][c]
            if ch == " ":
                continue
            v = int(bright[r][c] * 255)
            draw.text((c * CW, r * CH), ch, font=font, fill=(v, v, v))

    img.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    args = sys.argv[1:]

    if args and args[0] not in ("today",):
        try:
            target = date.fromisoformat(args[0])
            args = args[1:]
        except ValueError:
            target = date.today()
    else:
        target = date.today()

    if args:
        out = args[0]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        out = os.path.join(
            os.path.dirname(script_dir),
            "briefings",
            f"0704-cover-{target.isoformat()}.png",
        )

    result = generate(target, out)
    print(f"Saved: {result}")
