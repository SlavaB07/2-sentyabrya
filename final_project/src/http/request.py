"""
Класс Request — представляет HTTP-запрос.

Используется и клиентом (когда он формирует запрос),
и сервером (когда он получает запрос от браузера).

Пример:
    >>> req = Request(
    ...     method="GET",
    ...     path="/api/users",
    ...     headers={"Host": "example.com"},
    ... )
    >>> req.method
    'GET'
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Request:
    """
    HTTP-запрос.
    
    Атрибуты:
    - method: HTTP-метод (GET, POST, ...). Приводится к ВЕРХНЕМУ регистру.
    - path: путь запроса (например, "/echo"). Всегда начинается с "/".
    - version: версия HTTP. По умолчанию "HTTP/1.1".
    - headers: словарь заголовков. Ключи — с заглавной буквы (нормализуются).
    - body: тело запроса в байтах (по умолчанию пустое).
    """
    
    method: str
    path: str
    version: str = "HTTP/1.1"
    headers: Dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    
    def __post_init__(self):
        """
        Вызывается АВТОМАТИЧЕСКИ после __init__.
        
        Нужен, чтобы:
        1. Привести метод к верхнему регистру (get -> GET).
        2. Убедиться, что path начинается с "/".
        3. Нормализовать заголовки (привести ключи к каноническому виду).
        """
        # --- 1. Метод — всегда верхний регистр ---
        if not isinstance(self.method, str) or not self.method:
            raise ValueError("Метод должен быть непустой строкой")
        self.method = self.method.upper()
        
        # --- 2. Путь — всегда начинается с "/" ---
        if not isinstance(self.path, str) or not self.path:
            raise ValueError("Путь должен быть непустой строкой")
        if not self.path.startswith("/"):
            self.path = "/" + self.path
        
        # --- 3. Версия HTTP ---
        if not self.version.startswith("HTTP/"):
            raise ValueError(
                f"Версия должна начинаться с 'HTTP/', получено: {self.version}"
            )
        
        # --- 4. Заголовки: нормализуем ключи ---
        # "content-type" -> "Content-Type"
        # "HOST" -> "Host"
        normalized = {}
        for key, value in self.headers.items():
            # Приводим к виду "Первая-Буква-Заглавная"
            canonical_key = "-".join(
                part.capitalize() for part in key.split("-")
            )
            normalized[canonical_key] = str(value).strip()
        self.headers = normalized
        
        # --- 5. Тело — всегда байты ---
        if isinstance(self.body, str):
            self.body = self.body.encode("utf-8")
    
    def get_header(self, name: str) -> str:
        """
        Возвращает значение заголовка по имени (регистронезависимо).
        
        Пример:
            >>> req.get_header("content-type")
            'application/json'
        """
        canonical = "-".join(
            part.capitalize() for part in name.split("-")
        )
        return self.headers.get(canonical, "")
    
    def set_header(self, name: str, value: str) -> None:
        """Устанавливает заголовок (регистронезависимо)."""
        canonical = "-".join(
            part.capitalize() for part in name.split("-")
        )
        self.headers[canonical] = str(value).strip()