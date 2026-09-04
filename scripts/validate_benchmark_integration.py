#!/usr/bin/env python3
"""Validate that every active benchmark is fully connected to generated data."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "site" / "data" / "benchmarks.json"
APP = ROOT / "site" / "app.js"

REQUIRED_STORY_VIEWS = ("test-of-time", "still-frontier", "fastest-solved", "recently-saturated")


def validate_benchmark(benchmark, resources, models):
    errors = []
    required = ("id", "name", "benchmark_version_id", "release", "evaluation_type", "domain",
                "summary", "task_format", "scoring", "evaluation_target", "observations",
                "frontier", "resource_ids", "coverage")
    for field in required:
        if field not in benchmark or benchmark[field] in (None, "", []):
            errors.append(f"{benchmark.get('id', '<unknown>')}: missing {field}")
    for field in ("summary", "task_format"):
        value = benchmark.get(field, {})
        for lang in ("en", "zh"):
            if not value.get(lang):
                errors.append(f"{benchmark.get('id')}: missing {field}.{lang}")
    for resource_id in benchmark.get("resource_ids", []):
        if resource_id not in resources:
            errors.append(f"{benchmark['id']}: unresolved benchmark resource {resource_id}")
    observation_ids = set()
    for observation in benchmark.get("observations", []):
        observation_id = observation.get("observation_id")
        if not observation_id or observation_id in observation_ids:
            errors.append(f"{benchmark['id']}: missing or duplicate observation_id {observation_id}")
        observation_ids.add(observation_id)
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
