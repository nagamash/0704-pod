"""
M4IX Tiled Cover Art — Proof of Concept

Each story = one tile, sized by word count percentage.
Layout = squarified treemap.
Aesthetic = glitch/noise/grain with per-story emotional tint.

Requires: pip install pillow
"""
import requests
import time
import os
import random
from PIL import Image, ImageFilter
from io import BytesIO

# ----- CONFIG -----
COMFY_URL = "http://127.0.0.1:8000"
CHECKPOINT = "sd_xl_base_1.0.safetensors"
OUTPUT_DIR = r"C:\Users\Remote\Dropbox\Pod"
CANVAS_SIZE = 1024  # POC size, scale up later

# ----- FAKE STORIES (for POC) -----
# emotion_keywords describe the *feeling* not the content
STORIES = [
    {
        "title": "Stanford AI Index",
        "word_count": 220,
        "emotion": "dense information, overwhelming data, layered complexity, deep blue and electric teal, saturated grain"
    },
    {
        "title": "Meta Muse Spark",
        "word_count": 140,
        "emotion": "corporate monolith, metallic cold, hollow chrome, blue-grey, sterile geometry, glitched"
    },
    {
        "title": "Young Dev Jobs",
        "word_count": 90,
        "emotion": "erosion, decay, muted amber and rust, fading edges, entropy, melancholic grain"
    },
    {
        "title": "AI Regulation Wave",
        "word_count": 75,
        "emotion": "cold structure, fragmented boundaries, desaturated blue, bureaucratic noise, harsh lines"
    }
]

BASE_STYLE = "abstract, non-representational, chromatic aberration, heavy grain, signal noise, glitch art, no objects, no text"
NEGATIVE = "text, letters, faces, objects, photorealistic, clean, clear"


# ----- COMFYUI API -----
def generate_tile(prompt, width, height, seed):
    """Generate one tile via ComfyUI. Returns PIL Image."""
    workflow = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CHECKPOINT}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": 15, "cfg": 7, "sampler_name": "euler", "scheduler": "normal",
            "denoise": 1, "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0]
        }},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "m4ix_tile"}}
    }

    # Queue
    r = requests.post(f"{COMFY_URL}/prompt", json={"prompt": workflow})
    r.raise_for_status()
    prompt_id = r.json()["prompt_id"]

    # Poll
    start = time.time()
    while time.time() - start < 300:
        h = requests.get(f"{COMFY_URL}/history/{prompt_id}").json()
        if prompt_id in h and h[prompt_id].get("outputs"):
            img_info = h[prompt_id]["outputs"]["7"]["images"][0]
            # Download
            dl = requests.get(f"{COMFY_URL}/view", params={
                "filename": img_info["filename"],
                "subfolder": img_info.get("subfolder", ""),
                "type": img_info.get("type", "output")
            })
            return Image.open(BytesIO(dl.content))
        time.sleep(2)
    raise TimeoutError("Generation timed out")


# ----- SQUARIFIED TREEMAP -----
def squarify(values, x, y, w, h):
    """
    Simple squarified treemap.
    values: list of (id, normalized_area) sorted descending by area.
    Returns list of (id, x, y, w, h).
    """
    rects = []
    remaining = list(values)
    cur_x, cur_y, cur_w, cur_h = x, y, w, h

    while remaining:
        # Place current largest as row along shorter side
        if cur_w >= cur_h:
            # horizontal strip on left
            item_id, area = remaining.pop(0)
            strip_w = area / cur_h
            rects.append((item_id, cur_x, cur_y, strip_w, cur_h))
            cur_x += strip_w
            cur_w -= strip_w
        else:
            item_id, area = remaining.pop(0)
            strip_h = area / cur_w
            rects.append((item_id, cur_x, cur_y, cur_w, strip_h))
            cur_y += strip_h
            cur_h -= strip_h

    return rects


# ----- MAIN -----
def main():
    # 1. Calculate percentages
    total_words = sum(s["word_count"] for s in STORIES)
    for s in STORIES:
        s["pct"] = s["word_count"] / total_words
        s["area"] = s["pct"] * (CANVAS_SIZE ** 2)
        print(f"  {s['title']}: {s['pct']*100:.1f}% ({s['word_count']} words)")

    # 2. Sort descending by area
    sorted_stories = sorted(STORIES, key=lambda s: s["area"], reverse=True)

    # 3. Squarified layout
    values = [(i, s["area"]) for i, s in enumerate(sorted_stories)]
    rects = squarify(values, 0, 0, CANVAS_SIZE, CANVAS_SIZE)

    # 4. Generate each tile
    canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0))
    print(f"\nGenerating {len(rects)} tiles...\n")

    for idx, (story_idx, x, y, w, h) in enumerate(rects):
        story = sorted_stories[story_idx]
        # Round tile dims to multiples of 64 for SDXL
        gen_w = max(256, (int(w) // 64) * 64)
        gen_h = max(256, (int(h) // 64) * 64)

        prompt = f"{story['emotion']}, {BASE_STYLE}"
        seed = random.randint(0, 2147483647)
        print(f"  [{idx+1}/{len(rects)}] {story['title']} — gen {gen_w}×{gen_h}, seed {seed}")

        tile = generate_tile(prompt, gen_w, gen_h, seed)
        # Resize to exact rect dims and paste
        tile = tile.resize((int(w), int(h)), Image.LANCZOS)
        canvas.paste(tile, (int(x), int(y)))

    # 5. Unified glitch overlay (subtle chromatic aberration)
    r_ch, g_ch, b_ch = canvas.split()
    shift = 3
    r_shifted = Image.new("L", canvas.size, 0)
    r_shifted.paste(r_ch, (shift, 0))
    b_shifted = Image.new("L", canvas.size, 0)
    b_shifted.paste(b_ch, (-shift, 0))
    canvas = Image.merge("RGB", (r_shifted, g_ch, b_shifted))

    # 6. Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "m4ix-cover-poc.png")
    canvas.save(out_path, "PNG")
    print(f"\n✅ Cover saved: {out_path}")


if __name__ == "__main__":
    main()
