#!/usr/bin/env python3
"""Build the small static benchmark snapshot used by the local site."""

import csv
import json
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "site" / "data" / "benchmarks.json"
RESOURCE_OUT = ROOT / "data" / "resources.json"
OBSERVATION_OUT = ROOT / "data" / "observations.jsonl"
MODEL_OUT = ROOT / "data" / "models.json"

BENCHMARKS = [
    {"id": "mmlu", "name": "MMLU", "domain": "General knowledge", "file": "mmlu_external.csv", "score": "EM", "release": "2020-09-07", "floor": 0.25, "ceiling": 1.0, "source": "https://arxiv.org/abs/2009.03300", "summary": {"en": "MMLU tests broad knowledge across academic and professional subjects.", "zh": "MMLU 测试模型在多个学术和专业领域里的综合知识。"}, "task_format": {"en": "Each item is a four-choice multiple-choice question. The model selects one answer.", "zh": "每个 task 都是四选一问题，模型需要选出一个答案。"}, "scoring": {"metric_name": "Exact-match accuracy", "explanation": {"en": "A response is correct only when the selected answer matches the answer key. The score is the fraction of questions answered correctly.", "zh": "只有模型选中的答案和标准答案一致，这道题才算答对。分数就是答对题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "gsm8k", "name": "GSM8K", "domain": "Mathematics", "file": "gsm8k_external.csv", "score": "EM", "release": "2021-10-27", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2110.14168", "summary": {"en": "GSM8K tests whether a model can solve multi-step grade-school math word problems.", "zh": "GSM8K 测试模型能不能解决需要多步推理的小学数学应用题。"}, "task_format": {"en": "The model receives a natural-language math word problem and produces a solution with a final numerical answer.", "zh": "模型会收到一道自然语言数学应用题，需要给出解题过程和最后的数字答案。"}, "scoring": {"metric_name": "Exact-match accuracy", "explanation": {"en": "The final numerical answer must match the reference answer. The score is the percentage of problems answered correctly.", "zh": "最后的数字答案必须和标准答案一致。分数就是答对题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "math-level-5", "name": "MATH Level 5", "domain": "Mathematics", "file": "math_level_5.csv", "score": "Best score (across scorers)", "release": "2021-03-05", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2103.03874", "summary": {"en": "MATH Level 5 is the hardest level of a competition-math dataset, intended to test difficult mathematical problem solving.", "zh": "MATH Level 5 是竞赛数学数据集里最难的一档，用来测试模型解决高难度数学题的能力。"}, "task_format": {"en": "The model receives a competition-style math problem and must produce a solution and final answer.", "zh": "模型会收到一道竞赛数学题，需要给出解答和最后答案。"}, "scoring": {"metric_name": "Answer accuracy", "explanation": {"en": "A problem counts as correct when the reported answer matches the reference answer under the benchmark scorer. The score is the fraction of correct problems.", "zh": "按照 benchmark scorer 的规则，模型答案和标准答案一致时，这道题才算答对。分数就是答对题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "gpqa-diamond", "name": "GPQA Diamond", "domain": "Science reasoning", "file": "gpqa_diamond.csv", "score": "Best score (across scorers)", "release": "2023-11-20", "floor": 0.25, "ceiling": 1.0, "source": "https://arxiv.org/abs/2311.12022", "summary": {"en": "GPQA Diamond tests difficult science reasoning questions written and checked by domain experts.", "zh": "GPQA Diamond 测试由领域专家编写和核验的高难度科学推理题。"}, "task_format": {"en": "Each item is a four-choice science question. The model selects one answer, usually without access to external tools in the reported score.", "zh": "每个 task 都是四选一科学问题，模型需要选一个答案；公开分数通常不包含外部工具使用。"}, "scoring": {"metric_name": "Accuracy", "explanation": {"en": "The score is the percentage of questions for which the selected option is correct. Four choices make 25% the random-choice reference point.", "zh": "分数就是选项正确的题目占全部题目的比例。因为每题有四个选项，25% 是随机选择的参考 floor。"}}, "evaluation_target": "final_output"},
    {"id": "swe-bench-verified", "name": "SWE-bench Verified", "domain": "Coding / agents", "file": "swe_bench_verified.csv", "score": "Best score (across scorers)", "release": "2024-08-13", "floor": 0.0, "ceiling": 1.0, "source": "https://openai.com/index/introducing-swe-bench-verified/", "summary": {"en": "SWE-bench Verified tests whether a coding agent can resolve real GitHub issues in a repository.", "zh": "SWE-bench Verified 测试 coding agent 能不能在真实代码仓库里修复 GitHub issue。"}, "task_format": {"en": "The agent receives a repository and issue description, edits files in an environment, and submits a patch. This is not a one-shot answer task.", "zh": "agent 会收到一个代码仓库和 issue 描述，在环境里修改文件并提交 patch。这不是只回答一次文本的问题。"}, "scoring": {"metric_name": "Issue resolution rate", "explanation": {"en": "A task counts as solved when the submitted patch passes the task's required tests. The score is the percentage of issues resolved.", "zh": "如果提交的 patch 通过这个 task 要求的测试，这个 task 才算解决。分数就是解决 issue 占全部 issue 的比例。"}}, "evaluation_target": "environment_outcome"},
]

REFERENCE_ORGANIZATIONS = {"OpenAI", "Anthropic", "Google", "DeepSeek", "Qwen", "Meta", "xAI"}

for _spec in BENCHMARKS:
    _spec.setdefault("metric_id", f"{_spec['id']}-metric-v1")
    _spec.setdefault("protocol_id", f"{_spec['id']}-source-export-v1")
    _spec.setdefault("protocol", "Source export protocol; row-level protocol details are preserved when available.")


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def register_resource(resources, url, title, *, resource_type="other", publisher=None,
                      authority="trusted_secondary", scope=("benchmark", "model"),
                      notes=None):
    resource_id = f"resource-{slug(url)}"
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


def model_family(model, organization):
    return slug(f"{organization}-{re.sub(r'\\s*\\([^)]*\\)', '', model)}")


def parse_dates(row):
    evaluation_date = (row.get("Started at") or "")[:10] or None
    model_release_date = row.get("Release date") or None
    return evaluation_date, model_release_date


def build_frontier(rows, date_field, date_meaning):
    """Build a deterministic, step-function frontier from canonical observations.

    Observations sharing a date are evaluated as one cohort. The winning
    observation retains the lineage of the score that established the event;
    the cohort IDs document the other observations considered at that date.
    """
    cohorts = {}
    for row in rows:
        event_date = row.get(date_field)
        if event_date:
            cohorts.setdefault(event_date, []).append(row)
    frontier = []
    best_score = None
    for event_date in sorted(cohorts):
        cohort = sorted(cohorts[event_date], key=lambda item: (item["score"], item["observation_id"]))
        winner = cohort[-1]
        if best_score is None or winner["score"] > best_score:
            event = {**winner}
            event["plot_date"] = event_date
            event["date"] = event_date
            event["date_kind"] = date_meaning
            event["frontier_observation_ids"] = [item["observation_id"] for item in cohort]
            frontier.append(event)
            best_score = winner["score"]
    return frontier


def threshold_metrics(frontier, release, floor, ceiling):
    result = {}
    if floor is None or ceiling is None or ceiling == floor:
        for label in ("T50", "T80", "T90"):
            result[label] = {"status": "not_applicable", "reason": "No defensible fixed floor and ceiling."}
        return result
    for label, target in (("T50", 0.5), ("T80", 0.8), ("T90", 0.9)):
        crossing = next((point for point in frontier if (point["score"] - floor) / (ceiling - floor) >= target), None)
        if crossing:
            result[label] = {"status": "reached", "days": (date.fromisoformat(crossing["plot_date"]) - release).days}
        elif frontier:
            result[label] = {"status": "right_censored", "days": (date.fromisoformat(frontier[-1]["plot_date"]) - release).days}
        else:
            result[label] = {"status": "unknown", "reason": "No dated observations are available on this timeline."}
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


def build_benchmark(spec, resources, models):
    benchmark_resource_id = register_resource(
        resources, spec["source"], f"{spec['name']} primary source", resource_type="paper",
        publisher="Benchmark authors", authority="primary", scope=("benchmark",),
    )
    rows = []
    with (RAW / spec["file"]).open(newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                score = float(row[spec["score"]])
            except (KeyError, TypeError, ValueError):
                continue
            evaluation_date, model_release_date = parse_dates(row)
            model = row.get("Name") or row.get("Model version") or "Unknown model"
            source_url = row.get("Source link") or row.get("Logs") or spec["source"]
            source_is_benchmark_primary = source_url == spec["source"]
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
            model_id = f"model-{slug(model)}"
            family_id = model_family(model, row.get("Organization") or "unknown")
            is_math_retro = spec["id"] == "math-level-5"
            retrospective = is_math_retro or bool(
                evaluation_date and model_release_date and evaluation_date > model_release_date
            )
            models.setdefault(model_id, {
                "id": model_id,
                "canonical_name": model,
                "family_id": family_id,
                "release_date": model_release_date,
                "organization": row.get("Organization") or "Unknown",
                "resource_ids": [source_id],
                "roles": ["contemporary_frontier"],
                "domains": [spec["domain"]],
                "inclusion_reason": "Included as a representative observation in the curated pilot dataset.",
                "provenance_note": "The current export provides evaluation evidence but not a model-specific official resource.",
            })
            rows.append({
                "observation_id": f"obs-{spec['id']}-{row.get('id') or slug(model)}",
                "benchmark_id": spec["id"],
                "benchmark_version_id": f"{spec['id']}-canonical",
                "model_id": model_id,
                "model_family_id": family_id,
                "model": model,
                "organization": row.get("Organization") or "Unknown",
                "score": score,
                "metric_id": spec["metric_id"],
                "protocol_id": spec["protocol_id"],
                "metric": spec["score"],
                "evaluation_protocol": spec["protocol"],
                "model_release_date": model_release_date,
                "evaluation_date": evaluation_date,
                "result_public_date": None,
                "source_publication_date": None,
                "ingested_at": datetime.now().date().isoformat(),
                "date_precision": "day" if evaluation_date or model_release_date else None,
                "date_notes": "Result-public date is not present in the source export.",
                "date": evaluation_date or model_release_date,
                "date_kind": "evaluation_date" if evaluation_date else "unknown",
                "capability_date": model_release_date,
                "capability_date_meaning": "model_release_date",
                "reported_date_meaning": "result_public_date",
                "historical_frontier_date": None,
                "temporal_class": "retrospective_evaluation" if retrospective else "historical_or_unknown",
                "retrospective": retrospective,
                "capability_frontier_eligible": bool(model_release_date),
                "historical_frontier_eligible": False,
                "eligibility_reason": "Capability eligibility uses the model release date and the curated protocol; reported-result eligibility requires result_public_date.",
                "contemporaneous": not retrospective,
                "source_ids": [source_id, benchmark_resource_id] if source_id != benchmark_resource_id else [source_id],
                "source": source_url,
                "notes": "Operational evaluation timeline only; not a historical public-result date.",
            })
    capability_frontier = build_frontier(rows, "capability_date", "model release date")
    reported_frontier = build_frontier(
        [row for row in rows if row.get("result_public_date")],
        "result_public_date",
        "result first-public date",
    )
    current = capability_frontier[-1] if capability_frontier else None
    reported_current = reported_frontier[-1] if reported_frontier else None
    progress = None
    if current and spec["ceiling"] != spec["floor"]:
        progress = (current["score"] - spec["floor"]) / (spec["ceiling"] - spec["floor"])
        progress = max(0.0, min(1.0, progress))
    release = date.fromisoformat(spec["release"])
    threshold_days = threshold_metrics(capability_frontier, release, spec["floor"], spec["ceiling"])
    reported_threshold_days = threshold_metrics(reported_frontier, release, spec["floor"], spec["ceiling"])
    velocity_180d = frontier_velocity(capability_frontier)
    reported_velocity_180d = frontier_velocity(reported_frontier)
    organizations = {row["organization"] for row in rows}
    coverage_orgs = sorted(organizations & REFERENCE_ORGANIZATIONS)
    coverage = len(coverage_orgs) / len(REFERENCE_ORGANIZATIONS)
    return {
        **{key: spec[key] for key in ("id", "name", "domain", "release", "floor", "ceiling", "source")},
        "metric": spec["score"],
        "metric_id": spec["metric_id"],
        "protocol_id": spec["protocol_id"],
        "benchmark_version_id": f"{spec['id']}-canonical",
        "summary": spec["summary"],
        "task_format": spec["task_format"],
        "scoring": spec["scoring"],
        "evaluation_target": spec["evaluation_target"],
        "observation_count": len(rows),
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
        "coverage": {"value": coverage, "represented_organizations": coverage_orgs, "panel_size": len(REFERENCE_ORGANIZATIONS), "status": "high" if coverage >= 0.7 else "medium" if coverage >= 0.4 else "low"},
        "unavailable": ["T80: not included in the first vertical slice"],
        "resource_ids": [benchmark_resource_id],
        "date_policy": "Primary capability lifecycle metrics use model_release_date on protocol-compatible curated observations. Evaluation and result-public dates are preserved for provenance; they are not silently substituted into the capability timeline.",
        "historical_frontier_status": "unknown_public_dates" if not reported_frontier else "available",
        "timeline_default": "capability",
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    resources, models = {}, {}
    benchmarks = [build_benchmark(spec, resources, models) for spec in BENCHMARKS]
    payload = {
        "snapshot_id": datetime.now().strftime("%Y-%m-%d"),
        "source": "Curated benchmark exports; see resource registry for source lineage",
        "resources": sorted(resources.values(), key=lambda item: item["id"]),
        "models": sorted(models.values(), key=lambda item: item["id"]),
        "benchmarks": benchmarks,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    RESOURCE_OUT.write_text(json.dumps(payload["resources"], indent=2) + "\n")
    MODEL_OUT.write_text(json.dumps(payload["models"], indent=2) + "\n")
    observations = [observation for benchmark in benchmarks for observation in benchmark["observations"]]
    OBSERVATION_OUT.write_text("".join(json.dumps(observation, sort_keys=True) + "\n" for observation in observations))
    print(f"Wrote {OUT} ({len(payload['benchmarks'])} benchmarks)")


if __name__ == "__main__":
    main()
