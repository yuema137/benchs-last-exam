import unittest
from datetime import datetime

from benchmark_observatory.schema import (
    Bound,
    BoundType,
    Direction,
    MetricDefinition,
    ScoreObservation,
    SourceProvenance,
    SourceType,
    PanelMembership,
    PanelRole,
)


class SchemaTests(unittest.TestCase):
    def test_bounded_metric_requires_bounds(self):
        with self.assertRaises(ValueError):
            MetricDefinition("accuracy", "accuracy", Direction.HIGHER_IS_BETTER, "ratio", True)

    def test_equal_bounds_are_rejected(self):
        bound = Bound(1.0, BoundType.THEORETICAL)
        with self.assertRaises(ValueError):
            MetricDefinition(
                "accuracy", "accuracy", Direction.HIGHER_IS_BETTER, "ratio", True, bound, bound
            )

    def test_observation_requires_provenance(self):
        with self.assertRaises(ValueError):
            ScoreObservation(
                "obs-1", "mmlu-v1", "model-1", 0.5, "ratio", None, None, None, "5-shot"
            )

    def test_provenance_is_constructible(self):
        source = SourceProvenance(
            "src-1", SourceType.PRIMARY, "https://example.com", None, None, None, datetime(2026, 1, 1)
        )
        self.assertEqual(source.source_type, SourceType.PRIMARY)

    def test_panel_membership_requires_reason_and_nonnegative_weight(self):
        with self.assertRaises(ValueError):
            PanelMembership("panel-1", "model-1", PanelRole.CONTEMPORARY_FRONTIER, "Org", -1, None, None, "")


if __name__ == "__main__":
    unittest.main()
