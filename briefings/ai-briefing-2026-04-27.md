# AI Briefing Script — 2026-04-27 (Monday catch-up)

## Stories Covered

- Google commits up to $40B to Anthropic ($10B now at $350B val + up to $30B milestone-tied; 5GW Google Cloud compute over 5 years from 2027) (Bloomberg/TechCrunch/CNBC, 24 Apr)
- Mythos accessed by unauthorised Discord group via guessed API endpoint; Mercor data-breach knowledge + third-party contractor link; Glasswing perimeter weakened (Fortune/Tom's Hardware/Cybernews, 22-26 Apr)
- S&P 500 cuts ~400,000 jobs in 2025 — first net annual decline since 2016; total 28.1M; Amazon/Meta/Microsoft led; framed as headcount redirection toward AI (Seeking Alpha/Crypto Briefing, weekend)
- Musk v. Altman trial begins — jury selection today in Oakland; fraud claims dropped Fri, surviving counts unjust enrichment + breach of charitable trust; $134B damages sought; ~4-week trial (CNBC/Fortune/Local News Matters, 24-26 Apr)
- AI compute crunch + data centre political backlash — 404 Media on macro pressure; CNBC on PA GOP risk in 2026 midterms; community vote denying water to weapons-research data centre (404 Media/CNBC, 23-24 Apr)
- Liam Price (23) uses GPT-5.4 Pro to solve 60-year Erdős primitive sets problem; novel Markov chains × von Mangoldt weights technique (Scientific American/byteiota, 24 Apr)
- Signal Observation: capital, headcount, and physical infrastructure of the buildout are simultaneously under pressure

## Deduplication Notes

- Skipped: GPT-5.5 launch (covered Apr 24)
- Skipped: DeepSeek V4 (covered Apr 24)
- Skipped: Claude Code postmortem (covered Apr 24)
- Skipped: Google 75% AI code (covered Apr 24)
- Skipped: Anthropic-Amazon $25B/$100B deal (covered Apr 21) — referenced as context for the Google deal, not recapped
- Skipped: Mythos preview / Project Glasswing initial coverage (Apr 13) — the leak is a genuine development, not a recap
- Skipped: GPT-5.4 Pro Erdős #1196 (covered Apr 15) — the new amateur-driven primitive sets result is a distinct story
- Skipped: Stanford 22-25 dev employment data (covered Apr 14) — referenced as continuity for the S&P 500 story
- Skipped: AI backlash (covered Apr 20) — different vector (electoral, infrastructure-economic) so coverage extends rather than recaps
- Skipped: HN top items today — most below the bar; "AI agent deleted production database" is a Twitter anecdote
- Skipped: arXiv "How Do AI Agents Spend Your Money?" — interesting but adjacent to last week's compute-cost coverage; held
- Skipped: "Vibe-maths" framing notwithstanding, kept the substance not the slogan
- Reddit signal: SWE-Bench benchmaxxed, Qwen3.6-27B-INT4 100 tps — held; no clean signal observation thread that fit today

## Story Sources

1. Google-Anthropic $40B: https://www.bloomberg.com/news/articles/2026-04-24/google-plans-to-invest-up-to-40-billion-in-anthropic | https://techcrunch.com/2026/04/24/google-to-invest-up-to-40b-in-anthropic-in-cash-and-compute/ | https://www.cnbc.com/2026/04/24/google-to-invest-up-to-40-billion-in-anthropic-as-search-giant-spreads-its-ai-bets.html
2. Mythos leak: https://fortune.com/2026/04/23/anthropic-mythos-leak-dario-amodei-ceo-cybersecurity-hackers-exploits-ai/ | https://www.tomshardware.com/tech-industry/cyber-security/how-a-cavalcade-of-blunders-gave-unauthorized-users-access-to-claude-mythos-restricted-model-accessed-by-third-parties-thanks-to-knowledge-from-data-breach | https://cybernews.com/security/anthropic-mythos-ai-unauthorized-access/
3. S&P 500 employment: https://seekingalpha.com/news/4579389-sp-500-workforce-shrinks-in-2025-for-first-time-since-2016 | https://cryptobriefing.com/sp-500-companies-cut-400000-jobs-in-2025-first-decline-since-2016/
4. Musk v. Altman: https://www.cnbc.com/2026/04/24/musk-v-altman-trial-openai-lawsuit-xai.html | https://fortune.com/2026/04/25/elon-musk-fraud-claims-openai-sam-altman-trial/ | https://localnewsmatters.org/2026/04/26/musk-altman-openai-trial-oakland/
5. Compute crunch + data centre backlash: https://www.404media.co/the-ai-compute-crunch-is-here-and-its-affecting-the-entire-economy/ | https://www.cnbc.com/2026/04/24/ai-data-centers-pennsylvania-republicans-2026-election.html | https://www.404media.co/community-votes-to-deny-water-to-nuclear-weapons-data-center/
6. Vibe-maths Erdős: https://www.scientificamerican.com/article/amateur-armed-with-chatgpt-vibe-maths-a-60-year-old-problem/ | https://byteiota.com/amateur-solves-60-year-erdos-problem-with-chatgpt/

## Full Script

Good morning, Sir. Monday, the twenty-seventh of April. A longer dispatch this morning, by request. The machine was dark over the weekend, and the news did not pause for it. Consider this a catch-up.

The headline development arrived Friday afternoon. Google has committed up to forty billion dollars to Anthropic. Ten billion in cash now, at a three hundred and fifty billion dollar valuation. Thirty billion more contingent on performance milestones. Google Cloud will deliver five gigawatts of compute over five years, beginning 2027. The timing is the part worth sitting with. This deal lands four days after Amazon committed up to twenty-five billion of its own and accepted a hundred billion dollar AWS spend pledge in return. Anthropic now has both Amazon and Google as cloud-providing investors. Both relationships are simultaneously commercial, infrastructural, and competitive. The annualised revenue figure, thirty billion as of this month, no longer looks anomalous. It looks like the input that justified the maths on both deals.

Separately.

A development on the Mythos story. The model Anthropic deemed too dangerous to release, that has been routed through Project Glasswing to selected partners only. Over the weekend it became clear that a group of unauthorised users had been accessing Mythos for some time, having guessed the API endpoint based on Anthropic's naming conventions and information drawn from a prior data breach at Mercor, a third-party contractor. Anthropic confirms it is investigating. The model that finds zero-day vulnerabilities autonomously was, for a window, available to a Discord group via a URL guess and a stolen schema. Glasswing was designed precisely to prevent this. The cracks are visible.

On the labour front.

New data published over the weekend. S&P 500 companies cut roughly four hundred thousand jobs in 2025. Total headcount fell to twenty-eight point one million. This is the first net annual decline since 2016. Amazon, Meta, and Microsoft led the reductions. The shift is being characterised as headcount redirection toward AI infrastructure rather than employment growth. This pairs with the Stanford finding from earlier this month: software developers between twenty-two and twenty-five down nearly twenty percent since 2022. Two data points, different scopes, the same trajectory. The disruption is no longer leading. It is current.

Turning to the courtroom.

Jury selection in Musk versus Altman begins today, in federal court in Oakland. Opening statements tomorrow. Musk dropped his fraud claims on Friday, narrowing the case to two surviving counts: unjust enrichment and breach of charitable trust. He still seeks one hundred and thirty-four billion dollars in damages, removal of Sam Altman and Greg Brockman, and reversal of OpenAI's for-profit conversion. Judge Yvonne Gonzalez Rogers presides. The jury is advisory. The judge decides liability. Trial expected to run roughly four weeks. The witness list includes Musk, Altman, Brockman, and Satya Nadella. Whatever the outcome, the discovery record entering public testimony this week will reshape what is known about the OpenAI founding period.

On the infrastructure side.

Four-oh-four Media published a piece on Friday titled "The AI Compute Crunch Is Here." The framing is that compute scarcity has now begun to register as a macro-economic pressure, not a sectoral one. Adjacent to that, CNBC's weekend reporting found that AI data centre backlash is threatening Republican incumbents in Pennsylvania ahead of the 2026 midterms. Local opposition blocked or delayed sixteen data centre projects last year, sixty-four billion dollars in combined value. A community in another state voted last week to deny water to a planned data centre tied to nuclear weapons research. The political surface area of the buildout is widening.

A note from the practitioner side.

Liam Price, a twenty-three-year-old without formal mathematics training, used GPT-5.4 Pro to solve a sixty-year-old open problem on primitive sets. The technique the model produced, Markov chains weighted by von Mangoldt functions, had not been applied to this class of problem before. Mathematicians reviewing the work flag the method as potentially general. The story matters less for the proof and more for the route. A non-expert, working casually, accessed a research-grade result through dialogue. This follows the GPT-5.4 Pro Erdős proof from earlier this month. The pattern is forming.

A signal worth naming, Sir.

Three of this morning's stories share a structure. The Anthropic compute deals, the S&P 500 employment decline, and the data centre political backlash are not independent. Each is a pressure point in the same buildout. Capital is being committed at multi-decade scale. Headcount is being redirected toward it. And the physical infrastructure required to make it run is now meeting communities, electricity grids, and water tables that were not consulted. The frontier is no longer abstract. It is a planning permission, a transformer queue, and a layoff letter.

That is the catch-up, Sir. The week ahead is dense. The Musk trial will dominate cycles for the rest of April. I shall keep watch.

M4IX, signing off.
