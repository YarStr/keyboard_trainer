from collections import defaultdict
from pathlib import Path

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.base_dir import BASE_DIR
from src.exceptions.exceptions import UnknownWidgetException
from src.gui.game.battle_game import BattleGameWidget
from src.gui.widget_type import WidgetType
from src.gui.game.learn_game import LearnGameWidget
from src.gui.login import LoginWidget

from src.gui.levels import LevelWidget
from src.gui.ui_model import UIModel
from src.logic.user_data_model import UserDataModel

ICON_PATH = Path(BASE_DIR, 'gui/resources/images/icon.png')


def _default_widget_value():
    raise UnknownWidgetException


_widget = defaultdict(_default_widget_value)
_widget[WidgetType.LOGIN.name] = LoginWidget
_widget[WidgetType.LEVELS.name] = LevelWidget
_widget[WidgetType.LEARN.name] = LearnGameWidget
_widget[WidgetType.BATTLE.name] = BattleGameWidget


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon(str(ICON_PATH)))

        self._ui_model = UIModel()
        self._ui_model.widget_changed.connect(self.on_model_widget_changed)

        self._data_model = UserDataModel()

        self.setProperty('class', 'main-layout')

        self._layout = QVBoxLayout()
        self._widget = LoginWidget(self._ui_model, self._data_model)
        self._layout.addWidget(self._widget)

        self.setLayout(self._layout)

    @QtCore.pyqtSlot(WidgetType)
    def on_model_widget_changed(self, widget_type: WidgetType) -> None:
        self._layout.removeWidget(self._widget)
        self._widget.deleteLater()
        self._widget = self.get_widget_by_type(widget_type)
        self._layout.addWidget(self._widget)

    def get_widget_by_type(self, widget_type: WidgetType) -> QWidget:
        try:
            models = self._ui_model, self._data_model
            return _widget[widget_type.name](*models)

        except UnknownWidgetException:
            raise NotImplementedError(
                f'Виджет типа {widget_type} не существует!')
