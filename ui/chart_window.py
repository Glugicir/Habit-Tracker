"""
chart_window.py — окно с графиком активности за месяц (matplotlib).
"""

import customtkinter as ctk
import datetime

from core.stats import total_done_in_month

import matplotlib
matplotlib.use("TkAgg")  # важно для работы с tkinter

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ChartWindow(ctk.CTkToplevel):
    """Отдельное окно с графиком активности за текущий месяц."""

    def __init__(self, parent, habits):
        super().__init__(parent)
        self.title("📊 Активность за месяц")
        self.geometry("900x560")
        self.habits = habits

        self._build_ui()

    def _build_ui(self):
        today = datetime.date.today()
        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        title = f"Активность за {month_names[today.month - 1]} {today.year}"

        ctk.CTkLabel(
            self, text=title,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(14, 8))

        # Данные
        counts = total_done_in_month(self.habits)

        # Фигура matplotlib
        fig = Figure(figsize=(9, 4.5), dpi=100, facecolor="#1a1a1a")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#1a1a1a")

        days = list(range(1, len(counts) + 1))
        bars = ax.bar(days, counts, color="#3b8ed0", width=0.7)

        # Подсветка сегодняшнего дня
        if today.day <= len(counts):
            bars[today.day - 1].set_color("#4caf50")

        # Оформление
        ax.set_xlabel("День месяца", color="#cccccc", fontsize=11)
        ax.set_ylabel("Выполнено привычек", color="#cccccc", fontsize=11)
        ax.set_title("", color="#cccccc")
        ax.tick_params(colors="#aaaaaa")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color("#444444")
        ax.spines["left"].set_color("#444444")
        ax.grid(axis="y", color="#333333", linestyle="--", alpha=0.5)

        # Встраиваем в окно
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=14, pady=10)

        # Легенда
        legend = ctk.CTkLabel(
            self, text="🟩 сегодня    🟦 другие дни",
            font=ctk.CTkFont(size=11), text_color="gray60"
        )
        legend.pack(pady=(0, 12))