#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import random
import math
import os

random.seed(704)

W, H = 3000, 3000
FONT_SIZE = 16

font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", FONT_SIZE)

tmp = Image.new('RGB', (100, 50))
td = ImageDraw.Draw(tmp)
b = td.textbbox((0, 0), "M", font=font)
CW = b[2] - b[0]
CH = b[3] - b[1]
COLS = W // CW
ROWS = H // CH
print(f"Grid {COLS}x{ROWS}, char {CW}x{CH}")

HEAVY = list("╬╪╫╦╩╠╣╔╗╚╝║═▓")
MED   = list("╱╲┼┤├┬┴│─+×÷±≠")
LIGHT = list("·∙∘○◦∞≈≡∂∇∑∏∆")

GLYPH = {
    '0': [
        " █████  ",
        "██   ██ ",
        "██   ██ ",
        "██   ██ ",
        "██   ██ ",
        "██   ██ ",
        " █████  ",
    ],
    '7': [
        "███████ ",
        "     ██ ",
        "    ██  ",
        "   ██   ",
        "  ██    ",
        " ██     ",
        "██      ",
    ],
    '4': [
        "██   ██ ",
        "██   ██ ",
        "██   ██ ",
        "████████",
        "     ██ ",
        "     ██ ",
        "     ██ ",
    ],
}
TITLE = ['0', '7', '0', '4']

grid   = [[' '] * COLS for _ in range(ROWS)]
bright = [[0.0]  * COLS for _ in range(ROWS)]

def wave_pattern(c, r):
    x, y = c / COLS, r / ROWS
    v  = math.sin(x * 14 + y * 9)   * 0.16
    v += math.cos(x * 6  - y * 17)  * 0.14
    v += math.sin((x + y) * 11)     * 0.11
    v += math.cos((x - y) * 8)      * 0.11
    v += math.sin(x * 3  + y * 23)  * 0.09
    v += math.cos(x * 19 - y * 5)   * 0.09
    for (cx, cy, f) in [
        (0.12, 0.30, 22),
        (0.85, 0.65, 19),
        (0.50, 0.52, 28),
        (0.30, 0.80, 16),
        (0.70, 0.20, 24),
    ]:
        d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        v += math.sin(d * f) * 0.08
    v += random.gauss(0, 0.07)
    return (v + 1) / 2

for r in range(ROWS):
    for c in range(COLS):
        d = max(0.0, min(1.0, wave_pattern(c, r)))
        if d > 0.70:
            grid[r][c]   = random.choice(HEAVY)
            bright[r][c] = 0.72
        elif d > 0.46:
            grid[r][c]   = random.choice(MED)
            bright[r][c] = 0.44
        elif d > 0.18:
            grid[r][c]   = random.choice(LIGHT)
            bright[r][c] = 0.22
        # else: ' ' / black

SCALE    = 4   # chars per letter-pixel
GAP      = 3   # extra char-columns between letters
START_R  = 2
START_C  = 3

cc = START_C
for ch in TITLE:
    glyph = GLYPH[ch]
    gw    = len(glyph[0])
    for lr, line in enumerate(glyph):
        for lc, px in enumerate(line):
            if px != ' ':
                for dr in range(SCALE):
                    for dc in range(SCALE):
                        gr = START_R + lr * SCALE + dr
                        gc = cc       + lc * SCALE + dc
                        if 0 <= gr < ROWS and 0 <= gc < COLS:
                            # Boost brightness of whatever pattern char is already there
                            # so the letters emerge from the texture rather than replace it
                            if grid[gr][gc] == ' ':
                                grid[gr][gc] = random.choice(HEAVY)
                            bright[gr][gc] = 1.0
    cc += gw * SCALE + GAP * SCALE

img  = Image.new('RGB', (W, H), (0, 0, 0))
draw = ImageDraw.Draw(img)

for r in range(ROWS):
    for c in range(COLS):
        ch = grid[r][c]
        if ch == ' ':
            continue
        v = int(bright[r][c] * 255)
        draw.text((c * CW, r * CH), ch, font=font, fill=(v, v, v))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "0704_podcast_art_v2.png")
img.save(out, "PNG")
print(f"Saved: {out}")
