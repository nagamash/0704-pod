#!/usr/bin/env python3
"""
M4IX Cover Art Generator
------------------------
Generates episode cover art according to the M4IX visual identity system.

Usage:
    python generate_cover.py --date 2026-04-13 --episode 24 --headline "JAPAN BUILDS WALLS."

Outputs a 3000x3000 PNG to ./covers/ai-briefing-YYYY-MM-DD-cover.png
"""

import argparse
from datetime import date
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---------- Identity System Constants ----------

FONT_DIR = Path.home() / ".fonts" / "m4ix"

COLORS = {
    "ink":      (12, 12, 14),     # #0C0C0E
    "paper":    (243, 237, 226),  # #F3EDE2
    "cyan":     (0, 184, 196),    # #00B8C4  Signal Cyan
    "graphite": (85, 85, 91),     # #55555B
}

CANVAS = 3000
MARGIN = 200          # Outer canvas margin
FRAME_INSET = 80      # The 1px Ink rule inset from canvas edge (within margin)
FRAME_RULE_WIDTH = 2  # Hairline (scaled for 3000px)


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


# ---------- Drawing Primitives ----------

def draw_rule(draw, x1, y, x2, width, color):
    draw.line([(x1, y), (x2, y)], fill=color, width=width)


def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1], bbox[0], bbox[1]


def draw_tracked_text(draw, xy, text, fnt, fill, tracking=0):
    """Draw text with letter-spacing (in px). Returns total width."""
    x, y = xy
    total = 0
    for i, ch in enumerate(text):
        draw.text((x + total, y), ch, font=fnt, fill=fill)
        w, _, _, _ = text_size(draw, ch, fnt)
        total += w + (tracking if i < len(text) - 1 else 0)
    return total


def tracked_text_width(draw, text, fnt, tracking=0):
    total = 0
    for i, ch in enumerate(text):
        w, _, _, _ = text_size(draw, ch, fnt)
        total += w + (tracking if i < len(text) - 1 else 0)
    return total


# ---------- Cover Composition ----------

