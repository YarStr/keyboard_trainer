from abc import abstractmethod
from pathlib import Path

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from src.base_dir import BASE_DIR
from src.gui.ui_elements.game_line_edit import GameLineEdit
from src.gui.widget_type import WidgetType

from src.gui.ui_model import UIModel
from src.logic.game.game_model import GameModel
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
        self._game_model = self._get_game_model()

        start_mistakes = config['start_values']['mistakes']
        self._mistakes_indicator = QLabel(start_mistakes)

        start_time = config['start_values']['time']
        self._timer_indicator = QLabel(start_time)

        self._game_line_input = self._get_game_line_input()
        self._start_button = self._get_start_button()
        self._exit_button = self._get_exit_button()

        self._target_widget = self._get_target_widget()

        self._connect_game_model_signals()

        self.setLayout(self.get_layout_with_all_game_elements())

    @abstractmethod
    def _get_game_model(self) -> GameModel:
        pass

    @abstractmethod
    def _get_target_widget(self) -> QWidget:
        pass

    def _connect_game_model_signals(self) -> None:
        self._game_model.mistake_done.connect(self.on_mistake_done)
        self._game_model.mistake_fixed.connect(self.on_mistake_fixed)
        self._game_model.game_finished.connect(self.on_game_finished)
        self._game_model.timer_updated.connect(self.on_timer_updated)

    def _get_game_line_input(self) -> GameLineEdit:
        game_line_edit = GameLineEdit()
        game_line_edit.textChanged.connect(self.react_on_text_change)
        game_line_edit.setEnabled(False)
        return game_line_edit

    def _get_start_button(self) -> QPushButton:
        button = QPushButton('Старт')
        button.clicked.connect(self.start)
        return button

    def _get_exit_button(self) -> QPushButton:
        button = QPushButton('Выход')
        button.clicked.connect(self.exit)
        return button

    def get_layout_with_all_game_elements(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        layout.addWidget(QLabel('Кол-во ошибок:'))
        layout.addWidget(self._mistakes_indicator)

        layout.addWidget(QLabel('Время:'))
        layout.addWidget(self._timer_indicator)

        layout.addWidget(self._target_widget)
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
        self._game_line_input.setEnabled(True)
        self._game_model.start_timer()
        self._start_button.setEnabled(False)

    def exit(self) -> None:
        self._ui_model.set_widget(WidgetType.LEVELS)

    def react_on_text_change(self) -> None:
        input_text = self._game_line_input.text()
        self._game_model.handle_string(input_text)

    @QtCore.pyqtSlot(bool)
    def on_game_finished(self) -> None:
        self._data_model.update_stat_by_current_level(
            self._game_model.mistakes,
            self._game_model.time.toString(TIME_FORMAT))
        self.exit()

    def update_mistakes_indicator(self, mistakes: int) -> None:
        self._mistakes_indicator.setText(str(mistakes))
