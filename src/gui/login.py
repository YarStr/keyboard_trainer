from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, \
    QLabel

from src.gui.widget_type import WidgetType
from src.gui.ui_model import UIModel
from src.logic.user_data_model import UserDataModel


class LoginWidget(QWidget):
    def __init__(self, ui_model: UIModel, data_model: UserDataModel):
        super().__init__()

        self._ui_model = ui_model
        self._data_model = data_model

        self._user_name_input = self.get_user_name_input()
        self._login_button = self.get_login_button()

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Привет!'))
        layout.addWidget(QLabel('Для входа в приложение надо залогиниться:'))
        layout.addWidget(self._user_name_input)
        layout.addWidget(self._login_button)

        self.setLayout(layout)

    def get_login_button(self) -> QPushButton:
        login_button = QPushButton('Войти')
        login_button.clicked.connect(self.go_to_levels)
        login_button.setEnabled(False)
        return login_button

    def get_user_name_input(self) -> QLineEdit:
        user_name_input = QLineEdit()
        user_name_input.textChanged.connect(self.react_on_changed_text)
        return user_name_input

    def react_on_changed_text(self) -> None:
        text = self._user_name_input.text()
        if text:
            self._login_button.setEnabled(True)
        else:
            self._login_button.setEnabled(False)

    def go_to_levels(self) -> None:
        user_name = self._user_name_input.text()
        self._data_model.load_user_by_name(user_name)
        self._ui_model.set_widget(WidgetType.LEVELS)
