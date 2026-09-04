#!/usr/bin/env python3
"""Validate resource and observation lineage in the generated static snapshot."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "site" / "data" / "benchmarks.json"
REPORT = ROOT / "docs" / "PROVENANCE_GAPS.md"


def main():
    payload = json.loads(SNAPSHOT.read_text())
    resources = {item["id"]: item for item in payload.get("resources", [])}
    models = {item["id"]: item for item in payload.get("models", [])}
    errors = []
    gaps = []
    for benchmark in payload["benchmarks"]:
        threshold_days = benchmark.get("threshold_days", {})
        finite_thresholds = {
            name: item.get("days") for name, item in threshold_days.items()
            if item.get("status") in {"at_release", "reached"} and item.get("days") is not None
        }
        for lower, higher in (("T50", "T80"), ("T80", "T90"), ("T50", "T90")):
            if lower in finite_thresholds and higher in finite_thresholds and finite_thresholds[higher] < finite_thresholds[lower]:
                errors.append(f"{benchmark['id']}: {higher} ({finite_thresholds[higher]}) precedes {lower} ({finite_thresholds[lower]})")
        for resource_id in benchmark.get("resource_ids", []):
            if resource_id not in resources:
                errors.append(f"{benchmark['id']}: missing benchmark resource {resource_id}")
        observation_ids = {item["observation_id"] for item in benchmark["observations"]}
        observations_by_id = {item["observation_id"]: item for item in benchmark["observations"]}
        frontier_ids = set()
        for observation in benchmark["observations"]:
            if not observation.get("source_ids"):
                errors.append(f"{observation['observation_id']}: no source_ids")
            for source_id in observation.get("source_ids", []):
                if source_id not in resources:
                    errors.append(f"{observation['observation_id']}: missing resource {source_id}")
            if observation.get("model_id") not in models:
                errors.append(f"{observation['observation_id']}: missing model {observation.get('model_id')}")
            if observation.get("result_public_date") is None:
                gaps.append(f"{observation['observation_id']}: result_public_date is unknown")
        frontier_lists = {
            "frontier": benchmark.get("frontier", []),
            "frontier_events": benchmark.get("frontier_events", []),
            "capability_frontier": benchmark.get("capability_frontier", []),
            "reported_frontier": benchmark.get("reported_frontier", []),
        }
        for frontier_name, frontier_points in frontier_lists.items():
            point_ids = set()
            for point in frontier_points:
                observation_id = point.get("observation_id")
                point_ids.add(observation_id)
                if observation_id not in observation_ids:
                    errors.append(f"{benchmark['id']}: {frontier_name} point is not a canonical observation: {observation_id}")
                elif point.get("source_ids", []) != observations_by_id[observation_id].get("source_ids", []):
                    errors.append(f"{benchmark['id']} {frontier_name} {observation_id}: source lineage differs from observation")
                for source_id in point.get("source_ids", []):
                    if source_id not in resources:
                        errors.append(f"{benchmark['id']} {frontier_name} {observation_id}: missing resource {source_id}")
            if len(point_ids) != len(frontier_points):
                errors.append(f"{benchmark['id']}: duplicate {frontier_name} observation IDs")
        for point in benchmark.get("frontier", []):
            observation_id = point.get("observation_id")
            frontier_ids.add(observation_id)
        if len(frontier_ids) != len(benchmark.get("frontier", [])):
            errors.append(f"{benchmark['id']}: duplicate frontier observation IDs")
    REPORT.write_text("# Provenance Gaps\n\n" +
                      "The generated pilot snapshot passes structural lineage validation.\n\n" +
                      "Known evidence gaps:\n\n" +
                      "\n".join(f"- {gap}" for gap in gaps[:40]) +
                      (f"\n\n...and {len(gaps) - 40} more.\n" if len(gaps) > 40 else "\n") +
                      "\nThese gaps are preserved as unknown values; no source or date is fabricated.\n")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(payload['benchmarks'])} benchmarks, {len(models)} models, "
          f"{len(resources)} resources, and {sum(len(b['observations']) for b in payload['benchmarks'])} observations.")
    print(f"Documented {len(gaps)} observations with unknown result_public_date in {REPORT}.")


if __name__ == "__main__":
    main()