def render_cover(headline: str, date_str: str, episode: int, out_path: Path,
                 subtitle: str = "DAILY DISPATCH · MORNING BRIEFING",
                 classification: str = "CLASSIFIED — FOR M. BLOMQVIST ONLY"):
    """Render a single episode cover to PNG."""

    img = Image.new("RGB", (CANVAS, CANVAS), COLORS["paper"])
    draw = ImageDraw.Draw(img)

    # ----- Fonts -----
    wordmark_font    = font("PlayfairDisplay.ttf", 150)           # "M4IX"
    meta_font        = font("IBMPlexMono-Medium.ttf", 46)         # episode serial
    headline_font    = font("PlayfairDisplay.ttf", 440)           # The headline
    # Auto-scale headline if it's too wide
    subtitle_font    = font("IBMPlexSans-Medium.ttf", 42)         # section label
    classification_font = font("IBMPlexMono-Regular.ttf", 38)     # classification line
    flourish_font    = font("PlayfairDisplay-Italic.ttf", 54)     # italic flourish

    # ----- Document frame (1px Ink rule inset) -----
    frame_x1 = MARGIN
    frame_y1 = MARGIN
    frame_x2 = CANVAS - MARGIN
    frame_y2 = CANVAS - MARGIN
    draw.rectangle([frame_x1, frame_y1, frame_x2, frame_y2],
                   outline=COLORS["ink"], width=FRAME_RULE_WIDTH)

    # Inner padding inside the frame
    pad = 120
    inner_x1 = frame_x1 + pad
    inner_x2 = frame_x2 - pad

    # ----- TOP ZONE: Wordmark + serial -----
    top_baseline_y = frame_y1 + 140

    # Wordmark "M4IX" — Playfair Bold, tracked -40
    wordmark_text = "M4IX"
    wm_width = tracked_text_width(draw, wordmark_text, wordmark_font, tracking=-8)
    draw_tracked_text(draw, (inner_x1, top_baseline_y), wordmark_text,
                      wordmark_font, COLORS["ink"], tracking=-8)

    # Serial: "No. 024 · 2026-04-13" in mono, right-aligned
    serial_text = f"No. {episode:03d}  ·  {date_str}"
    sw = tracked_text_width(draw, serial_text, meta_font, tracking=2)
    # Vertical align to wordmark optical center
    serial_y = top_baseline_y + 75
    draw_tracked_text(draw, (inner_x2 - sw, serial_y), serial_text,
                      meta_font, COLORS["graphite"], tracking=2)

    # ----- Signal Cyan rule (the "transmission mark") -----
    cyan_rule_y = top_baseline_y + 240
    draw_rule(draw, inner_x1, cyan_rule_y, inner_x2, 4, COLORS["cyan"])

    # ----- HEADLINE ZONE -----
    # Auto-fit headline. Split on words; each line ALL CAPS Playfair Bold.
    headline_clean = headline.strip().upper()
    if not headline_clean.endswith(".") and not headline_clean.endswith("?") \
       and not headline_clean.endswith("!"):
        headline_clean += "."

    words = headline_clean.split()
    max_width = inner_x2 - inner_x1

    # Choose initial headline font size, shrink until longest word fits
    hf_size = 440
    while True:
        hf = font("PlayfairDisplay.ttf", hf_size)
        longest_word = max(words, key=lambda w: text_size(draw, w, hf)[0])
        if text_size(draw, longest_word, hf)[0] <= max_width or hf_size <= 180:
            break
        hf_size -= 10

    # Wrap words into lines greedily
    lines = []
    current = []
    for w in words:
        test = " ".join(current + [w])
        if text_size(draw, test, hf)[0] <= max_width:
            current.append(w)
        else:
            if current:
                lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))

    # If too many lines, shrink further
    while len(lines) > 4 and hf_size > 180:
        hf_size -= 20
        hf = font("PlayfairDisplay.ttf", hf_size)
        lines = []
        current = []
        for w in words:
            test = " ".join(current + [w])
            if text_size(draw, test, hf)[0] <= max_width:
                current.append(w)
            else:
                if current:
                    lines.append(" ".join(current))
                current = [w]
        if current:
            lines.append(" ".join(current))

    # Compute vertical placement: center the headline block in the middle zone
    line_height = int(hf_size * 1.02)
    block_h = len(lines) * line_height
    zone_top = cyan_rule_y + 120
    zone_bottom = frame_y2 - 420  # reserve space for bottom metadata
    zone_h = zone_bottom - zone_top
    start_y = zone_top + (zone_h - block_h) // 2

    for i, line in enumerate(lines):
        # Left-aligned (feels more document-like than centered)
        draw.text((inner_x1, start_y + i * line_height), line, font=hf, fill=COLORS["ink"])

    # ----- BOTTOM ZONE: Ink rule + subtitle + classification -----
    bottom_rule_y = frame_y2 - 340
    draw_rule(draw, inner_x1, bottom_rule_y, inner_x2, 2, COLORS["ink"])

    # Subtitle: "DAILY DISPATCH · MORNING BRIEFING"
    sub_y = bottom_rule_y + 50
    draw_tracked_text(draw, (inner_x1, sub_y), subtitle, subtitle_font,
                      COLORS["ink"], tracking=8)

    # Classification: mono, graphite
    class_y = sub_y + 80
    draw_tracked_text(draw, (inner_x1, class_y), classification,
                      classification_font, COLORS["graphite"], tracking=2)

    # Italic flourish (bottom-right, one per cover)
    flourish_text = "— served fresh"
    fw, _, _, _ = text_size(draw, flourish_text, flourish_font)
    draw.text((inner_x2 - fw, class_y - 10), flourish_text,
              font=flourish_font, fill=COLORS["graphite"])

    # ----- SAVE -----
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)
    print(f"Cover written: {out_path} ({out_path.stat().st_size:,} bytes)")


# ---------- Identity Preview Board ----------

