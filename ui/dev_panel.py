"""
dev_panel.py — панель DEV-инструментов.
"""

import customtkinter as ctk


class DevPanel(ctk.CTkFrame):
    """DEV-панель: ±1 день, произвольная дата, очистка."""

    def __init__(self, parent, on_minus, on_plus, on_date, on_clear):
        super().__init__(parent, corner_radius=10,
                         fg_color=("#e8e8e8", "#1a1a1a"))

        ctk.CTkLabel(
            self, text="🧪  DEV:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="gray60"
        ).pack(side="left", padx=(14, 8), pady=8)

        buttons = [
            ("−1 день",            "#7d5bbe", "#8b5cf6", on_minus),
            ("+1 день",            "#7d5bbe", "#8b5cf6", on_plus),
            ("Произвольная дата",  "#7d5bbe", "#8b5cf6", on_date),
            ("Очистить историю",   "#4a4a4a", "#5a5a5a", on_clear),
        ]
        for text, color, hover, cmd in buttons:
            ctk.CTkButton(
                self, text=text, command=cmd,
                font=ctk.CTkFont(size=11),
                fg_color=color, hover_color=hover,
                corner_radius=6, height=30,
                width=130
            ).pack(side="left", padx=3, pady=6)