#!/usr/bin/env python3
"""Produce a forensic audit of the dates used for MATH Level 5 plotting."""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/math_level_5.csv"
AUDIT_DIR = ROOT / "data/audits"
CSV_OUT = AUDIT_DIR / "math_level5_time_observations.csv"
REPORT_OUT = ROOT / "MATH_LEVEL5_TIME_AUDIT.md"
BENCHMARK_RELEASE = "2021-03-05"
EPOCH_URL = "https://epoch.ai/benchmarks/math-level-5"


def main():
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    with RAW.open(newline="") as handle:
        rows = list(csv.DictReader(handle))

    diagnostics = []
    for row in rows:
        model_release = row.get("Release date") or None
        evaluation = (row.get("Started at") or "")[:10] or None
        if evaluation:
            plotting_date, reason = evaluation, "Current build_snapshot.parse_date prefers Started at"
        elif model_release:
            plotting_date, reason = model_release, "Current build_snapshot.parse_date falls back to Release date"
        else:
            plotting_date, reason = None, "No usable date; current snapshot excludes this observation"
        diagnostics.append({
            "model": row.get("Model version") or "",
            "score": row.get("Best score (across scorers)") or "",
            "source": EPOCH_URL,
            "benchmark_version_protocol": "MATH Level 5 / Epoch standardized task; row-level protocol not present in CSV",
            "benchmark_release_date": BENCHMARK_RELEASE,
            "model_release_date": model_release or "Unknown",
            "evaluation_date": evaluation or "Unknown",
            "result_public_date": "Unknown",
            "source_publication_date": "Unknown",
            "plotting_date_current": plotting_date or "Unknown",
            "plotting_date_reason": reason,
            "retrospective": "yes",
            "historical_frontier_eligible": "no",
            "eligibility_reason": "No defensible result-public date or row-level comparable protocol; Epoch export is treated as retrospective standardized evaluation",
            "temporal_interpretation": "Retrospective Epoch internal run; contemporaneous public result not established",
            "protocol_evidence": "Epoch benchmark methodology page; CSV score column is Best score (across scorers)",
        })

    fields = list(diagnostics[0])
    with CSV_OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(diagnostics)

    plot_dates = Counter(row["plotting_date_current"] for row in diagnostics)
    model_dates = Counter(row["model_release_date"] for row in diagnostics)
    top = max(diagnostics, key=lambda row: float(row["score"]))
    lines = [
        "# MATH Level 5 Time Audit",
        "",
        "Status: forensic audit plus MATH semantic correction; visualization behavior is intentionally limited to separating historical and retrospective points.",
        "",
        "## Executive finding",
        "",
        "The current site does not plot MATH Level 5 on result-publication time. Its current `build_snapshot.py` date policy uses `Started at` first and `Release date` second. Every one of the 108 rows has both fields, so all 108 current plotting dates use `Started at`, not a model-release fallback.",
        "",
        "The dates describe Epoch evaluation runs. They do not establish when each score first became publicly available. Therefore the current MATH Level 5 curve is an Epoch retrospective evaluation trajectory ordered by run start, not a historical public-result frontier. T50/T90 computed from it must not yet be interpreted as historical benchmark lifetime metrics.",
        "The prior snapshot reported T50 = 46.8 months and T90 = 46.8 months because both thresholds were crossed by the same clustered evaluation-time frontier event. That was an artifact of the operational evaluation timeline, not evidence that the benchmark crossed both historical lifecycle thresholds on that date.",
        "",
        "## Findings",
        "",
        f"- Raw rows: **{len(rows)}**.",
        f"- Benchmark release date used by the registry: **{BENCHMARK_RELEASE}**, from the [MATH paper](https://arxiv.org/abs/2103.03874). The paper was submitted on 2021-03-05 and introduces the 12,500-problem MATH dataset.",
        f"- Rows with model release date: **{sum(bool(row['model_release_date'] != 'Unknown') for row in diagnostics)}**; distinct model-release dates: **{len(model_dates)}**.",
        f"- Rows with evaluation/run start date: **{sum(bool(row['evaluation_date'] != 'Unknown') for row in diagnostics)}**; distinct run-start dates: **{len({row['evaluation_date'] for row in diagnostics})}**.",
        f"- Rows using the current plotting date from `Started at`: **{sum(row['plotting_date_reason'].startswith('Current build_snapshot.parse_date prefers') for row in diagnostics)}**.",
        f"- Rows using model-release fallback: **{sum(row['plotting_date_reason'].startswith('Current build_snapshot.parse_date falls back') for row in diagnostics)}**.",
        f"- Rows with unknown result-public date: **{sum(row['result_public_date'] == 'Unknown' for row in diagnostics)}**; the export has no row-level public-result field or source-publication date.",
        f"- Most concentrated plotting date: **{plot_dates.most_common(1)[0][0]} ({plot_dates.most_common(1)[0][1]} rows)**.",
        f"- Highest observed score: **{float(top['score'])*100:.2f}%**, model `{top['model']}`, model release `{top['model_release_date']}`, evaluation start `{top['evaluation_date']}`.",
        "",
        "## Why the vertical cluster occurs",
        "",
        "The current code's `parse_date()` returns `Started at` before `Release date`. Epoch's MATH Level 5 export contains many standardized internal evaluation runs started on the same date, especially 2025-01-27. Those observations therefore share one x-coordinate even though their model release dates differ. The run date is useful for an evaluation-operation view, but it is not a public-result date. The corrected snapshot keeps these rows as retrospective observations and excludes them from the historical lifecycle frontier.",
        "",
        "The raw observations are not deleted or reordered in this audit. The diagnostic export preserves both model-release and evaluation-run dates so the same rows can later support separate views.",
        "",
        "## What the 98.1% score means",
        "",
        f"The maximum currently used by the site is from `{top['model']}` with raw score `{top['score']}`. The source row has model release date `{top['model_release_date']}` and Epoch run start `{top['evaluation_date']}`. Its source in the current canonical snapshot falls back to the Epoch MATH Level 5 methodology page: {EPOCH_URL}.",
        "",
        "The Epoch methodology page says MATH Level 5 is the 1,324-question Level 5 subset and that Epoch uses a fixed prompt plus three scorers; its plots use `model_graded_equiv` unless otherwise noted. The downloaded CSV column used here is `Best score (across scorers)`, so this particular derived value is not automatically identical to the default Epoch plot metric. This audit therefore treats the score as an Epoch-export observation whose exact row-level scorer choice must be retained before cross-source merging.",
        "",
        "## Comparability conclusion",
        "",
        "The original MATH paper and Epoch's later standardized internal runs are not demonstrated to be apples-to-apples by this export alone. The CSV does not provide a row-level protocol ID, result-public date, or source-publication date. Differences may include prompt/output format, answer extraction, scorer, decoding, and reporting context. The current implementation must not silently combine these rows with contemporaneous 2021 public MATH Level 5 results into one historical frontier.",
        "",
        "## Proposed date semantics",
        "",
        "```text",
        "historical_frontier_date = first defensible public date of this score",
        "model_generation_date    = model release date",
        "evaluation_date          = actual evaluation/run date",
        "```",
        "",
        "For the historical benchmark-lifecycle curve and T50/T90, use `historical_frontier_date`. If it cannot be established, keep the date unknown and exclude the observation from that curve rather than substituting model release or evaluation date. Use `model_generation_date` for a separate standardized capability-by-generation view and `evaluation_date` for evaluation-operation analysis. In the current corrected snapshot, MATH Level 5 therefore reports T50/T90 as `Unknown`.",
        "",
        "## Diagnostic artifacts",
        "",
        f"- Full row-level diagnostic table: `{CSV_OUT.relative_to(ROOT)}`.",
        "- The table includes model, score, source, benchmark/protocol note, all available date fields, current plotting date, selection reason, retrospective classification, historical-frontier eligibility, and protocol evidence.",
        "- The corrected snapshot excludes these retrospective rows from historical lifecycle metrics; the frontend renders them as a separate marker layer.",
        "",
        "## Source notes",
        "",
        f"- [MATH original paper](https://arxiv.org/abs/2103.03874)",
        f"- [Epoch MATH Level 5 methodology]({EPOCH_URL})",
        "- The local raw export is `data/raw/math_level_5.csv`; it contains 108 rows and no row-level `Source`, `Source link`, or result-publication field.",
    ]
    REPORT_OUT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {REPORT_OUT} and {CSV_OUT}")


if __name__ == "__main__":
    main()
