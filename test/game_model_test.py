import unittest
from unittest.mock import patch, MagicMock

from src.logic.game_model import GameModel
from src.logic.levels import Levels

TEST_STRING = 'I love Python so much!'


class TestGameModel(unittest.TestCase):
    @patch('src.logic.game_model.src.storage.levels')
    def setUp(self, mock) -> None:
        mock.get_target_string_by_level = MagicMock(return_value=TEST_STRING)
        self.model = GameModel(Levels.START)
        self.is_game_finished = False
        self.model.game_finished.connect(self.game_finished)

    def game_finished(self):
        self.is_game_finished = True

    def test_handle_correct_symbol_1(self):
        symbol = ''
        self.model.handle_string(symbol)
        self.assertEqual(self.model._is_mistake_still_there, False)
        self.assertEqual(self.model.mistakes, 0)

    def test_handle_correct_symbol_2(self):
        symbol = 'I'
        self.model.handle_string(symbol)
        self.assertEqual(self.model._is_mistake_still_there, False)
        self.assertEqual(self.model.mistakes, 0)

    def test_handle_correct_uncompleted_string(self):
        string = 'I love'
        self.model.handle_string(string)
        self.assertEqual(self.model._is_mistake_still_there, False)
        self.assertEqual(self.model.mistakes, 0)

    def test_handle_string_with_mistake_1(self):
        string = 'Y'
        self.model.handle_string(string)
        self.assertEqual(self.model._is_mistake_still_there, True)
        self.assertEqual(self.model.mistakes, 1)

    def test_handle_string_with_mistake_2(self):
        string = 'I love U'
        self.model.handle_string(string)
        self.assertEqual(self.model._is_mistake_still_there, True)
        self.assertEqual(self.model.mistakes, 1)

    def test_admit_and_correct_a_mistake(self):
        mistake_string = 'I love U'
        self.model.handle_string(mistake_string)
        self.assertEqual(self.model._is_mistake_still_there, True)
        self.assertEqual(self.model.mistakes, 1)

        fixed_mistake_string = 'I love '
        self.model.handle_string(fixed_mistake_string)
        self.assertEqual(self.model._is_mistake_still_there, False)
        self.assertEqual(self.model.mistakes, 1)

    def test_handle_correct_completed_string(self):
        self.model.handle_string(TEST_STRING)
        self.assertEqual(self.is_game_finished, True)


if __name__ == '__main__':
    unittest.main()
