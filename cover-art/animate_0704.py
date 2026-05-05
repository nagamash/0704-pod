#!/usr/bin/env python3
"""Animate 0704_podcast_art.png — flowing wave brightness modulation → MP4"""

import numpy as np
from PIL import Image
import subprocess
import math
import sys
import os

BASE_IMG  = "/Users/m.blomqvist/Desktop/video patrik/0704_podcast_art.png"
OUT_VIDEO = "/Users/m.blomqvist/Desktop/video patrik/0704_podcast_art.mp4"

FPS       = 30
DURATION  = 8          # seconds (seamless loop)
FRAMES    = FPS * DURATION

print(f"Loading base image…")
base = np.array(Image.open(BASE_IMG).convert("RGB")).astype(np.float32) / 255.0
H, W = base.shape[:2]
print(f"Base: {W}x{H}, generating {FRAMES} frames at {FPS}fps")

# Pre-build coordinate grids (normalised 0..1)
xs = np.linspace(0.0, 1.0, W, dtype=np.float32)
ys = np.linspace(0.0, 1.0, H, dtype=np.float32)
X, Y = np.meshgrid(xs, ys)   # (H, W)

def light_map(t: float) -> np.ndarray:
    """Returns (H,W) float32 multiplier in roughly [0.55, 1.15]"""
    # Multiple interference waves, each drifting at different speeds
    v  = np.sin(X * 14 + Y *  9 + t * 1.0)  * 0.12
    v += np.cos(X *  6 - Y * 17 + t * 0.7)  * 0.11
    v += np.sin((X + Y) * 11    + t * 1.3)  * 0.09
    v += np.cos((X - Y) *  8    + t * 0.5)  * 0.09
    # Radial pulses from off-centre anchors, each at its own tempo
    for (cx, cy, freq, speed) in [
        (0.12, 0.30, 22, 1.1),
        (0.85, 0.65, 19, 0.8),
        (0.50, 0.52, 28, 1.4),
        (0.30, 0.80, 16, 0.6),
        (0.70, 0.20, 24, 1.2),
    ]:
        d = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
        v += np.sin(d * freq + t * speed) * 0.07
    # Centre around 1.0
    return np.clip(v + 1.0, 0.55, 1.15).astype(np.float32)

# Pipe frames directly into ffmpeg
cmd = [
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{W}x{H}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "pipe:0",
    "-vcodec", "libx264",
    "-pix_fmt", "yuv420p",
    "-crf", "18",
    "-preset", "fast",
    OUT_VIDEO,
]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

for i in range(FRAMES):
    t = (i / FRAMES) * 2 * math.pi   # full cycle over the duration
    lm = light_map(t)                 # (H, W)
    frame = np.clip(base * lm[:, :, np.newaxis], 0.0, 1.0)
    proc.stdin.write((frame * 255).astype(np.uint8).tobytes())
    if i % 30 == 0:
        print(f"  frame {i}/{FRAMES}")

proc.stdin.close()
proc.wait()
print(f"\nSaved: {OUT_VIDEO}")
