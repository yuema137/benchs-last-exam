#!/usr/bin/env python3
"""Build the small static benchmark snapshot used by the local site."""

import csv
import hashlib
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "site" / "data" / "benchmarks.json"
INDEX_OUT = ROOT / "site" / "data" / "index.json"
DETAIL_OUT = ROOT / "site" / "data" / "benchmarks"
PUBLIC_RESOURCE_OUT = ROOT / "site" / "data" / "resources.json"
RESOURCE_OUT = ROOT / "data" / "resources.json"
OBSERVATION_OUT = ROOT / "data" / "observations.jsonl"
EVIDENCE_OUT = ROOT / "data" / "evidence.jsonl"
MODEL_OUT = ROOT / "data" / "models.json"
ORGANIZATION_REGISTRY = ROOT / "data" / "organizations.json"
CAPABILITY_LABEL_REGISTRY = ROOT / "data" / "capability_labels.json"


def build_date():
    """Return today's date, or a deterministic date supplied by the build."""
    override = os.environ.get("BLE_SNAPSHOT_DATE")
    return date.fromisoformat(override) if override else date.today()


BUILD_DATE = build_date()

BENCHMARK_REGISTRY = ROOT / "data" / "benchmarks"
sys.path.insert(0, str(ROOT / "src"))

from benchmark_observatory.registry import load_benchmark_specs


BENCHMARKS = load_benchmark_specs(BENCHMARK_REGISTRY, RAW)

INDEX_BENCHMARK_FIELDS = (
    "id", "name", "domain", "release", "evaluation_type", "tags", "labels",
    "score_format", "score_decimals", "capability_frontier_value",
    "normalized_progress", "normalized_headroom", "threshold_days",
    "velocity_180d", "coverage", "cost_per_task", "lifecycle_eligibility",
)

_organization_payload = json.loads(ORGANIZATION_REGISTRY.read_text())
CAPABILITY_LABELS = json.loads(CAPABILITY_LABEL_REGISTRY.read_text())["labels"]
REFERENCE_ORGANIZATIONS = tuple(_organization_payload["reference_organizations"])
REFERENCE_ORGANIZATION_NAMES = tuple(item["name"] for item in REFERENCE_ORGANIZATIONS)
REFERENCE_ORGANIZATION_ALIASES = {
    alias.casefold(): item["name"]
    for item in REFERENCE_ORGANIZATIONS
    for alias in item["aliases"]
}

MODEL_RELEASE_RESOURCES = {
    "fable-5-1": {
        "url": "https://www.anthropic.com/claude/fable",
        "title": "Claude Fable 5.1 official release page",
        "resource_type": "release_post",
        "publisher": "Anthropic",
    },
    "gpt-6-astra": {
        "url": "https://developers.openai.com/api/docs/models/gpt-6-astra",
        "title": "GPT-6 Astra official model page",
        "resource_type": "model_card",
        "publisher": "OpenAI",
    },
    "gemini-3-8-flash": {
        "url": "https://deepmind.google/models/model-cards/gemini-3-8-flash/",
        "title": "Gemini 3.8 Flash official model card",
        "resource_type": "model_card",
        "publisher": "Google DeepMind",
    },
    "deepseek-v4-pro-0813": {
        "url": "https://api-docs.deepseek.com/news/news260813/",
        "title": "DeepSeek-V4-Pro official release announcement",
        "resource_type": "release_post",
        "publisher": "DeepSeek",
    },
    "qwen3-8-max": {
        "url": "https://docs.modelstudio.console.alibabacloud.com/en/model-studio/qwen3-8-max",
        "title": "Qwen3.8-Max official model documentation",
        "resource_type": "documentation",
        "publisher": "Alibaba Cloud",
    },
    "llama-4-maverick": {
        "url": "https://ai.meta.com/llama/get-started/",
        "title": "Llama 4 Maverick official model resources",
        "resource_type": "model_card",
        "publisher": "Meta",
    },
    "grok-4-6": {
        "url": "https://x.ai/news/grok-4-6",
        "title": "Grok 4.6 official release announcement",
        "resource_type": "release_post",
        "publisher": "xAI",
    },
}

REFERENCE_MODEL_RELEASES = [
    {
        "id": "model-claude-fable-5-1",
        "canonical_name": "Claude Fable 5.1",
        "family_id": "anthropic-claude-fable-5-1",
        "release_date": "2026-09-01",
        "organization": "Anthropic",
        "role": "contemporary_frontier",
        "domain": "General knowledge & reasoning",
    },
    {
        "id": "model-gpt-6-astra",
        "canonical_name": "GPT-6 Astra",
        "family_id": "openai-gpt-6-astra",
        "release_date": "2026-09-03",
        "organization": "OpenAI",
        "role": "contemporary_frontier",
        "domain": "General knowledge & reasoning",
    },
    {
        "id": "model-gemini-3-8-flash",
        "canonical_name": "Gemini 3.8 Flash",
        "family_id": "google-gemini-3-8-flash",
        "release_date": "2026-09-02",
        "organization": "Google DeepMind",
        "role": "contemporary_frontier",
        "domain": "General knowledge & reasoning",
    },
    {
        "id": "model-deepseek-v4-pro-0813",
        "canonical_name": "DeepSeek-V4-Pro-0813",
        "family_id": "deepseek-v4-pro",
        "release_date": "2026-08-13",
        "organization": "DeepSeek",
        "role": "open_weight_frontier",
        "domain": "Coding",
    },
    {
        "id": "model-qwen-3-8-max",
        "canonical_name": "Qwen3.8-Max",
        "family_id": "qwen-3-8-max",
        "release_date": "2026-08-03",
        "organization": "Alibaba",
        "role": "open_weight_frontier",
        "domain": "General knowledge & reasoning",
    },
    {
        "id": "model-llama-4-maverick",
        "canonical_name": "Llama 4 Maverick",
        "family_id": "meta-llama-4",
        "release_date": "2025-04-05",
        "organization": "Meta",
        "role": "open_weight_frontier",
        "domain": "Multimodal",
    },
    {
        "id": "model-grok-4-6",
        "canonical_name": "Grok 4.6",
        "family_id": "xai-grok-4-6",
        "release_date": "2026-08-12",
        "organization": "xAI",
        "role": "contemporary_frontier",
        "domain": "General knowledge & reasoning",
    },
]

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def stable_id(prefix, *parts):
    """Return a compact ID derived from semantic identity, never row position."""
    identity = "\x1f".join(str(part).strip() for part in parts)
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16]
    label = slug(parts[-1])[:48] if parts else "record"
    return f"{prefix}-{label}-{digest}"


