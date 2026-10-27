"""Data provenance policy: benchmark-radar may only appear as a discovery source."""
import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_provenance import (
    SNAPSHOT,
    benchmark_radar_input_violations,
    benchmark_radar_violations,
    is_benchmark_radar_url,
)


def payload(resources, observations):
    return {"resources": resources, "benchmarks": [{"id": "demo", "observations": observations}]}


PAPER = {"id": "resource-paper", "url": "https://arxiv.org/abs/2401.00001", "title": "Demo paper", "publisher": "Benchmark authors"}
RADAR = {"id": "resource-radar", "url": "https://benchmark-radar.org/benchmarks/demo", "title": "Demo", "publisher": "Aggregator"}
RADAR_REPO = {"id": "resource-radar-repo", "url": "https://github.com/ktwu01/benchmark-radar/blob/main/data/x.yml",
              "title": "Demo", "publisher": "Aggregator"}


class BenchmarkRadarPolicyTests(unittest.TestCase):
    def test_url_matching(self):
        for url in ("https://benchmark-radar.org", "https://www.benchmark-radar.org/data/benchmark-index.json",
                    "https://github.com/ktwu01/benchmark-radar", "https://GitHub.com/ktwu01/benchmark-radar/tree/main"):
            self.assertTrue(is_benchmark_radar_url(url), url)
        for url in ("https://github.com/ktwu01/other-project", "https://arxiv.org/abs/2401.00001", "", None):
            self.assertFalse(is_benchmark_radar_url(url), url)

    def test_original_source_passes(self):
        self.assertEqual(benchmark_radar_violations(payload([PAPER], [{"observation_id": "o1", "source_ids": ["resource-paper"]}])), [])

    def test_radar_as_only_source_fails(self):
        for resource in (RADAR, RADAR_REPO):
            errors = benchmark_radar_violations(payload([resource], [{"observation_id": "o1", "source_ids": [resource["id"]]}]))
            self.assertTrue(any("o1: only cited source is benchmark-radar" in error for error in errors), errors)

    def test_radar_as_additional_cited_source_still_fails(self):
        errors = benchmark_radar_violations(payload(
            [PAPER, RADAR], [{"observation_id": "o1", "source_ids": ["resource-paper", "resource-radar"]}]))
        self.assertFalse(any("only cited source" in error for error in errors), errors)
        self.assertTrue(any("outside a discovery-source field" in error for error in errors), errors)

    def test_mentions_outside_discovery_field_fail(self):
        for observation in ({"observation_id": "o1", "source_ids": ["resource-paper"], "notes": "Copied from Benchmark Radar"},
                            {"observation_id": "o1", "source_ids": ["resource-paper"], "source": "benchmark-radar.org"}):
            errors = benchmark_radar_violations(payload([PAPER], [observation]))
            self.assertTrue(errors, observation)

    def test_explicit_discovery_field_is_allowed(self):
        observation = {"observation_id": "o1", "source_ids": ["resource-paper"],
                       "discovered_via": {"source": "benchmark-radar", "url": "https://benchmark-radar.org/x"}}
        self.assertEqual(benchmark_radar_violations(payload([PAPER], [observation])), [])

    def test_raw_csv_rows_are_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data" / "raw").mkdir(parents=True)
            (root / "data" / "benchmarks").mkdir(parents=True)
            with (root / "data" / "raw" / "demo.csv").open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["Name", "Score", "Source link", "Discovered via"])
                writer.writerow(["Model A", "0.5", "https://arxiv.org/abs/2401.00001", "https://benchmark-radar.org/x"])
                writer.writerow(["Model B", "0.6", "https://github.com/ktwu01/benchmark-radar", ""])
            (root / "data" / "benchmarks" / "demo.json").write_text(json.dumps({"id": "demo", "summary": "ok"}))
            errors = benchmark_radar_input_violations(root)
            self.assertEqual(len(errors), 1, errors)
            self.assertIn("row 2", errors[0])

    def test_published_snapshot_and_inputs_comply(self):
        self.assertEqual(benchmark_radar_violations(json.loads(SNAPSHOT.read_text())), [])
        self.assertEqual(benchmark_radar_input_violations(), [])


if __name__ == "__main__":
    unittest.main()
