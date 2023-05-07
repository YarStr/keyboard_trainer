import time
from abc import abstractmethod

from PyQt6 import QtCore
from PyQt6.QtCore import QObject


class GameModel(QObject):
    mistake_done = QtCore.pyqtSignal(int)
    mistake_fixed = QtCore.pyqtSignal()
    game_finished = QtCore.pyqtSignal()
    timer_updated = QtCore.pyqtSignal(QtCore.QTime)

    def __init__(self):
        super().__init__()
        self._start_time = None
        self._target_string = self._get_target_string()
        self._mistakes = 0
        self._is_mistake_done = False
        self._timer = QtCore.QTimer()
        self._time = QtCore.QTime(0, 0)
        self._timer.timeout.connect(self.timer_event)

    @abstractmethod
    def _get_target_string(self) -> str:
        pass

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
        if self._target_string.startswith(string):
            if self._is_mistake_done:
                self._is_mistake_done = False
                self.mistake_fixed.emit()

            elif self._target_string == string:
                self._react_on_word_typed()
        else:
            self._mistakes += 1
            self._is_mistake_done = True
            self.mistake_done.emit(self._mistakes)

    @abstractmethod
    def _react_on_word_typed(self) -> None:
        pass
