# October 2026 benchmark audit

Audit date: **2026-10-27**. New-work window: **2026-09-24 through 2026-10-27**. English-only dated audit snapshot, as allowed by `AGENT.md`.

Machine-readable records: [source inventory](../data/audits/october_2026_source_inventory.json) (dispositions, source hashes, extraction methods) and [added observations](../data/audits/october_2026_added_observations.json) (every accepted score, model, source and role).

## Releases reviewed

| Release | Date | Primary source |
|---|---|---|
| Claude Sonnet 5.5 | 2026-09-28 | [launch post](https://www.anthropic.com/news/claude-sonnet-5-5), [system card](https://www.anthropic.com/claude-sonnet-5-5-system-card) |
| GPT-6.1 Sol | 2026-09-29 | [launch post](https://openai.com/index/introducing-gpt-6-1-sol/) |
| Claude Haiku 5.5 | 2026-10-07 | [launch post](https://www.anthropic.com/news/claude-haiku-5-5), [system card](https://www.anthropic.com/claude-haiku-5-5-system-card) |
| DeepSeek-V4.1-Flash-1017 | 2026-10-17 | [model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) |
| Kimi K3.1 Pro | 2026-10-23 | [tech blog](https://www.kimi.com/blog/kimi-k3-1-pro); date from the [Kimi Forum announcement](https://forum.moonshot.ai/t/kimi-k3-1-pro-has-launched-start-exploring-now/629) (2026-10-23T20:12:59Z) and the [official X post](https://x.com/Kimi_Moonshot/status/2113680701770068067) (2026-10-23 17:15 UTC) |
| GPT-6.1 Terra | 2026-10-26 | [launch post](https://openai.com/index/introducing-gpt-6-1-terra/) |

OpenAI launch-page values come from chart point aria-labels in the rendered page (direct fetch returns HTTP 403); see the verification section below. Kimi values come from the table data embedded in the page. DeepSeek values come from the model-card text table.

## Changes

- **Epoch AI export** (`benchmark_data.zip`, 2026-10-27): new rows appended unmodified for ARC-AGI-2, BALROG, CritPt, FrontierMath Tier 4 v2 and Tiers 1–3 v2, GPQA Diamond, GSO, SimpleQA Verified and Vending-Bench 2 (new record IDs only); APEX-Agents, SciCode, DTBench and FrontierCode 1.1 (models released on or after 2026-09-22 only, because these files lack stable IDs or were re-keyed); and the two new Scale HLE leaderboard rows.
- **Vendor releases**: Terminal-Bench 4.0, Terminal-Bench-Science 0.1, DeepSWE v1.1, FrontierSWE v2, CursorBench 4.0, Agents' Last Exam, Chartography, HLE, OSWorld 2.0 (offline set), AutomationBench (auxiliary private split), GPQA Diamond and BrowseComp. Protocol mismatches are auxiliary series: ALE v1.1 (Kimi) and unpinned ALE (DeepSeek); vendor no-tools HLE; Kimi tool-enabled HLE.
- **New card: FrontierCS 2** ([arXiv 2610.29932v1](https://arxiv.org/abs/2610.29932v1), 2026-10-21; [leaderboard](https://frontier-cs.org)). 48 public CS R&D tasks, pass rate over 48 runs, 16 agent/harness rows covering 6 of 7 reference organizations, including DeepSeek-V4.1-Flash-1017, Kimi K3.1 Pro and GPT-6.1 Terra. The FCI index is not used.

## Lifecycle

The snapshot advances from 2026-09-23 to 2026-10-27.

| View | Added | Removed |
|---|---|---|
| test-of-time | climaqa-gold-mcq-default, eai-v3-virtualhome-action-sequencing-task-sr, mv-robobench-v2-unified-zeroshot-avg, ost-bench-v2-multiround | — |
| still-frontier | — | apex-agents, gso |
| fastest-solved | — | — |
| recently-saturated | — | arc-agi-2 |

`browsecomp` briefly entered Recently Saturated in the first October build on a single vendor-reported row; the verification pass below demotes that row, so BrowseComp is not in any story view.

## Not imported

See the inventory for each reason. Main groups: OSWorld 2.1 and GDPval-AA v2.1 results (versions differ from the tracked cards); HealthBench (raw versus length-adjusted decision pending); BenchCAD 1,000-file subsets; cyber evaluations with different scoring; MMMU-Pro Vision-only (Terra) and an unverified-aggregate MMMU-Pro (Kimi); and older models shown on new launch charts. New-benchmark candidates Doc2Harness, SCI-AGENT-EXAM and E2E-SWE are queued in `CURATION_QUEUE.md`.

## Verification pass (2026-10-27)

Follow-up on open questions from the first October pass. All sources accessed 2026-10-27; details and URLs are also in `verification_2026_10_27` of the source inventory.

- **BrowseComp / Kimi K3.1 Pro 92.1%.** No independent BrowseComp run of Kimi K3.1 Pro was found ([Vals](https://www.vals.ai/models/kimi_kimi-k3.1-pro) lists none). Other vendors already reported at least 90%: the [GPT-6 Astra page](https://openai.com/index/gpt-6-astra/) (2026-09-03) has a text table with GPT-6 Astra 91.5%, GPT-5.6 Sol 90.4% and Claude Opus 5 90.8%. With the earliest-date rule, those rows would date a 90% crossing to July 2026 (GPT-5.6 Sol, released 2026-07-09). That is outside the three-month Recently Saturated window, so the Kimi row was dating saturation from import coverage, not from evidence. The Kimi row is now the auxiliary series `browsecomp-vendor-reported-kimi-harness`. The canonical frontier falls back to Deep Research 51.5% (T80/T90 right-censored), and BrowseComp leaves Recently Saturated. Importing a reviewed vendor-reported series is queued in `CURATION_QUEUE.md`.
- **GPT-6.1 Sol / Terra chart values.** The system-card addenda ([Sol](https://deploymentsafety.openai.com/gpt-6-1-sol), [Terra](https://deploymentsafety.openai.com/gpt-6-1-terra)) do not report these evaluations, and no text or table source was found. All 40 imported values were re-read from the rendered pages' chart point aria-labels (`Model; Effort; Cost; Score: x%`, one decimal). Each matched exactly, so no value changed or was dropped. The page text states Terra's Terminal-Bench 4.0 max score (50.3%) and is arithmetically consistent with several more values (noted per row). The Sol Terminal-Bench-Science values are identical on the Sol and Terra pages.
- **Kimi K3.1 Pro release date.** It stays 2026-10-23, now from explicit timestamps: the official Kimi Forum announcement (created 2026-10-23T20:12:59Z) and the official X post (2026-10-23 17:15 UTC). The blog JSON-LD gives only `dateModified` 2026-10-24 (Beijing date). The [platform changelog](https://platform.kimi.com/docs/changelog) has no October entry yet.
- **Gemini 4 Argon release date.** Google [announced Argon on 2026-09-30](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/), with access limited to Fairwind Program cyber defenders. [General availability was 2026-10-13](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/), confirmed by the [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) and the [model card](https://deepmind.google/models/model-cards/gemini-4-argon/) ("Published 13 October 2026"). Repository-authored FrontierCS 2 rows now use the public release date, 2026-10-13. Epoch export rows keep 2026-09-30 unmodified, because raw rows are immutable and that date is Google's own announcement date. Lifecycle results do not change: FrontierCS 2 plots clip at its 2026-10-21 release.
- **Qwen 3.8 Max on FrontierCS 2.** The [FrontierCS-2 harness README](https://github.com/FrontierCS/FrontierCS-2/blob/a56a2afa0e/candidates/qwen-code/README.md) names the evaluated model `Qwen/Qwen3.8-Max-VL-Thinking` (alias `qwen3.8-max-vl-thinking`, effort high). That identifier does not appear in [Alibaba Cloud Model Studio documentation](https://docs.modelstudio.console.alibabacloud.com/en/model-studio/qwen3-8-max), which lists `qwen3.8-max` and the `qwen3.8-max-0902` snapshot, or as a public Hugging Face model. The row stays undated, and the identifier is recorded in its note.
- **Claude Sonnet 5.5 / Haiku 5.5 launch-post values.** Every launch-post value was found in system-card text: section text for Terminal-Bench 4.0 and Chartography, and Table 8.1.A for HLE. These are added as extra evidence rows that merge into the existing measurements. The Sonnet 5.5 no-tools HLE row had been cited from the Haiku launch post with a 2026-09-28 public date, but that post was published on 2026-10-07. The row now carries 2026-10-07, and the Sonnet system card supplies the 2026-09-28 publication. Observation dates are unchanged.
- **Not re-researched:** DeepSeek-V4.1-Flash-1017 (model-card text table) and system-card text rows.
- **Noted, not changed:** the GPT-6.1 Terra Terminal-Bench 4.0 chart also plots GPT-6.1 Sol (47.1–55.9%). These points were never imported and are recorded in the inventory for a separate decision.
