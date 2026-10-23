"""
Вкладка «Клиент».
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue

from ..client.http_client import HttpClient
from ..http.exceptions import HttpError, ConnectionError, TimeoutError


class ClientTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.client = HttpClient(timeout=10.0)
        self.result_queue = queue.Queue()
        
        # Верхняя часть: URL и метод
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(top_frame, text="URL:").pack(side="left")
        self.url_entry = ttk.Entry(top_frame, width=60)
        self.url_entry.pack(side="left", padx=5)
        self.url_entry.insert(0, "http://httpbin.org/get")
        
        self.method_var = tk.StringVar(value="GET")
        method_combo = ttk.Combobox(
            top_frame, textvariable=self.method_var,
            values=["GET", "POST"], state="readonly", width=8
        )
        method_combo.pack(side="left", padx=5)
        
        # Заголовки
        ttk.Label(self, text="Заголовки:").pack(anchor="w", padx=5)
        self.headers_text = tk.Text(self, height=4)
        self.headers_text.pack(fill="x", padx=5, pady=2)
        self.headers_text.insert("1.0", "User-Agent: MyClient/1.0\nAccept: */*")
        
        # Тело
        ttk.Label(self, text="Тело (для POST):").pack(anchor="w", padx=5)
        self.body_text = tk.Text(self, height=4)
        self.body_text.pack(fill="x", padx=5, pady=2)
        
        # Кнопки
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", padx=5, pady=5)
        
        self.send_btn = ttk.Button(btn_frame, text="Отправить", command=self._on_send)
        self.send_btn.pack(side="left")
        
        ttk.Button(btn_frame, text="Очистить", command=self._on_clear).pack(side="left", padx=5)
        
        self.status_label = ttk.Label(btn_frame, text="Готов", foreground="gray")
        self.status_label.pack(side="left", padx=20)
        
        # Ответ
        ttk.Label(self, text="Ответ:").pack(anchor="w", padx=5)
        self.response_text = tk.Text(self, state="disabled")
        self.response_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Запускаем проверку очереди
        self._poll_queue()
    
    def _on_send(self):
        url = self.url_entry.get().strip()
        method = self.method_var.get()
        body = self.body_text.get("1.0", "end-1c")
        
        # Парсим заголовки
        headers = {}
        for line in self.headers_text.get("1.0", "end-1c").split("\n"):
            if ":" in line:
                name, value = line.split(":", 1)
                headers[name.strip()] = value.strip()
        
        self.send_btn.config(state="disabled")
        self.status_label.config(text="Отправка...", foreground="blue")
        
        # Запускаем в отдельном потоке
        thread = threading.Thread(
            target=self._do_request,
            args=(method, url, headers, body.encode("utf-8")),
            daemon=True,
        )
        thread.start()
    
    def _do_request(self, method, url, headers, body):
        try:
            if method == "GET":
                resp = self.client.get(url, headers=headers)
            else:
                content_type = headers.pop("Content-Type", "text/plain")
                resp = self.client.post(url, body=body, content_type=content_type, headers=headers)
            
            # Кладём результат в очередь
            self.result_queue.put(("ok", resp))
        except Exception as e:
            self.result_queue.put(("error", e))
    
    def _poll_queue(self):
        try:
            while True:
                status, data = self.result_queue.get_nowait()
                if status == "ok":
                    self._show_response(data)
                else:
                    self._show_error(data)
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)
    
    def _show_response(self, resp):
        self.send_btn.config(state="normal")
        self.status_label.config(text=f"Готово: {resp.status}", foreground="green")
        
        self.response_text.config(state="normal")
        self.response_text.delete("1.0", "end")
        
        # Заголовки
        self.response_text.insert("end", f"СТАТУС: {resp.status} {resp.reason}\n\n")
        self.response_text.insert("end", "ЗАГОЛОВКИ:\n")
        for name, value in resp.headers.items():
            self.response_text.insert("end", f"  {name}: {value}\n")
        
        # Тело
        self.response_text.insert("end", "\nТЕЛО:\n")
        try:
            body_str = resp.body.decode("utf-8")
        except UnicodeDecodeError:
            body_str = repr(resp.body)
        self.response_text.insert("end", body_str)
        
        self.response_text.config(state="disabled")
    
    def _show_error(self, error):
        self.send_btn.config(state="normal")
        self.status_label.config(text=f"Ошибка: {type(error).__name__}", foreground="red")
        
        self.response_text.config(state="normal")
        self.response_text.delete("1.0", "end")
        self.response_text.insert("end", f"ОШИБКА:\n{type(error).__name__}: {error}")
        self.response_text.config(state="disabled")
    
    def _on_clear(self):
        self.response_text.config(state="normal")
        self.response_text.delete("1.0", "end")
        self.response_text.config(state="disabled")
        self.body_text.delete("1.0", "end")
        self.status_label.config(text="Готов", foreground="gray")