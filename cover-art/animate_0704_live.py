#!/usr/bin/env python3
"""0704 — live character cycling animation, vectorised via numpy atlas"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import subprocess, math, os

BASE = "/Users/m.blomqvist/Desktop/video patrik"
OUT  = f"{BASE}/0704_animated.mp4"

FPS      = 30
DURATION = 8          # seamless loop
FRAMES   = FPS * DURATION
W, H     = 3000, 3000
FONT_SIZE = 16

font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", FONT_SIZE)
tmp  = Image.new('L', (100, 50))
b    = ImageDraw.Draw(tmp).textbbox((0, 0), "M", font=font)
CW, CH = b[2]-b[0], b[3]-b[1]
COLS, ROWS = W // CW, H // CH
print(f"Grid {COLS}×{ROWS}  char {CW}×{CH}")

HEAVY = list("╬╪╫╦╩╠╣╔╗╚╝║═▓#")
MED   = list("╱╲┼┤├┬┴│─+×÷±≠@")
LIGHT = list("·∙∘○◦∞≈≡∂∇∑∏∆~%")
ALL   = HEAVY + MED + LIGHT
NH, NM, NL = len(HEAVY), len(MED), len(LIGHT)
NC = len(ALL)

# ── atlas: (NC, CH, CW) float32 ──────────────────────────────────────────────
print("Building char atlas…")
atlas = np.zeros((NC, CH, CW), dtype=np.float32)
for i, ch in enumerate(ALL):
    img = Image.new('L', (CW, CH), 0)
    ImageDraw.Draw(img).text((0, 0), ch, font=font, fill=255)
    atlas[i] = np.asarray(img, dtype=np.float32) / 255.0

# ── spatial grids (ROWS, COLS) ───────────────────────────────────────────────
CG = np.tile(np.linspace(0, 1, COLS, dtype=np.float32), (ROWS, 1))
RG = np.tile(np.linspace(0, 1, ROWS, dtype=np.float32)[:, None], (1, COLS))

def density(t):
    """Time-varying interference field → (ROWS, COLS) float32 in [0,1]"""
    v  = np.sin(CG*14 + RG* 9 + t*1) * 0.16
    v += np.cos(CG* 6 - RG*17 + t*2) * 0.14
    v += np.sin((CG+RG)*11    + t*3) * 0.11
    v += np.cos((CG-RG)* 8    + t*2) * 0.11
    v += np.sin(CG* 3  + RG*23 + t*1) * 0.09
    v += np.cos(CG*19  - RG* 5 + t*4) * 0.09
    for cx,cy,f,s in [(0.12,0.30,22,1),(0.85,0.65,19,2),
                      (0.50,0.52,28,3),(0.30,0.80,16,1),(0.70,0.20,24,2)]:
        d = np.sqrt((CG-cx)**2 + (RG-cy)**2)
        v += np.sin(d*f + t*s) * 0.08
    return np.clip((v+1)/2, 0, 1).astype(np.float32)

# per-cell cycling speed (integer → loops cleanly) and phase offset
rng   = np.random.default_rng(704)
rate  = rng.integers(3, 14, (ROWS, COLS)).astype(np.float32)   # 3–13 cycles / loop
phi   = rng.random((ROWS, COLS)).astype(np.float32)             # phase offset

# ── title mask ───────────────────────────────────────────────────────────────
GLYPH = {
    '0': [" █████  ","██   ██ ","██   ██ ","██   ██ ","██   ██ ","██   ██ "," █████  "],
    '7': ["███████ ","     ██ ","    ██  ","   ██   ","  ██    "," ██     ","██      "],
    '4': ["██   ██ ","██   ██ ","██   ██ ","████████","     ██ ","     ██ ","     ██ "],
}
SCALE, GAP, SR, SC = 4, 3, 2, 3
title_mask = np.zeros((ROWS, COLS), dtype=bool)
cc = SC
for ch in ['0','7','0','4']:
    gl = GLYPH[ch]; gw = len(gl[0])
    for lr,line in enumerate(gl):
        for lc,px in enumerate(line):
            if px != ' ':
                for dr in range(SCALE):
                    for dc in range(SCALE):
                        gr, gc = SR+lr*SCALE+dr, cc+lc*SCALE+dc
                        if 0<=gr<ROWS and 0<=gc<COLS:
                            title_mask[gr,gc] = True
    cc += gw*SCALE + GAP*SCALE

# ── frame builder ────────────────────────────────────────────────────────────
def make_frame(i):
    # t in [0, 2π) — all integer speed factors complete full cycles → seamless
    t = (i / FRAMES) * 2 * math.pi

    d = density(t)

    # cycling phase per cell: integer rate * (i/FRAMES) + offset → % 1
    ph = (rate * (i / FRAMES) + phi) % 1.0          # (ROWS, COLS)

    cidx  = np.zeros((ROWS, COLS), dtype=np.int32)
    brite = np.zeros((ROWS, COLS), dtype=np.float32)

    hm = d > 0.70
    mm = (d > 0.46) & ~hm
    lm = (d > 0.18) & ~hm & ~mm

    cidx[hm]  = (ph[hm]  * NH).astype(np.int32) % NH
    brite[hm] = 0.75

    cidx[mm]  = NH + (ph[mm]  * NM).astype(np.int32) % NM
    brite[mm] = 0.46

    cidx[lm]  = NH + NM + (ph[lm] * NL).astype(np.int32) % NL
    brite[lm] = 0.24

    # title: always bright, cycles 2× faster
    tp = (rate[title_mask] * (i / FRAMES) * 2 + phi[title_mask]) % 1.0
    cidx[title_mask]  = (tp * NH).astype(np.int32) % NH
    brite[title_mask] = 1.0

    # composite: atlas[(ROWS,COLS)] → (ROWS,COLS,CH,CW)
    tiles = atlas[cidx] * brite[:, :, None, None]

    # (ROWS,COLS,CH,CW) → (ROWS,CH,COLS,CW) → (H,W)
    canvas = tiles.transpose(0, 2, 1, 3).reshape(ROWS*CH, COLS*CW)

    rgb = np.stack([canvas, canvas, canvas], axis=-1)
    return (np.clip(rgb, 0, 1) * 255).astype(np.uint8)

# ── ffmpeg pipe ───────────────────────────────────────────────────────────────
cmd = ["ffmpeg","-y","-f","rawvideo","-vcodec","rawvideo",
       "-s",f"{W}x{H}","-pix_fmt","rgb24","-r",str(FPS),"-i","pipe:0",
       "-vcodec","libx264","-pix_fmt","yuv420p","-crf","18","-preset","fast",
       OUT]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

print(f"Rendering {FRAMES} frames…")
for i in range(FRAMES):
    proc.stdin.write(make_frame(i).tobytes())
    if i % FPS == 0:
        print(f"  {i//FPS}/{DURATION}s")

proc.stdin.close()
proc.wait()
print(f"\nSaved: {OUT}")
