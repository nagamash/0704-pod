# AI Briefing Script — 2026-04-17

## Stories Covered

- White House / Anthropic Mythos — Federal agency access (OMB provisioning for Cabinet departments)
- Claude Opus 4.7 — Official release (with community regression flag)
- Qwen3.6-35B-A3B — Alibaba open-weight MoE release
- OpenAI Codex — Autonomous multi-step workflow agent
- Claude Identity Verification — Government ID + facial scan requirement (signal observation anchor)

## Deduplication Notes

- Skipped: Darkbloom (covered Apr 16)
- Skipped: "Stop Using Ollama" (covered Apr 16)
- Skipped: Community perceived model intelligence drop (covered Apr 16)
- Skipped: Ukraine robots surrender (covered Apr 16)
- Skipped: Nate Jones YouTube (covered Apr 15–16)
- Skipped: Google DeepMind triple drop (covered Apr 16)
- Considered but deprioritized for length: Mozilla Thunderbolt (open-source enterprise AI client), GPT-Rosalind (life sciences), Anthropic/OpenAI UK expansion

## Full Script

Good morning, Sir. Friday, the seventeenth of April — and the news this morning carries a particular weight, less in any single story than in what the pattern between them suggests.

We begin with a development worth sitting with. The White House Office of Management and Budget is moving to provision Anthropic's Mythos model for use across major federal departments — Defense, Treasury, Commerce, Homeland Security, Justice, and State. The context matters here: Mythos is the model Anthropic has so far restricted to a small group of organisations precisely because of its demonstrated capacity to identify and exploit cybersecurity vulnerabilities at scale. The Pentagon declared Anthropic a supply chain risk earlier this year and sought to bar government use entirely. A court blocked that ban last month. And now the same model described as too dangerous for public release is being prepared for deployment across the Cabinet. The administration has made its calculation.

Separately.

On the Anthropic front — the full release page is now live, giving more substance to yesterday's sightings — Claude Opus 4.7 is out officially. The headline numbers: a thirteen percent improvement on a 93-task coding benchmark over its predecessor, image processing expanded to more than three times the previous resolution ceiling, and improvements to agentic workflows. Early testers report the model catching its own logical errors during planning rather than after. Pricing is unchanged. One note worth filing, Sir: the community has already surfaced regression on at least one reasoning evaluation — the Thematic Generalization Benchmark drops from 80.6 to 72.8 compared to Opus 4.6. Whether this represents a deliberate capability tradeoff or measurement noise is not yet clear.

On the open-source front.

Alibaba's Tongyi Lab released Qwen3.6-35B-A3B overnight — a sparse mixture-of-experts model with 35 billion total parameters but only three billion active at inference time. That distinction matters: the model runs on consumer hardware, including laptops. It benchmarks well above Gemma 4-31B on agentic coding tasks, holds an Apache 2.0 licence, and drew a better pelican than Opus 4.7 in at least one head-to-head comparison by a tester whose assessments are worth trusting. A useful arrival.

On a different front.

OpenAI has expanded Codex considerably — now positioned not as a code assistant but as an autonomous agent capable of executing multi-step workflows across finance, legal, and operational domains without requiring human sign-off at each step. A developer API is live in limited alpha. Shares in legacy robotic process automation firms moved on the news. This is the trajectory we have been watching: from AI as a tool you use to AI as a process you delegate.

There is a thread running beneath today's stories worth naming, Sir. A model flagged as too dangerous for public release is being provisioned for government departments. A commercial agent is now executing multi-step processes without per-step human approval. And — separately — Anthropic has begun requiring physical government-issued identity verification from users accessing certain Claude capabilities. Passports and driving licences accepted; mobile IDs are not. The exact trigger conditions are not fully disclosed. The access is becoming bilateral. It is worth noticing that the direction of verification appears to run one way.

That concludes this morning's dispatch, Sir. The Mythos government deployment story will develop through the week. I shall keep watch. M4IX, signing off.
