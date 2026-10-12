import datetime
from core.stats import count_streak, total_done


# ==================== КЛЮЧИ СОРТИРОВКИ ====================

def key_by_name(habit):
    """Ключ: по названию (регистр не важен)."""
    return habit["name"].lower()


def key_by_created(habit):
    """Ключ: по дате создания."""
    return habit["created"]


def key_by_streak(habit):
    """Ключ: по серии (по убыванию — поэтому отрицательное значение)."""
    return -count_streak(habit["history"])


def key_by_total(habit):
    """Ключ: по количеству выполнений (по убыванию)."""
    return -total_done(habit)


# ==================== ВСТРОЕННАЯ СОРТИРОВКА ====================

def sort_habits(habits, sort_type="name", reverse=False):
    """
    Сортирует привычки через встроенную сортировку Python.

    sort_type:
        "name"    — по названию
        "created" — по дате создания
        "streak"  — по серии
        "total"   — по количеству выполнений

    Сложность: O(N log N) — Timsort, гибрид merge sort и insertion sort.
    """
    keys = {
        "name": key_by_name,
        "created": key_by_created,
        "streak": key_by_streak,
        "total": key_by_total,
    }
    key_func = keys.get(sort_type, key_by_name)

    # Для streak и total порядок уже «по убыванию» в ключе,
    # поэтому reverse применяем только к name и created
    if sort_type in ("name", "created"):
        return sorted(habits, key=key_func, reverse=reverse)
    else:
        return sorted(habits, key=key_func)


# ==================== УЧЕБНАЯ РЕАЛИЗАЦИЯ QUICKSORT ====================

def quicksort(habits, key_func=None):
    """
    Быстрая сортировка (quicksort) — учебная реализация.

    Сложность:
    - В среднем: O(N log N)
    - В худшем:   O(N²) — если pivot всегда min или max.
    - Память:     O(log N) — глубина рекурсии.

    Это классический алгоритм «разделяй и властвуй».
    """
    if key_func is None:
        key_func = key_by_name

    if len(habits) <= 1:
        return habits[:]

    pivot = habits[len(habits) // 2]
    pivot_key = key_func(pivot)

    left = [h for h in habits if key_func(h) < pivot_key]
    middle = [h for h in habits if key_func(h) == pivot_key]
    right = [h for h in habits if key_func(h) > pivot_key]

    return quicksort(left, key_func) + middle + quicksort(right, key_func)