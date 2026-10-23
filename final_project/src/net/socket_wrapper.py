"""
SocketWrapper — обёртка над socket.socket.
"""

import socket
from typing import Optional

from ..http.exceptions import ConnectionError, TimeoutError


class SocketWrapper:
    def __init__(self):
        self._sock: Optional[socket.socket] = None
        self._connected = False
    
    def __enter__(self) -> "SocketWrapper":
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    def connect(self, host: str, port: int, timeout: float = 10.0) -> None:
        if self._sock is None:
            raise ConnectionError("Сокет не инициализирован. Используй with.")
        
        try:
            self._sock.settimeout(timeout)
            self._sock.connect((host, port))
            self._connected = True
        except socket.timeout:
            raise TimeoutError(f"Таймаут при подключении к {host}:{port} ({timeout} сек)")
        except socket.gaierror as e:
            raise ConnectionError(f"Хост не найден: {host} ({e})")
        except OSError as e:
            raise ConnectionError(f"Не удалось подключиться к {host}:{port}: {e}")
    
    def send_all(self, data: bytes) -> None:
        if not self._connected or self._sock is None:
            raise ConnectionError("Сокет не подключён")
        
        try:
            self._sock.sendall(data)
        except socket.timeout:
            raise TimeoutError("Таймаут при отправке данных")
        except OSError as e:
            raise ConnectionError(f"Ошибка при отправке: {e}")
    
    def recv(self, max_bytes: int = 4096) -> bytes:
        if not self._connected or self._sock is None:
            raise ConnectionError("Сокет не подключён")
        
        try:
            return self._sock.recv(max_bytes)
        except socket.timeout:
            raise TimeoutError("Таймаут при чтении данных")
        except OSError as e:
            raise ConnectionError(f"Ошибка при чтении: {e}")
    
    def recv_until(self, delimiter: bytes, max_bytes: int = 65536) -> bytes:
        data = b""
        while delimiter not in data:
            if len(data) > max_bytes:
                raise ConnectionError(f"Превышен лимит {max_bytes} байт при чтении заголовков")
            chunk = self.recv(4096)
            if not chunk:
                raise ConnectionError("Соединение закрыто до получения заголовков")
            data += chunk
        return data
    
    def recv_exact(self, n: int) -> bytes:
        data = b""
        while len(data) < n:
            chunk = self.recv(n - len(data))
            if not chunk:
                raise ConnectionError(f"Соединение закрыто. Получено {len(data)} из {n} байт")
            data += chunk
        return data
    
    def close(self) -> None:
        if self._sock is not None:
            try:
                self._sock.close()
            except OSError:
                pass
            finally:
                self._sock = None
                self._connected = False