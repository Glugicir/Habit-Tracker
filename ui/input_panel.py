"""
input_panel.py — панель добавления привычки и фильтр.
"""

import customtkinter as ctk


class InputPanel(ctk.CTkFrame):
    """Поле ввода + кнопка 'Добавить' + чекбокс фильтра."""

    def __init__(self, parent, on_add, only_undone_var):
        super().__init__(parent, fg_color="transparent")

        self.on_add = on_add
        self.only_undone_var = only_undone_var

        # Кнопка справа
        self.add_btn = ctk.CTkButton(
            self, text="➕  Добавить",
            command=self.on_add,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38, corner_radius=8,
            width=130
        )
        self.add_btn.pack(side="right")

        # Чекбокс справа
        self.checkbox = ctk.CTkCheckBox(
            self, text="Только невыполненные",
            variable=only_undone_var,
            font=ctk.CTkFont(size=12),
            command=lambda: self.event_generate("<<FilterChanged>>")
        )
        self.checkbox.pack(side="right", padx=(0, 14))

        # Поле ввода
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Название новой привычки...",
            font=ctk.CTkFont(size=13),
            height=38, corner_radius=8
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.entry.bind("<Return>", lambda e: self.on_add())

    def get_text(self):
        return self.entry.get()

    def clear(self):
        self.entry.delete(0, "end")