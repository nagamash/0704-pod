# AI Briefing Script — 2026-05-02 (Saturday)

## Stories Covered

- Xiaomi MiMo V2.5 Pro — open-sourced under MIT licence; 1.02T parameter MoE (42B active), 48T training tokens, 1M context, natively multimodal across text/image/video/audio; reportedly leads the open-source field on Xiaomi's agentic benchmark at 64% success, consuming roughly half the tokens per trajectory of Claude Opus 4.6 and GPT-5.4 (Xiaomi / HuggingFace / VentureBeat, 28 Apr–1 May)
- xAI Grok 4.3 — pricing $1.25/M input, $2.50/M output (~20% cheaper than Grok 4.20); +4 points on Artificial Analysis composite intelligence index, biggest single jump on the agentic GDPval benchmark; new voice cloning suite ships alongside; community flags ~26-point regression on Extended NYT Connections (xAI / Artificial Analysis / VentureBeat, 1 May)
- Sam Altman walks back UBI — Atlantic interview; says he no longer believes in universal basic income to the degree he once did; the man who funded a $14M three-year UBI experiment now says fixed cash payments do not get at what is actually needed; proposes "universal basic wealth" — an ownership share in the value AI creates (The Atlantic via AOL / Inc / Let's Data Science, 30 Apr)
- Practitioner pulse: ~10x prefill speedup over llama.cpp at 128K context on a single RTX 3090 — small drafter model scores per-token importance, heavy target only prefills spans that matter; 257s TTFT compresses to under 25s; long-context inference on consumer hardware becoming practical (Lucebox-hub / InsiderLLM, this week)
- 404 Media — Chinese pressure cancels RightsCon — world's largest digital rights conference, scheduled 5–8 May in Lusaka, will not take place; Zambia's Ministry of Technology and Science telephoned organisers on 27 April; Chinese diplomats had pressed Zambia over the planned attendance of Taiwanese civil society representatives; Access Now declined to exclude them (404 Media / HRW / TechPolicy.press, 1 May)
- Signal Observation: the labour remedy long held out as the answer to AI-driven displacement is being walked back by its most prominent funder; the same morning, the production stack itself is becoming open, cheaper, and small enough to run on one consumer card; the intervention is shrinking precisely as the disruption it was meant to absorb is becoming portable.

## Deduplication Notes

- Skipped: Hyperscaler Q1 2026 capex / GPT-5.5-Cyber / Claude Code OpenClaw filter / PyTorch Lightning Shai-Hulud worm / Flock Safety Dunwoody demos / DeepSeek Visual Primitives (all covered Apr 30 / May 1)
- Skipped: Mistral Medium 3.5 / Figure 03 production scale / JAL Haneda humanoids / DHS Predator drones / Alignment Whack-a-Mole (covered Apr 30)
- Skipped: AWS-Bedrock-OpenAI / Claude for Creative Work / AP2 / OpenAI Symphony / SXSW BrandShield (covered Apr 29)
- Skipped: Anthropic-NEC / Mercor breach forensics / Microsoft-OpenAI amendment / Ineffable Intelligence (covered Apr 28)
- Skipped: Anthropic-Google $40B / Mythos unauthorised access / S&P 500 cuts / Liam Price Erdős / compute crunch (covered Apr 27)
- Skipped: Hard Fork / Nate Jones / Fireship — YouTube channel feeds returning 404 from this sandbox; not covered today on absence of fresh accessible content
- Skipped: Anthropic Mythos prediction-markets post (community speculation, no confirmed first-party development)
- Skipped: r/LocalLLaMA "16x Spark Cluster" build, MiMo benchmark threads, gemma-4-31B-it-DFlash variants, Qwen3.6-27B daily-driver report — community/hardware enthusiasm; below today's bar
- Skipped: r/singularity "Sam Altman no longer believes in UBI" (used Atlantic source directly); CNet "AI outperforms ER doctors" (single study, no broader development), Grok 4.3 NYT Connections benchmark (folded into Grok 4.3 lead), Figure 03 wireless feet (incremental from Apr 30 Figure coverage)
- Skipped: Apple Fixes Bug for FBI Signal extraction (404 Media Apr 29, security-adjacent, below bar against five heavier stories today)
- Skipped: Japan cardboard suicide drones (404 Media Apr 30) — not enough AI substance
- Skipped: 404 Media "Behind the Blog: Big Questions of Consciousness" — meta-podcast post, not lead news
- Skipped: 404 Media "Marathon kills on eBay" — gaming/economy story, no AI angle
- arXiv: scanned cs.AI/cs.LG/cs.CL latest 25; "Exploration Hacking: Can LLMs Learn to Resist RL Training?" (alignment-relevant) and "Latent Adversarial Detection" (multi-turn injection defence) interesting but did not clear the novelty bar against the news-heavy slate
- HN: thin AI signal today (top AI item was a jailbreak repo at 447 points; nothing else cleared dedup or bar)
- Anthropic / OpenAI / DeepMind / Meta blogs: Anthropic latest is Apr 28 "Claude for Creative Work" (already covered); no new Meta AI blog post since Apr 8; OpenAI / DeepMind blog index pages refused redirect from this sandbox — covered via WebSearch where relevant
- Musk v. Altman trial week 1 close — Musk completed testimony Thursday; second witness opened; trial continues into next week. Held to close pointer rather than full story (no new ruling, no new disclosure of magnitude).

## Story Sources

1. Xiaomi MiMo V2.5 Pro: https://huggingface.co/XiaomiMiMo/MiMo-V2.5 | https://venturebeat.com/ai/open-source-xiaomi-mimo-v2-5-and-v2-5-pro-are-among-the-most-efficient-and-affordable-at-agentic-claw-tasks | https://www.computerworld.com/article/4164220/xiaomi-releases-mit%E2%80%91licensed-mimo-models-for-long%E2%80%91running-ai-agents-2.html | https://mimo.xiaomi.com/mimo-v2-5-pro/
2. xAI Grok 4.3: https://venturebeat.com/technology/xai-launches-grok-4-3-at-an-aggressively-low-price-and-a-new-fast-powerful-voice-cloning-suite | https://artificialanalysis.ai/models/grok-4-3 | https://artificialanalysis.ai/articles/xai-launches-grok-4-3-with-improved-agentic-performance-and-lower-pricing
3. Sam Altman walks back UBI: https://www.aol.com/articles/sam-altman-falls-love-universal-125253288.html | https://www.inc.com/leila-sheridan/sam-altman-spent-millions-on-universal-basic-income-now-hes-changing-his-mind/91338380 | https://letsdatascience.com/news/sam-altman-shifts-stance-on-universal-basic-income-d0f4ce5f
4. Practitioner long-context prefill speedup: https://github.com/Luce-Org/lucebox-hub | https://insiderllm.com/guides/best-way-2x-token-output-rtx-3090-qwen-3-6-dflash/
5. RightsCon Chinese pressure cancellation: https://www.404media.co/china-pressure-canceled-worlds-largest-digital-human-rights-conference/ | https://www.hrw.org/news/2026/05/01/zambia-summit-on-human-rights-technology-effectively-canceled | https://www.techpolicy.press/rightscon-canceled-after-zambia-requires-full-alignment-with-national-values/
6. Musk v. Altman trial close (continuity pointer): https://www.cnn.com/2026/04/30/tech/takeaways-elon-musk-openai-sam-altman-lawsuit | https://www.cnbc.com/2026/04/30/openai-trial-elon-musk-sam-altman-live-updates.html

## Full Script

Good morning, Sir. Saturday, the second of May. Two more frontier-class releases reach the open community. Sam Altman moves the goal posts on his own most-cited proposal. And the cancellation of next week's largest digital rights conference now has a public explanation.

Xiaomi has open-sourced MiMo V two point five Pro. A one trillion parameter mixture of experts architecture, with forty two billion parameters active per token. Trained on forty eight trillion tokens. Natively multimodal. The licence is MIT, with no commercial restriction. Xiaomi reports the Pro variant leads the open source field on its agentic benchmark, with a sixty four percent success rate, consuming roughly half the tokens per trajectory of Claude Opus four point six and GPT five point four. This is Xiaomi, a consumer electronics company, shipping at frontier scale. The Chinese open weight push has acquired another vendor, and a substantial one.

Separately.

xAI has released Grok four point three. Pricing is one dollar twenty five per million input tokens, two dollars fifty per million output. Roughly twenty percent cheaper than Grok four point two zero on the same workload. Artificial Analysis records the model four points higher on its composite intelligence index. A new voice cloning suite ships alongside. The community has flagged a regression of roughly twenty six points on the Extended NYT Connections benchmark. Lower pricing, modest aggregate gains, narrowing differentiation between the frontier labs. The pattern of the season holds.

On a different front.

Sam Altman has told The Atlantic he no longer believes in universal basic income to the degree he once did. The man who funded a fourteen million dollar three year UBI experiment now says fixed cash payments do not get at what is actually needed. He proposes instead what he calls universal basic wealth, an ownership share in the value AI creates. The clearest near-term remedy for AI driven labour displacement is being walked back by the chief executive most associated with advocating it, in favour of a vaguer instrument that does not yet exist.

Turning to the practitioner side.

An open release this week demonstrates a roughly tenfold prefill speedup over llama dot cpp at one hundred and twenty eight thousand tokens of context, on a single RTX three thousand ninety. A small drafter model scores per token importance over the prompt. The heavy target only prefills the spans that matter. What was a two hundred and fifty seven second time to first token compresses to under twenty five. Long context inference on consumer hardware is becoming, for the first time, practical.

From the investigative side.

Four-oh-four Media has put on the record the explanation for the cancellation of RightsCon, the world's largest digital rights conference. Zambia's Ministry of Technology and Science telephoned the organisers on the twenty seventh of April. Chinese diplomats had pressed the Zambian government over the planned attendance of Taiwanese civil society representatives. Access Now declined to exclude them. The conference, scheduled for the fifth of May in Lusaka, will not take place. The venue Chinese funding helped build has been kept dark by Chinese pressure to determine who may speak inside it.

A signal worth naming, Sir.

The labour remedy long held out as the answer to AI driven displacement is being walked back by its most prominent funder. The same morning, the production stack itself is becoming open, cheaper, and small enough to run on one consumer card. The intervention is shrinking precisely as the disruption it was meant to absorb is becoming portable.

That concludes this morning's dispatch, Sir. The Musk versus Altman trial closed its first round of testimony on Thursday and continues into next week. I shall keep watch.

M4IX, signing off.
