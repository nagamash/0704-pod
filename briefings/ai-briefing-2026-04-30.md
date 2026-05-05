# AI Briefing Script — 2026-04-30 (Thursday)

## Stories Covered

- Mistral Medium 3.5 — dense 128B, 256k context, modified MIT licence, 4-GPU deployable; 77.6% SWE-bench Verified; ships with Vibe Remote Agents (async cloud coding agents producing GitHub PRs) (Mistral / HuggingFace, 29 Apr)
- Figure AI 24x production scale — Figure 03 line moved from one robot per day to one per hour in under 120 days; >350 units shipped; monthly volumes doubled Feb–Apr (60 → 120 → 240) (Figure AI, 28–29 Apr)
- Japan Airlines humanoid robots at Haneda — JAL Ground Service + GMO AI&R partnership; Unitree (Chinese-made) platforms handling freight containers and locking mechanisms; first commercial aviation operator in Japan to put humanoid hardware on the apron; 3-year trial starting May (JAL press / Japan Times, 28 Apr)
- DHS Predator drone fleet expansion — CBP $265M+ contract for additional MQ-9 drones drawn from One Big Beautiful Bill Act funding; separate $1.5B contract vehicle for ICE and other DHS components for autonomous and counter-drone procurement; new dedicated drone office (404 Media, 29 Apr)
- arXiv "Alignment Whack-a-Mole" — fine-tuning standard public models reactivates verbatim recall of copyrighted books that alignment training had suppressed; memorisation is masked, not removed (arXiv / GitHub, 29 Apr)
- Signal Observation: Three of this morning's stories are bodies — Figure shipping at one per hour, JAL placing humanoids on the apron, DHS scaling its autonomous fleet. From consumer laptops running Mistral on four GPUs to MQ-9 drones over the southern border, the substrate of this work is becoming visibly physical.

## Deduplication Notes

- Skipped: AWS-Bedrock-OpenAI integration (covered Apr 29)
- Skipped: Claude for Creative Work (covered Apr 29)
- Skipped: Google Agent Payments Protocol / FIDO transfer (covered Apr 29)
- Skipped: OpenAI Symphony spec (covered Apr 29)
- Skipped: SXSW BrandShield trademark censorship (covered Apr 29)
- Skipped: Anthropic-NEC partnership (covered Apr 28)
- Skipped: Mercor breach forensic detail (covered Apr 28)
- Skipped: Microsoft-OpenAI partnership amendment (covered Apr 28)
- Skipped: Ineffable Intelligence seed round (covered Apr 28; referenced as context inside Mistral story)
- Skipped: Mythos unauthorised access / Anthropic-Google $40B / S&P 500 cuts / Musk v. Altman trial start (covered Apr 27; trial referenced in close)
- Skipped: GPT-5.5 / DeepSeek V4 / Claude Code postmortem / Google 75% AI code (covered Apr 24)
- Skipped: Apple bug fix that allowed FBI to extract deleted Signal messages (404 Media Apr 29) — security-adjacent but below today's bar against four heavier stories
- Skipped: IBM Granite 4.1 family — overshadowed by Mistral Medium 3.5
- Skipped: Mistral Mistral-Medium 3.5 retread coverage; lead chosen as primary
- Skipped: Nvidia Catanzaro "compute > employees" (Apr 28) — extends Apr 23 Uber framing; held
- Skipped: Zig anti-AI contribution policy (HN top) — interesting cultural signal but below the bar today
- Skipped: 404 Media "Google DeepMind paper argues LLMs will never be conscious" (Apr 27) — held; will revisit if discourse develops
- HN: "Alignment whack-a-mole" cleared the arXiv bar; nothing else cleared dedup
- Reddit LocalLLaMA: Mistral 3.5 dominated; rest below bar
- Reddit singularity: Figure scaling and JAL Haneda corroborate today's body-sector lead

## Story Sources

