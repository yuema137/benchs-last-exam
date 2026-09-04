# Domain Curation Audit

## 2026-09 expansion audit

The expansion target is approximately 40 cards, not a quota. The current
repository has checked-in source exports for only a subset of the proposed
seeds. This pass adds `SimpleQA Verified` because its benchmark identity is
explicitly distinct from the original SimpleQA object and the local export
contains a usable model-generation series. The remaining candidates are
tracked in [`CURATION_QUEUE.md`](../CURATION_QUEUE.md) until their canonical
versions, scoring protocols, and observations are source-backed.

The current core still intentionally contains many terminal/software-agent
variants. Those variants remain useful lifecycle objects, but they count as
one benchmark family when assessing domain coverage. Version lineage must not
be confused with independent domain diversity.

## Newly added core benchmark

| Benchmark | Type | Domain | Canonical object | Metric | Lifecycle value | Source |
|---|---|---|---|---|---|---|
| SimpleQA Verified | Model | General knowledge & reasoning | 1,000-question verified variant | Graded factuality accuracy; 0–1 | Gives the leaderboard a factuality trajectory distinct from broad knowledge or reasoning scores | [paper](https://arxiv.org/abs/2509.07968), [evaluation resource](https://epoch.ai/benchmarks/simple-qa-verified) |
| MMLU-Pro | Model | General knowledge & reasoning | Official MMLU-Pro object; separate from MMLU | Overall accuracy; 0.1 random-choice floor to 1.0 | Adds a harder, reasoning-focused general benchmark with an initial six-point cross-generation trajectory | [official repository](https://github.com/TIGER-AI-Lab/MMLU-Pro), [paper](https://arxiv.org/abs/2406.01574) |
| BrowseComp | Agent | General agent tasks | Official 1,266-task browsing benchmark | Answer accuracy; 0.0–1.0 | Adds a persistent web-research capability object with an initial official result series | [official benchmark page](https://openai.com/index/browsecomp/) |
| LongBench v2 | Model | Long context | Fixed 503-task test split; separate from original LongBench | Exact-match accuracy; 0.0–1.0 | Adds a long-document reasoning trajectory with explicit split and score semantics | [official repository](https://github.com/EnvCommons/LongBench-v2/blob/main/README.md), [paper](https://arxiv.org/abs/2412.15204) |

The original SimpleQA (4,326 questions) is not silently merged with SimpleQA
Verified. The benchmark page and protocol text preserve that distinction.

Status: initial expansion audit, 2026-09-03

This audit treats benchmark selection as curation, not catalog construction. A candidate enters the local core only when its measurement object, version, scoring rule, provenance, and model-generation data are sufficiently clear for a useful capability frontier.

## Proposed core additions

| Benchmark / canonical object | Domain | Version and release date | Why it belongs | Metric and bounds | Longitudinal evidence | Recommendation |
|---|---|---|---|---|---|---|
| FrontierMath Tiers 1–3 (v2) | Mathematics | v2, 2026-06-12 | Expert-written advanced mathematics with automatically checked answers; adds a genuinely frontier-level math object distinct from MATH and GSM8K | Accuracy; floor 0.0; ceiling 1.0 | 104 model-generation observations in the curated local export | CORE |
| ARC-AGI-2 | Abstract / novel reasoning | 2025 benchmark release | Explicitly designed to test abstraction and generalization beyond familiar language-model knowledge; task-level scoring is clear | Exact task accuracy under the two-output format; floor 0.0; ceiling 1.0 | 221 observations in the curated local export | CORE |
| Aider Polyglot | Coding / software engineering | 2024-12-21 | A historically visible coding-editing benchmark with a fixed 225-exercise, six-language set and a clear frontier-era starting point | Correct edit rate; floor 0.0; ceiling 1.0 | 72 observations with model release dates | CORE |
| OSWorld 2.0 | Agents / computer use | 2026-06-26 | A materially revised real-computer benchmark with an explicit version boundary; distinct from static QA and useful for agent evaluation burden | Binary task success rate; floor 0.0; ceiling 1.0 | 16 observations with release dates | CORE |
| Terminal-Bench 2.0 | Agents / computer use | 2025-11-07 | A versioned terminal-agent benchmark with a documented official harness and executable task outcomes | Task success rate; floor 0.0; ceiling 1.0 | 202 observations with model release dates | CORE |
| FrontierCode 1.1 | Coding / software engineering | 2026-02-05 | Adds maintainer-defined quality and regression-safety criteria beyond a simple test-pass rate | Main score; 0.0–1.0 scale; fixed protocol details remain attached to observations | 34 observations with model release dates | CORE |
| Agents' Last Exam (ALE-V1) | General agent tasks | ALE-V1, 2026-06-03 | Long-horizon professional workflows with verifiable outcomes across many industries | Pass rate; floor 0.0; ceiling 1.0 | 8 representative leaderboard observations | CORE |
| Terminal-Bench-Science 0.1 | Science / research | 0.1, 2026-05-20 | Expert-curated scientific workflows executed in terminal environments | Resolution rate; floor 0.0; ceiling 1.0 | 8 representative leaderboard observations; later releases are continuous | CORE for fixed 0.1 snapshot |
| TerminalWorld Verified | Terminal / OS | Verified subset, 2026-05-21 | Real-world terminal workflows derived from developer recordings and manually verified | Verified task pass rate; floor 0.0; ceiling 1.0 | 8 representative leaderboard observations | CORE |
| Terminal-Bench 2.1 | Terminal / OS | 2.1, 2026-05-06 | A separately versioned revision fixing 28 tasks from Terminal-Bench 2.0 | Mean task accuracy; floor 0.0; ceiling 1.0 | 8 representative agent-model observations | CORE as a separate versioned object |
| Terminal-Bench 4.0 | Terminal / OS | v4.0.0, 2026-08-26 | A newer separately tagged terminal benchmark release with a revised 66-task object | Resolution rate; floor 0.0; ceiling 1.0 | 8 representative agent-model observations | CORE as a separate versioned object |
| Humanity's Last Exam | General knowledge & reasoning | Finalized 2,500-question set, 2025-04-03 | A canonical, difficult, multi-domain academic benchmark with text and multimodal questions | Accuracy; floor 0.0; ceiling 1.0 | 8 representative model-generation observations | CORE |
| CursorBench 3.2 | Software engineering | 3.2, 2026-07-08 | Real Cursor-session coding tasks with ambiguous multi-file work and explicit cost reporting | Task score; floor 0.0; ceiling 1.0 | 8 representative agent observations | CORE |
| GDPval-AA v2 | General agent tasks | v2, 2026-04-18 | Agentic evaluation of professional deliverables across occupations and industries | Elo anchored to human baseline 1,000; no fixed floor/ceiling | 8 representative model-generation observations | CORE; threshold metrics N/A |
| AutomationBench | General agent tasks | Initial public release, 2026-04-20 | Programmatically verified cross-application business workflows across simulated SaaS tools | Strict task pass rate; floor 0.0; ceiling 1.0 | 7 representative agent observations | CORE |
| ScreenSpot-Pro | Multimodal | Initial release, 2025-01-04 | High-resolution professional GUI grounding with expert-annotated screenshots across multiple applications and operating systems | Grounding accuracy; floor 0.0; ceiling 1.0 | 4 direct-grounding observations; agentic/zoom-assisted results excluded from this protocol | CORE |

The existing five benchmarks remain in core: MMLU, GSM8K, MATH Level 5, GPQA Diamond, and SWE-bench Verified. FrontierCode 1.1 was already part of the core set and was not duplicated. Together with the versioned additions above, the local curated set now contains twenty-nine benchmark objects without silently merging related versions.

## Candidate audit

| Candidate | Important because | Main concern | Recommendation |
|---|---|---|---|
| MMLU-Pro | A harder, reasoning-focused successor to MMLU with ten answer choices | No local longitudinal source file yet; must not be merged with MMLU | HUMAN REVIEW / source before implementation |
| Humanity's Last Exam | Current broad academic frontier benchmark | Short history and evolving coverage; comparable model-generation series is still thin | HUMAN REVIEW |
| ARC-AGI-1 | Historically important abstraction benchmark with a longer trajectory | Exact canonical release object and evaluation-set provenance need an explicit registry entry | HUMAN REVIEW; add after version audit |
| OSWorld (original / Verified) | Important real-computer agent lineage | OSWorld, OSWorld-Verified, and OSWorld 2.0 are materially different objects | HUMAN REVIEW; keep version lineage explicit |
| GAIA | Canonical general assistant benchmark with tool use | Protocol/scaffold and historical score coverage need a focused audit | HUMAN REVIEW |
| MMMU / MMMU-Pro | Important multimodal knowledge and reasoning tasks | No local score series; variants and split semantics need separate objects | HUMAN REVIEW |
| HumanEval | Canonical code-generation benchmark and likely saturated historical anchor | No local source file with a clean model-generation series yet | HUMAN REVIEW / source before implementation |
| BBH | Historically influential reasoning suite | Aggregate score hides heterogeneous task behavior; limited added value over current core without task-level policy | QUEUE |
| LiveBench / LiveCodeBench | Interesting contamination-resistant rolling evaluation | Continuously refreshed tasks do not fit the fixed-target lifecycle definition | SKIP FOR NOW |

## Source audit notes

- FrontierMath's official documentation identifies Tiers 1–3 v2 as a distinct benchmark and records the 2026-06-12 update, including corrected and removed problems.
- ARC Prize describes ARC-AGI-2 as a new 2025 benchmark and specifies its two-output scoring rule for each task.
- Aider's official announcement dates the Polyglot benchmark to 2024-12-21 and defines its fixed 225-exercise, six-language set.
- The OSWorld official site dates OSWorld 2.0 to 2026-06-26 and describes it as a new version with official unified evaluations.
- Terminal-Bench's official announcement dates version 2.0 to 2025-11-07 and documents the versioned benchmark and Harbor harness.
- Cognition's FrontierCode 1.1 resource defines a distinct software-quality measurement object rather than a plain unit-test pass rate.
- Agents' Last Exam's official leaderboard and paper define ALE-V1 pass rate separately from partial-credit score; this snapshot uses the overall pass-rate leaderboard.
- Terminal-Bench-Science's official 0.1 announcement defines 70 scientific workflow tasks, three independent trials per task, and a continuous future release process; only the fixed 0.1 snapshot is represented here.
- The latest official 0.1 leaderboard refresh adds GLM 5.3 + Claude Code at 8.1%. It does not yet publish Terminal-Bench-Science results for Claude Fable 5.1 or GPT-6 Astra, so those releases are represented as release-only reference-panel anchors rather than fabricated benchmark observations.
- TerminalWorld's official Verified leaderboard defines a 200-task manually verified subset evaluated with the standardized Terminus-2 agent framework and Harbor harness.
- Terminal-Bench's official 2.1 announcement defines a separate revision of 2.0 with 28 task fixes; it is not merged with the existing 2.0 object.
- Terminal-Bench's v4.0.0 release is represented as a separate tagged object; its official partner leaderboard reports a 66-task resolution-rate setup and warns against comparing scores with earlier versions.
- Scale AI's HLE leaderboard identifies the finalized 2,500-question object; the curated release date is the finalization/update date rather than the earlier HLE-preview date.
- Cursor's official CursorBench page dates the 3.2 task release to 2026-07-08 and reports score, token, step, and cost columns; costs are retained as source-context observations.
- Artificial Analysis defines GDPval-AA v2 as an agentic, pairwise-judged Elo evaluation; because Elo has no fixed floor/ceiling, normalized progress and threshold timings are not computed.
- Zapier's AutomationBench repository distinguishes its public 600-task set from the official held-out private leaderboard; this snapshot uses the reproducible public set and labels that choice in observation notes.
- ScreenSpot-Pro's official leaderboard documents greedy decoding and micro-average reporting; the curated direct-grounding series excludes agentic multi-step and zoom-assisted variants so the capability frontier does not mix materially different setups.

ARC-AGI-1 remains in the queue because the current authoritative source establishes a 2019 origin but not a precise day-level release date suitable for the present schema.

## Model-panel implication

The new rows add model-generation probes already present in the curated exports. They do not turn the project into a model catalog. A later panel audit should consolidate near-duplicate model snapshots and assign stable family roles, especially for agent benchmarks where the agent scaffold is part of the measurement protocol.

## Current frontier release-resource audit

The current frontier release audit covers seven explicit panel anchors across the seven independent frontier organizations in the panel: Claude Fable 5.1, GPT-6 Astra, Gemini 3.8 Flash, DeepSeek-V4-Pro-0813, Qwen3.8-Max, Llama 4 Maverick, and Grok 4.6. Each anchor has a canonical release/model resource in the generated registry; a release-only anchor does not imply that a benchmark score exists. GLM-5.3 remains represented by its Terminal-Bench-Science score resource rather than being added as an eighth panel organization.

- Claude Fable 5.1 is represented where a curated score is available for ARC-AGI-2, FrontierMath Tiers 1–3 (v2), FrontierCode 1.1, CursorBench 3.2, and GDPval-AA v2. Its model records now point to Anthropic's official Claude Fable release page in addition to the score source.
- GPT-6 Astra is represented where a curated score is available for GPQA Diamond and FrontierMath Tiers 1–3 (v2). Its model records now point to OpenAI's official GPT-6 Astra model page in addition to the score source. A separate release-only panel record is retained for coverage checks until an authoritative score is published.
- No score is synthesized for a benchmark without an authoritative result. The absence of a new-model observation is retained as missing evidence rather than treated as a zero.
