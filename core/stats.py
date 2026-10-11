"""
stats.py — подсчёт статистики по привычкам.
"""

import datetime


def count_streak(history):
    """Считает серию дней подряд, включая сегодня."""
    if not history:
        return 0

    dates = set(history)
    today = datetime.date.today()
    streak = 0
    check = today

    while check.isoformat() in dates:
        streak += 1
        check -= datetime.timedelta(days=1)

    return streak


def week_status(habit):
    """Возвращает список из 7 True/False для текущей недели (Пн..Вс)."""
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())

    result = []
    for i in range(7):
        day = monday + datetime.timedelta(days=i)
        result.append(day.isoformat() in habit["history"])
    return result


def total_done(habit):
    """Сколько раз привычка была выполнена всего."""
    return len(set(habit["history"]))

def activity_for_month(habit, year=None, month=None):
    """
    Возвращает список (день_месяца, выполнено?) для всех дней месяца.
    Если year/month не указаны — берётся текущий месяц.
    """
    today = datetime.date.today()
    year = year or today.year
    month = month or today.month

    # Первый день месяца и количество дней в нём
    first_day = datetime.date(year, month, 1)
    if month == 12:
        next_month = datetime.date(year + 1, 1, 1)
    else:
        next_month = datetime.date(year, month + 1, 1)
    days_in_month = (next_month - first_day).days

    history_set = set(habit["history"])
    result = []
    for day in range(1, days_in_month + 1):
        date = datetime.date(year, month, day)
        result.append((day, date.isoformat() in history_set))
    return result


def total_done_in_month(habits, year=None, month=None):
    """
    Возвращает список из N чисел — сколько привычек выполнено
    в каждый день месяца (сумма по всем привычкам).
    """
    today = datetime.date.today()
    year = year or today.year
    month = month or today.month

    first_day = datetime.date(year, month, 1)
    if month == 12:
        next_month = datetime.date(year + 1, 1, 1)
    else:
        next_month = datetime.date(year, month + 1, 1)
    days_in_month = (next_month - first_day).days

    counts = [0] * days_in_month
    for h in habits:
        for date_str in h["history"]:
            try:
                d = datetime.date.fromisoformat(date_str)
            except ValueError:
                continue
            if d.year == year and d.month == month:
                counts[d.day - 1] += 1
    return counts