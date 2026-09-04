# Domain curation audit — expansion batch

Checked 2026-09-03. This batch favors established benchmarks with curated raw score exports already present in BLE and a defensible primary paper or project page. Citation/adoption is curation evidence, not a leaderboard value; counts should be refreshed from the cited index before the next expansion.

| Benchmark | Type / domain | Canonical release | Evidence and lifecycle value | Decision |
|---|---|---:|---|---|
| BIG-Bench Hard | Model / General knowledge & reasoning | 2022-10-17 | Canonical 23-task hard-reasoning suite; arXiv 2210.09261; multi-generation exports | ADD |
| ScienceQA | Model / Science | 2022-09-19 | Widely used multimodal science QA; official project and paper; score series present | ADD |
| HellaSwag | Model / General knowledge & reasoning | 2019-05-20 | Classic commonsense continuation benchmark with long model history | ADD |
| PIQA | Model / General knowledge & reasoning | 2019-11-26 | Canonical physical-commonsense evaluation with a stable binary metric | ADD |
| TriviaQA | Model / General knowledge & reasoning | 2017-05-09 | Long-running open-domain QA benchmark with exact-match reporting | ADD |
| SuperGLUE | Model / General knowledge & reasoning | 2019-05-01 | Canonical multi-task language understanding suite; aggregate semantics documented | ADD |
| CyBench | Agent / Cybersecurity | 2024-08-01 | Open cybersecurity agent benchmark with environment outcomes and official project page | ADD_WITH_PARTIAL_DATA |
| DeepResearch Bench | Agent / General agent tasks | 2025-06-13 | SciEval card and arXiv 2506.11763 define 100 research tasks and RACE/FACT scoring | ADD_WITH_PARTIAL_DATA |
| SciCode | Agent / Science & research | 2024-07-18 | SciEval card and arXiv 2407.13168; executable scientist-curated coding tasks | ADD |
| SpatialViz-Bench | Model / Multimodal | 2024-09-19 | Four stable visual-spatial subskills and a multi-model raw export | ADD_WITH_PARTIAL_DATA |
| Vending-Bench 2 | Agent / General agent tasks | 2025-05-01 | Long-horizon simulated business outcome; useful but sparse evidence | ADD_WITH_PARTIAL_DATA |
| TheAgentCompany | Agent / General agent tasks | 2024-10-01 | Simulated software-company workflows with browser, office, communication, and coding tools; 50-row public export across multiple model families | ADD |
| DeepSWE v1.1 | Agent / Software engineering | 2026-04-01 | Repository-level long-horizon coding evaluation with a fixed mini-SWE-agent export, multiple families, and reported cost | ADD |
| FrontierSWE V2 | Agent / Software engineering | 2026-07-01 | 34-task Mean@5 composite benchmark with separate implementation, performance, and research-quality dimensions | ADD |
| ScienceAgentBench | Agent / Science & research | 2024-10-07 | 102 expert-validated scientific discovery tasks; HAL exposes verified accuracy across 16 models and two scaffolds | ADD |
| MLE-bench | Agent / Science & research | 2024-10-10 | 75 fixed Kaggle-style ML engineering competitions with official AIDE baselines across four model generations | ADD |
| PaperBench | Agent / Science & research | 2025-04-02 | 20 ICML paper-replication tasks with 8,316 rubric outcomes and an official BasicAgent model series | ADD |
| MMMU | Model / Multimodal | 2023-12-04 | Canonical college-level multimodal reasoning benchmark with official validation results across major model families | ADD |
| MMMU-Pro | Model / Multimodal | 2024-09-05 | Fixed harder MMMU variant with Standard-10 and Vision settings; official release table keeps the combined metric explicit | ADD |
| BFCL V4 | Agent / Tool use | 2025-07-17 | Official fixed evaluator checkpoint, explicit overall-accuracy composition, and distinct FC/Prompt modes | ADD_WITH_PARTIAL_DATA |
| HumanEval | Model / Coding | 2021-07-07 | Canonical function-level code generation benchmark with executable hidden tests and a long model-generation history | ADD |
| BigCodeBench | Model / Coding | 2024-06-18 | 1,140 practical function tasks across diverse libraries; official Complete calibrated Pass@1 leaderboard | ADD |
| AssistantBench | Agent / General agent tasks | 2024-07-23 | Fixed 214-task web research benchmark; the HAL Browser-Use verified export provides eight dated results across OpenAI, Anthropic, and Google. Official resources: [project page](https://assistantbench.github.io/) and [HAL leaderboard](https://hal.cs.princeton.edu/assistantbench) | ADD_WITH_PARTIAL_DATA |
| BALROG | Agent / General agent tasks | 2024-11-20 | ICLR 2025 benchmark spanning six interactive game environments; official leaderboard provides a multi-generation Average progress series | ADD |
| GSO | Agent / Software engineering | 2025-05-29 | Fixed repository-level performance-optimization tasks with precise runtime tests and expert targets; official leaderboard export provides comparable Opt@1 rows | ADD_WITH_PARTIAL_DATA |
| METR Time Horizon 1.1 | Agent / Science & research | 2026-01-29 | Standardized long-horizon software/research task suite with a 50% human-equivalent time-horizon metric; percentage lifecycle thresholds are explicitly N/A | ADD_WITH_PARTIAL_DATA |
| ExploitBench | Agent / Cybersecurity | 2026-05-18 | Capability-ladder cybersecurity benchmark with a fixed public snapshot and separate base-harness / AutoNudge results; this batch keeps only base-harness rows | ADD_WITH_PARTIAL_DATA |
| ProofBench v1.1 | Model / Mathematics | 2026-08-14 | Formal theorem proving with Lean 4 kernel verification; Vals AI's v1.1 re-grade is modeled separately from v1.0-era results | ADD_WITH_PARTIAL_DATA |
| DTBench | Model / General knowledge & reasoning | 2026-08-12 | 407 handcrafted decision-theory multiple-choice questions reported as a distinct component of the Conceptual Reasoning Index; the aggregate CRI and attitude questions are excluded | ADD_WITH_PARTIAL_DATA |
| APEX-Agents | Agent / General agent tasks | 2026-01-20 | Fixed 480-task professional-work benchmark across banking, consulting, and legal workflows; the public leaderboard reports Pass@1 across multiple agent/model generations | ADD_WITH_PARTIAL_DATA |
| OpenBookQA | Model / Science | 2018-09-07 | Canonical fixed four-choice open-book science QA with a long model-generation record; the open-book facts and commonsense requirement are kept explicit | ADD |
| BoolQ | Model / General knowledge & reasoning | 2019-05-24 | Canonical fixed yes/no reading-comprehension benchmark with supporting passages and a large longitudinal score export | ADD |
| EEBench | Agent / Engineering | 2026-08-01 | Official electrical-engineering agent leaderboard with fixed Score (%) semantics, model/harness context, and reported cost/task; current snapshot has five dated results across four reference organizations | ADD_WITH_PARTIAL_DATA |
| PHYBench | Model / Physics | 2025-04-22 | Fixed 500-problem physics benchmark with separate Accuracy and EED metrics; this card keeps Accuracy and has a multi-family public trajectory | ADD |
| PHYSICS | Model / Physics | 2025-03-26 | Fixed 1,297 university-physics problems with automatic verification and a standardized ScienceEval cross-model panel | ADD |
| CompBioBench v1 | Agent / Life Science | 2026-04-09 | Fixed 100 computational-biology tool/code tasks with results from Codex CLI, Gemini CLI, and Claude Code; system-level setup remains explicit | ADD_WITH_PARTIAL_DATA |
| LLM-MSE-MCQs | Model / Materials Science | 2024-09-22 | Fixed 113-question materials multiple-choice subset with ScienceEval's standardized eight-sample pass@1 panel; other LLM-MSE datasets are excluded | ADD |
| EngDesign-Open | Agent / Engineering | 2025-07-01 | Fixed 67-task open engineering-design subset with simulation/rubric evaluation; headline Average Score is kept separate from iterative Average Pass Rate | ADD |
| SWE-bench Science | Agent / Engineering | 2026-08-20 | Fixed 119-task scientific-software repository benchmark with official Overall Pass@1 leaderboard and harness provenance | ADD_WITH_PARTIAL_DATA |
| RoboBench | Model / Engineering | 2025-10-23 | Official Perception Reasoning average provides a distinct robotics/embodied reasoning series; other dimensions remain separate | ADD_WITH_PARTIAL_DATA |

The current expansion batches add 27 measurement objects, not 27 model variants. Scores remain linked to their canonical observation/resource records, and thresholds remain `Unknown`, right-censored, or N/A when the evidence or metric does not support a crossing.

## Deferred candidates

AgentBench, WebArena, Mind2Web, WebShop, ALFWorld, InterCode, AppWorld, and AndroidWorld remain in the queue for a subsequent pass. Their SciEval cards are useful discovery evidence, but this repository does not yet have a sufficiently clean, source-linked score export for each candidate. HiPhO, Qiskit HumanEval, MaterialBENCH, TUA-Bench, and Material Discovery Bench remain deferred because their fixed version or headline protocol is not yet cleanly separable. EEBench remains partial because its first public benchmark date is not explicit on the current official page; the current snapshot records the official leaderboard snapshot date as a documented release proxy. They should be revisited when canonical dates and model release metadata can be reconciled without hand-entered chart values. BFCL V4 is now included using a small fixed-checkpoint export; the wider live leaderboard remains outside this snapshot.

## Curation notes

Benchmark-family variants remain separate measurement objects only when their task set or scoring protocol is materially different. A family version is not counted as independent domain coverage. Rolling benchmarks remain deferred because their target changes over time and therefore do not fit the fixed benchmark-release → model-release capability timeline without another methodology.

Citation counts are not hard-coded into the leaderboard. When used for a future admission decision, record the count, index/source, and `checked_at` date next to the candidate. New benchmarks may instead qualify through repeated official adoption by major model developers.
