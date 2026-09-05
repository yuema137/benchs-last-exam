#!/usr/bin/env python3
"""Validate that every active benchmark is fully connected to generated data."""

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "site" / "data" / "benchmarks.json"
APP = ROOT / "site" / "app.js"

REQUIRED_STORY_VIEWS = ("test-of-time", "still-frontier", "fastest-solved", "recently-saturated")
MONTH_DAYS = 30.44


def expected_lifecycle_decisions(benchmark, snapshot_date):
    """Independently recompute every hard-rule result from canonical metrics."""
    t50 = benchmark["threshold_days"].get("T50", {})
    t90 = benchmark["threshold_days"].get("T90", {})
    t50_days, t90_days = t50.get("days"), t90.get("days")
    progress = benchmark.get("normalized_progress")
    recent = False
    if t90.get("status") in {"reached", "at_release"} and t90_days is not None:
        release = date.fromisoformat(benchmark["release"])
        recent = 0 <= (snapshot_date - release).days - t90_days <= 3 * MONTH_DAYS
    return {
        "test-of-time": ((t50_days is not None and t50_days >= 12 * MONTH_DAYS)
                         or (t90_days is not None and t90_days >= 24 * MONTH_DAYS)),
        "still-frontier": (t50.get("status") == "right_censored" and progress is not None
                           and progress < 0.5 and benchmark["coverage"].get("status") != "low"),
        "fastest-solved": (t90.get("status") == "reached" and t90_days is not None
                           and t90_days < 6 * MONTH_DAYS),
        "recently-saturated": recent,
    }


def expected_lifecycle_views(benchmarks, snapshot_date):
    """Independently recompute memberships so stale generated tabs fail CI."""
    views = {name: set() for name in REQUIRED_STORY_VIEWS}
    for benchmark in benchmarks:
        for view, eligible in expected_lifecycle_decisions(benchmark, snapshot_date).items():
            if eligible:
                views[view].add(benchmark["id"])
    return views


def validate_benchmark(benchmark, resources, models):
    errors = []
    required = ("id", "name", "benchmark_version_id", "release", "evaluation_type", "domain",
                "summary", "task_format", "scoring", "evaluation_target", "observations",
                "frontier", "resource_ids", "coverage", "canonical_score",
                "lifecycle_eligibility")
    for field in required:
        if field not in benchmark or benchmark[field] in (None, "", []):
            errors.append(f"{benchmark.get('id', '<unknown>')}: missing {field}")
    for field in ("summary", "task_format"):
        value = benchmark.get(field, {})
        for lang in ("en", "zh"):
            if not value.get(lang):
                errors.append(f"{benchmark.get('id')}: missing {field}.{lang}")
    if not isinstance(benchmark.get("auxiliary_score_series"), list):
        errors.append(f"{benchmark.get('id')}: auxiliary_score_series must be a list")
    for resource_id in benchmark.get("resource_ids", []):
        if resource_id not in resources:
            errors.append(f"{benchmark['id']}: unresolved benchmark resource {resource_id}")
    observation_ids = set()
    observations_by_id = {}
    canonical = benchmark.get("canonical_score", {})
    if canonical.get("role") != "canonical" or not canonical.get("lifecycle_eligible"):
        errors.append(f"{benchmark.get('id')}: canonical_score must be the sole lifecycle-eligible series")
    for field in ("metric_id", "protocol_id", "score_format", "input_unit"):
        if canonical.get(field) != benchmark.get(field):
            errors.append(f"{benchmark.get('id')}: canonical_score.{field} does not match benchmark")
    for observation in benchmark.get("observations", []):
        observation_id = observation.get("observation_id")
        if not observation_id or observation_id in observation_ids:
            errors.append(f"{benchmark['id']}: missing or duplicate observation_id {observation_id}")
        observation_ids.add(observation_id)
        observations_by_id[observation_id] = observation
        if observation.get("score_role") not in {"canonical", "auxiliary"}:
            errors.append(f"{observation_id}: invalid score_role")
        if not observation.get("score_series_id"):
            errors.append(f"{observation_id}: missing score_series_id")
        if observation.get("score_role") == "canonical":
            if observation.get("metric_id") != canonical.get("metric_id"):
                errors.append(f"{observation_id}: canonical observation metric mismatch")
            if observation.get("protocol_id") != canonical.get("protocol_id"):
                errors.append(f"{observation_id}: canonical observation protocol mismatch")
        if observation.get("model_id") not in models:
            errors.append(f"{observation_id}: unresolved model")
        if not observation.get("source_ids"):
            errors.append(f"{observation_id}: no source_ids")
        for source_id in observation.get("source_ids", []):
            if source_id not in resources:
                errors.append(f"{observation_id}: unresolved source {source_id}")
    for point in benchmark.get("frontier", []):
        if point.get("observation_id") not in observation_ids:
            errors.append(f"{benchmark['id']}: frontier point is not canonical")
        if not point.get("source_ids"):
            errors.append(f"{benchmark['id']}: frontier point has no lineage")
        observation = observations_by_id.get(point.get("observation_id"), {})
        if observation.get("score_role") != "canonical":
            errors.append(f"{benchmark['id']}: auxiliary observation entered canonical frontier")
    auxiliary_ids = set()
    for series in benchmark.get("auxiliary_score_series", []):
        if series.get("role") != "auxiliary" or series.get("lifecycle_eligible") is not False:
            errors.append(f"{benchmark['id']}: auxiliary series must be lifecycle-ineligible")
        series_id = series.get("series_id")
        if not series_id or series_id in auxiliary_ids:
            errors.append(f"{benchmark['id']}: missing or duplicate auxiliary series ID")
        auxiliary_ids.add(series_id)
        for observation_id in series.get("observation_ids", []):
            observation = observations_by_id.get(observation_id)
            if not observation or observation.get("score_role") != "auxiliary":
                errors.append(f"{benchmark['id']}: invalid auxiliary observation {observation_id}")
            elif observation.get("score_series_id") != series_id:
                errors.append(f"{observation_id}: auxiliary series lineage mismatch")
    for observation in benchmark.get("observations", []):
        if observation.get("score_role") == "auxiliary" and observation.get("score_series_id") not in auxiliary_ids:
            errors.append(f"{observation.get('observation_id')}: auxiliary observation has no series definition")
    return errors


