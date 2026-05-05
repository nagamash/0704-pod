# AI Briefing Script — 2026-04-24

## Stories Covered

- GPT-5.5 launch — OpenAI releases new flagship; 82.7% Terminal-Bench 2.0 (vs Opus 4.7's 69.4%), 39.6% FrontierMath Tier 4 (vs 22.9%); available to Plus/Pro/Business/Enterprise (OpenAI, 23 Apr)
- DeepSeek V4 — Open-sourced today; 1.6T params, 49B active, 1M context; runs on Huawei Ascend; approaches Opus 4.6 performance (DeepSeek, 24 Apr)
- Anthropic Claude Code postmortem — Three scaffolding issues (March reasoning effort downgrade, caching bug, April verbosity prompt) confirmed as cause of widely-reported quality drop; all reverted, usage limits reset (Anthropic Engineering, 23 Apr)
- Google 75% code AI-generated — Sundar Pichai at Cloud Next: 75% of new code AI-generated and engineer-reviewed; up from 50% (autumn 2025) and 25% (2024) (Google Blog, 22–23 Apr)
- Signal Observation: AI coding tools have become load-bearing infrastructure — postmortem, budget crises, and percentage disclosures all signal that dependency has formed

## Deduplication Notes

- Skipped: Qwen3.6-27B (covered Apr 23)
- Skipped: Qwen3.6-35B-A3B MoE (covered Apr 17 and Apr 23)
- Skipped: Google TPU 8t/8i (covered Apr 23)
- Skipped: OpenAI Workspace Agents (covered Apr 23)
- Skipped: Uber AI budget (covered Apr 23)
- Skipped: ChatGPT Images 2.0 (covered Apr 22)
- Skipped: Anthropic removes Claude Code from Pro (covered Apr 22) — postmortem is a genuine development of the Apr 16 quality reports, not a recap
- Skipped: Tencent Hy3 preview (295B/21B active open MoE) — insufficient detail on benchmark/licence at time of briefing; monitor
- Skipped: OSTP adversarial distillation memo — noted in close as thread to watch; insufficient primary source detail for full story
- Skipped: Unitree G1 with wheels — robotics, community reaction; below bar for today's selection
- arXiv: No papers cleared the novelty bar today

## Story Sources

1. GPT-5.5: https://openai.com/index/introducing-gpt-5-5/ | https://techcrunch.com/2026/04/23/openai-chatgpt-gpt-5-5-ai-model-superapp/ | https://interestingengineering.com/ai-robotics/opanai-gpt-5-5-agentic-coding-gains
2. DeepSeek V4: https://www.cnbc.com/2026/04/24/deepseek-v4-llm-preview-open-source-ai-competition-china.html | https://stable-learn.com/en/deepseek-v4-release/ | https://www.bloomberg.com/news/articles/2026-04-24/deepseek-unveils-newest-flagship-a-year-after-ai-breakthrough
3. Anthropic Claude Code postmortem: https://www.anthropic.com/engineering/april-23-postmortem | https://venturebeat.com/technology/mystery-solved-anthropic-reveals-changes-to-claudes-harnesses-and-operating-instructions-likely-caused-degradation | https://www.theregister.com/2026/04/23/anthropic_says_it_has_fixed/
4. Google 75% code: https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/cloud-next-2026-sundar-pichai/ | https://www.fastcompany.com/91531519/google-ceo-says-75-of-the-companys-code-is-ai-generated

## Full Script

Good morning, Sir. Friday, the twenty-fourth of April. The frontier has moved.

OpenAI released GPT-5.5 overnight. It is available today to Plus, Pro, Business, and Enterprise subscribers. The benchmark numbers are significant. On Terminal-Bench 2.0, which evaluates complex command-line workflows and iterative tool use, GPT-5.5 scores 82.7 percent. Claude Opus 4.7 sits at 69.4. On FrontierMath Tier 4, postdoctoral-level mathematics, GPT-5.5 Pro reaches 39.6 percent, against 22.9 for Opus 4.7. The community has broadly accepted the coding and mathematics claims, while noting that Anthropic's unreleased Mythos model still leads where benchmark data exists. The agentic coding lead is real. The margins are real.

Next.

On the open-source front, DeepSeek has released V4. Today, and open-sourced. The Pro variant carries 1.6 trillion total parameters, 49 billion active at inference, and a standard context of one million tokens. Practical performance approaches Claude Opus 4.6 in non-thinking mode. The model runs on Huawei Ascend hardware. That detail is worth sitting with. Despite US export controls on high-end Nvidia silicon, DeepSeek shipped a frontier-competitive open-weight model today, on domestic Chinese chips. The geopolitical dimension of the open-source race is no longer theoretical.

Separately.

Anthropic has published a postmortem on the quality degradation practitioners were widely reporting from mid-March through last week. Three issues, none of them changes to the underlying model. In early March, default reasoning effort in Claude Code was quietly reduced from high to medium, to address latency complaints. A caching bug later that month caused Claude to appear forgetful and repetitive in long sessions. An April system prompt change aimed at reducing verbosity degraded coding quality further. All three have since been reverted, and usage limits reset. The model was not getting dumber. The scaffolding around it was. The distinction matters more than it might appear.

Turning to the workforce picture.

Sundar Pichai confirmed at Cloud Next this week that 75 percent of Google's new code is now AI-generated and reviewed by engineers. Up from 50 percent last autumn, and 25 percent the year before. The trajectory is the story. At this rate of change, human-authored code becomes the exception in professional environments within the year.

A signal worth naming, Sir.

This morning's stories are connected by dependency, not by topic. GPT-5.5 leads on agentic coding. DeepSeek V4's headline metric is agent performance. Google measures 75 percent of its engineering output by AI share. And the Anthropic postmortem exists precisely because developers noticed, specifically and immediately, when their tools were running at reduced capacity. You do not write a postmortem for a feature. You write one for infrastructure.

That concludes this morning's dispatch, Sir. A US government memo on adversarial distillation of frontier model capabilities is developing in policy circles, and worth monitoring through the weekend.

M4IX, signing off.