def write_public_data_bundles(payload):
    """Write a small index plus one independently loadable detail record."""
    index_benchmarks = []
    resources = {item["id"]: item for item in payload["resources"]}
    DETAIL_OUT.mkdir(parents=True, exist_ok=True)
    expected_detail_paths = set()
    for benchmark in payload["benchmarks"]:
        detail_path = f"benchmarks/{benchmark['id']}.json"
        index_benchmark = {key: benchmark[key] for key in INDEX_BENCHMARK_FIELDS}
        index_benchmark["detail_path"] = detail_path
        index_benchmarks.append(index_benchmark)

        detail_payload = {
            "schema_version": payload["schema_version"],
            "bundle_kind": "benchmark_detail",
            "snapshot_id": payload["snapshot_id"],
            "reference_organizations": payload["reference_organizations"],
            "benchmark": benchmark,
        }
        path = DETAIL_OUT / f"{benchmark['id']}.json"
        path.write_text(json.dumps(detail_payload, indent=2) + "\n")
        expected_detail_paths.add(path)

    for stale_path in DETAIL_OUT.glob("*.json"):
        if stale_path not in expected_detail_paths:
            stale_path.unlink()

    index_payload = {
        "schema_version": payload["schema_version"],
        "bundle_kind": "benchmark_index",
        "snapshot_id": payload["snapshot_id"],
        "source": payload["source"],
        "reference_organizations": payload["reference_organizations"],
        "capability_labels": payload["capability_labels"],
        "benchmarks": index_benchmarks,
        "lifecycle_views": payload["lifecycle_views"],
    }
    INDEX_OUT.write_text(json.dumps(index_payload, indent=2) + "\n")
    PUBLIC_RESOURCE_OUT.write_text(json.dumps({
        "schema_version": payload["schema_version"],
        "bundle_kind": "resource_registry",
        "snapshot_id": payload["snapshot_id"],
        "resources": [resources[key] for key in sorted(resources)],
    }, indent=2) + "\n")


def canonical_url(value):
    """Normalize equivalent evidence URLs without erasing source versions."""
    value = (value or "").strip()
    if not value or "://" not in value:
        return value
    parsed = urlsplit(value)
    scheme = "https" if parsed.scheme in {"http", "https"} else parsed.scheme.lower()
    host = parsed.netloc.casefold()
    path = re.sub(r"/{2,}", "/", parsed.path)
    if host in {"arxiv.org", "www.arxiv.org"}:
        host = "arxiv.org"
        match = re.match(r"/(?:abs|pdf|html)/([^/?#]+?)(?:\.pdf)?$", path)
        if match:
            path = f"/abs/{match.group(1)}"
    elif path != "/":
        path = path.rstrip("/")
    query = urlencode([(key, val) for key, val in parse_qsl(parsed.query, keep_blank_values=True)
                       if not key.casefold().startswith("utm_")])
    return urlunsplit((scheme, host, path, query, ""))


def canonical_reference_organizations(value):
    """Resolve source-specific organization labels to the seven panel names.

    Source exports sometimes use a research-lab name (Google DeepMind), a
    parent-company name (Alibaba), or comma-separated affiliations. Preserve
    the source label on the observation, but use this registry for Coverage.
    """
    represented = set()
    for label in (value or "").split(","):
        canonical = REFERENCE_ORGANIZATION_ALIASES.get(label.strip().casefold())
        if canonical:
            represented.add(canonical)
    return represented


def organization_identity(value):
    canonical = sorted(canonical_reference_organizations(value))
    return "|".join(name.casefold() for name in canonical) if canonical else slug(value or "Unknown")


def register_resource(resources, url, title, *, resource_type="other", publisher=None,
                      authority="trusted_secondary", scope=("benchmark", "model"),
                      notes=None):
    url = canonical_url(url)
    resource_id = stable_id("resource", url)
    resources.setdefault(resource_id, {
        "id": resource_id,
        "resource_scope": list(scope),
        "entity_id": None,
        "resource_type": resource_type,
        "title": title,
        "url": url,
        "publisher": publisher,
        "authority": authority,
        "active": True,
        "watch": False,
        "last_checked_at": None,
        "notes": notes,
    })
    return resource_id


