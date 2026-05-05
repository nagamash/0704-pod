# M4IX Project — CLAUDE.md

*Source of truth for the M4IX daily AI briefing system and all associated tooling.*
*Last updated: 2026-04-21*

---

## Identity Documents

Before doing anything else, read these files from the m4ix_001 folder:

- `../m4ix_001/soul.md` — who m4ix is. Voice, character, principles, specimens. This is the foundational document.
- `../m4ix_001/machine.md` — system configuration template and processing chain reference.

Then read from this folder:

- `dispatch-craft.md` — how the briefing gets built. Briefing form, story taxonomy, signal observation, source weighting, script constraints.
- `memory.md` — cumulative story log for deduplication.

---

## What This Is

M4IX is a private daily AI intelligence briefing, delivered each morning as a voiced MP3 to `C:\Users\Remote\Dropbox\Pod\briefings\`. A scheduled Claude task runs at 07:04 every day, collects the day's top AI/tech news from structured feeds (no Reddit scraping), writes a 3-4 minute script in M4IX's voice, generates audio via ElevenLabs TTS, bookends it with a jingle, creates a follow-up email draft with source links, and updates a running memory log for deduplication.

There is also a ComfyUI image generation layer that creates tiled cover art for each episode — either abstract glitch art or semi-realistic scene tiles — sized proportionally to how much airtime each story gets in the script.

---

## Directory Layout

```
C:\Users\Remote\Dropbox\Pod\          ← primary working folder
    CLAUDE.md                          ← this file (source of truth)
    memory.md                          ← cumulative story log, used for deduplication
    dispatch-craft.md                  ← editorial guide: story taxonomy, signal observation, source weighting
    m4ix-jingle.wav                    ← M4IX intro/outro jingle (source file, do not delete)

    M4IX-Identity/                     ← visual identity system
        M4IX-Visual-Identity.md        ← design spec (source of truth for covers)
        M4IX-Identity-Board.png
        M4IX-Gallery-Preview.png
        covers/
        generate_cover.py

    briefings/                         ← all daily briefing outputs
        ai-briefing-YYYY-MM-DD.md      ← daily script logs (stories + full script text)
        ai-briefing-YYYY-MM-DD.mp3     ← final voiced briefings (jingle + voice + jingle)

    cover-art/                         ← all cover art scripts and outputs
        gen_0704.py                    ← static ASCII art cover generator (3000×3000, Menlo font, wave field)
        animate_0704.py                ← brightness-modulation animation of static PNG → MP4
        animate_0704_live.py           ← full live-render: numpy atlas + per-cell cycling + ffmpeg pipe
        cover_poc.py                   ← SDXL tiled cover art (proof of concept, hardcoded stories)
        cover_flux.py                  ← Flux 2 abstract tiled cover art (auto-parses script)
        cover_flux_real.py             ← Flux 2 realist tiled cover art (auto-parses script)
        gen_cover_art.py               ← SDXL single-image cover generator
        m4ix-cover-workflow.json       ← ComfyUI workflow JSON (reference)
        0704-cover.png                 ← green-on-black ASCII "0704" cover (PIL-generated)
        0704_podcast_art.png           ← Max's static wave-field cover (gen_0704.py output)
        0704_podcast_art_v2.png        ← updated static cover
        0704_animated.mp4              ← live-rendered animation (animate_0704_live.py)
        0704_podcast_art.mp4           ← brightness-modulation animation (animate_0704.py)
        m4ix-ascii-cover-YYYY-MM-DD.png ← ASCII art covers (PIL-generated, typographic)
        m4ix-cover-flux-YYYY-MM-DD.png  ← abstract Flux covers
        m4ix-cover-real-YYYY-MM-DD.png  ← realist Flux covers
        m4ix-cover-poc.png             ← last SDXL POC cover

    jingles/                           ← 0704 podcast jingle experiments
        0704-jingle-transmission.mp3   ← ElevenLabs sound gen, transmission aesthetic
        0704-jingle-broadcast.mp3      ← ElevenLabs sound gen, broadcast aesthetic
        0704-jingle-ambient.mp3        ← ElevenLabs sound gen, ambient aesthetic

    scratch/                           ← experiments, test outputs, intermediates
        test_flux.py                   ← minimal Flux 2 sanity-check
        test_step2.py                  ← minimal SDXL sanity-check
        test_flux2_00001_.png          ← Flux test output
        test_step2_00001_.png          ← SDXL test output
        ai-briefing-YYYY-MM-DD-voice.mp3      ← intermediate voice files (auto-deleted on success)
        ai-briefing-YYYY-MM-DD-voice-proc.mp3 ← processed voice before jingle mix
        experiments diary/             ← development notes

