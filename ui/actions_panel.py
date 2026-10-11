"""
actions_panel.py — кнопки действий + экспорт и график.
"""

import customtkinter as ctk


class ActionsPanel(ctk.CTkFrame):
    def __init__(self, parent,
                 on_mark, on_unmark, on_delete, on_mark_all,
                 on_export, on_chart):
        super().__init__(parent, fg_color="transparent")

        buttons = [
            ("✅  Отметить",       "#2ea043", "#3fb950", on_mark),
            ("↩️  Снять",          "#d29922", "#e3b341", on_unmark),
            ("🗑  Удалить",        "#da3633", "#f85149", on_delete),
            ("✅✅  Отметить всё", "#1f883d", "#2ea043", on_mark_all),
            ("📤  Экспорт CSV",    "#4a4a4a", "#5a5a5a", on_export),
            ("📊  График",         "#7d5bbe", "#8b5cf6", on_chart),
        ]
        for text, color, hover, cmd in buttons:
            ctk.CTkButton(
                self, text=text, command=cmd,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color=color, hover_color=hover,
                corner_radius=8, height=36,
                text_color="white", width=125
            ).pack(side="left", padx=3)