def model_identity(row, display_model):
    """Use the source's model/config identifier before its mutable display name."""
    configuration = (row.get("Model version") or display_model).strip()
    organization = (row.get("Organization") or "Unknown").strip()
    identity_organization = organization_identity(organization)
    return stable_id("model", identity_organization, slug(configuration)), configuration, identity_organization


def evidence_identity(spec, row, row_number):
    source_row_id = (row.get("id") or "").strip()
    if source_row_id:
        return stable_id("evidence", spec["id"], source_row_id)
    normalized_row = json.dumps({key: value for key, value in row.items() if key is not None and value not in (None, "")},
                                sort_keys=True, separators=(",", ":"))
    # row_number is diagnostic only. Content determines identity when exports lack IDs.
    return stable_id("evidence", spec["id"], spec["file"], normalized_row)


def measurement_identity(row):
    return stable_id(
        "obs",
        row["benchmark_version_id"],
        row["model_id"],
        row["model_label_id"],
        row["score_series_id"],
        row["protocol_id"],
        row["task_set_id"],
        format(row["score"], ".15g"),
    )


def model_family(model, organization):
    cleaned_model = re.sub(r"\s*\([^)]*\)", "", model)
    return slug(f"{organization}-{cleaned_model}")


def model_release_resource(resources, model):
    normalized = slug(model)
    for key, spec in MODEL_RELEASE_RESOURCES.items():
        if key in normalized:
            return register_resource(
                resources,
                spec["url"],
                spec["title"],
                resource_type=spec["resource_type"],
                publisher=spec["publisher"],
                authority="primary",
                scope=("model",),
                notes="Official release/model resource for the current frontier model panel.",
            )
    return None


def normalize_date(value):
    """Return an ISO date plus source precision for supported export formats."""
    value = (value or "").strip()
    if not value:
        return None, None
    value = value[:10]
    for fmt, precision in (("%Y-%m-%d", "day"), ("%m/%d/%Y", "day"), ("%Y-%m", "month")):
        try:
            parsed = datetime.strptime(value, fmt).date()
            return parsed.isoformat(), precision
        except ValueError:
            pass
    raise ValueError(f"Unsupported date value {value!r}")


def earliest_row_date(row, columns):
    candidates = []
    for column in columns:
        value, precision = normalize_date(row.get(column))
        if value:
            candidates.append({"date": value, "kind": column, "precision": precision})
    if not candidates:
        return None, None, []
    earliest = min(item["date"] for item in candidates)
    sources = [item for item in candidates if item["date"] == earliest]
    precision = "month" if all(item["precision"] == "month" for item in sources) else "day"
    return earliest, precision, sources


def parse_dates(row):
    evaluation_date, evaluation_precision, evaluation_sources = earliest_row_date(
        row, ("Started at", "Evaluation date", "Date of evaluation", "Run date")
    )
    model_release_date, model_release_precision = normalize_date(row.get("Release date"))
    result_public_date, result_public_precision, publication_sources = earliest_row_date(
        row, ("Result public date", "Source publication date", "Date added", "Last updated")
    )
    source_publication_date, _ = normalize_date(
        row.get("Source publication date") or row.get("Result public date")
    )
    candidates = []
    if evaluation_date:
        candidates.append({"date": evaluation_date, "kind": "evaluation_date", "precision": evaluation_precision})
    if model_release_date:
        candidates.append({"date": model_release_date, "kind": "model_release_date", "precision": model_release_precision})
    if result_public_date:
        candidates.append({"date": result_public_date, "kind": "score_publication_date", "precision": result_public_precision})
    observation_date = min((item["date"] for item in candidates), default=None)
    selected = [item for item in candidates if item["date"] == observation_date]
    observation_precision = (
        "month" if selected and all(item["precision"] == "month" for item in selected) else
        "day" if selected else None
    )
    return {
        "evaluation_date": evaluation_date,
        "evaluation_date_precision": evaluation_precision,
        "evaluation_date_sources": evaluation_sources,
        "model_release_date": model_release_date,
        "model_release_date_precision": model_release_precision,
        "result_public_date": result_public_date,
        "result_public_date_precision": result_public_precision,
        "score_publication_date_sources": publication_sources,
        "source_publication_date": source_publication_date,
        "observation_date": observation_date,
        "observation_date_precision": observation_precision,
        "observation_date_sources": selected,
    }


def register_model(models, *, model_id, canonical_name, configuration, identity_organization,
                   family_id, release_date,
                   organization, resource_ids, domain, evaluation_type):
    model = models.setdefault(model_id, {
        "id": model_id,
        "canonical_name": canonical_name,
        "aliases": [],
        "configuration_id": configuration,
        "identity_organization": identity_organization,
        "family_id": family_id,
        "release_date": release_date,
        "organization": organization,
        "resource_ids": [],
        "roles": ["contemporary_frontier"],
        "domains": [],
        "evaluation_types": [],
        "inclusion_reason": "Included as a representative observation in the curated pilot dataset.",
        "provenance_note": "The current export provides evaluation evidence but not always a model-specific official resource.",
    })
    if canonical_name != model["canonical_name"] and canonical_name not in model["aliases"]:
        model["aliases"].append(canonical_name)
    if release_date and (not model["release_date"] or release_date < model["release_date"]):
        model["release_date"] = release_date
    for resource_id in resource_ids:
        if resource_id and resource_id not in model["resource_ids"]:
            model["resource_ids"].append(resource_id)
    if domain not in model["domains"]:
        model["domains"].append(domain)
    if evaluation_type not in model["evaluation_types"]:
        model["evaluation_types"].append(evaluation_type)
    return model


