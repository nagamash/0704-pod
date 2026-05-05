"""
M4IX Tiled Cover Art — Flux 2 Dev variant

Each story = one tile, sized by its word count as a % of the full script.
Layout = squarified treemap (same as cover_poc.py).
Aesthetic = glitch/noise/grain with per-story emotional tint.
Generation = Flux 2 Dev via UNETLoader + CLIPLoader + VAELoader.

Usage:
    python cover_flux.py                    # auto-finds today's briefing script
    python cover_flux.py 2026-04-15         # specific date
    python cover_flux.py path/to/script.md  # explicit path

Requires: pip install pillow requests
"""

import requests
import time
import os
import re
import sys
import random
from datetime import date
from pathlib import Path
from PIL import Image, ImageFilter
from io import BytesIO

# ----- CONFIG -----
COMFY_URL   = "http://127.0.0.1:8000"
UNET        = "flux2_dev_fp8mixed.safetensors"
CLIP        = "mistral_3_small_flux2_bf16.safetensors"
VAE         = "full_encoder_small_decoder.safetensors"
OUTPUT_DIR  = r"C:\Users\Remote\Dropbox\Pod"
CANVAS_SIZE = 1536   # ~1.5k for now; bump to 3072 when ready
STEPS       = 18     # Flux dev sweet spot; reduce to 12 for speed
TILE_MIN    = 128    # px — skip tiles smaller than this


# ----- EMOTION MAP -----
# Keywords in the story title/content → emotional color palette for the prompt.
# Order matters — first match wins. Be deliberate, not exhaustive.
EMOTION_MAP = [
    (["anthropic", "claude"],        "deep electric blue, precision, quiet intelligence, faint cyan glow, structured grain"),
    (["openai", "gpt", "chatgpt"],   "stark white and green, clinical sharpness, high contrast, minimal noise, synthetic clarity"),
    (["google", "gemini", "deepmind"],"warm amber and gold, expansive, layered data, radiant depth, soft noise"),
    (["meta", "llama", "muse"],      "chrome and steel, cold geometry, hollow metallic, glitched symmetry"),
    (["nvidia", "gpu", "chip", "hardware"], "red heat, circuit density, compressed energy, bright orange pulse, industrial grain"),
    (["arxiv", "research", "paper", "model"], "deep indigo and violet, academic density, precise but overwhelming, layered blue"),
    (["regulation", "law", "policy", "state", "government"], "cold steel blue, rigid structure, bureaucratic noise, desaturated, clinical"),
    (["job", "work", "engineer", "worker", "fired"], "muted amber and rust, erosion, fading edges, entropy, melancholic grain"),
    (["open.source", "local", "gguf", "ollama", "llama.cpp"], "organic green and earth, collaborative warmth, distributed texture, natural grain"),
    (["video", "image", "comfy", "diffusion", "lora", "generation"], "shifting spectrum, iridescent, chromatic bloom, prismatic noise, kaleidoscopic"),
    (["podcast", "youtube", "video", "watch"], "warm amber broadcast, analogue warmth, film grain, soft vignette"),
    (["math", "proof", "erdős", "theorem", "reasoning"], "pure white and silver, crystalline precision, cold logic, sharp edges"),
    (["surveillance", "privacy", "tracking", "data"], "dark green and black, surveillance grid, oppressive texture, paranoid noise"),
    (["quantum", "grid", "power", "energy", "infrastructure"], "deep space purple, vast and cold, cosmic grain, electromagnetic noise"),
    (["china", "japan", "geopolit", "global", "nation"], "complex layered texture, competing signals, rich density, saturated conflict"),
]

FALLBACK_EMOTION = "abstract signal, chromatic aberration, analog grain, digital noise, glitch texture, shifting light"

BASE_STYLE  = "non-representational abstract art, chromatic aberration, heavy grain, signal noise, glitch aesthetic, no objects, no faces, no text, no letters"
NEGATIVE    = ""  # Flux largely ignores negative prompts; keep empty


# ----- EMOTION TAGGER -----
def tag_emotion(text: str) -> str:
    low = text.lower()
    for keywords, palette in EMOTION_MAP:
        if any(k in low for k in keywords):
            return palette
    return FALLBACK_EMOTION


