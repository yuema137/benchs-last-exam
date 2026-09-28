# Repository and September 2026 benchmark audit

Audit date: **2026-09-27**. New-work window: **2026-09-14 through 2026-09-27**, inclusive. English-only dated audit snapshot, as allowed by `AGENT.md`.

## Architecture and audit findings

The repository is a small static knowledge base, with no backend. Its source-to-publication path is:

```text
data/benchmarks/*.json + data/raw/*.csv
  → src/benchmark_observatory/registry.py (typed registry validation)
  → scripts/build_snapshot.py (identity, normalization, frontiers, lifecycle)
  → data/evidence.jsonl, observations.jsonl, models.json, resources.json
  → site/data/benchmarks.json (tracked complete validation snapshot)
  → site/data/index.json + benchmarks/<id>.json + resources.json (generated runtime)
  → site/app.js (static UI, lazy detail loading)
```

The build discovers every typed card; four lifecycle views are derived together. Tests and standalone validators check units, dates, provenance, registry integration and the public bundle. The publication script builds a static Pages bundle; this update does not deploy it.

Findings:

- The baseline contains 158 cards; 166 after this update. Benchmark declarations are separate from computation and the UI. No architectural rewrite is needed.
- Baseline evidence predates these releases. A benchmark-centric, representative update is appropriate; the repository is not a model-complete leaderboard.
- Existing auxiliary-series rendering supports protocol separation, but ingestion only had a CyBench-specific branch. Added a small explicit CSV metadata mechanism, with validation before duplicate merging. Auxiliary rows now also stay out of organization coverage and cost summaries, preventing indirect lifecycle changes.
- The integration gate now permits an explicitly documented unknown canonical frontier when no eligible canonical observations exist. The UI renders auxiliary-only and numeric auxiliary curves, with separate source-linked observation details; it never promotes them into headline metrics.
- Existing HLE CSV rows contain unquoted comma overflow. New columns are prefixed rather than appended, preserving every old parsed field, overflow cell and evidence ID. No legacy scores or raw fields were repaired or overwritten in this update. The existing MMMU overflow was left untouched.
- The earlier GPT-6 audit is a dated snapshot; its OSWorld wording is not the current partial-reward measurement definition. Current typed card definitions control this update.
- Reference model panels remain versioned. This change adds measurement probes without retroactively replacing historical reference-panel anchors.

## Changes

Imported **238 source observations across 24 cards**: **160 canonical** and **78 auxiliary**. Eight cards are new: six within the window, plus two older measurement objects needed for release-score coverage. All new cards have English and Chinese copy.

