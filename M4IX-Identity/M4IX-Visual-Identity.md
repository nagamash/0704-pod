# M4IX — Visual Identity System

*A private intelligence dispatch. Composed daily for Sir.*

---

## The Strategic Premise

M4IX is not a podcast. It is **a daily dispatch** — a personal briefing composed by an AI butler for a single reader. The visual identity has to carry that double meaning: the ceremony of old-world service *and* the precision of a modern intelligence system.

Everything flows from one tension:

> A 1947 ministry memo rewritten by a 2026 machine.

If a visual choice leans too far into "butler" (monocles, bowties, serif filigree), it becomes a costume. If it leans too far into "AI" (gradients, glows, chrome), it becomes indistinguishable from every other podcast in the category. The identity lives in the disciplined middle — austere, archival, editorial, computational.

---

## Design Principles

**1. Restraint is the voice.** M4IX speaks measuredly, never decoratively. The design must do the same. If an element isn't carrying information, remove it.

**2. Every cover is a document.** Each episode is treated as a serialized dispatch — stamped, dated, numbered. The viewer should feel they are intercepting a piece of private correspondence.

**3. Typography is the image.** No illustrations. No photography. No generated imagery. The lead story's headline *is* the cover. The typographic system carries all the weight.

**4. A gallery, not a logo.** Scrolling through covers across weeks should form a readable history of the AI era as M4IX observed it. Consistency at a distance, specificity up close.

**5. The friction is the feature.** Classical serif ↔ monospaced data. Warm paper ↔ cold signal cyan. Ceremonial composition ↔ clinical metadata. Do not resolve the friction — display it.

---

## Color System

Four values. No more.

| Token | Hex | Role | Usage |
|---|---|---|---|
| **Ink** | `#0C0C0E` | Primary typography, rules | 70–80% of pigment |
| **Paper** | `#F3EDE2` | Base surface, aged ivory | Full background |
| **Signal Cyan** | `#00B8C4` | Single accent, the "live" mark | ≤5% of the composition |
| **Graphite** | `#55555B` | Metadata, secondary text | Dates, episode numbers |

### Rules

- **Paper is the ground; Ink is the voice.** Never invert (no ink backgrounds). The dispatch is printed, not projected.
- **Signal Cyan appears only as a "transmission mark"** — a single underline, dot, bracket, or serial indicator. It is the electronic pulse inside the paper document. One cyan element per cover. Never two.
- **No gradients. No shadows. No glows.** The system is flat. Depth comes from typographic scale, not atmospheric effects.
- Paper is warm on purpose. Pure white (`#FFFFFF`) would read as digital; the ivory reads as archival.

---

## Typography System

Two families. Three voices.

### Primary — **Playfair Display**
A contemporary Didone. High contrast between thick and thin strokes. Ceremonial. Literary. The voice of the dispatch itself.

- **Display headline**: Bold, 280–380pt on a 3000px cover
- **Wordmark "M4IX"**: Bold, set tightly
- **Body inscriptions**: Italic, used sparingly for flourishes only

### Secondary — **IBM Plex Sans**
A precise geometric sans with humanist detail. The editorial infrastructure.

- **Section labels**: Medium, UPPERCASE, tracked +160
- **Episode metadata**: Regular, small caps where available
- **Never use for headlines.** It is supporting scaffolding, not voice.

### Monospace — **IBM Plex Mono**
The computational counterpoint. All technical annotations — dates, episode serials, transmission codes, classification stamps.

- **Serial numbers**: Regular, tracked +80
- **Timestamps, hashes, identifiers**: Always monospace. Always.

### Hierarchy Rules

1. On any cover, the viewer's eye should land in this exact sequence: **wordmark → headline → date → classification**. Anything that disrupts this order is wrong.
2. Headlines are always **ALL CAPS** set in Playfair. The tension between Didone elegance and shouting caps is the entire point.
3. Tracking: tight on headlines (−20 to −40), loose on metadata (+100 to +200).

---

## The Wordmark — M4IX

The name is the mark. Do not design around it; let it *be* the logo.

### Construction

- Set in **Playfair Display Bold**
- Characters: `M`, `4`, `I`, `X`
- Tracking: −40
- The `4` is the pivot. It is a numeral among letters, exactly as M4IX is a machine among humans. Do not stylize it further. The friction is already there.

