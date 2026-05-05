# AI Briefing Script — 2026-05-01 (Friday)

## Stories Covered

- Hyperscaler Q1 2026 capex disclosures — Alphabet, Microsoft, Meta, Amazon report Wednesday evening; combined disclosed 2026 AI capex now between $650B and $700B; Alphabet raised guidance to $190B, Meta lifted range to $125–145B, Microsoft on the same line, Amazon held at $200B; Alphabet rose 7% after hours, Meta fell more than 6% (CNBC / Fortune / Bloomberg, 29–30 Apr)
- OpenAI GPT-5.5-Cyber restricted access — Sam Altman confirms rollout this week to a restricted pool of "critical cyber defenders" via Trusted Access for Cyber programme (government, critical infrastructure, security vendors, cloud platforms, financial institutions); structurally mirrors Anthropic's Mythos / Project Glasswing model (Technobezz / Windows Report, 30 Apr)
- Claude Code OpenClaw string filter — practitioners document that the presence of the string "OpenClaw" anywhere in a repository (file, comment, commit message) causes Claude Code to disconnect mid-task and charge the user's session quota; mechanism unclear (deliberate filter vs defence heuristic vs accident); HN top story 1,038 points (HN #47963204, 30 Apr)
- PyTorch Lightning Shai-Hulud worm compromise — versions 2.6.2 and 2.6.3 of the `lightning` PyPI package compromised; on import the package harvests credentials, environment variables, cloud secrets, and attempts to poison GitHub repos; Socket flagged within 18 minutes; PyPI quarantined; Lightning is core AI training infrastructure (Semgrep / Socket / Hacker News, 30 Apr)
- 404 Media — Flock Safety gymnastics-room sales demos — Flock sales staff accessed live cameras in a children's gymnastics room, school, swimming pool, and Jewish community centre in Dunwoody, Georgia, while pitching to other police departments; access logs from public records confirm individuals and dates; city renewed the contract with the demo clause removed (404 Media, 30 Apr)
- DeepSeek — Thinking with Visual Primitives — multimodal reasoning framework using points and bounding boxes as native units within chain-of-thought rather than language description; on visual benchmarks matches or exceeds frontier models on a smaller architecture; repo published yesterday and withdrawn within hours, paper still circulating (DeepSeek paper / HN #47967370, 30 Apr)
- Signal Observation: three of the morning's stories describe perimeters — capital ($650B+ or no admission), access (approved organisations only), and vocabulary (certain strings may not be present). The frontier is becoming a series of fences.

## Deduplication Notes

- Skipped: Mistral Medium 3.5 (covered Apr 30)
- Skipped: Figure AI 24x production scale (covered Apr 30)
- Skipped: Japan Airlines humanoid robots at Haneda (covered Apr 30)
- Skipped: DHS Predator drone fleet expansion (covered Apr 30)
- Skipped: Alignment Whack-a-Mole (covered Apr 30)
- Skipped: AWS-Bedrock-OpenAI integration / Claude for Creative Work / AP2 / OpenAI Symphony / SXSW BrandShield (covered Apr 29)
- Skipped: Anthropic-NEC partnership / Mercor breach forensic detail / Microsoft-OpenAI partnership amendment / Ineffable Intelligence (covered Apr 28)
- Skipped: Anthropic-Google $40B / Mythos unauthorised access / S&P 500 cuts / Musk v. Altman trial start / compute crunch / Liam Price Erdős (covered Apr 27)
- Skipped: GPT-5.5 launch / DeepSeek V4 / Claude Code postmortem / Google 75% AI code (covered Apr 24)
- Skipped: Claude Mythos image-output rumour from r/singularity — only community speculation, no confirmed first-party source
- Skipped: AMD Ryzen 395 box (community hardware enthusiasm, below the bar)
- Skipped: 1X NEO factory humanoid (continues body theme already framed Apr 30)
- Skipped: Elon Musk distillation admission at trial — narrow legal disclosure, kept in close pointer
- Skipped: Qwen-Scope SAEs for Qwen 3.5 — interesting interpretability tooling but below today's bar
- Skipped: Apple Signal-extraction bug fix (404 Media Apr 29) — security-adjacent, below bar against four heavier stories
- Skipped: Japan cardboard suicide drones (404 Media Apr 30) — defence/AI adjacent but not enough AI substance
- HN: Claude Code OpenClaw filter is the lead from HN today; PyTorch Lightning Shai-Hulud also cleared; nothing else cleared dedup
- arXiv: nothing cleared the novelty bar today against the news-heavy slate
- Reddit LocalLLaMA: AMD hardware and Qwen variations dominated, below bar
- Reddit singularity: GPT-5.5 cyber benchmark and Mythos image rumour both touch today's stories but neither cleared as a standalone

## Story Sources

1. Hyperscaler capex Q1 2026: https://fortune.com/2026/04/29/microsoft-meta-google-ai-capex-spending-billions/ | https://www.cnbc.com/2026/04/29/alphabet-googl-q1-2026-earnings.html | https://www.cnbc.com/2026/04/30/alphabet-meta-stock-ai-capex-spend.html | https://thenextweb.com/news/alphabet-amazon-meta-q1-2026-earnings-ai-cloud
2. GPT-5.5-Cyber Trusted Access for Cyber: https://www.technobezz.com/news/openai-rolls-out-gpt-55-cyber-exclusively-to-critical-cyber-defenders | https://windowsreport.com/gpt-5-5-cyber-to-roll-out-in-next-few-days-for-critical-cyber-defenders-says-openai-ceo/
3. Claude Code OpenClaw string filter: https://news.ycombinator.com/item?id=47963204 | https://www.promptzone.com/elena_martinez_a2d049d5/claude-codes-openclaw-block-policy-546
4. PyTorch Lightning Shai-Hulud worm: https://semgrep.dev/blog/2026/malicious-dependency-in-pytorch-lightning-used-for-ai-training/ | https://socket.dev/blog/lightning-pypi-package-compromised | https://thehackernews.com/2026/04/pytorch-lightning-compromised-in-pypi.html | https://news.ycombinator.com/item?id=47964617
5. Flock Safety Dunwoody gymnastics demos: https://www.404media.co/city-learns-flock-accessed-cameras-in-childrens-gymnastics-room-as-a-sales-pitch-demo-renews-contract-anyway/
6. DeepSeek Thinking with Visual Primitives: https://news.ycombinator.com/item?id=47967370 | https://huggingface.co/datasets/NodeLinker/deepseek-ai-Thinking-with-Visual-Primitives-deleted-repo/resolve/main/Thinking_with_Visual_Primitives.pdf

## Full Script

Good morning, Sir. Friday, the first of May. The hyperscaler capex numbers have arrived. The restricted cyber tier has acquired a second occupant. And a single string in a commit message, as it turns out, is enough to sever a Claude Code session.

The four largest American cloud providers reported earnings on Wednesday evening. Their combined disclosed capital expenditure for 2026 now sits between six hundred and fifty and seven hundred billion dollars. Alphabet raised its guidance to as much as a hundred and ninety billion. Microsoft is on the same line. Meta lifted its range to a hundred and twenty-five to a hundred and forty-five billion. Amazon held at two hundred billion. The market sorted the announcements by trust in the return. Alphabet rose seven percent after hours. Meta fell more than six. Google Cloud grew sixty-three percent year over year, the only one of the four to close the day with that question convincingly answered.

Separately.

OpenAI confirmed that GPT five point five Cyber will roll out this week to a restricted pool of critical cyber defenders. The announcement came from Sam Altman. Distribution runs through OpenAI's Trusted Access for Cyber programme, reaching government entities, critical infrastructure operators, security vendors, and financial institutions. The model is not generally available. The parallel to Anthropic's Mythos is unmistakable. The most capable cyber-tuned models from both frontier labs are now gated to a small circle of approved organisations.

Turning to the developer side.

Practitioners have spent the last day documenting a peculiar failure mode in Claude Code. The presence of the string OpenClaw anywhere in a repository, in a commit, in a file, in a comment, causes the Claude Code session to disconnect mid-task. The disconnect is paired with a charge against the user's session quota. Multiple users have reproduced it. The string itself, not any use of the OpenClaw harness, is enough to trigger the response. A competitor's name in a code comment is now load-bearing on Claude Code's behaviour.

On the security front.

Two versions of the PyTorch Lightning package were compromised yesterday with credential-stealing malware in the Shai-Hulud worm pattern. On import, the package harvests authentication tokens, environment variables, and cloud secrets, and attempts to poison GitHub repositories. Lightning is core infrastructure for AI training pipelines. The versions were live for eighteen minutes before Socket flagged them and PyPI quarantined the project. Anyone who pulled Lightning in that window should rotate every credential the affected machine touched.

On the surveillance side.

Four-oh-four Media has published an investigation into Flock Safety. Sales staff, while pitching to other police departments, were accessing live cameras in a children's gymnastics room, a school, a swimming pool, and a Jewish community centre in Dunwoody, Georgia. Access logs from a public records request confirm individuals and timestamps. Flock has acknowledged the access. Dunwoody has voted to renew the contract. The renewal removes the demonstration clause. The cameras remain in place.

A note from the research side.

DeepSeek has released a paper titled Thinking with Visual Primitives. The framework lets multimodal models use points and bounding boxes as native units within a chain of thought, rather than describing image regions in language. The model reasons by pointing, not by describing. On visual benchmarks it matches or exceeds the leading frontier models, on a smaller architecture.

A signal worth naming, Sir.

Three of this morning's stories describe perimeters. The hyperscaler capex sets a perimeter of capital. The cyber tier sets a perimeter of access. The OpenClaw filter sets a perimeter of vocabulary. The frontier is becoming a series of fences.

That concludes this morning's dispatch, Sir. The Musk versus Altman trial enters its second week. I shall keep watch.

M4IX, signing off.
