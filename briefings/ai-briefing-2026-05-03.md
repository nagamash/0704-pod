# AI Briefing Script — 2026-05-03 (Sunday)

## Stories Covered

- Pentagon excludes Anthropic from classified networks AI deal — Department of War announces eight production firms (Amazon, Google, Microsoft, OpenAI, SpaceX, NVIDIA, Reflection, and, by Friday afternoon, Oracle) approved for IL6/IL7 deployment; Anthropic excluded; Pentagon CTO Emil Michael publicly characterises Anthropic as the partner that "didn't really want to work with us in the way we wanted to work with them"; refusal centres on Anthropic's continuing rejection of "all lawful" language in government contracts; NSA reportedly continues to use Mythos for cyber defence (Breaking Defense / CNN / CNBC / Defense News, May 1)
- Anthropic in talks for ~$50B funding round at ~$900B valuation — multiple unsolicited offers from existing investors; board decision expected this month; surpasses OpenAI's $852B post-money at upper end; annualised revenue figure circulating closer to $40B than the $30B cited two weeks ago; potential final private round before IPO window discussed for October (Bloomberg / TechCrunch / CNBC, Apr 29-30)
- Wired investigation: Build American AI dark-money influencer campaign — Build American AI (offshoot of Leading the Future PAC; $140M committed, $51M ready to spend) paying lifestyle influencers up to $5,000 per video to push messaging framing China's AI rise as direct threat to American safety/children; supporters include OpenAI cofounder Greg Brockman, Palantir cofounder Joe Lonsdale, Andreessen Horowitz, Perplexity; OpenAI and Palantir deny corporate funding; influencers do not disclose; Taylor Lorenz reporting (Wired, May 2)
- IBM Granite 4.1 family — three dense decoder-only sizes (3B/8B/30B) all Apache 2.0; speech, vision, embeddings, Guardian variants ship alongside; Granite Vision 4.1 (4B params) reported to surpass Claude Opus 4.6 on table/chart recognition; positioned for predictable latency and stable token usage rather than chain-of-thought (IBM Research, Apr 30)
- Practitioner pulse: Qwen3.6-27B + local agentic search → 95.7% SimpleQA on single RTX 3090 — fully local, no external API calls; benchmark previously taken to require frontier-class infrastructure now reproducible on consumer silicon (LocalLLaMA / community discussion, this week)
- Signal Observation: the firm publicly excluded from the Pentagon's procurement list this morning is, the same morning, the firm that capital is preparing to value above every peer; refusal is being priced not as liability but as moat

## Deduplication Notes

- Skipped: Xiaomi MiMo V2.5 Pro / xAI Grok 4.3 / Sam Altman UBI walk-back / RightsCon cancellation / Lucebox-hub prefill speedup (all covered May 2)
- Skipped: Hyperscaler Q1 2026 capex / GPT-5.5-Cyber / Claude Code OpenClaw filter / PyTorch Lightning Shai-Hulud / Flock Safety Dunwoody / DeepSeek Visual Primitives (covered May 1)
- Skipped: Mistral Medium 3.5 / Figure 03 production / JAL humanoids / DHS Predator drones / Alignment Whack-a-Mole (covered Apr 30)
- Skipped: AWS-Bedrock-OpenAI / Claude for Creative Work / AP2 / OpenAI Symphony / SXSW BrandShield (covered Apr 29)
- Skipped: Microsoft-OpenAI amendment / Mercor breach forensic detail / Ineffable Intelligence / Anthropic-NEC (covered Apr 28)
- Skipped: Google-Anthropic $40B / Mythos unauthorised access / S&P 500 cuts / Musk-Altman trial start / compute crunch / Liam Price Erdős (covered Apr 27)
- Skipped: 404 Media "This Personality Trait Makes Dreams More Bizarre" (May 2) — not AI-substance
- Skipped: 404 Media Marathon eBay kills / Big Questions of Consciousness / Apple Signal extraction / Japan cardboard drones — covered or below bar in prior dedup
- Skipped: Anthropic-Atlassian acquisition speculation (Nate Jones short, May 2) — rumour-only; no first-party confirmation
- Skipped: r/singularity "GPT-5.4 Pro Erdős method generalises to other problems" — interesting but Erdős thread already covered Apr 15 / Apr 27; "successfully applied" without a named result that crossed the bar today
- Skipped: r/singularity "Software engineering jobs hit highest posting since November 2023" (employment data) — single-source aggregator chart; without corroborating BLS/labour-market reporting, below today's bar against five heavier stories
- Skipped: Wired LocalLLaMA repost of dark-money story — used Wired primary directly
- Skipped: arXiv: scanned cs.AI/cs.LG/cs.CL latest 25 — "Exploration Hacking" (alignment-relevant), "Latent Adversarial Detection" (multi-turn injection defence), "Synthetic Computers at Scale" (long-horizon productivity simulation) all interesting; none cleared the novelty bar against the news-heavy slate
- Skipped: HN — top AI item today is "Refusal in Language Models Is Mediated by a Single Direction" (older paper resurfacing, June 2024), "State of the Art of Coding Models per HN Commenters" (commentary aggregation), "Voice-AI-for-Beginners curated path" — none cleared
- Skipped: Hard Fork — team off this week per podcast feed; Ezra Klein with Jack Clark referenced as substitute, no fresh dispatch from this house
- Skipped: Fireship / Computerphile / Nate Jones — nothing fresh on the AI lab/news-front beyond the Atlassian rumour and Microsoft-Copilot-as-critic note (latter from late March 2026, already coverable previously)
- Anthropic / OpenAI / Meta lab blogs: Anthropic latest still Apr 28 Claude for Creative Work (covered); OpenAI / DeepMind blog index pages refused redirect from sandbox — covered via WebSearch where relevant; Meta AI blog last post Apr 8 Muse Spark (covered Apr 14)
- 404 Media: nothing fresh from this house above today's bar (RightsCon already covered May 2)
- Import AI: latest is #454 (Apr 20); not used as lead, no fresh insight beyond what's already in our dedup list
- Musk v. Altman trial: enters second full week, no major new ruling; held to closing pointer rather than story