### Placement on covers

- Always top-left or top-center
- Always in Ink
- Never smaller than 4% of the canvas width
- Never accompanied by a tagline, ever. The dispatch speaks for itself.

### Monogram variant

For very small contexts (favicon, 16×16 podcast app icon, social avatars), use the single character **`M`** in Playfair, centered in a square, with a Signal Cyan serial bar underneath.

---

## Episode Cover System

Each cover follows the same ritualized structure. Only three things change per episode:

1. The headline (the day's lead story, compressed to 2–5 words)
2. The date
3. The episode number / serial

Everything else is invariant.

### Canvas

- 3000 × 3000 px (Spotify / Apple Podcasts requirement)
- Exported as high-quality JPEG (≤500 KB) and PNG

### Grid

- 12-column grid with 120px outer margins
- Vertical rhythm: 60px baseline
- Primary content area sits within a 1px Ink rule border inset 80px from edges (the "document frame")

### Zones

```
┌─────────────────────────────────────────────┐
│  ┌───────────────────────────────────────┐  │  ← 80px inset rule
│  │  M4IX          No. 024 · 2026-04-13   │  │
│  │  ─────────────────────────────────    │  │  ← Signal Cyan rule
│  │                                        │  │
│  │                                        │  │
│  │      JAPAN                             │  │  ← Headline
│  │      BUILDS                            │  │     (Playfair Bold
│  │      WALLS.                            │  │      ALL CAPS)
│  │                                        │  │
│  │                                        │  │
│  │  ─────────────────────────────────    │  │
│  │  DAILY DISPATCH · MORNING BRIEFING    │  │
│  │  CLASSIFIED — FOR MAX BLOMQVIST ONLY  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### The Headline Distillation Rule

Every day's cover must compress the lead story to **2–5 words maximum**, treated as a period-terminated declaration. Examples:

- Japan forms sovereign AI alliance → **"JAPAN BUILDS WALLS."**
- Anthropic Mythos/Glasswing cybersecurity story → **"TOO SHARP TO SHIP."**
- GLM-5.1 open-source beats closed → **"OPEN WINS A ROUND."**
- Apple Smart Glasses four designs → **"NO SCREEN. STILL SEEING."**

The headline is an editorial judgment, not a summary. It should contain opinion, compression, and wit. If it reads as neutral reportage, rewrite it.

### What never appears on a cover

- Photography or illustration of any kind
- The word "podcast"
- Season or episode numbers styled as "Ep. 24"
- Multiple colors beyond the defined palette
- Decorative rules, dingbats, or ornaments
- Anthropic logos, OpenAI logos, or third-party trademarks

---

## Voice-to-Visual Alignment

M4IX speaks as a measured, dry, slightly wry butler. The visual language must match:

| M4IX says | M4IX looks |
|---|---|
| "Shall we?" | A single serial rule separating zones |
| "Rather eventful." | All-caps Didone headline with a full stop |
| "One imagines." | Italic flourish used exactly once per cover |
| "M4IX, signing off." | A monospaced classification line at the base |

Never jolly. Never loud. Never ornamented. The visual analogue of a butler's raised eyebrow.

---

## Extensions

### Transcript PDF / email header
Same frame, same palette, same typography. Headline sits at top; body text in IBM Plex Sans Regular, 11pt, leading 16pt, max 66 characters per line.

### Waveform / motion (future)
If an animated version is needed (social clips), the only motion permitted is the Signal Cyan rule pulsing subtly, like a transmission indicator. No bouncing waveforms. No typography animation.

### Social share cards
Square or 16:9. Same grid rules. Headline may shrink; classification line must remain legible.

---

## Do / Don't

**Do:**
- Let white space do the work.
- Treat every cover like a legal document. Serious by default.
- Compress the headline until it hurts. Then cut one more word.
- Keep the Signal Cyan rare and load-bearing.

**Don't:**
- Add imagery because the cover "feels empty." Empty is the point.
- Introduce a second accent color. Ever.
- Write the headline as a question. M4IX does not ask; M4IX observes.
- Use Playfair Italic for more than one element per cover.

---

*Version 1.0 — 2026-04-13*
*This document is the source of truth. When in doubt, consult the principles before improvising.*
