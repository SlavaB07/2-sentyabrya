"""
Router — маршрутизатор запросов.

Сопоставляет (метод, путь) с функцией-обработчиком.
"""

from typing import Callable, Dict, Tuple

from ..http.request import Request
from ..http.response import Response
from .handlers import (
    handle_echo_get,
    handle_echo_post,
    handle_time,
    handle_headers,
    handle_status,
    handle_not_found,
)


# Тип функции-обработчика
Handler = Callable[[Request], Response]


class Router:
    def __init__(self):
        # Словарь: (метод, путь) -> функция
        self._routes: Dict[Tuple[str, str], Handler] = {}
        
        # Регистрируем маршруты
        self.route("GET", "/echo", handle_echo_get)
        self.route("POST", "/echo", handle_echo_post)
        self.route("GET", "/time", handle_time)
        self.route("GET", "/headers", handle_headers)
        self.route("GET", "/status/{code}", handle_status)
    
    def route(self, method: str, path: str, handler: Handler) -> None:
        """Добавляет маршрут в таблицу."""
        key = (method.upper(), path)
        self._routes[key] = handler
    
    def dispatch(self, req: Request) -> Response:
        """
        Находит обработчик для запроса и вызывает его.
        
        Сначала ищет точное совпадение.
        Если не нашел — проверяет /status/{code}.
        Если и это не помогло — 404.
        """
        # 1. Точное совпадение
        key = (req.method.upper(), req.path)
        if key in self._routes:
            return self._routes[key](req)
        
        # 2. Специальный маршрут для /status/{code}
        if req.method.upper() == "GET" and req.path.startswith("/status/"):
            return handle_status(req)
        
        # 3. Если ничего не подошло — 404
        return handle_not_found(req)