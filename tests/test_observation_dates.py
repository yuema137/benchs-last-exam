import unittest
from datetime import date

from scripts.build_snapshot import build_frontier, parse_dates, threshold_metrics


class ObservationDateTests(unittest.TestCase):
    def test_earliest_candidate_wins(self):
        dates = parse_dates({
            "Started at": "2026-03-10",
            "Release date": "2025-06-01",
            "Result public date": "2026-04-01",
        })
        self.assertEqual(dates["observation_date"], "2025-06-01")
        self.assertEqual(dates["observation_date_sources"][0]["kind"], "model_release_date")

    def test_earliest_score_publication_record_wins(self):
        dates = parse_dates({
            "Result public date": "2026-04-03",
            "Source publication date": "2026-03-28",
            "Date added": "2026-04-05",
        })
        self.assertEqual(dates["result_public_date"], "2026-03-28")
        self.assertEqual(dates["observation_date"], "2026-03-28")

    def test_month_precision_is_preserved(self):
        dates = parse_dates({"Started at": "2026-01"})
        self.assertEqual(dates["observation_date"], "2026-01-01")
        self.assertEqual(dates["observation_date_precision"], "month")

    def test_pre_release_evidence_is_clipped_without_overwriting_provenance(self):
        row = {
            "observation_id": "obs-one",
            "score": 0.95,
            "observation_date": "2024-06-01",
            "capability_date": "2024-06-01",
            "capability_date_meaning": "earliest_observation_evidence_date",
        }
        frontier = build_frontier(
            [row], "capability_date", "earliest observation evidence date",
            minimum_date="2025-01-01",
        )
        self.assertEqual(row["observation_date"], "2024-06-01")
        self.assertEqual(frontier[0]["plot_date"], "2025-01-01")
        thresholds = threshold_metrics(frontier, date(2025, 1, 1), 0.0, 1.0)
        self.assertEqual(thresholds["T90"]["status"], "at_release")
        self.assertEqual(thresholds["T90"]["days"], 0)


if __name__ == "__main__":
    unittest.main()