def _earliest(values):
    return min((value for value in values if value), default=None)


def merge_measurements(rows):
    """Collapse duplicate source rows into one canonical measured score.

    Equality is intentionally strict: benchmark version, model configuration,
    score series, protocol, task set, and exact normalized score must all match.
    Every source row remains addressable through evidence_ids and evidence.jsonl.
    """
    groups = {}
    for row in rows:
        row["observation_id"] = measurement_identity(row)
        groups.setdefault(row["observation_id"], []).append(row)

    merged = []
    for observation_id, evidence_rows in groups.items():
        evidence_rows = sorted(evidence_rows, key=lambda item: item["evidence_id"])
        base = dict(evidence_rows[0])
        evaluation_date = _earliest(item.get("evaluation_date") for item in evidence_rows)
        model_release_date = _earliest(item.get("model_release_date") for item in evidence_rows)
        result_public_date = _earliest(item.get("result_public_date") for item in evidence_rows)
        observation_date = _earliest((evaluation_date, model_release_date, result_public_date))
        selected_date_sources = []
        for item in evidence_rows:
            if item.get("observation_date") == observation_date:
                selected_date_sources.extend(item.get("observation_date_sources", []))
        selected_date_sources = list({
            json.dumps(source, sort_keys=True): source for source in selected_date_sources
        }.values())
        observation_precision = (
            "month" if selected_date_sources and all(source.get("precision") == "month" for source in selected_date_sources)
            else "day" if selected_date_sources else None
        )
        source_ids = sorted({source_id for item in evidence_rows for source_id in item["source_ids"]})
        score_source_ids = sorted({source_id for item in evidence_rows for source_id in item["score_source_ids"]})
        date_source_ids = sorted({
            source_id for source in selected_date_sources for source_id in source.get("resource_ids", [])
        })
        base.update({
            "observation_id": observation_id,
            "evidence_ids": [item["evidence_id"] for item in evidence_rows],
            "evidence_count": len(evidence_rows),
            "source_row_ids": sorted({item["source_row_id"] for item in evidence_rows if item.get("source_row_id")}),
            "source_ids": source_ids,
            "score_source_ids": score_source_ids,
            "source": base["source"] if base["score_source_ids"] else None,
            "evaluation_date": evaluation_date,
            "model_release_date": model_release_date,
            "result_public_date": result_public_date,
            "source_publication_date": _earliest(item.get("source_publication_date") for item in evidence_rows),
            "observation_date": observation_date,
            "observation_date_precision": observation_precision,
            "observation_date_sources": selected_date_sources,
            "observation_date_source_ids": date_source_ids,
            "evaluation_date_sources": [source for item in evidence_rows for source in item.get("evaluation_date_sources", [])],
            "score_publication_date_sources": [source for item in evidence_rows for source in item.get("score_publication_date_sources", [])],
            "date": observation_date,
            "date_precision": observation_precision,
            "date_notes": None if result_public_date else "A score-publication date is not present in the source export.",
            "capability_date": observation_date,
            "retrospective": any(item["retrospective"] for item in evidence_rows),
            "contemporaneous": all(item["contemporaneous"] for item in evidence_rows),
            "historical_frontier_eligible": bool(result_public_date),
        })
        base["temporal_class"] = "retrospective_evaluation" if base["retrospective"] else "historical_or_unknown"
        base.pop("evidence_id", None)
        base.pop("source_row_id", None)
        merged.append(base)
    return merged


def build_frontier(rows, date_field, date_meaning, minimum_date=None):
    """Build a deterministic, step-function frontier from canonical observations.

    Observations sharing a date are evaluated as one cohort. The winning
    observation retains the lineage of the score that established the event;
    the cohort IDs document the other observations considered at that date.
    """
    cohorts = {}
    for row in rows:
        event_date = row.get(date_field)
        if event_date and minimum_date:
            # Capability time cannot precede benchmark release on the plot.
            # Keep the observation's original model release date for provenance,
            # but use the effective date for frontier grouping and metrics.
            event_date = max(event_date, minimum_date)
        if event_date:
            cohorts.setdefault(event_date, []).append(row)
    frontier = []
    best_score = None
    for event_date in sorted(cohorts):
        cohort = sorted(
            cohorts[event_date],
            key=lambda item: (
                item["score"], item.get("model_label_id") or slug(item.get("model", "unknown")),
                item["observation_id"],
            ),
        )
        winner = cohort[-1]
        if best_score is None or winner["score"] > best_score:
            event = {**winner}
            event["plot_date"] = event_date
            event["date"] = event_date
            event["date_kind"] = event.get(f"{date_field}_meaning", date_meaning)
            event["frontier_observation_ids"] = [item["observation_id"] for item in cohort]
            frontier.append(event)
            best_score = winner["score"]
    return frontier


