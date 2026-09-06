#!/usr/bin/env python3
"""Validate that every active benchmark is fully connected to generated data."""

import json
import hashlib
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "site" / "data" / "benchmarks.json"
APP = ROOT / "site" / "app.js"
ORGANIZATION_REGISTRY = ROOT / "data" / "organizations.json"
EVIDENCE = ROOT / "data" / "evidence.jsonl"

REQUIRED_STORY_VIEWS = ("test-of-time", "still-frontier", "fastest-solved", "recently-saturated")
MONTH_DAYS = 30.44


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def stable_id(prefix, *parts):
    identity = "\x1f".join(str(part).strip() for part in parts)
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]
    label = slug(parts[-1])[:48] if parts else "record"
    return f"{prefix}-{label}-{digest}"


def expected_measurement_id(observation):
    fields = ("benchmark_version_id", "model_id", "model_label_id", "score_series_id",
              "protocol_id", "task_set_id", "score")
    if any(observation.get(field) is None for field in fields):
        return None
    return stable_id(
        "obs",
        observation["benchmark_version_id"],
        observation["model_id"],
        observation["model_label_id"],
        observation["score_series_id"],
        observation["protocol_id"],
        observation["task_set_id"],
        format(observation["score"], ".15g"),
    )


def load_reference_organizations():
    payload = json.loads(ORGANIZATION_REGISTRY.read_text())
    organizations = payload.get("reference_organizations", [])
    names = [item.get("name") for item in organizations]
    aliases = {}
    errors = []
    if len(names) != 7 or len(names) != len(set(names)):
        errors.append("organization registry must contain seven unique reference organizations")
    for item in organizations:
        if not item.get("id") or not item.get("name") or not item.get("aliases"):
            errors.append(f"invalid reference organization record: {item}")
            continue
        for alias in item["aliases"]:
            key = alias.strip().casefold()
            if key in aliases and aliases[key] != item["name"]:
                errors.append(f"organization alias {alias!r} maps to multiple reference organizations")
            aliases[key] = item["name"]
    return organizations, aliases, errors


def represented_reference_organizations(observations, organizations, aliases):
    represented = set()
    for observation in observations:
        for label in (observation.get("organization") or "").split(","):
            canonical = aliases.get(label.strip().casefold())
            if canonical:
                represented.add(canonical)
    return [item["name"] for item in organizations if item["name"] in represented]


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
    if benchmark.get("observation_count") != len(benchmark.get("observations", [])):
        errors.append(f"{benchmark.get('id')}: observation_count does not match canonical measurements")
    expected_evidence_count = sum(
        len(observation.get("evidence_ids", [])) for observation in benchmark.get("observations", [])
    )
    if benchmark.get("evidence_record_count") != expected_evidence_count:
        errors.append(f"{benchmark.get('id')}: evidence_record_count does not match observation lineage")
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
        expected_id = expected_measurement_id(observation)
        if expected_id and observation_id != expected_id:
            errors.append(f"{observation_id}: ID is not derived from canonical measurement identity")
        if not observation.get("model_configuration"):
            errors.append(f"{observation_id}: missing model_configuration")
        if observation.get("model_label_id") != slug(observation.get("model") or "unknown"):
            errors.append(f"{observation_id}: model_label_id does not match display label")
        expected_model_id = stable_id(
            "model", observation.get("model_identity_organization") or "unknown",
            slug(observation.get("model_configuration") or "unknown")
        )
        if observation.get("model_id") != expected_model_id:
            errors.append(f"{observation_id}: model_id is not derived from model/config identity")
        if not observation.get("evidence_ids") or observation.get("evidence_count") != len(observation.get("evidence_ids", [])):
            errors.append(f"{observation_id}: invalid evidence lineage")
        if len(observation.get("evidence_ids", [])) != len(set(observation.get("evidence_ids", []))):
            errors.append(f"{observation_id}: duplicate evidence IDs")
        if not observation.get("score_source_ids"):
            errors.append(f"{observation_id}: no score_source_ids")
        if not set(observation.get("score_source_ids", [])).issubset(observation.get("source_ids", [])):
            errors.append(f"{observation_id}: score sources are absent from full source lineage")
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
        date_candidates = [
            observation.get("evaluation_date"),
            observation.get("model_release_date"),
            observation.get("result_public_date"),
        ]
        expected_observation_date = min((value for value in date_candidates if value), default=None)
        if observation.get("observation_date") != expected_observation_date:
            errors.append(f"{observation_id}: observation_date is not the earliest available candidate")
        if observation.get("capability_date") != expected_observation_date:
            errors.append(f"{observation_id}: capability_date does not match observation_date")
        if expected_observation_date and not observation.get("observation_date_sources"):
            errors.append(f"{observation_id}: observation_date has no date-source lineage")
        for date_source_id in observation.get("observation_date_source_ids", []):
            if date_source_id not in resources:
                errors.append(f"{observation_id}: unresolved observation-date source {date_source_id}")
    for point in benchmark.get("frontier", []):
        if point.get("observation_id") not in observation_ids:
            errors.append(f"{benchmark['id']}: frontier point is not canonical")
        if not point.get("source_ids"):
            errors.append(f"{benchmark['id']}: frontier point has no lineage")
        observation = observations_by_id.get(point.get("observation_id"), {})
        if observation.get("score_role") != "canonical":
            errors.append(f"{benchmark['id']}: auxiliary observation entered canonical frontier")
        expected_plot_date = max(benchmark["release"], observation.get("observation_date", ""))
        if point.get("plot_date") != expected_plot_date:
            errors.append(f"{benchmark['id']}: frontier point is not clipped to benchmark release")
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
    for label, threshold in benchmark.get("threshold_days", {}).items():
        if threshold.get("days") is not None and threshold["days"] < 0:
            errors.append(f"{benchmark['id']}: {label} lifecycle duration is negative")
    return errors


