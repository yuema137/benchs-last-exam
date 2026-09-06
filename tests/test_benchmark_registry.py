import json
import tempfile
import unittest
from pathlib import Path

from benchmark_observatory.registry import BenchmarkSpec, load_benchmark_specs


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "benchmarks"
RAW = ROOT / "data" / "raw"


class BenchmarkRegistryTests(unittest.TestCase):
    def test_repository_registry_loads_one_typed_record_per_file(self):
        specs = load_benchmark_specs(REGISTRY, RAW)
        self.assertEqual(len(specs), len(list(REGISTRY.glob("*.json"))))
        self.assertEqual(len(specs), len({spec.id for spec in specs}))
        self.assertTrue(all(isinstance(spec, BenchmarkSpec) for spec in specs))

    def test_registry_order_is_contiguous_and_deterministic(self):
        specs = load_benchmark_specs(REGISTRY, RAW)
        self.assertEqual([spec.registry_order for spec in specs], list(range(len(specs))))

    def test_missing_chinese_copy_is_rejected_at_source_boundary(self):
        payload = json.loads((REGISTRY / "mmlu.json").read_text())
        del payload["summary"]["zh"]
        with self.assertRaisesRegex(ValueError, "summary"):
            BenchmarkSpec.from_mapping(payload, path=Path("mmlu.json"))

    def test_unknown_source_field_is_rejected(self):
        payload = json.loads((REGISTRY / "mmlu.json").read_text())
        payload["manual_story_tab"] = "still-frontier"
        with self.assertRaisesRegex(ValueError, "unknown"):
            BenchmarkSpec.from_mapping(payload, path=Path("mmlu.json"))

    def test_missing_raw_evidence_file_is_rejected(self):
        payload = json.loads((REGISTRY / "mmlu.json").read_text())
        payload["file"] = "missing.csv"
        with tempfile.TemporaryDirectory() as directory:
            registry = Path(directory) / "benchmarks"
            raw = Path(directory) / "raw"
            registry.mkdir()
            raw.mkdir()
            (registry / "mmlu.json").write_text(json.dumps(payload))
            with self.assertRaisesRegex(ValueError, "raw observation file does not exist"):
                load_benchmark_specs(registry, raw)


if __name__ == "__main__":
    unittest.main()
