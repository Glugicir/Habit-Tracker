"""
habits.py — логика работы с привычками.
Без интерфейса и без сохранения — только операции над данными.
"""

import datetime
import csv
import os
from core.storage import save_habits


def today_str():
    """Возвращает сегодняшнюю дату в формате 'ГГГГ-ММ-ДД'."""
    return datetime.date.today().isoformat()


def add_habit(habits, name):
    """Добавляет новую привычку. Возвращает (успех, сообщение)."""
    name = name.strip()
    if not name:
        return False, "Название не может быть пустым."

    for h in habits:
        if h["name"].lower() == name.lower():
            return False, f"Привычка '{name}' уже существует."

    habits.append({
        "name": name,
        "created": today_str(),
        "history": []
    })
    save_habits(habits)
    return True, f"Привычка '{name}' добавлена."


def delete_habit(habits, index):
    """Удаляет привычку по индексу."""
    if index < 0 or index >= len(habits):
        return False, "Неверный индекс."
    name = habits[index]["name"]
    habits.pop(index)
    save_habits(habits)
    return True, f"Привычка '{name}' удалена."


def mark_done(habits, index):
    """Отмечает привычку выполненной сегодня."""
    if index < 0 or index >= len(habits):
        return False, "Неверный индекс."

    habit = habits[index]
    today = today_str()

    if today in habit["history"]:
        return False, f"'{habit['name']}' уже отмечена на сегодня."

    habit["history"].append(today)
    save_habits(habits)
    return True, f"'{habit['name']}' отмечена! 🎉"


def unmark_done(habits, index):
    """Снимает отметку за сегодня."""
    if index < 0 or index >= len(habits):
        return False, "Неверный индекс."

    habit = habits[index]
    today = today_str()

    if today not in habit["history"]:
        return False, f"'{habit['name']}' ещё не отмечена сегодня."

    habit["history"].remove(today)
    save_habits(habits)
    return True, f"Отметка с '{habit['name']}' снята."


def is_done_today(habit):
    """Проверяет, выполнена ли привычка сегодня."""
    return today_str() in habit["history"]

def export_to_csv(habits, filename="habits_export.csv"):
    """
    Экспортирует привычки в CSV в папку data/exports/.
    Даты форматируются как ДД.ММ.ГГГГ для совместимости с Excel.
    """
    if not habits:
        return False, "Нет данных для экспорта."

    import os
    import csv
    from datetime import date

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    export_dir = os.path.join(base_dir, "data", "exports")
    os.makedirs(export_dir, exist_ok=True)

    path = os.path.join(export_dir, filename)

    def fmt_date(iso_str):
        """2026-10-12 → 12.10.2026"""
        try:
            y, m, d = iso_str.split("-")
            return f"{d}.{m}.{y}"
        except (ValueError, AttributeError):
            return iso_str

    try:
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow([
                "Привычка", "Создана", "Всего выполнено",
                "Серия (дн.)", "Даты выполнения"
            ])

            from core.stats import count_streak, total_done

            for h in habits:
                streak = count_streak(h["history"])
                total = total_done(h)
                dates = ", ".join(
                    fmt_date(d) for d in sorted(h["history"])
                ) if h["history"] else "—"

                writer.writerow([
                    h["name"],
                    fmt_date(h["created"]),
                    total,
                    streak,
                    dates
                ])

        return True, path
    except OSError as e:
        return False, f"Ошибка записи: {e}"