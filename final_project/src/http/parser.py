"""
Класс Parser — превращает сырые байты HTTP в объекты Request/Response.

Пример:
    >>> data = b"GET /echo HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n"
    >>> req = Parser.parse_request(data)
    >>> req.method
    'GET'
    >>> req.path
    '/echo'
"""

import re
from typing import Dict, Optional, Tuple

from .request import Request
from .response import Response, STATUS_REASONS
from .exceptions import ParseError


# Максимальный размер заголовка (защита от overflow, см. тест U10)
MAX_HEADER_SIZE = 8 * 1024  # 8 КБ

# Максимальный размер тела (защита от DoS)
MAX_BODY_SIZE = 10 * 1024 * 1024  # 10 МБ


class Parser:
    """
    Парсер HTTP-запросов и ответов.
    
    Все методы — статические (classmethod), потому что парсеру 
    не нужно хранить состояние между вызовами.
    """
    
    # Регулярка для request line: "GET /path HTTP/1.1"
    # Группы: (метод) (путь) (версия)
    REQUEST_LINE_RE = re.compile(
        r"^([A-Z]+)\s+(\S+)\s+(HTTP/\d\.\d)$"
    )
    
    # Регулярка для status line: "HTTP/1.1 200 OK"
    # Группы: (версия) (код) (причина — может быть пустой)
    STATUS_LINE_RE = re.compile(
        r"^(HTTP/\d\.\d)\s+(\d{3})(?:\s+(.*))?$"
    )
    
    # Регулярка для строки заголовка: "Content-Type: text/plain"
    # Группы: (имя) (значение)
    HEADER_LINE_RE = re.compile(
        r"^([!#$%&'*+\-.^_`|~0-9A-Za-z]+):\s*(.*)$"
    )
    
    @classmethod
    def parse_request(cls, data: bytes) -> Request:
        """
        Разбирает байты HTTP-запроса в объект Request.
        
        Параметры:
        - data: сырые байты запроса.
        
        Исключения:
        - ParseError: если запрос некорректный.
        """
        # --- 1. Разделяем на заголовки и тело ---
        head_bytes, body_bytes = cls._split_head_body(data)
        
        # --- 2. Декодируем заголовки в текст ---
        # HTTP-заголовки всегда в ASCII/Latin-1 (по стандарту)
        try:
            head_text = head_bytes.decode("latin-1")
        except UnicodeDecodeError as e:
            raise ParseError(f"Не удалось декодировать заголовки: {e}")
        
        # --- 3. Разбиваем на строки ---
        # \r\n — стандартный разделитель строк в HTTP
        lines = head_text.split("\r\n")
        
        if not lines or not lines[0]:
            raise ParseError("Пустой запрос: нет request line")
        
        # --- 4. Парсим request line ---
        request_line = lines[0]
        method, path, version = cls._parse_request_line(request_line)
        
        # --- 5. Парсим заголовки ---
        headers = cls._parse_headers(lines[1:])
        
        # --- 6. Проверяем обязательный Host (для HTTP/1.1) ---
        if version == "HTTP/1.1" and "Host" not in headers:
            raise ParseError("HTTP/1.1 требует заголовок Host")
        
        # --- 7. Читаем тело по Content-Length ---
        body = cls._read_body(headers, body_bytes)
        
        return Request(
            method=method,
            path=path,
            version=version,
            headers=headers,
            body=body,
        )
    
    @classmethod
    def parse_response(cls, data: bytes) -> Response:
        """
        Разбирает байты HTTP-ответа в объект Response.
        """
        # --- 1. Разделяем на заголовки и тело ---
        head_bytes, body_bytes = cls._split_head_body(data)
        
        # --- 2. Декодируем ---
        try:
            head_text = head_bytes.decode("latin-1")
        except UnicodeDecodeError as e:
            raise ParseError(f"Не удалось декодировать заголовки: {e}")
        
        lines = head_text.split("\r\n")
        
        if not lines or not lines[0]:
            raise ParseError("Пустой ответ: нет status line")
        
        # --- 3. Парсим status line ---
        version, status, reason = cls._parse_status_line(lines[0])
        
        # --- 4. Парсим заголовки ---
        headers = cls._parse_headers(lines[1:])
        
        # --- 5. Читаем тело ---
        body = cls._read_body(headers, body_bytes)
        
        return Response(
            status=status,
            reason=reason,
            version=version,
            headers=headers,
            body=body,
        )
    
    # =========================================================
    # ВНУТРЕННИЕ МЕТОДЫ (начинаются с _)
    # =========================================================
    
    @classmethod
    def _split_head_body(cls, data: bytes) -> Tuple[bytes, bytes]:
        """
        Разделяет сырые байты на (заголовки, тело) по разделителю \r\n\r\n.
        
        Пример:
            b"GET / HTTP/1.1\r\nHost: x\r\n\r\nhello"
            -> (b"GET / HTTP/1.1\r\nHost: x", b"hello")
        """
        if not isinstance(data, bytes):
            raise ParseError(f"Ожидались байты, получено: {type(data)}")
        
        if not data:
            raise ParseError("Пустые данные")
        
        # Ищем разделитель \r\n\r\n
        separator = b"\r\n\r\n"
        idx = data.find(separator)
        
        if idx == -1:
            # Нет разделителя — значит, нет тела, только заголовки
            # Но проверяем, что заголовки не гигантские
            if len(data) > MAX_HEADER_SIZE:
                raise ParseError(
                    f"Заголовки слишком большие: {len(data)} > {MAX_HEADER_SIZE}"
                )
            return data, b""
        
        head = data[:idx]
        body = data[idx + len(separator):]
        
        # Защита от overflow
        if len(head) > MAX_HEADER_SIZE:
            raise ParseError(
                f"Заголовки слишком большие: {len(head)} > {MAX_HEADER_SIZE}"
            )
        
        return head, body
    
    @classmethod
    def _parse_request_line(cls, line: str) -> Tuple[str, str, str]:
        """
        Парсит request line: "GET /echo HTTP/1.1"
        
        Возвращает: (метод, путь, версия)
        """
        match = cls.REQUEST_LINE_RE.match(line)
        if not match:
            raise ParseError(f"Некорректная request line: {line!r}")
        
        method, path, version = match.groups()
        return method.upper(), path, version
    
    @classmethod
    def _parse_status_line(cls, line: str) -> Tuple[str, int, str]:
        """
        Парсит status line: "HTTP/1.1 200 OK"
        
        Возвращает: (версия, статус, причина)
        """
        match = cls.STATUS_LINE_RE.match(line)
        if not match:
            raise ParseError(f"Некорректная status line: {line!r}")
        
        version, status_str, reason = match.groups()
        status = int(status_str)
        reason = reason or STATUS_REASONS.get(status, "")
        
        return version, status, reason
    
    @classmethod
    def _parse_headers(cls, lines: list) -> Dict[str, str]:
        """
        Парсит строки заголовков в словарь.
        
        Пример:
            ["Host: localhost", "Content-Type: text/plain"]
            -> {"Host": "localhost", "Content-Type": "text/plain"}
        """
        headers = {}
        for line in lines:
            if not line:  # пустая строка — конец заголовков
                continue
            
            match = cls.HEADER_LINE_RE.match(line)
            if not match:
                raise ParseError(f"Некорректный заголовок: {line!r}")
            
            name, value = match.groups()
            
            # Нормализуем имя: "content-type" -> "Content-Type"
            canonical = "-".join(
                part.capitalize() for part in name.split("-")
            )
            
            # Если заголовок уже был — склеиваем через запятую
            # (стандарт HTTP: повторяющиеся заголовки объединяются)
            if canonical in headers:
                headers[canonical] += ", " + value.strip()
            else:
                headers[canonical] = value.strip()
        
        return headers
    
    @classmethod
    def _read_body(cls, headers: Dict[str, str], body_bytes: bytes) -> bytes:
        """
        Читает тело по Content-Length.
        
        Если Content-Length нет — тело считается пустым 
        (у GET-запросов и ответов 204/304 тела нет).
        """
        content_length_str = headers.get("Content-Length", "")
        
        if not content_length_str:
            # Нет Content-Length — тело пустое (или chunked, но это бонус)
            return b""
        
        try:
            content_length = int(content_length_str)
        except ValueError:
            raise ParseError(
                f"Content-Length должен быть числом: {content_length_str!r}"
            )
        
        if content_length < 0:
            raise ParseError(f"Content-Length не может быть отрицательным: {content_length}")
        
        if content_length > MAX_BODY_SIZE:
            raise ParseError(
                f"Тело слишком большое: {content_length} > {MAX_BODY_SIZE}"
            )
        
        # Если тело не помещается в переданные байты — ошибка
        if len(body_bytes) < content_length:
            raise ParseError(
                f"Тело короче Content-Length: "
                f"получено {len(body_bytes)}, ожидалось {content_length}"
            )
        
        return body_bytes[:content_length]