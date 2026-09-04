import json
import unittest
from datetime import date
from pathlib import Path


SNAPSHOT = Path(__file__).resolve().parents[1] / "site" / "data" / "benchmarks.json"


class SnapshotInvariantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.benchmarks = json.loads(SNAPSHOT.read_text())["benchmarks"]

    def test_benchmarks_use_the_two_level_taxonomy(self):
        allowed_types = {"Model", "Agent"}
        for benchmark in self.benchmarks:
            self.assertIn(benchmark["evaluation_type"], allowed_types)
            self.assertTrue(benchmark["domain"])

    def test_higher_thresholds_never_precede_lower_thresholds(self):
        for benchmark in self.benchmarks:
            thresholds = benchmark["threshold_days"]
            finite = {
                name: item["days"]
                for name, item in thresholds.items()
                if item.get("status") in {"at_release", "reached"}
            }
            if all(name in finite for name in ("T50", "T90")):
                self.assertGreaterEqual(finite["T90"], finite["T50"], benchmark["name"])

    def test_right_censored_thresholds_use_snapshot_age(self):
        payload = json.loads(SNAPSHOT.read_text())
        snapshot_date = date.fromisoformat(payload["snapshot_id"])
        for benchmark in self.benchmarks:
            for item in benchmark["threshold_days"].values():
                if item.get("status") == "right_censored":
                    release = date.fromisoformat(benchmark["release"])
                    self.assertEqual(item["days"], max(0, (snapshot_date - release).days), benchmark["name"])

    def test_every_benchmark_has_a_resolvable_detail_record(self):
        payload = json.loads(SNAPSHOT.read_text())
        resources = {resource["id"] for resource in payload["resources"]}
        for benchmark in self.benchmarks:
            self.assertTrue(benchmark["name"], benchmark["id"])
            self.assertTrue(benchmark["source"], benchmark["id"])
            self.assertTrue(benchmark["resource_ids"], benchmark["id"])
            self.assertTrue(set(benchmark["resource_ids"]).issubset(resources), benchmark["id"])
            self.assertTrue(benchmark["observations"], benchmark["id"])

    def test_recent_frontier_models_have_official_release_resources(self):
        payload = json.loads(SNAPSHOT.read_text())
        resources = {resource["id"]: resource["url"] for resource in payload["resources"]}
        models = [model for model in payload["models"] if any(
            marker in model["canonical_name"].lower() for marker in ("fable 5.1", "gpt-6-astra")
        )]
        self.assertTrue(models)
        for model in models:
            self.assertTrue(any(resources.get(resource_id) in {
                "https://www.anthropic.com/claude/fable",
                "https://developers.openai.com/api/docs/models/gpt-6-astra",
            } for resource_id in model["resource_ids"]), model["canonical_name"])


if __name__ == "__main__":
    unittest.main()