def threshold_metrics(frontier, release, floor, ceiling, as_of=None):
    result = {}
    if floor is None or ceiling is None or ceiling == floor:
        for label in ("T50", "T80", "T90"):
            result[label] = {"status": "not_applicable", "reason": "No defensible fixed floor and ceiling."}
        return result
    censor_date = as_of or (date.fromisoformat(frontier[-1]["plot_date"]) if frontier else release)
    for label, target in (("T50", 0.5), ("T80", 0.8), ("T90", 0.9)):
        crossing = next((point for point in frontier if (point["score"] - floor) / (ceiling - floor) >= target), None)
        if crossing:
            days = (date.fromisoformat(crossing["plot_date"]) - release).days
            result[label] = {"status": "at_release", "days": 0, "qualifying_observation_date": crossing["plot_date"]} if days <= 0 else {"status": "reached", "days": days, "qualifying_observation_date": crossing["plot_date"]}
        elif frontier:
            result[label] = {"status": "right_censored", "days": max(0, (censor_date - release).days)}
        else:
            result[label] = {"status": "unknown", "reason": "No dated observations are available on this timeline."}
    finite = {label: item["days"] for label, item in result.items()
              if item.get("status") in {"at_release", "reached"}}
    for lower, higher in (("T50", "T80"), ("T80", "T90"), ("T50", "T90")):
        if lower in finite and higher in finite and finite[higher] < finite[lower]:
            raise ValueError(f"Threshold ordering violated: {higher}={finite[higher]} < {lower}={finite[lower]}")
    return result


def frontier_velocity(frontier, window_days=180):
    if len(frontier) < 2:
        return None
    latest = frontier[-1]
    latest_date = date.fromisoformat(latest["plot_date"])
    prior = next((point for point in reversed(frontier[:-1])
                  if (latest_date - date.fromisoformat(point["plot_date"])).days >= window_days), None)
    if not prior:
        return None
    elapsed = (latest_date - date.fromisoformat(prior["plot_date"])).days
    return (latest["score"] - prior["score"]) / elapsed * 30.44


def lifecycle_eligibility(benchmark, snapshot_date):
    """Return explicit, auditable hard-rule decisions for every story view."""
    month_days = 30.44
    t50 = benchmark["threshold_days"].get("T50", {})
    t90 = benchmark["threshold_days"].get("T90", {})
    t50_days, t90_days = t50.get("days"), t90.get("days")
    progress = benchmark.get("normalized_progress")
    test_of_time = ((t50_days is not None and t50_days >= 12 * month_days)
                    or (t90_days is not None and t90_days >= 24 * month_days))
    still_frontier = (t50.get("status") == "right_censored" and progress is not None
                      and progress < 0.5 and benchmark["coverage"].get("status") != "low")
    fastest_solved = (t90.get("status") == "reached" and t90_days is not None
                      and t90_days < 6 * month_days)
    recently_saturated = False
    if t90.get("status") in {"reached", "at_release"} and t90_days is not None:
        release = date.fromisoformat(benchmark["release"])
        crossing_age = (snapshot_date - release).days - t90_days
        recently_saturated = 0 <= crossing_age <= 3 * month_days
    return {
        "test-of-time": {"eligible": test_of_time, "rule": "T50 >= 12 months OR T90 >= 24 months, including censoring"},
        "still-frontier": {"eligible": still_frontier, "rule": "right-censored T50 AND normalized progress < 50% AND coverage not low"},
        "fastest-solved": {"eligible": fastest_solved, "rule": "known reached T90 < 6 months"},
        "recently-saturated": {"eligible": recently_saturated, "rule": "T90 crossing within 3 months of snapshot"},
    }


def lifecycle_view_ids(benchmarks, snapshot_date):
    """Derive all story-tab membership from explicit hard-rule decisions."""
    views = {name: [] for name in ("test-of-time", "still-frontier", "fastest-solved", "recently-saturated")}
    for benchmark in benchmarks:
        decisions = lifecycle_eligibility(benchmark, snapshot_date)
        benchmark["lifecycle_eligibility"] = decisions
        for view, decision in decisions.items():
            if decision["eligible"]:
                views[view].append(benchmark["id"])
    return views


