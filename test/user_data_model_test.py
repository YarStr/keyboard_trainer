import unittest
from unittest.mock import patch, MagicMock

from src.logic.levels import Levels
from src.logic.statistics import Statistics
from src.logic.user_data_model import UserDataModel

BEST_TIME = Statistics.BEST_TIME.name
MIN_MISTAKES = Statistics.MIN_MISTAKES.name

USER_NAME = 'name'
STAT_BLOCK = {
    Levels.START.name: {
        BEST_TIME: None,
        MIN_MISTAKES: None
    },
    Levels.MIDDLE.name: {
        BEST_TIME: '00:04',
        MIN_MISTAKES: 4
    },
    Levels.HARD.name: {
        BEST_TIME: '01:34',
        MIN_MISTAKES: 2
    }
}


class TestGameModel(unittest.TestCase):
    @patch('src.logic.user_data_model.src.storage.user_data')
    def setUp(self, mock) -> None:
        mock.get_statistics_from_database = MagicMock(return_value=STAT_BLOCK)
        self.model = UserDataModel()
        self.model.load_user_by_name(USER_NAME)

    def test_update_none_statistic_fields(self):
        self.model.current_level = Levels.START
        mistakes = 2
        time = '00:32'
        self.model.update_stat_by_current_level(mistakes, time)

        self.assertEqual(
            self.model.stat_block[Levels.START.name][BEST_TIME], time)
        self.assertEqual(
            self.model.stat_block[Levels.START.name][MIN_MISTAKES], mistakes)

    def test_update_statistic_fields_with_better_time_and_mistakes(self):
        self.model.current_level = Levels.MIDDLE
        mistakes = 2
        time = '00:02'
        self.model.update_stat_by_current_level(mistakes, time)

        self.assertEqual(
            self.model.stat_block[Levels.MIDDLE.name][BEST_TIME], time)
        self.assertEqual(
            self.model.stat_block[Levels.MIDDLE.name][MIN_MISTAKES], mistakes)

    def test_update_statistic_fields_with_better_time_only(self):
        self.model.current_level = Levels.HARD
        mistakes = 5
        old_mistakes = self.model.stat_block[Levels.HARD.name][MIN_MISTAKES]
        time = '00:02'
        self.model.update_stat_by_current_level(mistakes, time)

        self.assertEqual(
            self.model.stat_block[Levels.HARD.name][BEST_TIME], time)
        self.assertEqual(
            self.model.stat_block[Levels.HARD.name][MIN_MISTAKES],
            old_mistakes)

    def test_update_statistic_fields_with_better_mistakes_only(self):
        self.model.current_level = Levels.HARD
        mistakes = 1
        old_time = self.model.stat_block[Levels.HARD.name][BEST_TIME]
        time = '20:02'
        self.model.update_stat_by_current_level(mistakes, time)

        self.assertEqual(
            self.model.stat_block[Levels.HARD.name][BEST_TIME], old_time)
        self.assertEqual(
            self.model.stat_block[Levels.HARD.name][MIN_MISTAKES], mistakes)


if __name__ == '__main__':
    unittest.main()
