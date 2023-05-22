from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from src.base_dir import BASE_DIR
from src.logic.game.battle_game_model import Monster

DATA_PATH = Path(BASE_DIR, 'gui/resources/images')


class MonsterWidget(QWidget):
    def __init__(self, monster: Monster):
        super().__init__()
        self._name = monster.name.value
        self._speed = monster.speed
        self.setLayout(self._get_layout_with_image_and_name())
        self.setFixedSize(80, 80)

    def _get_layout_with_image_and_name(self) -> QVBoxLayout:
        image_label = self._get_image_label()
        self._name_label = self._get_name_label()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)
        layout.addWidget(self._name_label)

        return layout

    def _get_image_label(self) -> QLabel:
        label = QLabel()
        pixmap = QPixmap(self._get_image_path()).scaled(40, 40)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _get_name_label(self) -> QLabel:
        label = QLabel(self._name)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _get_image_path(self) -> str:
        return f'{DATA_PATH}/{self._name}.png'

    def highlight_name(self) -> None:
        self._name_label.setStyleSheet('font-weight: bold')

    @property
    def speed(self):
        return self._speed
