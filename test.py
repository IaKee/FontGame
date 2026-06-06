import unittest

from constants import OPTION_COUNT_BY_DIFFICULTY, PHRASES, PREFERRED_FONTS, ROUNDS_PER_GAME


class ConstantsTest(unittest.TestCase):
    def test_game_has_enough_content(self):
        self.assertGreaterEqual(len(PREFERRED_FONTS), 10)
        self.assertGreaterEqual(len(PHRASES), 10)

    def test_difficulty_options_increase(self):
        self.assertLess(OPTION_COUNT_BY_DIFFICULTY[0], OPTION_COUNT_BY_DIFFICULTY[1])
        self.assertLess(OPTION_COUNT_BY_DIFFICULTY[1], OPTION_COUNT_BY_DIFFICULTY[2])

    def test_game_length_is_positive(self):
        self.assertGreater(ROUNDS_PER_GAME, 0)


if __name__ == "__main__":
    unittest.main()
