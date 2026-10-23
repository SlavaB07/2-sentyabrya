"""
Класс Url — разбирает строку URL на составные части.

Пример:
    >>> u = Url("http://example.com:8080/api/test?q=hello")
    >>> u.scheme
    'http'
    >>> u.host
    'example.com'
    >>> u.port
    8080
    >>> u.path
    '/api/test'
    >>> u.query
    'q=hello'
"""

from typing import Optional
from .exceptions import ParseError


class Url:
    """
    Разбирает URL на части и хранит их как атрибуты.
    
    Атрибуты после создания:
    - scheme: 'http' или 'https'
    - host: домен или IP (например, 'example.com' или '127.0.0.1')
    - port: порт (80 для http, 443 для https по умолчанию)
    - path: путь (всегда начинается с '/', по умолчанию '/')
    - query: строка параметров после '?' (или None, если нет)
    """
    
    # Дефолтные порты для схем
    DEFAULT_PORTS = {
        "http": 80,
        "https": 443,
    }
    
    def __init__(self, url: str):
        """
        Создаёт объект Url и сразу его парсит.
        
        Параметры:
        - url: строка URL, например "http://example.com/path"
        
        Исключения:
        - ParseError: если URL некорректный.
        """
        # Сохраняем оригинальную строку (на всякий случай)
        self.raw_url = url
        
        # Значения по умолчанию
        self.scheme: str = "http"
        self.host: str = ""
        self.port: int = 80
        self.path: str = "/"
        self.query: Optional[str] = None
        
        # Сразу парсим
        self._parse()
    
    def _parse(self) -> None:
        """
        Внутренний метод: разбирает URL на части.
        
        Используем подчёркивание в начале имени (_parse),
        чтобы показать: это внутренний метод, не для внешнего вызова.
        """
        # --- 1. Проверяем, что URL не пустой ---
        if not self.raw_url or not isinstance(self.raw_url, str):
            raise ParseError("URL не может быть пустым")
        
        url = self.raw_url.strip()  # убираем пробелы по краям
        
        # --- 2. Отделяем схему от остального ---
        # Ищем "://" в строке
        if "://" not in url:
            raise ParseError(
                f"URL должен содержать схему (http:// или https://): {url}"
            )
        
        # split("://", 1) разбивает строку на максимум 2 части
        # "http://example.com" -> ["http", "example.com"]
        scheme, rest = url.split("://", 1)
        self.scheme = scheme.lower()
        
        if self.scheme not in self.DEFAULT_PORTS:
            raise ParseError(
                f"Неподдерживаемая схема '{self.scheme}'. "
                f"Разрешены: {list(self.DEFAULT_PORTS.keys())}"
            )
        
        # --- 3. Отделяем host:port от path ---
        # Пример: "example.com:8080/api/test" -> host_part="example.com:8080", path="/api/test"
        if "/" in rest:
            host_part, path_part = rest.split("/", 1)
            self.path = "/" + path_part  # возвращаем "/" в начало
        else:
            host_part = rest
            self.path = "/"
        
        # --- 4. Отделяем query от path ---
        # Пример: "/api/test?q=hello" -> path="/api/test", query="q=hello"
        if "?" in self.path:
            self.path, self.query = self.path.split("?", 1)
        
        # --- 5. Разбираем host:port ---
        # Пример: "example.com:8080" -> host="example.com", port=8080
        if ":" in host_part:
            host, port_str = host_part.rsplit(":", 1)
            if not port_str.isdigit():
                raise ParseError(f"Порт должен быть числом: {port_str}")
            self.port = int(port_str)
            self.host = host
        else:
            # Порт не указан — берём дефолтный по схеме
            self.host = host_part
            self.port = self.DEFAULT_PORTS[self.scheme]
        
        # --- 6. Проверяем, что host не пустой ---
        if not self.host:
            raise ParseError(f"Пустой хост в URL: {self.raw_url}")
        
        # --- 7. Проверяем, что порт в допустимом диапазоне ---
        if not (1 <= self.port <= 65535):
            raise ParseError(
                f"Порт должен быть в диапазоне 1-65535, получено: {self.port}"
            )
    
    def __str__(self) -> str:
        """Строковое представление (для отладки)."""
        return self.raw_url
    
    def __repr__(self) -> str:
        """Техническое представление (для print в консоли)."""
        return (
            f"Url(scheme={self.scheme!r}, host={self.host!r}, "
            f"port={self.port}, path={self.path!r}, query={self.query!r})"
        )