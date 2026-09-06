#!/usr/bin/env python3
"""Write a compact audit of evidence-to-measurement reconciliation."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "site" / "data" / "benchmarks.json"
EVIDENCE = ROOT / "data" / "evidence.jsonl"
REPORT = ROOT / "docs" / "CANONICAL_IDENTITY_AUDIT.md"


def main():
    payload = json.loads(SNAPSHOT.read_text())
    evidence = [json.loads(line) for line in EVIDENCE.read_text().splitlines() if line]
    observations = [item for benchmark in payload["benchmarks"] for item in benchmark["observations"]]
    merged = [item for item in observations if item["evidence_count"] > 1]
    lines = [
        "# Canonical Identity Audit",
        "",
        f"Snapshot: `{payload['snapshot_id']}` · schema version `{payload['schema_version']}`",
        "",
        "A source row is preserved as evidence. Exact duplicate measurements may share one canonical observation; model/display setting, protocol, task set, score series, and score must all match.",
        "",
        f"- Source evidence records: **{len(evidence)}**",
        f"- Canonical measurements: **{len(observations)}**",
        f"- Measurements with multiple evidence records: **{len(merged)}**",
        f"- Duplicate evidence rows reconciled: **{len(evidence) - len(observations)}**",
        f"- Canonical models: **{len(payload['models'])}**",
        f"- Canonical resources: **{len(payload['resources'])}**",
        "",
        "## Reconciliation by benchmark",
        "",
        "| Benchmark | Evidence | Measurements | Merged rows |",
        "|---|---:|---:|---:|",
    ]
    for benchmark in sorted(payload["benchmarks"], key=lambda item: item["name"].casefold()):
        evidence_count = benchmark["evidence_record_count"]
        measurement_count = benchmark["observation_count"]
        if evidence_count != measurement_count:
            lines.append(
                f"| {benchmark['name']} | {evidence_count} | {measurement_count} | {evidence_count - measurement_count} |"
            )
    REPORT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {REPORT} ({len(evidence)} evidence records -> {len(observations)} measurements)")


if __name__ == "__main__":
    main()
