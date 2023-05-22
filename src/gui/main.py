from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.exceptions.exceptions import UnknownWidgetException
from src.gui.widget_type import WidgetType
from src.gui.game import GameWidget
from src.gui.login import LoginWidget

from src.gui.levels import LevelWidget
from src.gui.ui_model import UIModel
from src.logic.user_data_model import UserDataModel


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self._ui_model = UIModel()
        self._ui_model.widget_changed.connect(self.on_model_widget_changed)

        self._data_model = UserDataModel()

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
        models = self._ui_model, self._data_model
        match widget_type:
            case WidgetType.LOGIN:
                return LoginWidget(*models)
            case WidgetType.LEVELS:
                return LevelWidget(*models)
            case WidgetType.GAME:
                return GameWidget(*models)
            case _:
                raise UnknownWidgetException(
                    f'Виджет типа {widget_type} не существует!')
