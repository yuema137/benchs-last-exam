#!/usr/bin/env python3
"""Write an auditable summary of observation-date selection and clipping."""

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "site" / "data" / "benchmarks.json"
REPORT = ROOT / "docs" / "OBSERVATION_DATE_AUDIT.md"


def main():
    payload = json.loads(SNAPSHOT.read_text())
    observations = [item for benchmark in payload["benchmarks"] for item in benchmark["observations"]]
    selected_kinds = Counter(
        "+".join(source["kind"] for source in item.get("observation_date_sources", [])) or "unknown"
        for item in observations
    )
    pre_release = sum(
        bool(item.get("observation_date") and item["observation_date"] < benchmark["release"])
        for benchmark in payload["benchmarks"]
        for item in benchmark["observations"]
    )
    lines = [
        "# Observation Date Audit",
        "",
        f"Snapshot: `{payload['snapshot_id']}`",
        "",
        "The lifecycle date for one observation is the earliest available evaluation/run date, model release date, or score-publication date. The plotted date is clipped to benchmark release; source dates are never overwritten.",
        "",
        f"- Observations: **{len(observations)}**",
        f"- Observations without any candidate date: **{selected_kinds['unknown']}**",
        f"- Observations selected before benchmark release and plotted as `At release`: **{pre_release}**",
        "",
        "## Selected earliest-date evidence",
        "",
        "| Selected source kind(s) | Observations |",
        "|---|---:|",
    ]
    lines.extend(f"| `{kind}` | {count} |" for kind, count in selected_kinds.most_common())
    lines.extend([
        "",
        "## Benchmark coverage",
        "",
        "| Benchmark | Observations | Dated | Pre-release | Frontier events |",
        "|---|---:|---:|---:|---:|",
    ])
    for benchmark in sorted(payload["benchmarks"], key=lambda item: item["name"].casefold()):
        rows = benchmark["observations"]
        dated = sum(bool(item.get("observation_date")) for item in rows)
        before = sum(bool(item.get("observation_date") and item["observation_date"] < benchmark["release"]) for item in rows)
        lines.append(f"| {benchmark['name']} | {len(rows)} | {dated} | {before} | {len(benchmark['frontier_events'])} |")
    REPORT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {REPORT} ({len(observations)} observations)")


if __name__ == "__main__":
    main()
