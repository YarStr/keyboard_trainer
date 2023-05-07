from pathlib import Path

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from src.base_dir import BASE_DIR
from src.gui.ui_elements.game_line_edit import GameLineEdit
from src.gui.widget_type import WidgetType

from src.logic.game_model import GameModel
from src.gui.ui_model import UIModel
from src.logic.user_data_model import UserDataModel

import configparser

config = configparser.ConfigParser()
config.read(Path(BASE_DIR, 'gui/resources/ui_config.ini'))

TIME_FORMAT = config['format']['time']


class GameWidget(QWidget):
    def __init__(self, ui_model: UIModel, data_model: UserDataModel):
        super().__init__()

        self._ui_model = ui_model
        self._data_model = data_model
        self._game_model = GameModel(self._data_model.current_level)
        self.connect_game_model_signals()

        self._target_string = self._game_model.target_string

        start_mistakes = config['start_values']['mistakes']
        self._mistakes_indicator = QLabel(start_mistakes)

        start_time = config['start_values']['time']
        self._timer_indicator = QLabel(start_time)

        self._game_line_input = self.get_game_line_input()
        self._start_button = self.get_start_button()
        self._exit_button = self.get_exit_button()
        self._target_string_label = self.get_target_string_label()

        self.setLayout(self.get_layout_with_all_game_elements())

    def connect_game_model_signals(self) -> None:
        self._game_model.mistake_done.connect(self.on_mistake_done)
        self._game_model.mistake_fixed.connect(self.on_mistake_fixed)
        self._game_model.game_finished.connect(self.on_game_finished)
        self._game_model.timer_updated.connect(self.on_timer_updated)
        self._game_model.next_word_chosen.connect(self.highlight_word)

    def get_game_line_input(self) -> GameLineEdit:
        game_line_edit = GameLineEdit()
        game_line_edit.textChanged.connect(self.react_on_text_change)
        game_line_edit.setEnabled(False)
        return game_line_edit

    def get_start_button(self) -> QPushButton:
        button = QPushButton('Старт')
        button.clicked.connect(self.start)
        return button

    def get_exit_button(self) -> QPushButton:
        button = QPushButton('Выход')
        button.clicked.connect(self.exit)
        return button

    def get_target_string_label(self) -> QLabel:
        label = QLabel(self._target_string)
        label.setProperty('class', 'target-string')
        return label

    def get_layout_with_all_game_elements(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        layout.addWidget(QLabel('Кол-во ошибок:'))
        layout.addWidget(self._mistakes_indicator)

        layout.addWidget(QLabel('Время:'))
        layout.addWidget(self._timer_indicator)

        layout.addWidget(self._target_string_label)
        layout.addWidget(self._game_line_input)

        layout.addWidget(self._start_button)
        layout.addWidget(self._exit_button)

        return layout

    @QtCore.pyqtSlot(int)
    def on_mistake_done(self, mistakes: int) -> None:
        self.update_mistakes_indicator(mistakes)
        self._game_line_input.setReadOnly(True)
        input_with_mistake_style = config['style']['input_with_mistake']
        self._game_line_input.setStyleSheet(input_with_mistake_style)

    @QtCore.pyqtSlot()
    def on_mistake_fixed(self) -> None:
        self._game_line_input.setReadOnly(False)
        self._game_line_input.setStyleSheet('')

    @QtCore.pyqtSlot(QtCore.QTime)
    def on_timer_updated(self, time: QtCore.QTime) -> None:
        self._timer_indicator.setText(time.toString(TIME_FORMAT))

    def start(self) -> None:
        self.highlight_word(0)
        self._game_line_input.setEnabled(True)
        self._game_model.start_timer()
        self._start_button.setEnabled(False)

    def exit(self) -> None:
        self._ui_model.set_widget(WidgetType.LEVELS)

    def react_on_text_change(self) -> None:
        self._game_model.handle_string(self._game_line_input.text())

    def on_game_finished(self) -> None:
        self._data_model.update_stat_by_current_level(
            self._game_model.mistakes,
            self._game_model.time.toString(TIME_FORMAT))
        self.exit()

    def update_mistakes_indicator(self, mistakes: int) -> None:
        self._mistakes_indicator.setText(str(mistakes))

    @QtCore.pyqtSlot(int)
    def highlight_word(self, index: int) -> None:
        highlighted_words = []
        for number, word in enumerate(self._target_string.split()):
            if number == index:
                highlighted_words.append(f'<b>{word}</b>')
            else:
                highlighted_words.append(word)
        highlighted_sentence = ' '.join(highlighted_words)
        self._target_string_label.setText(highlighted_sentence)
