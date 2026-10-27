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
| Kimi K3.1 Pro | 2026-10-23 | [tech blog](https://www.kimi.com/blog/kimi-k3-1-pro) (no printed date; date from asset paths) |
| GPT-6.1 Terra | 2026-10-26 | [launch post](https://openai.com/index/introducing-gpt-6-1-terra/) |

OpenAI launch-page values come from chart point labels in the rendered page (direct fetch returns HTTP 403). Kimi values come from the table data embedded in the page. DeepSeek values come from the model-card text table.

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
| recently-saturated | browsecomp | arc-agi-2 |

`browsecomp` enters Recently Saturated on a single vendor-reported row (Kimi K3.1 Pro, 92.1%); the card's other evidence is sparse.

## Not imported

See the inventory for each reason. Main groups: OSWorld 2.1 and GDPval-AA v2.1 results (versions differ from the tracked cards); HealthBench (raw versus length-adjusted decision pending); BenchCAD 1,000-file subsets; cyber evaluations with different scoring; MMMU-Pro Vision-only (Terra) and an unverified-aggregate MMMU-Pro (Kimi); and older models shown on new launch charts. New-benchmark candidates Doc2Harness, SCI-AGENT-EXAM and E2E-SWE are queued in `CURATION_QUEUE.md`.
