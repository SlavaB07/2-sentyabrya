"""
Вкладка «Сервер».
"""

import tkinter as tk
from tkinter import ttk
import webbrowser
import queue
import logging

from ..server.http_server import HttpServer


class ServerTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.server = None
        self.log_queue = queue.Queue()

        # Верхняя часть: порт и кнопки
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(top_frame, text="Порт:").pack(side="left")
        self.port_entry = ttk.Entry(top_frame, width=8)
        self.port_entry.pack(side="left", padx=5)
        self.port_entry.insert(0, "8080")

        self.start_btn = ttk.Button(
            top_frame,
            text="Запустить",
            command=self._on_start)
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = ttk.Button(
            top_frame,
            text="Остановить",
            command=self._on_stop,
            state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        self.status_indicator = tk.Canvas(top_frame, width=20, height=20)
        self.status_indicator.pack(side="left", padx=5)
        self.status_circle = self.status_indicator.create_oval(
            2, 2, 18, 18, fill="red")

        self.status_label = ttk.Label(top_frame, text="Остановлен")
        self.status_label.pack(side="left", padx=5)

        # Кнопки лога
        log_btn_frame = ttk.Frame(self)
        log_btn_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            log_btn_frame,
            text="Очистить лог",
            command=self._on_clear_log).pack(
            side="left")
        ttk.Button(
            log_btn_frame,
            text="Открыть в браузере",
            command=self._on_open_browser).pack(
            side="left",
            padx=5)

        # Лог
        ttk.Label(self, text="Лог запросов:").pack(anchor="w", padx=5)
        self.log_text = tk.Text(self, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Настраиваем логгер для сервера
        self._setup_logger()

        # Запускаем проверку очереди
        self._poll_queue()

    def _setup_logger(self):
        class QueueHandler(logging.Handler):
            def __init__(self, q):
                super().__init__()
                self.q = q

            def emit(self, record):
                self.q.put(self.format(record))

        handler = QueueHandler(self.log_queue)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(message)s",
                datefmt="%H:%M:%S"))
        logger = logging.getLogger("src.server.http_server")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def _on_start(self):
        try:
            port = int(self.port_entry.get())
        except ValueError:
            self._append_log("Ошибка: порт должен быть числом")
            return

        self.server = HttpServer(host="0.0.0.0", port=port)
        self.server.start()

        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_indicator.itemconfig(self.status_circle, fill="green")
        self.status_label.config(text=f"Запущен на порту {port}")
        self._append_log(f"Сервер запущен на http://localhost:{port}")

    def _on_stop(self):
        if self.server:
            self.server.stop()
            self.server = None

        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_indicator.itemconfig(self.status_circle, fill="red")
        self.status_label.config(text="Остановлен")
        self._append_log("Сервер остановлен")

    def _on_clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    def _on_open_browser(self):
        port = self.port_entry.get()
        webbrowser.open(f"http://localhost:{port}/")

    def _poll_queue(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self._append_log(msg)
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    def _append_log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