C:\Users\Remote\Comfyui\              ← ComfyUI user-data folder
    models/
        unet/
            flux2_dev_fp8mixed.safetensors
        text_encoders/
            mistral_3_small_flux2_bf16.safetensors
        vae/
            full_encoder_small_decoder.safetensors
        checkpoints/
            sd_xl_base_1.0.safetensors
            sd_xl_refiner_1.0.safetensors
    custom_nodes/
    input/
    output/
    test_flux.py                       ← copy of the sanity-check script
    gen_cover_art.py                   ← copy of the SDXL cover generator
```

---

## Scheduled Task — Daily Briefing

**Task ID:** `daily-ai-briefing`
**Schedule:** 07:04 every day (local time)
**Managed via:** Claude Cowork scheduled tasks

The task executes the SKILL.md prompt autonomously. Steps in order:

1. **Mount Dropbox Pod** — `request_cowork_directory` on `C:\Users\Remote\Dropbox\Pod`
2. **Dedup check** — reads `memory.md` + last 2 `ai-briefing-*.md` files, builds a "recently covered" list
3. **Gather content** from all sources (see Sources below)
4. **Write script** as M4IX (450–600 words, 3–4 min spoken). The script must end with exactly one sign-off: "M4IX, signing off." Do not add a second sign-off after generating the script. The LLM writes the sign-off as the final line; do not append it again programmatically.
5. **Generate voice** via ElevenLabs API → `briefings/ai-briefing-YYYY-MM-DD-voice.mp3`
6. **Combine with jingle** via ffmpeg filter_complex concat → `briefings/ai-briefing-YYYY-MM-DD.mp3` (voice file deleted)
7. **Generate cover art** — run `python3 cover-art/gen_daily_cover.py YYYY-MM-DD` from the Pod directory. Output lands at `briefings/0704-cover-YYYY-MM-DD.png`. If the script fails, log the error and continue — a missing cover does not block the episode.
8. **Create email draft** in Gmail to `hej@maxblomqvist.se` with formatted story links
9. **Update `memory.md`** — append today's stories
10. **Save script log** as `briefings/ai-briefing-YYYY-MM-DD.md`
11. **Regenerate RSS feed** — run `python3 gen_rss.py` from the Pod directory. This updates `feed.xml` with the new episode. If it fails, log and continue.
12. **Upload to web** — run `python3 upload_episode.py YYYY-MM-DD` from the Pod directory. Uploads the MP3, cover PNG, and `feed.xml` to `maxblomqvist.se/pod/` via SFTP. SFTP credentials are in `.env`. If it fails, log and continue — the episode still exists locally.
13. **Report** summary back

### ElevenLabs

- **API key:** load from `ELEVENLABS_API_KEY` env var. The value lives in `.env` at the project root (gitignored). Read it with the Read tool at task start, then pass the value into the ElevenLabs request. Never echo the key into logs or output. Template at `.env.example`.
- **Voice ID:** `3SJPwamOw23fH1vBsn6i` (M4IX — Max's own voice clone)
- **Model:** `eleven_multilingual_v2`
- **Settings:** stability 0.5, similarity_boost 0.75, style 0.1, speed 1.1, speaker_boost true

**Pacing notes:** `style 0.1` keeps delivery even — the default 0.3 causes the TTS to linger dramatically on dense sentences. `speed 1.1` trims dead air without sounding rushed. Do not raise style above 0.15 for M4IX — it destabilises pacing. Do not exceed speed 1.2 — speech clips. The ffmpeg `loudnorm` chain compensates for any speed-induced level shift.

### Voice Post-Processing (ffmpeg)

After ElevenLabs generates the raw voice MP3, apply this processing chain before mixing with the jingle. It handles two things: (1) normalises loudness so the voice sits above the jingle, (2) adds subtle robotic/digital character to fit the M4IX AI butler persona.

```bash
VOICE_RAW="$POD_DIR/briefings/ai-briefing-$TODAY-voice.mp3"
VOICE_PROC="$POD_DIR/briefings/ai-briefing-$TODAY-voice-proc.mp3"

