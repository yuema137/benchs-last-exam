import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_benchmark_integration", ROOT / "scripts" / "validate_benchmark_integration.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BenchmarkIntegrationTests(unittest.TestCase):
    def test_missing_chinese_summary_is_rejected(self):
        benchmark = {
            "id": "demo", "name": "Demo", "benchmark_version_id": "demo-v1",
            "release": "2026-01-01", "evaluation_type": "Model", "domain": "Science",
            "summary": {"en": "summary"}, "task_format": {"en": "format", "zh": "格式"},
            "scoring": {"metric_name": "Accuracy"}, "evaluation_target": "final_output",
            "observations": [], "frontier": [], "resource_ids": [], "coverage": {},
        }
        errors = MODULE.validate_benchmark(benchmark, {}, {})
        self.assertTrue(any("summary.zh" in error for error in errors))

    def test_unresolved_observation_source_is_rejected(self):
        benchmark = {
            "id": "demo", "name": "Demo", "benchmark_version_id": "demo-v1",
            "release": "2026-01-01", "evaluation_type": "Model", "domain": "Science",
            "summary": {"en": "summary", "zh": "摘要"},
            "task_format": {"en": "format", "zh": "格式"},
            "scoring": {"metric_name": "Accuracy"}, "evaluation_target": "final_output",
            "observations": [{"observation_id": "obs-1", "model_id": "model-1", "source_ids": ["missing"]}],
            "frontier": [], "resource_ids": [], "coverage": {},
        }
        errors = MODULE.validate_benchmark(benchmark, {}, {"model-1": {"id": "model-1"}})
        self.assertTrue(any("unresolved source missing" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
