from functools import partial

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from src.gui.widget_type import WidgetType
from src.logic.statistics import Statistics
from src.gui.ui_model import UIModel
from src.logic.user_data_model import UserDataModel

from src.storage.levels import Levels


class LevelWidget(QWidget):
    def __init__(self, ui_model: UIModel, data_model: UserDataModel):
        super().__init__()
        self._ui_model = ui_model
        self._data_model = data_model
        self.setLayout(self.get_main_layout())

    def get_main_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.addWidget(QLabel(self.get_hello_message()))
        layout.addWidget(QLabel('Выбери уровень:'))
        self.add_level_widgets_to_layout(layout)
        return layout

    def get_hello_message(self) -> str:
        return f'Итак, {self._data_model.user_name}, вот твоя статистика!'

    def add_level_widgets_to_layout(self, layout: QVBoxLayout):
        for level in Levels:
            layout.addWidget(self.get_level_button(level))
            for stat in Statistics:
                layout.addWidget(QLabel(self.get_stat_message(level, stat)))

    def get_level_button(self, level: Levels) -> QPushButton:
        button = QPushButton(level.value)
        button.clicked.connect(partial(self.start_game, level))
        return button

    def get_stat_message(self, level: Levels, stat: Statistics) -> str:
        value = self._data_model.stat_block[level.name][stat.name]
        stat_name = stat.value
        if value is None:
            value = 'Нет результата'
        return f'{stat_name}: {value}'

    def start_game(self, level: Levels) -> None:
        self._data_model.current_level = level
        self._ui_model.set_widget(WidgetType.GAME)
