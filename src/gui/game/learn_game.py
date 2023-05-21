from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel

from src.gui.game.game import GameWidget
from src.logic.game.game_model import GameModel

from src.logic.game.learn_game_model import LearnGameModel
from src.gui.ui_model import UIModel
from src.logic.user_data_model import UserDataModel


class LearnGameWidget(GameWidget):
    def __init__(self, ui_model: UIModel, data_model: UserDataModel):
        super().__init__(ui_model, data_model)

    def _get_game_model(self) -> GameModel:
        return LearnGameModel(self._data_model.current_level)

    def _get_target_widget(self) -> QWidget:
        self._target_string = self._game_model.target_string
        widget = QLabel(self._target_string)
        widget.setProperty('class', 'target-string')
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return widget

    def _connect_game_model_signals(self) -> None:
        super()._connect_game_model_signals()
        self._game_model.next_word_chosen.connect(self.highlight_word)

    def start(self) -> None:
        self.highlight_word(0)
        super().start()

    @QtCore.pyqtSlot(int)
    def highlight_word(self, index: int) -> None:
        highlighted_words = []
        for number, word in enumerate(self._target_string.split()):
            if number == index:
                highlighted_words.append(f'<b>{word}</b>')
            else:
                highlighted_words.append(word)
        highlighted_sentence = ' '.join(highlighted_words)
        self._target_widget.setText(highlighted_sentence)
