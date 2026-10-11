[![Release](https://img.shields.io/github/v/release/твой-ник/habit-tracker?style=for-the-badge&color=blue)](https://github.com/твой-ник/habit-tracker/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
# 🌱 Трекер привычек

Приложение для отслеживания ежедневных привычек с современным тёмным интерфейсом на CustomTkinter.


## ✨ Возможности

- 📋 Добавление привычек и отметка выполнения в один клик
- 📅 Календарь недели с навигацией по прошлым неделям
- 🔥 Подсчёт серий (streak) — сколько дней подряд выполняешь
- 🏆 Система достижений: 🌱 3 дня, 🔥 7 дней, 💪 14 дней, 🏆 30 дней, 👑 100 дней
- 📈 Прогресс-бар выполнения за сегодня
- 📤 Экспорт данных в CSV (открывается в Excel)
- 📊 График активности за месяц (matplotlib)
- 🌑 Тёмная тема в стиле Catppuccin Mocha
- 🔔 Напоминание вечером, если привычки не отмечены

## 🛠️ Технологии

- **Python 3.12+**
- **CustomTkinter** — современный UI поверх tkinter
- **matplotlib** — график активности
- **Pillow** — работа с иконкой
- **JSON** — хранение данных
- **PyInstaller** — сборка в `.exe`

## 📁 Структура проекта
```text
habit_tracker/
│
├── main.py                  # Точка входа в приложение
├── requirements.txt         # Список зависимостей
├── README.md                # Описание проекта
├── .gitignore               # Что не коммитить в Git
│
├── core/                    # Бизнес-логика (не зависит от UI)
│   ├── __init__.py
│   ├── storage.py           # Чтение/запись JSON
│   ├── habits.py            # Операции с привычками
│   ├── stats.py             # Статистика (streak, неделя, месяц)
│   └── achievements.py      # Система достижений
│
├── ui/                      # Интерфейс на CustomTkinter
│   ├── __init__.py
│   ├── app.py               # Главное окно
│   ├── header.py            # Заголовок + прогресс-бар
│   ├── input_panel.py       # Поле ввода + фильтр
│   ├── habit_list.py        # Список привычек с календарём
│   ├── actions_panel.py     # Кнопки действий
│   ├── dev_panel.py         # DEV-инструменты
│   ├── chart_window.py      # Окно с графиком (matplotlib)
│   └── edit_dialog.py       # Диалог переименования
│
├── assets/                  # Ресурсы
│   ├── icon.ico             # Иконка приложения
│   └── icon.png             # Иконка в PNG
│
└── data/                    # Данные (создаётся автоматически)
    ├── habits.json          # Привычки пользователя
    └── exports/             # Экспортированные CSV
        └── habits_export.csv
```
