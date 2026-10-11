"""
main.py — точка входа. Настраивает тему CustomTkinter и запускает приложение.
"""

import customtkinter as ctk
import os
import sys
import ctypes
from ui.app import HabitTrackerApp


def set_taskbar_icon():
    """
    Устанавливает иконку для панели задач Windows.
    Работает только на Windows.
    """
    if sys.platform != "win32":
        return

    try:
        # ВАЖНО: этот вызов должен быть ДО создания окна Tk()!
        myappid = "com.habittracker.myapp.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        print("AppUserModelID установлен")
    except Exception as e:
        print(f"Не удалось установить AppUserModelID: {e}")


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Сначала регистрируем ID приложения для панели задач
    set_taskbar_icon()

    root = ctk.CTk()

    # Ищем иконку
    base = os.path.dirname(__file__)
    icon_path = os.path.join(base, "assets", "icon.ico")

    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
            print(f"Иконка окна загружена: {icon_path}")
        except Exception as e:
            print(f"Не удалось загрузить иконку окна: {e}")
    else:
        print(f"Иконка не найдена: {icon_path}")

    app = HabitTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()