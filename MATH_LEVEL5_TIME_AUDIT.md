# MATH Level 5 Time Audit

Status: forensic audit plus MATH semantic correction; visualization behavior is intentionally limited to separating historical and retrospective points.

## Executive finding

The current site does not plot MATH Level 5 on result-publication time. Its current `build_snapshot.py` date policy uses `Started at` first and `Release date` second. Every one of the 108 rows has both fields, so all 108 current plotting dates use `Started at`, not a model-release fallback.

The dates describe Epoch evaluation runs. They do not establish when each score first became publicly available. Therefore the current MATH Level 5 curve is an Epoch retrospective evaluation trajectory ordered by run start, not a historical public-result frontier. T50/T90 computed from it must not yet be interpreted as historical benchmark lifetime metrics.
The prior snapshot reported T50 = 46.8 months and T90 = 46.8 months because both thresholds were crossed by the same clustered evaluation-time frontier event. That was an artifact of the operational evaluation timeline, not evidence that the benchmark crossed both historical lifecycle thresholds on that date.

## Findings

- Raw rows: **108**.
- Benchmark release date used by the registry: **2021-03-05**, from the [MATH paper](https://arxiv.org/abs/2103.03874). The paper was submitted on 2021-03-05 and introduces the 12,500-problem MATH dataset.
- Rows with model release date: **108**; distinct model-release dates: **67**.
- Rows with evaluation/run start date: **108**; distinct run-start dates: **35**.
- Rows using the current plotting date from `Started at`: **108**.
- Rows using model-release fallback: **0**.
- Rows with unknown result-public date: **108**; the export has no row-level public-result field or source-publication date.
- Most concentrated plotting date: **2025-01-27 (52 rows)**.
- Highest observed score: **98.13%**, model `gpt-5-2025-08-07_high`, model release `2025-08-07`, evaluation start `2025-10-29`.

## Why the vertical cluster occurs

The current code's `parse_date()` returns `Started at` before `Release date`. Epoch's MATH Level 5 export contains many standardized internal evaluation runs started on the same date, especially 2025-01-27. Those observations therefore share one x-coordinate even though their model release dates differ. The run date is useful for an evaluation-operation view, but it is not a public-result date. The corrected snapshot keeps these rows as retrospective observations and excludes them from the historical lifecycle frontier.

The raw observations are not deleted or reordered in this audit. The diagnostic export preserves both model-release and evaluation-run dates so the same rows can later support separate views.

## What the 98.1% score means

The maximum currently used by the site is from `gpt-5-2025-08-07_high` with raw score `0.9813066465256798`. The source row has model release date `2025-08-07` and Epoch run start `2025-10-29`. Its source in the current canonical snapshot falls back to the Epoch MATH Level 5 methodology page: https://epoch.ai/benchmarks/math-level-5.

The Epoch methodology page says MATH Level 5 is the 1,324-question Level 5 subset and that Epoch uses a fixed prompt plus three scorers; its plots use `model_graded_equiv` unless otherwise noted. The downloaded CSV column used here is `Best score (across scorers)`, so this particular derived value is not automatically identical to the default Epoch plot metric. This audit therefore treats the score as an Epoch-export observation whose exact row-level scorer choice must be retained before cross-source merging.

## Comparability conclusion

The original MATH paper and Epoch's later standardized internal runs are not demonstrated to be apples-to-apples by this export alone. The CSV does not provide a row-level protocol ID, result-public date, or source-publication date. Differences may include prompt/output format, answer extraction, scorer, decoding, and reporting context. The current implementation must not silently combine these rows with contemporaneous 2021 public MATH Level 5 results into one historical frontier.

## Proposed date semantics

```text
historical_frontier_date = first defensible public date of this score
model_generation_date    = model release date
evaluation_date          = actual evaluation/run date
```

For the historical benchmark-lifecycle curve and T50/T90, use `historical_frontier_date`. If it cannot be established, keep the date unknown and exclude the observation from that curve rather than substituting model release or evaluation date. Use `model_generation_date` for a separate standardized capability-by-generation view and `evaluation_date` for evaluation-operation analysis. In the current corrected snapshot, MATH Level 5 therefore reports T50/T90 as `Unknown`.

## Diagnostic artifacts

- Full row-level diagnostic table: `data/audits/math_level5_time_observations.csv`.
- The table includes model, score, source, benchmark/protocol note, all available date fields, current plotting date, selection reason, retrospective classification, historical-frontier eligibility, and protocol evidence.
- The corrected snapshot excludes these retrospective rows from historical lifecycle metrics; the frontend renders them as a separate marker layer.

## Source notes

- [MATH original paper](https://arxiv.org/abs/2103.03874)
- [Epoch MATH Level 5 methodology](https://epoch.ai/benchmarks/math-level-5)
- The local raw export is `data/raw/math_level_5.csv`; it contains 108 rows and no row-level `Source`, `Source link`, or result-publication field.
