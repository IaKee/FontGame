import unittest

from constants import FACTORS, round_time_seconds, score_per_hit
from font_game import contrasting_color, mix_color


def settings(level):
    return {factor.key: level for factor in FACTORS}


class DifficultyTests(unittest.TestCase):
    def test_score_grows_from_easy_to_hard(self):
        self.assertEqual(score_per_hit(settings(1)), 100)
        self.assertEqual(score_per_hit(settings(3)), 500)
        self.assertLess(score_per_hit(settings(1)), score_per_hit(settings(2)))
        self.assertLess(score_per_hit(settings(2)), score_per_hit(settings(3)))

    def test_each_harder_factor_increases_score(self):
        easy = settings(1)
        base_score = score_per_hit(easy)
        for factor in FACTORS:
            harder = dict(easy)
            harder[factor.key] = 2
            self.assertGreater(score_per_hit(harder), base_score)

    def test_progressive_timer_stops_at_three_seconds(self):
        hard = settings(3)
        self.assertEqual(round_time_seconds(hard, 0), 15.0)
        self.assertEqual(round_time_seconds(hard, 20), 3.0)
        self.assertEqual(round_time_seconds(hard, 100), 3.0)


class ColorTests(unittest.TestCase):
    def test_progress_bar_moves_from_blue_to_red(self):
        self.assertEqual(mix_color((226, 54, 74), (44, 104, 232), 1), "#2c68e8")
        self.assertEqual(mix_color((226, 54, 74), (44, 104, 232), 0), "#e2364a")

    def test_text_color_never_equals_background(self):
        for background in ("#ffffff", "#000000", "#336699"):
            self.assertNotEqual(contrasting_color(background), background)
            self.assertNotEqual(contrasting_color(background, close=True), background)


if __name__ == "__main__":
    unittest.main()
