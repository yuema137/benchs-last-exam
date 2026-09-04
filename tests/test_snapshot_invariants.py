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

    def test_frontier_panel_has_release_resource_for_each_anchor(self):
        payload = json.loads(SNAPSHOT.read_text())
        resources = {resource["id"]: resource for resource in payload["resources"]}
        expected = {
            "Claude Fable 5.1": "https://www.anthropic.com/claude/fable",
            "GPT-6 Astra": "https://developers.openai.com/api/docs/models/gpt-6-astra",
            "Gemini 3.8 Flash": "https://deepmind.google/models/model-cards/gemini-3-8-flash/",
            "DeepSeek-V4-Pro-0813": "https://api-docs.deepseek.com/news/news260813/",
            "Qwen3.8-Max": "https://docs.modelstudio.console.alibabacloud.com/en/model-studio/qwen3-8-max",
            "Llama 4 Maverick": "https://ai.meta.com/llama/get-started/",
            "Grok 4.6": "https://x.ai/news/grok-4-6",
        }
        anchors = {name: next((model for model in payload["models"] if model["canonical_name"] == name), None) for name in expected}
        self.assertTrue(all(anchors.values()))
        for name, url in expected.items():
            model = anchors[name]
            model_urls = {resources[resource_id]["url"] for resource_id in model["resource_ids"]}
            self.assertIn(url, model_urls, name)

    def test_every_benchmark_has_complete_detail_metadata(self):
        payload = json.loads(SNAPSHOT.read_text())
        for benchmark in payload["benchmarks"]:
            self.assertTrue(benchmark.get("summary", {}).get("en"), benchmark["id"])
            self.assertTrue(benchmark.get("summary", {}).get("zh"), benchmark["id"])
            self.assertTrue(benchmark.get("task_format", {}).get("en"), benchmark["id"])
            self.assertTrue(benchmark.get("task_format", {}).get("zh"), benchmark["id"])
            self.assertTrue(benchmark.get("scoring", {}).get("metric_name"), benchmark["id"])
            self.assertTrue(benchmark.get("scoring", {}).get("explanation", {}).get("en"), benchmark["id"])
            self.assertTrue(benchmark.get("scoring", {}).get("explanation", {}).get("zh"), benchmark["id"])
            self.assertIn(benchmark.get("evaluation_target"), {"final_output", "environment_outcome", "process_and_output"})


if __name__ == "__main__":
    unittest.main()