def main():
    payload = json.loads(SNAPSHOT.read_text())
    benchmarks = payload.get("benchmarks", [])
    resources = {item["id"]: item for item in payload.get("resources", [])}
    models = {item["id"]: item for item in payload.get("models", [])}
    errors = []
    ids = [item.get("id") for item in benchmarks]
    if len(ids) != len(set(ids)):
        errors.append("duplicate active benchmark IDs")
    for benchmark in benchmarks:
        errors.extend(validate_benchmark(benchmark, resources, models))
    lifecycle_views = payload.get("lifecycle_views")
    if not isinstance(lifecycle_views, dict):
        errors.append("generated lifecycle_views missing")
    else:
        benchmark_ids = set(ids)
        for view in REQUIRED_STORY_VIEWS:
            if view == "leaderboard":
                continue
            members = lifecycle_views.get(view)
            if not isinstance(members, list):
                errors.append(f"generated lifecycle view missing {view}")
                continue
            unknown = set(members) - benchmark_ids
            if unknown:
                errors.append(f"{view}: unresolved benchmark IDs {sorted(unknown)}")
            if len(members) != len(set(members)):
                errors.append(f"{view}: duplicate benchmark IDs")
        expected = expected_lifecycle_views(benchmarks, date.fromisoformat(payload["snapshot_id"]))
        for view in REQUIRED_STORY_VIEWS:
            actual = set(lifecycle_views.get(view, []))
            if actual != expected[view]:
                errors.append(
                    f"{view}: stale derived membership; missing={sorted(expected[view] - actual)}, "
                    f"unexpected={sorted(actual - expected[view])}"
                )
        snapshot_date = date.fromisoformat(payload["snapshot_id"])
        for benchmark in benchmarks:
            expected_decisions = expected_lifecycle_decisions(benchmark, snapshot_date)
            actual_decisions = benchmark.get("lifecycle_eligibility", {})
            for view, eligible in expected_decisions.items():
                if actual_decisions.get(view, {}).get("eligible") is not eligible:
                    errors.append(
                        f"{benchmark['id']}: {view} hard-rule decision is stale or missing"
                    )
        by_id = {benchmark["id"]: benchmark for benchmark in benchmarks}
        for benchmark_id in lifecycle_views.get("still-frontier", []):
            benchmark = by_id.get(benchmark_id, {})
            progress = benchmark.get("normalized_progress")
            if progress is None or progress >= 0.5:
                errors.append(
                    f"still-frontier: {benchmark_id} has normalized_progress={progress}; expected < 0.5"
                )
            if benchmark.get("threshold_days", {}).get("T50", {}).get("status") != "right_censored":
                errors.append(f"still-frontier: {benchmark_id} does not have right-censored T50")
            if benchmark.get("coverage", {}).get("status") == "low":
                errors.append(f"still-frontier: {benchmark_id} has insufficient coverage")
    app = APP.read_text()
    for view in REQUIRED_STORY_VIEWS:
        if view not in app:
            errors.append(f"lifecycle selector missing {view}")
    if re.search(r"test_of_time\s*:\s*true|still_frontier\s*:\s*true", app):
        errors.append("manual lifecycle membership found in frontend")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated integration for {len(benchmarks)} active benchmarks, {len(models)} models, {len(resources)} resources.")


if __name__ == "__main__":
    main()