Primary model sources: [Claude Opus 5.5 release](https://www.anthropic.com/claude-opus-5-5/), [full system card](https://www.anthropic.com/claude-opus-5-5-system-card/), [GPT-6 Sol/Luna release](https://openai.com/index/introducing-gpt-6-sol-and-luna/), [September 22 system-card appendix](https://deploymentsafety.openai.com/gpt-6-astra), [Grok 4.7](https://x.ai/news/grok-4-7), and [MiMo original model-card commit](https://huggingface.co/XiaomiMiMo/MiMo-V2.6-Pro-RL/blob/c165b4c7d1936ec55425c029597f414f84bd5d34/README.md). All usable effort points from Anthropic’s five tracked release charts are retained, not just the largest score.

| New card | First public date | Measurement boundary |
|---|---|---|
| [CADWorld v1](https://arxiv.org/abs/2609.16251v1) | 2026-09-14 | Full 200-task success; seven model runs; expert reference excluded. |
| [BLINDSPOT v1 · Safety calibration](https://arxiv.org/abs/2609.16305v1) | 2026-09-14 | SCS safety–utility composite, not plain accuracy; all 13 model rows. |
| [ERPBench (state-grounded) v1 · T1](https://arxiv.org/abs/2609.17885v1) | 2026-09-15 | T1 only, six systems. Distinct from the GAIR ERPBench market-simulation paper. |
| [Akita coding benchmark v4 · Vigilance](https://akitaonrails.github.io/en/2026/09/15/new-llm-benchmark-v4-retesting-39-llms-part-2/) | 2026-09-15 | 39 author-audited model/harness rows. Single application and single-run results, including author-marked harness/artifact caveats. |
| [ShowAndTell v1 · Comprehension (AEI)](https://github.com/bracketthq/showAndTell-arena/tree/cd70351a3244bb3d433ffd72bc46406741b1bf2a) | 2026-09-15 | Official initial commit September 15; press announcement September 16. Only preliminary workbook grades exist: all three system scores auxiliary; canonical frontier Unknown. |
| [WhatWorkedBench v1 · Four-factor B=8](https://arxiv.org/abs/2609.27490v1) | 2026-09-23 | Table 2, d=4 B=8 family-macro recovery; four model/cohort rows. B=4, six-factor and post-hoc estimator results excluded from this card. |
| [CursorBench 4.0](https://cursor.com/cursorbench) | 2026-09-10 | Outside discovery window; added to separate new model results from CursorBench 3.2. |
| [Chartography v1 · No tools](https://arxiv.org/abs/2608.10677) | 2026-08-11 | Outside discovery window; supplemental release-score coverage. No-tools canonical; tools auxiliary; judge explicitly pinned. |

Canonical frontier changes (scores below are percentages, rounded here only):

| Card | Before | After |
|---|---:|---:|
| EEBench | 61.60 | 64.00 |
| FrontierCode 1.1 | 53.48 | 54.64 |
| Terminal-Bench 2.1 | 79.10 | 89.90 |
| Terminal-Bench 4.0 | 57.90 | 66.40 |
| Humanity's Last Exam | 57.20 | 67.70 |
| DeepSWE v1.1 | 73.83 | 74.20 |
| FrontierSWE V2 | 56.29 | 62.30 |

## Protocol and evidence decisions

- OSWorld: Anthropic’s September 10 task assets and context-compaction protocol stay auxiliary; the OpenAI August 8 offline partial-reward score matches the existing card. Strict success is not substituted for partial reward.
- AutomationBench: private held-out 1.0.6 is isolated from the public 600-task series. MiMo split/fallback details remain unpinned and get their own auxiliary series.
- GDPval-AA: v2.1 changes the calibration to a 1600 anchor; all v2.1 evidence remains numeric Elo in an auxiliary series under the existing v2 card. Grok’s version-unpinned rating is separately isolated.
- BenchCAD: Anthropic uses a random 1,000-file, 256px subset; it does not update the full canonical leaderboard.
- HealthBench: original-paper scores, Anthropic’s Opus 4.8 grader, and OpenAI’s September 22 configuration remain separate. Imported OpenAI values are the raw numbers inside parentheses, not length-adjusted headlines. The Astra correction is preserved in new evidence; no old row is overwritten. Professional, Hard and Consensus are not overall HealthBench.
- Toolathlon: Anthropic’s patched environment and MiMo’s unpinned environment are each auxiliary.
- ExploitGym: Anthropic’s exact 289/869 and 300/869 successes (2h/6h) differ from the canonical 898-task paper. OpenAI and MiMo task sets/time budgets are insufficiently pinned and remain auxiliary.
- HLE: tools and no-tools are separate. Chartography: tools and no-tools are separate, with the new judge recorded.
- Akita: the 94-point Nex result has an uncommitted-artifact caveat; Gemini 3.1 Pro’s low score has a harness-failure caveat. These are system/harness observations, not isolated model ability; no billing comparisons are imported.
- ShowAndTell: workbook grades explicitly described by the authors as non-canonical are all auxiliary. There is no invented full AEI value, confidence interval or model version. The new card has an unknown canonical frontier.
- WhatWorkedBench: the API aliases do not establish exact model checkpoints. The additional cohort ran September 14–15; no per-model day is invented.
- MiMo: September 21 result publication is verified against the original README commit, not inferred from the collection crawl or ingestion date. Model release dates remain unknown.

## Reconciliation and limitations

The machine-readable [source inventory](../data/audits/september_2026_source_inventory.json) records `UPDATED`, `EXTRACTION_FAILED`, `SKIPPED_WITH_REASON` and `NOT TRACKED` dispositions. `ALREADY CURRENT` is reserved for exact source/configuration matches; no such claim is needed for the newly imported release observations. [Added observations](../data/audits/september_2026_added_observations.json) gives every accepted score, model, source and role.

OpenAI’s release charts did not expose exact arrays in the readable page; direct fetch returned HTTP 403 and no browser surface was available. Exact prose/table values were imported, but the remaining chart-only points are explicitly extraction failures. No absence from a text extractor is described as “no published result.”

Discovery included paper/project pages, model release materials and benchmark announcements. RLE-Bench and AgentActionBench predate the window; Real-SWE’s exact first date was not verified. MLPerf releases measure hardware performance. The political-bias announcement did not establish a compatible capability metric. These exclusions are recorded rather than represented by speculative cards. This is a bounded source review, not a claim to enumerate every paper published worldwide.

## Lifecycle and validation

The observation-derived snapshot advances from 2026-09-04 to 2026-09-23. The audit date is September 27; snapshot time is still computed from source dates according to existing repository policy.

| Lifecycle view | Added members | Removed members |
|---|---|---|
| test-of-time | cfdcodebench-v1-zeroshot, matcha-v1-zeroshot, mmmu-pro | None |
| still-frontier | cadworld-v1 | None |
| fastest-solved | None | None |
| recently-saturated | akita-v4-vigilance, blindspot-v1-scs, erpbench-state-v1-t1 | None |

All four memberships, including non-membership, are independently recomputed by the integration validator. Runtime index/detail/resource files are rebuilt together; no UI data was hand-edited.

Validation commands:

```bash
python3 scripts/build_snapshot.py
python3 scripts/validate_score_semantics.py
python3 scripts/validate_provenance.py
python3 scripts/validate_benchmark_integration.py
python3 scripts/audit_observation_dates.py
python3 scripts/audit_canonical_identity.py
PYTHONPATH=src python3 -m unittest discover -s tests -v
node --check site/app.js
```

The regression suite includes high auxiliary scores that must leave canonical frontiers, thresholds, coverage, costs and every lifecycle decision unchanged, plus incomplete/conflicting metadata rejection. Original evidence IDs and raw fields were compared against HEAD and remain intact. All 81 tests pass, including Node execution of the real chart functions for numeric and auxiliary-only cards. Browser visual QA was unavailable; generated runtime parity, finite SVG geometry, static JavaScript syntax and static export are checked instead.
