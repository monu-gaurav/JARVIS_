"""Regression tests for strict local wake-word score selection."""
import unittest

from core.wake_word import _jarvis_model_score


class JarvisModelScoreTests(unittest.TestCase):
    def test_jarvis_score_is_selected_over_higher_unrelated_score(self):
        self.assertAlmostEqual(
            _jarvis_model_score({"hey_jarvis": 0.81, "alexa": 0.99}), 0.81
        )

    def test_versioned_jarvis_model_name_is_supported(self):
        self.assertAlmostEqual(_jarvis_model_score({"hey_jarvis_v0.1": 0.73}), 0.73)

    def test_unrelated_high_score_cannot_wake_jarvis(self):
        self.assertEqual(_jarvis_model_score({"alexa": 0.99, "computer": 0.95}), 0.0)

    def test_missing_or_invalid_scores_are_safe(self):
        self.assertEqual(_jarvis_model_score({}), 0.0)
        self.assertEqual(_jarvis_model_score(None), 0.0)
        self.assertEqual(_jarvis_model_score({"hey_jarvis": "not-a-score"}), 0.0)


if __name__ == "__main__":
    unittest.main()
