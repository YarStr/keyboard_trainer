from PyQt6 import QtCore
from PyQt6.QtCore import QObject

from gui.widget_type import WidgetType


class UIModel(QObject):
    widget_changed = QtCore.pyqtSignal(WidgetType)

    def __init__(self):
        super().__init__()

    def set_widget(self, widget_type: WidgetType):
        self.widget_changed.emit(widget_type)
