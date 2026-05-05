"""
M4IX Tiled Cover Art — Flux 2 Dev, Realist variant

Same squarified treemap as cover_flux.py, but each tile tries to
visually depict the story rather than express an abstract emotional palette.

Prompt strategy:
  - Strip M4IX butler phrasing from each paragraph
  - Extract the core event/concept as a visual scene
  - Add a cinematic photography style suffix
  - Flux 2 Dev handles the rest

Usage:
    python cover_flux_real.py                    # today's briefing
    python cover_flux_real.py 2026-04-15         # specific date
    python cover_flux_real.py path/to/script.md  # explicit path

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
from PIL import Image
from io import BytesIO

# ----- CONFIG -----
COMFY_URL   = "http://127.0.0.1:8000"
UNET        = "flux2_dev_fp8mixed.safetensors"
CLIP        = "mistral_3_small_flux2_bf16.safetensors"
VAE         = "full_encoder_small_decoder.safetensors"
OUTPUT_DIR  = r"C:\Users\Remote\Dropbox\Pod"
CANVAS_SIZE = 1536
STEPS       = 28     # more steps for realism vs. abstract (18 is enough for abstract)
TILE_MIN    = 128

# Style suffix applied to every tile prompt.
# Pushes toward cinematic editorial photography.
REALISM_SUFFIX = (
    "photorealistic, editorial photography, cinematic still frame, "
    "sharp focus, dramatic studio lighting, high detail, 4K, "
    "no text, no logos, no watermarks"
)

# Negative prompt — Flux mostly ignores it but doesn't hurt
NEGATIVE = (
    "cartoon, illustration, painting, abstract, blurry, watermark, "
    "text, logo, face distortion, doll, toy, anime"
)


# ----- BUTLER CLEANER -----
# Patterns that are M4IX narrator voice, not story content.
# Strip these so Flux gets the actual subject, not the framing.
BUTLER_STRIP = [
    r"^(Good morning|Good evening|Good afternoon),?\s+Sir\.?\s*",
    r"\bSir\b",
    r"\bI would (note|caution|observe|suggest|add)\b[^.]*\.",
    r"\bone might (note|observe|say|argue)\b[^.]*\.",
    r"\bif one (had been wondering|enjoys?|were to)\b[^.]*",
    r"\bshall we say\b[^.]*",
    r"\bI am (pleased|afraid|happy) to (report|note|inform)\b[^.]*",
    r"\bThat concludes[^.]*\.",
    r"\bThis morning'?s?\b[^,]*,",
    r"\bdo have a\b[^.]*\.",
    r"\bI shall be here[^.]*\.",
    r"\bThe links for[^.]*\.",
    r"\b(en route to your inbox|for your consideration)\b[^.]*\.",
    r"\bMake of that what you will[^.]*\.",
]

def clean_butler(text: str) -> str:
    """Remove M4IX narrator voice patterns, leaving the factual content."""
    for pattern in BUTLER_STRIP:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)
    # Collapse whitespace
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


# ----- SCENE MAPPER -----
# Topic keywords → a concrete visual scene anchor.
# This gives Flux something physical to render when the paragraph
# text alone is too abstract ("the community is quite engaged...").
SCENE_ANCHORS = [
    (["claude", "anthropic", "opus"],
     "a glowing humanoid AI interface hologram in a dark server room, blue light"),
    (["openai", "gpt", "chatgpt"],
     "a sleek black monolith terminal with green text, dramatic backlighting"),
    (["google", "gemini", "deepmind"],
     "a vast data center interior, orange and gold light, rows of servers"),
    (["meta", "llama", "muse"],
     "a chrome robot hand holding a mirror reflecting fractured light"),
    (["nvidia", "gpu", "chip", "hardware", "design"],
     "extreme macro close-up of a GPU die, circuit traces glowing orange-red"),
    (["arxiv", "research", "paper", "proof", "math", "erdős"],
     "a mathematician at a whiteboard covered in equations, dramatic side lighting"),
    (["regulation", "law", "policy", "government", "state"],
     "a marble government building hallway, cold fluorescent light, empty"),
    (["job", "engineer", "work", "fired", "developer", "employment"],
     "an empty open-plan office at dusk, chairs pushed in, monitors dark"),
    (["local", "gguf", "ollama", "llama.cpp", "open.source", "minimax"],
     "a home server rack glowing blue in a dark room, DIY cables"),
    (["video", "lora", "comfy", "diffusion", "image", "generate"],
     "a photographer's studio with holographic frames floating, vivid colour"),
    (["podcast", "youtube", "channel", "episode"],
     "a professional podcast studio, microphones, acoustic foam, warm lamp"),
    (["airbnb", "host", "guest", "rental"],
     "a minimalist apartment interior at golden hour, soft editorial light"),
    (["tracking", "surveillance", "privacy", "audit", "opt.out"],
     "a person's silhouette surrounded by floating data streams in darkness"),
    (["quantum", "grid", "power", "energy", "infrastructure"],
     "high-voltage electrical towers at night, lightning in the background"),
    (["china", "japan", "korea", "geopolit", "nation", "global"],
     "a city skyline at night with satellite dishes and data relay towers"),
    (["jingle", "music", "audio", "sound"],
     "a recording studio mixing desk, warm lighting, vintage aesthetic"),
]

FALLBACK_SCENE = "a dramatic close-up of a computer screen in a dark room, code reflecting on glasses"

def extract_scene_anchor(text: str) -> str:
    low = text.lower()
    for keywords, scene in SCENE_ANCHORS:
        if any(k in low for k in keywords):
            return scene
    return FALLBACK_SCENE


def build_visual_prompt(paragraph: str) -> str:
    """
    Turn a M4IX script paragraph into a Flux-friendly visual prompt.

    Strategy:
    1. Clean out butler language
    2. Take the first 1-2 sentences (core news event)
    3. Prepend a scene anchor for physicality
    4. Append realism style suffix
    """
    cleaned = clean_butler(paragraph)

    # Take first 1-2 sentences, cap at ~180 chars
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    core = " ".join(sentences[:2])[:180].rstrip(".,;:—")

    # Scene anchor gives Flux a physical subject to render
    anchor = extract_scene_anchor(paragraph)

    prompt = f"{anchor}. {core}. {REALISM_SUFFIX}"
    return prompt


# ----- SCRIPT PARSER -----
def parse_script(md_path: str) -> list:
    text = Path(md_path).read_text(encoding="utf-8")

    match = re.search(r"## Full Script\s*\n(.*?)(\Z|^##\s)", text, re.DOTALL | re.MULTILINE)
    if not match:
        raise ValueError(f"Could not find '## Full Script' section in {md_path}")

    script_body = match.group(1).strip()
    paragraphs = [p.strip() for p in re.split(r"\n{2,}", script_body) if p.strip()]

    if len(paragraphs) < 2:
        raise ValueError("Script has fewer than 2 paragraphs")

    # Drop greeting (first) and sign-off (last)
    story_paras = paragraphs[1:-1]

    if not story_paras:
        raise ValueError("No story paragraphs after removing greeting/sign-off")

    stories = []
    for i, para in enumerate(story_paras):
        word_count = len(para.split())
        first_sentence = re.split(r"(?<=[.!?])\s", clean_butler(para))[0]
        title = first_sentence[:60].rstrip(".,;:—") if first_sentence else f"Story {i+1}"
        visual_prompt = build_visual_prompt(para)

        stories.append({
            "title": title,
            "word_count": word_count,
            "prompt": visual_prompt,
            "para": para,
        })
        print(f"  [{i+1}] {title[:55]}...")
        print(f"       {word_count}w | prompt: {visual_prompt[:80]}...")

    return stories


# ----- FLUX 2 TILE GENERATOR -----
def build_flux_workflow(prompt: str, width: int, height: int, seed: int) -> dict:
    return {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": UNET, "weight_dtype": "fp8_e4m3fn"
        }},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": CLIP, "type": "flux2"
        }},
        "3": {"class_type": "VAELoader", "inputs": {
            "vae_name": VAE
        }},
        "4": {"class_type": "CLIPTextEncode", "inputs": {
            "text": prompt, "clip": ["2", 0]
        }},
        "5": {"class_type": "CLIPTextEncode", "inputs": {
            "text": NEGATIVE, "clip": ["2", 0]
        }},
        "6": {"class_type": "EmptySD3LatentImage", "inputs": {
            "width": width, "height": height, "batch_size": 1
        }},
        "7": {"class_type": "KSampler", "inputs": {
            "seed": seed,
            "steps": STEPS,
            "cfg": 1.0,         # Flux Dev: keep at 1.0
            "sampler_name": "euler",
            "scheduler": "simple",
            "denoise": 1.0,
            "model": ["1", 0],
            "positive": ["4", 0],
            "negative": ["5", 0],
            "latent_image": ["6", 0]
        }},
        "8": {"class_type": "VAEDecode", "inputs": {
            "samples": ["7", 0], "vae": ["3", 0]
        }},
        "9": {"class_type": "SaveImage", "inputs": {
            "images": ["8", 0], "filename_prefix": "m4ix_real_tile"
        }}
    }


def generate_tile(prompt: str, width: int, height: int, seed: int) -> Image.Image:
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


# ----- SUBTLE VIGNETTE -----
def add_vignette(img: Image.Image, strength: float = 0.35) -> Image.Image:
    """Darken edges slightly — gives editorial photo feel to the composite."""
    from PIL import ImageDraw
    vignette = Image.new("L", img.size, 255)
    draw = ImageDraw.Draw(vignette)
    cx, cy = img.width // 2, img.height // 2
    for i in range(min(cx, cy), 0, -1):
        val = int(255 * (1 - strength * ((1 - i / min(cx, cy)) ** 2)))
        draw.ellipse([cx-i, cy-i, cx+i, cy+i], fill=val)
    r, g, b = img.split()
    r = Image.fromarray(__import__("numpy").array(r) * __import__("numpy").array(vignette) // 255, "L") if False else r
    # Simple multiply via paste with mask
    dark = Image.new("RGB", img.size, (0, 0, 0))
    img = Image.composite(dark, img, ImageChops_invert(vignette))
    return img

def ImageChops_invert(img):
    from PIL import ImageChops
    return ImageChops.invert(img)


# ----- THIN BORDER BETWEEN TILES -----
def draw_tile_borders(canvas: Image.Image, rects: list, color=(20, 20, 20), width=2) -> Image.Image:
    """Draw thin dark borders between tiles for visual separation."""
    from PIL import ImageDraw
    draw = ImageDraw.Draw(canvas)
    for _, x, y, w, h in rects:
        draw.rectangle(
            [int(x), int(y), int(x + w) - 1, int(y + h) - 1],
            outline=color, width=width
        )
    return canvas


# ----- MAIN -----
def main():
    today_str = date.today().strftime("%Y-%m-%d")

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.exists(arg):
            script_path = arg
        else:
            script_path = os.path.join(OUTPUT_DIR, f"ai-briefing-{arg.strip()}.md")
    else:
        script_path = os.path.join(OUTPUT_DIR, f"ai-briefing-{today_str}.md")

    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        print(f"   Usage: python cover_flux_real.py [YYYY-MM-DD | path/to/script.md]")
        sys.exit(1)

    print(f"\n📖 Parsing briefing: {script_path}")
    stories = parse_script(script_path)
    total_words = sum(s["word_count"] for s in stories)
    print(f"\n   {len(stories)} stories, {total_words} total words")
    print(f"   Canvas: {CANVAS_SIZE}×{CANVAS_SIZE}, Steps: {STEPS}\n")

    for s in stories:
        s["pct"]  = s["word_count"] / total_words
        s["area"] = s["pct"] * (CANVAS_SIZE ** 2)

    sorted_stories = sorted(stories, key=lambda s: s["area"], reverse=True)
    values = [(i, s["area"]) for i, s in enumerate(sorted_stories)]
    rects  = squarify(values, 0, 0, CANVAS_SIZE, CANVAS_SIZE)

    canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), (10, 10, 10))
    print(f"🎨 Generating {len(rects)} tiles...\n")

    skipped = 0
    generated_rects = []  # track rects that actually produced tiles (for border drawing)

    for idx, (story_idx, x, y, w, h) in enumerate(rects):
        story = sorted_stories[story_idx]

        gen_w = max(TILE_MIN, (int(w) // 16) * 16)
        gen_h = max(TILE_MIN, (int(h) // 16) * 16)

        if int(w) < TILE_MIN or int(h) < TILE_MIN:
            print(f"  [{idx+1}/{len(rects)}] SKIP '{story['title'][:40]}' — {int(w)}×{int(h)}px too small")
            skipped += 1
            continue

        seed = random.randint(0, 2147483647)
        print(f"  [{idx+1}/{len(rects)}] {story['pct']*100:.1f}% | '{story['title'][:45]}'")
        print(f"           gen {gen_w}×{gen_h} | seed {seed}")
        print(f"           ↳ {story['prompt'][:100]}...")

        try:
            tile = generate_tile(story["prompt"], gen_w, gen_h, seed)
            tile = tile.resize((int(w), int(h)), Image.LANCZOS)
            canvas.paste(tile, (int(x), int(y)))
            generated_rects.append((story_idx, x, y, w, h))
            print(f"           ✓")
        except Exception as e:
            print(f"           ❌ {e}")

    # Draw subtle borders between tiles
    canvas = draw_tile_borders(canvas, generated_rects)

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_filename = f"m4ix-cover-real-{today_str}.png"
    out_path = os.path.join(OUTPUT_DIR, out_filename)
    canvas.save(out_path, "PNG")

    print(f"\n✅  Saved: {out_path}")
    print(f"    Tiles generated: {len(generated_rects)}/{len(rects)}")
    if skipped:
        print(f"    Skipped (too small): {skipped}")
    print()


if __name__ == "__main__":
    main()
