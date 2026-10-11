"""
habit_list.py — список привычек с календарём и навигацией по неделям.
"""

import customtkinter as ctk
import datetime

from core.habits import is_done_today
from core.stats import count_streak, week_status, total_done


WEEKDAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]


class HabitList(ctk.CTkFrame):
    """Список привычек с шапкой, календарём недели и навигацией."""

    def __init__(self, parent, on_select, on_double_click, on_right_click):
        super().__init__(parent, fg_color="transparent")

        self.on_select = on_select
        self.on_double_click = on_double_click
        self.on_right_click = on_right_click
        self.selected_index = None

        # Смещение недель: 0 = текущая, -1 = прошлая, +1 = следующая
        self.week_offset = 0

        self._build_header()
        self._build_scroll_area()

    def _build_header(self):
        """Шапка: навигация недель + названия колонок."""
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(4, 4))

        # Кнопки навигации
        ctk.CTkButton(
            top, text="←", width=32, height=26,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3a3a3a", hover_color="#4a4a4a",
            corner_radius=6, command=self._prev_week
        ).pack(side="left")

        ctk.CTkButton(
            top, text="→", width=32, height=26,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3a3a3a", hover_color="#4a4a4a",
            corner_radius=6, command=self._next_week
        ).pack(side="left", padx=(4, 8))

        self.week_label = ctk.CTkLabel(
            top, text="", font=ctk.CTkFont(size=11),
            text_color="gray70"
        )
        self.week_label.pack(side="left")

        self._update_week_label()

        # Шапка таблицы
        header = ctk.CTkFrame(self, fg_color=("#e5e5e5", "#2b2b2b"),
                              corner_radius=8, height=36)
        header.pack(fill="x", padx=4, pady=(0, 4))
        header.pack_propagate(False)

        specs = [("Привычка", 22, "w"),
                 ("Серия", 8, "center"),
                 ("Всего", 6, "center")]
        for text, width, anchor in specs:
            ctk.CTkLabel(
                header, text=text,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=width * 8, anchor=anchor
            ).pack(side="left", padx=2, pady=6)

        for d in WEEKDAYS:
            ctk.CTkLabel(
                header, text=d,
                font=ctk.CTkFont(size=11, weight="bold"),
                width=36
            ).pack(side="left", padx=1)

    def _build_scroll_area(self):
        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self.scroll.pack(fill="both", expand=True)

    def _update_week_label(self):
        """Показывает диапазон дат текущей отображаемой недели."""
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        monday += datetime.timedelta(weeks=self.week_offset)
        sunday = monday + datetime.timedelta(days=6)
        self.week_label.configure(
            text=f"{monday.strftime('%d.%m')} — {sunday.strftime('%d.%m.%Y')}"
        )

    def _prev_week(self):
        self.week_offset -= 1
        self._update_week_label()
        self.event_generate("<<WeekChanged>>")

    def _next_week(self):
        self.week_offset += 1
        self._update_week_label()
        self.event_generate("<<WeekChanged>>")

    def render(self, habits, only_undone=False):
        for w in self.scroll.winfo_children():
            w.destroy()

        visible = [
            (i, h) for i, h in enumerate(habits)
            if not (only_undone and is_done_today(h))
        ]

        if not visible:
            ctk.CTkLabel(
                self.scroll, text="Нет привычек для отображения.",
                font=ctk.CTkFont(size=12, slant="italic"),
                text_color="gray60"
            ).pack(pady=30)
            return

        for index, habit in visible:
            self._render_row(index, habit)

    def _render_row(self, index, habit):
        done_today = is_done_today(habit)
        is_selected = (self.selected_index == index)

        if is_selected:
            row_fg = "#1f4e79"
        elif done_today:
            row_fg = "#1e3a2e"
        else:
            row_fg = "transparent"

        row = ctk.CTkFrame(self.scroll, fg_color=row_fg,
                           corner_radius=8, height=44)
        row.pack(fill="x", pady=2, padx=2)
        row.pack_propagate(False)

        name_lbl = ctk.CTkLabel(
            row, text=habit["name"],
            font=ctk.CTkFont(size=12),
            width=176, anchor="w"
        )
        name_lbl.pack(side="left", padx=(12, 4), pady=8)

        streak = count_streak(habit["history"])
        if streak >= 7:
            icon = "🏆 "
        elif streak >= 3:
            icon = "🔥 "
        else:
            icon = ""
        ctk.CTkLabel(
            row, text=f"{icon}{streak} дн.",
            font=ctk.CTkFont(size=12), text_color="#f9a03f", width=64
        ).pack(side="left", padx=2)

        ctk.CTkLabel(
            row, text=str(total_done(habit)),
            font=ctk.CTkFont(size=12), width=48
        ).pack(side="left", padx=2)

        # Календарь недели с учётом смещения
        week = week_status_for_offset(habit, self.week_offset)
        today = datetime.date.today()
        monday_this = today - datetime.timedelta(days=today.weekday())

        day_colors = {"done": "#4caf50", "missed": "#3a3a3a", "today": "#3b8ed0"}

        for i, done in enumerate(week):
            day_date = monday_this + datetime.timedelta(weeks=self.week_offset)
            day_date += datetime.timedelta(days=i)
            is_today = (day_date == today)

            if is_today:
                color = day_colors["done"] if done else day_colors["today"]
                symbol = "✓" if done else "•"
            else:
                color = day_colors["done"] if done else day_colors["missed"]
                symbol = "✓" if done else ""

            ctk.CTkLabel(
                row, text=symbol,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=color, corner_radius=6,
                width=28, height=28, text_color="white"
            ).pack(side="left", padx=2)

        # Клики
        def click(e, i=index):
            self._click(i)

        def double(e, i=index):
            self.on_double_click(i)

        def right(e, i=index):
            self.selected_index = i
            self.on_select(i)
            self.on_right_click(i, e)

        for w in (row, name_lbl):
            w.bind("<Button-1>", click)
            w.bind("<Double-1>", double)
            w.bind("<Button-3>", right)  # ПКМ

        # Hover
        def on_enter(e):
            if not is_selected and not done_today:
                row.configure(fg_color=("#e0e0e0", "#2f2f2f"))

        def on_leave(e):
            if not is_selected and not done_today:
                row.configure(fg_color="transparent")

        row.bind("<Enter>", on_enter)
        row.bind("<Leave>", on_leave)

    def _click(self, index):
        self.selected_index = index
        self.on_select(index)


def week_status_for_offset(habit, offset):
    """Возвращает список True/False для недели со смещением."""
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    monday += datetime.timedelta(weeks=offset)

    history = set(habit["history"])
    result = []
    for i in range(7):
        day = monday + datetime.timedelta(days=i)
        result.append(day.isoformat() in history)
    return result