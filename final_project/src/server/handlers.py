"""
Обработчики (handlers) для HTTP-сервера.

Каждая функция принимает Request и возвращает Response.
"""

import json
from datetime import datetime, timezone

from ..http.request import Request
from ..http.response import Response


def handle_echo_get(req: Request) -> Response:
    """GET /echo — возвращает HTML-страницу."""
    html = "<html><body><h1>Hello from HTTP Server!</h1></body></html>"
    return Response(
        status=200,
        headers={"Content-Type": "text/html; charset=utf-8"},
        body=html.encode("utf-8"),
    )


def handle_echo_post(req: Request) -> Response:
    """POST /echo — возвращает то же тело, что прислали (эхо)."""
    # Сохраняем Content-Type из запроса, если есть
    content_type = req.get_header("Content-Type") or "text/plain"
    return Response(
        status=200,
        headers={"Content-Type": content_type},
        body=req.body,
    )


def handle_time(req: Request) -> Response:
    """GET /time — возвращает текущее время в JSON."""
    now = datetime.now(timezone.utc).isoformat()
    data = json.dumps({"time": now})
    return Response(
        status=200,
        headers={"Content-Type": "application/json; charset=utf-8"},
        body=data.encode("utf-8"),
    )


def handle_headers(req: Request) -> Response:
    """GET /headers — возвращает все заголовки запроса в JSON."""
    data = json.dumps(req.headers, indent=2)
    return Response(
        status=200,
        headers={"Content-Type": "application/json; charset=utf-8"},
        body=data.encode("utf-8"),
    )


def handle_status(req: Request) -> Response:
    """GET /status/{code} — возвращает указанный статус-код."""
    # Путь выглядит как /status/404
    parts = req.path.split("/")
    try:
        code = int(parts[-1])
    except (ValueError, IndexError):
        code = 400
    
    return Response.from_status(code, body=f"Status {code}".encode("utf-8"))


def handle_not_found(req: Request) -> Response:
    """Любой другой маршрут — 404 Not Found."""
    return Response.from_status(404, body=b"404 Not Found")