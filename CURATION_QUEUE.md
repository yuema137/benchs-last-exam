# Curation Queue

This is a shortlist of candidates that may be valuable, but are not yet part
of the curated leaderboard. A candidate is not added until its benchmark
version, release date, scoring protocol, and model-generation observations are
source-backed.

## Strong candidates requiring additional source work

| Candidate | Reason to include | Current hesitation | Recommendation |
|---|---|---|---|
| MMLU-Pro | Important harder successor to MMLU with broad model-report usage | No checked-in longitudinal score series yet; must not merge with MMLU | Human review after source import |
| IFEval | Canonical verifiable instruction-following evaluation | Need a stable version and comparable model-generation results | Human review |
| SimpleQA | Important frontier factuality benchmark | The available local export is SimpleQA Verified, a distinct 1,000-question object | Added as SimpleQA Verified; keep original SimpleQA separate |
| HealthBench | High-value physician-rubric health evaluation | Model scores use a model-based grader and variants need explicit separation | Human review |
| GeneBench-Pro | Research-level scientific-agent evaluation | New benchmark with limited longitudinal coverage | Human review |
| HumanEval | Canonical historical coding benchmark | No clean local model-generation series currently checked in | Human review |
| BigCodeBench | More realistic code-generation tasks than HumanEval | Protocol/configuration and score series need audit | Human review |
| GAIA | Canonical general assistant benchmark with tools and multimodality | Version/scaffold and comparable historical scores need audit | Human review |
| BrowseComp | Important persistent web-research benchmark | Need a checked-in score series and exact no-browse/browse setup | Human review |
| τ-bench | Representative tool-agent/user interaction benchmark | Select and freeze a version before adding; τ³ must not be silently merged | Human review |
| WebArena Verified | Canonical browser-agent environment | Verified task set and harness boundary need explicit registry records | Human review |
| MMMU | Canonical multimodal academic reasoning benchmark | No checked-in score series yet | Human review |
| MMMU-Pro | Useful harder multimodal successor | Must remain separate from MMMU and needs comparable scores | Human review |
| MathVista | Important visual-mathematical reasoning benchmark | Need a fixed version and source-backed model trajectory | Human review |
| Video-MME v2 | Important video understanding successor | Local data currently represents original Video-MME, not v2 | Human review |
| LongBench v2 | Meaningful long-context reasoning benchmark | Need a fixed configuration and score series; do not merge with LongBench original | Human review |
| RULER | Canonical effective-context evaluation | Score depends strongly on context-length/configuration | Human review |

## Do not add for now

Rolling benchmarks such as LiveBench and LiveCodeBench remain deferred. Their
task pools change over time, so the current fixed-object capability-lifetime
definition does not apply without a separate rolling-benchmark methodology.
