from src.client.http_client import HttpClient
from src.http.exceptions import HttpError, ConnectionError, TimeoutError

client = HttpClient(timeout=10.0)

print("=== ТЕСТ 1: GET на example.com ===")
try:
    resp = client.get("http://example.com/")
    print("Статус:", resp.status)
    print("Причина:", resp.reason)
    print("Content-Type:", resp.get_header("content-type"))
    print("Длина тела:", len(resp.body))
    print("Первые 100 байт тела:", repr(resp.body[:100]))
except Exception as e:
    print(f"ОШИБКА: {type(e).__name__}: {e}")

print("\n=== ТЕСТ 2: GET на httpbin.org/get ===")
try:
    resp = client.get("http://httpbin.org/get")
    print("Статус:", resp.status)
    print("Первые 200 байт тела:", repr(resp.body[:200]))
except Exception as e:
    print(f"ОШИБКА: {type(e).__name__}: {e}")

print("\n=== ТЕСТ 3: POST на httpbin.org/post ===")
try:
    resp = client.post("http://httpbin.org/post", body=b"hello", content_type="text/plain")
    print("Статус:", resp.status)
    print("Первые 300 байт тела:", repr(resp.body[:300]))
except Exception as e:
    print(f"ОШИБКА: {type(e).__name__}: {e}")

print("\n=== ТЕСТ 4: 404 ошибка ===")
try:
    resp = client.get("http://httpbin.org/status/404")
    print("Статус:", resp.status)
except HttpError as e:
    print(f"HttpError поймана: {e}")

print("\n=== ТЕСТ 5: Неверный хост ===")
try:
    resp = client.get("http://nonexistent-domain-xyz-12345.com/")
    print("Статус:", resp.status)
except ConnectionError as e:
    print(f"ConnectionError поймана: {e}")
except Exception as e:
    print(f"Другая ошибка: {type(e).__name__}: {e}")