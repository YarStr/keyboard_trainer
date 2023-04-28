from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from src.gui.ui_elements.game_line_edit import GameLineEdit
from src.gui.widget_type import WidgetType

from src.logic.game_model import GameModel
from src.gui.ui_model import UIModel
from src.logic.user_data_model import UserDataModel


class GameWidget(QWidget):
    def __init__(self, ui_model: UIModel, data_model: UserDataModel):
        super().__init__()

        self._ui_model = ui_model
        self._data_model = data_model

        self._game_model = GameModel(self._data_model.current_level)
        self._game_model.mistake_done.connect(self.on_mistake_done)
        self._game_model.mistake_fixed.connect(self.on_mistake_fixed)
        self._game_model.game_finished.connect(self.on_game_finished)
        self._game_model.timer_updated.connect(self.on_timer_updated)
        self._game_model.next_word_chosen.connect(self.highlight_word)

        self.layout = QVBoxLayout()

        self.mistakes_indicator = QLabel('0')
        self.timer_indicator = QLabel('00:00')

        self.input = GameLineEdit()
        self.input.textChanged.connect(self.react_on_text_change)
        self.input.setEnabled(False)

        self.start_button = QPushButton('Старт')
        self.start_button.clicked.connect(self.start)

        self.exit_button = QPushButton('Выход')
        self.exit_button.clicked.connect(self.exit)

        self.layout.addWidget(QLabel('Кол-во ошибок:'))
        self.layout.addWidget(self.mistakes_indicator)

        self.layout.addWidget(QLabel('Время:'))
        self.layout.addWidget(self.timer_indicator)

        self.target_string = self._game_model.target_string
        self.target_string_label = QLabel(self.target_string)
        self.target_string_label.setStyleSheet('font-size: 16px')
        self.layout.addWidget(self.target_string_label)
        self.layout.addWidget(self.input)

        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)

    @QtCore.pyqtSlot(int)
    def on_mistake_done(self, mistakes: int) -> None:
        self.update_mistakes_indicator(mistakes)
        self.input.setReadOnly(True)
        self.input.setStyleSheet('background-color: red;')

    @QtCore.pyqtSlot()
    def on_mistake_fixed(self) -> None:
        self.input.setReadOnly(False)
        self.input.setStyleSheet('')

    @QtCore.pyqtSlot(QtCore.QTime)
    def on_timer_updated(self, time: QtCore.QTime) -> None:
        self.timer_indicator.setText(time.toString("mm:ss"))

    def start(self) -> None:
        self.highlight_word(0)
        self.input.setEnabled(True)
        self._game_model.start_timer()
        self.start_button.setEnabled(False)

    def exit(self) -> None:
        self._ui_model.set_widget(WidgetType.LEVELS)

    def react_on_text_change(self) -> None:
        self._game_model.handle_string(self.input.text())

    def on_game_finished(self) -> None:
        self._data_model.update_stat_by_current_level(
            self._game_model.mistakes, self._game_model.time.toString("mm:ss"))
        self.exit()

    def update_mistakes_indicator(self, mistakes: int) -> None:
        self.mistakes_indicator.setText(str(mistakes))

    @QtCore.pyqtSlot(int)
    def highlight_word(self, index):

        words_html = []
        for number, word in enumerate(self.target_string.split()):
            if number == index:
                words_html.append(f"<b>{word}</b>")
            else:
                words_html.append(word)
        sentence_html = " ".join(words_html)
        print(index)
        self.target_string_label.setText(sentence_html)