# ----- SCRIPT PARSER -----
def parse_script(md_path: str) -> list[dict]:
    """
    Parse an ai-briefing-YYYY-MM-DD.md file.
    Splits the '## Full Script' section into paragraphs.
    Each paragraph (excluding greeting + sign-off) = one story.
    Returns list of {title, word_count, emotion}.
    """
    text = Path(md_path).read_text(encoding="utf-8")

    # Extract the full script section
    match = re.search(r"## Full Script\s*\n(.*?)(\Z|^##\s)", text, re.DOTALL | re.MULTILINE)
    if not match:
        raise ValueError(f"Could not find '## Full Script' section in {md_path}")

    script_body = match.group(1).strip()
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", script_body) if p.strip()]

    if len(paragraphs) < 2:
        raise ValueError("Script has fewer than 2 paragraphs — can't split into tiles")

    # Drop the greeting (first para) and sign-off (last para)
    # They're framing, not stories
    story_paras = paragraphs[1:-1]

    if not story_paras:
        raise ValueError("No story paragraphs found after removing greeting/sign-off")

    stories = []
    for i, para in enumerate(story_paras):
        word_count = len(para.split())
        # Best-effort title: first sentence up to 60 chars
        first_sentence = re.split(r"(?<=[.!?])\s", para)[0]
        title = first_sentence[:60].rstrip(".!?,;") if first_sentence else f"Story {i+1}"
        emotion = tag_emotion(para)
        stories.append({"title": title, "word_count": word_count, "emotion": emotion, "para": para})
        print(f"  [{i+1}] {title[:50]}... → {word_count} words")

    return stories


# ----- FLUX 2 TILE GENERATOR -----
def build_flux_workflow(prompt: str, width: int, height: int, seed: int) -> dict:
    return {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": UNET,
            "weight_dtype": "fp8_e4m3fn"
        }},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": CLIP,
            "type": "flux2"
        }},
        "3": {"class_type": "VAELoader", "inputs": {
            "vae_name": VAE
        }},
        "4": {"class_type": "CLIPTextEncode", "inputs": {
            "text": f"{prompt}, {BASE_STYLE}",
            "clip": ["2", 0]
        }},
        "5": {"class_type": "CLIPTextEncode", "inputs": {
            "text": NEGATIVE,
            "clip": ["2", 0]
        }},
        "6": {"class_type": "EmptySD3LatentImage", "inputs": {
            "width": width,
            "height": height,
            "batch_size": 1
        }},
        "7": {"class_type": "KSampler", "inputs": {
            "seed": seed,
            "steps": STEPS,
            "cfg": 1.0,
            "sampler_name": "euler",
            "scheduler": "simple",
            "denoise": 1.0,
            "model": ["1", 0],
            "positive": ["4", 0],
            "negative": ["5", 0],
            "latent_image": ["6", 0]
        }},
        "8": {"class_type": "VAEDecode", "inputs": {
            "samples": ["7", 0],
            "vae": ["3", 0]
        }},
        "9": {"class_type": "SaveImage", "inputs": {
            "images": ["8", 0],
            "filename_prefix": "m4ix_flux_tile"
        }}
    }


def generate_tile(prompt: str, width: int, height: int, seed: int) -> Image.Image:
    """Generate one tile via Flux 2. Returns PIL Image."""
    workflow = build_flux_workflow(prompt, width, height, seed)
    r = requests.post(f"{COMFY_URL}/prompt", json={"prompt": workflow}, timeout=15)
    r.raise_for_status()
    prompt_id = r.json()["prompt_id"]

    start = time.time()
    while time.time() - start < 600:
        h = requests.get(f"{COMFY_URL}/history/{prompt_id}", timeout=10).json()
        if prompt_id in h and h[prompt_id].get("outputs"):
            img_info = h[prompt_id]["outputs"]["9"]["images"][0]
            dl = requests.get(f"{COMFY_URL}/view", params={
                "filename": img_info["filename"],
                "subfolder": img_info.get("subfolder", ""),
                "type": img_info.get("type", "output")
            }, timeout=30)
            dl.raise_for_status()
            return Image.open(BytesIO(dl.content)).convert("RGB")
        time.sleep(2)

    raise TimeoutError(f"Tile timed out after {int(time.time()-start)}s")


