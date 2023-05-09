import random
from collections import namedtuple

from PyQt6 import QtCore
from PyQt6.QtCore import QPropertyAnimation, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout

from src.gui.ui_elements.monster_widget import MonsterWidget
from src.logic.game.battle_game_model import Monster, MonsterName

DRAGON = Monster(MonsterName.DRAGON, 1000)
TARRASQUE = Monster(MonsterName.TARRASQUE, 2000)

pool = [DRAGON, TARRASQUE]

MonsterData = namedtuple('MonsterData', 'widget animation')


def _get_corner_point() -> QPoint:
    variants = (0, 420)
    return QPoint(random.choice(variants), random.choice(variants))


class BattlefieldWidget(QWidget):
    monster_captured_flag = QtCore.pyqtSignal()

    def __init__(self, monsters_pool: list[Monster]):
        super().__init__()
        self.animation = None
        self.widget = None
        self.setFixedSize(500, 500)

        self.main_layout = QVBoxLayout()
        self._monsters_pool = monsters_pool
        self._monster_data_pool = []

        self.setLayout(self.main_layout)

    def get_animation(self, widget: MonsterWidget, ) -> QPropertyAnimation:
        animation = QPropertyAnimation(widget, b'pos')
        animation.setDuration(10000 - widget.speed)

        animation.setStartValue(_get_corner_point())
        animation.setEndValue(
            QPoint(self.width() // 2 - widget.width() // 2,
                   self.height() // 2 - widget.height() // 2))

        return animation

    @QtCore.pyqtSlot(Monster)
    def add_monster_widget(self, monster: Monster):
        widget = MonsterWidget(monster)
        animation = self.get_animation(widget)
        animation.finished.connect(self.method)

        self._monster_data_pool.append(
            MonsterData(widget=widget, animation=animation))

        self.main_layout.addWidget(widget)
        animation.start()

    @QtCore.pyqtSlot(int)
    def delete_monster_widget(self, index: int) -> None:
        animation = self._monster_data_pool[index].animation
        widget = self._monster_data_pool[index].widget

        animation.stop()
        self.main_layout.removeWidget(widget)
        widget.deleteLater()

        del self._monster_data_pool[index]

    @QtCore.pyqtSlot(int)
    def highlight_monster(self, index: int) -> None:
        self._monster_data_pool[index].widget.highlight_name()

    def method(self):
        self.monster_captured_flag.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0), 5)
        painter.setPen(pen)
        painter.drawEllipse(200, 200, 100, 100)

    def start(self):
        for monster in self._monsters_pool:
            self.add_monster_widget(monster)


if __name__ == '__main__':
    app = QApplication([])
    window = BattlefieldWidget(pool)
    window.show()
    app.exec()
