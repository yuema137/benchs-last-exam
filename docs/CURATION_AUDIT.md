# Curation Audit

Status: initial curated core proposal, 2026-09-03

## Curation principle

Benchmark Observatory is curated, not comprehensive. The core set contains benchmarks that are important, interpretable, historically meaningful, currently relevant, and useful for reconstructing a longitudinal frontier. It does not attempt to collect every benchmark, model, or reported score.

## Benchmark core proposal — Tier A

| Benchmark / canonical object | Why it belongs in core | Metric and bounds | Longitudinal evidence | Lifecycle role | Confidence |
|---|---|---|---|---|---|
| MMLU (original fixed version) | Canonical broad knowledge reference used across major model evaluations; useful as an older reference whose later trajectory can show saturation and version pressure | Accuracy; random-choice floor 0.25 for four-choice items; perfect ceiling 1.0 | 215 usable dated rows in the selected Epoch export after missing-date filtering | Historically important / likely saturated | High |
| GSM8K (original fixed version) | Canonical grade-school multi-step math benchmark with clear exact-answer scoring; useful for measuring rapid capability change | Exact-match accuracy; floor 0.0; ceiling 1.0 | 162 usable dated rows in selected export | Rapidly solved / historical math trajectory | High |
| MATH Level 5 | Hard competition-math subset with a clear fixed score scale and useful contrast with GSM8K | Accuracy; floor 0.0; ceiling 1.0 | Epoch internal export provides a concentrated, dated trajectory | Rapidly solving or saturating math benchmark | High |
| GPQA Diamond | Important expert-level science reasoning benchmark; its difficult starting point and later model results make it lifecycle-informative | Accuracy; four-choice floor 0.25; perfect ceiling 1.0, with data-quality caveats | 311 dated internal-run rows in selected export | Current difficult benchmark / rapid frontier movement | High |
| SWE-bench Verified | Important coding-agent evaluation with a distinct evaluation burden and human-validated fixed subset; adds a non-static QA object | Issue-resolution rate; floor 0.0; ceiling 1.0, protocol/scaffold must be retained | 35 rows in selected export; thinner than the QA benchmarks | Agent/coding trajectory; keep protocol caveats visible | Medium-high |

Sources: MMLU original paper, GSM8K original paper, MATH original paper, GPQA original paper, the official SWE-bench Verified announcement, and the Epoch AI export. The Epoch export is used as a trusted aggregator for this first snapshot; it does not replace primary benchmark metadata.

The five objects are intentionally not five minor variants of one task. They provide historical broad knowledge, two different math regimes, expert science reasoning, and repository-level coding agents. HumanEval remains a strong candidate but is not included in this first core because the current selected source export does not contain a comparable historical file.

## Why not force a larger core

Five benchmarks are enough to exercise the intended lifecycle views without manufacturing domain balance. More benchmarks should be added only when they add a distinct measurement object or materially improve longitudinal evidence.

## Data and date policy

The current export provides model release dates and, for some internal runs, evaluation start dates. The generated snapshot uses evaluation start when available and model release date otherwise. This is explicitly provisional and is shown in the card caveat. A future curated observation may replace this with an earliest-public-availability date when the source supports it.

No score is added merely because it exists. The curated slice retains rows that can be linked to a source and placed on a defensible historical timeline; missing dates and incompatible protocol details remain validation concerns.

## Reference Model Panel — initial proposal

The first panel is deliberately small and time-aware. It is a set of probes, not a model catalog. The actual panel membership should be represented by stable family/organization roles; model snapshots are added only when they change temporal, vendor, openness, or domain coverage.

| Probe family / representative generations | Organization | Role | Relevant domains | Inclusion reason |
|---|---|---|---|---|
| GPT-4 → GPT-4o → o1-era representative | OpenAI | Historical anchor + contemporary frontier | General, math, science, coding/agents | Major capability generations and broad evaluation coverage |
| Claude 3.5/3.7 Sonnet → major current Sonnet/Opus representative | Anthropic | Historical anchor + contemporary frontier | General, math, science, coding/agents | Independent frontier probe with strong coding relevance |
| Gemini 1.5/2.x representative generations | Google | Historical anchor + contemporary frontier | General, math, science, multimodal | Independent frontier/vendor coverage |
| Llama 3.x representative generation | Meta | Historical anchor + open-weight frontier | General, math, coding | Widely used open-weight family and temporal anchor |
| DeepSeek-V3 / reasoning-era representative | DeepSeek | Open-weight frontier | Math, science, coding | Adds a strong non-US/open-weight probe when source settings are comparable |
| Qwen 2.5 representative | Alibaba | Open-weight frontier | Math, coding, multilingual/general | Adds open-weight and organizational diversity |
| One coding-agent specialist when protocol is documented | Varies | Domain specialist | Coding/agents | Included only if it adds information beyond general frontier models |

Exact model versions and dates are a second audit task. They should be selected from official model cards/technical reports and matched to the panel validity interval, not inferred from product names or current leaderboards.

## Interpretation rule

The dashboard may report a high frontier score while still showing low current coverage. Conversely, a low frontier score across several independent contemporary families is stronger evidence that the benchmark remains difficult. Coverage is evidence strength, not benchmark health.