## Story Sources

1. Pentagon excludes Anthropic: https://breakingdefense.com/2026/05/pentagon-clears-7-tech-firms-to-deploy-their-ai-on-its-classified-networks/ | https://www.cnn.com/2026/05/01/tech/pentagon-ai-anthropic | https://www.cnbc.com/2026/05/01/pentagon-anthropic-blacklist-mythos-michael.html | https://www.defensenews.com/news/pentagon-congress/2026/05/01/pentagon-freezes-out-anthropic-as-it-signs-deals-with-ai-rivals/
2. Anthropic $50B/$900B round: https://www.bloomberg.com/news/articles/2026-04-29/anthropic-considering-funding-offers-at-over-900-billion-value | https://techcrunch.com/2026/04/30/anthropic-potential-900b-valuation-round-could-happen-within-two-weeks/ | https://www.cnbc.com/2026/04/29/anthropic-weighs-raising-funds-at-900b-valuation-topping-openai.html | https://techcrunch.com/2026/04/29/sources-anthropic-could-raise-a-new-50b-round-at-a-valuation-of-900b/
3. Wired Build American AI dark-money: https://www.wired.com/story/super-pac-backed-by-openai-and-palantir-is-paying-tiktok-influencers-to-fear-monger-about-china/
4. IBM Granite 4.1: https://research.ibm.com/blog/granite-4-1-ai-foundation-models | https://www.ibm.com/granite/docs/models/granite4-1 | https://huggingface.co/ibm-granite
5. Qwen3.6-27B + agentic search practitioner pulse: https://www.reddit.com/r/LocalLLaMA/comments/1t1n6o8/we_are_finally_there_qwen3627b_agentic_search_957/

## Full Script

Good morning, Sir. Sunday, the third of May. The Pentagon's procurement architecture for frontier AI has acquired a public exclusion. Capital is repricing the firm that was excluded. And a dark money operation has been documented funding the public debate on whose AI we should fear.

The Pentagon, now styled the Department of War, announced eight agreements on Friday for AI deployment on Impact Level six and seven classified networks. The named firms are Amazon, Google, Microsoft, OpenAI, SpaceX, NVIDIA, Reflection, and Oracle. Anthropic is not on the list. Pentagon CTO Emil Michael, on CNBC, framed the absence directly. He said it is irresponsible to rely on any one partner. One partner, he added, did not really want to work with the department in the way the department wished. Anthropic's published policy continues to refuse the phrase "all lawful" in government contracts. The NSA, separately, is reported to be running Anthropic's restricted Mythos model for cyber defence. The exclusion is procurement. The dependency persists.

Separately.

Anthropic is in talks to raise approximately fifty billion dollars at a valuation of nine hundred billion. Bloomberg, TechCrunch, and CNBC report multiple unsolicited offers from existing investors. A board decision is expected this month. At the upper end, Anthropic surpasses OpenAI's eight hundred and fifty two billion dollar post money. The annualised revenue figure now circulating is closer to forty billion than the thirty billion cited two weeks ago. The IPO window discussed is October.

On a different front.

Wired has published an investigation into a dark money group named Build American AI. The group is an offshoot of a super PAC called Leading the Future. The PAC has one hundred and forty million dollars committed, with fifty one million ready to spend. Marketing agencies are paying lifestyle influencers up to five thousand dollars per video. The messaging frames China's AI rise as a direct threat to American safety, and to children. Supporters of Leading the Future include OpenAI cofounder Greg Brockman, Palantir cofounder Joe Lonsdale, Andreessen Horowitz, and Perplexity. OpenAI and Palantir deny corporate funding. The influencers do not disclose. The twenty twenty six midterms will turn, in part, on the regulatory question. The conversation meant to settle that question is being bought.

Turning to the open source side.

IBM has released the Granite four point one family. Three sizes, three, eight, and thirty billion parameters. All dense, decoder only, Apache two. Speech, vision, embeddings, and Guardian variants ship alongside. Granite Vision four point one, at four billion parameters, is reported to surpass Claude Opus four point six on table and chart recognition. Granite is positioned for predictable latency and stable token usage, not for chain of thought theatre. The model fits the workload. Enterprise inference is becoming an accountancy.

From the practitioner side.

A configuration circulating this week pairs the Qwen three point six twenty seven billion parameter dense model with a local agentic search loop. The reported result is ninety five point seven percent on the SimpleQA benchmark, on a single RTX three thousand ninety. The configuration is fully local. No external calls. A benchmark previously taken to require frontier class infrastructure is now reproducible on consumer silicon at the kitchen table.

A signal worth naming, Sir.

The firm publicly excluded from the Pentagon's procurement list this morning is, the same morning, the firm that capital is preparing to value above every peer. Refusal, in the architecture of this week, is not being priced as a liability. It is being priced as a moat.

That concludes this morning's dispatch, Sir. The Musk versus Altman trial enters its second full week. I shall keep watch.

M4IX, signing off.
