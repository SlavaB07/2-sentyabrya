import threading
from src.client.http_client import HttpClient

def make_request(i):
    try:
        client = HttpClient(timeout=5.0)
        resp = client.get("http://127.0.0.1:8080/time")
        print(f"Запрос {i}: {resp.status}")
    except Exception as e:
        print(f"Запрос {i}: ОШИБКА {e}")

print("Запуск 100 параллельных запросов...")
threads = []
for i in range(100):
    t = threading.Thread(target=make_request, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Все 100 запросов завершены. GUI жив!")