# ----- SQUARIFIED TREEMAP -----
def squarify(values: list, x: float, y: float, w: float, h: float) -> list:
    """
    Greedy squarified treemap.
    values: list of (id, area) sorted descending.
    Returns list of (id, x, y, w, h).
    """
    rects = []
    remaining = list(values)
    cx, cy, cw, ch = x, y, w, h

    while remaining:
        item_id, area = remaining.pop(0)
        if cw >= ch:
            strip_w = area / ch
            rects.append((item_id, cx, cy, strip_w, ch))
            cx += strip_w
            cw -= strip_w
        else:
            strip_h = area / cw
            rects.append((item_id, cx, cy, cw, strip_h))
            cy += strip_h
            ch -= strip_h

    return rects


# ----- CHROMATIC ABERRATION -----
def chromatic_aberration(img: Image.Image, shift: int = 4) -> Image.Image:
    """Shift R channel right, B channel left for a unified glitch feel."""
    r, g, b = img.split()
    r_new = Image.new("L", img.size, 0)
    r_new.paste(r, (shift, 0))
    b_new = Image.new("L", img.size, 0)
    b_new.paste(b, (-shift, 0))
    return Image.merge("RGB", (r_new, g, b_new))


# ----- MAIN -----
def main():
    # Resolve script path
    today_str = date.today().strftime("%Y-%m-%d")
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.exists(arg):
            script_path = arg
        else:
            # treat as date string
            date_str = arg.strip()
            script_path = os.path.join(OUTPUT_DIR, f"ai-briefing-{date_str}.md")
    else:
        script_path = os.path.join(OUTPUT_DIR, f"ai-briefing-{today_str}.md")

    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        print(f"   Usage: python cover_flux.py [YYYY-MM-DD | path/to/script.md]")
        sys.exit(1)

    print(f"\n📖 Parsing briefing: {script_path}")
    stories = parse_script(script_path)
    total_words = sum(s["word_count"] for s in stories)
    print(f"   {len(stories)} stories, {total_words} total words\n")

    # Calculate proportional areas
    for s in stories:
        s["pct"]  = s["word_count"] / total_words
        s["area"] = s["pct"] * (CANVAS_SIZE ** 2)

    # Sort descending for squarify
    sorted_stories = sorted(stories, key=lambda s: s["area"], reverse=True)

    # Layout
    values = [(i, s["area"]) for i, s in enumerate(sorted_stories)]
    rects  = squarify(values, 0, 0, CANVAS_SIZE, CANVAS_SIZE)

    # Generate tiles
    canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0))
    print(f"🎨 Generating {len(rects)} tiles on Flux 2 Dev ({CANVAS_SIZE}×{CANVAS_SIZE} canvas, {STEPS} steps)...\n")

    skipped = 0
    for idx, (story_idx, x, y, w, h) in enumerate(rects):
        story = sorted_stories[story_idx]

        # Snap to multiples of 16 (Flux requirement); enforce minimum
        gen_w = max(TILE_MIN, (int(w) // 16) * 16)
        gen_h = max(TILE_MIN, (int(h) // 16) * 16)

        # Skip tiles too small to be meaningful (can't snap to valid dims)
        if gen_w < TILE_MIN or gen_h < TILE_MIN:
            print(f"  [{idx+1}/{len(rects)}] SKIP '{story['title'][:40]}' — tile too small ({int(w)}×{int(h)}px)")
            skipped += 1
            continue

        seed = random.randint(0, 2147483647)
        print(f"  [{idx+1}/{len(rects)}] '{story['title'][:45]}' — {story['pct']*100:.1f}%, gen {gen_w}×{gen_h}, seed {seed}")
        print(f"           palette: {story['emotion'][:60]}...")

        try:
            tile = generate_tile(story["emotion"], gen_w, gen_h, seed)
            tile = tile.resize((int(w), int(h)), Image.LANCZOS)
            canvas.paste(tile, (int(x), int(y)))
            print(f"           ✓ done")
        except Exception as e:
            print(f"           ❌ failed: {e} — leaving black")

    # Chromatic aberration pass over the whole canvas
    print(f"\n✨ Applying chromatic aberration...")
    canvas = chromatic_aberration(canvas, shift=4)

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_filename = f"m4ix-cover-flux-{today_str}.png"
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    canvas.save(out_path, "PNG")

    print(f"\n✅ Cover saved: {out_path}")
    if skipped:
        print(f"   ({skipped} tile(s) skipped — too small)")
    print()


if __name__ == "__main__":
    main()
