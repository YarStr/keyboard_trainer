import unittest
from collections import deque
from unittest.mock import patch

from src.logic.game.battle_game_model import BattleGameModel, Monster, \
    MonsterName

TEST_DRAGON = Monster(MonsterName.DRAGON, 2000)
TEST_BEHOLDER = Monster(MonsterName.BEHOLDER, 1000)
TEST_MIMIC = Monster(MonsterName.MIMIC, 3000)


def _get_test_monster_pool() -> deque[Monster]:
    pool = deque()
    pool.append(TEST_DRAGON)
    pool.append(TEST_BEHOLDER)
    pool.append(TEST_MIMIC)
    return pool


class TestBattleGameModel(unittest.TestCase):
    @patch('src.logic.game.battle_game_model._get_monsters_pool')
    def setUp(self, mock) -> None:
        mock.return_value = _get_test_monster_pool()
        self.model = BattleGameModel()

        self.is_word_typed = False
        self.model.game_finished.connect(self.word_typed)

        self.is_mistake_done = False
        self.model.mistake_done.connect(self.mistake_done)

        self.is_monster_dead = False
        self.model.monster_dead.connect(self.monster_dead)

    def mistake_done(self) -> None:
        self.is_mistake_done = True

    def word_typed(self) -> None:
        self.is_word_typed = True

    def monster_dead(self) -> None:
        self.is_monster_dead = True

    def check_choosing_target_string(self, string: str,
                                     expected_value: str | None) -> None:
        self.model.handle_string(string)
        self.assertEqual(self.model.target_string, expected_value)

    def check_monster_kill(self, monster: Monster):
        monster_name = monster.name.value
        self.model.handle_string(monster_name[0])
        self.model.handle_string(monster_name)
        self.assertEqual(None, self.model._target_string)
        self.assertEqual(True, monster not in self.model._monsters_pool)

    def test_chose_target_string_by_letter_d(self):
        self.check_choosing_target_string('d', MonsterName.DRAGON.value)

    def test_chose_target_string_by_letter_b(self):
        self.check_choosing_target_string('b', MonsterName.BEHOLDER.value)

    def test_chose_target_string_by_letter_m(self):
        self.check_choosing_target_string('m', MonsterName.MIMIC.value)

    def test_chose_target_string_by_incorrect_letter(self):
        self.check_choosing_target_string('x', None)
        self.assertEqual(True, self.is_mistake_done)

    def test_handle_mistake(self):
        self.model.handle_string('d')
        self.model.handle_string('db')
        self.assertEqual(1, self.model.mistakes)
        self.assertEqual(True, self.is_mistake_done)

    def test_handle_doing_and_fixing_mistake(self):
        self.test_handle_mistake()
        self.model.handle_string('d')
        self.assertEqual(1, self.model.mistakes)
        self.assertEqual(False, self.model._is_mistake_done)

    def test_kill_the_monsters(self):
        self.check_monster_kill(TEST_DRAGON)
        self.check_monster_kill(TEST_BEHOLDER)
        self.check_monster_kill(TEST_MIMIC)


if __name__ == '__main__':
    unittest.main()
