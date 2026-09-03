# Curation Queue

These are strong candidates or unresolved choices. They are intentionally outside the current Tier A core until they add clear lifecycle value or pass a focused source/protocol audit.

| Candidate | Why it may belong | Concern / overlap | Recommendation |
|---|---|---|---|
| HumanEval | Historically canonical coding benchmark with clear execution-based scoring | Current selected export lacks a comparable historical observation file; may be saturated and overlap with SWE-bench on coding only superficially | Add after sourcing a clean historical series; do not invent dates |
| Humanity's Last Exam | Important current expert-knowledge benchmark with potentially long useful lifetime | Limited history and disputed/uncertain item quality; ceiling interpretation needs care | Candidate for later current-frontier cohort, not first core |
| ARC-AGI-1 / ARC-AGI-2 | Distinct abstract reasoning task and useful contrast with language QA | Separate task-set versions and sparse comparable model coverage | Choose one version only after version/source audit |
| MMMU | Important multimodal knowledge benchmark | Floor depends on item format; modality adds protocol comparability work | Add if it supplies a genuinely different longitudinal object |
| MathVista | Multimodal math with clear domain relevance | Overlap with MATH/GSM8K and likely thinner historical series | Keep as alternative to MMMU, not automatic addition |
| SimpleQA Verified | Factuality is an important measurement target | Grading/abstention semantics and short history | Revisit after stable grader metadata is available |
| FrontierMath | Valuable hard-math frontier probe | Private-test semantics and fixed ceiling are not yet suitable for normalized thresholds | Keep as non-normalized candidate |
| SWE-bench original vs Verified | Both have historical relevance | They are related versions, not automatically separate homepage objects | Keep Verified in core; represent original as version lineage unless lifecycle value differs |

## Tier C: do not include for now

Do not add obscure, weakly sourced, minor-variant, or nearly empty-history benchmarks merely to increase the catalog count. No exhaustive rejected list is maintained.
