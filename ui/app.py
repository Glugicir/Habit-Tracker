"""
app.py — главное окно. Собирает всё вместе.
"""

import customtkinter as ctk
from tkinter import messagebox, simpledialog
import datetime
import os
import subprocess
import sys

from ui.header import Header
from ui.input_panel import InputPanel
from ui.habit_list import HabitList
from ui.actions_panel import ActionsPanel
from ui.dev_panel import DevPanel
from ui.chart_window import ChartWindow
from ui.edit_dialog import EditDialog
from core.search import search_habits, search_with_ranking
from core.sorting import sort_habits

from core.storage import load_habits, save_habits
from core.habits import (add_habit, delete_habit, mark_done, unmark_done,
                    is_done_today, export_to_csv)
from core.stats import count_streak
from core.achievements import check_achievement


class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер привычек")
        self.root.geometry("1060x780")
        self.root.minsize(940, 660)

        self.habits = load_habits()
        self.only_undone = ctk.BooleanVar(value=False)
        self.selected_index = None

        self._build_ui()
        self.refresh_all()
        self._check_reminder()

    # ==================== СБОРКА ====================

    def _build_ui(self):
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.header = Header(self.root)
        self.header.grid(row=0, column=0, sticky="ew", padx=25, pady=(10, 6))

        card_input = ctk.CTkFrame(self.root, corner_radius=12)
        card_input.grid(row=1, column=0, sticky="ew", padx=25, pady=(0, 12))
        self.input_panel = InputPanel(
            card_input,
            on_add=self.on_add,
            on_search=self.on_search,
            on_sort=self.on_sort,
            only_undone_var=self.only_undone
        )
        self.input_panel.pack(fill="x", padx=14, pady=14)
        self.input_panel.bind("<<FilterChanged>>", lambda e: self.refresh_all())
        self.input_panel.bind("<<SearchChanged>>", lambda e: self.on_search())
        self.input_panel.bind("<<SortChanged>>", lambda e: self.on_sort())

        self.actions = ActionsPanel(
            self.root,
            on_mark=self.on_mark,
            on_unmark=self.on_unmark,
            on_delete=self.on_delete,
            on_mark_all=self.on_mark_all,
            on_export=self.on_export,
            on_chart=self.on_chart
        )
        self.actions.grid(row=3, column=0, pady=(0, 10))

        self.dev = DevPanel(
            self.root,
            on_minus=self.on_dev_minus_day,
            on_plus=self.on_dev_plus_day,
            on_date=self.on_dev_add_date,
            on_clear=self.on_dev_clear
        )
        self.dev.grid(row=4, column=0, sticky="ew", padx=25, pady=(0, 16))

    # ==================== ОБНОВЛЕНИЕ ====================

    def refresh_all(self):
        """Обновляет счётчик и перерисовывает список с учётом поиска и сортировки."""
        # 1. Счётчик
        total = len(self.habits)
        done = sum(1 for h in self.habits if is_done_today(h))
        self.header.set_counter(done, total)

        # 2. Фильтрация по поиску
        query = self.input_panel.get_search_query()
        if query.strip():
            # Используем поиск с ранжированием — релевантные вперёд
            filtered = search_with_ranking(self.habits, query)
        else:
            filtered = list(enumerate(self.habits))

        # 3. Сортировка
        sort_type = self.input_panel.get_sort_type()
        if sort_type != "name" or True:
            # Сортируем только те, что в filtered
            indices = [i for i, _ in filtered]
            habit_objects = [h for _, h in filtered]
            sorted_objects = sort_habits(habit_objects, sort_type=sort_type)

            # Перестраиваем индексы в соответствии с сортировкой
            # (нужно для того, чтобы клик по строке работал правильно)
            new_filtered = []
            used = set()
            for h in sorted_objects:
                for orig_i, orig_h in filtered:
                    if orig_h is h and orig_i not in used:
                        new_filtered.append((orig_i, h))
                        used.add(orig_i)
                        break
            filtered = new_filtered

        # 4. Фильтр «только невыполненные»
        if self.only_undone.get():
            filtered = [(i, h) for i, h in filtered if not is_done_today(h)]

        # 5. Перерисовка
        self.habit_list.selected_index = self.selected_index
        self.habit_list.render_filtered(filtered)

    # ==================== ВЫБОР ====================

    def _get_selected(self):
        if self.selected_index is None or self.selected_index >= len(self.habits):
            messagebox.showinfo("Подсказка", "Сначала кликни по привычке.")
            return None
        return self.selected_index

    def on_select(self, index):
        self.selected_index = index
        self.refresh_all()

    def on_search(self):
        """Перерисовать список с учётом поиска."""
        self.refresh_all()

    def on_sort(self):
        """Перерисовать список с учётом сортировки."""
        self.refresh_all()

    def on_double_click(self, index):
        self.selected_index = index
        ok, msg, streak = self._mark_and_check(index)
        if not ok:
            messagebox.showinfo("Информация", msg)
        else:
            self._show_achievement(streak)
        self.refresh_all()

    def on_right_click(self, index, event):
        """Правый клик — контекстное меню."""
        import tkinter as tk
        popup = tk.Menu(
            self.root, tearoff=0,
            bg="#2b2b2b", fg="white",
            activebackground="#3b8ed0", activeforeground="white"
        )
        popup.add_command(label="✏️  Переименовать",
                          command=lambda: self.on_rename(index))
        popup.add_command(label="🗑  Удалить",
                          command=lambda: self.on_delete_index(index))
        try:
            popup.tk_popup(event.x_root, event.y_root)
        finally:
            popup.grab_release()

    def on_rename(self, index):
        current = self.habits[index]["name"]

        def save(new_name):
            self.habits[index]["name"] = new_name
            save_habits(self.habits)
            self.refresh_all()

        EditDialog(self.root, current, save)

    def on_delete_index(self, index):
        name = self.habits[index]["name"]
        if messagebox.askyesno("Удаление", f"Удалить привычку '{name}'?"):
            delete_habit(self.habits, index)
            self.selected_index = None
            self.refresh_all()

    # ==================== АЧИВКИ ====================

    def _mark_and_check(self, index):
        """Отмечает привычку и возвращает серию для проверки ачивки."""
        ok, msg = mark_done(self.habits, index)
        if not ok:
            return False, msg, 0
        streak = count_streak(self.habits[index]["history"])
        return True, msg, streak

    def _show_achievement(self, streak):
        ach = check_achievement(streak)
        if ach:
            emoji, title, desc = ach
            messagebox.showinfo(
                f"{emoji} {title}",
                f"{desc}\n\n🔥 Серия: {streak} дней подряд!"
            )

    # ==================== ДЕЙСТВИЯ ====================

    def on_add(self):
        text = self.input_panel.get_text()
        ok, msg = add_habit(self.habits, text)
        if ok:
            self.input_panel.clear()
            self.refresh_all()
        else:
            messagebox.showwarning("Ошибка", msg)

    def on_mark(self):
        idx = self._get_selected()
        if idx is None:
            return
        ok, msg, streak = self._mark_and_check(idx)
        if not ok:
            messagebox.showinfo("Информация", msg)
        else:
            self._show_achievement(streak)
        self.refresh_all()

    def on_unmark(self):
        idx = self._get_selected()
        if idx is None:
            return
        ok, msg = unmark_done(self.habits, idx)
        if not ok:
            messagebox.showinfo("Информация", msg)
        self.refresh_all()

    def on_delete(self):
        idx = self._get_selected()
        if idx is None:
            return
        self.on_delete_index(idx)

    def on_mark_all(self):
        count = 0
        achievements_shown = set()
        for h in self.habits:
            if not is_done_today(h):
                h["history"].append(datetime.date.today().isoformat())
                count += 1
                streak = count_streak(h["history"])
                ach = check_achievement(streak)
                if ach:
                    achievements_shown.add(f"{ach[0]} {ach[1]}")
        if count:
            save_habits(self.habits)
            self.refresh_all()
            msg = f"Отмечено привычек: {count}"
            if achievements_shown:
                msg += "\n\n🏆 Получены достижения:\n" + "\n".join(achievements_shown)
            messagebox.showinfo("Готово", msg)
        else:
            messagebox.showinfo("Информация", "Все привычки уже отмечены на сегодня.")

    # ==================== ЭКСПОРТ И ГРАФИК ====================

    def on_export(self):
        ok, result = export_to_csv(self.habits)
        if ok:
            messagebox.showinfo(
                "Экспорт готов",
                f"Файл сохранён:\n{result}\n\n"
                f"Можно открыть в Excel."
            )
            # Попробуем открыть папку с файлом
            try:
                folder = os.path.dirname(result)
                if sys.platform == "win32":
                    os.startfile(folder)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", folder])
                else:
                    subprocess.Popen(["xdg-open", folder])
            except Exception:
                pass
        else:
            messagebox.showerror("Ошибка экспорта", result)

    def on_chart(self):
        if not self.habits:
            messagebox.showinfo("График", "Нет данных для построения графика.")
            return
        ChartWindow(self.root, self.habits)

    # ==================== DEV ====================

    def _append_date(self, idx, date_str):
        habit = self.habits[idx]
        if date_str in habit["history"]:
            messagebox.showinfo("DEV", f"{date_str} уже есть.")
            return
        habit["history"].append(date_str)
        habit["history"].sort()
        save_habits(self.habits)
        self.refresh_all()

    def on_dev_minus_day(self):
        idx = self._get_selected()
        if idx is None:
            return
        habit = self.habits[idx]
        if not habit["history"]:
            new_date = datetime.date.today()
        else:
            earliest = datetime.date.fromisoformat(min(habit["history"]))
            new_date = earliest - datetime.timedelta(days=1)
        self._append_date(idx, new_date.isoformat())

    def on_dev_plus_day(self):
        idx = self._get_selected()
        if idx is None:
            return
        habit = self.habits[idx]
        if not habit["history"]:
            new_date = datetime.date.today()
        else:
            latest = datetime.date.fromisoformat(max(habit["history"]))
            new_date = latest + datetime.timedelta(days=1)
        self._append_date(idx, new_date.isoformat())

    def on_dev_add_date(self):
        idx = self._get_selected()
        if idx is None:
            return
        default = datetime.date.today().isoformat()
        date = simpledialog.askstring(
            "DEV: добавить дату",
            "Введи дату в формате ГГГГ-ММ-ДД:",
            initialvalue=default
        )
        if not date:
            return
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            messagebox.showerror("DEV", "Неверный формат. Нужно ГГГГ-ММ-ДД.")
            return
        self._append_date(idx, date)

    def on_dev_clear(self):
        idx = self._get_selected()
        if idx is None:
            return
        if not messagebox.askyesno("DEV", "Очистить всю историю этой привычки?"):
            return
        self.habits[idx]["history"] = []
        save_habits(self.habits)
        self.refresh_all()

    # ==================== НАПОМИНАНИЕ ПРИ ЗАПУСКЕ ====================

    def _check_reminder(self):
        """Если сейчас вечер и есть невыполненные привычки — напоминаем."""
        now = datetime.datetime.now()
        if now.hour < 18:
            return
        undone = [h for h in self.habits if not is_done_today(h)]
        if not undone:
            return

        names = "\n".join(f"• {h['name']}" for h in undone[:5])
        if len(undone) > 5:
            names += f"\n...и ещё {len(undone) - 5}"

        self.root.after(600, lambda: messagebox.showinfo(
            "🔔 Напоминание",
            f"Уже вечер, а эти привычки ещё не отмечены:\n\n{names}"
        ))