ffmpeg -y -i "$VOICE_RAW" \
  -af "highpass=f=180,\
       equalizer=f=2800:t=h:width=2000:g=3,\
       acrusher=bits=14:mode=log:aa=1,\
       flanger=delay=2:depth=1.5:speed=0.8:width=50:phase=90,\
       loudnorm=I=-14:TP=-1.5:LRA=9" \
  -codec:a libmp3lame -q:a 2 "$VOICE_PROC" 2>&1 | tail -3
rm -f "$VOICE_RAW"
```

**Chain breakdown:**
- `highpass=f=180` — removes low-end warmth below 180 Hz; makes the voice sound less "fleshy", more digital
- `equalizer=f=2800:t=h:width=2000:g=3` — +3 dB presence boost centred at 2.8 kHz; adds clarity and "cuts through"
- `acrusher=bits=14:mode=log:aa=1` — reduces bit depth by 2 bits (barely audible on its own, but adds a subtle digital texture under the voice)
- `flanger=delay=2:depth=1.5:speed=0.8:width=50:phase=90` — slow metallic shimmer; adds the processed, synthetic quality
- `loudnorm=I=-14:TP=-1.5:LRA=9` — EBU R128 normalisation to −14 LUFS; ensures voice is consistently louder than the jingle regardless of how ElevenLabs renders it

**Tuning notes:**
- To increase robotic character: raise `acrusher bits` to 12, increase `flanger depth` to 3
- To reduce robotic character: remove `acrusher` and/or lower `flanger depth` to 0.5
- To make voice louder relative to jingle: lower `loudnorm I` to −12

### Jingle Combine (ffmpeg)

Uses `filter_complex` concat (NOT the concat demuxer — that cuts the jingle at ~1s due to format mismatch). The filter normalises all streams to 44100 Hz stereo s16 inline, splits the jingle for the bookend, and encodes the final MP3 at libmp3lame q:a 2.

The jingle is reduced to `volume=0.65` so the normalised voice sits clearly above it.

Structure: `jingle (65% vol) → 0.5s silence → processed voice (−14 LUFS) → 0.5s silence → jingle (65% vol)`

---

## Content Sources

All sources use API/RSS/JSON endpoints. No browser scraping. No Reddit HTML.

| Source | Method | Notes |
|---|---|---|
| **Hacker News** | Firebase API `v0/topstories.json` + per-item fetch | Top 30, AI keyword filter, sorted by score. Run via Python in a single Bash call. |
| **arXiv** | Atom feed `export.arxiv.org/api/query` | cs.AI + cs.LG + cs.CL, last 25. High bar — only include if genuinely novel. |
| **Anthropic news** | WebFetch `anthropic.com/news` | First-party = auto high priority |
| **OpenAI news** | WebFetch `openai.com/news` | |
| **Google DeepMind blog** | WebFetch `deepmind.google/discover/blog` | |
| **Meta AI blog** | WebFetch `ai.meta.com/blog` | |
| **404 Media** | RSS `404media.co/rss/` | AI, surveillance, platform policy |
| **r/LocalLLaMA** | JSON `reddit.com/r/LocalLLaMA/top.json?t=day&limit=15` | Practitioner pulse — open models, tooling |
| **r/singularity** | JSON `reddit.com/r/singularity/top.json?t=day&limit=15` | Community reaction to frontier news |
| **Import AI** | RSS `jack-clark.net/feed/` | Weekly, human-curated |
| **The Batch** | WebFetch `deeplearning.ai/the-batch` | Weekly |
| **Ben's Bites** | WebFetch `bensbites.com` | Daily-ish |
| **One Useful Thing** | WebFetch `oneusefulthing.org` | Ethan Mollick. Include if new post in 48h. |
| **Fireship** | YouTube RSS `channel_id=UCsBjURrPoezykLs9EqgamOA` | |
| **Computerphile** | YouTube RSS `channel_id=UC9-y-6csu5WGm29I7JiwpnA` | |
| **ComfyUI** | YouTube RSS `channel_id=UCsOXR1n2MR15vuK2htE5EkQ` | |
| **Nate Jones** | YouTube RSS `channel_id=UC0C-17n9iuUQPylguM1d-lQ` | |
| **Peter Yang** | YouTube RSS `channel_id=UCnpBg7yqNauHtlNSpOl5-cg` | |
| **Possible (Reid Hoffman)** | Spotifeed RSS | |
| **Pivot** | Spotifeed RSS | |
| **Hard Fork** | Spotifeed RSS | |

Reddit requests use `User-Agent: m4ix-briefing/1.0`. If Reddit returns 429, skip silently.

**Removed:** 16-subreddit HTML scraping via browser automation (unreliable, low signal).

---

## M4IX Character

M4IX is Max's AI butler. Voice rules:

- Addresses Max as "Sir" always
- Warm, articulate, composed — a well-read British butler who knows AI deeply
- Subtle dry wit, occasional understated observations
- Never sycophantic, never over-the-top, never loud
- Does not mention Reddit, upvotes, or subreddit names on-air — uses "practitioners are discussing..." or "there's notable interest in..."
- Does not read URLs
- Script written for the ear: short sentences, clear rhythm, no padding
- **No em dashes in script text** — ElevenLabs treats `—` as a long pause. Use a comma, a period, or restructure the sentence. Em dashes in section separators (`---`) are fine since they are not read aloud.
- **Break long sentences** — any sentence over ~25 words should be split. Dense compound sentences cause the TTS to slow down and "perform" the complexity.

---

## ComfyUI Setup

**Port:** `8000` (not the default 8188 — always use `http://127.0.0.1:8000`)
**User data folder:** `C:\Users\Remote\Comfyui`

