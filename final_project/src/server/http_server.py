"""
HttpServer — многопоточный HTTP-сервер на голых сокетах.
"""

import socket
import threading
import logging
from typing import Optional

from ..http.parser import Parser
from ..http.serializer import Serializer
from ..http.exceptions import ParseError
from .router import Router


logger = logging.getLogger(__name__)


class HttpServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self.host = host
        self.port = port
        self.router = Router()
        
        self._sock: Optional[socket.socket] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False
    
    def start(self) -> None:
        """Запускает сервер в отдельном потоке."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info(f"Сервер запущен на http://{self.host}:{self.port}")
    
    def stop(self) -> None:
        """Останавливает сервер."""
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
        logger.info("Сервер остановлен")
    
    def _run(self) -> None:
        """Главный цикл сервера."""
        # Создаём сокет
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # SO_REUSEADDR — чтобы можно было перезапустить сразу после остановки
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self._sock.bind((self.host, self.port))
            self._sock.listen(10)  # очередь подключений
            self._sock.settimeout(1.0)  # чтобы можно было проверять _running
        except OSError as e:
            logger.error(f"Не удалось запустить сервер: {e}")
            self._running = False
            return
        
        while self._running:
            try:
                conn, addr = self._sock.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            
            # Обрабатываем каждое соединение в отдельном потоке
            threading.Thread(
                target=self._handle_client,
                args=(conn, addr),
                daemon=True,
            ).start()
    
    def _handle_client(self, conn: socket.socket, addr: tuple) -> None:
        """Обрабатывает одного клиента."""
        try:
            # Читаем запрос
            data = b""
            conn.settimeout(5.0)
            
            while b"\r\n\r\n" not in data:
                chunk = conn.recv(4096)
                if not chunk:
                    return
                data += chunk
            
            # Парсим заголовки, чтобы узнать Content-Length
            separator = b"\r\n\r\n"
            idx = data.find(separator)
            head_text = data[:idx].decode("latin-1")
            
            # Ищем Content-Length
            content_length = 0
            for line in head_text.split("\r\n"):
                if line.lower().startswith("content-length:"):
                    try:
                        content_length = int(line.split(":", 1)[1].strip())
                    except ValueError:
                        pass
            
            # Дочитываем тело, если нужно
            body_received = len(data) - idx - len(separator)
            remaining = content_length - body_received
            while remaining > 0:
                chunk = conn.recv(min(remaining, 4096))
                if not chunk:
                    break
                data += chunk
                remaining -= len(chunk)
            
            # Парсим запрос
            try:
                request = Parser.parse_request(data)
            except ParseError:
                # Невалидный запрос — 400
                resp = self._make_error_response(400, "Bad Request")
                conn.sendall(resp)
                return
            
            # Логируем
            logger.info(f"{addr[0]} {request.method} {request.path}")
            
            # Обрабатываем через роутер
            try:
                response = self.router.dispatch(request)
            except Exception as e:
                logger.error(f"Ошибка в обработчике: {e}")
                resp_bytes = self._make_error_response(500, "Internal Server Error")
                conn.sendall(resp_bytes)
                return
            
            # Отправляем ответ
            raw_response = Serializer.serialize_response(response)
            conn.sendall(raw_response)
            
        except Exception as e:
            logger.error(f"Ошибка при обработке клиента: {e}")
        finally:
            try:
                conn.close()
            except OSError:
                pass
    
    @staticmethod
    def _make_error_response(status: int, reason: str) -> bytes:
        """Создаёт простой ответ с ошибкой."""
        from ..http.response import Response
        resp = Response.from_status(status, reason.encode("utf-8"))
        return Serializer.serialize_response(resp)