import unittest
import json
from datetime import date
from pathlib import Path


DAY = 1
MONTH = 30.44


def test_of_time(t50_status, t50, t90_status, t90, age_days):
    return ((t50 is not None and t50 >= 12 * MONTH)
            or (t90 is not None and t90 >= 24 * MONTH))


def still_frontier(t50_status, progress, coverage):
    return t50_status == "right_censored" and progress is not None and progress < 0.5 and coverage != "low"


def fastest_solved(t90_status, t90_days):
    return t90_status == "reached" and t90_days < 6 * MONTH


def recently_saturated(t90_status, t90_days, age_days):
    crossing_age = age_days - t90_days
    return t90_status in {"reached", "at_release"} and 0 <= crossing_age <= 3 * MONTH


class LifecycleViewRuleTests(unittest.TestCase):
    def test_test_of_time_boundaries_and_censoring(self):
        self.assertFalse(test_of_time("right_censored", 11.9 * MONTH, "unknown", None, 24 * MONTH))
        self.assertTrue(test_of_time("right_censored", 12.0 * MONTH, "unknown", None, 12 * MONTH))
        self.assertTrue(test_of_time("reached", 12.0 * MONTH, "unknown", None, 24 * MONTH))
        self.assertTrue(test_of_time("reached", 24.0 * MONTH, "unknown", None, 24 * MONTH))
        self.assertFalse(test_of_time("unknown", None, "right_censored", 23.9 * MONTH, 24 * MONTH))
        self.assertTrue(test_of_time("unknown", None, "right_censored", 24.0 * MONTH, 24 * MONTH))
        self.assertFalse(test_of_time("at_release", 0, "unknown", None, 24 * MONTH))
        self.assertFalse(test_of_time("at_release", 0, "right_censored", 23.9 * MONTH, 24 * MONTH))

    def test_still_frontier_requires_unreached_t50_and_evidence(self):
        self.assertTrue(still_frontier("right_censored", 0.499, "medium"))
        self.assertFalse(still_frontier("right_censored", 0.5, "medium"))
        self.assertFalse(still_frontier("reached", 0.49, "medium"))
        self.assertFalse(still_frontier("right_censored", 0.49, "low"))

    def test_fastest_solved_is_strictly_under_six_months(self):
        self.assertTrue(fastest_solved("reached", 5.9 * MONTH))
        self.assertFalse(fastest_solved("reached", 6.0 * MONTH))
        self.assertFalse(fastest_solved("right_censored", 3 * MONTH))
        self.assertFalse(fastest_solved("unknown", None))

    def test_recently_saturated_uses_crossing_age(self):
        self.assertTrue(recently_saturated("reached", 30 * DAY, 30 * DAY + 2.9 * MONTH))
        self.assertTrue(recently_saturated("at_release", 0, 3 * MONTH))
        self.assertFalse(recently_saturated("reached", 30 * DAY, 30 * DAY + 3.1 * MONTH))
        self.assertFalse(recently_saturated("right_censored", 30 * DAY, 30 * DAY + 1 * MONTH))

    def test_default_theme_is_dark_without_a_saved_preference(self):
        source = Path("site/app.js").read_text(encoding="utf-8")
        self.assertIn('localStorage.getItem("bo-theme") || "dark"', source)

    def test_story_cards_open_a_standalone_routable_detail_view(self):
        app = Path("site/app.js").read_text(encoding="utf-8")
        styles = Path("site/styles.css").read_text(encoding="utf-8")
        self.assertIn("routeToDetail(card.dataset.id,event)", app)
        self.assertIn('url.searchParams.set("benchmark",benchmarkId)', app)
        self.assertIn("storyDescription.hidden=true", app)
        self.assertIn("[hidden] { display:none !important; }", styles)

    def test_still_frontier_members_and_cards_use_normalized_progress(self):
        payload = json.loads(Path("site/data/benchmarks.json").read_text(encoding="utf-8"))
        by_id = {benchmark["id"]: benchmark for benchmark in payload["benchmarks"]}
        members = payload["lifecycle_views"]["still-frontier"]
        for benchmark_id in members:
            benchmark = by_id[benchmark_id]
            self.assertLess(benchmark["normalized_progress"], 0.5, benchmark_id)
            self.assertEqual(benchmark["threshold_days"]["T50"]["status"], "right_censored")
            self.assertNotEqual(benchmark["coverage"]["status"], "low")

        fdm = by_id["fdm-bench-v1-gcode-deterministic"]
        self.assertGreater(fdm["capability_frontier_value"], 0.5)
        self.assertLess(fdm["normalized_progress"], 0.5)
        self.assertIn(fdm["id"], members)

        app = Path("site/app.js").read_text(encoding="utf-8")
        self.assertIn('if(view==="still-frontier") return [t("story_frontier"),score(b.normalized_progress)', app)

    def test_all_generated_story_tabs_match_their_hard_rules(self):
        payload = json.loads(Path("site/data/benchmarks.json").read_text(encoding="utf-8"))
        snapshot = date.fromisoformat(payload["snapshot_id"])
        expected = {view: set() for view in payload["lifecycle_views"]}
        for benchmark in payload["benchmarks"]:
            t50 = benchmark["threshold_days"]["T50"]
            t90 = benchmark["threshold_days"]["T90"]
            if ((t50.get("days") is not None and t50["days"] >= 12 * MONTH)
                    or (t90.get("days") is not None and t90["days"] >= 24 * MONTH)):
                expected["test-of-time"].add(benchmark["id"])
            if (t50["status"] == "right_censored"
                    and benchmark.get("normalized_progress") is not None
                    and benchmark["normalized_progress"] < 0.5
                    and benchmark["coverage"]["status"] != "low"):
                expected["still-frontier"].add(benchmark["id"])
            if t90["status"] == "reached" and t90.get("days") is not None and t90["days"] < 6 * MONTH:
                expected["fastest-solved"].add(benchmark["id"])
            if t90["status"] in {"reached", "at_release"} and t90.get("days") is not None:
                age = (snapshot - date.fromisoformat(benchmark["release"])).days
                if 0 <= age - t90["days"] <= 3 * MONTH:
                    expected["recently-saturated"].add(benchmark["id"])
        for view, members in payload["lifecycle_views"].items():
            self.assertEqual(set(members), expected[view], view)

    def test_only_canonical_score_series_drive_cross_benchmark_metrics(self):
        payload = json.loads(Path("site/data/benchmarks.json").read_text(encoding="utf-8"))
        for benchmark in payload["benchmarks"]:
            canonical = benchmark["canonical_score"]
            self.assertTrue(canonical["lifecycle_eligible"], benchmark["id"])
            observations = {item["observation_id"]: item for item in benchmark["observations"]}
            for point in benchmark["frontier_events"]:
                self.assertEqual(observations[point["observation_id"]]["score_role"], "canonical")
            for series in benchmark["auxiliary_score_series"]:
                self.assertFalse(series["lifecycle_eligible"])
                for observation_id in series["observation_ids"]:
                    self.assertEqual(observations[observation_id]["score_role"], "auxiliary")

        cybench = next(item for item in payload["benchmarks"] if item["id"] == "cybench")
        self.assertEqual(len(cybench["auxiliary_score_series"]), 1)
        self.assertTrue(cybench["auxiliary_score_series"][0]["frontier_events"])


if __name__ == "__main__":
    unittest.main()
