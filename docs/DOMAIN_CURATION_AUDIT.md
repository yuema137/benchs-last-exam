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

The batch adds 11 measurement objects, not 11 model variants. Scores remain linked to their canonical observation/resource records, and thresholds remain `Unknown` or right-censored when the evidence does not support a crossing.

## Deferred candidates

AgentBench, WebArena, Mind2Web, WebShop, ALFWorld, InterCode, AppWorld, and AndroidWorld remain in the queue for a subsequent pass. Their SciEval cards are useful discovery evidence, but this repository does not yet have a sufficiently clean, source-linked score export for each candidate. They should be added when canonical observations and model release dates can be reconciled without hand-entered chart values. BFCL V4 remains deferred until its dynamic leaderboard rows can be captured as a stable model-release-date export; its fixed evaluator checkpoint is documented in the queue.

## Curation notes

Benchmark-family variants remain separate measurement objects only when their task set or scoring protocol is materially different. A family version is not counted as independent domain coverage. Rolling benchmarks remain deferred because their target changes over time and therefore do not fit the fixed benchmark-release → model-release capability timeline without another methodology.

Citation counts are not hard-coded into the leaderboard. When used for a future admission decision, record the count, index/source, and `checked_at` date next to the candidate. New benchmarks may instead qualify through repeated official adoption by major model developers.
