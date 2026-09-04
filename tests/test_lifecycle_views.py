import unittest
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


if __name__ == "__main__":
    unittest.main()
