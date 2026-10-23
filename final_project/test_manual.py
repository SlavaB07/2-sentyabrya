from src.http.request import Request
from src.http.response import Response

print("=== ТЕСТ REQUEST ===")
req = Request(
    method="get",
    path="echo",
    headers={"content-type": "text/plain", "HOST": "example.com"},
)
print("Метод:", req.method)
print("Путь:", req.path)
print("Заголовки:", req.headers)
print("Content-Type:", req.get_header("CONTENT-TYPE"))
print("Host:", req.get_header("host"))

req2 = Request(method="POST", path="/echo", body="hello")
print("Тело:", req2.body)
print("Тип тела:", type(req2.body))

print("\n=== ТЕСТ RESPONSE ===")
resp = Response(status=404)
print("Статус:", resp.status)
print("Причина:", resp.reason)
print("Успех?", resp.is_success())
print("Ошибка?", resp.is_error())

resp2 = Response.from_status(200, b"Hello")
print("Статус:", resp2.status)
print("Причина:", resp2.reason)
print("Тело:", resp2.body)
print("Content-Type:", resp2.get_header("content-type"))

try:
    Response(status=999)
except ValueError as e:
    print("Ошибка поймана:", e)

resp3 = Response(status=418)
print("Чайник:", resp3.reason)