from PyQt6.QtCore import QObject

from src.logic.level import Level
from src.logic.statistics import Statistics
import src.storage.user_data

_BEST_TIME = Statistics.BEST_TIME.name
_MIN_MISTAKES = Statistics.MIN_MISTAKES.name


class UserDataModel(QObject):
    def __init__(self):
        super().__init__()
        self._user_name = None
        self._stat_block = None
        self._current_level = None

    def load_user_by_name(self, user_name: str):
        self._user_name = user_name
        self._stat_block = src.storage.user_data.get_statistics_from_database(
            user_name)

    @property
    def user_name(self):
        return self._user_name

    @property
    def stat_block(self):
        return self._stat_block

    @property
    def current_level(self):
        return self._current_level

    @current_level.setter
    def current_level(self, level: Level):
        self._current_level = level

    def update_stat_by_current_level(self, mistakes: int, time: str) -> None:
        level_name = self._current_level.name
        best_time = self._stat_block[level_name][_BEST_TIME]
        min_mistakes = self._stat_block[level_name][_MIN_MISTAKES]

        if min_mistakes is None or min_mistakes > mistakes:
            self._stat_block[level_name][_MIN_MISTAKES] = mistakes

        if best_time is None or str(best_time) > str(time):
            self._stat_block[level_name][_BEST_TIME] = str(time)

        src.storage.user_data.load_statistics_to_database(
            self._user_name, self._stat_block)
