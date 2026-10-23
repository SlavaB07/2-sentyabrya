"""
Кастомные исключения для нашего HTTP-проекта.

Зачем свои исключения?
1. Понятно, ЧТО именно пошло не так (сеть? парсинг? таймаут?).
2. Легко ловить в коде: try: ... except ParseError: ...
3. Не используем "магические" коды возврата вроде -1 или None.
"""


class HttpProjectError(Exception):
    """
    Базовое исключение для всего проекта.
    
    Все наши кастомные ошибки будут наследоваться от него.
    Это удобно: можно ловить все наши ошибки одной строкой:
        except HttpProjectError:
    """
    pass


class ParseError(HttpProjectError):
    """
    Ошибка парсинга.
    
    Бросаем, когда:
    - URL невалидный (нет схемы, пустой хост, кривой порт).
    - HTTP-запрос/ответ не соответствует формату.
    - Заголовок слишком длинный (> 8 КБ, защита от overflow).
    """
    pass


class ConnectionError(HttpProjectError):
    """
    Ошибка сетевого соединения.
    
    Бросаем, когда:
    - Не удалось подключиться к хосту (сервер недоступен).
    - Соединение разорвалось во время чтения.
    """
    pass


class TimeoutError(HttpProjectError):
    """
    Ошибка таймаута.
    
    Бросаем, когда:
    - Сервер не ответил за отведённое время.
    - Чтение данных заняло слишком долго.
    """
    pass


class HttpError(HttpProjectError):
    """
    HTTP-ошибка (сервер ответил статусом 4xx или 5xx).
    
    Атрибуты:
    - status: код ответа (например, 404, 500).
    - message: текстовое описание ошибки.
    
    Пример использования:
        try:
            client.get("http://example.com/missing")
        except HttpError as e:
            print(f"Сервер вернул {e.status}: {e.message}")
    """
    
    def __init__(self, status: int, message: str = ""):
        self.status = status
        self.message = message
        # Вызываем конструктор родителя с красивым текстом
        super().__init__(f"HTTP {status}: {message}")