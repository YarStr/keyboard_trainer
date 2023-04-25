from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit


class GameLineEdit(QLineEdit):
    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Backspace and self.isReadOnly():
            text = self.text()
            self.setText(text[:-1])
        else:
            super().keyPressEvent(event)