def main():
    payload = json.loads(SNAPSHOT.read_text())
    evidence_records = [json.loads(line) for line in EVIDENCE.read_text().splitlines() if line]
    organizations, organization_aliases, organization_errors = load_reference_organizations()
    benchmarks = payload.get("benchmarks", [])
    resources = {item["id"]: item for item in payload.get("resources", [])}
    models = {item["id"]: item for item in payload.get("models", [])}
    errors = list(organization_errors)
    if payload.get("schema_version") != 2:
        errors.append("generated snapshot must use schema_version 2")
    resource_ids = [item.get("id") for item in payload.get("resources", [])]
    model_ids = [item.get("id") for item in payload.get("models", [])]
    if len(resource_ids) != len(set(resource_ids)):
        errors.append("duplicate canonical resource IDs")
    if len(model_ids) != len(set(model_ids)):
        errors.append("duplicate canonical model IDs")
    for model in payload.get("models", []):
        expected_model_id = stable_id(
            "model", model.get("identity_organization") or "unknown",
            slug(model.get("configuration_id") or "unknown")
        )
        if model.get("id") != expected_model_id:
            errors.append(f"{model.get('id')}: model ID is not derived from model/config identity")
    for resource in payload.get("resources", []):
        if "://" not in resource.get("url", ""):
            errors.append(f"{resource.get('id')}: resource URL is not navigable")
        if resource.get("id") != stable_id("resource", resource.get("url", "")):
            errors.append(f"{resource.get('id')}: resource ID is not derived from canonical URL")
    if payload.get("reference_organizations") != organizations:
        errors.append("generated reference organization panel is stale")
    ids = [item.get("id") for item in benchmarks]
    if len(ids) != len(set(ids)):
        errors.append("duplicate active benchmark IDs")
    for benchmark in benchmarks:
        errors.extend(validate_benchmark(benchmark, resources, models))
        expected_organizations = represented_reference_organizations(
            benchmark.get("observations", []), organizations, organization_aliases
        )
        coverage = benchmark.get("coverage", {})
        if coverage.get("represented_organizations") != expected_organizations:
            errors.append(f"{benchmark.get('id')}: stale normalized coverage organizations")
        expected_value = len(expected_organizations) / len(organizations)
        if coverage.get("value") != expected_value:
            errors.append(f"{benchmark.get('id')}: stale normalized coverage value")
    evidence_by_id = {}
    for record in evidence_records:
        evidence_id = record.get("evidence_id")
        if not evidence_id or evidence_id in evidence_by_id:
            errors.append(f"missing or duplicate evidence ID {evidence_id}")
        evidence_by_id[evidence_id] = record
        if record.get("model_id") not in models:
            errors.append(f"{evidence_id}: unresolved evidence model")
        for source_id in record.get("source_ids", []):
            if source_id not in resources:
                errors.append(f"{evidence_id}: unresolved evidence source {source_id}")
    linked_evidence = []
    for benchmark in benchmarks:
        for observation in benchmark.get("observations", []):
            for evidence_id in observation.get("evidence_ids", []):
                linked_evidence.append(evidence_id)
                record = evidence_by_id.get(evidence_id)
                if not record:
                    errors.append(f"{observation['observation_id']}: unresolved evidence {evidence_id}")
                    continue
                if record.get("benchmark_id") != benchmark["id"]:
                    errors.append(f"{evidence_id}: benchmark lineage mismatch")
                if record.get("model_id") != observation.get("model_id"):
                    errors.append(f"{evidence_id}: model lineage mismatch")
                if not set(record.get("source_ids", [])).issubset(observation.get("score_source_ids", [])):
                    errors.append(f"{evidence_id}: source lineage missing from canonical measurement")
    if len(linked_evidence) != len(set(linked_evidence)):
        errors.append("one evidence record is linked to multiple canonical measurements")
    if set(linked_evidence) != set(evidence_by_id):
        errors.append(
            f"evidence reconciliation mismatch: unlinked={len(set(evidence_by_id)-set(linked_evidence))}, "
            f"missing={len(set(linked_evidence)-set(evidence_by_id))}"
        )
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
    print(f"Validated integration for {len(benchmarks)} active benchmarks, {len(models)} models, "
          f"{len(resources)} resources, and {len(evidence_records)} evidence records.")


if __name__ == "__main__":
    main()
