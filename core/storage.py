"""
storage.py — модуль для сохранения и загрузки данных.
Отвечает только за работу с файлом habits.json.
"""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "habits.json")


def load_habits():
    """Загружает список привычек из файла."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_habits(habits):
    """Сохраняет список привычек в файл."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(habits, f, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"Ошибка сохранения: {e}")