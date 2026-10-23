"""
Класс Response — представляет HTTP-ответ.

Пример:
    >>> resp = Response(
    ...     status=200,
    ...     reason="OK",
    ...     body=b"Hello",
    ... )
    >>> resp.status
    200
"""

from dataclasses import dataclass, field
from typing import Dict


# Справочник: код -> стандартная причина.
# Стандарт RFC 7231. Полезно, чтобы не писать "OK" вручную каждый раз.
STATUS_REASONS: Dict[int, str] = {
    200: "OK",
    201: "Created",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    304: "Not Modified",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    418: "I'm a teapot",  # да, это официальный код :)
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
}


@dataclass
class Response:
    """
    HTTP-ответ.
    
    Атрибуты:
    - status: код ответа (200, 404, ...).
    - reason: текстовая причина ("OK", "Not Found"). 
              Если пусто — возьмётся из STATUS_REASONS.
    - version: версия HTTP. По умолчанию "HTTP/1.1".
    - headers: словарь заголовков.
    - body: тело в байтах.
    """
    
    status: int
    reason: str = ""
    version: str = "HTTP/1.1"
    headers: Dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    
    def __post_init__(self):
        """Валидация и нормализация после создания объекта."""
        # --- 1. Статус должен быть числом в диапазоне 100-599 ---
        if not isinstance(self.status, int):
            raise ValueError(f"status должен быть int, получено: {type(self.status)}")
        if not (100 <= self.status <= 599):
            raise ValueError(f"status должен быть в диапазоне 100-599, получено: {self.status}")
        
        # --- 2. Если reason не задан — берём из справочника ---
        if not self.reason:
            self.reason = STATUS_REASONS.get(self.status, "")
        
        # --- 3. Версия HTTP ---
        if not self.version.startswith("HTTP/"):
            raise ValueError(
                f"Версия должна начинаться с 'HTTP/', получено: {self.version}"
            )
        
        # --- 4. Нормализация заголовков (как в Request) ---
        normalized = {}
        for key, value in self.headers.items():
            canonical_key = "-".join(
                part.capitalize() for part in key.split("-")
            )
            normalized[canonical_key] = str(value).strip()
        self.headers = normalized
        
        # --- 5. Тело — всегда байты ---
        if isinstance(self.body, str):
            self.body = self.body.encode("utf-8")
    
    def get_header(self, name: str) -> str:
        """Возвращает значение заголовка (регистронезависимо)."""
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
    
    def is_success(self) -> bool:
        """True, если статус 2xx (успех)."""
        return 200 <= self.status < 300
    
    def is_redirect(self) -> bool:
        """True, если статус 3xx (редирект)."""
        return 300 <= self.status < 400
    
    def is_error(self) -> bool:
        """True, если статус 4xx или 5xx (ошибка)."""
        return 400 <= self.status < 600
    
    @classmethod
    def from_status(cls, status: int, body: bytes = b"") -> "Response":
        """
        Удобный фабричный метод: создать ответ только по статусу.
        
        Пример:
            >>> Response.from_status(404, b"Not Found")
            Response(status=404, reason='Not Found', ...)
        """
        return cls(
            status=status,
            reason=STATUS_REASONS.get(status, ""),
            body=body,
            headers={"Content-Type": "text/plain; charset=utf-8"},
        )