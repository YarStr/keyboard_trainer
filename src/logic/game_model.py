import time

from PyQt6 import QtCore
from PyQt6.QtCore import QObject

from src.logic.levels import Levels
import src.storage.levels


class GameModel(QObject):
    mistake_done = QtCore.pyqtSignal(int)
    mistake_fixed = QtCore.pyqtSignal()
    game_finished = QtCore.pyqtSignal()
    timer_updated = QtCore.pyqtSignal(QtCore.QTime)
    next_word_chosen = QtCore.pyqtSignal(int)

    def __init__(self, level: Levels):
        super().__init__()
        self._start_time = None
        self._target_string = src.storage.levels.get_target_string_by_level(
            level)
        self._mistakes = 0
        self._current_word_number = 0
        self._is_mistake_still_there = False
        self._timer = QtCore.QTimer()
        self._time = QtCore.QTime(0, 0)
        self._timer.timeout.connect(self.timer_event)

    def timer_event(self) -> None:
        self._time = self._time.addSecs(1)
        self.timer_updated.emit(self._time)

    def start_timer(self) -> None:
        self._start_time = time.time()
        self._timer.start(1000)

    @property
    def mistakes(self) -> int:
        return self._mistakes

    @property
    def target_string(self) -> str:
        return self._target_string

    @property
    def time(self) -> QtCore.QTime:
        return self._time

    def handle_string(self, string: str) -> None:
        if not self._target_string.startswith(string):
            self._mistakes += 1
            self._is_mistake_still_there = True
            self.mistake_done.emit(self._mistakes)

        elif self._is_mistake_still_there:
            self._is_mistake_still_there = False
            self.mistake_fixed.emit()

        elif string[-1] == ' ':
            self._current_word_number += 1
            self.next_word_chosen.emit(self._current_word_number)

        elif self._target_string == string:
            self.game_finished.emit()
