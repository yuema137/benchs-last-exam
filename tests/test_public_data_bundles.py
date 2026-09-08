import hashlib
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "site" / "data"
SNAPSHOT = DATA / "benchmarks.json"
INDEX = DATA / "index.json"
DETAILS = DATA / "benchmarks"
RESOURCES = DATA / "resources.json"


def public_hashes():
    paths = [INDEX, RESOURCES, *sorted(DETAILS.glob("*.json"))]
    return {path.relative_to(DATA).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


class PublicDataBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = json.loads(SNAPSHOT.read_text())
        cls.index = json.loads(INDEX.read_text())

    def test_index_contains_every_benchmark_without_detail_payloads(self):
        self.assertEqual(self.index["capability_labels"], self.snapshot["capability_labels"])
        self.assertEqual(
            [item["id"] for item in self.index["benchmarks"]],
            [item["id"] for item in self.snapshot["benchmarks"]],
        )
        forbidden = {"observations", "frontier", "capability_frontier", "resources", "models"}
        for item in self.index["benchmarks"]:
            self.assertFalse(forbidden & set(item), item["id"])
            self.assertEqual(item["detail_path"], f"benchmarks/{item['id']}.json")

    def test_each_index_card_has_one_exact_detail_record(self):
        full = {item["id"]: item for item in self.snapshot["benchmarks"]}
        self.assertEqual(len(list(DETAILS.glob("*.json"))), len(full))
        for benchmark_id, benchmark in full.items():
            detail = json.loads((DETAILS / f"{benchmark_id}.json").read_text())
            self.assertEqual(detail["bundle_kind"], "benchmark_detail")
            self.assertEqual(detail["benchmark"], benchmark)

    def test_frontend_loads_index_then_one_detail_on_demand(self):
        app = (ROOT / "site" / "app.js").read_text()
        self.assertIn('fetch("data/index.json', app)
        self.assertIn("summary.detail_path", app)
        self.assertIn('fetch("data/resources.json', app)
        self.assertNotIn('fetch("data/benchmarks.json', app)

    def test_every_detail_navigation_invalidates_an_older_request(self):
        app = (ROOT / "site" / "app.js").read_text()
        function = app[app.index("async function showDetail"):app.index("const renderLeaderboardTable")]
        self.assertLess(
            function.index("const request=++state.detailRequest"),
            function.index("const cached=state.detailCache.get(id)"),
        )

    def test_resource_registry_matches_canonical_resources(self):
        resources = json.loads(RESOURCES.read_text())
        self.assertEqual(resources["bundle_kind"], "resource_registry")
        self.assertEqual(resources["resources"], self.snapshot["resources"])

    def test_public_data_generation_is_reproducible(self):
        before = public_hashes()
        subprocess.run(["python3", "scripts/build_snapshot.py"], cwd=ROOT, check=True)
        self.assertEqual(public_hashes(), before)


if __name__ == "__main__":
    unittest.main()
