# Curation Queue

This is a shortlist of candidates that may be valuable, but are not yet part
of the curated leaderboard. A candidate is not added until its benchmark
version, release date, scoring protocol, and model-generation observations are
source-backed.

## Strong candidates requiring additional source work

| Candidate | Reason to include | Current hesitation | Recommendation |
|---|---|---|---|
| MMLU-Pro | Important harder successor to MMLU with broad model-report usage | Initial six-point mini-leaderboard series is now included; expand only with matching prompt/protocol evidence | Review trajectory and protocol scope |
| IFEval | Canonical verifiable instruction-following evaluation | Need a stable version and comparable model-generation results | Human review |
| SimpleQA | Important frontier factuality benchmark | The available local export is SimpleQA Verified, a distinct 1,000-question object | Added as SimpleQA Verified; keep original SimpleQA separate |
| HealthBench | High-value physician-rubric health evaluation | Overall, Consensus, and Hard are separate variants; current core uses the overall score series | Added to core; review variant coverage |
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
| HealthBench | High-value physician-rubric health evaluation | Official page exposes methodology and model set, but a checked-in comparable score table still needs extraction | Add when the official score series is captured |
| MMMU / MMMU-Pro | Important multimodal academic reasoning objects | Official leaderboard is interactive and variants/splits need separate checked-in observations | Add after extracting a stable score series |
| IFEval | Canonical verifiable instruction-following evaluation | Need a stable source-backed model-generation series | Add after source audit |
| HumanEval | Canonical historical coding benchmark | Need a clean comparable multi-date score series | Add after source audit |
| BigCodeBench | More realistic code-generation tasks than HumanEval | Protocol/configuration and score series need audit | Add after source audit |

## Do not add for now

Rolling benchmarks such as LiveBench and LiveCodeBench remain deferred. Their
task pools change over time, so the current fixed-object capability-lifetime
definition does not apply without a separate rolling-benchmark methodology.
