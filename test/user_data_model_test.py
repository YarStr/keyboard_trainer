import unittest
from unittest.mock import patch, MagicMock

from src.logic.level import Level
from src.logic.statistics import Statistics
from src.logic.user_data_model import UserDataModel

BEST_TIME = Statistics.BEST_TIME.name
MIN_MISTAKES = Statistics.MIN_MISTAKES.name

USER_NAME = 'name'
STAT_BLOCK = {
    Level.START.name: {
        BEST_TIME: None,
        MIN_MISTAKES: None
    },
    Level.MIDDLE.name: {
        BEST_TIME: '00:04',
        MIN_MISTAKES: 4
    },
    Level.HARD.name: {
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

    def check_update_statistics(self,
                                level: Level,
                                mistakes: int,
                                time: str,
                                is_mistakes_update: bool,
                                is_time_update: bool):

        self.model.current_level = level
        new_best_time = self.model.stat_block[level.name][BEST_TIME]
        new_mistakes = self.model.stat_block[level.name][MIN_MISTAKES]

        if is_mistakes_update:
            new_mistakes = mistakes
        if is_time_update:
            new_best_time = time

        self.model.update_stat_by_current_level(mistakes, time)

        self.assertEqual(self.model.stat_block[level.name][BEST_TIME],
                         new_best_time)
        self.assertEqual(self.model.stat_block[level.name][MIN_MISTAKES],
                         new_mistakes)

    def test_update_none_statistic_fields(self):
        self.check_update_statistics(level=Level.START,
                                     mistakes=2,
                                     time='00:32',
                                     is_mistakes_update=True,
                                     is_time_update=True)

    def test_update_statistic_fields_with_better_time_and_mistakes(self):
        self.check_update_statistics(level=Level.MIDDLE,
                                     mistakes=2,
                                     time='00:02',
                                     is_mistakes_update=True,
                                     is_time_update=True)

    def test_update_statistic_fields_with_better_time_only(self):
        self.check_update_statistics(level=Level.HARD,
                                     mistakes=5,
                                     time='00:02',
                                     is_mistakes_update=False,
                                     is_time_update=True)

    def test_update_statistic_fields_with_better_mistakes_only(self):
        self.check_update_statistics(level=Level.HARD,
                                     mistakes=1,
                                     time='20:02',
                                     is_mistakes_update=True,
                                     is_time_update=False)


if __name__ == '__main__':
    unittest.main()
