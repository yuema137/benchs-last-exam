#!/usr/bin/env python3
"""Adversarially validate score units without confusing baselines with bounds."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "site" / "data" / "benchmarks.json"
REPORT = ROOT / "docs" / "SCORE_ADVERSARIAL_AUDIT.md"

# Values in these groups were checked against the named primary measurement
# object. Any newly introduced <1% ratio or >100 numeric benchmark must be
# explicitly reviewed here; otherwise the acceptance gate fails instead of
# normalizing the anomaly away.
REVIEWED_LOW_RATIO_BENCHMARKS = {
    "gsm8k": "HELM exact-match results for early models genuinely include zero and sub-1% accuracy.",
    "browsecomp": "OpenAI reports 0.6% for GPT-4o and 0.9% for GPT-4.5 without browsing.",
    "frontiermath-tiers-1-3-v2": "The fixed hard-math set permits zero and one/few-item successes.",
    "frontiermath-tier-4-v2": "The research-level Tier 4 set explicitly contains zero-score model runs.",
    "arc-agi-2": "ARC Prize reports pure LLMs near zero and public reasoning systems in single digits under pass@2.",
    "critpt": "The official 70-challenge, five-run leaderboard reports several 0–0.9% accuracies.",
    "screenspot-pro": "The official micro-average leaderboard reports GPT-4o at 0.8%.",
    "gso": "The official Opt@1 export includes a zero-task-success GPT-4o run.",
    "chemm-bench-acl2026": "The pinned ACL table reports zero/near-zero exact molecular-structure task performance.",
    "tomg-bench-v1-wacc": "The official v1 leaderboard reports 0.15% weighted accuracy for Qwen2-7B under the fixed open-molecule protocol.",
    "mollangbench-v1-generation-pass1": "The v1 supplementary table reports 0.5% exact structural generation accuracy for GPT-4o; validity is a separate metric.",
}

REVIEWED_LARGE_NUMERIC_BENCHMARKS = {
    "vending-bench-2": "Simulated business outcome denominated in dollars, not percent.",
    "gdpval-aa-v2": "Unbounded Elo-like rating, not percent.",
    "metr-time-horizon-1-1": "Human-equivalent task duration in minutes, not percent.",
}


def main():
    payload = json.loads(SNAPSHOT.read_text())
    errors = []
    low_ratios = []
    baseline_undershoots = []
    large_numeric = []
    low_ratio_counts = {}
    large_numeric_counts = {}

    for benchmark in payload["benchmarks"]:
        score_format = benchmark.get("score_format", "ratio")
        baseline = benchmark.get("progress_baseline", benchmark.get("floor"))
        target = benchmark.get("progress_target", benchmark.get("ceiling"))
        hard_min = benchmark.get("hard_min")
        hard_max = benchmark.get("hard_max")
        input_unit = benchmark.get("input_unit")
        for observation in benchmark["observations"]:
            score = observation["score"]
            input_score = observation.get("input_score")
            label = f"{benchmark['id']} / {observation['model']} / {score:g}"
            if score_format == "ratio":
                if not 0 <= score <= 1:
                    errors.append(f"{label}: ratio score is outside [0, 1]")
                elif score < 0.01:
                    low_ratios.append(label)
                    low_ratio_counts[benchmark["id"]] = low_ratio_counts.get(benchmark["id"], 0) + 1
            elif score_format == "number":
                if score > 100:
                    large_numeric.append(label)
                    large_numeric_counts[benchmark["id"]] = large_numeric_counts.get(benchmark["id"], 0) + 1
            else:
                errors.append(f"{benchmark['id']}: unknown score_format {score_format!r}")

            if observation.get("input_unit") != input_unit or input_score is None:
                errors.append(f"{label}: missing or inconsistent raw input-unit lineage")
            elif input_unit == "fraction" and (not 0 <= input_score <= 1 or abs(score - input_score) > 1e-12):
                errors.append(f"{label}: fraction input does not map identically to canonical score")
            elif input_unit == "percentage_points" and (not 0 <= input_score <= 100 or abs(score - input_score / 100) > 1e-12):
                errors.append(f"{label}: percentage-point input was not converted exactly once")
            elif input_unit == "number" and abs(score - input_score) > 1e-12:
                errors.append(f"{label}: numeric input was unexpectedly converted")

            if hard_min is not None and score < hard_min:
                errors.append(f"{label}: score is below hard minimum {hard_min:g}")
            if hard_max is not None and score > hard_max:
                errors.append(f"{label}: score is above hard maximum {hard_max:g}")

            # `floor` is the normalization/reference baseline, not necessarily
            # the physical minimum. Below-chance scores are valid evidence and
            # must not be deleted or silently raised to the baseline.
            if baseline is not None and score < baseline:
                baseline_undershoots.append(label)

        if score_format == "number" and benchmark.get("normalized_progress") is not None:
            if baseline is None or target is None:
                errors.append(f"{benchmark['id']}: unbounded numeric metric has normalized progress")

    unexpected_low = set(low_ratio_counts) - set(REVIEWED_LOW_RATIO_BENCHMARKS)
    unexpected_large = set(large_numeric_counts) - set(REVIEWED_LARGE_NUMERIC_BENCHMARKS)
    if unexpected_low:
        errors.append(f"unreviewed <1% ratio benchmark(s): {sorted(unexpected_low)}")
    if unexpected_large:
        errors.append(f"unreviewed >100 numeric benchmark(s): {sorted(unexpected_large)}")

    lines = [
        "# Adversarial Score-Semantics Audit",
        "",
        f"Snapshot: `{payload['snapshot_id']}`  ",
        f"Benchmarks: {len(payload['benchmarks'])}",
        "",
        "## Gate result",
        "",
        f"- Ratio observations outside `[0, 1]`: **{sum('ratio score' in item for item in errors)}**",
        f"- Ratio observations below `1%`: **{len(low_ratios)}**",
        f"- Observations below a normalization/reference floor: **{len(baseline_undershoots)}**",
        f"- Unbounded numeric observations above `100`: **{len(large_numeric)}**",
        "",
        "`progress_baseline` is treated as a chance/reference baseline for normalized progress, not as a hard observation bound. "
        "Accordingly, a model may score below the floor without the canonical observation being invalid.",
        "",
        "Values above 100 are accepted only for `score_format: number`; examples include minutes, Elo, and simulated business outcomes. "
        "They are never formatted or normalized as percentages unless explicit finite bounds exist.",
        "",
        "## Low ratio observations (<1%)",
        "",
    ]
    for benchmark_id in sorted(low_ratio_counts):
        lines.append(
            f"- **{benchmark_id}** — {low_ratio_counts[benchmark_id]} observations. "
            f"{REVIEWED_LOW_RATIO_BENCHMARKS[benchmark_id]}"
        )
    lines.extend(["", "### Observation sample", ""])
    lines.extend(f"- {item}" for item in low_ratios[:60])
    if len(low_ratios) > 60:
        lines.append(f"- …and {len(low_ratios) - 60} more canonical low-score observations.")
    lines.extend(["", "## Large unbounded numeric observations (>100)", ""])
    for benchmark_id in sorted(large_numeric_counts):
        lines.append(
            f"- **{benchmark_id}** — {large_numeric_counts[benchmark_id]} observations. "
            f"{REVIEWED_LARGE_NUMERIC_BENCHMARKS[benchmark_id]}"
        )
    lines.extend(["", "### Observation sample", ""])
    lines.extend(f"- {item}" for item in large_numeric[:30])
    if len(large_numeric) > 30:
        lines.append(f"- …and {len(large_numeric) - 30} more numeric observations.")
    lines.extend(["", "## Interpretation", "",
                  "The low ratios are retained because their source metrics genuinely permit zero or near-zero performance. "
                  "The large numeric values are retained because their metrics are not percentages. Every observation now preserves its raw input score and explicit input unit, and the validator checks the raw-to-canonical conversion.", ""])
    REPORT.write_text("\n".join(lines))

    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"Validated score semantics for {len(payload['benchmarks'])} benchmarks: "
        f"{len(low_ratios)} low ratios, {len(baseline_undershoots)} baseline undershoots, "
        f"{len(large_numeric)} large numeric observations; no unit violations."
    )


if __name__ == "__main__":
    main()
