"""
header.py — заголовок с датой, счётчик и прогресс-бар.
"""

import customtkinter as ctk
import datetime


class Header(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=(4, 2))

        ctk.CTkFrame(row, width=4, height=24,
                     fg_color="#3b8ed0", corner_radius=2
                     ).pack(side="left", padx=(0, 12))

        self.title_label = ctk.CTkLabel(
            row, text="", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(side="left")

        self.counter_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=11),
            text_color="gray70"
        )
        self.counter_label.pack(pady=(0, 4))

        # Прогресс-бар выполнения
        self.progress = ctk.CTkProgressBar(
            self, width=400, height=6,
            corner_radius=3,
            progress_color="#4caf50"
        )
        self.progress.pack(pady=(0, 8))
        self.progress.set(0)

        self.update_date()

    def update_date(self):
        today = datetime.date.today()
        weekdays = ["понедельник", "вторник", "среда", "четверг",
                    "пятница", "суббота", "воскресенье"]
        date_str = f"{today.strftime('%d.%m.%Y')}, {weekdays[today.weekday()]}"
        self.title_label.configure(text=f"Мои привычки · {date_str}")

    def set_counter(self, done, total):
        if total == 0:
            self.counter_label.configure(text="Пока нет привычек — добавь первую")
            self.progress.set(0)
        else:
            percent = int(done / total * 100)
            self.counter_label.configure(
                text=f"Сегодня выполнено: {done} из {total}  ·  {percent}%"
            )
            self.progress.set(done / total)