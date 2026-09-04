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
# Science and engineering expansion audit — 2026-09-04

This batch required at least two of the seven reference organizations to have public results for one pinned measurement object. Coverage counts organizations, not model snapshots. Alternate modalities, subsets, prompt regimes, and process metrics were not combined merely to raise coverage.

| Candidate | Type → Domain | Canonical measurement | Coverage | Decision | Main caveat |
|---|---|---|---:|---|---|
| PhysReason | Model → Physics | Full 1,200-item set; PSAS-A | 5/7 | ADD | Q+image and Q+caption conditions remain explicit. |
| OlympiadBench Physics | Model → Physics | Full multimodal Physics slice | 4/7 | ADD | Text-only experiment excluded. |
| QuantiPhy | Model → Physics | Unresolved | 5/7 | DEFER | Original and competition releases disagree on task count and checkpoint identity. |
| ChemIQ | Model → Chemistry | Final 816-question release | 3/7 | ADD | Parser-assisted DeepSeek result is identified explicitly. |
| SUPERChem (Multimodal) | Model → Chemistry | SUPERChem-500 multimodal Pass@1 | 2/7 | ADD_WITH_PARTIAL_DATA | Text-only accuracy and RPF are separate metrics. |
| ChemLLMBench | Model → Chemistry | Heterogeneous suite | ≥2/7 | DEFER | No canonical scalar metric across task families. |
| MatSciBench v2 | Model → Materials Science | v2 text-only direct/basic-CoT accuracy | 6/7 | ADD | Image, RAG, and self-correction settings excluded. |
| AtomWorld v4 | Model → Materials Science | Fixed 2,500-case full suite | 3/7 | ADD | Diagnostic subsets are not mixed with full-suite scores. |
| MatQnA objective subset | Model → Materials Science | Unpinned | 4/7 | DEFER | Prompt, extraction, and exact dataset configuration are not frozen. |
| EngiBench v2 — Level 3 | Model → Engineering | Level 3 Original average rubric score | 6/7 | ADD | Perturbed prompts and Levels 1–2 are separate objects. |
| EEE-Bench v2 | Model → Engineering | v2 overall zero-shot two-run accuracy | 4/7 | ADD | Dataset revision and GPT-4o-mini extraction procedure are material protocol fields. |
| TransportBench | Model → Engineering | Unpinned web snapshot | 4/7 | DEFER | Evaluated web-product snapshot and task count are not stable enough. |
| LABBench2 — TableQA2 PDF | Agent → Life Science | 100-task PDF/tools/high track | 3/7 | ADD | LABBench2 has no defensible all-suite composite; this card is one fixed track. |
| PG-LLM — ProteinGym | Model → Life Science | ProteinGym v1.3, N=50, seeds 1–3 | 3/7 | ADD | Recent-assay holdout uses a different aggregation and stays separate. |
| LifeSciBench | Agent → Life Science | Closed 750-task evaluation | 3/7 | DEFER | Tasks, artifacts, grader, and full run configuration are not publicly reproducible. |

The ten additions are partial or full core records. Missing cost and unreached thresholds remain explicit; they are not reasons to hide a methodologically identifiable benchmark.

## Multi-domain science and engineering expansion — 2026-09-04

This expansion applies one admission gate consistently: a fixed, named measurement object with comparable public observations from at least two of the seven reference organizations. It adds 40 objects across physics, chemistry, life science, materials, electrical, mechanical/aerospace, robotics, Earth science, energy/infrastructure, nuclear, biomedical, manufacturing, and computational engineering. Every accepted object includes bilingual task/scoring text, canonical resources, observations, a derived frontier, and automatic lifecycle-view evaluation.

| Domain | Added objects | Coverage range |
|---|---|---:|
| Physics | PhysBench Seq; OlympicArena Physics; JEEBench Physics | 2–4 / 7 |
| Chemistry | MaCBench; PSE-Bench; CheMM-Bench | 4–5 / 7 |
| Life Science | MedXpertQA Text; GMAI-MMBench v7; LAB-Bench ProtocolQA | 4–6 / 7 |
| Materials Science | OPENXRD; MatCha; OmniMatBench v2 | 5–7 / 7 |
| Electrical Engineering | ControlBench; CircuitSense; PCEval; VerilogEval v2 | 3–5 / 7 |
| Mechanical & Aerospace | APBench-γ; CADReview; TPS-CalcBench | 3–4 / 7 |
| Robotics | OpenEQA; EmbodiedBench Manipulation; OST-Bench | 3–5 / 7 |
| Earth Science | EarthSE Earth-Silver; GeoNatureAgent v5; ClimaQA-Gold | 3–7 / 7 |
| Energy & Infrastructure | FormationEval; CladBench; EnviroExam; GS-PowerFlow-100 | 3–7 / 7 |
| Nuclear Engineering | NuclearQAv2; ThermoQA v0.4 | 2–5 / 7 |
| Biomedical Engineering | MedAgentBench; MedCalc-Bench; MediConfusion | 2–6 / 7 |
| Manufacturing | FDM-Bench; iSafetyBench; Factorio Learning Environment Planning | 2–5 / 7 |
| Computational Engineering | FEABench; CFDCodeBench; FEM-Bench | 3–5 / 7 |

The domain count is not padded with incompatible variants. NRT-Bench is deferred because its canonical `ASR_CSF` is lower-is-better and the current lifecycle schema does not yet model inverse metrics safely. Sparse lifecycle crossings remain explicit rather than being fabricated.

## Seven-domain 3× expansion — 2026-09-04

This batch adds exactly three fixed measurement objects in each of seven science and engineering domains. Every object has comparable published results from at least two of the seven reference organizations; variants and alternate metrics remain separate.

| Domain | Added objects | Coverage |
|---|---|---:|
| Life Science | PubMedQA PQA-L Test 500; WMDP-Bio v1; VCT v2 Text 101 | 6/7 each |
| Chemistry | TOMG-Bench v1 wAcc; MolLangBench v1 Generation; ChemEBench Zero-shot Overall | 2–5/7 |
| Mechanical & Aerospace Engineering | DesignQA v2 Functional RAG; CADBench-Wild; AeroCopilotBench Tier 2 | 3–5/7 |
| Electrical Engineering | ChipBench v2 Verilog; CIRCUIT Zero-shot Global; PICBench Functional Pass@1 | 2–5/7 |
| Robotics | MV-RoboBench v2; Spatial457 v4 L5; EAI v3 VirtualHome Action Sequencing | 4/7 each |
| Physics | QuantiPhy Overall MRA; SeePhys Pro Level 4 Full; QCalEval April 2026 Zero-shot | 3–4/7 |
| Materials Science | MaScQA Corrected 644; MatQnA Objective; MatTools pymatgen Doc QA | 2–4/7 |

The two sub-1% observations in TOMG-Bench and MolLangBench were checked against their primary tables and added to the permanent adversarial-score gate. AeroCopilotBench excludes model labels whose release dates could not be independently pinned. All story-view membership remains derived from the rebuilt canonical metrics.
