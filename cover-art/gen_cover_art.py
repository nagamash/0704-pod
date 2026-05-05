#!/usr/bin/env python3
"""
ComfyUI Abstract Cover Art Generator for M4IX Briefing
Generates intriguing, glitchy, noisy abstract images via SDXL
"""

import json
import requests
import urllib.request
import urllib.error
import time
import uuid
import os
import random
from datetime import date
from pathlib import Path

# Configuration
COMFY_URL = "http://127.0.0.1:8000"
COMFY_OUTPUT_DIR = "outputs"  # Relative to ComfyUI folder
FINAL_OUTPUT_DIR = r"C:\Users\Remote\Dropbox\Pod"  # Where to save final images

# Ensure output dirs exist
os.makedirs(FINAL_OUTPUT_DIR, exist_ok=True)

# SDXL model - adjust to match your checkpoint filename
CHECKPOINT = "sd_xl_base_1.0.safetensors"  # Change this to your actual SDXL model

# Prompt for abstract glitch aesthetic
POSITIVE_PROMPT = """corrupted signal made visible, chromatic aberration cascading, color separation artifacts,
analog grain overlaid on digital noise, intriguing visual entropy, fragmented information landscape,
glitch texture, the feeling of data overload, color bleeding, quantum uncertainty rendered as light,
noisy texture, color glitches, grain, distorted reality, signal decay"""

NEGATIVE_PROMPT = "recognizable objects, faces, text, legible writing, photorealistic, clear subjects"

def build_workflow(seed: int = -1, width: int = 768, height: int = 768) -> dict:
    """Build SDXL txt2img workflow API format for abstract art generation"""
    # Convert -1 to random seed (ComfyUI requires seed >= 0)
    if seed < 0:
        seed = random.randint(0, 2147483647)

    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": CHECKPOINT}
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": POSITIVE_PROMPT,
                "clip": ["1", 1]
            }
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": NEGATIVE_PROMPT,
                "clip": ["1", 1]
            }
        },
        "4": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            }
        },
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": 28,
                "cfg": 7.5,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": 1.0,
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0]
            }
        },
        "6": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["5", 0],
                "vae": ["1", 2]
            }
        },
        "7": {
            "class_type": "SaveImage",
            "inputs": {
                "images": ["6", 0],
                "filename_prefix": f"m4ix-cover-{date.today()}"
            }
        }
    }


def queue_prompt(workflow: dict) -> str:
    """Queue workflow to ComfyUI and return prompt_id"""
    client_id = str(uuid.uuid4())
    payload = {"prompt": workflow, "client_id": client_id}

    try:
        response = requests.post(f"{COMFY_URL}/prompt", json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()
        prompt_id = result.get("prompt_id")
        if not prompt_id:
            raise ValueError(f"No prompt_id in response: {result}")
        return prompt_id
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to queue prompt: {e}")
        try:
            print(f"   Response: {response.text}")
        except:
            pass
        print("   Is ComfyUI running on http://127.0.0.1:8000?")
        raise


def wait_for_completion(prompt_id: str, timeout: int = 300) -> dict:
    """Poll ComfyUI until generation completes"""
    start_time = time.time()
    check_count = 0

    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{COMFY_URL}/history/{prompt_id}", timeout=10)
            history = response.json()

            if prompt_id in history:
                result = history[prompt_id]
                if result.get("outputs"):
                    return result
                # Debug: show what we got
                if check_count == 0:
                    print(f"   Got history response (waiting for outputs)...")
                    print(f"   Keys in result: {list(result.keys())}")
                    print(f"   Status keys: {result.get('status', {})}")
            else:
                if check_count == 0:
                    print(f"   Prompt ID not in history yet...")

            check_count += 1
            elapsed = int(time.time() - start_time)
            if check_count % 10 == 0:  # Print every 20 seconds
                print(f"⏳ Generating... ({elapsed}s)")
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Poll error: {e}, retrying...")
            time.sleep(3)

    raise TimeoutError(f"Generation timed out after {timeout}s")


def download_image(filename: str, subfolder: str = "") -> str:
    """Download generated image from ComfyUI"""
    params = {"filename": filename, "subfolder": subfolder, "type": "output"}
    url = f"{COMFY_URL}/view"

    try:
        print(f"📥 Downloading {filename}...")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        # Save to Windows Dropbox folder
        os.makedirs(FINAL_OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(FINAL_OUTPUT_DIR, filename)
        with open(output_path, "wb") as f:
            f.write(response.content)

        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"✅ Saved: {output_path} ({file_size_mb:.1f} MB)")
        return output_path
    except requests.exceptions.RequestException as e:
        print(f"❌ Download failed: {e}")
        raise


def generate_cover_art(seed: int = -1, width: int = 1000, height: int = 1000) -> str:
    """
    Main function: generate abstract cover art

    Args:
        seed: Random seed (-1 for random)
        width: Image width in pixels (default 1000)
        height: Image height in pixels (default 1000)

    Returns:
        Path to generated image
    """
    print(f"\n🎨 Generating M4IX cover art ({width}×{height})...")
    seed_display = seed if seed >= 0 else 'random'
    print(f"   Seed: {seed_display}")
    print(f"   Output: {FINAL_OUTPUT_DIR}")
    print()

    # Build and queue
    workflow = build_workflow(seed=seed, width=width, height=height)
    prompt_id = queue_prompt(workflow)
    print(f"✓ Queued: prompt_id={prompt_id}")

    # Wait for completion
    history = wait_for_completion(prompt_id)

    # Extract filename from output
    output_images = history.get("outputs", {}).get("7", {}).get("images", [])
    if not output_images:
        raise ValueError("No output images in history")

    image_info = output_images[0]
    filename = image_info["filename"]
    subfolder = image_info.get("subfolder", "")

    # Download
    output_path = download_image(filename, subfolder=subfolder)

    print(f"\n✨ Cover art ready: {output_path}\n")
    return output_path


if __name__ == "__main__":
    import sys

    # Optional: accept seed as command-line arg
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else -1

    try:
        output = generate_cover_art(seed=seed)
        print(f"Success! Image: {output}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Is ComfyUI running? (http://127.0.0.1:8188)")
        print("2. Check checkpoint name: CHECKPOINT = '{CHECKPOINT}'")
        print("3. Do you have SDXL model downloaded?")
        sys.exit(1)
