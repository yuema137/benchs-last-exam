import json
import unittest
from datetime import date
from pathlib import Path

from scripts.validate_score_semantics import (
    REVIEWED_LARGE_NUMERIC_BENCHMARKS,
    REVIEWED_LOW_RATIO_BENCHMARKS,
)


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

    def test_cybench_ratio_scores_are_not_double_converted(self):
        benchmark = next(item for item in self.benchmarks if item["id"] == "cybench")
        self.assertEqual(benchmark["observation_count"], 24)
        self.assertEqual(benchmark["score_format"], "ratio")
        self.assertTrue(all(item["capability_frontier_eligible"] for item in benchmark["frontier_events"]))
        self.assertTrue(all(item["task_set_id"] == "cybench-canonical" for item in benchmark["frontier_events"]))
        excluded = [item for item in benchmark["observations"] if not item["capability_frontier_eligible"]]
        self.assertTrue(any(item["score"] == 1.0 for item in excluded))
        self.assertTrue(all(item["task_set_id"] == "cybench-subset-or-unverified" for item in excluded))

    def test_unbounded_metrics_are_not_rendered_as_percentage_scores(self):
        by_id = {item["id"]: item for item in self.benchmarks}
        for benchmark_id in ("metr-time-horizon-1-1", "gdpval-aa-v2", "vending-bench-2"):
            benchmark = by_id[benchmark_id]
            self.assertEqual(benchmark["score_format"], "number", benchmark_id)
            self.assertIsNone(benchmark["floor"], benchmark_id)
            self.assertIsNone(benchmark["ceiling"], benchmark_id)
            self.assertIsNone(benchmark["normalized_progress"], benchmark_id)

    def test_science_engineering_batch_is_fully_integrated(self):
        payload = json.loads(SNAPSHOT.read_text())
        by_id = {item["id"]: item for item in payload["benchmarks"]}
        expected = {
            "physreason", "olympiadbench-physics", "chemiq", "superchem-multimodal",
            "matscibench-v2", "atomworld-v4", "engibench-v2-level3", "eee-bench-v2",
            "labbench2-tableqa-pdf", "pg-llm-proteingym",
        }
        self.assertTrue(expected.issubset(by_id))
        for benchmark_id in expected:
            benchmark = by_id[benchmark_id]
            self.assertGreaterEqual(len(benchmark["coverage"]["represented_organizations"]), 2, benchmark_id)
            self.assertTrue(benchmark["frontier_events"], benchmark_id)
            self.assertTrue(benchmark["summary"]["en"], benchmark_id)
            self.assertTrue(benchmark["summary"]["zh"], benchmark_id)

    def test_multidomain_science_engineering_expansion_is_end_to_end(self):
        payload = json.loads(SNAPSHOT.read_text())
        by_id = {item["id"]: item for item in payload["benchmarks"]}
        expected = {
            "apbench-gamma", "cadreview-human-feedback", "controlbench",
            "circuitsense-synthetic-analysis", "pceval-physical-circuit",
            "verilogeval-v2-spec-to-rtl", "openeqa-em-eqa-v0",
            "embodiedbench-manipulation-v3", "ost-bench-v2-multiround",
            "macbench-v1", "pse-bench-v3", "chemm-bench-acl2026",
            "physbench-seq", "olympic-arena-physics", "jeebench-physics",
            "openxrd-closedbook", "matcha-v1-zeroshot", "omnimatbench-v2-vanilla",
            "formationeval-v0-1", "cladbench-v1", "enviroexam-zeroshot",
            "medxpertqa-text-v3", "gmai-mmbench-v7-test", "lab-bench-v1-protocolqa",
            "earthse-earth-silver-mc", "geonatureagent-v5",
            "nuclearqav2-v1-aggregate", "thermoqa-v0-4-composite",
            "medagentbench-v1-overall-sr", "medcalc-bench-paper1047",
            "mediconfusion-v2-mc", "fdm-bench-v1-gcode-deterministic",
            "isafetybench-2025-single-avg", "fle-neurips-2025-planning",
            "feabench-gold-modelspecs-oneshot", "cfdcodebench-v1-zeroshot",
            "fem-bench-2025-first-run",
            "gs-powerflow-100-proctext",
            "climaqa-gold-mcq-default",
            "tps-calcbench-v1-core-exact",
        }
        self.assertTrue(expected.issubset(by_id))
        for benchmark_id in expected:
            benchmark = by_id[benchmark_id]
            self.assertGreaterEqual(
                len(benchmark["coverage"]["represented_organizations"]), 2, benchmark_id
            )
            self.assertTrue(benchmark["observations"], benchmark_id)
            self.assertTrue(benchmark["frontier_events"], benchmark_id)
            self.assertTrue(benchmark["summary"]["en"], benchmark_id)
            self.assertTrue(benchmark["summary"]["zh"], benchmark_id)
            for view_ids in payload["lifecycle_views"].values():
                self.assertIsInstance(benchmark_id in view_ids, bool)

    def test_new_story_membership_is_recomputed_from_metrics(self):
        payload = json.loads(SNAPSHOT.read_text())
        views = payload["lifecycle_views"]
        for benchmark_id in ("olympiadbench-physics", "eee-bench-v2"):
            self.assertIn(benchmark_id, views["test-of-time"])
            self.assertIn(benchmark_id, views["still-frontier"])
            self.assertNotIn(benchmark_id, views["fastest-solved"])
            self.assertNotIn(benchmark_id, views["recently-saturated"])

    def test_numeric_metrics_preserve_display_precision(self):
        by_id = {item["id"]: item for item in self.benchmarks}
        self.assertEqual(by_id["engibench-v2-level3"]["score_decimals"], 2)
        self.assertEqual(by_id["pg-llm-proteingym"]["score_decimals"], 3)

    def test_ratio_scores_never_cross_physical_percentage_bounds(self):
        for benchmark in self.benchmarks:
            if benchmark["score_format"] != "ratio":
                continue
            for observation in benchmark["observations"]:
                self.assertGreaterEqual(observation["score"], 0.0, observation["observation_id"])
                self.assertLessEqual(observation["score"], 1.0, observation["observation_id"])

    def test_every_extreme_score_group_has_explicit_adversarial_review(self):
        low_ratio_ids = set()
        large_numeric_ids = set()
        for benchmark in self.benchmarks:
            for observation in benchmark["observations"]:
                if benchmark["score_format"] == "ratio" and observation["score"] < 0.01:
                    low_ratio_ids.add(benchmark["id"])
                if benchmark["score_format"] == "number" and observation["score"] > 100:
                    large_numeric_ids.add(benchmark["id"])
        self.assertEqual(low_ratio_ids, set(REVIEWED_LOW_RATIO_BENCHMARKS))
        self.assertEqual(large_numeric_ids, set(REVIEWED_LARGE_NUMERIC_BENCHMARKS))

    def test_normalization_floor_is_not_treated_as_a_hard_score_bound(self):
        mmlu = next(item for item in self.benchmarks if item["id"] == "mmlu")
        self.assertTrue(any(item["score"] < mmlu["floor"] for item in mmlu["observations"]))
        self.assertGreaterEqual(mmlu["normalized_progress"], 0.0)

    def test_raw_score_units_map_exactly_once_to_canonical_scores(self):
        for benchmark in self.benchmarks:
            for observation in benchmark["observations"]:
                self.assertEqual(observation["input_unit"], benchmark["input_unit"])
                if benchmark["input_unit"] == "percentage_points":
                    self.assertAlmostEqual(observation["score"], observation["input_score"] / 100)
                else:
                    self.assertAlmostEqual(observation["score"], observation["input_score"])

    def test_mmmu_and_proteingym_keep_bounds_separate_from_progress_baselines(self):
        by_id = {item["id"]: item for item in self.benchmarks}
        mmmu = by_id["mmmu"]
        self.assertEqual(mmmu["hard_min"], 0.0)
        self.assertEqual(mmmu["progress_baseline"], 0.0)
        protein = by_id["pg-llm-proteingym"]
        self.assertEqual(protein["hard_min"], -1.0)
        self.assertEqual(protein["progress_baseline"], 0.0)

    def test_boolq_t0pp_uses_verified_helm_value(self):
        benchmark = next(item for item in self.benchmarks if item["id"] == "boolq")
        observation = next(item for item in benchmark["observations"] if "T0pp" in item["model"])
        self.assertEqual(observation["score"], 0.322)
        self.assertIn("v0.2.4", observation["source"])


if __name__ == "__main__":
    unittest.main()
