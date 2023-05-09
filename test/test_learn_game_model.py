import unittest
from unittest.mock import patch, MagicMock

from src.logic.game.learn_game_model import LearnGameModel
from src.logic.level import Level

TEST_STRING = 'I love Python so much!'


class TestLearnGameModel(unittest.TestCase):
    @patch('src.logic.game.learn_game_model.src.storage.levels')
    def setUp(self, mock) -> None:
        mock.get_target_string_by_level = MagicMock(return_value=TEST_STRING)
        self.model = LearnGameModel(Level.START)
        self.is_game_finished = False
        self.model.game_finished.connect(self.game_finished)

    def game_finished(self):
        self.is_game_finished = True

    def check_handling_input_string(self, string: str, mistakes: int,
                                    is_mistake_done: bool) -> None:
        self.model.handle_string(string)
        self.assertEqual(self.model._is_mistake_done, is_mistake_done)
        self.assertEqual(self.model.mistakes, mistakes)

    def test_handle_correct_symbol(self):
        self.check_handling_input_string('I', mistakes=0,
                                         is_mistake_done=False)

    def test_handle_correct_uncompleted_string(self):
        self.check_handling_input_string('I love', mistakes=0,
                                         is_mistake_done=False)

    def test_handle_string_with_mistake_1(self):
        self.check_handling_input_string('Y', mistakes=1,
                                         is_mistake_done=True)

    def test_handle_string_with_mistake_2(self):
        self.check_handling_input_string('I love U', mistakes=1,
                                         is_mistake_done=True)

    def test_admit_and_correct_a_mistake(self):
        self.check_handling_input_string('I love U', mistakes=1,
                                         is_mistake_done=True)
        self.check_handling_input_string('I love ', mistakes=1,
                                         is_mistake_done=False)

    def test_handle_correct_completed_string(self):
        self.model.handle_string(TEST_STRING)
        self.assertEqual(self.is_game_finished, True)


if __name__ == '__main__':
    unittest.main()
