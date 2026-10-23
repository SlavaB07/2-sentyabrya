"""
Класс Serializer — превращает объекты Request/Response в байты.

Пример:
    >>> req = Request(method="GET", path="/echo", headers={"Host": "localhost"})
    >>> data = Serializer.serialize_request(req)
    >>> data
    b'GET /echo HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n'
"""

from .request import Request
from .response import Response


# Стандартный User-Agent для нашего клиента
DEFAULT_USER_AGENT = "MyHttpClient/1.0 (Python; Educational)"


class Serializer:
    """
    Сериализатор HTTP-объектов в байты.
    
    Все методы — статические (classmethod).
    """
    
    @classmethod
    def serialize_request(cls, req: Request) -> bytes:
        """
        Превращает Request в байты для отправки.
        
        Структура:
        <МЕТОД> <ПУТЬ> <ВЕРСИЯ>\r\n
        <Заголовок 1>: <значение>\r\n
        ...
        \r\n
        <тело>
        """
        # --- 1. Автоматически добавляем обязательные заголовки ---
        headers = dict(req.headers)  # копия, чтобы не менять оригинал
        
        # Host обязателен для HTTP/1.1
        if "Host" not in headers:
            # Пытаемся взять из URL, но у нас его нет — ставим заглушку
            # В реальном клиенте Host передаётся из HttpClient
            headers["Host"] = "localhost"
        
        # User-Agent — хороший тон
        if "User-Agent" not in headers:
            headers["User-Agent"] = DEFAULT_USER_AGENT
        
        # Content-Length — если есть тело
        if req.body:
            headers["Content-Length"] = str(len(req.body))
        
        # --- 2. Формируем request line ---
        request_line = f"{req.method} {req.path} {req.version}"
        
        # --- 3. Формируем строки заголовков ---
        header_lines = [f"{name}: {value}" for name, value in headers.items()]
        
        # --- 4. Собираем всё в байты ---
        # Заголовки + пустая строка + тело
        head = "\r\n".join([request_line] + header_lines)
        data = head.encode("latin-1") + b"\r\n\r\n" + req.body
        
        return data
    
    @classmethod
    def serialize_response(cls, resp: Response) -> bytes:
        """
        Превращает Response в байты для отправки.
        
        Структура:
        <ВЕРСИЯ> <СТАТУС> <ПРИЧИНА>\r\n
        <Заголовок 1>: <значение>\r\n
        ...
        \r\n
        <тело>
        """
        # --- 1. Автоматические заголовки ---
        headers = dict(resp.headers)
        
        # Content-Length — обязателен, даже если тело пустое
        headers["Content-Length"] = str(len(resp.body))
        
        # Content-Type — если не задан, ставим text/plain
        if "Content-Type" not in headers and resp.body:
            headers["Content-Type"] = "text/plain; charset=utf-8"
        
        # --- 2. Status line ---
        status_line = f"{resp.version} {resp.status} {resp.reason}".rstrip()
        
        # --- 3. Заголовки ---
        header_lines = [f"{name}: {value}" for name, value in headers.items()]
        
        # --- 4. Сборка ---
        head = "\r\n".join([status_line] + header_lines)
        data = head.encode("latin-1") + b"\r\n\r\n" + resp.body
        
        return data