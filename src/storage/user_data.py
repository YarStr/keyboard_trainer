import json
from pathlib import Path
from src.config import BASE_DIR
from src.logic.levels import Levels
from src.logic.statistics import Statistics

DATA_PATH = Path(BASE_DIR, "storage", "resources", "users.json")

BEST_TIME = Statistics.BEST_TIME.name
MIN_MISTAKES = Statistics.MIN_MISTAKES.name


def get_statistics_from_database(user_name: str) -> dict:
    lower_name = user_name.casefold()
    with open(DATA_PATH, encoding="utf-8") as database:
        users_statistics = json.load(database)
        if lower_name in users_statistics:
            return users_statistics[lower_name]
        else:
            empty_stat_block = _get_empty_stat_block()
            load_statistics_to_database(user_name, empty_stat_block)
            return empty_stat_block


def _get_empty_stat_block() -> dict:
    return {
        Levels.START.name: {
            BEST_TIME: None,
            MIN_MISTAKES: None
        },
        Levels.MIDDLE.name: {
            BEST_TIME: None,
            MIN_MISTAKES: None
        },
        Levels.HARD.name: {
            BEST_TIME: None,
            MIN_MISTAKES: None
        }
    }


def load_statistics_to_database(user_name: str, data: dict) -> None:
    lower_name = user_name.casefold()
    with open(DATA_PATH, encoding="utf-8") as database:
        users_statistics = json.load(database)
        users_statistics[lower_name] = data
        with open(DATA_PATH, "w") as json_storage:
            json_storage.write(json.dumps(users_statistics, indent=4))
