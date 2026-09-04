import unittest
from benchmark_observatory.schema import (
    Bound,
    BoundType,
    Direction,
    MetricDefinition,
    ScoreObservation,
    Resource,
    ResourceAuthority,
    ResourceScope,
    ResourceType,
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

    def test_resource_is_constructible(self):
        resource = Resource(
            "resource-1",
            (ResourceScope.BENCHMARK,),
            "mmlu",
            ResourceType.PAPER,
            "MMLU paper",
            "https://example.com/mmlu",
            "Authors",
            ResourceAuthority.PRIMARY,
        )
        self.assertEqual(resource.resource_scope, (ResourceScope.BENCHMARK,))

    def test_observation_source_ids_are_canonical_lineage(self):
        observation = ScoreObservation(
            "obs-1", "mmlu-v1", "model-1", 0.5, "ratio", None, None, None,
            "5-shot", source_ids=("resource-1",), model_family_id="family-1",
            metric_id="accuracy", protocol_id="mmlu-5-shot-v1",
        )
        self.assertEqual(observation.provenance_ids, ("resource-1",))

    def test_panel_membership_requires_reason_and_nonnegative_weight(self):
        with self.assertRaises(ValueError):
            PanelMembership("panel-1", "model-1", PanelRole.CONTEMPORARY_FRONTIER, "Org", -1, None, None, "")


if __name__ == "__main__":
    unittest.main()
