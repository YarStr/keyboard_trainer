from PyQt6.QtWidgets import QApplication

from gui.main import MainWidget

if __name__ == '__main__':
    application = QApplication([])
    main_widget = MainWidget()
    main_widget.show()
    application.exec()
