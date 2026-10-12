import customtkinter as ctk


class InputPanel(ctk.CTkFrame):
    """Поле ввода + поиск + сортировка + фильтр + кнопка 'Добавить'."""

    def _init_(self, parent, on_add, on_search, on_sort,
                 only_undone_var):
        super()._init_(parent, fg_color="transparent")

        self.on_add = on_add
        self.on_search = on_search
        self.on_sort = on_sort
        self.only_undone_var = only_undone_var

        # ============ ВЕРХНЯЯ СТРОКА: добавление ============
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", pady=(0, 8))

        self.add_btn = ctk.CTkButton(
            top, text="➕  Добавить",
            command=self.on_add,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38, corner_radius=8,
            width=130
        )
        self.add_btn.pack(side="right")

        self.entry = ctk.CTkEntry(
            top,
            placeholder_text="Название новой привычки...",
            font=ctk.CTkFont(size=13),
            height=38, corner_radius=8
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.entry.bind("<Return>", lambda e: self.on_add())

        # ============ НИЖНЯЯ СТРОКА: поиск и сортировка ============
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(fill="x")

        # Поиск
        self.search_entry = ctk.CTkEntry(
            bottom,
            placeholder_text="🔍 Поиск по названию...",
            font=ctk.CTkFont(size=12),
            height=32, corner_radius=8
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.search_entry.bind("<KeyRelease>", lambda e: self._on_search_change())

        # Кнопка сброса поиска
        self.clear_search_btn = ctk.CTkButton(
            bottom, text="✕",
            command=self._clear_search,
            font=ctk.CTkFont(size=12, weight="bold"),
            width=32, height=32, corner_radius=8,
            fg_color="#4a4a4a", hover_color="#5a5a5a"
        )
        self.clear_search_btn.pack(side="left", padx=(0, 12))

        # Сортировка
        ctk.CTkLabel(
            bottom, text="Сортировка:",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        ).pack(side="left", padx=(0, 6))

        self.sort_menu = ctk.CTkOptionMenu(
            bottom,
            values=["По названию", "По дате", "По серии", "По количеству"],
            command=self._on_sort_change,
            font=ctk.CTkFont(size=12),
            width=150, height=32, corner_radius=8
        )
        self.sort_menu.set("По названию")
        self.sort_menu.pack(side="left", padx=(0, 12))

        # Фильтр
        self.checkbox = ctk.CTkCheckBox(
            bottom, text="Только невыполненные",
            variable=only_undone_var,
            font=ctk.CTkFont(size=12),
            command=lambda: self.event_generate("<<FilterChanged>>")
        )
        self.checkbox.pack(side="left")

    # ==================== ОБРАБОТЧИКИ ====================

    def _on_search_change(self):
        """Вызывается при каждом нажатии клавиши в поле поиска."""
        self.event_generate("<<SearchChanged>>")

    def _on_sort_change(self, value):
        """Вызывается при выборе пункта в выпадающем списке."""
        self.event_generate("<<SortChanged>>")

    def _clear_search(self):
        """Очищает поле поиска."""
        self.search_entry.delete(0, "end")
        self.event_generate("<<SearchChanged>>")

    # ==================== ГЕТТЕРЫ ====================

    def get_text(self):
        return self.entry.get()

    def get_search_query(self):
        return self.search_entry.get()

    def get_sort_type(self):
        """Преобразует русский вариант в ключ сортировки."""
        mapping = {
            "По названию": "name",
            "По дате": "created",
            "По серии": "streak",
            "По количеству": "total",
        }
        return mapping.get(self.sort_menu.get(), "name")

    def clear(self):
        self.entry.delete(0, "end")