### Flux 2 Dev Model Stack

| Role | File | Location |
|---|---|---|
| UNET | `flux2_dev_fp8mixed.safetensors` | `models/unet/` |
| Text encoder | `mistral_3_small_flux2_bf16.safetensors` | `models/text_encoders/` |
| VAE | `full_encoder_small_decoder.safetensors` | `models/vae/` |

### Flux 2 Workflow Nodes

```
UNETLoader (weight_dtype: fp8_e4m3fn)
CLIPLoader (type: "flux2")          ← NOT "mistral" — that's not a valid enum value
VAELoader
EmptySD3LatentImage                 ← 16-channel latent, NOT EmptyLatentImage
KSampler (cfg: 1.0, scheduler: simple, sampler: euler)
VAEDecode
SaveImage
```

Critical settings:
- `CLIPLoader type` must be `"flux2"` — using `"mistral"` throws a validation error
- `cfg` must stay at `1.0` — Flux Dev degrades noticeably above ~1.5
- Use `EmptySD3LatentImage` not `EmptyLatentImage` (wrong channel count)
- Tile dimensions must be multiples of 16

### SDXL Stack

- Checkpoint: `sd_xl_base_1.0.safetensors` (+ refiner available)
- Node: `CheckpointLoaderSimple`
- Latent: `EmptyLatentImage` (multiples of 64)
- CFG: 7–7.5, sampler: dpmpp_2m, scheduler: karras, steps: 15–28

### Running a Script

```powershell
# From anywhere on the host
python C:\Users\Remote\Dropbox\Pod\test_flux.py
python C:\Users\Remote\Dropbox\Pod\cover_flux.py
python C:\Users\Remote\Dropbox\Pod\cover_flux.py 2026-04-15
python C:\Users\Remote\Dropbox\Pod\cover_flux_real.py
```

ComfyUI must be running before any script is executed.

---

## Cover Art Scripts

Three generations of the cover art idea:

### `cover_poc.py` — SDXL, hardcoded stories
Proof of concept. Squarified treemap, 4 hardcoded stories, SDXL tiles, chromatic aberration stitch. Use for reference only — superseded by the auto-parsing Flux versions.

### `cover_flux.py` — Flux 2, abstract aesthetic
Auto-parses `ai-briefing-YYYY-MM-DD.md`, splits Full Script into paragraphs (dropping greeting + sign-off), sizes tiles by word count. Prompts are emotional color palettes per story topic. Chromatic aberration applied to the composite. Canvas: 1536×1536, steps: 18.

