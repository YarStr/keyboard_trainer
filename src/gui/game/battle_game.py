from functools import partial

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget

from src.gui.game.game import GameWidget
from src.gui.ui_elements.battlefield_widget import BattlefieldWidget
from src.logic.game.battle_game_model import BattleGameModel
from src.logic.game.game_model import GameModel

from src.gui.ui_model import UIModel
from src.logic.user_data_model import UserDataModel


class BattleGameWidget(GameWidget):
    def __init__(self, ui_model: UIModel, data_model: UserDataModel):
        super().__init__(ui_model, data_model)

    def _get_game_model(self) -> GameModel:
        return BattleGameModel()

    def _get_target_widget(self) -> QWidget:
        return BattlefieldWidget(self._game_model.monsters_pool)

    def _connect_game_model_signals(self) -> None:
        super()._connect_game_model_signals()

        self._game_model.highlight_monster_name.connect(
            self._target_widget.highlight_monster)

        self._game_model.monster_dead.connect(
            self._target_widget.delete_monster_widget
        )

        self._game_model.monster_dead.connect(
            partial(self._game_line_input.setText, '')
        )

        self._target_widget.monster_captured_flag.connect(
            self.exit
        )

        self._game_model.monster_added.connect(
            self._target_widget.add_monster_widget
        )

        self._game_model.game_finished.connect(
            self.end_game
        )

    def start(self) -> None:
        super().start()
        self._target_widget.start()

    @QtCore.pyqtSlot()
    def end_game(self):
        self.on_game_finished()
