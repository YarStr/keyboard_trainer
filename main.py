from PyQt6.QtWidgets import QApplication

from src.gui.main import MainWidget


def get_style_sheet() -> str:
    with open('src/gui/resources/style_sheet.css', 'r') as file:
        return file.read()


if __name__ == '__main__':
    application = QApplication([])
    application.setStyleSheet(get_style_sheet())
    main_widget = MainWidget()
    main_widget.show()
    application.exec()