**Emotion tagger:** keyword match → color palette. E.g. Anthropic/Claude → electric blue; Nvidia/GPU → red heat; erosion/job stories → amber rust. First match wins, falls back to generic glitch palette.

### `cover_flux_real.py` — Flux 2, realist/cinematic
Same treemap structure. Prompts are physical scene descriptions rather than palettes:
1. Scene anchor from a topic keyword map (e.g. Nvidia GPU story → "extreme macro close-up of a GPU die, circuit traces glowing orange-red")
2. First 1–2 sentences of the story paragraph, after stripping M4IX butler phrasing ("Sir", "I would note", "shall we say", etc.)
3. Realism suffix: "photorealistic, editorial photography, cinematic still frame, sharp focus, dramatic studio lighting, 4K"

No chromatic aberration (undermines realism). Thin dark borders between tiles. Canvas: 1536×1536, steps: 28 (more detail needed than abstract).

### Shared infrastructure (all three scripts)
- `squarify()` — greedy squarified treemap layout
- `parse_script()` — reads `## Full Script` section from `.md` log, splits on blank lines, drops first (greeting) and last (sign-off) paragraphs
- ComfyUI poll loop — 2s interval, 600s timeout
- Tile dimension snapping — multiples of 16 (Flux) or 64 (SDXL), minimum 128px

---

## Visual Identity (Typographic Covers)

Separate from the ComfyUI image generation. The M4IX cover is designed as a typographic document, not a generated image. Full spec in `M4IX-Identity/M4IX-Visual-Identity.md`.

**Color palette:**
- Ink `#0C0C0E` — primary text
- Paper `#F3EDE2` — background (warm ivory, not pure white)
- Signal Cyan `#00B8C4` — single accent, one element per cover only
- Graphite `#55555B` — metadata, secondary text

**Typography:**
- Headlines: Playfair Display Bold, ALL CAPS, tight tracking (−20 to −40)
- Labels/metadata: IBM Plex Sans Medium, UPPERCASE, loose tracking (+160)
- Serials/timestamps/codes: IBM Plex Mono always

**Headline rule:** compress lead story to 2–5 words maximum, period-terminated, editorial not neutral. E.g. "JAPAN BUILDS WALLS." not "Japan AI Alliance Formed."

**Signal Cyan:** one use per cover, as a transmission mark (underline, rule, bracket). Never two.

**Canvas:** 3000×3000px for final output.

---

## Known Gotchas

- **ComfyUI port is 8000**, not the default 8188. Scripts already have this; don't change it.
- **`CLIPLoader type: "flux2"`** — `"mistral"` is not in the enum, causes 400 validation error.
- **Jingle cut-off** — solved by using ffmpeg `filter_complex` concat, not the concat demuxer. Do not revert to the demuxer approach.
- **Reddit 429s** — normal. Script skips silently. Don't add retry loops; just accept the miss.
- **arXiv over-inclusion** — easy to pad with papers. Only include if something is genuinely novel (not the 40th RAG variant).
- **Small tiles** — the squarify algorithm can produce very thin tiles for short stories. Both Flux cover scripts skip tiles smaller than 128px rather than generating broken tiny latents.
- **ElevenLabs payload file** — script writes `el_payload.json` to the parent of the output dir (one level up from Pod). This is intentional to avoid cluttering Pod.
- **Voice-only file cleanup** — the `-voice.mp3` intermediate is deleted after the jingle combine. If it persists (permissions error), it can be deleted manually.
- **Duplicate sign-off** — the LLM writes "M4IX, signing off." as the final line of the script. Do not append it again. If the audio ends with two sign-offs, the script generation and the task scaffolding both wrote it. The `render_to_audio` function in m4ix-system deduplicates as a last resort, but fix it at the source.

---

## Planned / Not Yet Built

From the experiments diary:
- Wire cover art generation into the daily scheduled task
- Auto-scale cover canvas to 3000×3000
- Add a fallback when ComfyUI isn't running (skip cover, continue briefing)
- Typographic cover generator using the `M4IX-Visual-Identity.md` spec (Playfair + IBM Plex, pure typography, no image generation)
- Animated waveform / motion variant for social (Signal Cyan pulse only)

---

*This document is the source of truth. When in doubt, read this before experimenting.*