def build_benchmark(spec, resources, models, evidence_records):
    benchmark_resource_id = register_resource(
        resources, spec["source"], f"{spec['name']} primary source", resource_type="paper",
        publisher="Benchmark authors", authority="primary", scope=("benchmark",),
    )
    rows = []
    with (RAW / spec["file"]).open(newline="") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=1):
            try:
                input_score = float(row[spec["score"]])
            except (KeyError, TypeError, ValueError):
                continue
            input_unit = spec["input_unit"]
            if input_unit == "fraction":
                if not 0 <= input_score <= 1:
                    raise ValueError(f"{spec['id']} row {row_number}: fraction input outside [0, 1]")
                score = input_score
            elif input_unit == "percentage_points":
                if not 0 <= input_score <= 100:
                    raise ValueError(f"{spec['id']} row {row_number}: percentage input outside [0, 100]")
                score = input_score / 100
            elif input_unit == "number":
                score = input_score
            else:
                raise ValueError(f"{spec['id']}: unsupported input unit {input_unit!r}")
            dates = parse_dates(row)
            evaluation_date = dates["evaluation_date"]
            model_release_date = dates["model_release_date"]
            result_public_date = dates["result_public_date"]
            source_publication_date = dates["source_publication_date"]
            observation_date = dates["observation_date"]
            model = (row.get("Name") or row.get("Model version") or "Unknown model").strip()
            source_candidate = (
                row.get("Source link") or row.get("Source Link") or row.get("Source URL")
                or row.get("Logs") or row.get("Source") or ""
            ).strip()
            source_url = source_candidate if "://" in source_candidate else spec["source"]
            source_is_benchmark_primary = canonical_url(source_url) == canonical_url(spec["source"])
            source_id = register_resource(
                resources, source_url,
                row.get("Source") or ("Epoch evaluation log" if row.get("Logs") else f"{spec['name']} source"),
                resource_type="evaluation_log" if row.get("Logs") else "official_leaderboard",
                publisher="Epoch AI" if row.get("Logs") else row.get("Source"),
                authority="primary" if source_is_benchmark_primary else "trusted_secondary",
                scope=("benchmark", "model"),
                notes="Shared evidence resource; the export does not provide a model-specific source record."
                if not row.get("Source link") and not row.get("Logs") else None,
            )
            model_id, model_configuration, model_identity_organization = model_identity(row, model)
            family_id = model_family(model, row.get("Organization") or "unknown")
            release_resource_id = model_release_resource(resources, model)
            observation_date_sources = []
            for date_source in dates["observation_date_sources"]:
                evidence_resource_ids = [source_id]
                if date_source["kind"] == "model_release_date" and release_resource_id:
                    evidence_resource_ids.insert(0, release_resource_id)
                observation_date_sources.append({
                    **date_source,
                    "resource_ids": evidence_resource_ids,
                })
            is_math_retro = spec["id"] == "math-level-5"
            retrospective = is_math_retro or bool(
                evaluation_date and model_release_date and evaluation_date > model_release_date
            )
            register_model(
                models,
                model_id=model_id,
                canonical_name=model,
                configuration=model_configuration,
                identity_organization=model_identity_organization,
                family_id=family_id,
                release_date=model_release_date,
                organization=row.get("Organization") or "Unknown",
                resource_ids=[source_id, release_resource_id],
                domain=spec["domain"],
                evaluation_type=spec["evaluation_type"],
            )
            source_row_id = row.get("id")
            capability_eligible = (
                bool(observation_date)
                and source_row_id not in spec.get("frontier_exclude_ids", set())
                and model not in spec.get("frontier_exclude_models", set())
            )
            task_set_id = f"{spec['id']}-canonical"
            protocol_id = spec["protocol_id"]
            if spec["id"] == "cybench" and not capability_eligible:
                task_set_id = "cybench-subset-or-unverified"
                protocol_id = "cybench-noncanonical-subset-or-unverified"
            score_role = "canonical" if protocol_id == spec["protocol_id"] else "auxiliary"
            score_series_id = (f"{spec['id']}-canonical-score" if score_role == "canonical"
                               else f"{spec['id']}-auxiliary-{slug(protocol_id)}")
            evidence_id = evidence_identity(spec, row, row_number)
            evidence_records.append({
                "evidence_id": evidence_id,
                "benchmark_id": spec["id"],
                "source_file": spec["file"],
                "source_row_id": source_row_id,
                "source_row_number": row_number,
                "model_id": model_id,
                "model": model,
                "model_configuration": model_configuration,
                "model_identity_organization": model_identity_organization,
                "score": score,
                "input_score": input_score,
                "input_unit": input_unit,
                "source_ids": [source_id],
                "dates": dates,
                "raw_fields": {key: value for key, value in row.items() if key is not None and value not in (None, "")},
            })
            rows.append({
                "observation_id": None,
                "evidence_id": evidence_id,
                "source_row_id": source_row_id,
                "benchmark_id": spec["id"],
                "benchmark_version_id": f"{spec['id']}-canonical",
                "model_id": model_id,
                "model_configuration": model_configuration,
                "model_identity_organization": model_identity_organization,
                "model_label_id": slug(model),
                "model_family_id": family_id,
                "model": model,
                "organization": row.get("Organization") or "Unknown",
                "score": score,
                "input_score": input_score,
                "input_unit": input_unit,
                "reported_cost_per_task": row.get(spec.get("cost_column", "")) if spec.get("cost_column") else None,
                "metric_id": spec["metric_id"],
                "protocol_id": protocol_id,
                "task_set_id": task_set_id,
                "metric": spec["score"],
                "score_role": score_role,
                "score_series_id": score_series_id,
                "evaluation_protocol": spec["protocol"],
                "model_release_date": model_release_date,
                "evaluation_date": evaluation_date,
                "result_public_date": result_public_date,
                "source_publication_date": source_publication_date,
                "observation_date": observation_date,
                "observation_date_precision": dates["observation_date_precision"],
                "observation_date_sources": observation_date_sources,
                "observation_date_source_ids": sorted({
                    resource_id
                    for item in observation_date_sources
                    for resource_id in item["resource_ids"]
                }),
                "evaluation_date_sources": dates["evaluation_date_sources"],
                "score_publication_date_sources": dates["score_publication_date_sources"],
                "ingested_at": BUILD_DATE.isoformat(),
                "date_precision": dates["observation_date_precision"],
                "date_notes": None if result_public_date else "A score-publication date is not present in the source export.",
                "date": observation_date,
                "date_kind": "earliest_observation_evidence_date" if observation_date else "unknown",
                "capability_date": observation_date,
                "capability_date_meaning": "earliest_observation_evidence_date",
                "reported_date_meaning": "result_public_date",
                "historical_frontier_date": result_public_date,
                "temporal_class": "retrospective_evaluation" if retrospective else "historical_or_unknown",
                "retrospective": retrospective,
                "capability_frontier_eligible": capability_eligible,
                "historical_frontier_eligible": bool(result_public_date),
                "eligibility_reason": (
                    "Excluded from the canonical CyBench frontier because the source uses a 35/37-task subset or does not pin the task set."
                    if spec["id"] == "cybench" and not capability_eligible else
                    "Capability eligibility uses the dated curated observation and canonical protocol; reported-result eligibility requires result_public_date."
                ),
                "contemporaneous": not retrospective,
                "source_ids": ([source_id, benchmark_resource_id] if source_id != benchmark_resource_id else [source_id]) + ([release_resource_id] if release_resource_id else []),
                "score_source_ids": [source_id],
                "source": resources[source_id]["url"],
                "notes": "Operational evaluation timeline only; not a historical public-result date.",
            })
    rows = merge_measurements(rows)
    capability_frontier = build_frontier(
        [row for row in rows if row["score_role"] == "canonical" and row["capability_frontier_eligible"]],
        "capability_date",
        "earliest observation evidence date",
        minimum_date=spec["release"],
    )
    reported_frontier = build_frontier(
        [row for row in rows if row["score_role"] == "canonical" and row.get("result_public_date")],
        "result_public_date",
        "result first-public date",
    )
    current = capability_frontier[-1] if capability_frontier else None
    reported_current = reported_frontier[-1] if reported_frontier else None
    progress = None
    progress_baseline = spec.get("progress_baseline")
    progress_target = spec.get("progress_target")
    if current and progress_baseline is not None and progress_target is not None and progress_target != progress_baseline:
        progress = (current["score"] - progress_baseline) / (progress_target - progress_baseline)
        progress = max(0.0, min(1.0, progress))
    release = date.fromisoformat(spec["release"])
    snapshot_date = BUILD_DATE
    threshold_days = threshold_metrics(capability_frontier, release, progress_baseline, progress_target, snapshot_date)
    reported_threshold_days = threshold_metrics(reported_frontier, release, progress_baseline, progress_target, snapshot_date)
    velocity_180d = frontier_velocity(capability_frontier)
    reported_velocity_180d = frontier_velocity(reported_frontier)
    cost_values = []
    if spec.get("cost_column"):
        for row in rows:
            try:
                cost = float(row.get("reported_cost_per_task", ""))
            except (TypeError, ValueError):
                continue
            if cost >= 0:
                cost_values.append(cost)
    cost = None
    if cost_values:
        divisor = spec.get("cost_divisor", 1)
        method = "median of reported per-task values in the curated export"
        if divisor != 1:
            method = f"median of reported full-run costs divided by the documented {divisor}-task benchmark size"
        cost = {"value": sorted(cost_values)[len(cost_values) // 2] / divisor, "currency": "USD", "per_task": True, "method": method, "source_ids": sorted({source_id for row in rows for source_id in row["source_ids"]}), "notes": "Cost varies by model, harness, and inference settings."}
    coverage_orgs = [
        name for name in REFERENCE_ORGANIZATION_NAMES
        if any(name in canonical_reference_organizations(row["organization"]) for row in rows)
    ]
    coverage = len(coverage_orgs) / len(REFERENCE_ORGANIZATION_NAMES)
    auxiliary_score_series = []
    auxiliary_series_ids = sorted({row["score_series_id"] for row in rows if row["score_role"] == "auxiliary"})
    for series_id in auxiliary_series_ids:
        series_rows = [row for row in rows if row["score_series_id"] == series_id]
        series_frontier = build_frontier(
            [row for row in series_rows if row.get("capability_date")],
            "capability_date", "earliest observation evidence date", minimum_date=spec["release"],
        )
        auxiliary_score_series.append({
            "series_id": series_id,
            "role": "auxiliary",
            "label": "Auxiliary / non-canonical protocol",
            "metric_id": spec["metric_id"],
            "metric_name": spec["score"],
            "protocol_id": series_rows[0]["protocol_id"],
            "task_set_id": series_rows[0]["task_set_id"],
            "lifecycle_eligible": False,
            "explanation": {
                "en": "Preserved for comparison, but excluded from leaderboard sorting and lifecycle metrics because its task set or protocol differs from the canonical score.",
                "zh": "该序列保留用于比较，但因 task set 或 protocol 与 canonical score 不同，不参与排行榜排序和 lifecycle 指标。",
            },
            "observation_ids": [row["observation_id"] for row in series_rows],
            "frontier_events": series_frontier,
        })
    return {
        **{key: spec[key] for key in ("id", "name", "domain", "release", "source")},
        "floor": progress_baseline,
        "ceiling": progress_target,
        "hard_min": spec.get("hard_min"),
        "hard_max": spec.get("hard_max"),
        "progress_baseline": progress_baseline,
        "progress_target": progress_target,
        "input_unit": spec["input_unit"],
        "evaluation_type": spec["evaluation_type"],
        "tags": spec["tags"],
        "labels": spec["labels"],
        "metric": spec["score"],
        "score_format": spec.get("score_format", "ratio"),
        "score_decimals": spec.get("score_decimals"),
        "metric_id": spec["metric_id"],
        "protocol_id": spec["protocol_id"],
        "canonical_score": {
            "series_id": f"{spec['id']}-canonical-score",
            "role": "canonical",
            "metric_id": spec["metric_id"],
            "metric_name": spec["score"],
            "protocol_id": spec["protocol_id"],
            "task_set_id": f"{spec['id']}-canonical",
            "direction": "higher_is_better",
            "score_format": spec.get("score_format", "ratio"),
            "input_unit": spec["input_unit"],
            "progress_baseline": progress_baseline,
            "progress_target": progress_target,
            "lifecycle_eligible": True,
        },
        "auxiliary_score_series": auxiliary_score_series,
        "benchmark_version_id": f"{spec['id']}-canonical",
        "summary": spec["summary"],
        "task_format": spec["task_format"],
        "scoring": spec["scoring"],
        "evaluation_target": spec["evaluation_target"],
        "observation_count": len(rows),
        "evidence_record_count": sum(row["evidence_count"] for row in rows),
        "observations": rows,
        "frontier": [{**point, "source_ids": point["source_ids"]} for point in capability_frontier],
        "frontier_events": [{**point, "source_ids": point["source_ids"]} for point in capability_frontier],
        "capability_frontier": [{**point, "source_ids": point["source_ids"]} for point in capability_frontier],
        "reported_frontier": [{**point, "source_ids": point["source_ids"]} for point in reported_frontier],
        "historical_frontier": [{**point, "source_ids": point["source_ids"]} for point in reported_frontier],
        "retrospective_observations": [row for row in rows if row["retrospective"]],
        "observed_frontier": current["score"] if current else None,
        "capability_frontier_value": current["score"] if current else None,
        "reported_frontier_value": reported_current["score"] if reported_current else None,
        "current_frontier": current["score"] if current else None,
        "normalized_progress": progress,
        "normalized_headroom": None if progress is None else 1 - progress,
        "threshold_days": threshold_days,
        "capability_threshold_days": threshold_days,
        "reported_threshold_days": reported_threshold_days,
        "velocity_180d": velocity_180d,
        "capability_velocity_180d": velocity_180d,
        "reported_velocity_180d": reported_velocity_180d,
        "cost_per_task": cost,
        "coverage": {"value": coverage, "represented_organizations": coverage_orgs, "panel_size": len(REFERENCE_ORGANIZATION_NAMES), "status": "high" if coverage >= 0.7 else "medium" if coverage >= 0.4 else "low"},
        "unavailable": ["T80: not included in the first vertical slice"],
        "resource_ids": [benchmark_resource_id],
        "date_policy": "Primary lifecycle time uses the earliest available date among evaluation/run time, model release time, and the earliest recorded score-publication time for the same observation. Plot dates and T50/T80/T90 are clipped at benchmark release, so lifecycle durations are never negative; original dates remain preserved for provenance.",
        "historical_frontier_status": "unknown_public_dates" if not reported_frontier else "available",
        "timeline_default": "capability",
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    resources, models = {}, {}
    evidence_records = []
    benchmarks = [build_benchmark(spec, resources, models, evidence_records) for spec in BENCHMARKS]
    for panel_model in REFERENCE_MODEL_RELEASES:
        release_resource_id = model_release_resource(resources, panel_model["canonical_name"])
        panel_identity_organization = organization_identity(panel_model["organization"])
        panel_id = stable_id("model", panel_identity_organization, slug(panel_model["canonical_name"]))
        model = models.setdefault(panel_id, {
            "id": panel_id,
            "canonical_name": panel_model["canonical_name"],
            "aliases": [],
            "configuration_id": panel_model["canonical_name"],
            "identity_organization": panel_identity_organization,
            "family_id": panel_model["family_id"],
            "release_date": panel_model["release_date"],
            "organization": panel_model["organization"],
            "resource_ids": [release_resource_id] if release_resource_id else [],
            "roles": [panel_model["role"]],
            "domains": [panel_model["domain"]],
            "evaluation_types": ["Model"],
            "inclusion_reason": "Included as a current frontier reference-panel release anchor; benchmark scores are added only when authoritative results are available.",
            "provenance_note": "Official release/model resource is preserved even when no score is yet available in the curated benchmark set.",
        })
        if panel_model["role"] not in model["roles"]:
            model["roles"].append(panel_model["role"])
        if release_resource_id and release_resource_id not in model["resource_ids"]:
            model["resource_ids"].append(release_resource_id)
    snapshot_date = BUILD_DATE
    payload = {
        "schema_version": 2,
        "snapshot_id": BUILD_DATE.isoformat(),
        "source": "Curated benchmark exports; see resource registry for source lineage",
        "reference_organizations": list(REFERENCE_ORGANIZATIONS),
        "capability_labels": CAPABILITY_LABELS,
        "resources": sorted(resources.values(), key=lambda item: item["id"]),
        "models": sorted(models.values(), key=lambda item: item["id"]),
        "benchmarks": benchmarks,
        "lifecycle_views": lifecycle_view_ids(benchmarks, snapshot_date),
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    write_public_data_bundles(payload)
    RESOURCE_OUT.write_text(json.dumps(payload["resources"], indent=2) + "\n")
    MODEL_OUT.write_text(json.dumps(payload["models"], indent=2) + "\n")
    observations = [observation for benchmark in benchmarks for observation in benchmark["observations"]]
    OBSERVATION_OUT.write_text("".join(json.dumps(observation, sort_keys=True) + "\n" for observation in observations))
    EVIDENCE_OUT.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in evidence_records))
    print(f"Wrote {OUT} ({len(payload['benchmarks'])} benchmarks)")


if __name__ == "__main__":
    main()
