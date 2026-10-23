import time
from src.server.http_server import HttpServer
from src.client.http_client import HttpClient

print("=== ЗАПУСК СЕРВЕРА ===")
server = HttpServer(host="127.0.0.1", port=8080)
server.start()
time.sleep(0.5)  # даем серверу время на запуск
print("Сервер запущен на порту 8080")

client = HttpClient(timeout=5.0)
base = "http://127.0.0.1:8080"

print("\n=== ТЕСТ 1: GET /echo ===")
try:
    resp = client.get(f"{base}/echo")
    print("Статус:", resp.status)
    print("Тело:", resp.body.decode("utf-8"))
except Exception as e:
    print(f"ОШИБКА: {type(e).__name__}: {e}")

print("\n=== ТЕСТ 2: POST /echo ===")
try:
    resp = client.post(f"{base}/echo", body=b"Hello, Server!", content_type="text/plain")
    print("Статус:", resp.status)
    print("Тело:", resp.body.decode("utf-8"))
except Exception as e:
    print(f"ОШИБКА: {type(e).__name__}: {e}")

print("\n=== ТЕСТ 3: GET /time ===")
try:
    resp = client.get(f"{base}/time")
    print("Статус:", resp.status)
    print("Тело:", resp.body.decode("utf-8"))
except Exception as e:
    print(f"ОШИБКА: {type(e).__name__}: {e}")

print("\n=== ТЕСТ 4: GET /headers ===")
try:
    resp = client.get(f"{base}/headers")
    print("Статус:", resp.status)
    print("Тело:", resp.body.decode("utf-8"))
except Exception as e:
    print(f"ОШИБКА: {type(e).__name__}: {e}")

print("\n=== ТЕСТ 5: GET /status/418 ===")
try:
    resp = client.get(f"{base}/status/418")
    print("Статус:", resp.status)
except Exception as e:
    print(f"ОШИБКА: {type(e).__name__}: {e}")

print("\n=== ТЕСТ 6: GET /nonexistent (404) ===")
try:
    resp = client.get(f"{base}/nonexistent")
    print("Статус:", resp.status)
except Exception as e:
    print(f"ОШИБКА: {type(e).__name__}: {e}")

print("\n=== ОСТАНОВКА СЕРВЕРА ===")
server.stop()
time.sleep(0.5)
print("Сервер остановлен")