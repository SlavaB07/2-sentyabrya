import pytest
import time
from src.server.http_server import HttpServer
from src.client.http_client import HttpClient


@pytest.fixture(scope="module")
def server():
    s = HttpServer(host="127.0.0.1", port=8081)
    s.start()
    time.sleep(0.5)
    yield s
    s.stop()


def test_get_echo(server):
    client = HttpClient(timeout=2.0)
    resp = client.get("http://127.0.0.1:8081/echo")
    assert resp.status == 200
    assert b"Hello" in resp.body


def test_post_echo(server):
    client = HttpClient(timeout=2.0)
    resp = client.post("http://127.0.0.1:8081/echo", body=b"test")
    assert resp.body == b"test"


def test_404(server):
    client = HttpClient(timeout=2.0)
    with pytest.raises(Exception):  # HttpError
        client.get("http://127.0.0.1:8081/nonexistent")