def render_identity_board(out_path: Path):
    """A single large preview showing the entire system: wordmark, monogram,
    color palette, type specimens, and a sample cover thumbnail."""

    W, H = 3000, 4200
    img = Image.new("RGB", (W, H), COLORS["paper"])
    draw = ImageDraw.Draw(img)

    pad = 200

    # Document frame
    draw.rectangle([100, 100, W - 100, H - 100], outline=COLORS["ink"], width=2)

    # --- Top: system title ---
    title_font = font("PlayfairDisplay.ttf", 170)
    draw.text((pad, 230), "M4IX", font=title_font, fill=COLORS["ink"])

    subtitle_f = font("IBMPlexSans-Medium.ttf", 38)
    draw_tracked_text(draw, (pad, 430),
                      "VISUAL IDENTITY SYSTEM  ·  VERSION 1.0  ·  2026",
                      subtitle_f, COLORS["graphite"], tracking=8)

    # Signal cyan rule across
    draw_rule(draw, pad, 520, W - pad, 4, COLORS["cyan"])

    # --- Wordmark section ---
    label_f = font("IBMPlexSans-Medium.ttf", 32)
    draw_tracked_text(draw, (pad, 600), "01  ·  WORDMARK", label_f,
                      COLORS["ink"], tracking=6)

    wm_f = font("PlayfairDisplay.ttf", 380)
    draw_tracked_text(draw, (pad, 680), "M4IX", wm_f, COLORS["ink"], tracking=-20)

    caption_f = font("IBMPlexMono-Regular.ttf", 28)
    draw.text((pad, 1130),
              "Playfair Display Bold · tracking -40 · Ink #0C0C0E",
              font=caption_f, fill=COLORS["graphite"])

    # --- Monogram section (right side of wordmark zone) ---
    mono_x = W - pad - 520
    mono_y = 680
    draw.rectangle([mono_x, mono_y, mono_x + 520, mono_y + 520],
                   outline=COLORS["ink"], width=2)
    mono_f = font("PlayfairDisplay.ttf", 380)
    mw, mh, mox, moy = text_size(draw, "M", mono_f)
    draw.text((mono_x + (520 - mw) // 2 - mox, mono_y + (520 - mh) // 2 - moy - 20),
              "M", font=mono_f, fill=COLORS["ink"])
    # Cyan serial bar underneath
    draw_rule(draw, mono_x + 120, mono_y + 440, mono_x + 400, 4, COLORS["cyan"])

    draw.text((mono_x, mono_y + 560),
              "Small-context monogram (16×16 favicons, avatars)",
              font=caption_f, fill=COLORS["graphite"])

    # Divider
    draw_rule(draw, pad, 1260, W - pad, 1, COLORS["ink"])

    # --- Color system ---
    draw_tracked_text(draw, (pad, 1340), "02  ·  COLOR SYSTEM", label_f,
                      COLORS["ink"], tracking=6)

    swatch_y = 1440
    swatch_size = 340
    swatch_gap = 60
    swatches = [
        ("INK",           COLORS["ink"],      "#0C0C0E",  "Primary type, rules"),
        ("PAPER",         COLORS["paper"],    "#F3EDE2",  "Base surface, aged ivory"),
        ("SIGNAL CYAN",   COLORS["cyan"],     "#00B8C4",  "Accent ≤5% — live mark"),
        ("GRAPHITE",      COLORS["graphite"], "#55555B",  "Secondary text, metadata"),
    ]
    total_w = len(swatches) * swatch_size + (len(swatches) - 1) * swatch_gap
    sx = (W - total_w) // 2
    for i, (name, rgb, hexv, desc) in enumerate(swatches):
        x0 = sx + i * (swatch_size + swatch_gap)
        draw.rectangle([x0, swatch_y, x0 + swatch_size, swatch_y + swatch_size],
                       fill=rgb, outline=COLORS["ink"] if rgb == COLORS["paper"] else None,
                       width=2 if rgb == COLORS["paper"] else 0)
        # Name
        name_f = font("IBMPlexSans-Bold.ttf", 28)
        draw_tracked_text(draw, (x0, swatch_y + swatch_size + 30), name,
                          name_f, COLORS["ink"], tracking=4)
        hex_f = font("IBMPlexMono-Regular.ttf", 26)
        draw.text((x0, swatch_y + swatch_size + 75), hexv,
                  font=hex_f, fill=COLORS["graphite"])
        desc_f = font("IBMPlexSans-Regular.ttf", 22)
        draw.text((x0, swatch_y + swatch_size + 115), desc,
                  font=desc_f, fill=COLORS["graphite"])

    # Divider
    draw_rule(draw, pad, 2000, W - pad, 1, COLORS["ink"])

    # --- Typography specimens ---
    draw_tracked_text(draw, (pad, 2080), "03  ·  TYPOGRAPHY", label_f,
                      COLORS["ink"], tracking=6)

    # Playfair specimen
    specimen_h1 = font("PlayfairDisplay.ttf", 180)
    draw.text((pad, 2170), "Playfair Display", font=specimen_h1, fill=COLORS["ink"])
    draw.text((pad, 2385), "Ceremonial. Didone. The voice of the dispatch.",
              font=font("PlayfairDisplay-Italic.ttf", 48), fill=COLORS["graphite"])

    # IBM Plex Sans specimen
    specimen_h2 = font("IBMPlexSans-Medium.ttf", 130)
    draw.text((pad, 2510), "IBM Plex Sans", font=specimen_h2, fill=COLORS["ink"])
    draw.text((pad, 2670),
              "Geometric sans — editorial scaffolding. Labels, metadata.",
              font=font("IBMPlexSans-Regular.ttf", 40), fill=COLORS["graphite"])

    # IBM Plex Mono specimen
    specimen_h3 = font("IBMPlexMono-Medium.ttf", 110)
    draw.text((pad, 2790), "IBM Plex Mono", font=specimen_h3, fill=COLORS["ink"])
    draw.text((pad, 2930),
              "2026-04-13  ·  No.024  ·  SERIAL 0xCAFE  ·  TRANSMISSION OK",
              font=font("IBMPlexMono-Regular.ttf", 36), fill=COLORS["graphite"])

    # Divider
    draw_rule(draw, pad, 3100, W - pad, 1, COLORS["ink"])

    # --- Sample cover thumbnail ---
    draw_tracked_text(draw, (pad, 3180), "04  ·  EPISODE COVER APPLICATION",
                      label_f, COLORS["ink"], tracking=6)

    # Render a mini cover and paste it
    mini_path = Path("/tmp/m4ix_preview_cover.png")
    render_cover("JAPAN BUILDS WALLS.", "2026-04-13", 24, mini_path)
    mini = Image.open(mini_path).resize((850, 850), Image.LANCZOS)
    thumb_x = pad
    thumb_y = 3280
    img.paste(mini, (thumb_x, thumb_y))

    # Caption next to cover
    cap_title = font("PlayfairDisplay.ttf", 72)
    draw.text((thumb_x + 920, thumb_y + 40),
              "Episode 024", font=cap_title, fill=COLORS["ink"])
    cap_sub = font("IBMPlexMono-Regular.ttf", 32)
    draw.text((thumb_x + 920, thumb_y + 130),
              "2026-04-13", font=cap_sub, fill=COLORS["graphite"])

    # Principle snippets
    prin_f = font("IBMPlexSans-Regular.ttf", 28)
    principles = [
        "· Each cover is a document, not a poster.",
        "· Typography is the image. No photography.",
        "· Headlines compress the day into 2–5 words.",
        "· One Signal Cyan element per cover. Never two.",
        "· Restraint is the voice.",
    ]
    for i, p in enumerate(principles):
        draw.text((thumb_x + 920, thumb_y + 240 + i * 60),
                  p, font=prin_f, fill=COLORS["ink"])

    # Footer classification
    footer_f = font("IBMPlexMono-Regular.ttf", 26)
    draw_tracked_text(draw, (pad, H - 200),
                      "M4IX · VISUAL IDENTITY SYSTEM · COMPOSED FOR M. BLOMQVIST · 2026",
                      footer_f, COLORS["graphite"], tracking=3)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)
    print(f"Identity board written: {out_path} ({out_path.stat().st_size:,} bytes)")


# ---------- CLI ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=str(date.today()))
    ap.add_argument("--episode", type=int, default=24)
    ap.add_argument("--headline", default="JAPAN BUILDS WALLS.")
    ap.add_argument("--out-dir",
                    default="/sessions/happy-confident-wozniak/mnt/Pod/M4IX-Identity/covers")
    ap.add_argument("--identity-board", action="store_true",
                    help="Also render the identity preview board")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    cover_path = out_dir / f"ai-briefing-{args.date}-cover.png"
    render_cover(args.headline, args.date, args.episode, cover_path)

    if args.identity_board:
        board_path = Path(args.out_dir).parent / "M4IX-Identity-Board.png"
        render_identity_board(board_path)


if __name__ == "__main__":
    main()
