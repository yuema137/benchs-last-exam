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
    {"id": "mmlu", "name": "MMLU", "domain": "General knowledge", "file": "mmlu_external.csv", "score": "EM", "release": "2020-09-07", "floor": 0.25, "ceiling": 1.0, "source": "https://arxiv.org/abs/2009.03300"},
    {"id": "gsm8k", "name": "GSM8K", "domain": "Mathematics", "file": "gsm8k_external.csv", "score": "EM", "release": "2021-10-27", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2110.14168"},
    {"id": "math-level-5", "name": "MATH Level 5", "domain": "Mathematics", "file": "math_level_5.csv", "score": "Best score (across scorers)", "release": "2021-03-05", "floor": 0.0, "ceiling": 1.0, "source": "https://arxiv.org/abs/2103.03874"},
    {"id": "gpqa-diamond", "name": "GPQA Diamond", "domain": "Science reasoning", "file": "gpqa_diamond.csv", "score": "Best score (across scorers)", "release": "2023-11-20", "floor": 0.25, "ceiling": 1.0, "source": "https://arxiv.org/abs/2311.12022"},
    {"id": "swe-bench-verified", "name": "SWE-bench Verified", "domain": "Coding / agents", "file": "swe_bench_verified.csv", "score": "Best score (across scorers)", "release": "2024-08-13", "floor": 0.0, "ceiling": 1.0, "source": "https://www.swebench.com/"},
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
        "metric": "accuracy-like score",
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
