from PyQt6 import QtCore

from src.logic.game.game_model import GameModel
from src.logic.level import Level
import src.storage.levels


class LearnGameModel(GameModel):
    next_word_chosen = QtCore.pyqtSignal(int)

    def __init__(self, level: Level):
        self._level = level
        self._current_word_number = 0
        super().__init__()
        self._number_of_words = len(self._target_string.split())

    def _get_target_string(self) -> str:
        return src.storage.levels.get_target_string_by_level(self._level)

    def _react_on_word_typed(self) -> None:
        self.game_finished.emit(True)

    def highlight_current_word(self, string) -> None:
        if string and string[-1] == ' ' and not self._is_mistake_done:
            self._current_word_number = len(string.split())
            self.next_word_chosen.emit(self._current_word_number)

    def handle_string(self, string: str) -> None:
        super().handle_string(string)
        self.highlight_current_word(string)
