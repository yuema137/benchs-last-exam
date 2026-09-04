# Domain Curation Audit

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

The existing five benchmarks remain in core: MMLU, GSM8K, MATH Level 5, GPQA Diamond, and SWE-bench Verified. This produces a ten-benchmark core without treating related versions as silently interchangeable.

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

## Model-panel implication

The new rows add model-generation probes already present in the curated exports. They do not turn the project into a model catalog. A later panel audit should consolidate near-duplicate model snapshots and assign stable family roles, especially for agent benchmarks where the agent scaffold is part of the measurement protocol.

