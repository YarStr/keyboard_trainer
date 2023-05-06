import json
import random
from pathlib import Path
from src.base_dir import BASE_DIR
from src.logic.level import Level

DATA_PATH = Path(BASE_DIR, 'storage', 'resources', 'levels.json')


def get_target_string_by_level(level: Level) -> str:
    with open(DATA_PATH, encoding='utf-8') as database:
        lessons = json.load(database)
        lesson_number = random.randint(0, len(lessons[level.name]) - 1)
        return lessons[level.name][lesson_number]
