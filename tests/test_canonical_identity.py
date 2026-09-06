import unittest

from scripts.build_snapshot import (
    canonical_url,
    evidence_identity,
    measurement_identity,
    merge_measurements,
    stable_id,
)


def measurement(**overrides):
    row = {
        "benchmark_version_id": "demo-v1",
        "benchmark_id": "demo",
        "model_id": stable_id("model", "example lab", "model-v1"),
        "model_label_id": "model-v1",
        "model_configuration": "model-v1",
        "model": "Model V1",
        "organization": "Example Lab",
        "score_series_id": "demo-canonical-score",
        "protocol_id": "demo-protocol-v1",
        "task_set_id": "demo-task-set-v1",
        "score": 0.75,
        "source_ids": ["resource-score", "resource-benchmark"],
        "score_source_ids": ["resource-score"],
        "source": "https://example.org/result",
        "evidence_id": "evidence-one",
        "source_row_id": "row-one",
        "evaluation_date": "2026-03-10",
        "model_release_date": "2026-02-01",
        "result_public_date": "2026-03-20",
        "source_publication_date": "2026-03-20",
        "observation_date": "2026-02-01",
        "observation_date_sources": [{
            "date": "2026-02-01", "kind": "model_release_date", "precision": "day",
            "resource_ids": ["resource-model"],
        }],
        "observation_date_source_ids": ["resource-model"],
        "evaluation_date_sources": [],
        "score_publication_date_sources": [],
        "retrospective": True,
        "contemporaneous": False,
        "historical_frontier_eligible": True,
        "temporal_class": "retrospective_evaluation",
        "date": "2026-02-01",
        "capability_date": "2026-02-01",
    }
    row.update(overrides)
    return row


class CanonicalIdentityTests(unittest.TestCase):
    def test_resource_url_normalization_preserves_arxiv_version(self):
        self.assertEqual(
            canonical_url("http://arxiv.org/pdf/2311.12983v2.pdf?utm_source=test"),
            "https://arxiv.org/abs/2311.12983v2",
        )

    def test_evidence_id_does_not_depend_on_row_number(self):
        spec = {"id": "demo", "file": "demo.csv"}
        row = {"Name": "Model", "Score": "0.5"}
        self.assertEqual(evidence_identity(spec, row, 1), evidence_identity(spec, row, 999))

    def test_measurement_id_uses_semantic_fields(self):
        first = measurement()
        second = measurement(evidence_id="evidence-two", source_row_id="row-two")
        self.assertEqual(measurement_identity(first), measurement_identity(second))

    def test_duplicate_evidence_merges_without_losing_lineage(self):
        first = measurement()
        second = measurement(
            evidence_id="evidence-two",
            source_row_id="row-two",
            source_ids=["resource-other", "resource-benchmark"],
            score_source_ids=["resource-other"],
            source="https://example.org/earlier",
            evaluation_date="2026-01-15",
            observation_date="2026-01-15",
            observation_date_sources=[{
                "date": "2026-01-15", "kind": "evaluation_date", "precision": "day",
                "resource_ids": ["resource-other"],
            }],
        )
        merged = merge_measurements([first, second])
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["evidence_count"], 2)
        self.assertEqual(set(merged[0]["evidence_ids"]), {"evidence-one", "evidence-two"})
        self.assertEqual(set(merged[0]["score_source_ids"]), {"resource-score", "resource-other"})
        self.assertEqual(merged[0]["observation_date"], "2026-01-15")
        reversed_merge = merge_measurements([second, first])
        self.assertEqual(merged[0]["observation_id"], reversed_merge[0]["observation_id"])
        self.assertEqual(merged[0]["evidence_ids"], reversed_merge[0]["evidence_ids"])

    def test_distinct_display_setting_is_not_merged(self):
        first = measurement()
        second = measurement(
            evidence_id="evidence-two",
            source_row_id="row-two",
            model="Model V1 Few-Shot",
            model_label_id="model-v1-few-shot",
        )
        self.assertEqual(len(merge_measurements([first, second])), 2)


if __name__ == "__main__":
    unittest.main()
