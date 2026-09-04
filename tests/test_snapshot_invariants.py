import json
import unittest
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


if __name__ == "__main__":
    unittest.main()
