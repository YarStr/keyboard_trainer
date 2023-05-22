from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, \
    QGridLayout

from src.gui.widget_type import WidgetType
from src.logic.statistics import Statistics
from src.gui.ui_model import UIModel
from src.logic.user_data_model import UserDataModel

from src.storage.levels import Level


def _get_level_choose_widget() -> QWidget:
    message = f'Выбери уровень!'
    label = QLabel(message)
    label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    label.setProperty('class', 'levels-text')
    return label


class LevelWidget(QWidget):
    def __init__(self, ui_model: UIModel, data_model: UserDataModel):
        super().__init__()
        self._ui_model = ui_model
        self._data_model = data_model
        self.setLayout(self.get_main_layout())

    def get_main_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._get_hello_message_widget())
        layout.addWidget(_get_level_choose_widget())
        self.add_level_widgets_to_layout(layout)
        return layout

    def _get_hello_message_widget(self) -> QWidget:
        message = f'Статистика профиля: <b>{self._data_model.user_name}</b>'
        label = QLabel(message)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        label.setProperty('class', 'levels-text')
        return label

    def add_level_widgets_to_layout(self, layout: QVBoxLayout):
        for level in Level:
            button = self._get_level_button(level)
            layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

            for stat in Statistics:
                layout.addWidget(self._get_stat_message_label(level, stat))

    def _get_level_button(self, level: Level) -> QPushButton:
        button = QPushButton(level.value)
        button.setProperty('class', 'button')
        button.setFixedSize(400, 100)
        button.clicked.connect(partial(self.start_game, level))
        return button

    def _get_stat_message_label(
            self, level: Level, stat: Statistics) -> QLabel:
        label = QLabel(self.get_stat_message(level, stat))
        label.setProperty('class', 'stat-text')
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        return label

    def get_stat_message(self, level: Level, stat: Statistics) -> str:
        if level == Level.BATTLE and stat == Statistics.BEST_TIME:
            return 'Сразись с монстрами!'
        else:
            value = self._data_model.stat_block[level.name][stat.name]
            stat_name = stat.value
            if value is None:
                value = 'Нет'
            return f'{stat_name}: {value}'

    def start_game(self, level: Level) -> None:
        self._data_model.current_level = level
        if level == level.BATTLE:
            self._ui_model.set_widget(WidgetType.BATTLE)
        else:
            self._ui_model.set_widget(WidgetType.LEARN)