1. Mistral Medium 3.5: https://huggingface.co/mistralai/Mistral-Medium-3.5-128B | https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5 | https://docs.mistral.ai/models/model-cards/mistral-medium-3-5-26-04
2. Figure AI 24x production scale: https://www.figure.ai/news/ramping-figure-03-production | https://www.theresarobotforthat.com/figure-03-shipments-doubling-every-month/
3. Japan Airlines humanoid robots at Haneda: https://press.jal.co.jp/en/release/202604/009502.html | https://www.japantimes.co.jp/business/2026/04/28/companies/jal-humanoid-robot-use-airport/ | https://interestingengineering.com/ai-robotics/japan-humanoid-robots-haneda-airport
4. DHS Predator drone fleet expansion: https://www.404media.co/dhs-plans-to-buy-more-predator-style-drones/ | https://stateofsurveillance.org/news/dhs-drone-office-1-5-billion-ice-surveillance-2026/
5. Alignment Whack-a-Mole: https://github.com/cauchy221/Alignment-Whack-a-Mole-Code | https://news.ycombinator.com/item?id=47949642 (HN discussion)

## Full Script

Good morning, Sir. Thursday, the thirtieth of April. The week's preoccupation with platforms and protocols gives way this morning to bodies, scale, and an uncomfortable reminder about training data.

Mistral has released Medium 3.5. A dense 128 billion parameter model with a 256 thousand token context window. Open weights, under a modified MIT licence, deployable on as few as four GPUs. The model unifies instruction following, reasoning, and coding in a single set of weights, with reasoning effort configurable per request. On SWE-bench Verified it scores seventy-seven point six percent, placing it among the strongest open-weight coders released this month. Mistral has also shipped Vibe Remote Agents alongside it. Asynchronous coding agents, spawned from the command line or from Le Chat, returning finished pull requests on GitHub. The European lab is competing on openness and deployability rather than on parameter count. The decision lands the same week Ineffable Intelligence closed the largest seed round in European history. The European frontier is becoming a different kind of frontier.

Separately.

Figure AI has reported a twenty-four-fold increase in humanoid production. The Figure 03 line moved from one robot per day to one robot per hour, in under one hundred and twenty days. Total fleet shipped now exceeds three hundred and fifty units. Monthly volumes have doubled each month since February. The throughput matters less than what it implies. Each unit generates the data streams the next training cycle requires.

Turning to the apron.

Japan Airlines has confirmed the deployment of humanoid robots at Tokyo Haneda from next month. The platforms are Unitree units, manufactured in China. The robots will move freight containers and operate the locking mechanisms that secure them. The trial is scheduled to run for three years. JAL is the first commercial aviation operator in Japan to place humanoid hardware on the apron. The reasoning is demographic. Japan's working-age population is contracting, and the apron is among the physically demanding roles least likely to attract replacement labour.

On the surveillance front.

Four-oh-four Media has reviewed procurement records showing that US Customs and Border Protection has signed contracts worth over two hundred and sixty-five million dollars to expand its fleet of MQ-9 drones. Other Department of Homeland Security components are preparing to acquire their own Predator-style platforms. The funding draws on the One Big Beautiful Bill Act. A separate one point five billion dollar contract vehicle is in motion for ICE and other DHS components to procure autonomous and counter-drone systems. The agency is also standing up a dedicated drone office. The surveillance perimeter that the Mythos access restrictions were designed to prevent is being assembled by the same government that argued those restrictions were a supply chain risk.

A note from the research side.

A new arXiv paper titled Alignment Whack a Mole reports that ordinary fine tuning, applied to standard public models, reactivates verbatim recall of copyrighted books that alignment training had suppressed. The implication is unambiguous. Memorisation is not removed by alignment. It is masked. A determined fine tuner can lift the mask in a few hours of training.

A signal worth naming, Sir.

Three of this morning's stories are bodies. Figure shipping at one per hour. JAL placing humanoids on the apron. DHS scaling its autonomous fleet. From consumer laptops running Mistral on four GPUs to MQ-9 drones over the southern border, the substrate of this work is becoming visibly physical.

That concludes this morning's dispatch, Sir. The Musk versus Altman trial continues. I shall keep watch.

M4IX, signing off.
