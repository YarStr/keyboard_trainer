import random
from dataclasses import dataclass
from enum import Enum
from collections import deque

from PyQt6 import QtCore

from src.logic.game.game_model import GameModel


class MonsterName(Enum):
    DRAGON = 'dragon'
    BEHOLDER = 'beholder'
    MIMIC = 'mimic'
    OWLBEAR = 'owlbear'
    TARRASQUE = 'tarrasque'


@dataclass
class Monster:
    name: MonsterName
    speed: int


def _get_monsters_pool() -> deque[Monster]:
    pool = deque()
    for _ in range(1):
        pool.append(_get_random_monster())
    return pool


def _get_random_monster() -> Monster:
    random_number = random.randint(0, len(MonsterName) - 1)
    for index, monster_name in enumerate(MonsterName):
        if index == random_number:
            return Monster(monster_name, _get_random_speed())


def _get_random_speed() -> int:
    return random.randint(1000, 2000)


class BattleGameModel(GameModel):
    monster_dead = QtCore.pyqtSignal(int)
    highlight_monster_name = QtCore.pyqtSignal(int)
    monster_captured_flag = QtCore.pyqtSignal()
    monster_added = QtCore.pyqtSignal(Monster)

    def __init__(self):
        self._monsters_pool = _get_monsters_pool()
        self._target_monster_position = None
        super().__init__()
        self.timer_updated.connect(self._on_timer_updated)
        self.monster_captured_flag.connect(self._on_monster_captured_flag)

    def _get_target_string(self) -> str | None:
        if self._target_monster_position is None:
            return None
        else:
            return self._monsters_pool[
                self._target_monster_position].name.value

    def handle_string(self, string: str) -> None:
        if string:
            if self._target_monster_position is not None:
                super().handle_string(string)
            else:
                self._chose_target_monster(string)
                self._target_string = self._get_target_string()

    def _chose_target_monster(self, string: str) -> None:
        for position, monster in enumerate(self._monsters_pool):
            if monster.name.value.startswith(string):
                self._target_monster_position = position
                self.highlight_monster_name.emit(position)
                return
        self.mistake_done.emit(self._mistakes)

    def _react_on_word_typed(self) -> None:
        self.monster_dead.emit(self._target_monster_position)
        self._target_string = None
        del self._monsters_pool[self._target_monster_position]
        self._target_monster_position = None

    @QtCore.pyqtSlot()
    def _on_timer_updated(self) -> None:
        if self._time.second() == 15:
            self.game_finished.emit(True)
        elif self._time.second() % 2 == 0:
            self._add_monster()
            self.monster_added.emit(self._monsters_pool[-1])

    def _add_monster(self) -> None:
        self._monsters_pool.append(_get_random_monster())

    @QtCore.pyqtSlot()
    def _on_monster_captured_flag(self):
        self.game_finished.emit(False)

    @property
    def monsters_pool(self):
        return self._monsters_pool
