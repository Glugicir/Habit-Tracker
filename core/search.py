def search_habits(habits, query):
    """
    Возвращает список (индекс, привычка) для привычек,
    в названии которых встречается query (регистр не важен).

    Сложность: O(N × M), где N — привычек, M — длина query.
    """
    if not query:
        return list(enumerate(habits))

    query_lower = query.lower().strip()
    result = []

    for index, habit in enumerate(habits):
        if query_lower in habit["name"].lower():
            result.append((index, habit))

    return result


def search_with_ranking(habits, query):
    """
    Поиск с ранжированием:
    - Названия, начинающиеся с query, идут первыми.
    - Затем те, где query встречается как отдельное слово.
    - Затем все остальные совпадения.
    - Алфавитный порядок внутри каждой группы.

    Сложность: O(N × M + N log N).
    """
    if not query:
        return list(enumerate(habits))

    query_lower = query.lower().strip()
    matches = []

    for index, habit in enumerate(habits):
        name_lower = habit["name"].lower()
        if query_lower not in name_lower:
            continue

        # Определяем приоритет
        if name_lower.startswith(query_lower):
            priority = 0   # начинается с query
        elif f" {query_lower}" in name_lower:
            priority = 1   # отдельное слово
        else:
            priority = 2   # просто вхождение

        matches.append((priority, name_lower, index, habit))

    # Сортируем: сначала по приоритету, потом по алфавиту
    matches.sort(key=lambda x: (x[0], x[1]))

    return [(m[2], m[3]) for m in matches]