"""
Главное окно приложения с вкладками.
"""

import tkinter as tk
from tkinter import ttk

from .client_tab import ClientTab
from .server_tab import ServerTab


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HTTP Client & Server (Python)")
        self.geometry("900x700")

        # Создаём вкладки
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)

        self.client_tab = ClientTab(notebook)
        self.server_tab = ServerTab(notebook)

        notebook.add(self.client_tab, text="Клиент")
        notebook.add(self.server_tab, text="Сервер")


def run_app():
    app = App()
    app.mainloop()
