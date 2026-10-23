from src.http.request import Request
from src.http.response import Response
from src.http.parser import Parser
from src.http.serializer import Serializer

print("=== ТЕСТ: ПАРСИНГ ЗАПРОСА ===")
raw = (
    b"GET /echo HTTP/1.1\r\n"
    b"Host: localhost:8080\r\n"
    b"User-Agent: TestClient\r\n"
    b"\r\n"
)
req = Parser.parse_request(raw)
print("Метод:", req.method)
print("Путь:", req.path)
print("Версия:", req.version)
print("Заголовки:", req.headers)
print("Тело:", req.body)

print("\n=== ТЕСТ: ПАРСИНГ POST С ТЕЛОМ ===")
raw2 = (
    b"POST /echo HTTP/1.1\r\n"
    b"Host: localhost:8080\r\n"
    b"Content-Type: text/plain\r\n"
    b"Content-Length: 5\r\n"
    b"\r\n"
    b"hello"
)
req2 = Parser.parse_request(raw2)
print("Метод:", req2.method)
print("Тело:", req2.body)
print("Content-Length:", req2.get_header("content-length"))

print("\n=== ТЕСТ: ПАРСИНГ ОТВЕТА ===")
raw3 = (
    b"HTTP/1.1 200 OK\r\n"
    b"Content-Type: text/html\r\n"
    b"Content-Length: 13\r\n"
    b"\r\n"
    b"Hello, World!"
)
resp = Parser.parse_response(raw3)
print("Статус:", resp.status)
print("Причина:", resp.reason)
print("Тело:", resp.body)

print("\n=== ТЕСТ: СЕРИАЛИЗАЦИЯ ЗАПРОСА ===")
req3 = Request(
    method="GET",
    path="/time",
    headers={"Host": "localhost:8080"},
)
data = Serializer.serialize_request(req3)
print("Байты запроса:")
print(repr(data))

print("\n=== ТЕСТ: СЕРИАЛИЗАЦИЯ ОТВЕТА ===")
resp2 = Response(
    status=200,
    reason="OK",
    headers={"Content-Type": "text/plain; charset=utf-8"},
    body=b"Hello",
)
data2 = Serializer.serialize_response(resp2)
print("Байты ответа:")
print(repr(data2))

print("\n=== ТЕСТ: ROUND-TRIP (запрос -> байты -> запрос) ===")
original = Request(
    method="POST",
    path="/echo",
    headers={"Host": "localhost", "Content-Type": "text/plain"},
    body=b"test body",
)
bytes_data = Serializer.serialize_request(original)
parsed_back = Parser.parse_request(bytes_data)
print("Метод совпал:", original.method == parsed_back.method)
print("Путь совпал:", original.path == parsed_back.path)
print("Тело совпало:", original.body == parsed_back.body)

print("\n=== ТЕСТ: ОШИБКА (нет Host) ===")
try:
    Parser.parse_request(b"GET / HTTP/1.1\r\n\r\n")
except Exception as e:
    print("Ошибка поймана:", e)

print("\n=== ТЕСТ: ОШИБКА (битая request line) ===")
try:
    Parser.parse_request(b"GARBAGE\r\n\r\n")
except Exception as e:
    print("Ошибка поймана:", e)

print("\n=== ТЕСТ: ОШИБКА (тело короче Content-Length) ===")
try:
    Parser.parse_request(
        b"POST /echo HTTP/1.1\r\nHost: x\r\nContent-Length: 100\r\n\r\nshort"
    )
except Exception as e:
    print("Ошибка поймана:", e)