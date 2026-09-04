#!/usr/bin/env python3
"""Build the small static benchmark snapshot used by the local site."""

import csv
import json
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "site" / "data" / "benchmarks.json"

BENCHMARKS = [
    {"id": "mmlu", "name": "MMLU", "domain": "General knowledge", "file": "mmlu_external.csv", "score": "EM", "release": "2020-09-07", "floor": 0.25, "ceiling": 1.0, "source": "https://arxiv.org/abs/2009.03300", "summary": {"en": "MMLU tests broad knowledge across academic and professional subjects.", "zh": "MMLU 测试模型在多个学术和专业领域里的综合知识。"}, "task_format": {"en": "Each item is a four-choice multiple-choice question. The model selects one answer.", "zh": "每个 task 都是四选一问题，模型需要选出一个答案。"}, "scoring": {"metric_name": "Exact-match accuracy", "explanation": {"en": "A response is correct only when the selected answer matches the answer key. The score is the fraction of questions answered correctly.", "zh": "只有模型选中的答案和标准答案一致，这道题才算答对。分数就是答对题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "gsm8k", "name": "GSM8K", "domain": "Mathematics", "file": "gsm8k_external.csv", "score": "EM", "release": "2021-10-27", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2110.14168", "summary": {"en": "GSM8K tests whether a model can solve multi-step grade-school math word problems.", "zh": "GSM8K 测试模型能不能解决需要多步推理的小学数学应用题。"}, "task_format": {"en": "The model receives a natural-language math word problem and produces a solution with a final numerical answer.", "zh": "模型会收到一道自然语言数学应用题，需要给出解题过程和最后的数字答案。"}, "scoring": {"metric_name": "Exact-match accuracy", "explanation": {"en": "The final numerical answer must match the reference answer. The score is the percentage of problems answered correctly.", "zh": "最后的数字答案必须和标准答案一致。分数就是答对题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "math-level-5", "name": "MATH Level 5", "domain": "Mathematics", "file": "math_level_5.csv", "score": "Best score (across scorers)", "release": "2021-03-05", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2103.03874", "summary": {"en": "MATH Level 5 is the hardest level of a competition-math dataset, intended to test difficult mathematical problem solving.", "zh": "MATH Level 5 是竞赛数学数据集里最难的一档，用来测试模型解决高难度数学题的能力。"}, "task_format": {"en": "The model receives a competition-style math problem and must produce a solution and final answer.", "zh": "模型会收到一道竞赛数学题，需要给出解答和最后答案。"}, "scoring": {"metric_name": "Answer accuracy", "explanation": {"en": "A problem counts as correct when the reported answer matches the reference answer under the benchmark scorer. The score is the fraction of correct problems.", "zh": "按照 benchmark scorer 的规则，模型答案和标准答案一致时，这道题才算答对。分数就是答对题目占全部题目的比例。"}}, "evaluation_target": "final_output"},
    {"id": "gpqa-diamond", "name": "GPQA Diamond", "domain": "Science reasoning", "file": "gpqa_diamond.csv", "score": "Best score (across scorers)", "release": "2023-11-20", "floor": 0.25, "ceiling": 1.0, "source": "https://arxiv.org/abs/2311.12022", "summary": {"en": "GPQA Diamond tests difficult science reasoning questions written and checked by domain experts.", "zh": "GPQA Diamond 测试由领域专家编写和核验的高难度科学推理题。"}, "task_format": {"en": "Each item is a four-choice science question. The model selects one answer, usually without access to external tools in the reported score.", "zh": "每个 task 都是四选一科学问题，模型需要选一个答案；公开分数通常不包含外部工具使用。"}, "scoring": {"metric_name": "Accuracy", "explanation": {"en": "The score is the percentage of questions for which the selected option is correct. Four choices make 25% the random-choice reference point.", "zh": "分数就是选项正确的题目占全部题目的比例。因为每题有四个选项，25% 是随机选择的参考 floor。"}}, "evaluation_target": "final_output"},
    {"id": "swe-bench-verified", "name": "SWE-bench Verified", "domain": "Coding / agents", "file": "swe_bench_verified.csv", "score": "Best score (across scorers)", "release": "2024-08-13", "floor": 0.0, "ceiling": 1.0, "source": "https://openai.com/index/introducing-swe-bench-verified/", "summary": {"en": "SWE-bench Verified tests whether a coding agent can resolve real GitHub issues in a repository.", "zh": "SWE-bench Verified 测试 coding agent 能不能在真实代码仓库里修复 GitHub issue。"}, "task_format": {"en": "The agent receives a repository and issue description, edits files in an environment, and submits a patch. This is not a one-shot answer task.", "zh": "agent 会收到一个代码仓库和 issue 描述，在环境里修改文件并提交 patch。这不是只回答一次文本的问题。"}, "scoring": {"metric_name": "Issue resolution rate", "explanation": {"en": "A task counts as solved when the submitted patch passes the task's required tests. The score is the percentage of issues resolved.", "zh": "如果提交的 patch 通过这个 task 要求的测试，这个 task 才算解决。分数就是解决 issue 占全部 issue 的比例。"}}, "evaluation_target": "environment_outcome"},
]

REFERENCE_ORGANIZATIONS = {"OpenAI", "Anthropic", "Google", "DeepSeek", "Qwen", "Meta", "xAI"}


def parse_date(row):
    started = (row.get("Started at") or "")[:10]
    release = row.get("Release date") or ""
    return started or release or None, "evaluation_start" if started else "model_release_date"


def build_benchmark(spec):
    rows = []
    with (RAW / spec["file"]).open(newline="") as handle:
        for row in csv.DictReader(handle):
            try:
                score = float(row[spec["score"]])
            except (KeyError, TypeError, ValueError):
                continue
            event_date, date_kind = parse_date(row)
            if not event_date:
                continue
            model = row.get("Name") or row.get("Model version") or "Unknown model"
            source_url = row.get("Source link") or row.get("Logs") or spec["source"]
            rows.append({
                "model": model,
                "organization": row.get("Organization") or "Unknown",
                "score": score,
                "date": event_date,
                "date_kind": date_kind,
                "source": source_url,
            })
    rows.sort(key=lambda item: (item["date"], item["score"]))
    frontier = []
    best = None
    for row in rows:
        if best is None or row["score"] > best["score"]:
            best = row
            frontier.append({**row})
    current = max(rows, key=lambda row: row["score"]) if rows else None
    progress = None
    if current and spec["ceiling"] != spec["floor"]:
        progress = (current["score"] - spec["floor"]) / (spec["ceiling"] - spec["floor"])
        progress = max(0.0, min(1.0, progress))
    release = date.fromisoformat(spec["release"])
    threshold_days = {}
    for label, target in (("T50", 0.5), ("T90", 0.9)):
        crossing = next((p for p in frontier if (p["score"] - spec["floor"]) / (spec["ceiling"] - spec["floor"]) >= target), None)
        threshold_days[label] = {"status": "reached", "days": (date.fromisoformat(crossing["date"]) - release).days} if crossing else {"status": "right_censored", "days": (date.fromisoformat(rows[-1]["date"]) - release).days}
    latest_frontier = frontier[-1] if frontier else None
    velocity_180d = None
    if latest_frontier:
        latest_date = date.fromisoformat(latest_frontier["date"])
        prior = next((p for p in reversed(frontier[:-1]) if (latest_date - date.fromisoformat(p["date"])).days >= 180), None)
        if prior:
            elapsed = (latest_date - date.fromisoformat(prior["date"])).days
            velocity_180d = (latest_frontier["score"] - prior["score"]) / elapsed * 30.44
    organizations = {row["organization"] for row in rows}
    coverage_orgs = sorted(organizations & REFERENCE_ORGANIZATIONS)
    coverage = len(coverage_orgs) / len(REFERENCE_ORGANIZATIONS)
    return {
        **{key: spec[key] for key in ("id", "name", "domain", "release", "floor", "ceiling", "source")},
        "metric": spec["score"],
        "summary": spec["summary"],
        "task_format": spec["task_format"],
        "scoring": spec["scoring"],
        "evaluation_target": spec["evaluation_target"],
        "observation_count": len(rows),
        "observations": rows,
        "frontier": frontier,
        "observed_frontier": current["score"] if current else None,
        "current_frontier": current["score"] if current else None,
        "normalized_progress": progress,
        "normalized_headroom": None if progress is None else 1 - progress,
        "threshold_days": threshold_days,
        "velocity_180d": velocity_180d,
        "coverage": {"value": coverage, "represented_organizations": coverage_orgs, "panel_size": len(REFERENCE_ORGANIZATIONS), "status": "high" if coverage >= 0.7 else "medium" if coverage >= 0.4 else "low"},
        "unavailable": ["T80: not included in the first vertical slice"],
        "date_policy": "Use evaluation start when available; otherwise model release date. This is a provisional historical ordering policy.",
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {"snapshot_id": datetime.now().strftime("%Y-%m-%d"), "source": "Epoch AI benchmark export", "benchmarks": [build_benchmark(spec) for spec in BENCHMARKS]}
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {OUT} ({len(payload['benchmarks'])} benchmarks)")


if __name__ == "__main__":
    main()
