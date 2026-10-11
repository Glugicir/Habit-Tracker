"""
edit_dialog.py — простое окно для изменения названия привычки.
"""

import customtkinter as ctk


class EditDialog(ctk.CTkToplevel):
    """Модальное окно для редактирования названия привычки."""

    def __init__(self, parent, current_name, on_save):
        super().__init__(parent)
        self.title("✏️ Редактировать привычку")
        self.geometry("420x180")
        self.resizable(False, False)

        self.on_save = on_save
        self.result = None

        # Модальное — блокирует родительское окно
        self.transient(parent)
        self.grab_set()

        ctk.CTkLabel(
            self, text="Новое название:",
            font=ctk.CTkFont(size=13)
        ).pack(pady=(18, 6), padx=20, anchor="w")

        self.entry = ctk.CTkEntry(
            self, font=ctk.CTkFont(size=13),
            height=36, corner_radius=8
        )
        self.entry.pack(fill="x", padx=20)
        self.entry.insert(0, current_name)
        self.entry.select_range(0, "end")
        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self._save())

        # Кнопки
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=18)

        ctk.CTkButton(
            btn_frame, text="Отмена",
            fg_color="#4a4a4a", hover_color="#5a5a5a",
            width=110, height=34, corner_radius=8,
            command=self.destroy
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btn_frame, text="Сохранить",
            fg_color="#3b8ed0", hover_color="#2e7ab8",
            width=110, height=34, corner_radius=8,
            command=self._save
        ).pack(side="left", padx=6)

    def _save(self):
        new_name = self.entry.get().strip()
        if not new_name:
            return
        self.on_save(new_name)
        self.destroy()